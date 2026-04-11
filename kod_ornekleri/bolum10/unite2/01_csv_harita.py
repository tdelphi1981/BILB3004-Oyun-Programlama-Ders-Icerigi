"""
CSV Dosyasından Harita Yükleme

Bu program, 2B liste yerine harita verisini dışarıda bir CSV
dosyasından okur. Böylece kodu değiştirmeden haritayı değiştirebilirsin.
CSV formatı basit: her satır bir grid satırı, virgülle ayrılmış tile ID'ler.

Öğrenilecek kavramlar:
- Python csv modülü (csv.reader)
- Metin -> int dönüşümü
- Dosya yolunu script konumuna göre çözme

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 2 - Harita Oluşturma

Çalıştırma: python 01_csv_harita.py
Gereksinimler: pygame, harita.csv (aynı dizinde)
"""

import csv
from pathlib import Path

import pygame

TILE = 32

RENKLER = {
    0: (140, 80, 40),    # topraksı (yol)
    1: (80, 180, 80),    # çim
    2: (120, 120, 120),  # taş duvar
    3: (60, 120, 220),   # su
    4: (240, 230, 140),  # altın
}


def harita_yukle(yol):
    """CSV dosyasından 2B int listesi döndürür."""
    harita = []
    with open(yol, "r", encoding="utf-8") as f:
        okuyucu = csv.reader(f)
        for satir in okuyucu:
            if not satir:
                continue
            harita.append([int(hucre) for hucre in satir])
    return harita


def harita_ciz(ekran, harita):
    for r, satir in enumerate(harita):
        for c, tile_id in enumerate(satir):
            renk = RENKLER.get(tile_id, (0, 0, 0))
            pygame.draw.rect(ekran, renk,
                             (c * TILE, r * TILE, TILE, TILE))


def main():
    pygame.init()

    # Script'in kendi dizinindeki harita.csv dosyasını bul
    dosya_yolu = Path(__file__).parent / "harita.csv"
    harita = harita_yukle(dosya_yolu)
    print(f"[OK] Harita yüklendi: {len(harita[0])}x{len(harita)}")

    gen = len(harita[0]) * TILE
    yuk = len(harita) * TILE
    ekran = pygame.display.set_mode((gen, yuk))
    pygame.display.set_caption("CSV Haritası")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        ekran.fill((0, 0, 0))
        harita_ciz(ekran, harita)

        bilgi = font.render("harita.csv dosyasından yüklendi",
                            True, (255, 255, 255))
        ekran.blit(bilgi, (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
harita.csv içeriğine göre 20x15 grid bir pencere açılır. Taş duvarla
çevrili, içinde bir yapı (topraksı hücrelerle bir oda ve ortasında
altın tile), bir su birikintisi görülür. Terminalde harita boyutu yazar.
"""
