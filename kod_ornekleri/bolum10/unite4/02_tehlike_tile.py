"""
Tehlike Tile'ları - Lava ve Diken

Bu program solid tile'lara ek olarak tehlike tile'ları (lava, diken)
ekler. Oyuncu bunlara dokununca can azalır ve son kontrol noktasına
geri döner.

Öğrenilecek kavramlar:
- Birden fazla tile grubu: katilar, tehlikeler
- Rect listesi üzerinde collidelist ile tarama
- Kontrol noktası (spawn) mantığı

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 4 - Seviye Tasarımı

Çalıştırma: python 02_tehlike_tile.py
Gereksinimler: pygame
"""

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480

# 2 = taş solid, L = lava, D = diken
HARITA = [
    "                    ",
    "                    ",
    "                    ",
    "        22          ",
    "                    ",
    "   22      22       ",
    "              DDD   ",
    "                    ",
    "         22         ",
    "               22   ",
    "  DD              22",
    "                    ",
    "2            LLL    ",
    "22222222LLLL22222222",
    "22222222LLLL22222222",
]


def tile_listelerini_cikar(harita):
    katilar, tehlikeler = [], []
    for r, satir in enumerate(harita):
        for c, ch in enumerate(satir):
            rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
            if ch == "2":
                katilar.append(rect)
            elif ch in ("L", "D"):
                tehlikeler.append((ch, rect))
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
        self.rect.topleft = self.spawn
        self.vx = 0
        self.vy = 0

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


def tehlike_ciz(ekran, tehlikeler):
    for tip, rect in tehlikeler:
        if tip == "L":
            pygame.draw.rect(ekran, (220, 80, 0), rect)
            pygame.draw.rect(ekran, (255, 180, 60), rect, 2)
        elif tip == "D":
            pygame.draw.rect(ekran, (40, 40, 60), rect)
            # Diken üçgenleri
            for i in range(4):
                x = rect.x + i * 8
                pygame.draw.polygon(
                    ekran, (200, 200, 220),
                    [(x, rect.bottom),
                     (x + 4, rect.top + 4),
                     (x + 8, rect.bottom)],
                )


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Tehlike Tile'ları")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    katilar, tehlikeler = tile_listelerini_cikar(HARITA)
    oyuncu = Oyuncu(48, 384)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP):
                    oyuncu.zipla()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)

        # Tehlike kontrolü
        for tip, rect in tehlikeler:
            if oyuncu.rect.colliderect(rect):
                oyuncu.can -= 1
                oyuncu.yeniden_dogur()
                print(f"[!] Tehlike ({tip})! Kalan can: {oyuncu.can}")
                if oyuncu.can <= 0:
                    print("[GAME OVER]")
                    calistir = False
                break

        ekran.fill((30, 30, 60))
        for k in katilar:
            pygame.draw.rect(ekran, (120, 120, 120), k)
            pygame.draw.rect(ekran, (80, 80, 80), k, 2)
        tehlike_ciz(ekran, tehlikeler)

        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)
        pygame.draw.rect(ekran, (255, 255, 255), oyuncu.rect, 2)

        ekran.blit(font.render(
            f"Can: {oyuncu.can}  (Oklar + SPACE)",
            True, (255, 255, 255)), (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Haritada turuncu lava ve mavi-metalik diken tile'ları bulunur. Oyuncu
bunlara dokununca can kaybeder ve spawn noktasına döner. Terminalde
her dokunuşta uyarı mesajı yazılır. Can 0 olunca "[GAME OVER]" yazar.
"""
