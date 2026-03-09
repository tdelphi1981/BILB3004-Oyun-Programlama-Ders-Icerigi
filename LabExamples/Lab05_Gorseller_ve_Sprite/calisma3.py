"""
Lab 05 - Calisma 3 Baslangic Kodu
Katmanli Sahne Olusturma

Bu dosya Lab 05 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Birden fazla gorsel yonetimi
- Z-order (cizim sirasi kavrami)
- gorsel_yukle() fallback fonksiyonu
- Prosedural yildizli arkaplan olusturma

Lab: 05 - Gorseller ve Sprite Temelleri
Calisma: 3 - Katmanli Sahne Olusturma

Calistirma: uv run python calisma3.py
"""

# --- Lab foyundeki ornek kod ---

import os
import random
import pygame

pygame.init()
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
saat = pygame.time.Clock()

DIZIN = os.path.dirname(os.path.abspath(__file__))

def gorsel_yukle(ad, boyut=None):
    yol = os.path.join(DIZIN, "assets", "images", ad)
    try:
        g = pygame.image.load(yol).convert_alpha()
        if boyut:
            g = pygame.transform.scale(g, boyut)
        return g
    except (FileNotFoundError, pygame.error):
        yt = pygame.Surface(boyut or (64, 64), pygame.SRCALPHA)
        yt.fill((255, 0, 255, 180))
        return yt

# Yildizli arkaplan olustur
arkaplan = pygame.Surface((GENISLIK, YUKSEKLIK))
arkaplan.fill((5, 5, 25))
for _ in range(150):
    x = random.randint(0, GENISLIK)
    y = random.randint(0, YUKSEKLIK)
    arkaplan.set_at((x, y), (200, 200, 200))

# Gorseller
gemi = gorsel_yukle("playerShip1_blue.png", (64, 64))
dusman = gorsel_yukle("enemyRed1.png", (48, 48))

# 4 dusman konumu
dusmanlar = [(100 + i * 160, 100) for i in range(4)]

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    fare_x, fare_y = pygame.mouse.get_pos()

    # Z-ORDER: sira onemli!
    ekran.blit(arkaplan, (0, 0))       # 1. Arkaplan
    for dx, dy in dusmanlar:           # 2. Dusmanlar
        ekran.blit(dusman, (dx, dy))
    ekran.blit(gemi, (fare_x - 32, fare_y - 32))  # 3. Oyuncu

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 3.1 - Sahneyi Test Edin ===
# TODO: a) Kodu calistirin, fareyi hareket ettirerek oyuncu
#          gemisinin dusmanlarin uzerinden gectigini dogrulayin
# TODO: b) Cizim sirasini degistirerek (gemiyi dusmanlardan
#          once cizin) ne oldugunu gozlemleyin
# ============================================


# === GOREV 3.2 - Dusman Hareketi ===
# TODO: a) Dusman gemilerini yatay olarak saga dogru
#          hareket ettirin
# TODO: b) Ekranin sag kenarindan cikan dusmani soldan
#          tekrar sokun (wrap stratejisi)
# ============================================


# === GOREV 3.3 - UI Katmani Ekleyin ===
# TODO: a) Ekranin sol ust kosesine skor metni ekleyin
#          (pygame.font kullanin)
# TODO: b) Sag ust koseye FPS bilgisi ekleyin
# TODO: c) Bu yazilari tum gorsellerin USTUNDE cizdiginizden
#          emin olun (z-order)
# Ipucu kodu:
#
#   font = pygame.font.Font(None, 28)
#   skor_yazi = font.render("Skor: 0", True, (255, 255, 255))
#   ekran.blit(skor_yazi, (10, 10))
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda yildizli arkaplan gorulur.
4 dusman gemisi ust sirada, oyuncu gemisi ise fareyi
takip eder. Oyuncu gemisi her zaman dusmanlarin
ustunde cizilir.
"""
