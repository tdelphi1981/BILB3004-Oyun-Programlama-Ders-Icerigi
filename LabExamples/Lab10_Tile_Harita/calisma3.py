"""
Lab 10 - Çalışma 3 Başlangıç Kodu
Kamera ve Platform Çarpışması

Bu dosya Lab 10 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- Camera sınıfı ve apply()
- Yatay + dikey ayrık tile çarpışması
- Yerçekimi ve zıplama

Lab: 10 - Tile-Based Oyun Dünyası
Çalışma: 3 - Kamera ve Platform Çarpışması

Çalıştırma: uv run python calisma3.py
"""

import pygame

GENISLIK = 640
YUKSEKLIK = 480
TILE = 32

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
    "22222222222222222222",
    "22222222222222222222",
]


def katilari_cikar(harita):
    katilar = []
    for r, satir in enumerate(harita):
        for c, ch in enumerate(satir):
            if ch == "2":
                katilar.append(pygame.Rect(c * TILE, r * TILE, TILE, TILE))
    return katilar


class Camera:
    def __init__(self, gen, yuk, dunya_gen=None, dunya_yuk=None):
        self.offset = pygame.Vector2(0, 0)
        self.gen = gen
        self.yuk = yuk
        self.dunya_gen = dunya_gen
        self.dunya_yuk = dunya_yuk

    def apply(self, rect):
        return rect.move(-int(self.offset.x), -int(self.offset.y))

    def update(self, hedef):
        self.offset.x += (hedef.centerx - self.gen // 2 - self.offset.x) * 0.1
        self.offset.y += (hedef.centery - self.yuk // 2 - self.offset.y) * 0.1

        # GOREV 5: Clamp (harita sınırları)
        # if self.dunya_gen is not None:
        #     max_x = max(0, self.dunya_gen - self.gen)
        #     max_y = max(0, self.dunya_yuk - self.yuk)
        #     self.offset.x = max(0, min(self.offset.x, max_x))
        #     self.offset.y = max(0, min(self.offset.y, max_y))


class Oyuncu:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0
        self.vy = 0
        self.yerde = False

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
    pygame.display.set_caption("Lab 10 - Çalışma 3")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    katilar = katilari_cikar(HARITA_STR)
    dunya_gen = len(HARITA_STR[0]) * TILE
    dunya_yuk = len(HARITA_STR) * TILE
    oyuncu = Oyuncu(80, 200)
    kamera = Camera(GENISLIK, YUKSEKLIK, dunya_gen, dunya_yuk)

    # GOREV 6: Altınlar listesi ekle
    # altinlar = [pygame.Rect(...), ...]  # en az 5 altın
    skor = 0

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_SPACE:
                    oyuncu.zipla()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)

        # GOREV 6: Altın çarpışma
        # for a in altinlar[:]:
        #     if oyuncu.rect.colliderect(a):
        #         altinlar.remove(a)
        #         skor += 10

        kamera.update(oyuncu.rect)

        ekran.fill((30, 30, 60))
        for k in katilar:
            pygame.draw.rect(ekran, (120, 120, 120), kamera.apply(k))

        # GOREV 6: Altınları çiz
        # for a in altinlar:
        #     pygame.draw.circle(ekran, (240,200,60),
        #                        kamera.apply(a).center, 10)

        pygame.draw.rect(ekran, (220, 80, 80), kamera.apply(oyuncu.rect))

        ekran.blit(font.render(
            f"Skor: {skor}   (Oklar + SPACE)",
            True, (255, 255, 255)), (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
