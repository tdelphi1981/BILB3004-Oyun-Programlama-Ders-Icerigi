"""
Lab 03 - Calisma 2 Baslangic Kodu
Oyun Penceresi Olusturma

Bu dosya Lab 03 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.display.set_mode() ile pencere olusturma
- Pencere boyutlari ve baslik
- RGB renk sistemi
- Koordinat sistemi (sol ust = 0,0)
- pygame.draw.rect() ile dikdortgen cizme

Lab: 03 - PyGame'e Giris ve Oyun Penceresi
Calisma: 2 - Oyun Penceresi Olusturma

Calistirma: uv run python calisma2.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import sys

pygame.init()

# Pencere boyutlari
GENISLIK = 640
YUKSEKLIK = 480

# Pencere olustur
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Ilk PyGame Penceresi")

# Renkler (RGB)
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)

# Basit dongu - pencereyi acik tut
calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    ekran.fill(BEYAZ)
    pygame.display.flip()

pygame.quit()
sys.exit()


# === GOREV 2.1 - Farkli Boyutlar ===
# TODO: a) Pencere boyutunu 800x600 olarak degistirin,
#          calistirip gozlemleyin
# TODO: b) Pencere boyutunu 1024x768 olarak degistirin,
#          calistirip gozlemleyin
# ============================================


# === GOREV 2.2 - Koordinatlari Anla ===
# TODO: a) Pencerenin dort kosesine 10x10 piksel boyutunda
#          kucuk kareler cizin
# TODO: b) pygame.draw.rect() fonksiyonunu kullanin
# Ipucu kodlari (ekran.fill(BEYAZ) satirindan sonra ekleyin):
#
#   KIRMIZI = (255, 0, 0)
#   # Sol ust kose
#   pygame.draw.rect(ekran, KIRMIZI, (0, 0, 10, 10))
#   # Sag ust kose
#   pygame.draw.rect(ekran, KIRMIZI, (GENISLIK - 10, 0, 10, 10))
#   # Sol alt kose
#   pygame.draw.rect(ekran, KIRMIZI, (0, YUKSEKLIK - 10, 10, 10))
#   # Sag alt kose
#   pygame.draw.rect(ekran, KIRMIZI,
#       (GENISLIK - 10, YUKSEKLIK - 10, 10, 10))
# ============================================


# === GOREV 2.3 - Pencere Basligi ===
# TODO: a) Pencere basligina adinizi ve pencere boyutunu
#          ekleyin
# TODO: b) f-string kullanarak boyut degerlerini
#          degiskenlerden alin
# Ornek: "Ali - 800x600"
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
640x480 piksel boyutunda beyaz bir pencere acilir.
Pencere basliginda "Ilk PyGame Penceresi" yazar.
Pencere kapatildiginda program duzgun sekilde sonlanir.
"""
