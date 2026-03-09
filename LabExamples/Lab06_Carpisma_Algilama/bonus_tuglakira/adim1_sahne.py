"""
Tugla Kirma (Breakout) - Adim 1: Gorsel Sahne

Raket, top ve tugla nesnelerini olusturup ekrana cizen ilk adim.
Henuz hareket veya carpisma yok, sadece gorsel sahne.

Ogrenilecek kavramlar:
- Sprite sinifi olusturma
- pygame.draw ile sekil cizme
- Izgara duzeni ile tugla yerlestirme

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Tugla Kirma (Adim 1/7)

Calistirma: uv run python adim1_sahne.py
Gereksinimler: pygame
"""

import pygame
import sys

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60

# --- Renkler ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (0, 0, 139)
ACIK_MAVI = (100, 149, 237)
KIRMIZI = (220, 50, 50)
YESIL = (50, 200, 50)
SARI = (240, 220, 50)
TURUNCU = (240, 150, 30)
MOR = (160, 50, 200)

TUGLA_RENKLERI = [KIRMIZI, TURUNCU, SARI, YESIL]

# --- Tugla sabitleri ---
TUGLA_GENISLIK = 70
TUGLA_YUKSEKLIK = 25
TUGLA_BASLANGIC_X = 90
TUGLA_BASLANGIC_Y = 60
TUGLA_SATIR_YUKSEKLIK = 35
TUGLA_SUTUN_SAYISI = 5
TUGLA_SUTUN_BOSLUK = 5


class Raket(pygame.sprite.Sprite):
    """Oyuncunun kontrol ettigi raket."""

    def __init__(self):
        super().__init__()
        self.genislik = 120
        self.yukseklik = 15
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image, ACIK_MAVI,
            (0, 0, self.genislik, self.yukseklik),
            border_radius=7
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.y = YUKSEKLIK - 30


class Top(pygame.sprite.Sprite):
    """Oyun topu."""

    def __init__(self):
        super().__init__()
        self.yaricap = 8
        boyut = self.yaricap * 2
        self.image = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BEYAZ, (self.yaricap, self.yaricap), self.yaricap)
        self.rect = self.image.get_rect()
        self.rect.center = (GENISLIK // 2, YUKSEKLIK // 2)


class Tugla(pygame.sprite.Sprite):
    """Kirilan tugla nesnesi."""

    def __init__(self, x, y, renk):
        super().__init__()
        self.image = pygame.Surface((TUGLA_GENISLIK, TUGLA_YUKSEKLIK))
        self.image.fill(renk)
        # Beyaz kenarlık
        pygame.draw.rect(
            self.image, BEYAZ,
            (0, 0, TUGLA_GENISLIK, TUGLA_YUKSEKLIK), 1
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def tugla_olustur():
    """5 sutun x 4 satir tugla izgara duzeni olusturur."""
    tuglalar = pygame.sprite.Group()
    for satir in range(4):
        renk = TUGLA_RENKLERI[satir]
        for sutun in range(TUGLA_SUTUN_SAYISI):
            x = TUGLA_BASLANGIC_X + sutun * (TUGLA_GENISLIK + TUGLA_SUTUN_BOSLUK)
            y = TUGLA_BASLANGIC_Y + satir * TUGLA_SATIR_YUKSEKLIK
            tugla = Tugla(x, y, renk)
            tuglalar.add(tugla)
    return tuglalar


def main():
    """Ana oyun dongusu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Tugla Kirma - Adim 1: Gorsel Sahne")
    saat = pygame.time.Clock()
    yazi_tipi = pygame.font.SysFont("Arial", 24)

    # Nesneleri olustur
    raket = Raket()
    top = Top()
    tuglalar = tugla_olustur()

    tum_spritelar = pygame.sprite.Group()
    tum_spritelar.add(raket, top)
    tum_spritelar.add(tuglalar)

    skor = 0
    can = 3

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Ciz
        ekran.fill(SIYAH)
        tum_spritelar.draw(ekran)

        # Skor ve can
        skor_yazi = yazi_tipi.render(f"Skor: {skor}", True, BEYAZ)
        can_yazi = yazi_tipi.render(f"Can: {can}", True, BEYAZ)
        ekran.blit(skor_yazi, (10, 10))
        ekran.blit(can_yazi, (GENISLIK - 80, 10))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# --- BEKLENEN CIKTI ---
# [OK] 800x600 siyah pencere acilir
# [OK] Ekranin alt kisminda mavi yuvarlatilmis raket gorulur
# [OK] Ekranin ortasinda beyaz top gorulur
# [OK] Ust kisimda 5x4 = 20 renkli tugla gorulur (Kirmizi, Turuncu, Sari, Yesil sirasi)
# [OK] Sol ustte "Skor: 0", sag ustte "Can: 3" yazilari gorulur
# [OK] Henuz hareket veya etkilesim yoktur
# [OK] ESC veya pencere kapatma ile cikis yapilir
