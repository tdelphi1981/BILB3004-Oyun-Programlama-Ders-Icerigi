"""
Hareketli Sprite - update() metodu ile Sprite hareketi

Bu program update() metodunu override ederek Sprite'lara
hareket kazandirmayi gosterir. Birden fazla dusman Sprite'i
ekranin ustunden asagiya dogru hareket eder. Ekrandan cikan
Sprite'lar kill() ile yok edilir ve yenileri olusturulur.

Ogrenilecek kavramlar:
- update() metodunu override etme
- self.rect.x / self.rect.y ile hareket
- kill() ile Sprite'i yok etme
- Ekran siniri kontrolu (sarmalama ve yok etme)

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 3 - Sprite Sinifi

Calistirma: python 02_hareketli_sprite.py
Gereksinimler: pygame
"""

import os
import random
import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Hareketli Sprite Ornegi"
ARKA_PLAN = (10, 10, 30)
DUSMAN_SAYISI = 8


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
        if boyut is None:
            boyut = (40, 40)
        yuzey = pygame.Surface(boyut, pygame.SRCALPHA)
        yuzey.fill((200, 60, 60))  # Kirmizi fallback
        return yuzey


# ---------------------------------------------------------------------------
# Sprite Siniflari
# ---------------------------------------------------------------------------

class SolaKayanKare(pygame.sprite.Sprite):
    """Soldan saga suren bir kare Sprite'i.

    Ekranin sagindan cikinca soldan tekrar girer (sarmalama).
    """

    def __init__(self, x, y, renk, hiz):
        """Sprite'i olusturur.

        Args:
            x: Baslangic x koordinati
            y: Baslangic y koordinati
            renk: (R, G, B) renk demeti
            hiz: Kare basina piksel hareketi
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(renk)
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz = hiz

    def update(self):
        """Her karede saga dogru hareket et. Ekrandan cikinca sarmala."""
        self.rect.x += self.hiz
        # Sarmalama: sagdan cikinca soldan gir
        if self.rect.left > GENISLIK:
            self.rect.right = 0


class DusmanSprite(pygame.sprite.Sprite):
    """Ekranin ustunden asagiya inen dusman Sprite'i.

    Rastgele yatay konum ve hizla olusturulur.
    Ekranin altindan cikinca kill() ile yok edilir.
    """

    def __init__(self):
        """Sprite'i rastgele konum ve hizla olusturur."""
        super().__init__()
        # Rastgele boyut (25-45 piksel arasi)
        boyut = random.randint(25, 45)
        self.image = pygame.Surface((boyut, boyut), pygame.SRCALPHA)

        # Rastgele kirmizi tonu
        kirmizi = random.randint(150, 230)
        renk = (kirmizi, random.randint(20, 60), random.randint(20, 60))
        pygame.draw.rect(self.image, renk, (0, 0, boyut, boyut),
                         border_radius=4)

        # Rastgele yatay konum, ekranin ustunde baslat
        self.rect = self.image.get_rect(
            center=(random.randint(40, GENISLIK - 40), random.randint(-80, -20))
        )
        self.hiz = random.uniform(1.5, 4.5)

    def update(self):
        """Her karede asagiya dogru hareket et. Ekrandan cikinca yok et."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


class YildizSprite(pygame.sprite.Sprite):
    """Arka planda yavas hareket eden yildiz efekti."""

    def __init__(self):
        """Yildiz Sprite'i olusturur."""
        super().__init__()
        boyut = random.randint(1, 3)
        self.image = pygame.Surface((boyut, boyut))
        parlaklik = random.randint(100, 220)
        self.image.fill((parlaklik, parlaklik, parlaklik + 30))
        self.rect = self.image.get_rect(
            center=(random.randint(0, GENISLIK),
                    random.randint(0, YUKSEKLIK))
        )
        self.hiz = random.uniform(0.3, 1.2)

    def update(self):
        """Yavasca asagi kay, ekrandan cikinca ustten tekrar baslat."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, GENISLIK)


def main():
    """Ana program fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # --- Sprite'lari olustur ---
    # Yildizlar (arka plan efekti)
    yildizlar = [YildizSprite() for _ in range(60)]

    # Yatay kayan kareler
    kayan_kareler = [
        SolaKayanKare(100, 100, (50, 180, 80), 2),
        SolaKayanKare(300, 100, (80, 120, 220), 3),
        SolaKayanKare(500, 100, (220, 180, 40), 4),
    ]

    # Dusmanlar
    dusmanlar = [DusmanSprite() for _ in range(DUSMAN_SAYISI)]

    # Istatistikler
    yok_edilen = 0
    font = pygame.font.Font(None, 26)

    print("=" * 55)
    print("  Hareketli Sprite Ornegi")
    print("  Dusmanlar yukari sagdan asagiya hareket eder.")
    print("  Ekrandan cikan dusmanlar yok edilir, yenileri olusur.")
    print("  ESC ile cikis.")
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

        # --- Guncelleme ---
        # Yildizlari guncelle
        for yildiz in yildizlar:
            yildiz.update()

        # Kayan kareleri guncelle
        for kare in kayan_kareler:
            kare.update()

        # Dusmanlari guncelle
        onceki_sayi = len(dusmanlar)
        for dusman in dusmanlar:
            dusman.update()

        # Yok edilen dusmanlari listeden cikar
        dusmanlar = [d for d in dusmanlar if d.alive()]
        yok_edilen += onceki_sayi - len(dusmanlar)

        # Eksik dusmanlari yenile
        while len(dusmanlar) < DUSMAN_SAYISI:
            dusmanlar.append(DusmanSprite())

        # --- Cizim ---
        ekran.fill(ARKA_PLAN)

        # Yildizlari ciz
        for yildiz in yildizlar:
            ekran.blit(yildiz.image, yildiz.rect)

        # Kayan kareleri ciz
        for kare in kayan_kareler:
            ekran.blit(kare.image, kare.rect)

        # Dusmanlari ciz
        for dusman in dusmanlar:
            ekran.blit(dusman.image, dusman.rect)

        # Bilgi metni
        bilgi_metin = (
            f"Aktif dusmanlar: {len(dusmanlar)}  |  "
            f"Yok edilen: {yok_edilen}  |  ESC: Cikis"
        )
        bilgi = font.render(bilgi_metin, True, (180, 180, 200))
        ekran.blit(bilgi, (10, 10))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()
    print(f"\nToplam yok edilen dusman: {yok_edilen}")
    print("Program sonlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
=======================================================
  Hareketli Sprite Ornegi
  Dusmanlar yukari sagdan asagiya hareket eder.
  Ekrandan cikan dusmanlar yok edilir, yenileri olusur.
  ESC ile cikis.
=======================================================

Ekranda 800x600 boyutunda koyu pencere acilir.
- Arka planda yavasca kayan yildiz efektleri gorulur.
- Ust sirada 3 farkli renkte kare soldan saga kayar.
- Ortada ve asagida kirmizi tonlarinda dusmanlar yukari sagdan
  asagiya dogru hareket eder.
- Ekrandan cikan dusmanlar yok edilir ve yenileri olusturulur.
- Sol ustte aktif dusman sayisi ve yok edilen sayisi gorulur.

Toplam yok edilen dusman: 42
Program sonlandi.
"""
