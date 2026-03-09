"""
Lab 04 - Calisma 2 Baslangic Kodu
Klavye ile Hareket

Bu dosya Lab 04 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.key.get_pressed() ile surekli girdi
- KEYDOWN ile ayrik girdi
- Delta time (dt) ile kare hizindan bagimsiz hareket
- Hiz sabiti ve hareket hesaplama
- WASD klavye duzeni

Lab: 04 - Kullanici Girdileri ve Hareket
Calisma: 2 - Klavye ile Hareket

Calistirma: uv run python calisma2.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Klavye ile Hareket")
saat = pygame.time.Clock()
FPS = 60

LACIVERT = (20, 30, 70)
SARI     = (255, 220, 50)

# Kare ozellikleri
kare_x = GENISLIK // 2
kare_y = YUKSEKLIK // 2
kare_bov = 40
HIZ = 200  # piksel/saniye

calistir = True
while calistir:
    dt = saat.tick(FPS) / 1000.0  # saniye cinsinden delta time

    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_ESCAPE:
                calistir = False

    # Surekli girdi kontrolu (get_pressed)
    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_UP]:
        kare_y -= HIZ * dt
    if tuslar[pygame.K_DOWN]:
        kare_y += HIZ * dt
    if tuslar[pygame.K_LEFT]:
        kare_x -= HIZ * dt
    if tuslar[pygame.K_RIGHT]:
        kare_x += HIZ * dt

    ekran.fill(LACIVERT)
    pygame.draw.rect(ekran, SARI,
        (int(kare_x), int(kare_y), kare_bov, kare_bov))
    pygame.display.flip()

pygame.quit()
sys.exit()


# === GOREV 2.1 - Hiz Deneyi ===
# TODO: a) HIZ sabitini sirasiyla 100, 300 ve 500 olarak
#          degistirip programi calistirin
# TODO: b) Her hiz degerindeki davranis farkini gozlemleyin
#          ve lab foyundeki tabloya not edin
# ============================================


# === GOREV 2.2 - WASD Destegi ===
# TODO: a) Ok tuslarinin yani sira WASD klavye duzenini
#          de destekleyin:
#          K_w -> Yukari
#          K_a -> Sol
#          K_s -> Asagi
#          K_d -> Sag
# ============================================


# === GOREV 2.3 - Renk Degisimi ===
# TODO: a) Space tusuna basildiginda karenin rengi degissin
# TODO: b) KEYDOWN olayini kullanarak her basista farkli
#          bir renk secin
# Ipucu kodu:
#
#   renkler = [(255,220,50), (50,200,100), (50,150,255), (255,100,100)]
#   renk_indis = 0
#
#   # KEYDOWN olayinda:
#   if olay.key == pygame.K_SPACE:
#       renk_indis = (renk_indis + 1) % len(renkler)
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda lacivert bir pencere acilir.
Ortada 40x40 piksel boyutunda sari bir kare vardir.
Ok tuslariyla kare hareket ettirilebilir.
ESC tusuna basinca program sonlanir.
"""
