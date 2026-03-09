"""
Lab 03 - Calisma 4 Baslangic Kodu
Sekil Cizimi

Bu dosya Lab 03 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.draw.rect() - Dikdortgen
- pygame.draw.circle() - Daire
- pygame.draw.line() - Cizgi
- pygame.draw.ellipse() - Elips
- pygame.draw.polygon() - Cokgen
- RGB renk sistemi
- Cizim sirasi (z-order)

Lab: 03 - PyGame'e Giris ve Oyun Penceresi
Calisma: 4 - Sekil Cizimi

Calistirma: uv run python calisma4.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Sekil Cizimi")
saat = pygame.time.Clock()

# Renkler
BEYAZ   = (255, 255, 255)
KIRMIZI = (220, 50, 50)
YESIL   = (50, 180, 50)
MAVI    = (50, 100, 220)
SARI    = (240, 220, 50)
TURUNCU = (240, 150, 30)

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    ekran.fill(BEYAZ)

    # Dikdortgen: (ekran, renk, (x, y, gen, yuk))
    pygame.draw.rect(ekran, KIRMIZI,
        (50, 50, 200, 100))

    # Daire: (ekran, renk, (mx, my), yaricap)
    pygame.draw.circle(ekran, MAVI, (400, 300), 80)

    # Cizgi: (ekran, renk, (x1,y1), (x2,y2), w)
    pygame.draw.line(ekran, YESIL,
        (100, 400), (700, 400), 3)

    # Elips: (ekran, renk, (x, y, gen, yuk))
    pygame.draw.ellipse(ekran, TURUNCU,
        (500, 100, 200, 100))

    # Cokgen: (ekran, renk, [noktalar])
    pygame.draw.polygon(ekran, SARI,
        [(400, 450), (350, 550), (450, 550)])

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
sys.exit()


# === GOREV 4.1 - Renk Denemeleri ===
# TODO: a) Asagidaki RGB degerlerini deneyerek farkli
#          renkler olusturun ve ekrana cizin:
#          - Mor: (128, 0, 128)
#          - Turkuaz: (0, 200, 200)
#          - Pembe: (255, 105, 180)
# TODO: b) Her renkle bir dikdortgen, bir daire ve bir
#          cizgi cizin
# ============================================


# === GOREV 4.2 - Basit Sahne ===
# TODO: a) Sekil cizim fonksiyonlarini kullanarak basit bir
#          manzara sahnesi olusturun:
#          - Gokyuzu: Acik mavi arka plan (135, 206, 235)
#          - Gunes: Sag ust kosede sari daire
#          - Zemin: Alt kisimda yesil dikdortgen (cim)
#          - Ev: Kirmizi dikdortgen (duvar) +
#                kahverengi ucgen (cati)
#          - Agac: Kahverengi dikdortgen (govde) +
#                  yesil daire (yaprak)
# TODO: b) Cizim sirasi onemlidir! Once arkaplan, sonra
#          arkadaki nesneler, en son ondeki nesneleri cizin
# ============================================


# === GOREV 4.3 - Kendi Sahneniz ===
# TODO: a) Kendi hayal gucunuzu kullanarak farkli bir sahne
#          tasarlayin. Ornek fikirler:
#          - Gece gokyuzu (siyah arka plan, beyaz daireler
#            -> yildizlar)
#          - Deniz manzarasi (mavi tonlari, sari kum)
#          - Basit bir yuz ifadesi (daire + gozler + agiz)
# TODO: b) En az 5 farkli sekil cizim fonksiyonu kullanin
# ============================================


# BONUS: Animasyonlu Sahne
# TODO: a) Sahnenize animasyon ekleyin
# 1. Gunes Hareketi: Gunesi her karede yavaca hareket ettirin
# Ipucu kodu:
#
#   gunes_x = 700
#   gunes_y = 80
#
#   # Dongu icinde:
#   gunes_x -= 1  # Her karede 1 piksel sola
#   if gunes_x < -50:
#       gunes_x = GENISLIK + 50  # Tekrar baslat
#
#   pygame.draw.circle(ekran, SARI,
#       (gunes_x, gunes_y), 40)
#
# 2. Renk Degisimi: Gokyuzu rengini gunesin konumuna gore
#    degistirin (gun batimi efekti)
# Ipucu kodu:
#
#   oran = gunes_x / GENISLIK  # 0.0 - 1.0
#   r = int(135 + (220 - 135) * (1 - oran))
#   g = int(206 - (206 - 100) * (1 - oran))
#   b = int(235 - (235 - 80) * (1 - oran))
#   gokyuzu_renk = (r, g, b)
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda beyaz arka planli bir pencere acilir.
Pencerede kirmizi dikdortgen, mavi daire, yesil cizgi,
turuncu elips ve sari ucgen gorulur.
"""
