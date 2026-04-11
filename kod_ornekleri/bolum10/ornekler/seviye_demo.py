"""
Seviye Demosu - Solid + Tehlike + Toplanabilir

Aynı harita üzerinde üçü birden: katı platformlar, lava, altın.
Mini tam deneyim. Kamera yoktur, tek ekran sabit.

Bölüm: 10 - Tile-Based Oyun Dünyası

Çalıştırma: python seviye_demo.py
"""

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480

HARITA = [
    "                    ",
    "                    ",
    "  A     A      A    ",
    " 22    22     22    ",
    "                    ",
    "        A           ",
    "       222     A    ",
    "               22   ",
    " A                  ",
    "22    A             ",
    "     22             ",
    "         LL      A  ",
    "2        LL      22 ",
    "22222222222222222222",
    "22222222222222222222",
]


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Seviye Demosu")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    katilar = []
    tehlikeler = []
    altinlar = []
    for r, satir in enumerate(HARITA):
        for c, ch in enumerate(satir):
            rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
            if ch == "2":
                katilar.append(rect)
            elif ch == "L":
                tehlikeler.append(rect)
            elif ch == "A":
                altinlar.append(rect)

    spawn = (80, 300)
    oyuncu = pygame.Rect(*spawn, 24, 32)
    vy = 0
    skor = 0
    can = 3

    calistir = True
    while calistir and can > 0:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP):
                    yerde_mi = any(
                        oyuncu.move(0, 2).colliderect(k) for k in katilar)
                    if yerde_mi:
                        vy = -10

        tuslar = pygame.key.get_pressed()
        dx = (tuslar[pygame.K_RIGHT] - tuslar[pygame.K_LEFT]) * 3
        oyuncu.x += dx
        for k in katilar:
            if oyuncu.colliderect(k):
                if dx > 0:
                    oyuncu.right = k.left
                elif dx < 0:
                    oyuncu.left = k.right

        vy += 0.5
        oyuncu.y += int(vy)
        for k in katilar:
            if oyuncu.colliderect(k):
                if vy > 0:
                    oyuncu.bottom = k.top
                elif vy < 0:
                    oyuncu.top = k.bottom
                vy = 0

        # Tehlikeler
        for t in tehlikeler:
            if oyuncu.colliderect(t):
                can -= 1
                oyuncu.topleft = spawn
                vy = 0
                break

        # Altınlar
        for a in altinlar[:]:
            if oyuncu.colliderect(a):
                altinlar.remove(a)
                skor += 10

        ekran.fill((30, 30, 60))
        for k in katilar:
            pygame.draw.rect(ekran, (120, 120, 120), k)
        for t in tehlikeler:
            pygame.draw.rect(ekran, (220, 80, 0), t)
        for a in altinlar:
            pygame.draw.circle(ekran, (240, 200, 60), a.center, 10)
        pygame.draw.rect(ekran, (220, 80, 80), oyuncu)

        ekran.blit(font.render(
            f"Can: {can}   [ALTIN] {skor}",
            True, (255, 255, 255)), (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
