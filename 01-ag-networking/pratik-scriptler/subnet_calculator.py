#!/usr/bin/env python3
"""
subnet_calculator.py — CIDR / Subnet Hesaplayıcı (eğitim amaçlı)
================================================================
Bir CIDR bloğu (ör. 192.168.1.100/26) verildiğinde ağ adresi, broadcast,
kullanılabilir host aralığı, maske, host sayısı ve ikili gösterimi hesaplar.

Amaç: subnetting-cidr.md'de ELLE çözdüğün problemleri DOĞRULAMAK.
Önce elle çöz, sonra bu scriptle kontrol et — öğrenme elle olur.

Kullanım:
    python3 subnet_calculator.py 192.168.1.100/26
    python3 subnet_calculator.py 10.0.0.0/8
    python3 subnet_calculator.py            # etkileşimli mod

Bağımlılık yok — yalnızca Python 3 standart kütüphanesi (ipaddress).
Python 3.6+ ile çalışır.
"""

import sys
import ipaddress

# Windows konsolunda Türkçe karakterlerin bozulmaması için çıktıyı UTF-8'e al.
# (Python 3.7+; eski sürümlerde sessizce atlanır.)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def ikili_goster(ip: ipaddress.IPv4Address) -> str:
    """Bir IPv4 adresini noktalı ikili (binary) biçimde döndürür.

    Örn. 192.168.1.0 -> '11000000.10101000.00000001.00000000'
    Subnetting'i ikili düşünmeyi görselleştirmek için.
    """
    # Her okteti 8 bitlik (soldan sıfır dolgulu) ikiliye çevir.
    return ".".join(f"{int(oktet):08b}" for oktet in str(ip).split("."))


def hesapla(cidr: str) -> None:
    """Verilen CIDR bloğu için tüm subnetting bilgilerini yazdırır."""
    try:
        # strict=False: host bitleri dolu bir adres verilse de (ör. .100/26)
        # ipaddress bunu içeren AĞA yuvarlar; hata fırlatmaz.
        ag = ipaddress.ip_network(cidr, strict=False)
    except ValueError as hata:
        print(f"[!] Geçersiz CIDR: {cidr}  ({hata})")
        return

    onek = ag.prefixlen            # /24 -> 24
    host_biti = ag.max_prefixlen - onek   # IPv4 için 32 - onek
    toplam = ag.num_addresses      # 2^host_biti

    print("=" * 60)
    print(f"  Girdi          : {cidr}")
    print(f"  Ağ (network)   : {ag.network_address}/{onek}")
    print(f"  Maske          : {ag.netmask}")
    print(f"  Wildcard maske : {ag.hostmask}")
    print(f"  Broadcast      : {ag.broadcast_address}")
    print(f"  Önek / host bit: /{onek}  ({host_biti} host biti)")
    print(f"  Toplam adres   : {toplam}  (2^{host_biti})")

    # Kullanılabilir host sayısı ve aralığı.
    # /31 ve /32 özel durumdur (bkz. subnetting-cidr.md, RFC 3021).
    if host_biti >= 2:
        kullanilabilir = toplam - 2  # ağ + broadcast düşülür
        hostlar = list(ag.hosts())
        print(f"  Kullanılabilir : {kullanilabilir}  (2^{host_biti} - 2)")
        print(f"  İlk host       : {hostlar[0]}")
        print(f"  Son host       : {hostlar[-1]}")
    elif onek == 31:
        # RFC 3021: nokta-nokta linkte 2 adresin ikisi de host.
        adresler = list(ag)
        print(f"  Kullanılabilir : 2  (RFC 3021 — nokta-nokta, broadcast yok)")
        print(f"  Host'lar       : {adresler[0]}  ve  {adresler[1]}")
    else:  # /32
        print(f"  Kullanılabilir : 1  (tek host / host route)")

    print("-" * 60)
    print(f"  Ağ (ikili)     : {ikili_goster(ag.network_address)}")
    print(f"  Maske (ikili)  : {ikili_goster(ag.netmask)}")
    print("=" * 60)


def main() -> None:
    if len(sys.argv) >= 2:
        # Komut satırından bir veya daha fazla CIDR
        for cidr in sys.argv[1:]:
            hesapla(cidr)
    else:
        # Etkileşimli mod
        print("CIDR gir (ör. 192.168.1.100/26), çıkmak için boş bırak:")
        while True:
            try:
                cidr = input("cidr> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not cidr:
                break
            hesapla(cidr)


if __name__ == "__main__":
    main()
