# 📤 Dosya Yükleme Zafiyetleri ve Web Shell

Neredeyse her uygulama dosya yükletir: profil fotoğrafı, CV, fatura, destek eki. Bu, saldırgan için en doğrudan **initial access** (ilk erişim) yollarından biridir — çünkü kontrolsüz bir yükleme, çoğu zaman **sunucuda kod çalıştırmaya** (RCE) kadar gider. Bu dosya, mekanizmayı, atlatma tekniklerini ve savunmayı kurar.

> Kardeş dosyalar: [enjeksiyon-aileleri.md](enjeksiyon-aileleri.md) (özellikle LFI/RFI — yükleme ile birleşir), [idor-erisim-kontrolu.md](idor-erisim-kontrolu.md). Saldırı sonrası: [../../10-pentest-metodolojisi/somuru-ve-sonrasi.md](../../10-pentest-metodolojisi/somuru-ve-sonrasi.md) (web shell → reverse shell).

---

## 1. Web shell nedir? (hedef bu)

Bir **web shell**, saldırganın sunucuya yerleştirdiği ve **web üzerinden erişilebilen** küçük bir script'tir; tarayıcıdan/curl'den komut çalıştırma yeteneği verir. Klasik (ve neden tehlikeli olduğunu gösteren) tek satırlık örnek:

```php
<?php system($_GET['cmd']); ?>
```
Bu dosya sunucuya `shell.php` olarak düşer ve web kökünden çalıştırılabilirse:
```
https://hedef.com/uploads/shell.php?cmd=id
→ uid=33(www-data) gid=33(www-data) ...
```
Artık saldırgan, web sunucusunun yetkisiyle (`www-data`) komut çalıştırıyor — bu, tam olarak [somuru-ve-sonrasi.md](../../10-pentest-metodolojisi/somuru-ve-sonrasi.md)'deki "initial foothold"un ta kendisidir. Sıradaki adım bu sınırlı web shell'i **tam bir reverse shell'e yükseltmek** (aynı dosyadaki bash `/dev/tcp` tek satırıyla) ve ardından **privilege escalation**'dır ([../../10-pentest-metodolojisi/privilege-escalation.md](../../10-pentest-metodolojisi/privilege-escalation.md)).

> **Neden "yükleme" ile "RCE" aynı cümlede:** Bir dosyayı yüklemek tek başına zararsızdır; tehlike, yüklenen dosyanın **sunucu tarafından çalıştırılabilir** bir yere, çalıştırılabilir bir türle düşmesidir. Yani kök sorun yine tanıdık: kullanıcının verdiği **veri** (dosya), sunucu için **kod**a dönüşüyor — [enjeksiyon-aileleri.md](enjeksiyon-aileleri.md)'nin "veri kod olarak yorumlanıyor" temasının dosya-sistemi katmanındaki hâli.

---

## 2. Neden mümkün? — güvenilmez üçlü

Uygulama, yükleme hakkında istemciden gelen **üç şeye** körü körüne güvenirse zafiyet doğar:

1. **Dosya adı / uzantı:** İstemcinin gönderdiği `avatar.php` adına güvenip diske öyle yazmak.
2. **Content-Type (MIME):** İstek başlığındaki `Content-Type: image/png` değerine güvenmek — bu değer tamamen saldırgan kontrolündedir ([../web-mimarisi.md](../web-mimarisi.md) "istemci tarafı saldırganın kontrolündedir").
3. **Depolama yeri + çalıştırma:** Dosyayı **web kökü (webroot) içine** ve o dizinde script çalıştırma açıkken koymak.

Üçü birden yanlışsa: saldırgan çalıştırılabilir bir dosyayı, çalıştırılabilir bir konuma, çalıştırılabilir bir türle koyar → web shell.

---

## 3. Atlatma teknikleri (zayıf filtreler nasıl aşılır)

Çoğu uygulama "sadece resim kabul et" der ama bunu **yanlış/eksik** yapar. Sahada karşılaşılan tipik zayıf filtreler ve aşılması:

| Zayıf filtre | Atlatma |
|--------------|---------|
| **Content-Type kontrolü** | İsteği Burp ile yakala, `Content-Type: image/png` yap ama içerik PHP olsun ([../burp-suite-rehberi.md](../burp-suite-rehberi.md)). |
| **Uzantı kara listesi** (`.php` yasak) | Alternatif çalıştırılabilir uzantılar: `.phtml`, `.php5`, `.phar`, `.pHp` (büyük/küçük harf), `.jsp`/`.jspx`, `.aspx`. |
| **Sadece son uzantıya bakma** | Çift uzantı: `shell.php.jpg` veya `shell.jpg.php` (sunucu yapılandırmasına göre biri çalışır). |
| **İçerik/magic byte kontrolü** | Dosyanın başına geçerli bir sihirli bayt (magic byte, ör. `GIF89a;`) koyup ardına PHP kodu ekle — dosya "resim gibi" başlar ama PHP olarak çalışır. |
| **Uzantı beyaz listesi ama dizin çalıştırıyor** | `.htaccess` yükleyip yeni bir uzantıyı çalıştırılabilir yapmak (Apache), ya da yalnızca dosya okumak için **LFI ile birleştirme** (aşağıda). |

> **Null byte (tarihsel):** Eski sistemlerde `shell.php%00.jpg` — `%00` (null byte), C tabanlı kontrolde stringi erken kesip uzantıyı `.php` yapardı. Modern dillerde büyük ölçüde kapandı ama neden çalıştığını anlamak önemli: filtre ile dosya sistemi, string'in sonunu farklı yerde görüyordu.

**LFI + yükleme kombinasyonu:** Dosya çalıştırılamıyor ama sadece okunabiliyorsa bile — PHP kodunu içeren bir "resmi" yükleyip, ardından bir **LFI** ([enjeksiyon-aileleri.md](enjeksiyon-aileleri.md)) ile o dosyayı `include` ettirmek kodu çalıştırır. İki orta-şiddetli kusur birleşince RCE olur — bu, "zafiyetleri tek tek değil zincir olarak düşün" dersidir.

---

## 4. Savunma (katmanlı)

Tek bir kontrol yetmez; katmanlar:

- **Uzantı için beyaz liste (allow-list):** "Yasak olanları" değil, **izin verilenleri** (`.jpg`, `.png`, `.pdf`) tanımla — [enjeksiyon-aileleri.md](enjeksiyon-aileleri.md)'deki "kara liste her zaman kaybeder" ilkesinin aynısı.
- **İçeriği doğrula:** Uzantıya değil, gerçek dosya türüne bak (magic byte / kütüphane ile); mümkünse resmi yeniden işle (re-encode) — gömülü kod bu işlemde bozulur.
- **Web kökü dışında sakla:** Yüklenen dosyayı hiçbir zaman doğrudan çalıştırılabilir bir dizine koyma; ayrı bir dosya deposunda/CDN'de tut, uygulama üzerinden servis et.
- **Sunucu tarafında yeniden adlandır:** Kullanıcının verdiği adı kullanma; rastgele bir ad ver, uzantıyı sen belirle. Bu aynı zamanda [IDOR](idor-erisim-kontrolu.md)-tarzı tahmin edilebilir dosya adı erişimini de engeller.
- **Dizinde çalıştırmayı kapat:** Yükleme dizininde script yürütmeyi web sunucusu düzeyinde devre dışı bırak.
- **Boyut/oran sınırı + AV taraması:** DoS ve bilinen zararlıya karşı.

```python
# GÜVENLİ (kavramsal) — allow-list + içerik doğrulama + güvenli ad + webroot dışı
import os, imghdr, secrets

IZINLI = {"jpg": b"\xff\xd8\xff", "png": b"\x89PNG"}   # uzantı → beklenen magic byte

def guvenli_yukle(dosya, uzanti):
    if uzanti not in IZINLI:                       # beyaz liste
        raise ValueError("İzin verilmeyen tür")
    bas = dosya.read(8)
    if not bas.startswith(IZINLI[uzanti]):         # gerçek içerik kontrolü
        raise ValueError("İçerik uzantıyla uyuşmuyor")
    ad = secrets.token_hex(16) + "." + uzanti      # sunucu üretir, kullanıcı adı kullanılmaz
    yol = os.path.join("/var/uploads", ad)         # web kökü DIŞINDA
    # ... güvenli şekilde yaz
```

---

## 5. Saldırı–savunma kesişimi (özet)

- **Web shell = kalıcı initial access:** Yüklenen shell, tarayıcı üzerinden erişilebilen bir arka kapıdır; bu yüzden aynı zamanda bir **persistence** ([../../10-pentest-metodolojisi/somuru-ve-sonrasi.md](../../10-pentest-metodolojisi/somuru-ve-sonrasi.md) §5) mekanizmasıdır.
- **Savunmacı tarafı — tespit:** Web kökünde **yeni/beklenmedik bir script dosyası** ve daha da kesini, **web sunucusu sürecinin (`www-data`) bir shell/komut doğurması** (`apache → sh → id`) klasik bir web shell işaretidir → süreç soy ağacı ([../../11-soc-mavi-takim/log-analizi.md](../../11-soc-mavi-takim/log-analizi.md); [../../03-isletim-sistemi-ici/surecler-ve-bellek.md](../../03-isletim-sistemi-ici/surecler-ve-bellek.md)). File integrity monitoring (FIM), web köküne düşen dosyayı yakalar.
- **Magic byte hem saldırıda hem savunmada:** Dosyayı uzantısına değil **içeriğine** göre tanımak, hem saldırganın atlatma yüzeyidir hem de forensics/malware analizinde ([../../11-soc-mavi-takim/malware-analiz.md](../../11-soc-mavi-takim/malware-analiz.md) file carving, PE tanıma) dosya türünü doğru belirleme yöntemidir — aynı teknik, iki taraf.
- **OWASP bağlamı:** Kontrolsüz dosya yükleme, [OWASP "Unrestricted File Upload"](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload) altında ele alınır ve sonucu genelde RCE olduğu için [owasp-top10-tam-rehber.md](../owasp-top10-tam-rehber.md)'deki A05 Injection ve A06 Insecure Design temalarıyla kesişir.

> **Modül 04 devam:** [../pratik-lab/juice-shop-notlari.md](../pratik-lab/juice-shop-notlari.md) — bir yükleme kusurunu elle dene.
