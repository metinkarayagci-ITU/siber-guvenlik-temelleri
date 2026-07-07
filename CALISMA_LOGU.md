# 📋 Çalışma Logu

Bu dosya, reponun derinleştirme/genişletme turlarının ilerleme kaydını tutar. Her aşamada: hangi dosyalar değişti, hangi kavramlar eklendi/derinleştirildi, hangi ilişkiler kuruldu, hangi kaynaklar doğrulandı, hangi hatalar düzeltildi.

**Çalışma prensibi:** Kavramlar arası bağlantı düzyazı içinde ve simetriktir (X↔Y hem X'te hem Y'de). Dış iddialar satır-içi kaynakla doğrulanır. İş kesilirse bu logdan kaldığı yer görülüp sürdürülebilir.

---

## 🔶 TUR 2 — Uzman-öncesi hacker düzeyine genişletme (devam ediyor)

**Amaç:** Persona = sistemi gerçekten anlayan, sahada öğrenmiş hacker (script kiddie üstü, tek-alan uzmanı altı). Kapsam ölçütü THM değil, bu persona. Savunma tarafı (SOC/forensics/IR/malware) saldırıya göre zayıftı — dengeleniyor.

**Bilinen boşluklar (Bölüm 2 — doldurulacak):** Moniker Link/CVE-2024-21413, Hydra (online brute-force), Digital Forensics çekirdeği, Malware analiz araç/akışı, IR tam yaşam döngüsü (PICERL), zafiyet tarayıcıları (Nessus/OpenVAS/Qualys).

**Tur 2 çıktı özeti:** 4 yeni dosya (dijital-forensics, malware-analiz, olay-mudahale-ir, zafiyet-tarama), Bölüm 2'nin tüm boşlukları dolduruldu, 27 ekran görüntüsü yer tutucusu metne çevrildi (repo görsele bağımsız), sqli/mitre persona düzeyine derinleştirildi, ~26 yeni sözlük terimi, ~10 yeni kaynak. İçerik dosyası 64→68, diyagram 122→129. Tüm iç linkler geçerli, mojibake yok. Savunma tarafı (forensics/malware/IR) saldırıyla dengelendi.

### Tur 2 ilerleme

**Persona-düzeyi derinleştirme ✅ (Bölüm 3)**
- `sqli.md`: UNION-based (information_schema keşfi), blind SQLi (boolean + time-based, somut `SUBSTRING`/`SLEEP`/`IF` payload'ları), out-of-band (DNS sızdırma), WAF atlatma temel mantığı (case/comment/encoding/eşdeğer) eklendi — task'ın kalibrasyon örneği. WAF atlatma ↔ kara liste eleştirisi (enjeksiyon) + UTF-8 atlatma (00) + DNS tünelleme (01) simetrik.
- `mitre-attck.md`: T1003.001 (LSASS dumping) uçtan uca örneği (prosedür→tespit/Sysmon Event 10→azaltma/Credential Guard) + D3FEND — ATT&CK'i "katalog"dan "kullanılabilir araç"a taşıdı. LSASS ↔ 02 (kimlik saklama) + 11 (tespit).

**Bölüm 2 boşlukları — DURUM: tümü dolduruldu ✅** (Moniker Link, Hydra, forensics, malware analiz, IR/PICERL, zafiyet tarayıcıları).

**Ek persona boşlukları (Bölüm 1 kapsam kuralı) — devam ediyor:**
- **Privesc derinlemesine ✅** (kalibrasyonun açık isteği "privesc/enumerasyon derinlemesine"): yeni `10/privilege-escalation.md` — Linux (SUID/GTFOBins, sudo/LD_PRELOAD/Baron Samedit, cron wildcard/PATH, capabilities, yazılabilir /etc/passwd, NFS no_root_squash, kernel exploit) + Windows (unquoted service path, weak service perms, SeImpersonate/Potato, SeBackup/SeDebug, AlwaysInstallElevated, DLL hijacking) — her vektörün *neden* çalıştığı. somuru-ve-sonrasi §3 → bu dosyaya işaret (tekrar önleme). Simetrik: SUID/sudo/PATH ↔ 02, token/servis ↔ 02, kernel ↔ 03, savunma ↔ hardening lab.
- **Active Directory saldırıları ✅** (persona, forest tasarımı hariç): yeni `10/active-directory-saldirilari.md` — Kerberos temelli Kerberoasting/AS-REP (offline kırma bağı 05), PtH/PtT/Overpass, DCSync, Golden Ticket, BloodHound; her birinin mekanizması + savunma + tespit. Simetrik: windows-temelleri Kerberos ↔ bu dosya [iki yönlü]; Golden Ticket ↔ imza anahtarı (05); AD yanal hareket ↔ zero-trust gerekçesi (06); Moniker Link NTLM ↔ PtH.
- **Sözlük:** GTFOBins/LOLBins, unquoted service path, SeImpersonate/Potato, Kerberoasting, AS-REP, PtT, DCSync/Golden Ticket, BloodHound (9 terim).

**11-soc-mavi-takim — savunma genişletmesi ✅**
- **Yeni dosyalar:** `dijital-forensics.md`, `malware-analiz.md`, `olay-mudahale-ir.md` (savunma tarafındaki en büyük boşluklar).
- **Eklenen kavramlar:** chain of custody, order of volatility (RFC 3227), disk imaging + write blocker, canlı vs ölü analiz, Volatility bellek forensics, MAC times + timestomping (anti-forensics), file carving; statik vs dinamik malware analizi, packing/entropi, PE imports, CAPA, YARA, sandbox, INetSim/FakeNet, CyberChef/REMnux/FLARE-VM; PICERL + NIST 800-61 tam IR döngüsü (kısa/uzun containment, yeniden kurulum, out-of-band iletişim, yasal bildirim).
- **Tekrar önleme:** `log-analizi.md`'deki IR bölümü özete indirilip `olay-mudahale-ir.md`'ye işaret edildi (tam anlatım tek yerde).
- **Kurulan ilişkiler (simetrik):** forensics hash ↔ bütünlük (00/05); order of volatility ↔ RAM uçuculuğu (03); LSASS bellek kanıtı ↔ Mimikatz (02); Volatility pstree ↔ Sysmon süreç ağacı (11 log); CyberChef ↔ kodlama≠şifreleme (00) + `-enc` yükü (11 log); CAPA/YARA ↔ ATT&CK (07) + Pyramid of Pain (07); IR ↔ Kill Chain (07) + NIST CSF Respond/Recover (08) + yanal hareket (10) + zero-trust segmentasyon (06). siem-edr-soar ↔ yeni üçlü [iki yönlü].
- **Kaynaklar (satır-içi):** RFC 3227, NIST SP 800-61, Mandiant CAPA/FLARE-VM, REMnux, CyberChef (GCHQ).
- **Sözlük:** 12 yeni savunma terimi eklendi.

**10-pentest — saldırı boşlukları ✅**
- **Yeni dosya:** `zafiyet-tarama.md` (Nessus/OpenVAS/Qualys, tarama≠sömürü/yanlış pozitif, authenticated vs unauthenticated, zafiyet yönetimi döngüsü, CISA KEV önceliklendirme).
- **Eklenen kavram:** Hydra (online brute-force) + online vs offline parola saldırısı ayrımı (§1.5 somuru-ve-sonrasi), password spraying.
- **Kurulan ilişkiler (simetrik):** online (Hydra) ↔ offline kırma (05 hash lab) [iki yönlü]; offline sessizliği ↔ salt/KDF savunması (05); NTLM çalma ↔ Moniker Link (12, sıradaki); zafiyet tarama ↔ CVE/CVSS (10) + risk önceliklendirme (08) + SCA (13) + web tarayıcı (04); tarama gürültüsü ↔ log tespiti (11).
- **Kaynaklar (satır-içi):** THC-Hydra, Greenbone/OpenVAS.
- **Sözlük:** 7 yeni terim (Hydra, online/offline, spraying, credential stuffing, zafiyet tarama, auth/unauth).

**Ekran görüntüsü yer tutucuları → metinsel çıktı ✅ (Bölüm 8)**
- **27 `📸 EKRAN GÖRÜNTÜSÜ EKLENECEK` yer tutucusunun tümü** gerçekçi metinsel çıktıyla değiştirildi (nmap -sV, gobuster, reverse shell/whoami, Meterpreter/getuid, SQL hata, XSS DOM, IDOR istek/yanıt, hashcat Cracked+hız, openssl verify, ss -tulnp, ufw/fail2ban, öncesi/sonrası nmap, phishing ham başlık spf/dkim/dmarc=fail, vb.). THM not şablonundaki yer tutucular "çıktı yapıştır" kod bloklarına çevrildi.
- **Sonuç:** Repo artık görsele bağımlı değil; her dosya tek başına tam. README + nasil-calisilir güncellendi. 15 dosyada değişiklik.

**12-phishing — Moniker Link ✅**
- **Değişen dosyalar:** `phishing-analizi.md` (yeni bölüm), `windows-temelleri.md` (simetrik).
- **Eklenen kavram:** Moniker Link / CVE-2024-21413 (Outlook, `file://...!` ile Protected View atlatma → SMB'ye zorunlu bağlantı → NTLMv2 hash sızması → offline kırma / NTLM relay). Coerced authentication genel kavramı.
- **Kurulan ilişkiler (simetrik):** Moniker Link ↔ NTLM/SAM (02) [iki yönlü — windows-temelleri'ne coerced auth bölümü eklendi]; NTLM sızması ↔ offline kırma (05) + online/offline ayrımı (10 §1.5) + Pass-the-Hash/relay (02); phishing süreç zinciri ↔ log Senaryo B (11).
- **⚠️ Doğrulama:** CVE-2024-21413 CVSS puanı ve tam exploit string biçimi bu oturumda WebSearch limiti nedeniyle canlı teyit edilemedi — dosyada "doğrulanmalı" notu bırakıldı, aşağıdaki listeye eklendi.

---

## ✅ TUR 1 tamamlandı — genel özet

**16/16 modül işlendi.** Öne çıkan sonuçlar:

- **En büyük düzeltme:** `owasp-top10-tam-rehber.md` **OWASP Top 10:2025**'e göre baştan yazıldı ve bu değişiklik repo genelinde 10+ dosyadaki OWASP numara atıflarına yansıtıldı (tutarlılık).
- **PQC doğrulama (kariyer alanı):** FIPS 203/204/205 tarihleri, FIPS 206/FN-DSA taslak durumu, HQC seçimi (Mart 2025), CNSA 2.0 takvimi (2025/2030/2033) resmî kaynaklarla teyit edildi; tüm "doğrulanmalı" hedge'leri kaldırıldı.
- **THM boşlukları dolduruldu:** ARP, DHCP (DORA), MAC adresi (Modül 01); parola hash saklama SAM/LSASS + /etc/shadow simetrik (Modül 02); önyükleme/Secure Boot/TPM (Modül 00).
- **Satır-içi kaynaklar:** ~35 resmî kaynak (RFC 826/1034/1035/1918/2131/3021/4632/6376/6749/7208/7489/7519/8446/9110/9112/9293, NIST FIPS 203-206/CSF 2.0/SP 800-30/61/145/207, NSA CNSA 2.0, W3C WebAuthn, OWASP 2025/GenAI/ReDoS, MITRE, Lockheed, OASIS, FIRST CVSS, CISA, SLSA, ISO 27001).
- **Simetrik bağlantı örnekleri:** hash (00↔02↔05↔10), von Neumann/kod-veri (00↔03↔04), Secure Boot/dijital imza (00↔05), FIDO2/TPM (00↔06), SSRF/shared-responsibility (04↔09), MITM/LAN protokolleri (01 içi + 05), prompt injection/enjeksiyon (04↔15), fail-securely/OWASP A10 (13↔04).

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

### 05-kriptografi ✅
- **Değişen dosyalar:** `post-kuantum-kriptografi.md`, `anahtar-degisimi-ve-imza.md`, `pki-x509.md`, `terminoloji-sozlugu.md`
- **Doğrulanan/güncellenen gerçekler (kariyer alanı — yüksek özen):** FIPS 203/204/205 (13 Ağu 2024 sonlandı, yürürlük 14 Ağu 2024); FIPS 206/FN-DSA (FALCON, taslak 2025, final ~2026-27); HQC (Mart 2025 ek/yedek KEM, kod tabanlı); CNSA 2.0 (öncelik 2025, geçiş 2030, emeklilik 2033). Tüm "doğrulanmalı" hedge'leri kesin satır-içi kaynaklarla değiştirildi.
- **Dış kaynaklar (satır-içi):** NIST CSRC (FIPS 203/204/205 final sayfaları), DigiCert (FN-DSA), NIST PQC, NSA CNSA 2.0 PDF, RFC 8446 (TLS 1.3).
- **Kurulan ilişkiler (simetrik, 00 ile tamamlandı):** Dijital imza ↔ Secure Boot (00) [iki yönlü]; PKI güven zinciri ↔ Secure Boot güven zinciri (00); firmware imzalama ↔ CNSA 2.0 öncelik; TLS 1.3 forward secrecy ↔ HNDL.
- **Sözlük:** ML-KEM/ML-DSA/SLH-DSA, Shor/Grover, HNDL eklendi; PQC/crypto-agility güncellendi.

### 06-kimlik-erisim-yonetimi-iam ✅
- **Değişen dosyalar:** `aaa-ve-mfa.md`, `federasyon-sso.md`, `zero-trust.md`
- **Kurulan ilişkiler (simetrik, 00/05/12 ile):** FIDO2 özel anahtar donanımda saklama ↔ TPM (00) [iki yönlü, 00'daki TPM notu FIDO2'ye işaret ediyordu]; FIDO2 challenge-response ↔ dijital imza (05); FIDO2 phishing direnci ↔ AiTM phishing (12); JWT güvencesi ↔ dijital imza (05).
- **Dış kaynaklar (satır-içi):** WebAuthn=W3C, OAuth 2.0=RFC 6749, JWT=RFC 7519, Zero Trust=NIST SP 800-207.
- **Not:** Modül zaten derindi (OAuth akış diyagramı, RBAC/ABAC karşılaştırması mevcut); ana katkı simetrik bağlantı + kaynak.

### 07-tehdit-modelleme-cerceveler ✅
- **Değişen dosyalar:** `mitre-attck.md`, `cyber-kill-chain.md`, `pyramid-of-pain-diamond-model.md`, `tehdit-istihbarati-ioc-ioa.md`
- **Eklenen:** Çerçevelerin resmî köken/kaynak atıfları (ATT&CK'in açılımı da eklendi).
- **Dış kaynaklar (satır-içi):** MITRE (attack.mitre.org), Lockheed Kill Chain, Bianco Pyramid of Pain orijinal blog, OASIS STIX/TAXII.
- **Not:** Modül zaten iç-çapraz bağlantıları güçlüydü (4 çerçeve birbirine + SOC/pentest'e bağlı); ana katkı doğru atıf/kaynak.

### 08-grc-yonetisim-risk-uyum ✅
- **Değişen dosyalar:** `cerceveler-nist-iso.md`, `stride-tehdit-modelleme.md`, `risk-yonetimi.md` (+ Modül 04'te OWASP A06 düzeltmesi yapılmıştı)
- **Dış kaynaklar (satır-içi):** NIST CSF 2.0 (Şubat 2024), ISO/IEC 27001:2022, Microsoft STRIDE, NIST SP 800-30 (risk).
- **Not:** Modül zaten kontrol matrisi ↔ CIA ↔ kill chain ↔ OWASP bağlantılarıyla güçlüydü; ana katkı resmî kaynaklar.

### 09-cloud-virtualizasyon ✅
- **Değişen dosyalar:** `temel-kavramlar.md` (+ Modül 04'te container OWASP A03 düzeltmesi)
- **Eklenen:** NIST SP 800-145 bulut tanımı kaynağı; Capital One 2019 ihlali (SSRF→meta-veri→S3) somut örnek olarak eklendi ve OWASP 2025 SSRF→A01 taşınmasına bağlandı.
- **Kurulan ilişki (simetrik):** Cloud shared responsibility ↔ SSRF (04) [iki yönlü]; SSRF metadata ↔ A01 gerekçesi (04).
- **Not:** Konteyner izolasyonu ↔ OS namespaces/cgroups (03) bağı zaten mevcuttu.

### 10-pentest-metodolojisi ✅
- **Değişen dosyalar:** `somuru-ve-sonrasi.md`, `kesif-enumerasyon.md`, `metodoloji-ve-rules-of-engagement.md`
- **Dış kaynaklar (satır-içi):** CVSS=FIRST.org (v4.0), Nmap=nmap.org, PTES/OSSTMM/OWASP WSTG.
- **Kurulan ilişkiler (simetrik):** Nmap ↔ TCP handshake/port (01) + CIDR/RoE kapsam (01); CVSS ↔ risk önceliklendirme (08). Privesc/lateral ↔ SUID/sudo (02)/Kerberos (02) bağları zaten mevcuttu.
- **Not:** Modül zaten shell diyagramları, privesc enumerasyonu ile derindi.

### 11-soc-mavi-takim ✅
- **Değişen dosyalar:** `log-analizi.md`
- **Dış kaynaklar (satır-içi):** Sysmon=Microsoft Sysinternals, NIST SP 800-61 (IR), Microsoft Security auditing events.
- **Kurulan ilişkiler (simetrik):** Windows Event 4625 ↔ Linux auth.log "Failed password" (02) [iki yönlü]; Event ID'ler ↔ Windows kimlik/oturum kavramları (02); Sysmon süreç ağacı ↔ süreç soy ağacı (03) zaten mevcuttu.
- **Not:** Modül zaten TP/FP/FN, IR state diagram, 3-senaryolu lab ile derindi.

### 12-sosyal-muhendislik-phishing ✅
- **Değişen dosyalar:** `phishing-analizi.md`
- **Dış kaynaklar (satır-içi):** SPF=RFC 7208, DKIM=RFC 6376, DMARC=RFC 7489.
- **Not:** Simetrik bağlar zaten mevcuttu — DKIM↔dijital imza (05), SPF/DKIM/DMARC↔DNS TXT (01), phishing zinciri↔log-analizi Senaryo B (11), FIDO2↔AiTM (06 tarafından eklenmişti).

### 13-guvenli-kodlama-devsecops ✅
- **Değişen dosyalar:** `guvenli-kodlama-ilkeleri.md`, `devsecops-ssdlc.md` (OWASP numaraları Modül 04'te düzeltilmişti)
- **Kurulan ilişki (simetrik, yeni 2025 kategorisi):** "Güvenli başarısızlık (fail securely)" ilkesi ↔ OWASP Top 10:2025 A10 Mishandling of Exceptional Conditions (04) [iki yönlü — owasp dosyası A10→guvenli-kodlama bağlıyordu].
- **Dış kaynak (satır-içi):** SLSA (slsa.dev) tedarik zinciri çerçevesi.
- **Not:** Bellek-güvenli dil ↔ 03 bağı zaten mevcuttu.

### 14-scripting-otomasyon ✅
- **Değişen dosyalar:** `regex-referans.md` (git-temelleri OWASP numarası Modül 04'te düzeltilmişti)
- **Dış kaynak (satır-içi):** OWASP ReDoS.
- **Not:** Modül pratik ve büyük ölçüde kendine yeterliydi (çalışan örnek scriptler, Python/Bash/Git/Regex). Scriptler değiştirilmedi. Git sır sızıntısı ↔ secrets management (13), regex ↔ log analizi (11)/enjeksiyon allow-list (04) bağları zaten mevcuttu.

### 15-projeler ✅
- **Değişen dosyalar:** `spesifikasyon-sonrasi-yol-haritasi.md`, `04-web-guvenligi/zafiyet-siniflari/enjeksiyon-aileleri.md`
- **Kurulan ilişki (simetrik):** Prompt injection ↔ enjeksiyon ailesi kök nedeni (04) [iki yönlü — hem 15'te hem 04'te açıklandı]; AI Security ↔ enjeksiyon refleksi transferi.
- **Dış kaynak (satır-içi):** OWASP GenAI/LLM Top 10.
- **Not:** PQC→Architect yol haritası zaten 05'e derinlemesine bağlıydı.

---

## ⚠️ Doğrulanması gereken noktalar

Bu liste, tüm araştırmaya rağmen kesin/canlı kaynakla teyit edilemeyen (veya oturum kısıtları nedeniyle ertelenen) noktaları toplar. İçerikte de yanında "doğrulanmalı" notu vardır.

- **CVE-2024-21413 (Moniker Link):** Çekirdek mekanizma (Outlook `file://...!` ile Protected View atlatma → SMB → NTLMv2 sızması), kâşif (Check Point) ve yama ayı (Şubat 2024) bilgime dayanır; ancak **kesin CVSS taban puanı (9.8 olarak yazıldı)** ve **tam exploit string biçimi** bu oturumda WebSearch oturum limiti nedeniyle canlı teyit edilemedi. Resmî kaynak: NVD (nvd.nist.gov/vuln/detail/CVE-2024-21413) ve Check Point Research yazısı ile doğrulanmalı. Yer: `12-sosyal-muhendislik-phishing/phishing-analizi.md`.
