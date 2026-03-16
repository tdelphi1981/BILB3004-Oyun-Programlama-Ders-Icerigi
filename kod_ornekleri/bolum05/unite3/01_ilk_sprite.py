"""
Ilk Sprite - pygame.sprite.Sprite ile temel Sprite olusturma

Bu program PyGame'in Sprite sinifini kullanarak ekranda
renkli kareler olusturur. Sprite kavrami, gorsel + konum + davranis
uclusunu tek bir nesne icinde birlestirmenin temelini gosterir.

Ogrenilecek kavramlar:
- pygame.sprite.Sprite sinifindan kalitim
- self.image ve self.rect zorunlu ozellikleri
- super().__init__() cagrisi
- blit() ile Sprite cizimi

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 3 - Sprite Sinifi

Calistirma: python 01_ilk_sprite.py
Gereksinimler: pygame
"""

import os
import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Ilk Sprite Ornegi"
ARKA_PLAN = (15, 15, 35)


def gorsel_yukle(dosya_yolu, boyut=None):
    """Gorsel dosyasini yukler, bulunamazsa renkli yuzey dondurur.

    Args:
        dosya_yolu: Gorsel dosyasinin yolu
        boyut: (genislik, yukseklik) demeti, None ise orijinal boyut

    Returns:
        pygame.Surface nesnesi
    """
    try:
        gorsel = pygame.image.load(dosya_yolu).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        return gorsel
    except (pygame.error, FileNotFoundError):
        # Dosya bulunamazsa renkli bir kare olustur
        if boyut is None:
            boyut = (40, 40)
        yuzey = pygame.Surface(boyut, pygame.SRCALPHA)
        yuzey.fill((100, 150, 255))  # Mavi fallback
        return yuzey


# ---------------------------------------------------------------------------
# Sprite Siniflari
# ---------------------------------------------------------------------------

class KirmiziKare(pygame.sprite.Sprite):
    """En basit Sprite: renkli bir kare.

    Bu sinif, Sprite olusturmanin temel adimlarini gosterir:
    1. super().__init__() ile ust sinifi baslat
    2. self.image ile gorunumu belirle
    3. self.rect ile konumu belirle
    """

    def __init__(self, x, y):
        """Sprite'i belirtilen konumda olusturur.

        Args:
            x: Merkezin x koordinati
            y: Merkezin y koordinati
        """
        super().__init__()
        # 40x40 piksel boyutunda bos bir Surface olustur
        self.image = pygame.Surface((40, 40))
        self.image.fill((220, 30, 30))  # Kirmizi ile doldur
        # Rect'i belirtilen konuma yerlestir
        self.rect = self.image.get_rect(center=(x, y))


class MaviDaire(pygame.sprite.Sprite):
    """Daire seklinde bir Sprite.

    Surface uzerinde daire cizerek farkli sekiller
    olusturulabilecegini gosterir.
    """

    def __init__(self, x, y):
        """Sprite'i belirtilen konumda olusturur.

        Args:
            x: Merkezin x koordinati
            y: Merkezin y koordinati
        """
        super().__init__()
        # Seffaf arka planli bir Surface olustur
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Daire ciz
        pygame.draw.circle(self.image, (50, 120, 220), (25, 25), 25)
        self.rect = self.image.get_rect(center=(x, y))


class YesilKare(pygame.sprite.Sprite):
    """Gorsel dosyasindan veya fallback'ten olusturulan Sprite."""

    def __init__(self, x, y):
        """Sprite'i belirtilen konumda olusturur.

        Args:
            x: Merkezin x koordinati
            y: Merkezin y koordinati
        """
        super().__init__()
        self.image = pygame.Surface((35, 35))
        self.image.fill((30, 180, 60))  # Yesil
        # Kenarlık ekle
        pygame.draw.rect(self.image, (20, 120, 40), (0, 0, 35, 35), 2)
        self.rect = self.image.get_rect(center=(x, y))


class UzayGemisi(pygame.sprite.Sprite):
    """Kenney asset paketinden uzay gemisi Sprite'i.

    gorsel_yukle() fonksiyonu ile dosyadan yuklenir.
    Dosya bulunamazsa mavi kare fallback kullanilir.
    """

    def __init__(self, x, y):
        """Sprite'i belirtilen konumda olusturur.

        Args:
            x: Merkezin x koordinati
            y: Merkezin y koordinati
        """
        super().__init__()
        self.image = gorsel_yukle(
            "assets/images/playerShip1_blue.png", (50, 40)
        )
        self.rect = self.image.get_rect(center=(x, y))


def main():
    """Ana program fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Sprite'lari olustur
    sprite_listesi = [
        KirmiziKare(200, 200),
        KirmiziKare(300, 200),
        MaviDaire(400, 200),
        MaviDaire(500, 200),
        YesilKare(600, 200),
        UzayGemisi(400, 400),
    ]

    # Bilgilendirme yazisi icin font
    font = pygame.font.Font(None, 28)

    print("=" * 55)
    print("  Ilk Sprite Ornegi")
    print("  Ekranda farkli turde Sprite'lar goruyor olmalisin.")
    print("  ESC ile cikis yapabilirsin.")
    print("=" * 55)

    calistir = True
    while calistir:
        # --- Olay isleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- Cizim ---
        ekran.fill(ARKA_PLAN)

        # Her Sprite'i tek tek ciz (Grup olmadan)
        for sprite in sprite_listesi:
            ekran.blit(sprite.image, sprite.rect)

        # Bilgilendirme metni
        bilgi = font.render(
            "6 farkli Sprite -- ESC ile cikis",
            True, (180, 180, 200)
        )
        ekran.blit(bilgi, (GENISLIK // 2 - bilgi.get_width() // 2, 30))

        # Sprite turlerini etiketle
        etiketler = [
            ("KirmiziKare", 250, 160),
            ("MaviDaire", 450, 160),
            ("YesilKare", 600, 160),
            ("UzayGemisi", 400, 360),
        ]
        etiket_font = pygame.font.Font(None, 22)
        for metin, ex, ey in etiketler:
            etiket = etiket_font.render(metin, True, (140, 140, 160))
            ekran.blit(etiket, (ex - etiket.get_width() // 2, ey))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()
    print("\nProgram sonlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
=======================================================
  Ilk Sprite Ornegi
  Ekranda farkli turde Sprite'lar goruyor olmalisin.
  ESC ile cikis yapabilirsin.
=======================================================

Ekranda 800x600 boyutunda koyu lacivert pencere acilir.
Ust sirada 2 kirmizi kare, 2 mavi daire ve 1 yesil kare gorulur.
Alt sirada uzay gemisi Sprite'i (veya mavi kare fallback) gorulur.
Her Sprite'in uzerinde sinif adi etiketi yer alir.
ESC tusuna basildiginda program kapanir.

Program sonlandi.
"""
