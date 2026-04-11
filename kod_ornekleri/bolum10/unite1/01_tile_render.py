"""
İlk Tile Haritası - Elle Tanımlanmış 2B Liste

Bu program, elle yazılmış bir 2B listeyi tile tile çizmeyi gösterir.
Harita verisi Python listesinde saklanır; her rakam farklı bir tile
tipini temsil eder (0 = boş, 1 = çim, 2 = taş, 3 = su).

Öğrenilecek kavramlar:
- 2B liste ile harita temsili
- İç içe for döngüsü ile tile yerleştirme
- Grid -> piksel dönüşümü (row * TILE, col * TILE)

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 1 - Tile Sistemi Temelleri

Çalıştırma: python 01_tile_render.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
TILE = 32          # Her tile 32x32 piksel
GENISLIK = 640     # 20 tile genişliği
YUKSEKLIK = 480    # 15 tile yüksekliği

# Renk paleti (tile_id -> renk)
RENKLER = {
    0: (30, 30, 50),     # boş (koyu mavi)
    1: (80, 180, 80),    # çim (yeşil)
    2: (120, 120, 120),  # taş (gri)
    3: (60, 120, 220),   # su (mavi)
}

# Harita verisi (15 satır x 20 sütun)
HARITA = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 2, 1, 2, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 2, 1, 2, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 2, 1, 2, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 2, 2, 2, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


def harita_ciz(ekran, harita):
    """2B listeyi ekrana tile tile çizer."""
    for satir_idx, satir in enumerate(harita):
        for sutun_idx, tile_id in enumerate(satir):
            renk = RENKLER.get(tile_id, (0, 0, 0))
            x = sutun_idx * TILE
            y = satir_idx * TILE
            pygame.draw.rect(ekran, renk, (x, y, TILE, TILE))
            # Izgara çizgileri (hafif)
            pygame.draw.rect(ekran, (20, 20, 30), (x, y, TILE, TILE), 1)


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("İlk Tile Haritası")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        ekran.fill((0, 0, 0))
        harita_ciz(ekran, HARITA)

        bilgi = font.render(
            f"Grid: {len(HARITA[0])}x{len(HARITA)} | Tile: {TILE}px",
            True, (255, 255, 255)
        )
        ekran.blit(bilgi, (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
640x480 piksel bir pencere açılır. Taş duvarlarla çevrili,
içinde bir su birikintisi ve birkaç yapının bulunduğu küçük
bir harita görülür. Izgara çizgileri tile sınırlarını belli eder.
"""
