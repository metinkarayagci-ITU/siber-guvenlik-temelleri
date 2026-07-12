# 🏁 Yarış Koşulları (Race Conditions) — Web

Çoğu web zafiyeti tek bir isteğin *içeriğiyle* ilgilidir (enjeksiyon, XSS). Yarış koşulu farklıdır: sorun tek istekte değil, **birden çok isteğin zamanlamasındadır**. Uygulama bir işlemi "kontrol et, sonra uygula" (check-then-act) olarak iki adımda yaparsa ve bu adımlar atomik değilse, aynı anda gönderilen istekler kontrolü aynı "eski" durumda yakalayıp işi birden çok kez yaptırabilir.

> Ön koşul: [web-mimarisi.md](../web-mimarisi.md). OS/dosya düzeyindeki kardeşi (TOCTOU): [../../03-isletim-sistemi-ici/surecler-ve-bellek.md](../../03-isletim-sistemi-ici/surecler-ve-bellek.md).

---

## 1. Mekanizma: limit-overrun (limit aşımı)

Klasik örnek — tek kullanımlık bir indirim kuponu veya bir hesap bakiyesi:
1. İstek, "kupon kullanıldı mı?" / "bakiye yeterli mi?" diye **kontrol eder** (henüz hayır).
2. Kuponu uygular / bakiyeyi düşer.

Saldırgan bu isteği **eşzamanlı** (ör. 50 paralel istek) gönderirse, hepsi 1. adımı "kupon kullanılmadı" durumunda yakalar → kupon 50 kez uygulanır, bakiye eksiye düşer, hediye kartı çoğaltılır. Buna **limit-overrun** denir. (Aynı fikir: para çekme, oy verme, davet kodu, stok rezervasyonu.)

> ⚠️ Bu bir **iş mantığı (business logic)** zafiyetidir — girdi "geçerli"dir; kusur, **eşzamanlılığın** hesaba katılmamasıdır. Bu yüzden girdi doğrulama/sanitizasyon onu durdurmaz.

---

## 2. Neden fark edilmesi/tespiti zor?

- Tek tek istekler **meşrudur** (her biri geçerli bir kupon isteği); anormallik yalnızca **zamanlama ve tekrar** desenindedir.
- Saldırgan pencereyi büyütmek için istekleri, ağ jitter'ını yok edecek kadar eş-zamanlı gönderir (ör. Burp Suite "single-packet attack" / turbo intruder — [burp-suite-rehberi.md](../burp-suite-rehberi.md)).
- Savunmacı için ipucu: kısa sürede aynı kaynağa/uç noktaya çok sayıda paralel istek ([../../11-soc-mavi-takim/log-analizi.md](../../11-soc-mavi-takim/log-analizi.md)).

---

## 3. Savunma — pencereyi kapat

- **Atomiklik:** Kontrol ve güncellemeyi tek, bölünemez işlemde yap — veritabanı düzeyinde koşullu/atomik güncelleme (`UPDATE ... SET balance = balance - x WHERE balance >= x`), benzersizlik kısıtı (unique constraint), idempotency anahtarı ile tekrarları yut.
- **Kilitleme:** İlgili kaydı işlem boyunca kilitle (row lock / `SELECT ... FOR UPDATE`); eşzamanlı erişimi serileştir.
- **Sınırlama (katman, kök çözüm değil):** Kritik uçlarda hız sınırlama (rate limit) pencereyi daraltır ama atomikliğin yerini tutmaz.

---

## 4. Saldırı–savunma kesişimi (özet)

- **Kök neden ortaktır:** Bu, OS'taki [TOCTOU](../../03-isletim-sistemi-ici/surecler-ve-bellek.md)'nun web karşılığıdır — ikisinin de kökü "kontrol ile kullanım arasındaki atomik-olmayan pencere". OS'ta symlink yarışı, web'de çift-harcama.
- **Girdi değil zamanlama:** Enjeksiyon ailesi "veri kod gibi yorumlanır" kök nedenine dayanırken, yarış koşulu "işlemler atomik değildir" kök nedenine dayanır — bu yüzden savunması da farklıdır (kaçış değil, atomiklik/kilitleme).
- **OWASP bağlamı:** 2025'te hatalı istisna/durum yönetimi (A10) ve iş-mantığı kusurları başlığıyla ilişkilidir ([../owasp-top10-tam-rehber.md](../owasp-top10-tam-rehber.md)).
