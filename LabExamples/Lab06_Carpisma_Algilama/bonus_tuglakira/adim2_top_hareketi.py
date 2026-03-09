"""
Tugla Kirma (Breakout) - Adim 2: Top Hareketi ve Duvar Sekmeleri

Raket hareket eder, top hareket eder ve duvarlardan sekme yapar.
Top ekranin altindan cikarsa ortaya doner.

Ogrenilecek kavramlar:
- Sprite hareket kontrolu (klavye girisi)
- Hiz vektoru ile top hareketi
- Duvar carpisma kontrolu ve yon degistirme

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Tugla Kirma (Adim 2/7)

Calistirma: uv run python adim2_top_hareketi.py
Gereksinimler: pygame
"""

import pygame
import sys

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
        # Ekran sinirlarinda tut
        self.rect.clamp_ip(pygame.Rect(0, 0, GENISLIK, YUKSEKLIK))


class Top(pygame.sprite.Sprite):
    """Oyun topu - hareket eder ve duvarlardan sekme yapar."""

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

        # Sol ve sag duvar sekmeleri
        if self.rect.left <= 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x)
        elif self.rect.right >= GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x)

        # Ust duvar sekmesi
        if self.rect.top <= 0:
            self.rect.top = 0
            self.hiz_y = abs(self.hiz_y)

        # Alt sinir - top ekrandan cikarsa ortaya don
        if self.rect.top > YUKSEKLIK:
            self.rect.center = (GENISLIK // 2, YUKSEKLIK // 2)
            self.hiz_x = 3.0
            self.hiz_y = -4.0


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
    pygame.display.set_caption("Tugla Kirma - Adim 2: Top Hareketi")
    saat = pygame.time.Clock()
    yazi_tipi = pygame.font.SysFont("Arial", 24)

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

        # Guncelle
        raket.update()
        top.update()

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
# [OK] Top ekranin ortasindan hareket etmeye baslar
# [OK] Top sol, sag ve ust duvarlardan sekmeler yapar
# [OK] Top ekranin altindan cikarsa ortaya geri doner
# [OK] Sol/Sag ok tuslari ile raket hareket eder
# [OK] Raket ekran sinirlarinin disina cikamaz
# [OK] Tuglalar gorulur ama henuz kirilmaz
# [OK] ESC ile cikis yapilir
