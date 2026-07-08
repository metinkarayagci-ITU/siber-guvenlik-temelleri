# 🐍 Güvenlik için Python

Python, güvenlik dünyasının fiili betik dilidir: okunabilir, zengin kütüphaneli ve hızlı prototiplenebilir. Bir güvenlik uzmanı için Python, tekrarlayan işleri otomatikleştirmenin, özel araçlar yazmanın ve mevcut araçları birbirine bağlamanın yoludur. Bu dosya, güvenlik odaklı Python temellerini örnek scriptlerle kurar.

> Uygulama örnekleri: [subnet_calculator.py](../01-ag-networking/pratik-scriptler/subnet_calculator.py), [port_tarayici.py](../01-ag-networking/pratik-scriptler/port_tarayici.py). Otomasyon kardeşi: [bash-otomasyon.md](bash-otomasyon.md).

---

## 1. Neden Python? (güvenlikte)

- **Hız (geliştirme):** Bir fikirden çalışan araca dakikalar içinde geçersin.
- **Kütüphaneler:** `socket` (ağ), `requests` (HTTP), `scapy` (paket), `hashlib` (kripto), `re` (regex), `paramiko` (SSH).
- **Yapıştırıcı:** Nmap çıktısını al, işle, rapor üret — araçları zincirle.
- **Okunabilirlik:** Başkasının (ve gelecekteki senin) anlayabileceği kod.

> **Etik hatırlatma:** Aşağıdaki scriptler eğitim içindir ve yalnızca **kendi/izinli sistemlerde** çalıştırılır → [metodoloji-ve-rules-of-engagement.md](../10-pentest-metodolojisi/metodoloji-ve-rules-of-engagement.md).

---

## 2. Güvenlik için kritik standart kütüphaneler

| Kütüphane | Ne için |
|-----------|---------|
| `socket` | Ham TCP/UDP — port tarayıcı, banner grabber |
| `requests` (harici) | HTTP istekleri — web testi, API |
| `hashlib` | Hash (SHA-256, MD5) — bütünlük, parola |
| `hmac`, `secrets` | HMAC, güvenli rastgelelik ([temel-kavramlar.md](../05-kriptografi/temel-kavramlar.md)) |
| `re` | Regex — log/veri ayrıştırma ([regex-referans.md](regex-referans.md)) |
| `ipaddress` | IP/subnet hesabı ([subnetting-cidr.md](../01-ag-networking/subnetting-cidr.md)) |
| `subprocess` | Harici komut çalıştırma (güvenli: `shell=False`) |
| `json`, `csv` | Veri işleme, rapor |
| `argparse` | Komut satırı arayüzü |

> ⚠️ **`secrets` vs `random`:** Güvenlik amaçlı rastgelelik (token, parola, anahtar) için **`secrets`** kullan, `random` **değil**. `random` öngörülebilir (deterministik seed); `secrets` kriptografik olarak güvenlidir.
```python
import secrets
token = secrets.token_hex(16)        # güvenli rastgele token
sifre = secrets.choice(karakterler)  # güvenli seçim
```

---

## 3. Örnek script: HTTP güvenlik başlığı denetleyici

Bir sitenin güvenlik başlıklarını ([http-web-iletisimi.md](../01-ag-networking/http-web-iletisimi.md)) kontrol eden pratik bir araç:

```python
#!/usr/bin/env python3
"""guvenlik_basligi_kontrol.py — bir sitenin güvenlik başlıklarını denetler.
Kullanım: python3 guvenlik_basligi_kontrol.py https://ornek.com
Bağımlılık: requests (pip install requests)
"""
import sys
import requests

# Olması beklenen güvenlik başlıkları ve kısa açıklamaları (→ 01-ag/http-web-iletisimi.md)
BEKLENEN = {
    "Strict-Transport-Security": "HTTPS zorlaması (HSTS)",
    "Content-Security-Policy":    "XSS azaltma (CSP)",
    "X-Frame-Options":            "Clickjacking koruması",
    "X-Content-Type-Options":     "MIME sniffing engeli",
    "Referrer-Policy":            "Referrer sızıntısı kontrolü",
}

def kontrol(url: str) -> None:
    try:
        r = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print(f"[!] Bağlanılamadı: {e}")
        return

    print(f"\n=== {url} (HTTP {r.status_code}) ===")
    for baslik, aciklama in BEKLENEN.items():
        if baslik in r.headers:
            print(f"  [+] {baslik}: VAR  ({aciklama})")
        else:
            print(f"  [-] {baslik}: EKSİK  ← {aciklama}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python3 guvenlik_basligi_kontrol.py https://ornek.com")
        sys.exit(1)
    kontrol(sys.argv[1])
```

---

## 4. Örnek script: log ayrıştırıcı (başarısız giriş sayacı)

Bir `auth.log`'dan brute-force kaynağını bulan araç ([log-analizi.md](../11-soc-mavi-takim/log-analizi.md) mantığı, Python'da):

```python
#!/usr/bin/env python3
"""basarisiz_giris_sayaci.py — auth.log'da başarısız SSH denemelerini
IP'ye göre sayar (brute-force kaynağını bulur).
Kullanım: python3 basarisiz_giris_sayaci.py /var/log/auth.log
"""
import sys
import re
from collections import Counter

# IPv4 yakalayan regex (→ regex-referans.md)
IP_DESENI = re.compile(r"Failed password.*?from (\d{1,3}(?:\.\d{1,3}){3})")

def analiz(dosya_yolu: str) -> None:
    sayac = Counter()
    try:
        with open(dosya_yolu, encoding="utf-8", errors="ignore") as f:
            for satir in f:
                eslesme = IP_DESENI.search(satir)
                if eslesme:
                    sayac[eslesme.group(1)] += 1
    except FileNotFoundError:
        print(f"[!] Dosya bulunamadı: {dosya_yolu}")
        return

    if not sayac:
        print("[i] Başarısız giriş bulunamadı.")
        return

    print("Başarısız giriş denemeleri (IP → sayı):")
    for ip, adet in sayac.most_common(10):
        bayrak = "  ⚠️ ŞÜPHELİ" if adet > 20 else ""
        print(f"  {adet:>5}  {ip}{bayrak}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python3 basarisiz_giris_sayaci.py <auth.log>")
        sys.exit(1)
    analiz(sys.argv[1])
```

---

## 5. Örnek script: dosya bütünlüğü (hash) doğrulayıcı

```python
#!/usr/bin/env python3
"""hash_dogrula.py — bir dosyanın SHA-256 hash'ini hesaplar ve
verilen beklenen hash ile karşılaştırır (bütünlük doğrulama).
Kullanım: python3 hash_dogrula.py dosya.iso <beklenen_sha256>
"""
import sys
import hashlib

def dosya_hash(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        # Büyük dosyalar için parça parça oku (belleği taşırma)
        for parca in iter(lambda: f.read(8192), b""):
            h.update(parca)
    return h.hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 hash_dogrula.py <dosya> [beklenen_hash]")
        sys.exit(1)

    hesaplanan = dosya_hash(sys.argv[1])
    print(f"SHA-256: {hesaplanan}")

    if len(sys.argv) == 3:
        beklenen = sys.argv[2].lower()
        if hesaplanan == beklenen:
            print("[+] EŞLEŞTİ — dosya bütünlüğü doğrulandı ✓")
        else:
            print("[!] EŞLEŞMEDİ — dosya değişmiş/bozuk olabilir!")
```

---

## 6. Güvenli Python yazma (kendi kodunun güvenliği)

Bir güvenlik aracı bile zafiyetli yazılabilir. [Güvenli kodlama ilkeleri](../13-guvenli-kodlama-devsecops/guvenli-kodlama-ilkeleri.md) Python'da:

```python
# ❌ KÖTÜ — komut enjeksiyonu (→ enjeksiyon-aileleri.md)
import os
os.system(f"ping {kullanici_girdisi}")     # girdi: "8.8.8.8; rm -rf /"

# ✅ İYİ — subprocess + liste + shell=False
import subprocess
subprocess.run(["ping", "-c", "1", kullanici_girdisi], shell=False, timeout=5)

# ❌ KÖTÜ — eval/exec ile kullanıcı girdisi (kod çalıştırma)
eval(kullanici_girdisi)                     # ASLA

# ❌ KÖTÜ — güvensiz deserialization (→ A08, mekanizma+Log4Shell vakası:
# ../04-web-guvenligi/zafiyet-siniflari/enjeksiyon-aileleri.md)
import pickle
pickle.loads(guvenilmeyen_veri)             # RCE riski; JSON kullan
```

> **Kural:** `os.system`, `eval`, `exec`, `pickle.loads` kullanıcı girdisiyle = tehlike. Güvenli alternatifler: `subprocess` (liste), parametreli işlemler, `json`.

---

## 7. Saldırı–savunma kesişimi (özet)

- **Python iki taraflıdır:** Saldırgan araçları (tarayıcı, exploit, C2) da savunma araçları (log analizi, otomasyon, tespit) da Python'la yazılır. Aynı beceri her iki tarafta değerli.
- **Otomasyon ölçek kazandırır:** El ile 100 log dosyası okunmaz; Python ile saniyeler. SOC ([11-soc](../11-soc-mavi-takim/log-analizi.md)) ve pentest ([10-pentest](../10-pentest-metodolojisi/kesif-enumerasyon.md)) otomasyona dayanır.
- **Kendi aracını yaz:** [15-projeler](../15-projeler/proje-onerileri.md), bu becerileri portföy-kalite araçlara dönüştürmeyi önerir — bir mimar/kurucu için kendi araçlarını yazabilmek büyük avantaj.

> **Sonraki:** [bash-otomasyon.md](bash-otomasyon.md).
