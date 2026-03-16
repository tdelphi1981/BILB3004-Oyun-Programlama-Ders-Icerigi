"""
Coklu Sprite Yonetimi - Yildiz Arka Plani

Bu program, cok sayida Sprite'i bir Group ile yoneterek
kayan yildiz arka plani olusturur. Her yildiz farkli
boyut ve hizda hareket eder, ekran disindan tekrar girer.

Ogrenilecek kavramlar:
- Cok sayida Sprite olusturma ve yonetme
- Group ile toplu draw() ve update()
- Farkli hizlarda paralaks efekti
- Ekran disi kontrolu ve yeniden konumlandirma

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 4 - Sprite Gruplari

Calistirma: python 02_coklu_sprite.py
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
BASLIK = "Kayan Yildiz Arka Plani"

# Renkler
KOYU_MAVI = (5, 5, 25)
BEYAZ = (255, 255, 255)
ACIK_GRI = (180, 180, 190)
SOLUK_BEYAZ = (200, 200, 210)

# Yildiz ayarlari
YILDIZ_SAYISI = 60
YILDIZ_MIN_HIZ = 0.5
YILDIZ_MAX_HIZ = 4.0


def gorsel_yukle(dosya_adi, boyut=None):
    """Gorsel dosyasini yukle, bulunamazsa renkli yedek olustur."""
    try:
        yol = os.path.join("kod_ornekleri", "bolum05", "assets", dosya_adi)
        gorsel = pygame.image.load(yol).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        return gorsel
    except (pygame.error, FileNotFoundError):
        genislik = boyut[0] if boyut else 32
        yukseklik = boyut[1] if boyut else 32
        yuzey = pygame.Surface((genislik, yukseklik), pygame.SRCALPHA)
        pygame.draw.rect(yuzey, (100, 100, 255),
                         (0, 0, genislik, yukseklik), border_radius=3)
        return yuzey


# --- Sprite Siniflari ---
class Yildiz(pygame.sprite.Sprite):
    """Farkli boyut ve hizda kayan yildiz Sprite."""

    def __init__(self, baslangic_y=None):
        """Yildizi olustur.

        Args:
            baslangic_y: Baslangic y konumu. None ise rastgele.
        """
        super().__init__()

        # Rastgele boyut (1-3 piksel yaricap)
        self.boyut = random.randint(1, 3)

        # Boyuta gore parlaklik ayarla (buyuk = parlak)
        parlaklik = 100 + self.boyut * 50
        self.renk = (parlaklik, parlaklik, min(255, parlaklik + 20))

        # Gorsel olustur (kucuk daire)
        cap = self.boyut * 2
        self.image = pygame.Surface((cap, cap), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.renk,
                          (self.boyut, self.boyut), self.boyut)

        # Konum ayarla
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK)
        if baslangic_y is not None:
            self.rect.y = baslangic_y
        else:
            self.rect.y = random.randint(-YUKSEKLIK, YUKSEKLIK)

        # Hiz: buyuk yildizlar daha hizli (yakin gorunur)
        self.hiz = self.boyut * random.uniform(
            YILDIZ_MIN_HIZ, YILDIZ_MAX_HIZ / 3
        ) + YILDIZ_MIN_HIZ

    def update(self):
        """Yildizi asagi kaydir, ekran disindan tekrar sok."""
        self.rect.y += self.hiz

        # Ekranin altindan ciktiysa ustten tekrar gir
        if self.rect.top > YUKSEKLIK:
            self.rect.x = random.randint(0, GENISLIK)
            self.rect.bottom = 0
            # Her dongude hizi biraz degistir (dogallik)
            self.hiz = self.boyut * random.uniform(
                YILDIZ_MIN_HIZ, YILDIZ_MAX_HIZ / 3
            ) + YILDIZ_MIN_HIZ


class HareketliNesne(pygame.sprite.Sprite):
    """Ok tuslariyla kontrol edilen basit bir nesne."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Basit bir ucgen (gemi silhueti)
        noktalar = [(15, 0), (0, 30), (30, 30)]
        pygame.draw.polygon(self.image, (0, 200, 255), noktalar)
        pygame.draw.polygon(self.image, BEYAZ, noktalar, 2)
        self.rect = self.image.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK // 2)
        )
        self.hiz = 5

    def update(self):
        """Ok tuslariyla hareket et."""
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += self.hiz
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            self.rect.y -= self.hiz
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            self.rect.y += self.hiz

        # Ekran sinirlarinda tut
        self.rect.clamp_ip(pygame.Rect(0, 0, GENISLIK, YUKSEKLIK))


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # --- Gruplari olustur ---
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()

    # Yildizlari olustur
    for _ in range(YILDIZ_SAYISI):
        yildiz = Yildiz()
        tum_spritelar.add(yildiz)
        yildizlar.add(yildiz)

    # Hareketli nesneyi olustur (yildizlarin ustunde cizdirmek icin
    # yildizlardan sonra ekliyoruz)
    nesne = HareketliNesne()
    tum_spritelar.add(nesne)

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

        # --- Guncelleme ---
        tum_spritelar.update()

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        # Bilgi yazisi
        bilgi = f"Yildiz: {len(yildizlar)} | Toplam: {len(tum_spritelar)}"
        yazi = font.render(bilgi, True, ACIK_GRI)
        ekran.blit(yazi, (10, 10))

        kontrol = font.render("WASD/Ok tuslari: Hareket | ESC: Cikis",
                              True, SOLUK_BEYAZ)
        ekran.blit(kontrol, (10, YUKSEKLIK - 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
Koyu mavi arka plan uzerinde 60 adet yildiz farkli hizlarda
asagiya dogru kayar. Buyuk yildizlar daha parlak ve hizli,
kucuk yildizlar daha soluk ve yavas hareket eder (paralaks).
Ok tuslari veya WASD ile mavi ucgen nesne kontrol edilebilir.
Ekranin altindan cikan yildizlar ustten tekrar girer.
"""
