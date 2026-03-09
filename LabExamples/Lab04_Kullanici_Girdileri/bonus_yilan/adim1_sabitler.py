"""
Yilan Oyunu - Adim 1: Temel Yapi ve Sabitler

Izgara tabanli oyun penceresi olusturur.
Henuz yilan veya hareket yok, sadece bos bir
izgara goruntusu.

Ogrenilecek kavramlar:
- Izgara sabitleri tanimlama
- Renk sabitleri
- Bos oyun penceresi ve ana dongu
- Izgarayi cizme

Bolum: 04 - Kullanici Girdileri ve Hareket
Lab: 04 - Bonus: Yilan Oyunu (Adim 1/6)

Calistirma: uv run python adim1_sabitler.py
Gereksinimler: pygame
"""

import pygame
import random

# --- Sabitler ---
HUCRE_BOYUTU = 20
IZGARA_GENISLIK = 30    # 30 hucre yatay
IZGARA_YUKSEKLIK = 20   # 20 hucre dikey
GENISLIK = IZGARA_GENISLIK * HUCRE_BOYUTU    # 600 piksel
YUKSEKLIK = IZGARA_YUKSEKLIK * HUCRE_BOYUTU  # 400 piksel
FPS = 10  # Yilan hizi (kare/saniye)

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
YESIL = (0, 200, 0)
KOYU_YESIL = (0, 140, 0)
KIRMIZI = (220, 50, 50)
GRI = (40, 40, 40)
KOYU_GRI = (25, 25, 25)


def izgara_ciz(ekran):
    """Arka plana hafif izgara cizgileri ciz."""
    for x in range(0, GENISLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, KOYU_GRI, (x, 0), (x, YUKSEKLIK))
    for y in range(0, YUKSEKLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, KOYU_GRI, (0, y), (GENISLIK, y))


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Yilan Oyunu - Adim 1")
    saat = pygame.time.Clock()

    calistir = True
    while calistir:
        saat.tick(FPS)

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Ciz
        ekran.fill(SIYAH)
        izgara_ciz(ekran)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
600x400 piksel boyutunda siyah bir pencere acilir.
Arka planda hafif gri izgara cizgileri gorulur.
ESC ile program kapanir.
"""
