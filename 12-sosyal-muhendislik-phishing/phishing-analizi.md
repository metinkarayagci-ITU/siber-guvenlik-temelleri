# 🎣 Sosyal Mühendislik ve Phishing Analizi

En güçlü teknik savunmalar bile, bir çalışanın kötü bir linke tıklamasıyla aşılabilir. Sosyal mühendislik, teknolojiyi değil **insanı** hedefler — ve saldırıların ezici çoğunluğunun başlangıç noktasıdır. Bu dosya, sosyal mühendislik türlerini, phishing e-posta analizini ve e-posta kimlik doğrulama savunmalarını (SPF/DKIM/DMARC) kurar.

> İlgili: [aaa-ve-mfa.md](../06-kimlik-erisim-yonetimi-iam/aaa-ve-mfa.md) (kimlik), [dns-derinlemesine.md](../01-ag-networking/dns-derinlemesine.md) (SPF/DKIM DNS kaydıdır), [log-analizi.md](../11-soc-mavi-takim/log-analizi.md) (süreç zinciri).

---

## 1. Sosyal mühendislik nedir? "İnsan katmanı"

Sosyal mühendislik, insanları **manipüle ederek** gizli bilgi ifşa etmelerini, güvenlik kurallarını çiğnemelerini veya zararlı bir eylem yapmalarını sağlamaktır. "İnsan hackleme"dir.

> **Neden en etkili saldırı vektörü:** Bir yazılım zafiyeti yamalanır; ama insan doğası (yardımseverlik, otoriteye itaat, korku, aciliyet, merak) yamalanmaz. [Kill chain](../07-tehdit-modelleme-cerceveler/cyber-kill-chain.md)'in "Delivery" aşamasının en yaygın yolu phishing'dir, çünkü en güçlü firewall'u değil, en zayıf halkayı (insan) hedefler.

### Manipülasyon ilkeleri (Cialdini)
Saldırganların istismar ettiği psikolojik kaldıraçlar:
| İlke | Nasıl kullanılır |
|------|------------------|
| **Otorite (authority)** | "CEO'dan acil talep", "IT departmanı" |
| **Aciliyet/kıtlık (urgency)** | "Hesabınız 24 saatte kapanacak!" |
| **Korku (fear)** | "Şüpheli giriş tespit edildi, hemen doğrulayın" |
| **Güven/tanıdıklık** | Bilinen marka/kişi taklidi |
| **Yardımseverlik/karşılıklılık** | "Size yardım ediyorum, siz de..." |

---

## 2. Sosyal mühendislik türleri

```mermaid
flowchart TD
    SE["Sosyal Mühendislik"]
    SE --> P["Phishing<br/>(toplu e-posta)"]
    SE --> SP["Spear phishing<br/>(hedefli, kişiselleştirilmiş)"]
    SE --> W["Whaling<br/>(üst yönetim hedefi)"]
    SE --> Sm["Smishing<br/>(SMS)"]
    SE --> V["Vishing<br/>(sesli/telefon)"]
    SE --> Pr["Pretexting<br/>(uydurma senaryo/kimlik)"]
    SE --> B["Baiting<br/>(yem: bırakılmış USB)"]
    SE --> T["Tailgating<br/>(fiziksel: peşine takılma)"]
```

| Tür | Kanal | Örnek |
|-----|-------|-------|
| **Phishing** | E-posta (toplu) | Sahte banka "hesabınızı doğrulayın" |
| **Spear phishing** | E-posta (hedefli) | İsminle, pozisyonunla kişiselleştirilmiş |
| **Whaling** | E-posta (VIP) | CEO/CFO hedefli, yüksek değerli |
| **BEC** (Business Email Compromise) | E-posta | "CEO'dan" acil havale talebi |
| **Smishing** | SMS | "Kargonuz bekliyor, link" |
| **Vishing** | Telefon | "Banka güvenlik ekibi" arıyor |
| **Pretexting** | Her kanal | Uydurma kimlik/senaryo ile güven kazanma |
| **Baiting** | Fiziksel/dijital | Otoparka "maaş bordrosu" etiketli USB bırakma |
| **Tailgating** | Fiziksel | Kartlı kapıdan birinin peşine takılma |

> **Kesişim — SMS OTP neden zayıf:** Smishing + SIM swap, SMS tabanlı MFA'yı ([aaa-ve-mfa.md](../06-kimlik-erisim-yonetimi-iam/aaa-ve-mfa.md)) atlatmanın yoludur — bu yüzden FIDO2/passkey phishing'e dayanıklı savunma olarak öne çıkar.

---

## 3. Phishing saldırı zinciri

```mermaid
sequenceDiagram
    participant A as Saldırgan
    participant V as Kurban
    participant S as Sahte site / Payload
    participant C as Saldırgan altyapısı (C2)
    A->>V: Phishing e-postası (otorite + aciliyet)
    V->>S: Linke tıklar / eki açar
    alt Kimlik hırsızlığı
        S->>V: Sahte giriş sayfası (gerçeğe benzer)
        V->>S: Kullanıcı adı + parola girer
        S->>A: Kimlik bilgileri saldırgana
    else Zararlı yazılım
        S->>V: Makrolu belge / zararlı dosya
        V->>C: Makro çalışır → reverse shell / C2 bağlantısı
    end
    A->>C: Kurban hesabı/makinesi ele geçirildi
```

Bu zincir, [log-analizi.md](../11-soc-mavi-takim/log-analizi.md) Senaryo B'deki `Outlook→Word→PowerShell→C2` süreç zincirinin saldırgan tarafıdır. Savunmacı bu zinciri loglardan tersine okur.

---

## 4. Phishing e-posta analizi (savunmacı becerisi)

Bir SOC analisti veya dikkatli kullanıcı, bir e-postayı şu göstergelerle inceler:

### Kontrol listesi
- [ ] **Gönderen adresi (from):** Görünen ad ile gerçek adres uyuşuyor mu? `Apple Support <security@apple-verify.ru>` → sahte.
- [ ] **Alan adı sahteciliği:** Benzer görünen alan adları — `paypa1.com` (l yerine 1), `micros0ft.com`, `apple-verify.com` (typosquatting/homoglyph).
- [ ] **Link hedefi:** Linkin **görünen metni** ile **gerçek URL'si** farklı mı? (Üzerine gel, tıklama.) `www.banka.com` yazıp `evil.ru`'ya gitmek klasik.
- [ ] **Aciliyet/tehdit dili:** "Hemen", "24 saat", "hesabınız kapatılacak".
- [ ] **Genel selamlama:** "Sayın müşteri" (isminizi bilmiyor) — toplu phishing işareti.
- [ ] **Ekler:** Beklenmedik `.docm`, `.zip`, `.exe`, `.html` ekleri.
- [ ] **Dilbilgisi/yazım:** (Giderek azalan bir gösterge — AI ile artık daha az güvenilir.)

### E-posta başlıklarını (headers) inceleme
Gerçek analiz, e-posta **başlıklarındadır** (raw header):
```
Received: ...           → e-postanın gerçek yolculuğu (kaynak sunucu)
Return-Path: ...        → gerçek dönüş adresi (from ile uyuşuyor mu?)
Authentication-Results: → SPF / DKIM / DMARC sonuçları (aşağıda!)
```

> 📸 EKRAN GÖRÜNTÜSÜ EKLENECEK: Bir phishing örneğinin ham başlıkları — `Authentication-Results` satırında `spf=fail` veya `dmarc=fail`.

---

## 5. E-posta kimlik doğrulama: SPF, DKIM, DMARC

E-posta protokolü (SMTP) 1980'lerde **kimlik doğrulama düşünülmeden** tasarlandı — bu yüzden gönderen adresi sahtelemek (spoofing) kolaydır. Üç mekanizma bu boşluğu kapatır; **hepsi DNS kayıtlarıdır** ([dns-derinlemesine.md](../01-ag-networking/dns-derinlemesine.md) TXT kayıtları).

```mermaid
flowchart TD
    E["Gelen e-posta"] --> SPF{"SPF<br/>gönderen IP, alan adının<br/>yetkili sunucular listesinde mi?"}
    SPF --> DKIM{"DKIM<br/>e-posta dijital imzası<br/>geçerli mi? (değiştirilmemiş)"}
    DKIM --> DMARC{"DMARC<br/>SPF/DKIM hizalı mı +<br/>başarısızsa ne yapılsın?"}
    DMARC -->|"geçti"| OK["Teslim et ✓"]
    DMARC -->|"başarısız + politika=reject"| Rej["Reddet/karantina"]
```

| Mekanizma | Ne doğrular | Nasıl | DNS kaydı |
|-----------|-------------|-------|-----------|
| **SPF** (Sender Policy Framework) | Gönderen **IP'sinin** alan adına ait olması | Alan adı, "bu sunucular benim adıma mail atabilir" der | TXT: `v=spf1 include:_spf.google.com ~all` ([RFC 7208](https://www.rfc-editor.org/rfc/rfc7208)) |
| **DKIM** (DomainKeys Identified Mail) | E-postanın **değiştirilmediği** + gerçekten o alandan geldiği | Gönderen sunucu e-postayı **imzalar** ([anahtar-degisimi-ve-imza.md](../05-kriptografi/anahtar-degisimi-ve-imza.md) dijital imza), alıcı açık anahtarla doğrular | TXT: DKIM açık anahtarı ([RFC 6376](https://www.rfc-editor.org/rfc/rfc6376)) |
| **DMARC** | SPF/DKIM'in **hizalı** olması + başarısızlık **politikası** | "SPF/DKIM başarısızsa ne yap: none/quarantine/reject" + rapor | TXT: `v=DMARC1; p=reject; rua=...` ([RFC 7489](https://www.rfc-editor.org/rfc/rfc7489)) |

### Nasıl birlikte çalışırlar
- **SPF** IP'yi kontrol eder ama e-posta iletilirse (forward) bozulabilir.
- **DKIM** içeriğin bütünlüğünü/kaynağını imzayla kanıtlar.
- **DMARC** ikisini birleştirir: "SPF **veya** DKIM geçmeli **ve** görünen from ile hizalı olmalı; değilse politikamı (reject) uygula" + gönderene **rapor** yollar.

> **DMARC politikası kritik:** `p=none` (sadece izle), `p=quarantine` (spam'e at), `p=reject` (tamamen reddet). Birçok kuruluş `p=none`'da kalır (izleme) ve spoofing'e açık kalır — gerçek koruma `p=reject`'tedir. Kendi alan adının DMARC durumunu kontrol et:
```bash
dig TXT _dmarc.ornek.com +short
dig TXT ornek.com +short | grep spf
```

---

## 6. Nüans ve savunma katmanları

- **Teknik + insan katmanı birlikte:** SPF/DKIM/DMARC spoofing'i büyük ölçüde durdurur ama saldırgan **kendi** (meşru DMARC'lı) alan adından benzer-isimli (`ornek-destek.com`) mail atabilir. Bu yüzden teknik savunma + **kullanıcı farkındalığı** ([kontrol matrisi](../08-grc-yonetisim-risk-uyum/guvenlik-kontrolleri-matrisi.md) idari kontrol) birlikte gerekir.
- **Phishing simülasyonu:** Kuruluşlar çalışanlara kontrollü sahte phishing gönderip eğitir (tıklama oranını ölçer). En etkili idari kontrollerden.
- **Savunma derinliği:** E-posta filtresi (Delivery'yi kır) + makro kısıtlama (Exploitation'ı kır) + EDR (Installation'ı kır) + MFA (çalınan parola işe yaramasın) + segmentasyon (yayılmayı durdur). Tek katman yeterli değil.
- **AI çağında phishing:** Üretken yapay zeka, dilbilgisi hatalarını (klasik ipucu) ortadan kaldırıp çok daha inandırıcı, kişiselleştirilmiş phishing üretiyor. "Kötü yazım" göstergesine güven azalıyor; teknik doğrulama (SPF/DKIM/DMARC, link analizi) ve sıfır güven daha da kritik.

---

## 7. Saldırı–savunma kesişimi (özet)

- **İnsan en zayıf ama en güçlü halka:** Eğitimli, şüpheci bir kullanıcı en iyi sensördür ("bir şey yanlış" deyip bildiren çalışan, bir saldırıyı erken durdurur). Savunma insanı hem korur hem savunma katmanına dönüştürür.
- **DNS savunmanın parçası:** SPF/DKIM/DMARC'ın DNS'te ([dns-derinlemesine.md](../01-ag-networking/dns-derinlemesine.md)) yaşaması, e-posta güvenliğinin ağ temeliyle iç içe olduğunu gösterir.
- **Kill chain'in ilk halkası:** Phishing çoğu saldırının başlangıcı olduğu için, burada kırmak ([cyber-kill-chain.md](../07-tehdit-modelleme-cerceveler/cyber-kill-chain.md)) en yüksek getirili savunmadır — hasar başlamadan durur.

> **Modül 12 tamamlandı.** Sonraki: [13-guvenli-kodlama-devsecops/guvenli-kodlama-ilkeleri.md](../13-guvenli-kodlama-devsecops/guvenli-kodlama-ilkeleri.md).
