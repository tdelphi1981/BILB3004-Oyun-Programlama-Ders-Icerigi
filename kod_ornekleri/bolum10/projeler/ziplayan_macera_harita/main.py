"""
Zıplayan Macera - Seviye 1 (Harita Entegrasyonu)

Bölüm 10'da oluşturduğumuz tile sistemi, CSV yükleme, kamera ve
seviye tile türlerini bir araya getiren ilk oynanabilir seviye.

Harita: harita/seviye1.csv
- 1 = çim (boş)
- 2 = taş (solid)
- 4 = altın (toplanabilir)
- 5 = diken (tehlike)

Öğrenilecek kavramlar:
- CSV harita + tile gruplarına ayırma
- Kamera clamp ile takip
- Platformer fiziği + toplanabilir + tehlike
- Seviyeyi ayrı bir dosyadan yükleme

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 4 - Seviye Tasarımı

Çalıştırma: python main.py
Gereksinimler: pygame
"""

import csv
from pathlib import Path

import pygame

TILE = 32
GENISLIK = 960
YUKSEKLIK = 540


class Camera:
    def __init__(self, ekran_gen, ekran_yuk, dunya_gen, dunya_yuk, lerp=0.12):
        self.offset = pygame.Vector2(0, 0)
        self.ekran_gen = ekran_gen
        self.ekran_yuk = ekran_yuk
        self.dunya_gen = dunya_gen
        self.dunya_yuk = dunya_yuk
        self.lerp = lerp

    def update(self, hedef):
        istenen = pygame.Vector2(
            hedef.centerx - self.ekran_gen // 2,
            hedef.centery - self.ekran_yuk // 2,
        )
        self.offset += (istenen - self.offset) * self.lerp
        max_x = max(0, self.dunya_gen - self.ekran_gen)
        max_y = max(0, self.dunya_yuk - self.ekran_yuk)
        self.offset.x = max(0, min(self.offset.x, max_x))
        self.offset.y = max(0, min(self.offset.y, max_y))

    def apply(self, rect):
        return rect.move(-int(self.offset.x), -int(self.offset.y))


class Seviye:
    """CSV'den tile gruplarını çıkarır ve çizim yardımcıları sunar."""

    def __init__(self, csv_yol):
        self.harita = self._yukle(csv_yol)
        self.yuk = len(self.harita)
        self.gen = len(self.harita[0])
        self.dunya_gen = self.gen * TILE
        self.dunya_yuk = self.yuk * TILE

        self.katilar = []
        self.tehlikeler = []
        self.altinlar = []
        self._grupla()

    @staticmethod
    def _yukle(yol):
        with open(yol, newline="") as f:
            return [[int(x) for x in row] for row in csv.reader(f) if row]

    def _grupla(self):
        for r, satir in enumerate(self.harita):
            for c, t in enumerate(satir):
                rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
                if t == 2:
                    self.katilar.append(rect)
                elif t == 4:
                    self.altinlar.append(rect)
                elif t == 5:
                    self.tehlikeler.append(rect)

    def ciz(self, ekran, kamera):
        # Arkaplan dolgusu
        for r in range(self.yuk):
            for c in range(self.gen):
                rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
                pygame.draw.rect(ekran, (80, 140, 200), kamera.apply(rect))
        for k in self.katilar:
            pygame.draw.rect(ekran, (120, 100, 80), kamera.apply(k))
            pygame.draw.rect(ekran, (80, 60, 40), kamera.apply(k), 2)
        for t in self.tehlikeler:
            c = kamera.apply(t)
            pygame.draw.rect(ekran, (40, 40, 60), c)
            for i in range(4):
                x = c.x + i * 8
                pygame.draw.polygon(
                    ekran, (220, 220, 240),
                    [(x, c.bottom - 2),
                     (x + 4, c.top + 4),
                     (x + 8, c.bottom - 2)],
                )
        for a in self.altinlar:
            c = kamera.apply(a)
            pygame.draw.circle(ekran, (240, 200, 60), c.center, 10)
            pygame.draw.circle(ekran, (255, 240, 120), c.center, 10, 2)


class Oyuncu:
    def __init__(self, x, y):
        self.spawn = (x, y)
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0
        self.vy = 0
        self.yerde = False

    def yeniden_dogur(self):
        self.rect.topleft = self.spawn
        self.vx = 0
        self.vy = 0

    def guncelle(self, tuslar, katilar):
        self.vx = 0
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.vx = -3
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.vx = 3
        self.rect.x += self.vx
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vx > 0:
                    self.rect.right = k.left
                elif self.vx < 0:
                    self.rect.left = k.right

        self.vy += 0.5
        if self.vy > 12:
            self.vy = 12
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
            self.vy = -11


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Zıplayan Macera - Seviye 1")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    kucuk = pygame.font.Font(None, 20)

    harita_yolu = Path(__file__).parent / "harita" / "seviye1.csv"
    seviye = Seviye(harita_yolu)
    kamera = Camera(GENISLIK, YUKSEKLIK, seviye.dunya_gen, seviye.dunya_yuk)

    oyuncu = Oyuncu(80, seviye.dunya_yuk - 120)
    skor = 0
    can = 3

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    oyuncu.zipla()

        oyuncu.guncelle(pygame.key.get_pressed(), seviye.katilar)

        for t in seviye.tehlikeler:
            if oyuncu.rect.colliderect(t):
                can -= 1
                oyuncu.yeniden_dogur()
                break
        for a in seviye.altinlar[:]:
            if oyuncu.rect.colliderect(a):
                seviye.altinlar.remove(a)
                skor += 10

        # Düşme ile can kaybı
        if oyuncu.rect.top > seviye.dunya_yuk:
            can -= 1
            oyuncu.yeniden_dogur()

        kamera.update(oyuncu.rect)

        ekran.fill((30, 30, 60))
        seviye.ciz(ekran, kamera)
        pygame.draw.rect(ekran, (220, 80, 80), kamera.apply(oyuncu.rect))
        pygame.draw.rect(ekran, (255, 255, 255), kamera.apply(oyuncu.rect), 2)

        # HUD
        ekran.blit(font.render(
            f"Can: {can}   [ALTIN] {skor}",
            True, (255, 255, 255)), (10, 10))
        ekran.blit(kucuk.render(
            "Oklar/WASD: hareket  SPACE: zıpla",
            True, (220, 220, 220)), (10, 42))

        if can <= 0:
            metin = font.render("[GAME OVER]", True, (255, 80, 80))
            ekran.blit(metin, metin.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2)))

        if not seviye.altinlar and can > 0:
            metin = font.render("Seviye tamamlandı!",
                                True, (120, 255, 120))
            ekran.blit(metin, metin.get_rect(
                center=(GENISLIK // 2, 80)))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
960x540 pencerede Zıplayan Macera'nın ilk seviyesi açılır. Mavi arkaplan
üzerinde kahverengi platformlar, yerde dikenler ve dağılmış altınlar
görülür. Oyuncu kamerası (clamp + lerp) ile takip edilir. Tüm altınlar
toplandığında "Seviye tamamlandı!" yazısı çıkar.
"""
