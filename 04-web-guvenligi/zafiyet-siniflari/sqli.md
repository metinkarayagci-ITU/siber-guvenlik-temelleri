# 💉 SQL Injection (SQLi)

SQL Injection, saldırganın bir uygulamanın veritabanı sorgularına müdahale etmesine izin veren bir enjeksiyon zafiyetidir. En eski, en bilinen ve hâlâ en yıkıcı web zafiyetlerindendir — çünkü doğrudan verinin (kullanıcılar, parolalar, kartlar) kalbine ulaşır.

> Aile bağlamı: [enjeksiyon-aileleri.md](enjeksiyon-aileleri.md) (ortak kök neden). OWASP Top 10:2025: [A05 Injection](../owasp-top10-tam-rehber.md).

---

## 1. Ne? — Mekanizma

Bir uygulama, kullanıcı girdisini **doğrudan bir SQL sorgusuna string olarak yapıştırdığında** SQLi doğar. Veritabanı, "veri" olması gereken girdiyi "kod (sorgu)" olarak yorumlar.

### Zafiyetli kod (kaçınılacak örnek)
```python
# ZAFİYETLİ — girdi doğrudan sorguya yapıştırılıyor
kullanici = request.form['kullanici']
parola = request.form['parola']
sorgu = f"SELECT * FROM users WHERE username = '{kullanici}' AND password = '{parola}'"
db.execute(sorgu)
```

Normal girdi `ali` / `1234` için sorgu:
```sql
SELECT * FROM users WHERE username = 'ali' AND password = '1234'
```

### Saldırı: kimlik doğrulama atlatma
Saldırgan **kullanıcı adı** alanına şunu yazarsa:
```
' OR '1'='1' --
```
Sorgu şuna dönüşür:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = '...'
```
- `OR '1'='1'` her zaman **doğru** → tüm kullanıcılar döner (genelde ilki = admin).
- `--` SQL yorum işareti → parola kontrolü **devre dışı** kalır.

**Sonuç:** Parola bilmeden giriş. Kod ile verinin karışmasının ders kitabı örneği.

---

## 2. Neden? — Kök neden ve etkisi

**Kök neden:** Uygulama, girdiyi "veri" ile "sorgu yapısı"nı ayırmadan birleştiriyor. Veritabanı motoru için `' OR '1'='1` artık veri değil, mantıksal bir ifade.

**Etki spektrumu (neden bu kadar ciddi):**
- Kimlik doğrulama atlatma (yukarıdaki).
- **Veri sızdırma:** UNION saldırılarıyla başka tabloları okuma (`UNION SELECT username, password FROM users`).
- **Veri değiştirme/silme:** `; DROP TABLE users; --`.
- **Kör (blind) SQLi:** Çıktı görünmese bile, doğru/yanlış cevaplardan (boolean) veya zaman gecikmelerinden (time-based, `SLEEP(5)`) veriyi bit bit çıkarma.
- **RCE'ye tırmanma:** Bazı DB'lerde dosya yazma / komut çalıştırma (`xp_cmdshell`, `INTO OUTFILE`) → tam sunucu ele geçirme.

---

## 3. SQLi türleri

| Tür | Nasıl | Ne zaman |
|-----|-------|----------|
| **In-band (klasik)** | Sonuç doğrudan yanıtta görünür | Error-based, UNION-based |
| **Blind (kör)** | Sonuç görünmez, dolaylı çıkarılır | Boolean-based, Time-based |
| **Out-of-band** | Veri ayrı bir kanaldan (DNS/HTTP) sızdırılır | In-band mümkün olmadığında |

```mermaid
flowchart TD
    I["Kullanıcı girdisi"] --> Q{"Sorguya nasıl giriyor?"}
    Q -->|"doğrudan string birleştirme"| V["ZAFİYETLİ"]
    Q -->|"parametreli sorgu (prepared statement)"| S["GÜVENLİ"]
    V --> R["Sonuç yanıtta görünür mü?"]
    R -->|"evet"| IB["In-band SQLi"]
    R -->|"hayır ama davranış değişiyor"| BL["Blind SQLi (boolean/time)"]
```

---

## 4. Nüans: sık yapılan yanlışlar

- **"Kaçış karakterleri (escaping) yeterli":** Girdideki `'` işaretini `\'` yapmak (manuel escaping) kırılgan ve atlatılabilir (farklı kodlamalar, farklı DB motorları). Gerçek çözüm parametreli sorgudur, manuel escaping değil.
- **"Kara liste (blacklist) filtresi koydum":** `OR`, `UNION`, `--` gibi kelimeleri engellemek atlatılabilir (`UnIoN`, yorumlarla `UN/**/ION`, kodlama). Kara liste enjeksiyonda **temelde yanlış** yaklaşımdır.
- **"ORM kullanıyorum, güvendeyim":** ORM'ler (Hibernate, Django ORM) çoğu durumda güvenli **ama** ham SQL (`raw()`, string birleştirme) kullanıldığında zafiyet geri gelir.
- **Sadece login değil:** Arama kutuları, sıralama parametreleri (`ORDER BY`), filtreler, HTTP başlıkları — girdinin sorguya değdiği **her yer** hedeftir.

---

## 5. Saldırı–savunma kesişimi: PoC senaryosu

**Ortam:** DVWA veya Juice Shop yerel lab ([../pratik-lab/juice-shop-notlari.md](../pratik-lab/juice-shop-notlari.md)).

1. Bir giriş/arama formu bul.
2. Girdiye tek tırnak (`'`) koy → SQL hatası dönerse (500 / "SQL syntax") zafiyet sinyali.
3. `' OR '1'='1' -- ` ile atlatmayı dene.
4. `UNION SELECT` ile sütun sayısını ve veri çekmeyi keşfet.
5. Otomasyon için **sqlmap** (yalnızca izinli hedefte):
   ```bash
   # Yalnızca kendi lab'ında / izinli hedefte!
   sqlmap -u "http://localhost/urun?id=1" --dbs --batch
   ```

**Tek tırnak (`'`) girildiğinde dönen tipik hata** (error-based SQLi sinyali):
```text
You have an error in your SQL syntax; check the manual that corresponds to
your MySQL server version for the right syntax to use near ''' AND password='' at line 1
```
Bu hata, girdinin doğrudan sorguya gittiğinin (parametreleştirilmediğinin) kanıtıdır — tek tırnak sorgunun sözdizimini bozdu. Ardından `' OR '1'='1' -- ` ile giriş "Login successful — Welcome admin" döner. Not: ayrıntılı SQL hatasının kullanıcıya dönmesi ayrıca bir bilgi ifşası zafiyetidir (OWASP 2025 A02/A10 → [../owasp-top10-tam-rehber.md](../owasp-top10-tam-rehber.md)); üretimde hata mesajları gizlenir ama saldırgana da yol gösterir.

---

## 6. Önleme (birincil savunma): parametreli sorgu

**Altın kural:** Girdiyi sorgu **metnine** hiç sokma. Sorgu yapısını sabitle, girdiyi ayrı **parametre** olarak gönder. Veritabanı böylece girdiyi asla "kod" olarak yorumlayamaz.

### Python (parametreli / prepared statement)
```python
# GÜVENLİ — girdi parametre olarak geçer, sorgu yapısına karışmaz
kullanici = request.form['kullanici']
parola = request.form['parola']
db.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (kullanici, parola),           # parametreler ayrı tuple
)
```
`?` (veya `%s`, `:isim`) yer tutucularıdır; sürücü değerleri güvenli şekilde bağlar (bind). `' OR '1'='1` girdisi artık yalnızca aranan bir **kullanıcı adı stringi** olur, mantıksal ifade değil.

### PHP (PDO)
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$kullanici, $parola]);
```

### Java (PreparedStatement)
```java
PreparedStatement ps = conn.prepareStatement(
    "SELECT * FROM users WHERE username = ? AND password = ?");
ps.setString(1, kullanici);
ps.setString(2, parola);
```

### Katmanlı savunma (defense in depth)
| Katman | Ne yapar |
|--------|----------|
| **Parametreli sorgu / ORM** | Birincil ve zorunlu savunma. |
| **En az ayrıcalık (DB kullanıcısı)** | Uygulama DB hesabı `DROP`/`FILE` yetkisi olmasın → hasar sınırlanır. |
| **Girdi doğrulama (allow-list)** | Beklenen formatı zorla (ör. id sayısal olmalı). |
| **WAF** | Bilinen kalıpları filtreler (yardımcı, tek başına yetmez). |
| **Hata mesajlarını gizle** | Ayrıntılı SQL hatası kullanıcıya dönmesin (error-based SQLi'yi köreltir). |

> ⚠️ **Parolayı asla düz saklama:** Yukarıdaki örneklerde parola karşılaştırması sadeleştirilmiştir. Gerçekte parolalar **Argon2/bcrypt** ile hash'lenir ve sorguda düz parola karşılaştırılmaz → [05-kriptografi/temel-kavramlar.md](../../05-kriptografi/temel-kavramlar.md).

---

## 7. Özet

- **Ne:** Girdinin SQL sorgusuna kod olarak karışması.
- **Neden ciddi:** Doğrudan veritabanına — kimlik atlatma, veri sızdırma, hatta RCE.
- **Birincil savunma:** **Parametreli sorgu (prepared statement)** — tartışmasız, tek gerçek çözüm.
- **Ek katmanlar:** en az ayrıcalık, girdi doğrulama, hata gizleme, WAF.

> **Sonraki:** [xss.md](xss.md).
