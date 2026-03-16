"""
Olay Islemeli Oyun Dongusu - Temel olay yakalama ornegi

Bu program, PyGame'in olay sistemini gosterir. Pencere acilir,
olay kuyrugu her turda okunur ve QUIT olayi yakalandiginda
program duzgun sekilde kapanir. Konsola olay bilgileri yazdirilir.

Ogrenilecek kavramlar:
- pygame.event.get() ile olay kuyrugunu okuma
- pygame.QUIT olayi ile pencere kapatma
- while bayragi ile dongu kontrolu

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 3 - Ana Oyun Dongusu (Game Loop)

Calistirma: python 01_olay_dongusu.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 600
YUKSEKLIK = 400
BASLIK = "Olay Islemeli Oyun Dongusu"
ARKA_PLAN = (15, 15, 45)  # Koyu mavi


def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)

    print("Oyun baslatildi!")
    print("Pencereyi kapatmak icin X dugmesine basin.")
    print("-" * 40)

    # Ana oyun dongusu
    calistir = True
    sayac = 0

    while calistir:
        # ASAMA 1: Olaylari isle
        for olay in pygame.event.get():
            # Olay turunu konsola yazdir
            if olay.type == pygame.QUIT:
                print(f"\n[QUIT] Pencere kapatma istegi alindi.")
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                print(f"[KEYDOWN] Tusa basildi: {pygame.key.name(olay.key)}")
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                print(f"[MOUSEBUTTONDOWN] Fare tiklandi: konum={olay.pos}")

        # ASAMA 2: Guncelle
        sayac += 1

        # ASAMA 3: Ciz
        ekran.fill(ARKA_PLAN)
        pygame.display.flip()

    # PyGame'i kapat
    pygame.quit()
    print(f"\nOyun sonlandi. Toplam kare sayisi: {sayac}")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
Oyun baslatildi!
Pencereyi kapatmak icin X dugmesine basin.
----------------------------------------
[KEYDOWN] Tusa basildi: space
[MOUSEBUTTONDOWN] Fare tiklandi: konum=(312, 198)
[KEYDOWN] Tusa basildi: a

[QUIT] Pencere kapatma istegi alindi.

Oyun sonlandi. Toplam kare sayisi: 4523
"""
