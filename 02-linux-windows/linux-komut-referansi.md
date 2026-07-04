# 📟 Linux Komut Referansı

Kategorize edilmiş, güvenlik odaklı bir Linux komut referansı. Amaç ezber değil, **elinin altında bir başvuru** olması. Her kategoride en sık kullanılan komutlar ve güvenlikte ne işe yaradıkları vardır.

> Kavramsal temel: [linux-temelleri.md](linux-temelleri.md). Otomasyon için: [14-scripting/bash-otomasyon.md](../14-scripting-otomasyon/bash-otomasyon.md).

---

## 1. Gezinme ve dosya işlemleri

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `pwd` | Bulunulan dizin | `pwd` |
| `ls -la` | Gizli dahil tüm dosyalar + izinler | `ls -la /etc` |
| `cd` | Dizin değiştir | `cd /var/log` |
| `cp`, `mv`, `rm` | Kopyala, taşı/adlandır, sil | `rm -rf dizin/` (dikkat!) |
| `mkdir -p`, `rmdir` | Dizin oluştur/sil | `mkdir -p a/b/c` |
| `ln -s` | Sembolik link | `ln -s /gerçek /link` |
| `touch` | Boş dosya / zaman damgası | `touch dosya` |
| `stat` | Dosya meta verisi (zaman, izin, inode) | `stat dosya` |
| `file` | Dosya türünü içeriğe göre tespit | `file suphe.bin` |

> 🔍 `stat` ve `file`, adli analizde (bir dosya gerçekten ne, ne zaman değişti?) kritiktir.

---

## 2. Metin okuma, arama, işleme

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `cat`, `less`, `head`, `tail` | Dosya içeriği görüntüle | `tail -f /var/log/syslog` |
| `grep` | Desen ara (regex) | `grep -ri "password" /etc` |
| `find` | Dosya bul (isim, izin, zaman) | `find / -name "*.conf" 2>/dev/null` |
| `awk` | Sütun/alan işleme | `awk -F: '{print $1}' /etc/passwd` |
| `sed` | Akış düzenleme (bul-değiştir) | `sed 's/eski/yeni/g' d.txt` |
| `cut`, `sort`, `uniq`, `wc` | Kesme, sıralama, tekilleştirme, sayma | `sort log \| uniq -c \| sort -rn` |
| `xargs` | Girdiyi komuta argüman yap | `find . -name '*.log' \| xargs grep hata` |
| `tr` | Karakter çevirisi | `echo ABC \| tr A-Z a-z` |

> `grep`, `awk`, `sed`, `cut`, `sort`, `uniq` — log analizinin (regex referansı: [14-scripting/regex-referans.md](../14-scripting-otomasyon/regex-referans.md)) ekmek-su komutlarıdır. Örnek: en çok başarısız giriş denemesi yapan IP'yi bulmak:
> ```bash
> grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head
> ```

---

## 3. İzin ve sahiplik

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `chmod` | İzin değiştir | `chmod 640 dosya` |
| `chown` | Sahip/grup değiştir | `chown root:root dosya` |
| `umask` | Yeni dosya varsayılan izni | `umask 077` |
| `getfacl`/`setfacl` | Gelişmiş ACL (POSIX) | `getfacl dosya` |
| `find / -perm -4000` | SUID'li dosyaları bul | privilege escalation enumerasyonu |

---

## 4. Kullanıcı ve yetki

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `whoami`, `id` | Ben kimim / UID-GID-gruplar | `id` |
| `su`, `sudo` | Kullanıcı değiştir / yetki yükselt | `sudo -l` |
| `useradd`, `passwd`, `usermod` | Kullanıcı yönetimi | `useradd -m ali` |
| `w`, `who`, `last` | Oturum açanlar / giriş geçmişi | `last -a` |
| `groups` | Üyesi olunan gruplar | `groups metin` |

> `id`, `whoami`, `sudo -l`, `groups` — bir sisteme erişince "neyim, ne yapabilirim?" sorusunun ilk cevabı. Bir shell aldıktan sonra çalıştırılan ilk komutlardır.

---

## 5. Süreç ve kaynak

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `ps aux` | Tüm süreçler | `ps aux \| grep nginx` |
| `top`, `htop` | Canlı süreç izleme | `htop` |
| `kill`, `killall`, `pkill` | Süreç sonlandır | `kill -9 1234` |
| `nice`, `renice` | Öncelik ayarı | — |
| `free -h`, `df -h`, `du -sh` | Bellek / disk kullanımı | `du -sh /var/*` |
| `lsof` | Açık dosyalar/portlar | `lsof -i :80` |
| `uptime` | Sistem çalışma süresi + yük | `uptime` |

---

## 6. Ağ

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `ip a` / `ifconfig` | Arayüz/IP bilgisi | `ip a` |
| `ip r` / `route` | Yönlendirme tablosu | `ip r` |
| `ss -tulnp` / `netstat -tulnp` | Dinleyen portlar + süreç | `ss -tulnp` |
| `ping`, `traceroute` | Erişilebilirlik / yol | `ping -c4 8.8.8.8` |
| `dig`, `nslookup`, `host` | DNS sorgusu | `dig ornek.com` |
| `curl`, `wget` | HTTP istek / dosya indir | `curl -I https://ornek.com` |
| `nc` (netcat) | "TCP/IP çakısı": bağlan, dinle, aktar | `nc -lvnp 4444` |
| `tcpdump` | Paket yakalama | `tcpdump -i eth0 port 80` |

> 🔑 `ss -tulnp` (hangi servis hangi portu dinliyor) ve `nc` (ters kabuk, banner grabbing, veri aktarımı) güvenlikte en çok kullanılan iki komuttur. `nc -lvnp 4444` klasik bir ters kabuk dinleyicisidir → [somuru-ve-sonrasi.md](../10-pentest-metodolojisi/somuru-ve-sonrasi.md).

---

## 7. Paket, servis, zamanlama

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `apt`/`dnf`/`yum`/`pacman` | Paket yöneticisi | `apt install nmap` |
| `systemctl` | Servis yönetimi | `systemctl status ssh` |
| `journalctl` | systemd logları | `journalctl -u nginx -f` |
| `crontab -l/-e` | Zamanlanmış görevler | `crontab -l` |
| `at` | Tek seferlik zamanlama | `at now + 5 min` |

> **Kesişim:** `crontab -l`, `/etc/crontab`, `/etc/cron.d/` — hem yönetici otomasyonu hem saldırgan kalıcılığı burada yaşar. Yazılabilir bir cron script'i = zamanlanmış root kodu.

---

## 8. Arşiv, sıkıştırma, transfer

| Komut | Açıklama | Örnek |
|-------|----------|-------|
| `tar` | Arşivle/aç | `tar -czvf yedek.tar.gz dizin/` |
| `gzip`/`gunzip`, `zip`/`unzip` | Sıkıştır/aç | `unzip veri.zip` |
| `scp`, `rsync` | Güvenli/verimli transfer | `scp dosya user@host:/yol` |
| `ssh` | Uzak güvenli kabuk | `ssh -i anahtar user@host` |
| `base64`, `md5sum`, `sha256sum` | Kodlama / hash doğrulama | `sha256sum imaj.iso` |

> `sha256sum` ile indirilen bir dosyanın bütünlüğü doğrulanır (yayınlanan hash ile karşılaştır). `scp`/`rsync` pentest'te veri sızdırma (exfiltration) için de kullanılır.

---

## 9. Hızlı kombinasyonlar (tek satırlık güç)

```bash
# En çok CPU tüketen 5 süreç
ps aux --sort=-%cpu | head -6

# Bir dizinde son 24 saatte değişen dosyalar (adli analiz)
find /var/www -type f -mtime -1

# Dinleyen tüm servisleri ve süreçlerini listele
sudo ss -tulnp

# Bir IP'ye giden başarısız SSH denemelerini say
grep "Failed password" /var/log/auth.log | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq -c | sort -rn

# Sistemdeki tüm SUID binary'leri (privesc enumerasyonu)
find / -perm -4000 -type f 2>/dev/null
```

> **Sonraki:** [windows-temelleri.md](windows-temelleri.md).
