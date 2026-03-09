"""
Uzay Kacisi v2 - Adim 1: v1 Temeli (Oyuncu + Kayan Yildizlar)

v1'den alinan temel: Oyuncu gemisi ve parallax yildiz arka plani.
Bu adimda oyun penceresi, oyuncu hareketi ve kayan yildizlari
olusturuyoruz. Tum sonraki adimlar bu temel uzerine insa edilecek.

Ogrenilecek kavramlar:
- pygame.sprite.Sprite temel kullanimi
- pygame.draw.polygon ile sekil cizimi
- Parallax yildiz efekti (farkli boyut ve hizlar)
- Oyun dongusu ve FPS kontrolu

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Uzay Kacisi v2 (Adim 1/7)

Calistirma: uv run python adim1_v1_temeli.py
Gereksinimler: pygame

Kontroller:
- WASD / Ok tuslari: Hareket
- ESC: Cikis
"""

import pygame
import random
import sys

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60

# --- Renkler ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (10, 10, 40)
ACIK_MAVI = (100, 150, 255)
MAVI = (50, 100, 200)
GUMI = (200, 200, 220)
SARI = (255, 255, 0)

# --- Oyuncu Hizi ---
OYUNCU_HIZ = 5


class Yildiz(pygame.sprite.Sprite):
    """Parallax kayan yildiz. 3 farkli boyut ve hiz katmani."""

    def __init__(self):
        super().__init__()
        # Rastgele katman sec (kucuk/uzak, orta, buyuk/yakin)
        self.katman = random.choice([1, 2, 3])

        if self.katman == 1:
            self.boyut = 1
            self.hiz = random.uniform(0.5, 1.0)
            self.renk = (100, 100, 120)
        elif self.katman == 2:
            self.boyut = 2
            self.hiz = random.uniform(1.5, 2.5)
            self.renk = (180, 180, 200)
        else:
            self.boyut = 3
            self.hiz = random.uniform(3.0, 4.5)
            self.renk = BEYAZ

        self.image = pygame.Surface((self.boyut, self.boyut))
        self.image.fill(self.renk)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK)
        self.rect.y = random.randint(0, YUKSEKLIK)
        # Kesirli konum takibi
        self.y_float = float(self.rect.y)

    def update(self):
        self.y_float += self.hiz
        self.rect.y = int(self.y_float)
        if self.rect.top > YUKSEKLIK:
            self.rect.x = random.randint(0, GENISLIK)
            self.rect.y = -self.boyut
            self.y_float = float(self.rect.y)


class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi. Ucgen seklinde cizilir."""

    def __init__(self):
        super().__init__()
        self.genislik = 40
        self.yukseklik = 50
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        self._gemi_ciz()
        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20

    def _gemi_ciz(self):
        """Oyuncu gemisini ucgen olarak ciz."""
        # Ana govde - acik mavi ucgen
        noktalar = [
            (self.genislik // 2, 0),          # Burun (ust)
            (0, self.yukseklik),               # Sol alt
            (self.genislik, self.yukseklik),   # Sag alt
        ]
        pygame.draw.polygon(self.image, ACIK_MAVI, noktalar)
        # Ic detay - daha koyu mavi
        ic_noktalar = [
            (self.genislik // 2, 10),
            (8, self.yukseklik - 5),
            (self.genislik - 8, self.yukseklik - 5),
        ]
        pygame.draw.polygon(self.image, MAVI, ic_noktalar)
        # Motor alevi - sari
        alev_noktalar = [
            (self.genislik // 2 - 6, self.yukseklik),
            (self.genislik // 2, self.yukseklik - 8),
            (self.genislik // 2 + 6, self.yukseklik),
        ]
        pygame.draw.polygon(self.image, SARI, alev_noktalar)

    def update(self):
        tuslar = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            dx = -OYUNCU_HIZ
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            dx = OYUNCU_HIZ
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            dy = -OYUNCU_HIZ
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            dy = OYUNCU_HIZ

        self.rect.x += dx
        self.rect.y += dy

        # Ekran sinirlari
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > YUKSEKLIK:
            self.rect.bottom = YUKSEKLIK


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Uzay Kacisi v2 - Adim 1: v1 Temeli")
    saat = pygame.time.Clock()

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()

    # Yildizlari olustur
    for _ in range(100):
        y = Yildiz()
        tum_spritelar.add(y)
        yildizlar.add(y)

    # Oyuncuyu olustur
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Font
    font = pygame.font.SysFont(None, 28)

    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olaylar ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- Guncelleme ---
        tum_spritelar.update()

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        # Bilgi metni
        bilgi = font.render("Uzay Kacisi v2 - WASD/Ok tuslari ile hareket", True, GUMI)
        ekran.blit(bilgi, (10, YUKSEKLIK - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# ============================================================
# BEKLENEN CIKTI
# ============================================================
# - 800x600 koyu mavi pencere
# - Kayan yildiz arka plani (3 farkli boyut ve hiz)
# - Acik mavi ucgen oyuncu gemisi (ekranin altinda)
# - WASD / Ok tuslari ile 4 yonde hareket
# - Oyuncu ekran disina cikamaz
# - ESC ile cikis
# - [OK] Parallax yildiz efekti calisiyor
# - [OK] Oyuncu hareketi akici
