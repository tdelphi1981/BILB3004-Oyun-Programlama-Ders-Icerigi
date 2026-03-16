"""
Carpisma Demosu - Rect Carpisma Teknikleri

Hareket eden oyuncu kutusu, rastgele engeller ve fare ile
yeni engel ekleme. colliderect(), collidepoint() ve
collidelistall() kullanimi.

Ogrenilecek kavramlar:
- Rect hareket ve sinir kontrolu
- colliderect() ile carpisma algilama
- collidelistall() ile coklu carpisma
- Fare tiklama ile nesne olusturma

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 1 - Rect Sinifi ve Carpisma

Calistirma: python 03_carpisma_demo.py
Gereksinimler: pygame
"""

import pygame
import random

# Sabitler
EKRAN_GENISLIK = 800
EKRAN_YUKSEKLIK = 600
FPS = 60
OYUNCU_BOYUT = 40
OYUNCU_HIZ = 5
ENGEL_BOYUT = 50

# Renkler
BEYAZ = (255, 255, 255)
MAVI = (50, 100, 200)
KIRMIZI = (200, 50, 50)
YESIL = (50, 200, 50)
SARI = (200, 200, 50)
GRI = (40, 40, 40)
KOYU_GRI = (80, 80, 80)


def engel_olustur(adet):
    """Rastgele konumlarda engel Rect'leri olusturur."""
    engeller = []
    for _ in range(adet):
        x = random.randint(0, EKRAN_GENISLIK - ENGEL_BOYUT)
        y = random.randint(0, EKRAN_YUKSEKLIK - ENGEL_BOYUT)
        engeller.append(pygame.Rect(x, y, ENGEL_BOYUT, ENGEL_BOYUT))
    return engeller


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
    pygame.display.set_caption("Carpisma Demosu")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    # Oyuncu
    oyuncu = pygame.Rect(
        EKRAN_GENISLIK // 2 - OYUNCU_BOYUT // 2,
        EKRAN_YUKSEKLIK // 2 - OYUNCU_BOYUT // 2,
        OYUNCU_BOYUT, OYUNCU_BOYUT
    )

    # Baslangic engelleri
    engeller = engel_olustur(8)

    # Ekran sinir Rect'i (clamp_ip icin)
    ekran_rect = pygame.Rect(0, 0, EKRAN_GENISLIK, EKRAN_YUKSEKLIK)

    carpisma_sayisi = 0

    calistir = True
    while calistir:
        # -- Olaylari isle --
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            # Fare tiklamasiyla yeni engel ekle
            if olay.type == pygame.MOUSEBUTTONDOWN:
                fare_x, fare_y = olay.pos
                yeni_engel = pygame.Rect(
                    fare_x - ENGEL_BOYUT // 2,
                    fare_y - ENGEL_BOYUT // 2,
                    ENGEL_BOYUT, ENGEL_BOYUT
                )
                engeller.append(yeni_engel)

            # R tusu ile engelleri sifirla
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_r:
                    engeller = engel_olustur(8)
                    carpisma_sayisi = 0

        # -- Guncelle --
        # Klavye ile hareket
        tuslar = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if tuslar[pygame.K_LEFT]:
            dx = -OYUNCU_HIZ
        if tuslar[pygame.K_RIGHT]:
            dx = OYUNCU_HIZ
        if tuslar[pygame.K_UP]:
            dy = -OYUNCU_HIZ
        if tuslar[pygame.K_DOWN]:
            dy = OYUNCU_HIZ

        oyuncu.move_ip(dx, dy)

        # Ekran sinirlarinda tut
        oyuncu.clamp_ip(ekran_rect)

        # Carpisma kontrolu - tum carpisan engelleri bul
        carpisan_indeksler = oyuncu.collidelistall(engeller)
        carpisma_var = len(carpisan_indeksler) > 0
        if carpisma_var:
            carpisma_sayisi += 1

        # -- Ciz --
        ekran.fill(GRI)

        # Engelleri ciz
        for i, engel in enumerate(engeller):
            if i in carpisan_indeksler:
                # Carpisan engel sari yanip soner
                pygame.draw.rect(ekran, SARI, engel)
            else:
                pygame.draw.rect(ekran, KIRMIZI, engel)
            # Engel kenarligi
            pygame.draw.rect(ekran, KOYU_GRI, engel, 2)

        # Oyuncuyu ciz
        if carpisma_var:
            oyuncu_renk = YESIL
        else:
            oyuncu_renk = MAVI
        pygame.draw.rect(ekran, oyuncu_renk, oyuncu)
        pygame.draw.rect(ekran, BEYAZ, oyuncu, 2)

        # Bilgi metinleri
        bilgi1 = font.render(
            f"Engel sayisi: {len(engeller)}  |  "
            f"Carpisma: {carpisma_sayisi}",
            True, BEYAZ
        )
        ekran.blit(bilgi1, (10, 10))

        bilgi2 = font.render(
            "Ok tuslari: Hareket  |  Fare: Engel ekle  |  R: Sifirla",
            True, (150, 150, 150)
        )
        ekran.blit(bilgi2, (10, EKRAN_YUKSEKLIK - 30))

        if carpisma_var:
            uyari = font.render(
                f"CARPISMA! ({len(carpisan_indeksler)} engel)",
                True, SARI
            )
            uyari_rect = uyari.get_rect(
                centerx=EKRAN_GENISLIK // 2, top=50
            )
            ekran.blit(uyari, uyari_rect)

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda bir pencere acilir.
Mavi kare ok tuslariyla hareket eder.
Kirmizi engellere carptigi anda yesile doner ve
carpisan engeller sari renk alir.
Fare tiklamasiyla yeni kirmizi engeller eklenir.
R tusu ile tum engeller sifirlanir.
"""
