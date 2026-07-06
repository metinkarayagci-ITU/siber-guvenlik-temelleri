# 🧪 Pratik Lab: Log Analizi Alıştırması

> Bu bir **pratik laboratuvardır**. Aşağıda gerçekçi (uydurma ama gerçeğe yakın) bir log seti var. Amacın: bir SOC Tier 1/2 analisti gibi bu logları okuyup **saldırıyı yeniden kurmak** (reconstruct). Anki'nin kart yapmadığı "log okuma refleksi" burada gelişir.

> Ön koşul: [../log-analizi.md](../log-analizi.md) (Event ID'ler, TP/FP/FN). Komut araçları: [../../02-linux-windows/linux-komut-referansi.md](../../02-linux-windows/linux-komut-referansi.md).

**Nasıl çalış:** Her senaryoyu önce **kendin analiz et** (soruları cevapla), sonra "Çözüm"ü aç. Gerçek bir olayı çözüyormuş gibi not tut.

---

## Senaryo A — SSH Brute-Force (Linux)

Aşağıda bir sunucunun `/var/log/auth.log` parçası var:

```
Jul 02 03:14:02 web01 sshd[2011]: Failed password for invalid user admin from 45.83.x.12 port 51002 ssh2
Jul 02 03:14:03 web01 sshd[2012]: Failed password for invalid user admin from 45.83.x.12 port 51004 ssh2
Jul 02 03:14:05 web01 sshd[2013]: Failed password for root from 45.83.x.12 port 51010 ssh2
Jul 02 03:14:06 web01 sshd[2014]: Failed password for root from 45.83.x.12 port 51012 ssh2
Jul 02 03:14:08 web01 sshd[2015]: Failed password for invalid user oracle from 45.83.x.12 port 51020 ssh2
... (aynı IP'den 340 başarısız deneme, 3 dakika içinde) ...
Jul 02 03:17:44 web01 sshd[2410]: Accepted password for deploy from 45.83.x.12 port 52001 ssh2
Jul 02 03:17:59 web01 sudo[2420]:   deploy : TTY=pts/0 ; PWD=/home/deploy ; USER=root ; COMMAND=/bin/bash
```

### 🔍 Sorular (önce kendin cevapla)
1. Ne tür bir saldırı görüyorsun?
2. Saldırgan başarılı oldu mu? Hangi satır bunu gösteriyor?
3. Bu bir TP mi FP mi? Neden?
4. Saldırgan erişim sonrası ne yaptı?
5. Kill chain'in ([../../07-tehdit-modelleme-cerceveler/cyber-kill-chain.md](../../07-tehdit-modelleme-cerceveler/cyber-kill-chain.md)) hangi aşamalarını görüyorsun?

<details>
<summary><b>Çözümü göster</b></summary>

1. **SSH brute-force / password spraying** — tek IP'den (`45.83.x.12`) çok sayıda farklı kullanıcıya (`admin`, `root`, `oracle`) hızlı başarısız denemeler.
2. **Evet, başarılı oldu.** `Accepted password for deploy` satırı — 3 dakikalık denemeden sonra `deploy` hesabına giriş sağlandı.
3. **True Positive (gerçek saldırı).** 3 dakikada 340 deneme + ardından başarılı giriş, meşru kullanıcı davranışı değildir.
4. **Ayrıcalık yükseltme:** `sudo ... USER=root ... COMMAND=/bin/bash` — `deploy` kullanıcısı root shell aldı ([../../10-pentest-metodolojisi/somuru-ve-sonrasi.md](../../10-pentest-metodolojisi/somuru-ve-sonrasi.md)).
5. Delivery/Exploitation (brute-force ile erişim) → Installation/Actions (root shell). 

**Analiz komutu:**
```bash
grep "Failed password" auth.log | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn
# → 45.83.x.12 en tepede: saldırgan kaynağı
```
**Müdahale:** IP'yi engelle (fail2ban), `deploy` hesabını dondur, root shell sonrası ne yapıldığını araştır (`.bash_history`, yeni dosyalar `find -mtime -1`), kök neden: zayıf parola → parola politikası + SSH anahtar + MFA.
</details>

**Analiz komutunun çıktısı:**
```text
$ grep "Failed password" auth.log | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn
    340 45.83.x.12
      3 192.168.1.50
      1 10.0.0.8
```
`340` başarısız deneme yapan `45.83.x.12`, gürültüden anında sıyrılır — saldırgan kaynağı budur. Diğer IP'lerin 1-3 denemesi normal kullanıcı hatasıdır (yanlış parola). Bu "sayıp sıralama" tekniği, log analizinin en temel refleksidir.

---

## Senaryo B — Şüpheli Süreç Zinciri (Windows/Sysmon)

Sysmon Event ID 1 (süreç oluşturma) logları (sadeleştirilmiş):

```
EventID 1 | Image: C:\...\OUTLOOK.EXE       | Parent: explorer.exe
EventID 1 | Image: C:\...\WINWORD.EXE        | Parent: OUTLOOK.EXE     | CommandLine: "...fatura_2026.docm"
EventID 1 | Image: C:\Windows\System32\cmd.exe | Parent: WINWORD.EXE
EventID 1 | Image: C:\...\powershell.exe      | Parent: cmd.exe        | CommandLine: powershell -enc SQBFAFgA...
EventID 3 | Image: powershell.exe             | Dest: 185.220.x.7:443  (giden bağlantı)
```

### 🔍 Sorular
1. Bu süreç zincirinde anormal olan ne?
2. Hangi başlangıç erişim (initial access) yöntemi kullanılmış olabilir?
3. `powershell -enc SQBFAFgA...` ne anlama geliyor?
4. Event ID 3 neyi gösteriyor ve neden önemli?
5. Bu bir IOC mu IOA mı tespiti?

<details>
<summary><b>Çözümü göster</b></summary>

1. **Word'ün (WINWORD.EXE) cmd.exe → powershell.exe başlatması anormaldir.** Bir belge neden komut satırı açsın? Bu klasik makro-tabanlı saldırı süreç zinciridir ([../log-analizi.md](../log-analizi.md) süreç soy ağacı).
2. **Phishing + makrolu belge** — Outlook → Word (`.docm` = makro etkin belge) → makro çalıştı → cmd/powershell ([../../12-sosyal-muhendislik-phishing/phishing-analizi.md](../../12-sosyal-muhendislik-phishing/phishing-analizi.md)).
3. `-enc` = **encoded command** (Base64). `SQBFAFgA...` çözülürse muhtemelen `IEX` (indir-çalıştır) ([../../02-linux-windows/windows-komut-referansi.md](../../02-linux-windows/windows-komut-referansi.md)). Saldırgan gerçek komutu gizlemek için kodlamış — ama kodlama şifreleme değil, çözülebilir.
4. **Event ID 3 = ağ bağlantısı.** PowerShell'in `185.220.x.7:443`'e bağlanması → muhtemelen **C2 (komuta-kontrol)** kanalı ([../../07-tehdit-modelleme-cerceveler/cyber-kill-chain.md](../../07-tehdit-modelleme-cerceveler/cyber-kill-chain.md) C2 aşaması). Kritik, çünkü artık makine dışarıdan kontrol ediliyor.
5. **IOA (Indicator of Attack)** — davranış temelli tespit ([../../07-tehdit-modelleme-cerceveler/tehdit-istihbarati-ioc-ioa.md](../../07-tehdit-modelleme-cerceveler/tehdit-istihbarati-ioc-ioa.md)). Dosya hash'i (IOC) değişse bile, "Word→PowerShell→ağ" davranışı saldırıyı ele verir.

**Çözülmüş komut:** `SQBFAFgA` Base64'te `IEX` demektir:
```bash
echo 'SQBFAFgA' | base64 -d   # (UTF-16 nedeniyle tam çözüm için iconv gerekir) → "IEX"
```
**Müdahale:** Host'u izole et (EDR), C2 IP'sini engelle, kodlanmış PowerShell'i tam çöz, kurbanı ve benzer e-postaları bul, makroları GPO ile kısıtla.
</details>

---

## Senaryo C — Log Temizleme (kanıt karartma)

```
EventID 4624 | Account: jsmith  | Logon Type 10 (RDP) | Source: 10.0.0.55 | 02:03
EventID 4672 | Account: jsmith  | Special privileges assigned | 02:03
EventID 4688 | New Process: net.exe user backup_svc P@ss! /add | 02:05
EventID 4720 | A user account was created: backup_svc | 02:05
EventID 4732 | Member added to Administrators group: backup_svc | 02:06
EventID 1102 | The audit log was cleared | Account: jsmith | 02:08
```

### 🔍 Sorular
1. Olayları zaman sırasına göre bir saldırı anlatısına çevir.
2. En kritik/alarm verici Event ID hangisi ve neden?
3. Saldırgan hangi kalıcılık yöntemini kurdu?

<details>
<summary><b>Çözümü göster</b></summary>

1. **Anlatı:** `jsmith` hesabı RDP ile (Type 10) uzaktan giriş yaptı (02:03) → ayrıcalıklı oturum (4672) → yeni bir hesap oluşturdu `backup_svc` (4688 + 4720, meşru görünen isim!) → bu hesabı **Administrators grubuna** ekledi (4732 — ayrıcalık yükseltme + kalıcılık) → sonra **denetim logunu temizledi** (1102, iz karartma).
2. **1102 (log temizlendi)** en alarm verici — meşru yöneticiler rutin olarak logları temizlemez. Bu, aktif bir saldırganın **iz karartma (defense evasion)** işaretidir. Ayrıca `backup_svc` gibi "meşru görünen" backdoor hesabı da yüksek şüphe ([../log-analizi.md](../log-analizi.md)).
3. **Backdoor admin hesabı** (`backup_svc`) — yeniden giriş için kalıcılık. Ayrıca `jsmith` hesabı ele geçirilmiş olabilir (kimlik hırsızlığı).

**Ders — merkezî log neden kritik:** Saldırgan yerel logu temizledi (1102) ama loglar zaten SIEM'e ([../siem-edr-soar.md](../siem-edr-soar.md)) gönderildiyse, kanıt orada duruyor. Yerel silme işe yaramaz. Bu, "logları merkezîleştir" savunmasının ([../../02-linux-windows/pratik-lab/linux-hardening-checklist.md](../../02-linux-windows/pratik-lab/linux-hardening-checklist.md)) neden hayati olduğunu gösterir.
</details>

---

## Kendi lab'ını kur (ileri)

Gerçek log üretmek ve analiz etmek için:
1. Bir Windows VM'e **Sysmon** kur (`sysmon -i sysmonconfig.xml` — SwiftOnSecurity config popüler).
2. Zararsız test aktiviteleri yap (PowerShell komutları, yeni kullanıcı) ve Event Viewer'da izle.
3. **Wazuh** veya **ELK** (açık kaynak SIEM → [../siem-edr-soar.md](../siem-edr-soar.md)) kurup logları merkezîleştir, kendi korelasyon kuralını yaz.
4. Bir TryHackMe "SOC/Blue Team" odası ([../../10-pentest-metodolojisi/pratik-lab/tryhackme-oda-notlari-sablonu.md](../../10-pentest-metodolojisi/pratik-lab/tryhackme-oda-notlari-sablonu.md)) çöz.

**Ne gözlemlenir:** Wazuh/ELK panelinde, ürettiğin test aktiviteleri kurallarla eşleşip uyarı (alert) olarak listelenir — ör. "Multiple authentication failures" (kural seviyesi 10, kaynak IP, zaman) veya "Windows: New user created" (Event 4720). SIEM'in değeri budur: tek tek loglar yerine, korelasyon kurallarının ürettiği önceliklendirilmiş uyarıları görürsün ([../siem-edr-soar.md](../siem-edr-soar.md)).

---

## Öğrenme köprüsü

Bu alıştırma, saldırgan bilgisini ([10-pentest](../../10-pentest-metodolojisi/somuru-ve-sonrasi.md)) savunmacı gözüyle **tersinden okumayı** öğretir: her saldırı adımı bir log izi bırakır; analistin işi o izleri saldırı anlatısına çevirmektir. Bir saldırıyı bilmeden onun logunu okuyamazsın — bu yüzden kırmızı ve mavi takım birbirini besler.

> **Modül 11 tamamlandı.** Sonraki: [../../12-sosyal-muhendislik-phishing/phishing-analizi.md](../../12-sosyal-muhendislik-phishing/phishing-analizi.md).
