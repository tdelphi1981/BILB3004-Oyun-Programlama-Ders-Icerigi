"""
Lab 04 - Calisma 3 Baslangic Kodu
Fare ile Etkilesim

Bu dosya Lab 04 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.MOUSEBUTTONDOWN olayi
- olay.button ile fare dugmesi kontrolu
- olay.pos ile tiklama konumu
- pygame.mouse.get_pos() ile fare takibi
- Liste ile nesne yonetimi

Lab: 04 - Kullanici Girdileri ve Hareket
Calisma: 3 - Fare ile Etkilesim

Calistirma: uv run python calisma3.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Fare ile Etkilesim")
saat = pygame.time.Clock()

KOYU_MAVI = (15, 25, 60)
MAVI      = (50, 120, 255)

daireler = []  # (x, y) pozisyonlarini tut

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.MOUSEBUTTONDOWN:
            if olay.button == 1:  # Sol tikla
                daireler.append(olay.pos)

    ekran.fill(KOYU_MAVI)

    for konum in daireler:
        pygame.draw.circle(ekran, MAVI, konum, 20)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
sys.exit()


# === GOREV 3.1 - Tiklama Rengi ===
# TODO: a) Sol tiklama mavi (50, 120, 255), sag tiklama
#          kirmizi (220, 60, 60) daire olustursun
# TODO: b) Listeye renk bilgisini de ekleyin
# TODO: c) Sag tiklama icin olay.button == 3 kosulunu
#          kullanin
# Ipucu kodu:
#
#   # (x, y, renk) uclusu olarak sakla
#   daireler.append((olay.pos[0], olay.pos[1], MAVI))
# ============================================


# === GOREV 3.2 - Fareyi Takip Eden Nesne ===
# TODO: a) pygame.mouse.get_pos() ile fare konumunu her
#          karede okuyun
# TODO: b) Fareyi takip eden kucuk bir daire cizin
# Ipucu kodu:
#
#   # Guncelleme ve cizim bolumunde:
#   fare_x, fare_y = pygame.mouse.get_pos()
#   pygame.draw.circle(ekran, (255, 255, 100),
#       (fare_x, fare_y), 12)
# ============================================


# === GOREV 3.3 - Daireleri Temizle ===
# TODO: a) K_c tusuna basildiginda tum daireler silinsin
# TODO: b) KEYDOWN olayinda listeyi bosaltin
# Ipucu kodu:
#
#   if olay.type == pygame.KEYDOWN:
#       if olay.key == pygame.K_c:
#           daireler.clear()
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Sol fare dugmesiyle tiklandiginda tiklanan yerde mavi
bir daire olusturulur.
"""
