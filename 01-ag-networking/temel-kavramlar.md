# 🌐 Ağ Temel Kavramları ve OSI Modeli

Ağ bilgisi, siber güvenliğin omurgasıdır: her saldırı ya ağ üzerinden gelir ya da ağda iz bırakır. Bu dosya, bir paketin bir cihazdan diğerine giderken geçtiği katmanları ve bunların güvenlik anlamını kurar.

> Devamı: [tcp-ip-protokoller.md](tcp-ip-protokoller.md), [subnetting-cidr.md](subnetting-cidr.md). Terimler: [terminoloji-sozlugu.md](../00-baslangic/terminoloji-sozlugu.md).

---

## 1. Ağ nedir ve neden katmanlıdır?

Ağ, veri paylaşmak için birbirine bağlı cihazlar topluluğudur. Ama iki cihazın "konuşması" aslında onlarca alt problemin çözülmesini gerektirir: fiziksel sinyal nasıl taşınacak? Hangi cihaza gidecek? Paket kaybolursa ne olacak? Uygulama veriyi nasıl anlayacak?

Bu karmaşayı yönetmek için ağ **katmanlara** bölünür. Her katman yalnızca kendi işini yapar ve altındaki/üstündeki katmana standart bir arayüz sunar. Böylece bir katman (ör. Wi-Fi yerine Ethernet) değişse üsttekiler etkilenmez. Bu **soyutlama (abstraction)**, güvenlikte de kritiktir: bir saldırı hangi katmandaysa savunma da o katmanda konumlanır.

### LAN, WAN ve topolojiler
- **LAN (yerel ağ):** Tek bir fiziksel alanda (ofis, ev) sınırlı ağ.
- **WAN (geniş ağ):** Coğrafi olarak dağıtık ağların birleşimi; internet en büyük WAN'dır.
- **Topoloji:** Cihazların bağlanış biçimi — yıldız (star, bugün en yaygın; merkezde switch), mesh (her düğüm birbirine; dayanıklı), bus/ring (eski). Topoloji, bir düğüm düştüğünde ağın ne kadar etkileneceğini belirler.

### Temel ağ cihazları

| Cihaz | Çalıştığı katman | Görevi | Güvenlik notu |
|-------|------------------|--------|---------------|
| **Hub** | 1 (fiziksel) | Geleni tüm portlara tekrarlar (eski). | Tüm trafiği herkese gönderir → dinleme (sniffing) çok kolay. |
| **Switch (anahtar)** | 2 (veri bağı) | MAC adresine göre yalnızca doğru porta iletir. | MAC tablosu taşırma (CAM overflow) ile hub gibi davranmaya zorlanabilir. |
| **Router (yönlendirici)** | 3 (ağ) | Farklı ağlar arasında IP'ye göre yol bulur. | ACL ve firewall'un doğal yeri; ağ segmentasyonunun kalbi. |
| **Firewall (güvenlik duvarı)** | 3–7 | Trafiği kurallara göre geçirir/engeller. | Bkz. [routing-nat-vpn.md](routing-nat-vpn.md). |
| **Access Point (AP)** | 2 | Kablosuz cihazları kablolu ağa bağlar. | Sahte AP (evil twin), WPA saldırıları → [kablosuz-guvenlik.md](kablosuz-guvenlik.md). |

---

## 2. Yerel ağın çalışması: MAC adresleri, ARP ve DHCP

Bir cihazın yerel ağda (LAN) konuşabilmesi için iki adres türü ve iki yardımcı protokol devreye girer. Bunlar TryHackMe "Intro to LAN" düzeyinde çekirdek kavramlardır ve katman-2/3 saldırılarının (ARP zehirleme, sahte DHCP) neden mümkün olduğunu anlamanın temelidir.

### MAC adresi (fiziksel adres)
Her ağ arayüzü kartının (NIC) fabrikada verilmiş, 48-bit (6 byte), hex ile yazılan benzersiz bir **MAC adresi** (`00:1A:2B:3C:4D:5E`) vardır. MAC, katman-2'de (yerel ağ içinde) cihazı belirler; IP ise katman-3'te (ağlar arası) belirler. Ayrım kritik: **IP adresi "hangi ağdaki hangi mantıksal düğüm" (değişebilir, yönlendirilebilir); MAC "hangi fiziksel kart" (yerel, yönlendirilemez).** Bir paket bir yönlendiriciden (router) her geçtiğinde IP başlığı korunur ama MAC başlığı **her adımda yenilenir** (o segmentteki bir sonraki cihazın MAC'iyle). MAC neden hex yazılır sorusunun cevabı [00-baslangic/bilgisayar-temelleri.md](../00-baslangic/bilgisayar-temelleri.md)'de (1 byte = 2 hex karakter) verilmişti.

> **Kesişim:** MAC adresleri yazılımla değiştirilebilir (**MAC spoofing**) — MAC tabanlı erişim kontrolü (MAC filtering) bu yüzden tek başına zayıf bir savunmadır. Ayrıca switch'in MAC tablosunu taşırmak (CAM overflow, yukarıdaki tabloda), switch'i "hub gibi" davranıp tüm trafiği yaymaya zorlar ve dinlemeyi (sniffing) mümkün kılar.

### ARP — IP'yi MAC'e çevirme
Yerel ağda bir cihaz veri gönderirken hedefin IP'sini bilir ama çerçeveyi (frame) teslim etmek için hedefin **MAC'ine** ihtiyaç duyar. Bu ikisi arasındaki köprü **ARP** (Address Resolution Protocol) protokolüdür (kaynak: [RFC 826](https://www.rfc-editor.org/rfc/rfc826)):

```mermaid
sequenceDiagram
    participant A as Cihaz A (192.168.1.5)
    participant Ağ as Yayın (broadcast)
    participant B as Cihaz B (192.168.1.9)
    A->>Ağ: ARP Request — "192.168.1.9'un MAC'i kimde?" (herkese)
    B->>A: ARP Reply — "O benim, MAC'im 00:1A:2B:..." (sadece A'ya)
    Note over A: Cevabı ARP önbelleğine (cache) kaydeder
```

ARP cevapları bir **ARP önbelleğinde** (arp cache) tutulur (`arp -a` ile görülür). Sorun: ARP kimlik doğrulaması yapmaz — bir cihaz, sorulmadan da "sahte" ARP cevabı gönderebilir ve kurbanın önbelleğini zehirleyebilir.

> **Kesişim — ARP zehirleme (ARP poisoning/spoofing):** Saldırgan, "yönlendiricinin IP'si benim MAC'imde" diyen sahte ARP cevapları yollayarak kurbanın trafiğini kendi üzerinden geçmeye zorlar — klasik bir **ortadaki adam (man-in-the-middle, MITM)** saldırısı. Bu, [05-kriptografi/anahtar-degisimi-ve-imza.md](../05-kriptografi/anahtar-degisimi-ve-imza.md)'de anlatılan MITM tehdidinin katman-2'deki somut hâlidir ve TLS'in ([05-kriptografi/pki-x509.md](../05-kriptografi/pki-x509.md)) neden gerekli olduğunu gösterir: trafik şifreliyse, saldırgan araya girse bile içeriği okuyamaz. MITM konumuna geçen saldırgan, kurbanın düz metin trafiğini Wireshark ile okur — bunu pcap'te görmek ve ARP zehirlemeyi tespit etmek için → [pratik-lab/paket-analizi-wireshark.md](pratik-lab/paket-analizi-wireshark.md). Savunma: Dynamic ARP Inspection (DAI), statik ARP girdileri, port güvenliği.

### DHCP — otomatik IP dağıtımı
Bir cihaz ağa bağlandığında IP adresini elle değil, genellikle **DHCP** (Dynamic Host Configuration Protocol) ile otomatik alır (kaynak: [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131)). Süreç dört adımlıdır — **DORA**:

```mermaid
sequenceDiagram
    participant C as İstemci (yeni cihaz)
    participant S as DHCP Sunucusu
    C->>S: 1. DISCOVER — "ağda DHCP sunucusu var mı?" (broadcast)
    S->>C: 2. OFFER — "şu IP'yi kullanabilirsin"
    C->>S: 3. REQUEST — "o IP'yi istiyorum"
    S->>C: 4. ACK — "onaylandı, senin (kira/lease süresince)"
```

DHCP, IP'nin yanında ağ geçidi (gateway), DNS sunucusu ([dns-derinlemesine.md](dns-derinlemesine.md)) ve alt ağ maskesi ([subnetting-cidr.md](subnetting-cidr.md)) gibi kritik bilgileri de dağıtır. DHCP başarısız olursa cihaz kendine `169.254.x.x` (APIPA) adresi verir — bu adresi görmek genelde DHCP arızasının işaretidir ([subnetting-cidr.md](subnetting-cidr.md)).

> **Kesişim — sahte DHCP (rogue DHCP):** DHCP de kimlik doğrulamaz; saldırgan ağa sahte bir DHCP sunucusu koyup kurbanlara kendi IP'sini "ağ geçidi" veya "DNS sunucusu" olarak dağıtabilir → trafiği ele geçirir (MITM) veya kurbanı zararlı bir DNS'e yönlendirir ([dns-derinlemesine.md](dns-derinlemesine.md) DNS spoofing). Savunma: DHCP snooping. IPv6'da bunun karşılığı sahte Router Advertisement saldırısıdır ([tcp-ip-protokoller.md](tcp-ip-protokoller.md)).

---

## 3. OSI 7 katman modeli

OSI (Open Systems Interconnection), ağ iletişimini 7 kavramsal katmana ayıran referans modeldir. Gerçekte internet TCP/IP modelini kullanır, ama OSI **düşünme ve sorun giderme dili** olarak standarttır: "bu bir katman 3 sorunu mu, katman 7 mi?" sorusu, hem ağ arızasını hem saldırıyı sınıflandırır.

```mermaid
flowchart TD
    L7["7 · Uygulama (Application)<br/>HTTP, DNS, SMTP — kullanıcının gördüğü"]
    L6["6 · Sunum (Presentation)<br/>şifreleme, kodlama, TLS, sıkıştırma"]
    L5["5 · Oturum (Session)<br/>oturum kurma/sürdürme"]
    L4["4 · Taşıma (Transport)<br/>TCP/UDP, port, segment, güvenilirlik"]
    L3["3 · Ağ (Network)<br/>IP, router, paket, yönlendirme"]
    L2["2 · Veri Bağı (Data Link)<br/>MAC, switch, çerçeve (frame)"]
    L1["1 · Fiziksel (Physical)<br/>kablo, sinyal, bit"]
    L7 --> L6 --> L5 --> L4 --> L3 --> L2 --> L1
```

### Katman katman — ne, hangi veri birimi, hangi saldırı

| # | Katman | Veri birimi (PDU) | Örnek protokol/adres | Tipik saldırı |
|---|--------|-------------------|----------------------|---------------|
| 7 | Uygulama | Veri (data) | HTTP, DNS, SMTP, SSH | SQLi, XSS, DNS zehirleme |
| 6 | Sunum | Veri | TLS/SSL, JPEG, ASCII | SSL stripping, zayıf şifre paketi |
| 5 | Oturum | Veri | NetBIOS, RPC, oturum belirteçleri | Oturum ele geçirme (hijacking) |
| 4 | Taşıma | **Segment** (TCP) / Datagram (UDP) | TCP, UDP, port numaraları | SYN flood, port tarama |
| 3 | Ağ | **Paket** (packet) | IP, ICMP, IPsec | IP spoofing, ICMP tünelleme |
| 2 | Veri Bağı | **Çerçeve** (frame) | Ethernet, MAC, ARP | ARP zehirleme, MAC spoofing, VLAN hopping |
| 1 | Fiziksel | **Bit** | Kablo, radyo, voltaj | Kablo dinleme (tap), jamming |

> 💡 **Hafıza ipucu (aşağıdan yukarı):** "**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way" → Physical, Data-link, Network, Transport, Session, Presentation, Application.

### Kapsülleme (encapsulation) — verinin katmanlarda paketlenişi

Bir uygulama veri gönderdiğinde, her katman kendi başlığını (header) ekleyerek veriyi "sarar". Alıcıda ters işlem (de-encapsulation) olur. Bu, bir mektubun zarfa, zarfın çantaya, çantanın araca konulması gibidir.

```mermaid
flowchart LR
    D["Veri (L7)"] --> S["[TCP başlık | Veri]<br/>Segment (L4)"]
    S --> P["[IP başlık | TCP | Veri]<br/>Paket (L3)"]
    P --> F["[Ethernet | IP | TCP | Veri | FCS]<br/>Çerçeve (L2)"]
    F --> B["01010111... Bit (L1)"]
```

**Güvenlik açısından neden önemli?** Wireshark gibi bir araçla bir paketi incelediğinde, tam olarak bu iç içe başlıkları görürsün. Bir saldırıyı analiz etmek, doğru katmanın başlığını okuyup anormalliği bulmaktır: kaynak IP'de spoofing (L3), beklenmedik port (L4), veya kötü niyetli HTTP yükü (L7).

---

## 4. Nüans: OSI vs TCP/IP modeli

Sık karıştırılır. OSI 7 katmanlı *teorik* modeldir; TCP/IP 4 katmanlı *uygulanan* modeldir. Eşleme:

| TCP/IP (4 katman) | Karşılık gelen OSI katmanları |
|-------------------|-------------------------------|
| Uygulama | 7 + 6 + 5 |
| Taşıma | 4 |
| İnternet | 3 |
| Ağ Erişimi (Link) | 2 + 1 |

Pratikte mühendisler ikisini karıştırıp konuşur ("katman 7 firewall'u", "katman 2 switch"i). Önemli olan hangi işin nerede yapıldığını bilmektir, model sayısını değil.

---

## 5. Saldırı–savunma kesişimi

- **Segmentasyon = katmanlı savunma:** Ağı VLAN'lar ve firewall'larla bölmek, bir katmandaki ihlalin tüm ağa yayılmasını engeller ([routing-nat-vpn.md](routing-nat-vpn.md)). Bu, [zero-trust](../06-kimlik-erisim-yonetimi-iam/zero-trust.md) ve mikro-segmentasyonun temelidir.
- **Katman farkındalığı tespitte:** Bir SOC analisti "bu bir L3 DDoS mu yoksa L7 uygulama saldırısı mı?" ayrımını yapmak zorundadır çünkü savunma tamamen farklıdır (biri hacim filtreleme, diğeri WAF/rate limit).
- **Switch güvenliği:** Port güvenliği (port security), DHCP snooping ve Dynamic ARP Inspection, katman-2 saldırılarını (ARP zehirleme, sahte DHCP) durduran temel savunmalardır.

> **Sonraki:** Protokollerin nasıl konuştuğunu görmek için [tcp-ip-protokoller.md](tcp-ip-protokoller.md).
