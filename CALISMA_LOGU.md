# 📋 Çalışma Logu (Derinleştirme ve Bağlama Turu)

Bu dosya, reponun "tam kapsamlı hale getirme ve kavramlar arası bağlantı kurma" turunun ilerleme kaydını tutar. Her modül işlendiğinde: hangi dosyalar değişti, hangi kavramlar eklendi/genişletildi, hangi ilişkiler kuruldu, hangi dış kaynaklar doğrulandı.

**Çalışma prensibi:** Modüller README sırasıyla (00 → 15) işlenir, her modül sonunda ayrı commit atılır. Kavramlar arası bağlantı düzyazı içinde ve simetriktir (X↔Y hem X'te hem Y'de). Dış iddialar satır-içi kaynakla doğrulanır.

---

## İlerleme

### 00-baslangic ✅
- **Değişen dosyalar:** `bilgisayar-temelleri.md`, `terminoloji-sozlugu.md`
- **Eklenen/genişletilen kavramlar:** Von Neumann darboğazı ve "kod/veri ayrılmaması" birleştirici teması; önyükleme (boot) zinciri, firmware (UEFI/BIOS), bootkit, Secure Boot, TPM, güven zinciri (chain of trust); UTF-8 çok-byte yapısı ve WAF atlatma bağlantısı.
- **Kurulan ilişkiler:** von Neumann → buffer overflow (03) + enjeksiyon (04) + Spectre (03); UTF-8 → WAF atlatma (04); hash → kripto (05) + SAM/shadow (02) + hashdump/John (10); Secure Boot → dijital imza (05); TPM → FIDO2 (06); güven zinciri → PKI (05); kernel/user → syscall (03) + Linux/Windows (02).
- **Dış kaynak:** UTF-8 için RFC 3629 satır-içi alıntılandı.
- **Sözlük:** "Sistem ve donanım temelleri" kategorisi eklendi (7 yeni terim).
- **Not:** Simetrik ters bağlantılar (ör. 03'te von Neumann'a, 05'te Secure Boot'a geri değinme) ilgili modüller işlenirken tamamlanacak.

### 01-ag-networking
- **Durum:** ⏳ sırada
