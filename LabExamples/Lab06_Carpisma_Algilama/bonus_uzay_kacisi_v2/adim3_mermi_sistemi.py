"""
Uzay Kacisi v2 - Adim 3: Mermi Sistemi + Space ile Ates

Oyuncuya ates etme yetenegini ekliyoruz. Space tusuna basinca
oyuncunun burun noktasindan sari mermiler firlatilar.
Cooldown sistemi ile cok hizli ates etme engellenir.

Ogrenilecek kavramlar:
- Mermi sprite sinifi
- pygame.time.get_ticks() ile cooldown yonetimi
- Tus basma ile sprite olusturma
- Birden fazla sprite grubu yonetimi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Uzay Kacisi v2 (Adim 3/7)

Calistirma: uv run python adim3_mermi_sistemi.py
Gereksinimler: pygame

Kontroller:
- WASD / Ok tuslari: Hareket
- Space: Ates
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
KIRMIZI = (220, 50, 50)
KOYU_KIRMIZI = (150, 30, 30)
SARI = (255, 255, 0)
GUMI = (200, 200, 220)

# --- Oyuncu ---
OYUNCU_HIZ = 5

# --- Mermi ---
MERMI_HIZ = 8
MERMI_COOLDOWN = 250  # milisaniye

# --- Dusman ---
DUSMAN_OLAY = pygame.USEREVENT + 1
DUSMAN_ARALIK = 800


class Yildiz(pygame.sprite.Sprite):
    """Parallax kayan yildiz."""

    def __init__(self):
        super().__init__()
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
        self.y_float = float(self.rect.y)

    def update(self):
        self.y_float += self.hiz
        self.rect.y = int(self.y_float)
        if self.rect.top > YUKSEKLIK:
            self.rect.x = random.randint(0, GENISLIK)
            self.rect.y = -self.boyut
            self.y_float = float(self.rect.y)


class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi."""

    def __init__(self):
        super().__init__()
        self.genislik = 40
        self.yukseklik = 50
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        self._gemi_ciz()
        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.son_atis_zamani = 0

    def _gemi_ciz(self):
        noktalar = [
            (self.genislik // 2, 0),
            (0, self.yukseklik),
            (self.genislik, self.yukseklik),
        ]
        pygame.draw.polygon(self.image, ACIK_MAVI, noktalar)
        ic_noktalar = [
            (self.genislik // 2, 10),
            (8, self.yukseklik - 5),
            (self.genislik - 8, self.yukseklik - 5),
        ]
        pygame.draw.polygon(self.image, MAVI, ic_noktalar)
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

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > YUKSEKLIK:
            self.rect.bottom = YUKSEKLIK

    def ates_edebilir_mi(self):
        """Cooldown kontrolu."""
        simdi = pygame.time.get_ticks()
        if simdi - self.son_atis_zamani >= MERMI_COOLDOWN:
            self.son_atis_zamani = simdi
            return True
        return False


class Dusman(pygame.sprite.Sprite):
    """Dusman gemisi."""

    def __init__(self):
        super().__init__()
        self.genislik = 35
        self.yukseklik = 30
        self.hiz = random.uniform(2, 5)
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        self._gemi_ciz()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - self.genislik)
        self.rect.y = -self.yukseklik
        self.y_float = float(self.rect.y)

    def _gemi_ciz(self):
        noktalar = [
            (0, 0),
            (self.genislik, 0),
            (self.genislik // 2, self.yukseklik),
        ]
        pygame.draw.polygon(self.image, KIRMIZI, noktalar)
        ic_noktalar = [
            (6, 4),
            (self.genislik - 6, 4),
            (self.genislik // 2, self.yukseklik - 6),
        ]
        pygame.draw.polygon(self.image, KOYU_KIRMIZI, ic_noktalar)

    def update(self):
        self.y_float += self.hiz
        self.rect.y = int(self.y_float)
        if self.rect.top > YUKSEKLIK:
            self.kill()


class Mermi(pygame.sprite.Sprite):
    """Oyuncu mermisi. Sari dikdortgen, yukari hareket eder."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(SARI)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= MERMI_HIZ
        # Ekrandan ciktiysa sil
        if self.rect.bottom < 0:
            self.kill()


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Uzay Kacisi v2 - Adim 3: Mermi Sistemi")
    saat = pygame.time.Clock()

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()

    # Yildizlari olustur
    for _ in range(100):
        y = Yildiz()
        tum_spritelar.add(y)
        yildizlar.add(y)

    # Oyuncuyu olustur
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Dusman zamanlayicisi
    pygame.time.set_timer(DUSMAN_OLAY, DUSMAN_ARALIK)

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
            elif olay.type == DUSMAN_OLAY:
                d = Dusman()
                tum_spritelar.add(d)
                dusmanlar.add(d)

        # Space tusu ile ates (basili tutunca surekli ates)
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_SPACE] and oyuncu.ates_edebilir_mi():
            m = Mermi(oyuncu.rect.centerx, oyuncu.rect.top)
            tum_spritelar.add(m)
            mermiler.add(m)

        # --- Guncelleme ---
        tum_spritelar.update()

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        # HUD bilgileri
        dusman_metin = font.render(
            f"Dusmanlar: {len(dusmanlar)}", True, KIRMIZI
        )
        ekran.blit(dusman_metin, (10, 10))

        mermi_metin = font.render(
            f"Mermiler: {len(mermiler)}", True, SARI
        )
        ekran.blit(mermi_metin, (10, 36))

        bilgi = font.render(
            "WASD: Hareket | Space: Ates | ESC: Cikis", True, GUMI
        )
        ekran.blit(bilgi, (10, YUKSEKLIK - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# ============================================================
# BEKLENEN CIKTI
# ============================================================
# - Adim 2'deki her sey (yildizlar, oyuncu, dusmanlar)
# - Space tusuna basinca sari mermiler atesilir
# - Mermiler oyuncunun burun noktasindan cikar
# - 250ms cooldown: cok hizli ates edilemez
# - Space basili tutulunca surekli ates eder
# - Ekrandan cikan mermiler otomatik silinir
# - Sol ustte dusman ve mermi sayisi gosterilir
# - [OK] Mermi cooldown sistemi calisiyor
# - [OK] Mermiler duz yukari gidiyor
