"""
CSV Parse Detayı - Ham csv Modülü Kullanımı

Bu program pygame kullanmadan CSV dosyasından harita verisini
okumanın farklı yollarını gösterir. Aldığımız veriyi terminalde
güzel biçimde yazdırır.

Öğrenilecek kavramlar:
- csv.reader vs pathlib
- list comprehension ile tip dönüşümü
- Harita doğrulaması (tüm satırlar aynı uzunlukta mı?)

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 2 - Harita Oluşturma

Çalıştırma: python 02_csv_parse.py
Gereksinimler: (sadece standart kütüphane)
"""

import csv
from pathlib import Path


def harita_yukle(yol):
    """CSV dosyasından 2B int listesi okur."""
    with open(yol, newline="", encoding="utf-8") as f:
        return [[int(h) for h in row] for row in csv.reader(f) if row]


def harita_dogrula(harita):
    """Tüm satırların aynı uzunlukta olup olmadığını kontrol eder."""
    if not harita:
        return False, "Harita boş"
    beklenen = len(harita[0])
    for i, satir in enumerate(harita):
        if len(satir) != beklenen:
            return False, f"Satır {i} uzunluğu hatalı: {len(satir)} (beklenen {beklenen})"
    return True, f"{len(harita)}x{beklenen} geçerli harita"


def harita_istatistik(harita):
    """Her tile ID'sinin kaç kere kullanıldığını sayar."""
    sayac = {}
    for satir in harita:
        for tile_id in satir:
            sayac[tile_id] = sayac.get(tile_id, 0) + 1
    return sayac


def harita_yazdir(harita):
    """Konsola ASCII görünüm verir."""
    semboller = {0: ".", 1: "#", 2: "X", 3: "~", 4: "$"}
    for satir in harita:
        print("".join(semboller.get(h, "?") for h in satir))


def main():
    yol = Path(__file__).parent / "harita.csv"
    harita = harita_yukle(yol)

    gecerli, mesaj = harita_dogrula(harita)
    if gecerli:
        print(f"[OK] {mesaj}")
    else:
        print(f"[X] {mesaj}")
        return

    print()
    print("Tile sayıları:")
    for tile_id, sayi in sorted(harita_istatistik(harita).items()):
        print(f"  ID {tile_id}: {sayi} tile")

    print()
    print("ASCII harita:")
    harita_yazdir(harita)


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
[OK] 15x20 geçerli harita

Tile sayıları:
  ID 0: 8 tile
  ID 1: 183 tile
  ...

ASCII harita:
XXXXXXXXXXXXXXXXXXXX
X##################X
...
"""
