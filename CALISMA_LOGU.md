# 📋 Çalışma Logu (Derinleştirme ve Bağlama Turu)

Bu dosya, reponun "tam kapsamlı hale getirme ve kavramlar arası bağlantı kurma" turunun ilerleme kaydını tutar. Her modül işlendiğinde: hangi dosyalar değişti, hangi kavramlar eklendi/genişletildi, hangi ilişkiler kuruldu, hangi dış kaynaklar doğrulandı.

**Çalışma prensibi:** Modüller README sırasıyla (00 → 15) işlenir, her modül sonunda ayrı commit atılır. Kavramlar arası bağlantı düzyazı içinde ve simetriktir (X↔Y hem X'te hem Y'de). Dış iddialar satır-içi kaynakla doğrulanır.

---

## İlerleme

### 00-baslangic ✅
- **Değişen dosyalar:** `bilgisayar-temelleri.md`, `terminoloji-sozlugu.md`
- **Eklenen/genişletilen kavramlar:** Von Neumann darboğazı ve "kod/veri ayrılmaması" birleştirici teması; önyükleme (boot) zinciri, firmware (UEFI/BIOS), bootkit, Secure Boot, TPM, güven zinciri (chain of trust); UTF-8 çok-byte yapısı ve WAF atlatma bağlantısı.
- **Kurulan ilişkiler:** von Neumann → buffer overflow (03) + enjeksiyon (04) + Spectre (03); UTF-8 → WAF atlatma (04); hash → kripto (05) + SAM/shadow (02) + hashdump/John (10); Secure Boot → dijital imza (05); TPM → FIDO2 (06); güven zinciri → PKI (05); kernel/user → syscall (03) + Linux/Windows (02).
- **Dış kaynak:** UTF-8 için RFC 3629 satır-içi alıntılandı.
- **Sözlük:** "Sistem ve donanım temelleri" kategorisi eklendi (7 yeni terim).
- **Not:** Simetrik ters bağlantılar (ör. 03'te von Neumann'a, 05'te Secure Boot'a geri değinme) ilgili modüller işlenirken tamamlanacak.

### 01-ag-networking ✅
- **Değişen dosyalar:** `temel-kavramlar.md`, `tcp-ip-protokoller.md`, `subnetting-cidr.md`, `dns-derinlemesine.md`, `http-web-iletisimi.md`, `terminoloji-sozlugu.md`
- **Eklenen kavramlar (THM "Intro to LAN" boşlukları):** MAC adresi (IP vs MAC ayrımı, MAC spoofing), ARP (IP→MAC çözümleme, ARP request/reply sequence diyagramı, ARP zehirleme), DHCP (DORA süreci sequence diyagramı, sahte DHCP). MITM kavramı merkezî olarak tanımlandı ve ağ katmanı saldırılarına bağlandı.
- **Kurulan ilişkiler (simetrik):** ARP zehirleme ↔ MITM ↔ TLS/PKI (05); rogue DHCP ↔ rogue RA/IPv6 (aynı "kimlik doğrulamayan LAN protokolü istismarı" teması); MAC hex ↔ bilgisayar-temelleri (00); DHCP ↔ DNS/subnetting; SLAAC ↔ DHCP.
- **Dış kaynaklar (satır-içi):** TCP=RFC 9293, ARP=RFC 826, DHCP=RFC 2131, /31=RFC 3021, RFC 1918, CIDR=RFC 4632, DNS=RFC 1034/1035, HTTP=RFC 9110/9112.
- **Sözlük:** MAC, ARP, DHCP, MITM eklendi.

### 02-linux-windows ✅
- **Değişen dosyalar:** `linux-temelleri.md`, `windows-temelleri.md`, `terminoloji-sozlugu.md`
- **Eklenen/genişletilen:** Linux parola hash saklama (`/etc/shadow`, `$6$`/`$y$`, salt); Windows kimlik saklama (SAM, LSASS, NTLM hash), Pass-the-Hash.
- **Kurulan ilişkiler (task'ın "hash" örneği — 3 modül simetrik):** `/etc/shadow` ↔ SAM/LSASS ↔ hash tanımı (00) ↔ kripto salt/KDF (05) ↔ hashdump/John kırma (10) + hash_kirma lab (05). NTLM salt'sızlığı ↔ rainbow table (05). LSASS dump ↔ SeDebugPrivilege (03).
- **Sözlük:** SAM/LSASS, NTLM hash, Pass-the-Hash eklendi.

### 03-isletim-sistemi-ici ✅
- **Değişen dosyalar:** `surecler-ve-bellek.md`, `bellek-zafiyetleri-giris.md`
- **Kurulan ilişkiler (simetrik, 00 ile):** Spectre/Meltdown ↔ von Neumann darboğazı/bellek hiyerarşisi (00) — performans optimizasyonunun güvenlik zayıflığına dönüşmesi; buffer overflow "kod/veri karışması" ↔ von Neumann mimarisi (00) + enjeksiyon (04). Bellek-güvenli dil ↔ güvenli kodlama (13).
- **Dış kaynak:** CISA/NSA "Memory Safe Roadmaps" satır-içi alıntılandı.
- **Not:** Modül zaten derindi; ana katkı simetrik ters bağlantılar ve kaynak.

### 04-web-guvenligi ✅
- **Önemli düzeltme:** `owasp-top10-tam-rehber.md` **OWASP Top 10:2025**'e göre baştan yazıldı (önceki 2021 idi). Yeni sıralama, 2021→2025 değişim tablosu, yeni A10 (Mishandling of Exceptional Conditions), SSRF'in A01'e taşınması, A03 Supply Chain. Resmî kaynak (owasp.org/Top10/2025) satır-içi alıntılandı.
- **Repo genelinde tutarlılık:** Eski OWASP numaraları düzeltildi — sqli (A03→A05), temel-kavramlar+hash_kirma (A02→A04), stride+guvenli-kodlama (A04→A06), devsecops+container+guvenli-kodlama (A06→A03 supply chain), git-temelleri+juice-shop (A02/A05→A02/A04). 8 dosyada güncelleme.
- **Kurulan ilişki (simetrik):** csrf-ssrf'te SSRF↔A01 açıklaması güncellendi (SSRF = erişim kontrolü ihlali). Enjeksiyon↔buffer overflow (03) kök neden bağı A05 bölümünde pekiştirildi.
- **Sözlük:** OWASP Top 10 / SQLi / XSS / SSRF girişleri 2025'e güncellendi.
- **Not:** Web deep-dive dosyaları (sqli/xss/csrf-ssrf/idor/enjeksiyon) zaten PoC+önleme koduyla derindi; içerik korundu, yalnızca OWASP eşlemesi güncellendi.

### 05-kriptografi
- **Durum:** ⏳ sırada
