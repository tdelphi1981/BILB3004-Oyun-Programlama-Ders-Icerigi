"""
Lab 04 - Calisma 1 Baslangic Kodu
Event Gozlemcisi

Bu dosya Lab 04 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.event.get() ile olay okuma
- Olay turleri (KEYDOWN, MOUSEBUTTONDOWN, QUIT, vb.)
- Olay filtreleme
- pygame.key.name() ile tus adi alma

Lab: 04 - Kullanici Girdileri ve Hareket
Calisma: 1 - Event Gozlemcisi

Calistirma: uv run python calisma1.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Olay Gozlemci")
saat = pygame.time.Clock()

KOYU_GRI = (40, 40, 40)

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        else:
            # Tum olaylari konsola yazdir
            print(f"Olay: {olay}")

    ekran.fill(KOYU_GRI)
    pygame.display.flip()
    saat.tick(60)

pygame.quit()
sys.exit()


# === GOREV 1.1 - Olaylari Gozlemle ===
# TODO: a) Kodu calistirin, farkli tuslara basin ve fare
#          ile tiklayin
# TODO: b) Terminalde gozlemlenen olay turlerini lab
#          foyundeki tabloya yazin:
#          - Klavyeye basinca
#          - Klavyeyi birakinca
#          - Fare tiklayinca
#          - Fare hareket edince
#          - Pencere kapatilinca
# ============================================


# === GOREV 1.2 - Olay Filtresi ===
# TODO: a) Olay isleme blogunu duzenleyerek yalnizca
#          KEYDOWN ve MOUSEBUTTONDOWN olaylarini yazdirin,
#          digerlerini goz ardi edin
# Ipucu kodu:
#
#   if olay.type == pygame.KEYDOWN:
#       print(f"Basildi: {pygame.key.name(olay.key)}")
#   elif olay.type == pygame.MOUSEBUTTONDOWN:
#       print(f"Fare: dugme={olay.button}, konum={olay.pos}")
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu gri bir pencere acilir.
Herhangi bir tusa basildiginda veya fare hareket ettiginde
terminalde olay bilgisi yazdirilir.
"""
