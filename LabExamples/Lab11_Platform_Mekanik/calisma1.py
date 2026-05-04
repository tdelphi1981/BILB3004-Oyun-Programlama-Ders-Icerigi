"""
Lab 11 - Çalışma 1 Başlangıç Kodu
Coyote Time + Jump Buffer

Bu dosya Lab 11 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- Coyote time sayacı
- Jump buffer sayacı
- İki mekaniğin birlikte çalışması

Lab: 11 - Platform Oyunu Mekaniği
Çalışma: 1 - Coyote Time + Jump Buffer

Çalıştırma: uv run python calisma1.py
"""

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480

COYOTE_SURE = 6
BUFFER_SURE = 6
ZIP_HIZI = -11
YERCEKIMI = 0.5
MAX_DUSUS = 10

HARITA = [
    "                    ",
    "                    ",
    "        22          ",
    "                    ",
    "   222        22    ",
    "                    ",
    "              222   ",
    "2                   ",
    "22222222 2222222222 ",
    "22222222222222222222",
]


def katilari_cikar(harita):
    katilar = []
    for r, s in enumerate(harita):
        for c, ch in enumerate(s):
            if ch == "2":
                katilar.append(pygame.Rect(c * TILE, r * TILE, TILE, TILE))
    return katilar


class Oyuncu:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0.0
        self.vy = 0.0
        self.yerde = False
        self.coyote_sayac = 0
        self.buffer_sayac = 0

    def zipla_istegi(self):
        # GOREV 1: Buffer'ı doldur (buffer_sayac = BUFFER_SURE)
        pass

    def guncelle(self, tuslar, katilar):
        # Yatay hareket
        self.vx = 0
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.vx = -4
        elif tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.vx = 4

        self.rect.x += int(self.vx)
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vx > 0:
                    self.rect.right = k.left
                elif self.vx < 0:
                    self.rect.left = k.right

        # Dikey + yerçekimi
        eski_yerde = self.yerde
        self.vy = min(self.vy + YERCEKIMI, MAX_DUSUS)
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

        # GOREV 2: Coyote sayacı
        # Eğer eski_yerde TRUE ve self.yerde FALSE olduysa
        #   coyote_sayac = COYOTE_SURE (6)
        # Yoksa coyote_sayac her karede 1 azalmalı (0'ın altına inmesin)

        # GOREV 3: Buffer sayacı
        # buffer_sayac her karede 1 azalmalı

        # GOREV 4: Zıplama karari
        # Eğer buffer_sayac > 0 VE (yerde VEYA coyote_sayac > 0) ise:
        #   vy = ZIP_HIZI
        #   yerde = False
        #   buffer_sayac = 0
        #   coyote_sayac = 0
        pass


def harita_ciz(ekran, katilar):
    for k in katilar:
        pygame.draw.rect(ekran, (120, 120, 120), k)
        pygame.draw.rect(ekran, (80, 80, 80), k, 2)


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 11 - Calisma 1 (Coyote + Buffer)")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    katilar = katilari_cikar(HARITA)
    oyuncu = Oyuncu(80, 200)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    oyuncu.zipla_istegi()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)

        ekran.fill((30, 30, 60))
        harita_ciz(ekran, katilar)

        # GOREV 5: Görsel feedback
        # Coyote aktifken (coyote_sayac > 0) oyuncu.rect.inflate(6, 6) ile altın çerçeve
        # Buffer aktifken mavi çerçeve

        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)
        pygame.draw.rect(ekran, (255, 255, 255), oyuncu.rect, 2)

        ekran.blit(font.render(
            f"coyote:{oyuncu.coyote_sayac}  buffer:{oyuncu.buffer_sayac}  yerde:{oyuncu.yerde}",
            True, (220, 220, 220)), (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
