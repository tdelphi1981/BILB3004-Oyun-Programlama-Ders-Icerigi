"""
Sprite Grubu Temel Islemleri - Group kullanimi ornegi

Bu program, pygame.sprite.Group sinifinin temel islemlerini
gosterir: Sprite olusturma, gruba ekleme, cikarma, uyelik
kontrolu, toplu cizim ve guncelleme.

Ogrenilecek kavramlar:
- pygame.sprite.Group() ile grup olusturma
- add(), remove(), has(), kill() islemleri
- group.draw() ve group.update() kullanimi
- Bir Sprite'in birden fazla gruba ait olmasi

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 4 - Sprite Gruplari

Calistirma: python 01_sprite_grubu.py
Gereksinimler: pygame
"""

import pygame
import random
import os
import sys


# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Sprite Grubu Islemleri"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_GRI = (30, 30, 40)
ACIK_GRI = (180, 180, 180)

# Sprite renkleri
RENKLER = [
    (255, 80, 80),    # Kirmizi
    (80, 255, 80),    # Yesil
    (80, 80, 255),    # Mavi
    (255, 255, 80),   # Sari
    (255, 80, 255),   # Pembe
    (80, 255, 255),   # Camgobegi
]


def gorsel_yukle(dosya_adi, boyut=None):
    """Gorsel dosyasini yukle, bulunamazsa renkli yedek olustur."""
    try:
        yol = os.path.join("kod_ornekleri", "bolum05", "assets", dosya_adi)
        gorsel = pygame.image.load(yol).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        return gorsel
    except (pygame.error, FileNotFoundError):
        # Yedek yuzey olustur
        genislik = boyut[0] if boyut else 40
        yukseklik = boyut[1] if boyut else 40
        yuzey = pygame.Surface((genislik, yukseklik), pygame.SRCALPHA)
        renk = random.choice(RENKLER)
        pygame.draw.rect(yuzey, renk, (0, 0, genislik, yukseklik),
                         border_radius=4)
        pygame.draw.rect(yuzey, BEYAZ, (0, 0, genislik, yukseklik),
                         width=2, border_radius=4)
        return yuzey


# --- Sprite Siniflari ---
class RenkliKare(pygame.sprite.Sprite):
    """Rastgele renkli, yatay hareket eden kare Sprite."""

    def __init__(self, x, y, boyut=40):
        super().__init__()
        self.renk = random.choice(RENKLER)
        self.image = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.renk, (0, 0, boyut, boyut),
                         border_radius=5)
        pygame.draw.rect(self.image, BEYAZ, (0, 0, boyut, boyut),
                         width=2, border_radius=5)
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz_x = random.choice([-2, -1, 1, 2])
        self.hiz_y = random.choice([-1, 0, 1])

    def update(self):
        """Her karede konumu guncelle ve sinir kontrolu yap."""
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Ekran sinirlarina carparsa yon degistir
        if self.rect.left < 0 or self.rect.right > GENISLIK:
            self.hiz_x *= -1
        if self.rect.top < 0 or self.rect.bottom > YUKSEKLIK:
            self.hiz_y *= -1

        # Ekran icinde tut
        self.rect.clamp_ip(pygame.Rect(0, 0, GENISLIK, YUKSEKLIK))


def bilgi_yazdir(ekran, font, tum_spritelar, ozel_grup):
    """Ekrana grup bilgilerini yazdir."""
    bilgiler = [
        f"Toplam Sprite: {len(tum_spritelar)}",
        f"Ozel Grup: {len(ozel_grup)}",
        "",
        "Kontroller:",
        "  SPACE : Yeni Sprite ekle",
        "  R     : Rastgele Sprite sil (kill)",
        "  C     : Ozel grubu bosalt (empty)",
        "  ESC   : Cikis",
    ]
    y_pos = 10
    for satir in bilgiler:
        yazi = font.render(satir, True, ACIK_GRI)
        ekran.blit(yazi, (10, y_pos))
        y_pos += 22


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # --- Gruplari olustur ---
    tum_spritelar = pygame.sprite.Group()
    ozel_grup = pygame.sprite.Group()

    # Baslangicta 10 adet Sprite ekle
    for _ in range(10):
        x = random.randint(100, GENISLIK - 100)
        y = random.randint(100, YUKSEKLIK - 100)
        sprite = RenkliKare(x, y)
        tum_spritelar.add(sprite)
        # Cift sayili olanlar ozel gruba da eklensin
        if random.random() > 0.5:
            ozel_grup.add(sprite)

    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olay isleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                elif olay.key == pygame.K_SPACE:
                    # Yeni Sprite ekle
                    x = random.randint(50, GENISLIK - 50)
                    y = random.randint(50, YUKSEKLIK - 50)
                    yeni = RenkliKare(x, y)
                    tum_spritelar.add(yeni)
                    if random.random() > 0.5:
                        ozel_grup.add(yeni)

                elif olay.key == pygame.K_r:
                    # Rastgele bir Sprite'i kill() ile sil
                    sprite_listesi = tum_spritelar.sprites()
                    if sprite_listesi:
                        secilen = random.choice(sprite_listesi)
                        secilen.kill()  # Tum gruplardan cikar

                elif olay.key == pygame.K_c:
                    # Ozel grubu bosalt
                    ozel_grup.empty()

        # --- Guncelleme ---
        tum_spritelar.update()

        # --- Cizim ---
        ekran.fill(KOYU_GRI)
        tum_spritelar.draw(ekran)
        bilgi_yazdir(ekran, font, tum_spritelar, ozel_grup)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
Ekranda 10 adet renkli kare rastgele yonlerde hareket eder.
Space ile yeni kare eklenir, R ile rastgele biri silinir.
C ile ozel grup bosaltilir. Sol ustte grup bilgileri gosterilir.
Kareler ekran sinirlarina carptiklari zaman yon degistirir.
"""
