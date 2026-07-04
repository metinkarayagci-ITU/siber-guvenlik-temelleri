# 📖 Terminoloji Sözlüğü

Bu dosya, tüm repodaki teknik terimlerin **tek merkezî tanım kaynağıdır**. Diğer dosyalar bir terimi ilk kullandığında gerektiğinde buraya link verir. Terimler kategorilere ayrıldı; kategori içinde alfabetik/kavramsal sıralıdır.

**Dil kuralı:** İngilizce terim korunur, yanında Türkçe karşılık verilir. Bir kısaltmayı çalışma boyunca hangi biçimde kullandığımız burada sabitlenir (ör. "en az ayrıcalık" = least privilege, kısaltmasız).

---

## Genel güvenlik ilkeleri

| Terim | Tanım |
|-------|-------|
| **CIA üçlüsü** | Gizlilik (Confidentiality), Bütünlük (Integrity), Erişilebilirlik (Availability). Bilgi güvenliğinin üç temel hedefi. Bkz. [08-grc](../08-grc-yonetisim-risk-uyum/guvenlik-kontrolleri-matrisi.md). |
| **AAA** | Kimlik doğrulama (Authentication), Yetkilendirme (Authorization), Hesap verebilirlik/kayıt (Accounting). Bkz. [06-iam](../06-kimlik-erisim-yonetimi-iam/aaa-ve-mfa.md). |
| **Kimlik doğrulama (authentication)** | "Kim olduğunu" kanıtlama. Faktörler: bildiğin (parola), sahip olduğun (token), olduğun (biyometri). |
| **Yetkilendirme (authorization)** | Doğrulanmış kimliğin "neye erişebileceğini" belirleme. |
| **En az ayrıcalık (least privilege)** | Bir özneye görevini yapması için gereken **asgari** yetkiyi verme ilkesi. İhlalin etki alanını daraltır. |
| **Derinlemesine savunma (defense in depth)** | Tek bir kontrole güvenmeyip katmanlı savunma kurma. Bir katman düşse diğeri tutar. |
| **Saldırı yüzeyi (attack surface)** | Bir sistemin dışarıya açık, saldırılabilir tüm giriş noktalarının toplamı. |
| **Sıfır güven (zero trust)** | "Asla güvenme, her zaman doğrula." Ağ konumuna göre örtük güven vermeme. Bkz. [zero-trust.md](../06-kimlik-erisim-yonetimi-iam/zero-trust.md). |
| **Reddedilemezlik (non-repudiation)** | Bir eylemi yapanın onu inkâr edememesi (ör. dijital imza ile). |

## Zafiyet ve tehdit terminolojisi

| Terim | Tanım |
|-------|-------|
| **Zafiyet (vulnerability)** | Bir sistemdeki, istismar edilebilir güvenlik zayıflığı. |
| **Tehdit (threat)** | Bir zafiyeti istismar edebilecek potansiyel tehlike/aktör. |
| **Risk** | Bir tehdidin bir zafiyeti istismar etme olasılığı × etkisi. Bkz. [risk-yonetimi.md](../08-grc-yonetisim-risk-uyum/risk-yonetimi.md). |
| **İstismar/sömürü (exploit)** | Bir zafiyeti fiilen kullanan kod veya teknik. |
| **Payload (yük)** | Sömürü başarılı olduktan sonra çalışan asıl kod (ör. ters kabuk açan kısım). |
| **CVE** | Common Vulnerabilities and Exposures — bilinen zafiyetlere verilen küresel kimlik (ör. `CVE-2021-44228`). |
| **CVSS** | Common Vulnerability Scoring System — bir zafiyetin ciddiyetini 0–10 arası puanlayan sistem. Bkz. [somuru-ve-sonrasi.md](../10-pentest-metodolojisi/somuru-ve-sonrasi.md). |
| **Sıfır-gün (zero-day)** | Satıcının henüz bilmediği/yamalamadığı, kamuya açık olmayan zafiyet. |
| **IOC / IOA** | Ele geçirilme göstergesi (Indicator of Compromise) / saldırı göstergesi (Indicator of Attack). Bkz. [tehdit-istihbarati](../07-tehdit-modelleme-cerceveler/tehdit-istihbarati-ioc-ioa.md). |
| **TTP** | Taktikler, Teknikler ve Prosedürler — bir saldırganın davranış imzası. Bkz. [MITRE ATT&CK](../07-tehdit-modelleme-cerceveler/mitre-attck.md). |

## Ağ (networking)

| Terim | Tanım |
|-------|-------|
| **OSI modeli** | Ağ iletişimini 7 katmana ayıran referans model. Bkz. [temel-kavramlar.md](../01-ag-networking/temel-kavramlar.md). |
| **Paket / çerçeve / segment** | Sırasıyla katman-3 (IP), katman-2 (Ethernet), katman-4 (TCP) veri birimleri. |
| **TCP / UDP** | Güvenilir-bağlantılı (TCP) vs hızlı-bağlantısız (UDP) taşıma protokolleri. Bkz. [tcp-ip-protokoller.md](../01-ag-networking/tcp-ip-protokoller.md). |
| **Port** | Bir IP adresindeki servisi belirleyen 16-bit numara (0–65535). |
| **CIDR** | Classless Inter-Domain Routing — `IP/önek` gösterimi (ör. `10.0.0.0/8`). Bkz. [subnetting-cidr.md](../01-ag-networking/subnetting-cidr.md). |
| **Önek (prefix)** | CIDR'da kaç bitin ağ kısmı olduğu (`/24` = 24 bit ağ). |
| **Subnet mask (alt ağ maskesi)** | Adresin ağ ve host bitlerini ayıran maske (`255.255.255.0`). Adresin *parçası değildir*, yorumlanışını belirler. |
| **Ağ adresi / broadcast adresi** | Alt ağın ilk (host bitleri tümü 0) ve son (tümü 1) adresi; host'a atanamaz. |
| **VLSM** | Değişken uzunlukta alt ağ maskeleme (Variable Length Subnet Masking). |
| **NAT / PAT** | Ağ/port adres çevirisi — özel IP'leri tek genel IP'ye çevirme. Bkz. [routing-nat-vpn.md](../01-ag-networking/routing-nat-vpn.md). |
| **DNS** | Alan adı → IP çözümleme sistemi. Bkz. [dns-derinlemesine.md](../01-ag-networking/dns-derinlemesine.md). |
| **VLAN** | Sanal LAN — tek fiziksel ağı mantıksal bölme. |
| **VPN** | Sanal özel ağ — güvenilmeyen ağ üzerinden şifreli tünel. |

## Kriptografi

| Terim | Tanım |
|-------|-------|
| **Simetrik şifreleme** | Aynı anahtarla şifreleme+çözme (AES). Hızlı. |
| **Asimetrik şifreleme** | Açık/özel anahtar çifti (RSA, ECC). Yavaş ama anahtar dağıtımını çözer. |
| **Hash** | Tek yönlü, sabit uzunlukta parmak izi (SHA-256). Bkz. [temel-kavramlar.md](../05-kriptografi/temel-kavramlar.md). |
| **Salt / pepper** | Hash'e eklenen rastgele (salt) / gizli (pepper) değer; rainbow table saldırısını kırar. |
| **KDF** | Anahtar türetme fonksiyonu (Argon2, bcrypt, PBKDF2) — paroladan yavaşça anahtar üretir. |
| **HMAC** | Hash tabanlı mesaj doğrulama kodu — bütünlük + kimlik. |
| **AEAD** | Kimliği doğrulanmış şifreleme (Authenticated Encryption with Associated Data) — gizlilik + bütünlük tek işlemde (AES-GCM, ChaCha20-Poly1305). |
| **DH / ECDH** | Diffie-Hellman anahtar değişimi — güvensiz kanalda ortak sır üretme. Bkz. [anahtar-degisimi-ve-imza.md](../05-kriptografi/anahtar-degisimi-ve-imza.md). |
| **PKI / X.509** | Açık anahtar altyapısı ve sertifika standardı. Bkz. [pki-x509.md](../05-kriptografi/pki-x509.md). |
| **CA** | Sertifika Yetkilisi (Certificate Authority) — sertifikaları imzalayan güvenilen taraf. |
| **PQC** | Post-kuantum kriptografi — kuantum bilgisayara dayanıklı algoritmalar. Bkz. [post-kuantum-kriptografi.md](../05-kriptografi/post-kuantum-kriptografi.md). |
| **Kripto çevikliği (crypto-agility)** | Kullanılan algoritmayı sistemi baştan yazmadan değiştirebilme yeteneği. |

## Kimlik ve erişim (IAM)

| Terim | Tanım |
|-------|-------|
| **MFA / 2FA** | Çok/iki faktörlü kimlik doğrulama. |
| **TOTP / HOTP** | Zaman/sayaç tabanlı tek kullanımlık parola. |
| **FIDO2 / WebAuthn** | Kimlik avına (phishing) dayanıklı, açık anahtar tabanlı kimlik doğrulama. |
| **SSO** | Tek oturum açma (Single Sign-On). |
| **OAuth 2.0 / OIDC** | Yetkilendirme (OAuth) ve üstüne kimlik katmanı (OpenID Connect) protokolleri. Bkz. [federasyon-sso.md](../06-kimlik-erisim-yonetimi-iam/federasyon-sso.md). |
| **SAML** | XML tabanlı federasyon/SSO protokolü (kurumsal). |
| **JWT** | JSON Web Token — imzalı, taşınabilir kimlik/talep (claim) taşıyıcısı. |
| **RBAC / ABAC / DAC / MAC** | Rol / öznitelik / isteğe bağlı / zorunlu erişim kontrol modelleri. Bkz. [erisim-kontrol-modelleri.md](../06-kimlik-erisim-yonetimi-iam/erisim-kontrol-modelleri.md). |

## Web güvenliği

| Terim | Tanım |
|-------|-------|
| **OWASP Top 10** | En kritik web zafiyetlerinin standart listesi. Bkz. [owasp-top10-tam-rehber.md](../04-web-guvenligi/owasp-top10-tam-rehber.md). |
| **SQLi** | SQL enjeksiyonu — girdi ile veritabanı sorgusunu değiştirme. |
| **XSS** | Siteler-arası betik çalıştırma (Cross-Site Scripting). |
| **CSRF / SSRF** | Siteler-arası istek sahteciliği / sunucu-taraflı istek sahteciliği. |
| **IDOR** | Güvensiz doğrudan nesne referansı — yetki kontrolü eksik ID erişimi. |
| **SOP / CORS** | Aynı köken politikası ve onu gevşeten paylaşım mekanizması. |
| **CSP** | İçerik güvenlik politikası (Content Security Policy) — XSS azaltma başlığı. |
| **WAF** | Web uygulama güvenlik duvarı. |

## Saldırgan / savunmacı operasyon

| Terim | Tanım |
|-------|-------|
| **Kırmızı takım (red team)** | Saldırgan rolü — gerçek saldırıyı taklit eder. |
| **Mavi takım (blue team)** | Savunmacı rolü — tespit ve müdahale. Bkz. [11-soc](../11-soc-mavi-takim/siem-edr-soar.md). |
| **Mor takım (purple team)** | Kırmızı+mavi işbirliği. |
| **Recon (keşif)** | Hedef hakkında bilgi toplama (pasif/aktif). |
| **Enumerasyon** | Servis/kullanıcı/paylaşım gibi detayları aktif olarak listeleme. |
| **Ayrıcalık yükseltme (privilege escalation)** | Düşük yetkiden yüksek yetkiye geçiş (dikey) veya eş seviyede yayılma (yatay). |
| **Yanal hareket (lateral movement)** | Ele geçirilen bir makineden ağdaki diğerlerine geçme. |
| **Kalıcılık (persistence)** | Yeniden başlatma/temizlik sonrası erişimi koruma. |
| **C2 (komuta-kontrol)** | Ele geçirilen makinelerle saldırganın haberleşme altyapısı. |
| **Ters kabuk (reverse shell)** | Hedefin saldırgana doğru başlattığı kabuk bağlantısı (firewall'u atlatır). |
| **Bind shell** | Hedefte bir portu dinleyen kabuk; saldırgan bağlanır. |

## SOC / savunma araçları

| Terim | Tanım |
|-------|-------|
| **SIEM** | Güvenlik olay ve bilgi yönetimi — log toplama+korelasyon. |
| **EDR / XDR** | Uç nokta / genişletilmiş tespit ve müdahale. |
| **SOAR** | Güvenlik orkestrasyon, otomasyon ve müdahale. |
| **IDS / IPS** | Saldırı tespit / önleme sistemi. |
| **TP / FP / FN / TN** | Doğru pozitif / yanlış pozitif / yanlış negatif / doğru negatif. Bkz. [log-analizi.md](../11-soc-mavi-takim/log-analizi.md). |
| **Sysmon** | Windows için ayrıntılı olay günlüğü aracı. |
| **IR (olay müdahalesi)** | Incident Response — bir güvenlik olayına yapılandırılmış yanıt. |

## Yönetişim, risk, uyum (GRC)

| Terim | Tanım |
|-------|-------|
| **GRC** | Governance, Risk, Compliance. Bkz. [08-grc](../08-grc-yonetisim-risk-uyum/cerceveler-nist-iso.md). |
| **NIST CSF** | NIST Siber Güvenlik Çerçevesi (2.0: Govern, Identify, Protect, Detect, Respond, Recover). |
| **ISO 27001** | Bilgi güvenliği yönetim sistemi (ISMS) standardı. |
| **SLE / ARO / ALE** | Tek kayıp beklentisi / yıllık olay sıklığı / yıllık kayıp beklentisi (nicel risk). |
| **RTO / RPO** | Kurtarma süre / veri kaybı hedefi (iş sürekliliği). |
| **STRIDE** | Microsoft tehdit modelleme çerçevesi. Bkz. [stride](../08-grc-yonetisim-risk-uyum/stride-tehdit-modelleme.md). |

## Bulut ve sanallaştırma

| Terim | Tanım |
|-------|-------|
| **IaaS / PaaS / SaaS** | Altyapı / platform / yazılım hizmet modelleri. Bkz. [09-cloud](../09-cloud-virtualizasyon/temel-kavramlar.md). |
| **Paylaşılan sorumluluk (shared responsibility)** | Güvenliğin bulut sağlayıcı ile müşteri arasında bölünmesi. |
| **Hipervizör (hypervisor)** | Sanal makineleri yöneten katman (Type 1/Type 2). |
| **Container / konteyner** | Çekirdeği paylaşan, izole edilmiş uygulama paketi (Docker). |
| **Container escape** | Konteynerden ana makineye kaçış zafiyeti. |
| **CSPM** | Bulut güvenlik duruşu yönetimi. |

---

> Bir terim eksikse veya bir dosyada tanımsız geçtiyse, buraya eklenmesi gereken bir boşluktur — repo büyüdükçe bu sözlük de büyür.
