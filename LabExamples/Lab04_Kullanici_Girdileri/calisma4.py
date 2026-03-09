"""
Lab 04 - Calisma 4 Baslangic Kodu
Sinir Kontrolu

Bu dosya Lab 04 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Clamp (kilitleme) stratejisi
- Bounce (sekme) stratejisi
- Wrap (sarmalama) stratejisi
- Delta time ile hareket
- Hiz bilesenleri (hiz_x, hiz_y)

Lab: 04 - Kullanici Girdileri ve Hareket
Calisma: 4 - Sinir Kontrolu

Calistirma: uv run python calisma4.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Sinir Kontrolu - Clamp")
saat = pygame.time.Clock()
FPS = 60

LACIVERT  = (15, 25, 60)
TURUNCU   = (255, 160, 20)

# Top ozellikleri
top_x  = 100.0
top_y  = 100.0
top_r  = 25       # yaricap
hiz_x  = 250.0    # piksel/saniye
hiz_y  = 180.0

calistir = True
while calistir:
    dt = saat.tick(FPS) / 1000.0

    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    # Hareketi guncelle
    top_x += hiz_x * dt
    top_y += hiz_y * dt

    # Clamp: sinir icerisinde tut
    top_x = max(top_r, min(top_x, GENISLIK - top_r))
    top_y = max(top_r, min(top_y, YUKSEKLIK - top_r))

    ekran.fill(LACIVERT)
    pygame.draw.circle(ekran, TURUNCU,
        (int(top_x), int(top_y)), top_r)
    pygame.display.flip()

pygame.quit()
sys.exit()


# === GOREV 4.1 - Bounce Stratejisi ===
# TODO: a) Clamp yerine Bounce (sekme) stratejisini
#          uygulayin
# TODO: b) Top duvara carptiginda ilgili hiz bilesenini
#          tersine cevirin
# Ipucu kodu:
#
#   if top_x - top_r < 0 or top_x + top_r > GENISLIK:
#       hiz_x = -hiz_x
#   if top_y - top_r < 0 or top_y + top_r > YUKSEKLIK:
#       hiz_y = -hiz_y
# ============================================


# === GOREV 4.2 - Wrap Stratejisi ===
# TODO: a) Wrap (sarmalama) stratejisini uygulayin
# TODO: b) Top sag kenardan cikinca sol kenardan, alt
#          kenardan cikinca ust kenardan tekrar girsin
# Ipucu kodu:
#
#   if top_x - top_r > GENISLIK:
#       top_x = -top_r
#   elif top_x + top_r < 0:
#       top_x = GENISLIK + top_r
#   if top_y - top_r > YUKSEKLIK:
#       top_y = -top_r
#   elif top_y + top_r < 0:
#       top_y = YUKSEKLIK + top_r
# ============================================


# === GOREV 4.3 - Uc Top, Uc Strateji ===
# TODO: a) Uc topu ayni anda farkli stratejilerle hareket
#          ettirin:
#          - Turuncu top: Clamp -- kenarda durur
#          - Mavi top: Bounce -- sekme yapar
#          - Yesil top: Wrap -- karsi kenardan girer
# TODO: b) Her top icin ayri x, y, hiz_x, hiz_y
#          degiskenleri tanimlayin
# ============================================


# BONUS: Mini Yilan Prototipi
# TODO: a) Ogrendiklerinizi birlestirerek yilan oyununun
#          basit bir prototipini yazin
# Kurallar:
#   - Izgara tabanli hareket (her adimda bir hucre ilerler)
#   - Ok tuslariyla yon degistirme (KEYDOWN ile)
#   - Kirmizi bir yem rastgele konumda belirir
#   - Yem yenince yilan bir hucre buyur
# Ipucu - Temel yapi:
#
#   HUCRE = 20          # piksel cinsinden hucre boyutu
#   COLS  = 800 // HUCRE
#   ROWS  = 600 // HUCRE
#
#   # Yilani liste olarak tut: [(sutun, satir), ...]
#   yilan = [(10, 10), (9, 10), (8, 10)]
#   yon   = (1, 0)      # (dx, dy): sag
#
#   # Her hareket adiminda:
#   yeni_bas = (yilan[0][0] + yon[0],
#               yilan[0][1] + yon[1])
#   yilan.insert(0, yeni_bas)  # Basa yeni konum ekle
#   # Yem yenmediyse kuyrugu kaldir:
#   yilan.pop()
#
# Ipucu - Hiz kontrolu:
#
#   ADIM_KAREDE = 10   # kac karede bir adim atilacagi
#   sayac = 0
#
#   # Dongu icinde:
#   sayac += 1
#   if sayac >= ADIM_KAREDE:
#       sayac = 0
#       # Yilani hareket ettir
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda lacivert bir pencere acilir.
Turuncu bir top saga-asagi hareket eder ve ekranin sag
alt kosesine ulastiginda durur (Clamp stratejisi).
"""
