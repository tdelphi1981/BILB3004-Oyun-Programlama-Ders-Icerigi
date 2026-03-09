"""
Lab 05 - Calisma 2 Baslangic Kodu
convert() ve convert_alpha() Karsilastirmasi

Bu dosya Lab 05 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- convert() ile format donusumu
- convert_alpha() ile alpha kanali koruma
- Performans olcumu (blit hizi)
- set_colorkey() ile seffaflik

Lab: 05 - Gorseller ve Sprite Temelleri
Calisma: 2 - convert() ve convert_alpha() Karsilastirmasi

Calistirma: uv run python calisma2.py
"""

# --- Lab foyundeki ornek kod ---

import os
import time
import pygame

pygame.init()
ekran = pygame.display.set_mode((800, 600))

DIZIN = os.path.dirname(os.path.abspath(__file__))
dosya = os.path.join(DIZIN, "assets", "images", "playerShip1_blue.png")

# 3 farkli yukleme yontemi
try:
    ham = pygame.image.load(dosya)           # Donusumsuz
    donusmus = pygame.image.load(dosya).convert()      # convert
    alpha = pygame.image.load(dosya).convert_alpha()   # convert_alpha
except FileNotFoundError:
    print("Gorsel bulunamadi, cikiliyor.")
    pygame.quit()
    exit()

# Performans testi
def blit_testi(gorsel, tekrar=10000):
    baslangic = time.time()
    for _ in range(tekrar):
        ekran.blit(gorsel, (0, 0))
    return (time.time() - baslangic) * 1000

print(f"Ham      : {blit_testi(ham):.2f} ms")
print(f"convert  : {blit_testi(donusmus):.2f} ms")
print(f"convert_a: {blit_testi(alpha):.2f} ms")

pygame.quit()


# === GOREV 2.1 - Performans Olcumu ===
# TODO: a) Kodu calistirin ve 3 yontemin suresini lab
#          foyundeki tabloya yazin
# TODO: b) Hangi yontemin en hizli oldugunu belirleyin
# ============================================


# === GOREV 2.2 - Gorsel Farki Gozlemleme ===
# TODO: a) Dama deseni arkaplan olusturun
# TODO: b) Hem convert() ile hem convert_alpha() ile
#          yuklenmisTR gorseli yan yana cizin
# TODO: c) Alpha kanalinin korunup korunmadigini gozlemleyin
# ============================================


# === GOREV 2.3 - set_colorkey() Deneyi ===
# TODO: a) convert() ile yuklenmisTR bir gorsele
#          set_colorkey((0, 0, 0)) uygula
# TODO: b) Siyah piksellerin seffaf olup olmadigini gozlemleyin
# TODO: c) Farkli renklerle (beyaz, kirmizi) deneyin
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
Terminalde 3 farkli yukleme yonteminin blit suresi yazdirilir.
convert() ve convert_alpha() ham yuklemeye gore cok daha hizlidir.
"""
