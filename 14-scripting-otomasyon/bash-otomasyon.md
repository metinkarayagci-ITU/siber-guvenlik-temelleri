# 🐚 Bash Otomasyon

Bash, Linux/Unix dünyasının otomasyon dilidir. Sistem yönetimi, log analizi, araç zincirleme ve hızlı görevler için vazgeçilmezdir. Bir güvenlik uzmanı Bash'i hem savunma (log işleme, sertleştirme scriptleri) hem saldırı (enumerasyon otomasyonu, reverse shell) tarafında kullanır. Bu dosya, güvenlik odaklı Bash betiklemeyi kurar.

> Komut temeli: [linux-komut-referansi.md](../02-linux-windows/linux-komut-referansi.md). Kardeş: [python-guvenlik-icin.md](python-guvenlik-icin.md), [regex-referans.md](regex-referans.md).

---

## 1. Bash betik temelleri

```bash
#!/usr/bin/env bash
# Yukarıdaki "shebang" satırı: bu dosya bash ile çalışsın der.

set -euo pipefail   # GÜVENLİ betikleme: hata olunca dur, tanımsız değişkende dur,
                    # pipe'ta hatayı yakala. Her ciddi betiğin başına koy.

# Değişkenler (= etrafında BOŞLUK YOK)
hedef="192.168.1.10"
port=80

# Kullanım (tırnak içinde — boşluk/özel karakter güvenliği)
echo "Hedef: ${hedef}:${port}"
```

| Öğe | Söz dizimi |
|-----|-----------|
| Değişken | `ad="deger"` (boşluksuz), kullan `${ad}` |
| Komut çıktısını değişkene | `sonuc=$(komut)` |
| Koşul | `if [[ $x -eq 1 ]]; then ... fi` |
| Döngü | `for i in {1..10}; do ...; done` |
| Fonksiyon | `fonk() { ...; }` |
| Argümanlar | `$1 $2 ... $@ $#` |

> **`set -euo pipefail` neden önemli:** Bir sertleştirme veya dağıtım betiği sessizce bir adımda başarısız olup devam ederse, sistemi yarı-yapılandırılmış (belki güvensiz) bırakır. Bu satır, hatada durup güvenli başarısızlığı ([guvenli-kodlama-ilkeleri.md](../13-guvenli-kodlama-devsecops/guvenli-kodlama-ilkeleri.md)) sağlar.

---

## 2. Metin işleme boru hatları (Bash'in gücü)

Bash'in asıl gücü, küçük araçları **pipe (`|`) ile zincirlemektir** ([linux-komut-referansi.md](../02-linux-windows/linux-komut-referansi.md)). Log analizinin ekmek-suyu:

```bash
# Başarısız SSH denemesi yapan IP'leri say (→ log-analizi.md)
grep "Failed password" /var/log/auth.log \
  | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' \
  | sort | uniq -c | sort -rn | head

# Bir web log'unda en çok istek yapan 10 IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head

# 404 dönen istekleri say (tarama/keşif tespiti)
grep ' 404 ' access.log | wc -l

# Belirli bir saatteki hataları filtrele
grep "03:1[0-9]:" auth.log | grep -i error
```

| Araç | İş |
|------|-----|
| `grep` | Satır filtreleme (desen) |
| `awk` | Sütun/alan işleme |
| `sed` | Bul-değiştir, akış düzenleme |
| `cut` | Sütun kesme |
| `sort`, `uniq -c` | Sıralama, tekilleştirme+sayma |
| `wc -l` | Satır sayma |
| `xargs` | Girdiyi komuta argüman yapma |

---

## 3. Örnek script: hızlı host keşfi

```bash
#!/usr/bin/env bash
# ping_tara.sh — bir /24 ağdaki canlı host'ları bulur (eğitim/izinli ağ).
# Kullanım: ./ping_tara.sh 192.168.1
# ⚠️ Yalnızca kendi/izinli ağında → 10-pentest/metodoloji-ve-rules-of-engagement.md
set -euo pipefail

onek="${1:?Kullanım: ./ping_tara.sh <ilk-3-oktet, ör. 192.168.1>}"

echo "[*] ${onek}.0/24 taranıyor..."
for son in {1..254}; do
    ip="${onek}.${son}"
    # -c1: tek paket, -W1: 1 sn zaman aşımı; arka planda paralel
    if ping -c1 -W1 "$ip" &>/dev/null; then
        echo "  [+] $ip CANLI"
    fi &
done
wait   # tüm arka plan işlerinin bitmesini bekle
echo "[*] Tarama tamamlandı."
```

---

## 4. Örnek script: mini sertleştirme denetleyici

```bash
#!/usr/bin/env bash
# hardening_kontrol.sh — temel Linux sertleştirme durumunu denetler.
# (→ 02-linux-windows/pratik-lab/linux-hardening-checklist.md)
set -uo pipefail   # pipefail ama -e yok (kontroller başarısız olabilir)

echo "=== Basit Sertleştirme Denetimi ==="

# 1. Root SSH girişi kapalı mı?
if grep -qE "^\s*PermitRootLogin\s+no" /etc/ssh/sshd_config 2>/dev/null; then
    echo "  [+] Root SSH girişi kapalı"
else
    echo "  [-] Root SSH girişi AÇIK olabilir ← kapat"
fi

# 2. UID 0 olan tek hesap root mu?
uid0=$(awk -F: '($3==0){print $1}' /etc/passwd)
if [[ "$uid0" == "root" ]]; then
    echo "  [+] Sadece root UID 0"
else
    echo "  [-] Birden fazla UID 0 hesap: $uid0 ← incele!"
fi

# 3. Dünya-yazılabilir dosyalar (ilk 5)
echo "  [i] Dünya-yazılabilir dosyalar (örnek):"
find / -xdev -type f -perm -0002 2>/dev/null | head -5 | sed 's/^/      /'

echo "=== Denetim tamamlandı ==="
```

> 📸 EKRAN GÖRÜNTÜSÜ EKLENECEK: `hardening_kontrol.sh` çıktısı (kendi lab VM'inde).

---

## 5. Zamanlama ve otomasyon (cron)

Betikleri otomatik/periyodik çalıştırma ([linux-temelleri.md](../02-linux-windows/linux-temelleri.md)):
```bash
crontab -e
# Her gün 03:00'te sertleştirme denetimi çalıştır, çıktıyı logla
0 3 * * * /opt/scripts/hardening_kontrol.sh >> /var/log/hardening.log 2>&1
```

> **Kesişim:** Cron hem savunma otomasyonu (periyodik denetim/yedek) hem saldırgan kalıcılığı ([somuru-ve-sonrasi.md](../10-pentest-metodolojisi/somuru-ve-sonrasi.md)) için kullanılır. Bir cron denetiminde beklenmedik bir girdi görmek, kalıcılık işaretidir.

---

## 6. Güvenli Bash betikleme

- **`set -euo pipefail`** her ciddi betiğin başında.
- **Değişkenleri tırnakla:** `"$degisken"` — boşluk/özel karakter enjeksiyonunu önler.
- **`eval`'den kaçın:** Kullanıcı girdisiyle `eval` = komut enjeksiyonu ([enjeksiyon-aileleri.md](../04-web-guvenligi/zafiyet-siniflari/enjeksiyon-aileleri.md)).
- **Girdi doğrula:** Betik argümanlarını (IP, dosya adı) beklenen formata karşı kontrol et.
- **Sırları koyma:** Parola/anahtarı betiğe gömme; ortam değişkeni veya güvenli dosya kullan ([guvenli-kodlama-ilkeleri.md](../13-guvenli-kodlama-devsecops/guvenli-kodlama-ilkeleri.md)).

```bash
# ❌ KÖTÜ
DB_PASS="P@ssw0rd"                  # betikte düz sır

# ✅ İYİ
DB_PASS="${DB_PASS:?Ortam değişkeni gerekli}"   # ortamdan al, yoksa dur
```

---

## 7. Bash vs Python: ne zaman hangisi?

| Kullan | Bash | Python |
|--------|------|--------|
| Hızlı komut zincirleme | ✅ | daha ağır |
| Metin/log işleme (basit) | ✅ (grep/awk) | ✅ |
| Karmaşık mantık/veri yapısı | zorlaşır | ✅ |
| API/HTTP/veri yapıları | zor | ✅ (requests) |
| Sistem yönetimi görevleri | ✅ | ✅ |
| Taşınabilirlik (Windows) | zayıf | ✅ |

> Pratik kural: Birkaç komutu zincirliyorsan Bash; mantık/veri yapısı/HTTP/çapraz platform gerekiyorsa Python ([python-guvenlik-icin.md](python-guvenlik-icin.md)).

---

## 8. Saldırı–savunma kesişimi (özet)

- **Otomasyon = ölçek:** Yüzlerce sunucuda aynı denetimi/sertleştirmeyi elle yapamazsın; Bash betiği saniyeler.
- **Aynı araç iki taraf:** Reverse shell tek satır Bash'tir ([somuru-ve-sonrasi.md](../10-pentest-metodolojisi/somuru-ve-sonrasi.md)); sertleştirme denetimi de Bash. Beceri nötr, niyet belirler.
- **Betik güvenliği önemli:** Kök yetkiyle çalışan bir sertleştirme betiğindeki bir enjeksiyon/hata, koruması gereken sistemi düşürebilir — güvenli betikleme kuralları burada da geçerli.

> **Sonraki:** [regex-referans.md](regex-referans.md).
