"""
Lab 05 - Calisma 1 Baslangic Kodu
Gorsel Yukleme ve Gosterme

Bu dosya Lab 05 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.image.load() ile gorsel yukleme
- convert_alpha() ile performansli yukleme
- FileNotFoundError yonetimi (fallback/placeholder)
- Z-order (cizim sirasi)

Lab: 05 - Gorseller ve Sprite Temelleri
Calisma: 1 - Gorsel Yukleme ve Gosterme

Calistirma: uv run python calisma1.py
"""

# --- Lab foyundeki ornek kod ---

import os
import pygame

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Gorsel Yukleme Testi")
saat = pygame.time.Clock()

# Dosya dizini
DIZIN = os.path.dirname(os.path.abspath(__file__))
GORSEL = os.path.join(DIZIN, "assets", "images")

# Gorsel yukle
dosya_yolu = os.path.join(GORSEL, "playerShip1_blue.png")
try:
    gemi = pygame.image.load(dosya_yolu).convert_alpha()
    print("[OK] Gorsel yuklendi")
except FileNotFoundError:
    print("[UYARI] Dosya bulunamadi, placeholder olusturuluyor")
    gemi = pygame.Surface((64, 64), pygame.SRCALPHA)
    gemi.fill((255, 0, 255, 180))

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    ekran.fill((10, 10, 40))
    ekran.blit(gemi, (GENISLIK // 2 - 32, YUKSEKLIK // 2 - 32))
    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 1.1 - Kendi Gorselinizi Yukleyin ===
# TODO: a) Farkli bir gorsel dosyasi (PNG veya JPG) yukleyin
# TODO: b) Ekranin sol ust kosesine (50, 50) konumuna cizin
# TODO: c) Terminaldeki [OK] mesajini gozlemleyin
# ============================================


# === GOREV 1.2 - Birden Fazla Gorsel ===
# TODO: a) En az 3 farkli gorsel yukleyin (gemi, dusman, arkaplan)
# TODO: b) Her birini ekranin farkli konumlarina cizin
# TODO: c) Cizim sirasini degistirerek z-order etkisini
#          gozlemleyin
# ============================================


# === GOREV 1.3 - gorsel_yukle() Fonksiyonu ===
# TODO: a) Var olmayan bir dosya adi vererek FileNotFoundError
#          hatasini test edin
# TODO: b) Asagidaki fonksiyonu tamamlayin: dosya bulunamazsa
#          magenta renkli ve capraz cizgili bir placeholder
#          dondursun
# Ipucu kodu:
#
#   def gorsel_yukle(yol, boyut=None):
#       try:
#           g = pygame.image.load(yol).convert_alpha()
#           if boyut:
#               g = pygame.transform.scale(g, boyut)
#           return g
#       except (FileNotFoundError, pygame.error):
#           b = boyut or (64, 64)
#           s = pygame.Surface(b, pygame.SRCALPHA)
#           s.fill((255, 0, 255, 180))
#           return s
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Ekranin ortasinda bir uzay gemisi gorseli (veya magenta
placeholder) gorunur.
"""
