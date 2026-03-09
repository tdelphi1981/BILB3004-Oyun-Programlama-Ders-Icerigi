"""
Uzay Kacisi v2 - Adim 5: HUD: Can Cubugu + Skor

Profesyonel gorunumlu bir HUD (Heads-Up Display) ekliyoruz.
Can cubugu renk degistirir (yesil/turuncu/kirmizi), skor ve
dusman sayisi gorsel olarak gosterilir.

Ogrenilecek kavramlar:
- HUD tasarimi ve cizimi
- Can cubugu (health bar) uygulamasi
- Renk gecisleri (can durumuna gore)
- Oyun bilgisi gosterimi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Uzay Kacisi v2 (Adim 5/7)

Calistirma: uv run python adim5_can_ve_skor.py
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
YESIL = (50, 200, 50)
TURUNCU = (255, 165, 0)
GUMI = (200, 200, 220)
KOYU_GRI = (40, 40, 50)

# --- Oyuncu ---
OYUNCU_HIZ = 5
OYUNCU_CAN = 100
DUSMAN_HASAR = 25

# --- Mermi ---
MERMI_HIZ = 8
MERMI_COOLDOWN = 250

# --- Dusman ---
DUSMAN_OLAY = pygame.USEREVENT + 1
DUSMAN_ARALIK = 800
DUSMAN_PUAN = 10


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
        self.can = OYUNCU_CAN

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
        simdi = pygame.time.get_ticks()
        if simdi - self.son_atis_zamani >= MERMI_COOLDOWN:
            self.son_atis_zamani = simdi
            return True
        return False

    def hasar_al(self, miktar):
        self.can -= miktar
        if self.can < 0:
            self.can = 0


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
    """Oyuncu mermisi."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(SARI)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= MERMI_HIZ
        if self.rect.bottom < 0:
            self.kill()


def hud_ciz(ekran, font, skor, oyuncu, dusmanlar):
    """HUD (Heads-Up Display) ciz: skor, dusman sayisi, can cubugu."""
    # --- Sol ust: Skor ---
    skor_metin = font.render(f"Skor: {skor}", True, SARI)
    ekran.blit(skor_metin, (10, 10))

    # --- Sol ust ikinci satir: Dusman sayisi ---
    dusman_metin = font.render(
        f"Dusmanlar: {len(dusmanlar)}", True, KIRMIZI
    )
    ekran.blit(dusman_metin, (10, 36))

    # --- Sag ust: Can cubugu ---
    cubuk_genislik = 200
    cubuk_yukseklik = 20
    cubuk_x = GENISLIK - cubuk_genislik - 10
    cubuk_y = 10

    # Can yuzdesi
    can_yuzde = oyuncu.can / OYUNCU_CAN

    # Renk secimi: yesil > 60%, turuncu > 30%, kirmizi <= 30%
    if can_yuzde > 0.6:
        cubuk_renk = YESIL
    elif can_yuzde > 0.3:
        cubuk_renk = TURUNCU
    else:
        cubuk_renk = KIRMIZI

    # Arka plan (koyu gri)
    pygame.draw.rect(
        ekran, KOYU_GRI,
        (cubuk_x, cubuk_y, cubuk_genislik, cubuk_yukseklik)
    )
    # Dolu kisim
    dolu_genislik = int(cubuk_genislik * can_yuzde)
    if dolu_genislik > 0:
        pygame.draw.rect(
            ekran, cubuk_renk,
            (cubuk_x, cubuk_y, dolu_genislik, cubuk_yukseklik)
        )
    # Cerceve
    pygame.draw.rect(
        ekran, BEYAZ,
        (cubuk_x, cubuk_y, cubuk_genislik, cubuk_yukseklik), 2
    )

    # Can metni (cubuk altinda)
    can_metin = font.render(f"Can: {oyuncu.can}/{OYUNCU_CAN}", True, BEYAZ)
    can_rect = can_metin.get_rect()
    can_rect.right = GENISLIK - 10
    can_rect.top = cubuk_y + cubuk_yukseklik + 4
    ekran.blit(can_metin, can_rect)

    # --- Alt: Kontrol bilgisi ---
    kontrol_metin = font.render(
        "WASD: Hareket | Space: Ates | ESC: Cikis", True, GUMI
    )
    ekran.blit(kontrol_metin, (10, YUKSEKLIK - 30))


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Uzay Kacisi v2 - Adim 5: Can ve Skor HUD")
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
    skor = 0

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

        # Space ile ates
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_SPACE] and oyuncu.ates_edebilir_mi():
            m = Mermi(oyuncu.rect.centerx, oyuncu.rect.top)
            tum_spritelar.add(m)
            mermiler.add(m)

        # --- Guncelleme ---
        tum_spritelar.update()

        # --- Carpisma Algilama ---
        carpismalar = pygame.sprite.groupcollide(
            mermiler, dusmanlar, True, True
        )
        for mermi, vurulan_dusmanlar in carpismalar.items():
            skor += DUSMAN_PUAN * len(vurulan_dusmanlar)

        dusman_carpismalari = pygame.sprite.spritecollide(
            oyuncu, dusmanlar, True
        )
        for dusman in dusman_carpismalari:
            oyuncu.hasar_al(DUSMAN_HASAR)

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        # HUD cizimi
        hud_ciz(ekran, font, skor, oyuncu, dusmanlar)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# ============================================================
# BEKLENEN CIKTI
# ============================================================
# - Adim 4'teki her sey (carpismalar, skor, can)
# - Sol ustte sari skor metni
# - Sol ustte ikinci satirda kirmizi dusman sayisi
# - Sag ustte can cubugu:
#   - Can > %60: yesil
#   - Can > %30: turuncu
#   - Can <= %30: kirmizi
# - Can cubugunun altinda "Can: XX/100" metni
# - Alt kisimda kontrol bilgisi
# - [OK] HUD profesyonel gorunumlu
# - [OK] Can cubugu renk gecisleri calisiyor
