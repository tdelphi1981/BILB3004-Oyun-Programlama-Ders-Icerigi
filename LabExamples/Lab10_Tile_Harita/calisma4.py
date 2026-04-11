"""
Lab 10 - Çalışma 4 (Bonus) Başlangıç Kodu
Tehlike ve Spawn Sistemi

Bu dosya Lab 10 föyü ile birlikte kullanılır.
Çalışma 3'ün üzerine lava tehlikesi ve spawn dönüş mekaniği ekleyin.

Lab: 10 - Tile-Based Oyun Dünyası
Çalışma: 4 - Tehlike ve Spawn (Bonus)

Çalıştırma: uv run python calisma4.py
"""

import pygame

GENISLIK = 640
YUKSEKLIK = 480
TILE = 32

# GOREV BONUS: Haritaya L (lava) karakterleri ekle
HARITA_STR = [
    "                    ",
    "                    ",
    "        22          ",
    "                    ",
    "  22          22    ",
    "                    ",
    "       222          ",
    "               22   ",
    "2                   ",
    "22222222LLLL22222222",  # örnek: LLLL lava zemini
    "22222222LLLL22222222",
]


def tile_gruplari(harita):
    katilar, tehlikeler = [], []
    for r, satir in enumerate(harita):
        for c, ch in enumerate(satir):
            rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
            if ch == "2":
                katilar.append(rect)
            elif ch == "L":
                tehlikeler.append(rect)
    return katilar, tehlikeler


class Oyuncu:
    def __init__(self, x, y):
        self.spawn = (x, y)
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0
        self.vy = 0
        self.yerde = False
        self.can = 3

    def yeniden_dogur(self):
        """GOREV BONUS: Oyuncuyu spawn'a döndür, hızları sıfırla."""
        # self.rect.topleft = self.spawn
        # self.vx = 0
        # self.vy = 0
        pass  # buraya kod yaz

    def guncelle(self, tuslar, katilar):
        self.vx = 0
        if tuslar[pygame.K_LEFT]:
            self.vx = -3
        if tuslar[pygame.K_RIGHT]:
            self.vx = 3
        self.rect.x += self.vx
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vx > 0:
                    self.rect.right = k.left
                elif self.vx < 0:
                    self.rect.left = k.right
        self.vy += 0.5
        self.rect.y += int(self.vy)
        self.yerde = False
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vy > 0:
                    self.rect.bottom = k.top
                    self.yerde = True
                elif self.vy < 0:
                    self.rect.top = k.bottom
                self.vy = 0

    def zipla(self):
        if self.yerde:
            self.vy = -10


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 10 - Çalışma 4 (Bonus)")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    katilar, tehlikeler = tile_gruplari(HARITA_STR)
    oyuncu = Oyuncu(80, 200)
    oyun_bitti = False

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_SPACE and not oyun_bitti:
                    oyuncu.zipla()

        if not oyun_bitti:
            oyuncu.guncelle(pygame.key.get_pressed(), katilar)

            # GOREV BONUS: Tehlike kontrolü
            # for t in tehlikeler:
            #     if oyuncu.rect.colliderect(t):
            #         oyuncu.can -= 1
            #         oyuncu.yeniden_dogur()
            #         if oyuncu.can <= 0:
            #             oyun_bitti = True
            #         break

        ekran.fill((30, 30, 60))
        for k in katilar:
            pygame.draw.rect(ekran, (120, 120, 120), k)
        for t in tehlikeler:
            pygame.draw.rect(ekran, (220, 80, 0), t)

        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)

        ekran.blit(font.render(
            f"Can: {oyuncu.can}",
            True, (255, 255, 255)), (10, 10))

        if oyun_bitti:
            m = font.render("[GAME OVER]", True, (255, 80, 80))
            ekran.blit(m, m.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2)))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
