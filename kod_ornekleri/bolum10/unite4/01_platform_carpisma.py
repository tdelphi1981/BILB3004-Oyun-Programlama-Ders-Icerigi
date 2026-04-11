"""
Tile Tabanlı Platform Çarpışması

Bu program bir 2B harita üzerinde yerçekimi + zıplama + solid tile
çarpışması gösterir. Oyuncu solid tile'lara (ID=2) çarpar, diğerlerinden
serbestçe geçer.

Öğrenilecek kavramlar:
- Harita -> Rect listesi dönüşümü
- Yatay ve dikey çarpışmayı ayrı çözme
- Yerçekimi ve zıplama mekaniği

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 4 - Seviye Tasarımı

Çalıştırma: python 01_platform_carpisma.py
Gereksinimler: pygame
"""

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480

# 1 = çim (boş), 2 = taş (solid)
HARITA = [
    "                    ",
    "                    ",
    "                    ",
    "         22         ",
    "                    ",
    "     22             ",
    "             22     ",
    "                    ",
    "   222              ",
    "             222    ",
    "                    ",
    "                    ",
    " 2          22      ",
    "22222222222222222222",
    "22222222222222222222",
]


def katilari_cikar(harita):
    """Harita metninden solid Rect listesi üretir."""
    katilar = []
    for r, satir in enumerate(harita):
        for c, ch in enumerate(satir):
            if ch == "2":
                katilar.append(pygame.Rect(c * TILE, r * TILE, TILE, TILE))
    return katilar


class Oyuncu:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0
        self.vy = 0
        self.yerde = False

    def guncelle(self, tuslar, katilar):
        # Yatay hareket
        self.vx = 0
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.vx = -3
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.vx = 3

        self.rect.x += self.vx
        self._yatay_carpisma(katilar)

        # Yerçekimi
        self.vy += 0.5
        if self.vy > 10:
            self.vy = 10
        self.rect.y += int(self.vy)
        self.yerde = False
        self._dikey_carpisma(katilar)

    def zipla(self):
        if self.yerde:
            self.vy = -10

    def _yatay_carpisma(self, katilar):
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vx > 0:
                    self.rect.right = k.left
                elif self.vx < 0:
                    self.rect.left = k.right

    def _dikey_carpisma(self, katilar):
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vy > 0:
                    self.rect.bottom = k.top
                    self.vy = 0
                    self.yerde = True
                elif self.vy < 0:
                    self.rect.top = k.bottom
                    self.vy = 0


def harita_ciz(ekran, katilar):
    for k in katilar:
        pygame.draw.rect(ekran, (120, 120, 120), k)
        pygame.draw.rect(ekran, (80, 80, 80), k, 2)


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Tile Platform Çarpışması")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    katilar = katilari_cikar(HARITA)
    oyuncu = Oyuncu(80, 200)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    oyuncu.zipla()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)

        ekran.fill((30, 30, 60))
        harita_ciz(ekran, katilar)
        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)
        pygame.draw.rect(ekran, (255, 255, 255), oyuncu.rect, 2)

        ekran.blit(font.render(
            "Oklar/WASD: hareket  SPACE/UP: zıpla",
            True, (220, 220, 220)), (10, 10))
        ekran.blit(font.render(
            f"Yerde: {oyuncu.yerde}  vy: {oyuncu.vy:.1f}",
            True, (180, 180, 180)), (10, 32))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Gri taş platformların olduğu bir haritada kırmızı bir oyuncu kutusu
yerçekimi ile düşer, oklarla sağa sola koşar, SPACE ile zıplar.
Oyuncu solid platformların üzerinde durur ve yanlardan çarpışmayı
doğru şekilde çözer.
"""
