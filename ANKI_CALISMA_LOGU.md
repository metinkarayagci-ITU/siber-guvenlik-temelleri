# ANKI DESTE ÜRETİMİ — ÇALIŞMA LOGU

> Bu dosya, "Siber Güvenlik Temelleri" reposuyla tam uyumlu Anki destesi üretme işinin
> **kesintisiz sürdürülebilir** kaydıdır. Oturum kesilirse: **bu dosyayı oku, "AÇIK
> DURUM / SONRAKİ ADIM" bölümünden devam et.** Tüm ara veriler `.anki-build/` altında
> (gitignore'lu, diskte kalıcı).

Son güncelleme: 2026-07-12 · Durum: **✅ TAMAMLANDI (FAZ 1+2a+2b+3 — COMMON-CORE BİTTİ).
FINAL BUILD: `siber_guvenlik_temelleri.apkg` (1500 not, 2 kanonik not tipi, 7 Bütünsel tema).
121 yeni kart, 3 kalıcı sil, 15 advisory. guid 1379/1379 (KAYIP=0), zamanlama+revlog+media gömülü.
KALAN: yalnız kullanıcının import etmesi (rapor §9 DAL A/B).**

---

## 0. ÖZET KARAR (kullanıcı onayladı)

**Teslim modeli = "Reorg + geçmişi dosya içinde taşı" (Seçenek A).**
- Mevcut koleksiyon **16 modül** hiyerarşisine yeniden düzenlenir.
- 5 not tipi → **2 kanonik CyberFlow** not tipine birleştirilir (+ yeni tema).
- İçerik repoya göre yeniden yazılır/genişletilir.
- Her kartın **guid + zamanlama (ivl/factor/due/reps/lapses) + revlog**'u `.apkg` **içine** gömülür.
- Kullanıcı eski `Siber Güvenlik` üst-destesini **silip** yeni `.apkg`'yi bir kez import eder
  ("Import any learning progress" **açık** olmalı). Böylece hem reorg hem geçmiş korunur.

**KRİTİK KULLANICI HATIRLATMASI (teslimde tekrar et):** Import'tan hemen önce Anki'den
**taze bir export** alınmalı. Elimizdeki export `Siber Güvenlik.apkg` (2026-07-09 19:52).
O tarihten sonra yapılan tekrarlar dosyada YOKtur; sil+reimport onları geri alır.

### Neden bu model? (Anki import kısıtları — doğrulandı)
- Anki manuel: *"This updating process is generally not possible if the note type is
  changed… notes you have imported previously will not be updated."* → Not tipi değişince
  guid eşleşse bile güncelleme OLMAZ. Yani additive import ile 5→2 birleştirme yapılamaz.
- `.apkg` **re-import mevcut kartları farklı desteye TAŞIMAZ** (dosyadaki deste yalnızca
  YENİ kartlar için kullanılır). Yani additive import ile 16-modül reorg yapılamaz.
- Ama `.apkg` **zamanlama + revlog taşıyabilir** → eski deste silinip reimport edilince
  geçmiş korunur. Seçenek A bunu kullanır.

---

## 1. ORTAM (kurulum bitti)

- Python: `C:\Users\metin\AppData\Local\Programs\Python\Python312\python.exe`
  (winget ile user-scope kuruldu; PATH'te değil, tam yol kullan).
- Paketler: `genanki 0.13.1`, `zstandard 0.25.0` (+ stdlib sqlite3).
- Çalıştırma: PowerShell'de `$env:PYTHONUTF8=1` ver (konsol UTF-8).
- **Cursor tuzağı:** aynı `cursor` üzerinde dış `execute` döngüsü içinde iç `execute`
  çalıştırma → dış döngü 1 satırda kesilir. Her iç sorgu için ayrı cursor kullan.

## 2. GİRDİLER

- **Repo** (doğruluk/kapsam otoritesi): 16 modül (`00-baslangic`…`15-projeler`), ~73 `.md`.
  Persona: matematik müh. öğrencisi, hedef PQC + Security Architect. THM Pre Security +
  Cyber Security 101 path'lerini bitirmiş. Repo = bu bilginin yazılı, derin, bağlantılı hâli.
- **Mevcut deste**: `Siber Güvenlik.apkg` (repo kökünde; gitignore'lu). Modern export
  (meta v3, `collection.anki21b` = zstd, yeni normalize şema v18). `collection.anki2` boş
  legacy stub — kullanma. Gerçek veri anki21b'de.

## 3. MEVCUT DESTE — GERÇEK ENVANTER (doğrulandı)

- **1382 not / 1382 kart** (hepsi tek şablonlu ⇒ 1 kart/not), tamamı `Siber Güvenlik::…` altında.
- `col.crt = 1769302800` (zamanlama için ŞART: yeni koleksiyonun crt'si buna eşitlenecek).
- **Revlog: 1132 satır / 251 kart** review görmüş; kalan ~1131 kart hâlâ "new".
- **Tüm 1382 `kart_id` benzersiz.**

### 5 kaynak not tipi → 2 kanonik hedef
| src mid | ad | not | hedef |
|---|---|---:|---|
| 1980455173 | CyberFlow THM (flip) | 764 | **flip → 1980455173** |
| 1782661330691 | CyberFlow THM+ | 295 | flip → 1980455173 |
| 1607392913 | Siber Guvenlik CORE | 225 | flip → 1980455173 |
| 1980455180 | CyberFlow THM (Interaktif) | 45 | **type → 1980455180** |
| 1782661330692 | CyberFlow THM (Interaktif)+ | 53 | type → 1980455180 |

Hedef sayımı: **1284 flip + 98 interaktif**.

**MODEL_ID korunur:** flip = `1980455173`, interaktif = `1980455180` (spec §9).
Diğer 3 tip (691/692/CORE) hedefte yok olur; notları kanonik tipe taşınır.

### Alan eşleme — POZİSYONEL kimlik (7 slot)
Kanonik (CyberFlow): `[Kategori, Aciklama, Soru, Cevap, TerminalArg, Detay, kart_id]`
- cf tipleri (173/180/691/692): birebir aynı alan adları.
- CORE (`[Tur, Baglam, Soru, Cevap, Ornek, Aciklama, ID]`): pozisyonel eşlenir →
  Kategori=Tur, Aciklama=Baglam, Soru=Soru, Cevap=Cevap, TerminalArg=Ornek, Detay=Aciklama, kart_id=ID.
- Yani **field[i] → field[i]**, hepsinde. `inventory.json` zaten kanonik 7 slotla yazıldı.

Not: `Kategori`/`Tur` alanı kart TÜRÜ etiketidir (KAVRAM, PROTOKOL, KOMUT, NÜANS, KESİŞİM,
NEDEN VAR, ARAÇ, PORT, KATMAN…). Sekmede (cf-tab) gösterilir.

## 4. HEDEF DESTE HİYERARŞİSİ (16 modül)

Üst deste: `Siber Güvenlik Temelleri`. Altında modül desteleri (repo 00→15 sırası). Ayrı üst
deste: `Siber Güvenlik Temelleri · Bütünsel` (spec §10; `·` ile ayrı kalır, birleşmez).

Repo modülleri: 00-baslangic, 01-ag-networking, 02-linux-windows, 03-isletim-sistemi-ici,
04-web-guvenligi, 05-kriptografi, 06-kimlik-erisim-yonetimi-iam, 07-tehdit-modelleme-cerceveler,
08-grc-yonetisim-risk-uyum, 09-cloud-virtualizasyon, 10-pentest-metodolojisi, 11-soc-mavi-takim,
12-sosyal-muhendislik-phishing, 13-guvenli-kodlama-devsecops, 14-scripting-otomasyon, 15-projeler.

Okunabilir deste adları (öneri): `01 - Ağ / Networking`, `05 - Kriptografi`, … (00→15 sıralı).

### THM oda / CORE → modül DEFAULT eşlemesi (içerik fazında kart-bazlı incelenip kesinleşir)
- **00 Başlangıç:** inside-a-computer-system, computer-types, data-representation,
  become-a-hacker, become-a-defender, temel-terimler
- **01 Ağ:** what-is-networking, intro-to-lan, osi-model, packets-and-frames,
  extending-your-network, dns-in-detail, networking-concepts/essentials/core-protocols/
  secure-protocols, wireshark, tcpdump, subnet(core), http-in-detail(→ 01 veya 04, karar: 01
  temel HTTP, 04 web-saldırı bağlamı)
- **02 Linux&Windows:** linux-fundamentals(1-3)/cli/shells, windows-basics/fundamentals(1-3)/
  cli/powershell, active-directory, operating-system-security, operating-systems-introduction, os(core)
- **03 OS İç Yapısı:** (doğrudan THM odası yok) → repodan YENİ kartlar (süreç/bellek, user/kernel, bellek zafiyeti)
- **04 Web:** how-websites-work, web-application-basics, client-server-basics, burp-suite,
  gobuster, sqlmap, owasp-iaaa/design/data-handling, moniker-link, webvuln(core), putting-it-all-together
- **05 Kripto:** cryptography-concepts, cryptography-basics, public-key-cryptography, hashing,
  john-the-ripper, crypto(core), data-encoding(→05 veya 00), cyberchef(→05 veya 11)
- **06 IAM:** iam(core)  · **07 Tehdit Modelleme:** fw(core) = ATT&CK/KillChain/Pyramid/Diamond
- **08 GRC:** grc(core), the-cia-triad, security-principles, training-impact-on-teams
- **09 Cloud:** cloud-computing-fundamentals, virtualisation-basics, cloud(core)
- **10 Pentest:** metasploit(intro/exploitation/meterpreter), hydra, shells-overview, blue,
  vulnerability-scanner, nmap, search-skills(→10 veya 01)
- **11 SOC:** soc-fundamentals, digital-forensics, incident-response, logs-fundamentals,
  introduction-to-siem, firewall-fundamentals, ids-fundamentals, capa, remnux, flarevm, cyberchef
- **12 Sosyal Müh.:** (THM kartı ~yok) → repodan YENİ (phishing, SPF/DKIM/DMARC)
- **13 Güvenli Kodlama:** (THM kartı ~yok) → repodan YENİ
- **14 Scripting:** python-simple-demo, javascript-simple-demo, javascript-essentials,
  database-sql-basics, sql-fundamentals, + repodan regex/bash/git
- **15 Projeler:** kart yok (referans modül)
- **Bütünsel:** mevcut "· Bütünsel" (Pre Security M1-6 + CS101 M1-6) kartları → yeni
  `· Bütünsel` üst-destesinde repo-geneli NÜANS/KESİŞİM/NEDEN VAR olarak yeniden düzenlenir (spec §10).

## 5. YAPIM HATTI (pipeline) — mimari

1. **genanki** ile kur: 2 not tipi (tam MODEL_ID + spec §9 şablon/CSS), 16 modül + Bütünsel
   deste hiyerarşisi, notlar (mevcutlar **guid + kart_id korunarak**, yeniler yeni SGT- id).
2. genanki geçerli schema-11 `.apkg` (collection.anki2) üretir; kartlar "new".
3. **Zamanlama enjeksiyonu** (post-process, sqlite):
   - `UPDATE col SET crt = 1769302800` (orijinal crt — due değerleri geçerli kalsın).
   - Korunan her not için: guid→nid→cid bul, `cards` satırına orijinal
     type/queue/due/ivl/factor/reps/lapses/left/odue yaz.
   - Orijinal `revlog` satırlarını yeni cid ile ekle (id/timestamp korunur).
   - Kaynak: `.anki-build/schedule.json`, `.anki-build/revlog.json`.
4. Media (`0` = paste-…jpg) korunur.
5. Re-zip → `siber_guvenlik_temelleri.apkg`.

**Not:** genanki zamanlama/revlog set edemez; bu yüzden 3. adım şart. Interaktif ve flip
tiplerinin ikisi de tek şablon ⇒ not başına 1 kart ⇒ cid eşleme basit (ord=0).

## 6. KART TASARIM KURALLARI (spec §6, §8, §9 — üretimde uygula)
- Atomik: 1 kart = 1 bilgi. Bileşik/sıralı kavramı parçala.
- Cevap kısa; nüans/neden/kaynak → Detay. Bağlam (Aciklama) KOŞULLU (yalnız bileşik/karışan).
- **Bilgi sızdırma yasağı:** Soru+Aciklama, Cevap'ın anahtar terimini içermemeli. Üretimde denetle.
- Interaktif ({{type:Cevap}}) YALNIZ gerçek tek-komut/sözdizimi cevapları için. Kavram = flip.
- Dil akademik Türkçe; teknik terim İngilizce kalır, ilk geçişte parantez Türkçe. kart_id ASCII.
- `<...>` yer tutucular HTML olarak yorumlanmasın (köşeli parantez/kaçış).

## 7. DOĞRULAMA (spec §11 — `verify.py`, sonuç: work/verify_report.txt)  ✅ 2026-07-10
- [x] Türkçe karakter: 1451/1451 not Türkçe karakter içeriyor, **mojibake=0** ✓
- [x] kart_id: **1451 benzersiz, ASCII-dışı=0, tekrar=0** ✓
- [x] guid korunması: **envanterdeki 1382 guid'in 1382'si korundu, eksik=0** ✓
- [x] Bilgi sızdırma: heuristik 635 şüpheli (çoğu mevcut kart + yanlış-pozitif). YENİ (SGT-) kartlarda
      gerçek sızıntılar düzeltildi (VONNEUMANN/BOOT-003/PRIVESC-004/XXE-001/SC-003); kalan 20 SGT
      uyarısı yanlış-pozitif (karşılaştırma kartı, konu-adı yankısı, jenerik kelime). ✓
- [x] Flag/lab-değeri/exploit payload sızıntısı: **0** ✓
- [x] `<...>` HTML riski: **0** (THM-JS-002 `<script>`, `<ad>`/`<id>` yer tutucuları `&lt;`/`&gt;` ile kaçışlandı — edits.json) ✓
- [x] Bütünsel ↔ oda örtüşmesi: **224 Bütünsel kart, örtüşen=0** ✓
- [x] Interaktif (type) kart tek-komut: **şüpheli=0** (98 interaktif kartın hepsi tek-komut) ✓
- [x] .apkg zamanlama+revlog: 1382 kart zamanlaması + 1132 revlog gömülü, crt=1769302800 ✓
- [~] Near-duplicate (cross-path): net olanlar SILINECEK'e eklendi (ARP, CIA×3, systeminfo).
      Daha geniş Pre Security↔CS101 komut kartı örtüşmesi (whoami/systeminfo/ipconfig vb.) var;
      hepsi ayrı guid+geçmişe sahip → toplu silme yerine kullanıcı incelemesine bırakıldı.

## 8. TESLİMLER (spec §12)
- `siber_guvenlik_temelleri.apkg` (final; ara .apkg ÜRETME)
- `SILINECEK_KARTLAR.md` (repoda karşılığı olmayan/uzman-alanı kartlar; kullanıcı elle siler — spec §7)
- `ANKI_CALISMA_LOGU.md` (bu dosya)

## 9. `.anki-build/` ARTEFAKTLARI (kalıcı; gitignore'lu)
- `01_extract_inventory.py` … `06_aggregate.py` — analiz scriptleri
- `work/collection_live.sqlite` — orijinal koleksiyon (zstd'den açılmış; kaynak-of-truth)
- `inventory.json` — 1382 not, kanonik 7 alan + guid + hedef + deck + tags (BUG-FREE)
- `schedule.json` — guid → kart zamanlama; `revlog.json` — orig_cid → revlog satırları
- `notetype_probe.txt`, `_diag04.txt`, `aggregate.txt` — teşhis çıktıları

---

## 📦 FAZ 1 KAYDI (2026-07-10) — delta işi BİTTİ, final build BEKLİYOR
Bayraklar: THM_ODA_ALT_DESTE=KORU · SILINECEK_MODU=OTO_SIL_DUP · BUTUNSEL_REFINE=HAYIR · README_MOTTO=EKLE.
- **§2 Modül 01:** +20 kart (routing-nat-vpn + dns-derinlemesine tam tarandı). Bkz modül tablosu.
- **§4A mekanik denetim (tüm deste):** açılı-parantez=0 (edits.json), boş zorunlu alan=0, SIKI sızıntı
  taraması → 55 aday ama hepsi karşılaştırma-kartı yanlış-pozitifi veya "nedir/manuel" alt-dize kazası;
  gerçek sızıntı yalnız THM-OFF-* (zaten SILINECEK'te). Terminoloji uyumlu.
- **§4B üretken (yalnız Modül 01):** 8 NÜANS + 6 KESİŞİM eklendi.
- **§5 OTO_SIL_DUP:** 3 kesin cross-path dup `deltas/delete.json` ile build'den ÇIKARILDI
  (thm-c101-ne-04/THM-DEF-003/THM-WCLI-006); korunan eşleri geçmişiyle sağlam. 14 düşük-kalite/cihaz
  kartı destede kaldı (SILINECEK advisory). `build_final.py` artık `delete.json`'ı uygular.
- **§6 README:** "🧭 Persona / Motto" alt-bölümü eklendi (dört-katman tablosu). Mevcut misyon/PQC dokunulmadı.
- **§7 Yapı:** KORU — dokunulmadı.
- **Doğrulama (stale envanter üzerinde, mekanizma testi):** 1468 not, guid korunması 1379/1379 (KAYIP=0),
  silinen 3/3 doğru yok, mojibake=0, açılı-parantez=0, Bütünsel örtüşme=0, boş zorunlu=0. Persona haritası
  `work/verify_report.txt` §11'de. **FAZ 2 adayı (NÜANS+KESİŞİM=0): yalnız Modül 00** (02/09/10/11/14 seyrek).

## 📦 FAZ 2a KAYDI (2026-07-10) — persona-zayıf modül üretken derinleştirme (BUILD YOK)
Yalnız gerçek, repo-destekli NÜANS/KESİŞİM eklendi (kalite-kapılı; sayı için kart uydurulmadı).
Faz-1 delta'larına APPEND. Anti-örtüşme=0 (yeni Soru hiçbir mevcut kartla birebir eşleşmiyor).
**Repo .md değişmedi** — tüm açılar zaten repoda vardı (§2 zenginleştirme gerekmedi).
- **Modül 10 (+11):** av-edr-atlatma → AV/AMSI/EDR üç mantık, imza vs davranış (Pyramid), LOLBins,
  encoder≠evasion, AMSI deobf, log 4104 atlatmayı hükümsüzler, EDR süreç soy ağacı, beaconing/jitter;
  + persistence↔tespit, pivoting↔segmentasyon, CT logs↔pasif keşif. **persona 4→15.**
- **Modül 11 (+4):** logon type (4624) nüansı, şifreli trafik IDS'i kör eder→JA3/JA4, packing/entropi,
  RAM/LSASS fişi-çekme kuralı. **persona 4→8.**
- **Modül 03 (+1):** process injection (izolasyon kırma ↔ EDR hooking). 09 (+2): paylaşılan sorumluluk
  yanlış-yapılandırma/Capital One, VM vs konteyner kaçış zorluğu. 12 (+1): SMS-MFA/SIM-swap↔FIDO2.
  13 (+1): kök-neden vs belirti (WAF vs parametreli sorgu). 00 (+2, §6): veri=kod birleştirici kök,
  kodlama→WAF bypass. **14: +0 (lab-materyali, kalite-kapısı — zorlanmadı).**
- **Faz 2a sonrası persona (NÜANS+KESİŞİM):** 00:2 01:14 02:2 03:4 04:6 05:18 06:9 07:7 08:6 09:5
  10:15 11:8 12:4 13:3 14:1 · BT:162. (Kalan seyrek: 02/14 — komut-referansı ağırlıklı, kabul.)
- Kontrol: `.anki-build/faz2_check.py` (BUILD'siz; modül×katman + anti-örtüşme).

## ✅ FAZ 2b KAYDI (2026-07-12) — Bütünsel rafine + global dedup + FINAL BUILD
- **Taze export geldi** (schema 11 / collection.anki21, JSON models/decks). `05` şema-agnostik yapıldı;
  `build_final` media eski-format (düz JSON) desteği eklendi. Fresh crt/scheduling Jul-9 ile özdeş.
- **§1 Bütünsel rafine (Seçenek B):** 224 kartın guid/içeriği DEĞİŞMEDİ; 12 müfredat alt-destesi
  **7 güvenlik-temasına** yeniden atandı (placement APPEND, `gen_butunsel_placement.py`):
  T1 Temeller-Veri(40) T2 Ağ(46) T3 Web(27) T4 Kimlik-Kripto(9) T5 Saldırı Zinciri(46)
  T6 Savunma-Tespit(13) T7 İlkeler-Yönetişim(43). +3 sentez kartı (SGT-BUT-001/002/003:
  imza≠davranış birleştirici, çok-yüzeyli offline-kırma, AD saldırı zinciri).
- **§2 global dedup:** OWASP birebir-Soru ikizi (DESIGN/DATA-001) `edits.json` ile ayrıştırıldı;
  Linux whoami cross-path dup (THM-LCLI-006) advisory'ye eklendi. Kalan same-Soru gruplar =
  tasarım-gereği jenerik interaktif kalıplar ("Komutu yaz" vb.) — dup değil.
- **§3 FINAL BUILD:** `01→05→build_final→verify→gen_silinecek` çalıştı; çıktı repo köküne kopyalandı.
- **§4 DOĞRULAMA (final apkg):** notes=1493 · guid korunması **1379/1379, KAYIP=0** · silinen **3/3**
  db'de yok · boş zorunlu alan=0 · Bütünsel↔oda örtüşme=0 · kanonik not tipi=2 (`+`/CORE YOK) ·
  interaktif tek-komut · mojibake=0 · media (paste-…jpg) dahil · crt=1769302800 zamanlama gömülü.

## ✅ FAZ 3 KAYDI (2026-07-12) — Katman-1 son boşluk (race/TOCTOU + JWT saldırı) + repo zenginleştirme
- **Repo-önce (2 dosya değişti/eklendi — kullanıcı commit'leyecek):**
  - `03-isletim-sistemi-ici/surecler-ve-bellek.md`: yeni "§7 TOCTOU yarışı" bölümü (symlink→privesc,
    atomiklik/O_NOFOLLOW savunması, web-race'e simetrik link) + özet maddesi.
  - `04-web-guvenligi/zafiyet-siniflari/race-condition.md`: YENİ dosya (web limit-overrun, atomiklik/
    kilit savunması, TOCTOU'ya simetrik link). (İstenirse README/modül index'e link eklenebilir.)
- **+7 kart (persona-freni: mekanizma, silah-reçetesi yok):**
  - Web race: SGT-RACE-001 (limit-overrun KAVRAM), SGT-RACE-002 (atomiklik KESİŞİM) → 04.
  - TOCTOU: SGT-TOCTOU-001 (KAVRAM), SGT-TOCTOU-002 (symlink→privesc KESİŞİM) → 03.
  - JWT saldırı (federasyon-sso.md §3'ten): SGT-JWT-001 (alg:none), SGT-JWT-002 (RS256→HS256 karışıklığı),
    SGT-JWT-003 (stateless exp/iptal) → 06.
- Anti-örtüşme=0. Persona: 03→5, 04→7, 06→12.
- **NOT:** `dosya-yukleme-webshell.md` git'te 'D' görünüyor — bu oturum-öncesi Defender karantinası
  (bkz [[defender-webshell-false-positive]]), FAZ 3 değişikliği DEĞİL.

## 🧊 BİLİNÇLİ ERTELENEN (Katman 2/3 — uzmanlaşınca, common-core DEĞİL)
Bunlar geniş ortak-çekirdeğin parçası değildir; ilgili alanda uzmanlaşma başlayınca eklenir:
- **Cloud-native derinlik:** Kubernetes RBAC/pod-security, serverless saldırı yüzeyi.
- **Modern API yüzeyi:** GraphQL (introspection/derinlik saldırıları), mass-assignment, BOLA.
- **Active Directory derinliği:** forest trust sömürüsü, DCSync ayrıntı, unconstrained/constrained delegation.
- **OS-spesifik iç yapı:** Windows PEB/handle/token manipülasyonu, Linux ptrace/LD_PRELOAD.
- **Tasarım-tarafı tehdit modelleme:** STRIDE/DREAD/attack-tree uygulamalı.
> **Common-core FAZ 3 ile TAMAMLANMIŞTIR.**

## 🎉 SONUÇ / TESLİM
- `siber_guvenlik_temelleri.apkg` — repo kökü, final. `SILINECEK_KARTLAR.md` (3 kalıcı + 15 advisory).
- Kullanıcı import talimatı: aşağıdaki "TAM TEMİZ KURULUM" (rapor §7). Import sonrası: 2 not tipi,
  ~1493 kart, tüm tekrar geçmişi korunmuş.

### ▶️ TAZE EXPORT GELİNCE ÇALIŞTIRILACAK SIRA (KRİTİK — sadece build_final YETMEZ!)
`build_final.py`, `inventory.json`/`schedule.json`/`revlog.json`'u okur; bunlar ESKİ snapshot'tan
üretildi. Taze export'un zamanlamasını taşımak için önce yeniden çıkarım şart:
```
py = C:\Users\metin\AppData\Local\Programs\Python\Python312\python.exe
$env:PYTHONUTF8=1
& $py .anki-build\01_extract_inventory.py   # taze apkg → work/collection_live.sqlite
& $py .anki-build\05_build_inventory.py     # inventory/schedule/revlog YENİDEN
& $py .anki-build\build_final.py            # delta'ları uygula + zamanlama enjekte
& $py .anki-build\verify.py                 # §11 tekrar
& $py .anki-build\gen_silinecek.py          # SILINECEK tazele
cp .anki-build\work\siber_guvenlik_temelleri.apkg .\siber_guvenlik_temelleri.apkg
```
Sonra kullanıcı: eski `Siber Güvenlik` üst-destesini SİL → yeni apkg'yi "Import any learning
progress" AÇIK ile içe aktar. (Delta'lar kart_id ile eşleşir; guid'ler taze export'tan gelir.)

## AÇIK DURUM / SONRAKİ ADIM

**Bitti:** Ortam kurulumu; envanter (bug-free); 5→2 not tipi + pozisyonel alan eşleme; crt +
zamanlama + revlog çıkarımı; Anki import davranışı doğrulama; teslim modeli kararı (A);
16-modül deste iskeleti + THM→modül default eşleme; repo yapısı taraması (README/ROADMAP).

**✅ PIPELINE PoC BAŞARILI (2026-07-10):** `07_build.py` — genanki ile 1382 not (içerik
değişmeden) reorg + 2 not tipine birleştirildi, zamanlama+revlog enjekte edildi. Doğrulama:
notes=1382, cards=1382, revlog=1132, crt=1769302800, model_ids=[1980455173,1980455180],
**tüm 1382 guid birebir korundu**, zamanlaması olan kart=251, eşleşmeyen=0. Çıktı:
`work/poc_injected.apkg`. → **Geçmiş-taşıma hattı KANITLANDI; mimari risk kalmadı.**
Modül dağılımı: 00:139 01:191 02:203 03:0 04:133 05:141 06:27 07:23 08:55 09:33 10:88 11:100
12:0 13:0 14:25 15:0 butun:224. (03/12/13/15 = repodan YENİ kart gelecek.)

**FINAL BUILD İÇİN DÜZELTİLECEK (PoC'de görüldü):**
- Media adı regex'i protobuf'tan başına "2" ekliyor ("2paste-…jpg"). Doğru ad
  `paste-86d591f0e6b61bcf6e6ab5778a07b8c4fcd3ab50.jpg`. `<img src>` referansıyla eşleşmesi
  için regex'i düzelt (uzunluk önekini at). Anki'de import edilemedi (test ortamı yok) — yapı
  doğrulaması yapıldı.
- genanki "Default" destesini de ekliyor; final'de kaldır/yok say.

**✅ DELTA PIPELINE KURULDU (2026-07-10):** `build_final.py` — inventory + module_map +
`deltas/{placement,edits,new_cards,silinecek}.json` → nihai apkg + zamanlama enjeksiyonu +
doğrulama. Doğrulandı: notes=1391 (1382+9 yeni), tüm mevcut guid korundu, model_ids doğru,
zamanlama+revlog tam, media adı düzeltildi (`paste-…jpg`). `gen_silinecek.py` →
`SILINECEK_KARTLAR.md`. **İçerik fazı artık bu delta dosyalarına yazarak ilerliyor.**

### Delta dosya sözleşmesi (`.anki-build/deltas/`)
- `placement.json`: `{kart_id: {module, subdeck?}}` — module_map'i ezer (kart taşıma).
- `edits.json`: `{kart_id: {alan: yeni_deger}}` — mevcut kart içerik/sızdırma düzeltmesi.
- `new_cards.json`: `[{kart_id(SGT-…), target, module, subdeck?, 7 alan, tags}]` — yeni kart.
- `silinecek.json`: `[{kart_id, module, reason}]` — TAVSİYE; kart destede kalır, MD'ye yazılır.

### === Modül 00 kaydı (BİTTİ) ===
- **Kalan (00'da):** THM-PC-* (11, donanım+boot), THM-DR-* (11, ikili/hex/veri-temsili).
- **Taşındı (27):** THM-HACK-001..010 → 10 · THM-BDEF-001..009,013 → 11, -010 → 07, -011/012 → 08 ·
  THM-DEF-003(CIA) → 08, -009/010/011(SOC/TI/DFIR) → 11.
- **Silinecek-aday (14, hepsi GEÇMİŞ VAR):** THM-OFF-005/006/007/008/012 (düşük kalite/tekrar/sızdırma),
  THM-CT-001..009 (cihaz türleri — repo 00 kapsamı dışı; kullanıcı vetosu mümkün).
- **Yeni (9):** SGT-DONANIM-001/002/003 (CPU alt-birim, fetch-decode-execute, bellek hiyerarşisi),
  SGT-VONNEUMANN-001 (kod=veri kök nedeni), SGT-KODLAMA-001/002 (ASCII, UTF-8),
  SGT-BOOT-001/002/003 (Secure Boot, TPM, bootkit/firmware persistence).
- **NOT:** THM-BDEF/HACK/DEF taşındıkları modül işlenirken içerik-doğrulaması + olası
  ek silme/düzeltme alacak (şu an sadece yerleşim düzeltildi).

**Sıradaki adımlar (öneri sıra):**
1. ✅ ~~Pipeline PoC~~ — BİTTİ. ✅ ~~Delta pipeline + Modül 00~~ — BİTTİ.
2. **İçerik fazı, kalan modüller (01→15 + Bütünsel):** her repo dosyasını oku → kavram listesi çıkar →
   mevcut kartla eşle (repoda VAR+deste VAR=güncelle / VAR+YOK=yeni / YOK+VAR=SILINECEK).
   Her kartın modül destesi + notetype + guid/kart_id'sini kesinleştir. İçeriği repoya göre
   yaz (tasarım kuralları §6). Her modül bitince bu logu güncelle (aşağıya modül tablosu).
3. **Bütünsel** kartları repo-geneli yeniden üret (spec §10).
4. **Doğrulama** (§7) + **teslimler** (§8).

### ✅ REORG EŞLEMESİ TAMAMLANDI (ilk taslak — içerik fazında kart-bazlı doğrulanacak)
`module_map.py` her mevcut kartı bir modüle eşliyor; **gerçek fallback = 0** (kalan "16 c101"
uyarısı sahte pozitif: `08_worksheets.py:is_fallback` yeni `thm-c101-search→10` kuralını
yansıtmıyor, ama `module_of` doğru eşliyor). Modül-bazlı mevcut-kart çalışma sayfaları:
`.anki-build/worksheets/mod_<NN>.md` (içerik fazının diff yüzeyi).

**Mevcut kart dağılımı (draft reorg):**
00:63 · 01:196 · 02:226 · 03:0 · 04:133 · 05:141 · 06:27 · 07:23 · 08:55 · 09:33 · 10:112 ·
11:110 · 12:6 · 13:8 · 14:25 · 15:0 · Bütünsel:224  (Σ=1382).
→ 03/12/13/15 büyük ölçüde repodan **YENİ** kartlarla dolacak.

### İçerik fazı — kart-bazlı iş (her modül için)
Her modülde: (a) repo `.md` dosyalarını oku, kavram/komut/araç listesi çıkar; (b)
`worksheets/mod_<NN>.md`'deki mevcut kartlarla eşle → **repoda VAR+kart VAR**=içeriği repoya
göre güncelle (guid+kart_id korunur) · **VAR+YOK**=yeni kart (SGT- id) · **YOK+VAR**=
`SILINECEK_KARTLAR.md`'ye ekle (uzman-alanı/repoda yok); (c) modül destesi + notetype +
tasarım kurallarını (§6) uygula; (d) bu tabloyu güncelle.

### Modül ilerleme tablosu (içerik fazı)
| Modül | Durum | Mevcut kart | Not |
|---|---|---:|---|
| 00-baslangic | ✅ BİTTİ | 45 (36 kalan +9 yeni) | Bkz aşağı "Modül 00 kaydı". 27 kart taşındı, 14 silinecek-aday, 9 yeni. |
| 01-ag-networking | ✅ BİTTİ (FAZ1) | 224 | +11 kablosuz + **+20 (FAZ1)**: NAT/PAT, longest-prefix, statik/dinamik routing, BGP hijack, default-deny, VLAN hopping, VPN türleri/split-tunnel, DNS PTR/NS/DNSSEC/DoH-DoT/cache-poisoning/tunneling/hosts + dig interaktif. Persona: 8 NÜANS + 6 KESİŞİM. gobuster→04, hydra→10, ne-04 SİLİNDİ. |
| 02-linux-windows | ✅ BİTTİ | 216 | Zaten doygun (linux/windows/AD/PS/CLI/shells). 10 OS-internals kartı (thm-core-os-01..09,17) → 03'e taşındı. Yeni kart yok. İzin kartları (rwx/SUID/sticky/ACL/UAC os-10..16) 02'de kaldı. |
| 03-isletim-sistemi-ici | ✅ BİTTİ | 20 | 10 taşınan (süreç/bellek/user-kernel/syscall) + 10 YENİ (SGT-MEM-001..010: buffer overflow mekanizma, kök neden, zafiyetli C fn, ASLR, DEP/NX, canary, ROP, UAF, format string, bellek-güvenli diller). |
| 04-web-guvenligi | ✅ BİTTİ | 141 | Zaten doygun (OWASP 2025 tam, webvuln core: SQLi/XSS/CSRF/SSRF/IDOR/cmdi/LFI-RFI/SOP/CORS/JWT). +5 dosya-yükleme/webshell (SGT-UPLOAD-001..005) +2 XXE (SGT-XXE-001/002). **Not:** dosya-yukleme-webshell.md diskte Defender karantinasında; `git show HEAD:` ile (payload filtreli) okundu — bkz [[defender-webshell-false-positive]]. |
| 05-kriptografi | ✅ BİTTİ | 132 | Zaten doygun (crypto CORE 61 kart: sim/asim/hash/PKI/DH/imza + **PQC baseline** crypto-40..61: Shor/Grover/harvest/lattice/LWE/FIPS203-205/agility/CNSA2.0). **PQC'ye ek derinlik EKLENMEDİ** (kullanıcı düzeltmesi). THM-DE-001..009 (encoding) → **00'a taşındı** (kodlama≠kripto). Dup SGT-KODLAMA-001 silindi. |
| 06-iam | ✅ BİTTİ | 29 | iam(core) doygun (AAA/MFA/TOTP/FIDO2/SSO/OAuth/OIDC/SAML/RBAC-ABAC-DAC-MAC/PAM/Kerberos/LDAP). +2 Zero Trust baseline (SGT-ZT-001/002). |
| 07-tehdit-modelleme | ✅ BİTTİ | 24 | fw(core) tam doygun (ATT&CK/KillChain/UnifiedKC/Pyramid/Diamond/IOC-IOA/TTP/threat-intel/ATLAS) + BDEF-010(attack chain) taşındı. Yeni kart yok. |
| 08-grc | ✅ BİTTİ | 58 | Doygun: CIA(derin), güvenlik ilkeleri (DAD/Parkerian/Bell-LaPadula/Biba/Clark-Wilson/defense-in-depth/least-priv/SoD), risk (quant/qual/SLE-ARO-ALE/appetite/residual), NIST CSF 2.0, ISO 27001, PCI/HIPAA/GDPR, STRIDE, threat actors/APT, training. Yeni kart yok. **NOT: CIA ×3 (THM-CIA-001/SECPRIN-001/DEF-003) → global dedup pass'e bırakıldı.** |
| 09-cloud | ✅ BİTTİ | 37 | cloud/virtualisation/shared-resp/hypervisor/VM-container doygun. +4 konteyner güvenliği (SGT-CNTR-001..004: namespaces/cgroups, escape, escape yolları, savunma). |
| 10-pentest | ✅ BİTTİ (F1+F2a) | 145 | F1: privesc + AD saldırıları (11). **F2a: +11 KESİŞİM/NÜANS** (av-edr/beaconing/LOLBins/persistence/pivoting/CT-logs). persona 4→**15**. |
| 11-soc | ✅ BİTTİ (F1+F2a) | 125 | F1: +2 malware. **F2a: +4** (logon-type, JA3/şifreli-IDS, packing/entropi, RAM/LSASS). persona 4→**8**. thm-core-tool→14 taşındı. |
| 12-sosyal-muhendislik | ✅ BİTTİ | 13 | phishing(core) 6 + **7 YENİ** (SGT-SE-001..007: SE neden etkili, Cialdini, BEC, SMTP-spoofing, DMARC politikaları, header spf/dkim/dmarc=fail üçlüsü, typosquatting). |
| 13-guvenli-kodlama | ✅ BİTTİ | 13 | seccode(core) 8 + **5 YENİ** (SGT-SC-001..005: güvenlik=kalite, output encoding, fail securely/A10, don't-roll-crypto, secure defaults). Birleştirici "zafiyet→ilke" görüşü Bütünsel'e bırakıldı. |
| 14-scripting | ✅ BİTTİ | 31 | py/js/sql demo (25) + taşınan regex/git (thm-core-tool 4) + **2 YENİ** (SGT-REGEX-001 karakter sınıfı, SGT-GIT-001 .gitignore-sır). Pratik scripting = lab materyali (README), fazla kart yok. |
| 15-projeler | ✅ (referans) | 0 | Kart yok (portföy projeleri referans modülü). |
| Bütünsel | ✅ BİTTİ (F2b) | 227 | 224 kart (guid/içerik korundu) → **7 güvenlik-teması (T1-T7)** yeniden atandı (12 müfredat alt-destesinden). +3 sentez (SGT-BUT-001/002/003). Oda↔Bütünsel örtüşme=0. |
