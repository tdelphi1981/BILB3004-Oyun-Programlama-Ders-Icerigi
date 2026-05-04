"""
Lab 11 - Çalışma 2 Başlangıç Kodu
Variable Jump + Double Jump

Bu dosya Lab 11 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- KEYUP olayı ile tuş bırakma
- Yukarı hızı variable jump çarpanıyla kesme
- Double jump sayacı

Lab: 11 - Platform Oyunu Mekaniği
Çalışma: 2 - Variable + Double Jump

Çalıştırma: uv run python calisma2.py
"""

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480

COYOTE_SURE = 6
BUFFER_SURE = 6
ZIP_HIZI = -11
DOUBLE_ZIP_HIZI = -9
YERCEKIMI = 0.5
MAX_DUSUS = 10
MAX_ZIPLAMA = 2
VAR_KES = 0.4   # GOREV 3'te değiştirilecek

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
        self.kalan_ziplama = MAX_ZIPLAMA
        self.zipliyor = False

    def zipla_istegi(self):
        self.buffer_sayac = BUFFER_SURE

    def tus_birakildi(self):
        # GOREV 1: Variable jump kesme
        # Eğer self.zipliyor TRUE ve self.vy < 0 (yukarı gidiyor) ise:
        #   self.vy *= VAR_KES
        # self.zipliyor = False
        pass

    def guncelle(self, tuslar, katilar):
        # Yatay hareket
        self.vx = 0
        if tuslar[pygame.K_LEFT]:
            self.vx = -4
        elif tuslar[pygame.K_RIGHT]:
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

        # GOREV 2: Yere değince zıplama haklarını yenile
        # Eğer self.yerde TRUE ise self.kalan_ziplama = MAX_ZIPLAMA

        # Coyote + buffer
        if eski_yerde and not self.yerde:
            self.coyote_sayac = COYOTE_SURE
        elif self.coyote_sayac > 0:
            self.coyote_sayac -= 1
        if self.buffer_sayac > 0:
            self.buffer_sayac -= 1

        # GOREV 3: Zıplama karari (double jump dahil)
        # Eğer buffer_sayac > 0 ise:
        #   - yerde veya coyote_sayac > 0: ilk zıplama
        #     self.vy = ZIP_HIZI
        #     kalan_ziplama = MAX_ZIPLAMA - 1
        #     yerde = False, zipliyor = True
        #     buffer_sayac = 0, coyote_sayac = 0
        #   - yoksa kalan_ziplama > 0: double jump
        #     self.vy = DOUBLE_ZIP_HIZI
        #     kalan_ziplama -= 1
        #     zipliyor = True
        #     buffer_sayac = 0
        pass


def harita_ciz(ekran, katilar):
    for k in katilar:
        pygame.draw.rect(ekran, (120, 120, 120), k)
        pygame.draw.rect(ekran, (80, 80, 80), k, 2)


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 11 - Calisma 2 (Variable + Double)")
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
            elif olay.type == pygame.KEYUP:
                if olay.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    oyuncu.tus_birakildi()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)

        ekran.fill((30, 30, 60))
        harita_ciz(ekran, katilar)

        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)
        pygame.draw.rect(ekran, (255, 255, 255), oyuncu.rect, 2)

        ekran.blit(font.render(
            f"kalan:{oyuncu.kalan_ziplama}  zipliyor:{oyuncu.zipliyor}  "
            f"VAR_KES:{VAR_KES}",
            True, (220, 220, 220)), (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
