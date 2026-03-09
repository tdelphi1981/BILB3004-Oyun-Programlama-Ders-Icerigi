"""
Tugla Kirma (Breakout) - Adim 4: spritecollide ile Tugla Kirma + Skor

Top tuglalara carptiginda tuglalar kirilir ve skor artar.
Tum tuglalar kirildiginda kazanma mesaji gosterilir.

Ogrenilecek kavramlar:
- pygame.sprite.spritecollide() kullanimi
- Grup icerisinden sprite silme (dokill=True)
- Skor takibi ve kazanma kosulu

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Tugla Kirma (Adim 4/7)

Calistirma: uv run python adim4_tugla_kirma.py
Gereksinimler: pygame
"""

import pygame
import sys
import math

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
TOP_HIZ = 5
RAKET_HIZ = 7

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

    def update(self):
        """Klavye ile raket hareketi."""
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]:
            self.rect.x -= RAKET_HIZ
        if tuslar[pygame.K_RIGHT]:
            self.rect.x += RAKET_HIZ
        self.rect.clamp_ip(pygame.Rect(0, 0, GENISLIK, YUKSEKLIK))


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
        self.hiz_x = 3.0
        self.hiz_y = -4.0

    def update(self):
        """Top hareketi ve duvar sekmeleri."""
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        if self.rect.left <= 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x)
        elif self.rect.right >= GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.hiz_y = abs(self.hiz_y)

    def raket_sekmesi(self, raket):
        """Raket ile carpisma ve aci hesabi."""
        if self.rect.colliderect(raket.rect) and self.hiz_y > 0:
            vurun_x = self.rect.centerx - raket.rect.left
            oran = vurun_x / raket.rect.width
            aci = (oran - 0.5) * 120

            self.hiz_x = math.sin(math.radians(aci)) * TOP_HIZ
            self.hiz_y = -abs(math.cos(math.radians(aci)) * TOP_HIZ)
            self.rect.bottom = raket.rect.top


class Tugla(pygame.sprite.Sprite):
    """Kirilan tugla nesnesi."""

    def __init__(self, x, y, renk):
        super().__init__()
        self.image = pygame.Surface((TUGLA_GENISLIK, TUGLA_YUKSEKLIK))
        self.image.fill(renk)
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
    pygame.display.set_caption("Tugla Kirma - Adim 4: Tugla Kirma + Skor")
    saat = pygame.time.Clock()
    yazi_tipi = pygame.font.SysFont("Arial", 24)
    buyuk_yazi = pygame.font.SysFont("Arial", 48, bold=True)

    raket = Raket()
    top = Top()
    tuglalar = tugla_olustur()

    tum_spritelar = pygame.sprite.Group()
    tum_spritelar.add(raket, top)
    tum_spritelar.add(tuglalar)

    skor = 0
    can = 3
    kazandi = False

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        if not kazandi:
            # Guncelle
            raket.update()
            top.update()
            top.raket_sekmesi(raket)

            # Tugla carpisma kontrolu - spritecollide ile
            kirilan_tuglalar = pygame.sprite.spritecollide(top, tuglalar, True)
            if kirilan_tuglalar:
                top.hiz_y = -top.hiz_y
                skor += len(kirilan_tuglalar) * 10

            # Top ekrandan cikarsa sifirla
            if top.rect.top > YUKSEKLIK:
                top.rect.center = (GENISLIK // 2, YUKSEKLIK // 2)
                top.hiz_x = 3.0
                top.hiz_y = -4.0

            # Kazanma kontrolu
            if len(tuglalar) == 0:
                kazandi = True

        # Ciz
        ekran.fill(SIYAH)
        tum_spritelar.draw(ekran)

        skor_yazi = yazi_tipi.render(f"Skor: {skor}", True, BEYAZ)
        can_yazi = yazi_tipi.render(f"Can: {can}", True, BEYAZ)
        ekran.blit(skor_yazi, (10, 10))
        ekran.blit(can_yazi, (GENISLIK - 80, 10))

        if kazandi:
            kazan_yazi = buyuk_yazi.render("KAZANDINIZ!", True, YESIL)
            kazan_rect = kazan_yazi.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2))
            ekran.blit(kazan_yazi, kazan_rect)

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# --- BEKLENEN CIKTI ---
# [OK] Top tuglalara carptiginda tuglalar kirilir (kaybolur)
# [OK] Her kirilan tugla icin skor 10 puan artar
# [OK] Top tugla carpismasinda yon degistirir (hiz_y ters doner)
# [OK] Skor sol ustte guncellenir
# [OK] Tum tuglalar kirildiktan sonra "KAZANDINIZ!" mesaji gorulur
# [OK] Kazanma durumunda oyun durur
# [OK] ESC ile cikis yapilir
