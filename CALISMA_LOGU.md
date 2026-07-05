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

### 03-isletim-sistemi-ici
- **Durum:** ⏳ sırada
