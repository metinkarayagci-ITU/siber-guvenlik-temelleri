#!/usr/bin/env python3
"""
port_tarayici.py — Basit TCP Port Tarayıcı (eğitim amaçlı)
==========================================================
Bir hedefteki TCP portlarının açık olup olmadığını, standart 'socket'
kütüphanesiyle TCP connect (tam 3-way handshake) yöntemiyle test eder.

Bu, nmap'in yaptığı işin en yalın halidir. Amaç, tcp-ip-protokoller.md'deki
üçlü el sıkışmasının pratikte nasıl port keşfine dönüştüğünü GÖRMEK.

⚠️  ETİK VE YASAL UYARI
    Bu aracı YALNIZCA sana ait veya TARAMASINA AÇIKÇA İZİN VERİLMİŞ
    sistemlerde kullan. İzinsiz port taraması birçok ülkede suçtur.
    Güvenli test hedefleri: 127.0.0.1 (kendi makinen), scanme.nmap.org
    (Nmap projesinin bilerek açtığı yasal test sunucusu).
    Bkz. 10-pentest-metodolojisi/metodoloji-ve-rules-of-engagement.md

Kullanım:
    python3 port_tarayici.py 127.0.0.1
    python3 port_tarayici.py scanme.nmap.org 20 100
    python3 port_tarayici.py 192.168.1.1 --ports 22,80,443,3389

Bağımlılık yok — yalnızca Python 3 standart kütüphanesi.
"""

import sys
import socket
from datetime import datetime

# Windows konsolunda Türkçe karakterlerin bozulmaması için çıktıyı UTF-8'e al.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# En sık karşılaşılan portların servis adları (tcp-ip-protokoller.md tablosu).
BILINEN_SERVISLER = {
    20: "FTP-data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP", 80: "HTTP", 110: "POP3", 143: "IMAP",
    389: "LDAP", 443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    8080: "HTTP-alt", 8443: "HTTPS-alt",
}


def port_tara(hedef_ip: str, port: int, zaman_asimi: float = 1.0) -> bool:
    """Tek bir TCP portunu tarar. Açıksa True döner.

    socket.connect_ex(), bağlantı başarılıysa 0 döndürür; bu, TCP üçlü
    el sıkışmasının tamamlandığı (port AÇIK) anlamına gelir. Sıfırdan
    farklı bir değer = kapalı/filtreli.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(zaman_asimi)
        sonuc = s.connect_ex((hedef_ip, port))
        return sonuc == 0


def hedefi_coz(hedef: str) -> str:
    """Alan adını IP'ye çevirir (DNS çözümleme). Hata olursa çıkar."""
    try:
        ip = socket.gethostbyname(hedef)
        if ip != hedef:
            print(f"[i] {hedef} -> {ip} (DNS çözümlendi)")
        return ip
    except socket.gaierror:
        print(f"[!] '{hedef}' çözümlenemedi. Ad/bağlantıyı kontrol et.")
        sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        print("Örnek: python3 port_tarayici.py scanme.nmap.org 20 100")
        sys.exit(1)

    hedef = sys.argv[1]

    # Port aralığını belirle: --ports listesi VEYA baslangic/bitis VEYA varsayılan.
    if "--ports" in sys.argv:
        idx = sys.argv.index("--ports")
        portlar = [int(p) for p in sys.argv[idx + 1].split(",")]
    elif len(sys.argv) >= 4:
        baslangic, bitis = int(sys.argv[2]), int(sys.argv[3])
        portlar = range(baslangic, bitis + 1)
    else:
        # Varsayılan: en kritik servis portları
        portlar = sorted(BILINEN_SERVISLER.keys())

    hedef_ip = hedefi_coz(hedef)

    print("=" * 55)
    print(f"  Hedef      : {hedef} ({hedef_ip})")
    print(f"  Port sayısı: {len(list(portlar))}")
    print(f"  Başlangıç  : {datetime.now():%H:%M:%S}")
    print("=" * 55)

    acik_sayisi = 0
    try:
        for port in portlar:
            if port_tara(hedef_ip, port):
                servis = BILINEN_SERVISLER.get(port, "bilinmiyor")
                print(f"  [+] {port:>5}/tcp  AÇIK   ({servis})")
                acik_sayisi += 1
    except KeyboardInterrupt:
        print("\n[!] Kullanıcı tarafından durduruldu.")
        sys.exit(0)

    print("=" * 55)
    print(f"  Tamamlandı: {acik_sayisi} açık port bulundu "
          f"({datetime.now():%H:%M:%S})")


if __name__ == "__main__":
    main()
