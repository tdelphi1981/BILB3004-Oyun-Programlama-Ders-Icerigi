"""
Carpisma Yontemi Karsilastirma - rect, circle, mask

Ucgen bir gemiyi fare ile hareket ettirerek bir daireye
yaklastirdiginda, uc farkli carpisma yonteminin hangisinin
carpisma tespit ettigini gercek zamanli olarak gosterir.

Ogrenilecek kavramlar:
- collide_rect (dikdortgen carpisma)
- collide_circle (daire carpisma)
- collide_mask (piksel carpisma)
- Uc yontem arasindaki fark

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 2 - Sprite Carpisma Fonksiyonlari

Calistirma: python 03_carpisma_yontemleri.py
Gereksinimler: pygame
"""

import pygame
import sys


# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Carpisma Yontemleri Karsilastirma"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (220, 50, 50)
YESIL = (50, 200, 50)
SARI = (255, 220, 50)
ACIK_MAVI = (100, 180, 255)
KOYU_MAVI = (8, 8, 32)
GRI = (120, 120, 120)
ACIK_KIRMIZI = (255, 100, 100)
ACIK_YESIL = (100, 255, 100)


# --- Sprite Siniflari ---
class Gemi(pygame.sprite.Sprite):
    """Ucgen seklinde fare ile kontrol edilen gemi."""

    def __init__(self):
        super().__init__()
        boyut = 60
        self.image = pygame.Surface(
            (boyut, boyut), pygame.SRCALPHA
        )
        # Ucgen ciz
        pygame.draw.polygon(
            self.image, ACIK_MAVI,
            [(boyut // 2, 5), (boyut - 5, boyut - 5), (5, boyut - 5)]
        )
        self.rect = self.image.get_rect(center=(200, 300))
        # Piksel bazli carpisma icin maske
        self.mask = pygame.mask.from_surface(self.image)
        # Daire bazli carpisma icin yaricap
        self.radius = boyut // 2

    def update(self):
        """Fare konumunu takip et."""
        self.rect.center = pygame.mouse.get_pos()


class Hedef(pygame.sprite.Sprite):
    """Sabit duran daire seklinde hedef."""

    def __init__(self, x, y, yaricap):
        super().__init__()
        boyut = yaricap * 2
        self.image = pygame.Surface(
            (boyut, boyut), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, KIRMIZI,
            (yaricap, yaricap), yaricap
        )
        self.rect = self.image.get_rect(center=(x, y))
        # Piksel bazli carpisma icin maske
        self.mask = pygame.mask.from_surface(self.image)
        # Daire bazli carpisma icin yaricap
        self.radius = yaricap


def rect_ciz(ekran, sprite):
    """Sprite'in rect sinirlariini ciz."""
    pygame.draw.rect(ekran, GRI, sprite.rect, 1)


def circle_ciz(ekran, sprite):
    """Sprite'in circle sinirini ciz."""
    yaricap = getattr(sprite, "radius", sprite.rect.width // 2)
    pygame.draw.circle(
        ekran, GRI, sprite.rect.center, yaricap, 1
    )


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    font_buyuk = pygame.font.Font(None, 40)

    # Sprite'lari olustur
    gemi = Gemi()
    hedef = Hedef(GENISLIK // 2, YUKSEKLIK // 2, 50)

    gemi_grup = pygame.sprite.Group(gemi)
    hedef_grup = pygame.sprite.Group(hedef)

    # Fare imlecini gizle
    pygame.mouse.set_visible(False)

    # --- Ana Oyun Dongusu ---
    calistir = True
    while calistir:
        saat.tick(FPS)

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Guncelleme
        gemi.update()

        # --- Uc farkli carpisma kontrolu ---
        rect_carpisma = pygame.sprite.spritecollide(
            gemi, hedef_grup, False, pygame.sprite.collide_rect
        )
        circle_carpisma = pygame.sprite.spritecollide(
            gemi, hedef_grup, False, pygame.sprite.collide_circle
        )
        mask_carpisma = pygame.sprite.spritecollide(
            gemi, hedef_grup, False, pygame.sprite.collide_mask
        )

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)

        # Rect sinirlarini ciz
        rect_ciz(ekran, gemi)
        rect_ciz(ekran, hedef)

        # Circle sinirlarini ciz
        circle_ciz(ekran, gemi)
        circle_ciz(ekran, hedef)

        # Sprite'lari ciz
        ekran.blit(hedef.image, hedef.rect)
        ekran.blit(gemi.image, gemi.rect)

        # --- Sonuc tablosu ---
        tablo_x = 20
        tablo_y = 20

        baslik_yazi = font_buyuk.render(
            "Carpisma Yontemleri", True, BEYAZ
        )
        ekran.blit(baslik_yazi, (tablo_x, tablo_y))
        tablo_y += 45

        # Rect sonucu
        rect_renk = ACIK_YESIL if rect_carpisma else ACIK_KIRMIZI
        rect_durum = "CARPISMA" if rect_carpisma else "---"
        rect_yazi = font.render(
            f"collide_rect:   {rect_durum}", True, rect_renk
        )
        ekran.blit(rect_yazi, (tablo_x, tablo_y))
        tablo_y += 30

        # Circle sonucu
        circle_renk = ACIK_YESIL if circle_carpisma else ACIK_KIRMIZI
        circle_durum = "CARPISMA" if circle_carpisma else "---"
        circle_yazi = font.render(
            f"collide_circle: {circle_durum}", True, circle_renk
        )
        ekran.blit(circle_yazi, (tablo_x, tablo_y))
        tablo_y += 30

        # Mask sonucu
        mask_renk = ACIK_YESIL if mask_carpisma else ACIK_KIRMIZI
        mask_durum = "CARPISMA" if mask_carpisma else "---"
        mask_yazi = font.render(
            f"collide_mask:   {mask_durum}", True, mask_renk
        )
        ekran.blit(mask_yazi, (tablo_x, tablo_y))

        # Bilgi yazisi
        bilgi = font.render(
            "Fare ile gemiyi hedefe yaklastir | ESC: Cikis",
            True, GRI
        )
        bilgi_rect = bilgi.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 15
        )
        ekran.blit(bilgi, bilgi_rect)

        aciklama = font.render(
            "Gri: rect siniri | Gri daire: circle siniri",
            True, GRI
        )
        aciklama_rect = aciklama.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 45
        )
        ekran.blit(aciklama, aciklama_rect)

        pygame.display.flip()

    # --- Temizlik ---
    pygame.mouse.set_visible(True)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
Ekranin ortasinda kirmizi bir daire (hedef) durur.
Fare ile mavi ucgen (gemi) hareket ettirilir.

Sol ustte uc carpisma yonteminin sonucu gercek zamanli
gosterilir:
- collide_rect: Dikdortgen sinirlar ortusunce CARPISMA
- collide_circle: Daire sinirlari ortusunce CARPISMA
- collide_mask: Gercek pikseller ortusunce CARPISMA

Ucgenin kose bolgelerinde rect "CARPISMA" derken mask
"---" der -- cunku koseler seffaf.
Daire ile ucgenin tam arasinda circle "CARPISMA" derken
mask hala "---" diyebilir -- cunku pikseller henuz
ortusmuyor olabilir.
"""
