"""
Temel Oyun Penceresi - PyGame ile ilk pencere

Bu program PyGame kullanarak temel bir oyun penceresi olusturur.
Pencere koyu mavi arka planla acilir ve kullanici kapatana kadar
calisir.

Ogrenilecek kavramlar:
- pygame.display.set_mode() ile pencere olusturma
- Surface nesnesi ile calisma
- fill() ile arka plan boyama
- flip() ile ekrani guncelleme

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 2 - Oyun Penceresi Olusturma

Calistirma: python 01_temel_pencere.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
BASLIK = "Ilk Oyun Penceresi"
ARKAPLAN_RENGI = (30, 30, 60)  # Koyu mavi

def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Oyun penceresini olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)

    # Ana oyun dongusu
    calistir = True
    while calistir:
        # Olaylari isle
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        # Ekrani arka plan rengiyle doldur
        ekran.fill(ARKAPLAN_RENGI)

        # Ekrani guncelle
        pygame.display.flip()

    # PyGame'i kapat
    pygame.quit()

if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Pencere basliginda "Ilk Oyun Penceresi" yazar.
Pencere kapatildiginda program duzgun sekilde sonlanir.
"""
