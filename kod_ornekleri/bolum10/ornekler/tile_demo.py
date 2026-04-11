"""
Tile Demosu - Tüm Bölüm 10 Tile Temellerini Bir Arada

Bu örnek; elle tanımlanmış harita, tileset subsurface kesimi ve
fare ile tile seçimi özelliklerini tek programda birleştirir.

Bölüm: 10 - Tile-Based Oyun Dünyası

Çalıştırma: python tile_demo.py
"""

import pygame

TILE = 32
GRID_GEN = 20
GRID_YUK = 12

PALETTE = [
    (30, 30, 50),    # 0 boş
    (80, 180, 80),   # 1 çim
    (120, 120, 120), # 2 taş
    (60, 120, 220),  # 3 su
]


def main():
    pygame.init()
    ekran = pygame.display.set_mode((TILE * GRID_GEN, TILE * GRID_YUK + 40))
    pygame.display.set_caption("Tile Demosu")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    harita = [[1 for _ in range(GRID_GEN)] for _ in range(GRID_YUK)]
    for c in range(GRID_GEN):
        harita[0][c] = 2
        harita[-1][c] = 2
    for r in range(GRID_YUK):
        harita[r][0] = 2
        harita[r][-1] = 2

    secilen = 2

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if pygame.K_0 <= olay.key <= pygame.K_3:
                    secilen = olay.key - pygame.K_0
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                px, py = olay.pos
                if py < TILE * GRID_YUK:
                    c = px // TILE
                    r = py // TILE
                    harita[r][c] = secilen

        ekran.fill((0, 0, 0))
        for r in range(GRID_YUK):
            for c in range(GRID_GEN):
                pygame.draw.rect(
                    ekran, PALETTE[harita[r][c]],
                    (c * TILE, r * TILE, TILE, TILE))
                pygame.draw.rect(
                    ekran, (20, 20, 30),
                    (c * TILE, r * TILE, TILE, TILE), 1)

        # Panel
        pygame.draw.rect(ekran, (10, 10, 20),
                         (0, TILE * GRID_YUK, TILE * GRID_GEN, 40))
        ekran.blit(font.render(
            f"Seçilen tile: {secilen}  (0-3: seç, tıkla: yerleştir)",
            True, (255, 255, 255)),
            (10, TILE * GRID_YUK + 12))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
