# 🔤 Regex (Düzenli İfadeler) Referansı

Düzenli ifadeler (regular expressions / regex), metin içinde desen aramanın ve çıkarmanın evrensel dilidir. Güvenlikte her yerdedir: log analizi (IP/hata çıkarma), IDS/IPS imzaları, girdi doğrulama, veri sızıntısı tespiti (DLP), grep/sed/awk. Bu dosya, güvenlik odaklı bir regex referansıdır.

> Uygulama: [linux-komut-referansi.md](../02-linux-windows/linux-komut-referansi.md) (grep), [log-analizi.md](../11-soc-mavi-takim/log-analizi.md), [python-guvenlik-icin.md](python-guvenlik-icin.md) (`re`), [bash-otomasyon.md](bash-otomasyon.md).

---

## 1. Temel karakterler ve metakarakterler

| Sembol | Anlam | Örnek | Eşleşir |
|--------|-------|-------|---------|
| `.` | Herhangi bir karakter | `a.c` | `abc`, `a1c` |
| `*` | Öncekinden 0+ | `ab*` | `a`, `ab`, `abbb` |
| `+` | Öncekinden 1+ | `ab+` | `ab`, `abbb` (not `a`) |
| `?` | Öncekinden 0 veya 1 | `ab?` | `a`, `ab` |
| `^` | Satır başı | `^Hata` | "Hata" ile başlayan |
| `$` | Satır sonu | `son$` | "son" ile biten |
| `[]` | Karakter kümesi | `[aeiou]` | herhangi bir sesli |
| `[^]` | Küme dışı (negatif) | `[^0-9]` | rakam olmayan |
| `[a-z]` | Aralık | `[a-z]` | küçük harf |
| `\|` | VEYA (alternatif) | `cat\|dog` | `cat` veya `dog` |
| `()` | Gruplama/yakalama | `(ab)+` | `ab`, `abab` |
| `{n,m}` | n ile m arası tekrar | `a{2,4}` | `aa`, `aaa`, `aaaa` |
| `\` | Kaçış (özel karakteri sabit yap) | `\.` | gerçek nokta `.` |

---

## 2. Karakter sınıfları (kısayollar)

| Kısayol | Anlam | Eşdeğeri |
|---------|-------|----------|
| `\d` | Rakam | `[0-9]` |
| `\D` | Rakam olmayan | `[^0-9]` |
| `\w` | Kelime karakteri | `[a-zA-Z0-9_]` |
| `\W` | Kelime olmayan | `[^a-zA-Z0-9_]` |
| `\s` | Boşluk (space, tab, newline) | `[ \t\n]` |
| `\S` | Boşluk olmayan | `[^ \t\n]` |
| `\b` | Kelime sınırı | (konum) |

> **Not:** `grep` (temel/BRE) bazı metakarakterlerde `\` gerektirir (`\+`, `\?`, `\{\}`); `grep -E` (genişletilmiş/ERE), Python `re` ve çoğu modern motor bunları doğrudan kullanır. Aşağıdaki örneklerde `grep -E` veya Python söz dizimi kullanıyoruz.

---

## 3. Güvenlikte en çok kullanılan desenler

### IPv4 adresi
```regex
\b(?:\d{1,3}\.){3}\d{1,3}\b
```
```bash
# Log'dan tüm IP'leri çıkar
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' access.log | sort -u
```
> Not: Bu desen `999.999.999.999` gibi geçersizleri de yakalar (basit ama pratik). Tam doğrulama için oktet aralık kontrolü (`0-255`) gerekir — ama log çıkarımı için bu yeterli.

### E-posta adresi
```regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```
```bash
# Bir dosyadan e-posta topla (OSINT / veri sızıntısı)
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' dosya.txt
```

### Diğer kritik desenler
| Amaç | Regex |
|------|-------|
| MAC adresi | `([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}` |
| SHA-256 hash | `\b[a-fA-F0-9]{64}\b` |
| MD5 hash | `\b[a-fA-F0-9]{32}\b` |
| URL | `https?://[^\s"'<>]+` |
| Kredi kartı (kaba) | `\b(?:\d[ -]?){13,16}\b` (DLP için) |
| Tarih (ISO) | `\d{4}-\d{2}-\d{2}` |
| Windows Event ID satırı | `EventID[:\s]+(\d+)` |

---

## 4. Güvenlik uygulama örnekleri

### Log analizi (başarısız girişten IP çıkar)
```bash
# → log-analizi.md, python-guvenlik-icin.md ile aynı desen
grep "Failed password" auth.log | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}'
```

### Girdi doğrulama (allow-list — güvenli kodlama)
```python
import re
# Kullanıcı adı SADECE harf/rakam/alt çizgi, 3-16 karakter (→ enjeksiyon-aileleri.md allow-list)
DESEN = re.compile(r'^[a-zA-Z0-9_]{3,16}$')

def gecerli_kullanici_adi(ad: str) -> bool:
    return bool(DESEN.fullmatch(ad))   # fullmatch: tüm string eşleşmeli

gecerli_kullanici_adi("ali_123")     # True
gecerli_kullanici_adi("ali; DROP")   # False ← enjeksiyon reddedildi
```

### Veri sızıntısı tespiti (DLP)
```bash
# Bir dosyada kredi kartı benzeri veri var mı? (DLP mantığı)
grep -oE '\b([0-9]{4}[ -]?){4}\b' cikti.txt
```

---

## 5. Nüans: regex ve güvenlik tuzakları

### ReDoS (Regular Expression Denial of Service)
Kötü yazılmış bir regex, belirli girdilerde **katlanarak yavaşlayabilir** (catastrophic backtracking) → bir DoS zafiyeti ([stride](../08-grc-yonetisim-risk-uyum/stride-tehdit-modelleme.md) D). Örnek tehlikeli desen: `(a+)+$`. Kötü niyetli bir girdi CPU'yu kilitler.
> **Savunma:** İç içe niceleyicilerden (`(a+)+`) kaçın, girdi uzunluğunu sınırla, güvenli regex motorları (RE2 gibi backtracking'siz) kullan.

### Regex ile güvenlik filtresi yazma tehlikesi
Regex'i **kara liste** (blacklist) olarak kullanmak ([enjeksiyon-aileleri.md](../04-web-guvenligi/zafiyet-siniflari/enjeksiyon-aileleri.md)) kırılgandır: "`<script>` engelle" deseni `<ScRiPt>`, `<img onerror>`, kodlama ile atlatılır. **Regex doğrulama için allow-list'te güçlüdür ("sadece şuna izin ver"), kötüyü engelleme kara listesinde zayıftır.**

### Girdiyi kaçırma (escaping)
Kullanıcı girdisini bir regex'in **içine** koyacaksan, özel karakterleri kaçır (`re.escape` Python'da) — yoksa girdi regex'i değiştirebilir (regex injection).
```python
import re
guvenli = re.escape(kullanici_girdisi)   # kullanıcı girdisini sabit metne çevir
```

---

## 6. Pratik: test ve öğrenme

- **regex101.com** — canlı regex test/açıklama aracı (deseni yaz, eşleşmeyi anlık gör). Öğrenmenin en hızlı yolu.
- `grep -oE`, `sed -E`, Python `re` ile kendi loglarında pratik yap.
- Bir deseni her zaman **gerçek veriyle test et** — regex sık sık beklenmedik eşleşir/kaçırır.

---

## 7. Saldırı–savunma kesişimi (özet)

- **Regex her yerde:** Log analizi (mavi takım), IDS imzaları, DLP, girdi doğrulama, veri toplama (OSINT) — güvenliğin ortak dokusu.
- **Çift kenarlı:** Regex hem savunma (doğrulama, tespit) hem zafiyet kaynağı (ReDoS, kötü filtre) olabilir.
- **Allow-list'te kullan:** Regex'in güvenlik gücü "izin verileni tanımlamakta"dır, "kötüyü kovalamakta" değil — bu, tüm modülün ([enjeksiyon-aileleri.md](../04-web-guvenligi/zafiyet-siniflari/enjeksiyon-aileleri.md)) ana temasıyla aynı.

> **Sonraki:** [git-temelleri.md](git-temelleri.md).
