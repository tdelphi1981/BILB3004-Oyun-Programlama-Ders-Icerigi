"""
Grid <-> Piksel Dönüşümü

Fare tıklamasının grid hücresini nasıl bulacağımızı ve tersine
grid koordinatından piksel koordinatına nasıl gideceğimizi
gösterir. "Taş at" oyunu: fare ile tıkladığın hücreye taş koyar.

Öğrenilecek kavramlar:
- piksel -> grid: (px // TILE, py // TILE)
- grid -> piksel: (col * TILE, row * TILE)
- Grid sınır kontrolü (0 <= col < GENISLIK, ...)

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 1 - Tile Sistemi Temelleri

Çalıştırma: python 03_grid_donusum.py
Gereksinimler: pygame
"""

import pygame

TILE = 40
GRID_GEN = 16   # sütun sayısı
GRID_YUK = 12   # satır sayısı
GENISLIK = TILE * GRID_GEN
YUKSEKLIK = TILE * GRID_YUK + 60  # alt bilgi satırı


def piksel_to_grid(px, py):
    """Piksel koordinatını grid (col, row) koordinatına çevirir."""
    col = px // TILE
    row = py // TILE
    return col, row


def grid_to_piksel(col, row):
    """Grid koordinatından tile'ın sol üst köşeye piksel konumunu verir."""
    return col * TILE, row * TILE


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Grid-Piksel Dönüşümü")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    # Yerleştirilen taşlar: set of (col, row)
    taslar = set()

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if olay.button == 1:  # sol tık -> taş koy/kaldır
                    px, py = olay.pos
                    if py < TILE * GRID_YUK:  # oyun alanı içinde mi?
                        col, row = piksel_to_grid(px, py)
                        if (col, row) in taslar:
                            taslar.remove((col, row))
                        else:
                            taslar.add((col, row))

        ekran.fill((30, 30, 50))

        # Izgarayı çiz
        for r in range(GRID_YUK):
            for c in range(GRID_GEN):
                x, y = grid_to_piksel(c, r)
                pygame.draw.rect(ekran, (50, 50, 80), (x, y, TILE, TILE), 1)

        # Taşları çiz
        for (c, r) in taslar:
            x, y = grid_to_piksel(c, r)
            pygame.draw.rect(ekran, (120, 120, 120), (x + 4, y + 4,
                                                       TILE - 8, TILE - 8))
            pygame.draw.rect(ekran, (200, 200, 200), (x + 4, y + 4,
                                                       TILE - 8, TILE - 8), 2)

        # Fare konumu -> hover tile
        fx, fy = pygame.mouse.get_pos()
        if fy < TILE * GRID_YUK:
            hc, hr = piksel_to_grid(fx, fy)
            hx, hy = grid_to_piksel(hc, hr)
            pygame.draw.rect(ekran, (255, 255, 0), (hx, hy, TILE, TILE), 2)

            bilgi = (f"Fare piksel=({fx}, {fy})   "
                     f"grid=({hc}, {hr})   "
                     f"tile sol-üst=({hx}, {hy})")
        else:
            bilgi = "Oyun alanının içine tıkla: taş koy/kaldır"

        # Alt panel
        pygame.draw.rect(ekran, (10, 10, 20),
                         (0, TILE * GRID_YUK, GENISLIK, 60))
        ekran.blit(font.render(bilgi, True, (255, 255, 255)),
                   (10, TILE * GRID_YUK + 10))
        ekran.blit(font.render(
            f"Grid: {GRID_GEN}x{GRID_YUK}   Tile: {TILE}px   "
            f"Yerleştirilen taş: {len(taslar)}",
            True, (180, 180, 180)),
            (10, TILE * GRID_YUK + 32))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Izgaralı bir oyun alanı açılır. Fareyi bir hücrenin üzerine getirdiğinde
hücre sarı çerçeveyle vurgulanır ve alt panelde piksel/grid/tile konum
bilgileri gerçek zamanlı güncellenir. Sol tıklama taş ekler/kaldırır.
"""
