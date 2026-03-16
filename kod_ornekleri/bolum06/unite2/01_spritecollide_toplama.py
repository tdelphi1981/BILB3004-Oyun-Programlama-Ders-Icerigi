"""
spritecollide ile Yildiz Toplama Oyunu

Ekranda rastgele konumlarda yildizlar belirir ve oyuncu
fare ile hareket ederek yildizlari toplar. spritecollide()
fonksiyonu ile carpisma kontrolu yapilir.

Ogrenilecek kavramlar:
- pygame.sprite.spritecollide() kullanimi
- dokill parametresinin etkisi
- Carpisan Sprite listesi ile calisma
- Basit skor sistemi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 2 - Sprite Carpisma Fonksiyonlari

Calistirma: python 01_spritecollide_toplama.py
Gereksinimler: pygame
"""

import pygame
import random
import sys


# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "spritecollide - Yildiz Toplama"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
SARI = (255, 220, 50)
ACIK_MAVI = (100, 180, 255)
KOYU_MAVI = (8, 8, 32)
GRI = (150, 150, 150)

# Oyun ayarlari
YILDIZ_SAYISI = 15
YILDIZ_BOYUT = 20
OYUNCU_BOYUT = 40


# --- Sprite Siniflari ---
class Oyuncu(pygame.sprite.Sprite):
    """Fare ile kontrol edilen oyuncu Sprite'i."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(
            (OYUNCU_BOYUT, OYUNCU_BOYUT), pygame.SRCALPHA
        )
        # Basit bir gemi sekli ciz
        pygame.draw.polygon(
            self.image, ACIK_MAVI,
            [(OYUNCU_BOYUT // 2, 0),
             (OYUNCU_BOYUT, OYUNCU_BOYUT),
             (0, OYUNCU_BOYUT)]
        )
        pygame.draw.polygon(
            self.image, BEYAZ,
            [(OYUNCU_BOYUT // 2, 0),
             (OYUNCU_BOYUT, OYUNCU_BOYUT),
             (0, OYUNCU_BOYUT)], 2
        )
        self.rect = self.image.get_rect(center=(GENISLIK // 2,
                                                 YUKSEKLIK // 2))

    def update(self):
        """Fare konumunu takip et."""
        self.rect.center = pygame.mouse.get_pos()
        # Ekran sinirlari icinde tut
        self.rect.clamp_ip(pygame.Rect(0, 0, GENISLIK, YUKSEKLIK))


class Yildiz(pygame.sprite.Sprite):
    """Toplanabilir yildiz Sprite'i."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(
            (YILDIZ_BOYUT, YILDIZ_BOYUT), pygame.SRCALPHA
        )
        # Sari daire ciz
        pygame.draw.circle(
            self.image, SARI,
            (YILDIZ_BOYUT // 2, YILDIZ_BOYUT // 2),
            YILDIZ_BOYUT // 2
        )
        # Parildama efekti
        pygame.draw.circle(
            self.image, BEYAZ,
            (YILDIZ_BOYUT // 2 - 2, YILDIZ_BOYUT // 2 - 2), 3
        )
        self.rect = self.image.get_rect()
        self.yeniden_konumlan()

    def yeniden_konumlan(self):
        """Rastgele bir konuma yerlestir."""
        self.rect.x = random.randint(20, GENISLIK - 20 - YILDIZ_BOYUT)
        self.rect.y = random.randint(20, YUKSEKLIK - 60 - YILDIZ_BOYUT)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # --- Sprite Gruplari ---
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()

    # Oyuncuyu olustur
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Yildizlari olustur
    for _ in range(YILDIZ_SAYISI):
        yildiz = Yildiz()
        tum_spritelar.add(yildiz)
        yildizlar.add(yildiz)

    # Skor
    skor = 0

    # Fare imlecini gizle
    pygame.mouse.set_visible(False)

    # --- Ana Oyun Dongusu ---
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

        # --- Carpisma kontrolu ---
        # spritecollide: oyuncu ile yildizlar arasinda
        # dokill=True: carpisan yildizlar otomatik silinir
        toplanan = pygame.sprite.spritecollide(
            oyuncu, yildizlar, True
        )

        # Toplanan yildizlar icin skor artir
        for yildiz in toplanan:
            skor += 10

        # Tum yildizlar toplandiysa yenilerini olustur
        if len(yildizlar) == 0:
            for _ in range(YILDIZ_SAYISI):
                yildiz = Yildiz()
                tum_spritelar.add(yildiz)
                yildizlar.add(yildiz)

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)

        # Sprite'lari ciz
        tum_spritelar.draw(ekran)

        # Skor yazisi
        skor_yazi = font.render(f"Skor: {skor}", True, BEYAZ)
        ekran.blit(skor_yazi, (15, 15))

        # Kalan yildiz sayisi
        kalan_yazi = font.render(
            f"Kalan: {len(yildizlar)}", True, GRI
        )
        ekran.blit(kalan_yazi, (15, 50))

        # Bilgi yazisi
        bilgi = font.render(
            "Fare ile yildizlari topla | ESC: Cikis", True, GRI
        )
        bilgi_rect = bilgi.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 10
        )
        ekran.blit(bilgi, bilgi_rect)

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
Koyu mavi arka plan uzerinde 15 adet sari yildiz
rastgele konumlarda belirir. Fare ile kontrol edilen
mavi ucgen seklinde bir gemi ile yildizlara dokunarak
onlari toplarsin. Her toplanan yildiz 10 puan kazandirir.
Tum yildizlar toplandiysa yeni bir set belirir.

Sol ust kosede skor ve kalan yildiz sayisi gosterilir.
ESC tusu ile oyundan cikabilirsin.
"""
