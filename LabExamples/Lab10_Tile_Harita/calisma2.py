"""
Lab 10 - Çalışma 2 Başlangıç Kodu
CSV Haritası ve Grid Dönüşümü

Bu dosya Lab 10 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- csv modülü ile harita yükleme
- Piksel -> grid dönüşümü (//)
- Fare tıklaması ile tile düzenleme

Lab: 10 - Tile-Based Oyun Dünyası
Çalışma: 2 - CSV Haritası ve Grid Dönüşümü

Çalıştırma: uv run python calisma2.py
"""

import csv
from pathlib import Path

import pygame

TILE = 32
RENKLER = {
    0: (140, 80, 40),
    1: (80, 180, 80),
    2: (120, 120, 120),
    3: (60, 120, 220),
    4: (240, 230, 140),
}


def harita_yukle(yol):
    """CSV dosyasından 2B int listesi döndürür.

    GOREV 3: Doğrulama ekle. Tüm satırlar aynı uzunlukta olmalıdır.
    Aksi halde ValueError fırlat:
        raise ValueError(f"Satir {i}: uzunluk hatali")
    """
    with open(yol, newline="") as f:
        harita = [[int(x) for x in row] for row in csv.reader(f) if row]

    # GOREV 3: Buraya doğrulama ekle
    # if not harita: raise ...
    # beklenen = len(harita[0])
    # for i, satir in enumerate(harita): ...

    return harita


def main():
    pygame.init()

    yol = Path(__file__).parent / "harita.csv"
    harita = harita_yukle(yol)
    gen = len(harita[0]) * TILE
    yuk = len(harita) * TILE

    ekran = pygame.display.set_mode((gen, yuk + 40))
    pygame.display.set_caption("Lab 10 - Çalışma 2")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            # GOREV 4: Fare ile düzenleme
            # elif olay.type == pygame.MOUSEBUTTONDOWN:
            #     px, py = olay.pos
            #     if py < yuk:
            #         col = px // TILE
            #         row = py // TILE
            #         if olay.button == 1:    # sol tık -> taş
            #             harita[row][col] = 2
            #         elif olay.button == 3:  # sağ tık -> çim
            #             harita[row][col] = 1

        for r, satir in enumerate(harita):
            for c, tid in enumerate(satir):
                pygame.draw.rect(ekran, RENKLER[tid],
                                 (c * TILE, r * TILE, TILE, TILE))

        # Fare hover tile'ını vurgula
        fx, fy = pygame.mouse.get_pos()
        if fy < yuk:
            col = fx // TILE
            row = fy // TILE
            pygame.draw.rect(ekran, (255, 255, 0),
                             (col * TILE, row * TILE, TILE, TILE), 2)
            bilgi = f"piksel=({fx},{fy}) grid=({col},{row})"
        else:
            bilgi = "Fareyi harita üzerine getir"

        pygame.draw.rect(ekran, (10, 10, 20), (0, yuk, gen, 40))
        ekran.blit(font.render(bilgi, True, (255, 255, 255)),
                   (10, yuk + 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
