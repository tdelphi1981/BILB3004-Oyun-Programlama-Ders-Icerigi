"""
Lab 03 - Calisma 3 Baslangic Kodu
Game Loop ve Olay Isleme

Bu dosya Lab 03 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Game Loop'un 5 adimi
- pygame.event.get() ile olay isleme
- KEYDOWN olaylari
- pygame.time.Clock() ile FPS kontrolu
- Arka plan rengi degistirme

Lab: 03 - PyGame'e Giris ve Oyun Penceresi
Calisma: 3 - Game Loop ve Olay Isleme

Calistirma: uv run python calisma3.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
saat = pygame.time.Clock()
FPS = 60

KOYU_MAVI = (20, 40, 80)

calistir = True
while calistir:
    # 1. Olaylari isle
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_ESCAPE:
                calistir = False
            elif olay.key == pygame.K_SPACE:
                print("Bosluk tusuna basildi!")

    # 2. Guncelle (simdilik bos)

    # 3. Ciz
    ekran.fill(KOYU_MAVI)

    # 4. Ekrani guncelle
    pygame.display.flip()

    # 5. FPS kontrolu
    saat.tick(FPS)

pygame.quit()
sys.exit()


# === GOREV 3.1 - FPS'i Baslikta Goster ===
# TODO: a) saat.get_fps() fonksiyonuyla anlik FPS degerini
#          alin ve pencere basliginda gosterin
# TODO: b) FPS degerinin 60 civarinda oldugunu gozlemleyin
# TODO: c) FPS sabitini 30 ve 120 yaparak farki gorun
# Ipucu kodu (4. adimdan sonra ekleyin):
#
#   fps_deger = saat.get_fps()
#   pygame.display.set_caption(
#       f"Oyunum - FPS: {fps_deger:.1f}")
# ============================================


# === GOREV 3.2 - Tus Olaylari ===
# TODO: a) Asagidaki tuslar icin olay isleme ekleyin:
#          K_UP    -> Terminale "Yukari" yazdirsin
#          K_DOWN  -> Terminale "Asagi" yazdirsin
#          K_LEFT  -> Terminale "Sol" yazdirsin
#          K_RIGHT -> Terminale "Sag" yazdirsin
# ============================================


# === GOREV 3.3 - Arka Plan Rengi Degistirme ===
# TODO: a) Tuslara basarak arka plan rengini degistiren
#          bir sistem yapin:
#          K_1 -> Kirmizi (180, 40, 40)
#          K_2 -> Yesil (40, 180, 40)
#          K_3 -> Mavi (40, 40, 180)
# TODO: b) Arka plan rengini bir degiskende tutun ve tusa
#          basildiginda degistirin
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Space tusuna basinca terminalde "Bosluk tusuna basildi!" yazar.
ESC tusuna basinca veya pencere kapatilinca program sonlanir.
"""
