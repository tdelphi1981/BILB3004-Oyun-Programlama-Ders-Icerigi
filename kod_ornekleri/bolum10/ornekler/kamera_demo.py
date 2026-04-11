"""
Kamera Demosu - Tile Haritası + Kamera Clamp

CSV haritasını yükler, üzerinde hareket eden bir oyuncu yerleştirir
ve kamerayı clamp ile harita sınırları içinde tutar.

Bölüm: 10 - Tile-Based Oyun Dünyası

Çalıştırma: python kamera_demo.py
"""

import csv
from pathlib import Path

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480
RENKLER = {
    0: (140, 80, 40),
    1: (80, 180, 80),
    2: (120, 120, 120),
    3: (60, 120, 220),
    4: (240, 230, 140),
}


class Camera:
    def __init__(self, ekran_gen, ekran_yuk, dunya_gen, dunya_yuk):
        self.offset = pygame.Vector2(0, 0)
        self.ekran_gen = ekran_gen
        self.ekran_yuk = ekran_yuk
        self.dunya_gen = dunya_gen
        self.dunya_yuk = dunya_yuk

    def update(self, hedef):
        self.offset.x = hedef.centerx - self.ekran_gen // 2
        self.offset.y = hedef.centery - self.ekran_yuk // 2
        self.offset.x = max(0, min(self.offset.x,
                                    self.dunya_gen - self.ekran_gen))
        self.offset.y = max(0, min(self.offset.y,
                                    self.dunya_yuk - self.ekran_yuk))

    def apply(self, rect):
        return rect.move(-int(self.offset.x), -int(self.offset.y))


def harita_yukle(yol):
    with open(yol, newline="") as f:
        return [[int(x) for x in row] for row in csv.reader(f) if row]


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Kamera Demosu")
    saat = pygame.time.Clock()

    # Bölüm içindeki CSV dosyasını bul
    csv_yol = Path(__file__).parent.parent / "unite2" / "harita.csv"
    if not csv_yol.exists():
        print(f"[X] CSV bulunamadı: {csv_yol}")
        return
    harita = harita_yukle(csv_yol)
    dunya_gen = len(harita[0]) * TILE
    dunya_yuk = len(harita) * TILE

    # Katı tile Rect'leri
    katilar = []
    for r, satir in enumerate(harita):
        for c, t in enumerate(satir):
            if t == 2:
                katilar.append(pygame.Rect(c * TILE, r * TILE, TILE, TILE))

    oyuncu = pygame.Rect(64, 64, 24, 32)
    kamera = Camera(GENISLIK, YUKSEKLIK, dunya_gen, dunya_yuk)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        tuslar = pygame.key.get_pressed()
        dx = (tuslar[pygame.K_RIGHT] - tuslar[pygame.K_LEFT]) * 3
        dy = (tuslar[pygame.K_DOWN] - tuslar[pygame.K_UP]) * 3
        oyuncu.x += dx
        for k in katilar:
            if oyuncu.colliderect(k):
                if dx > 0:
                    oyuncu.right = k.left
                elif dx < 0:
                    oyuncu.left = k.right
        oyuncu.y += dy
        for k in katilar:
            if oyuncu.colliderect(k):
                if dy > 0:
                    oyuncu.bottom = k.top
                elif dy < 0:
                    oyuncu.top = k.bottom

        kamera.update(oyuncu)

        ekran.fill((0, 0, 0))
        for r, satir in enumerate(harita):
            for c, t in enumerate(satir):
                renk = RENKLER.get(t, (0, 0, 0))
                rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
                pygame.draw.rect(ekran, renk, kamera.apply(rect))

        pygame.draw.rect(ekran, (220, 80, 80), kamera.apply(oyuncu))
        pygame.draw.rect(ekran, (255, 255, 255), kamera.apply(oyuncu), 2)

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
