"""
Lab 05 - Calisma 4 Baslangic Kodu
Boyut Degistirme

Bu dosya Lab 05 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.transform.scale() ile boyut degistirme
- pygame.transform.smoothscale() ile kaliteli olcekleme
- En-boy orani koruma
- Dinamik boyutlandirma (fare tekerlegi)

Lab: 05 - Gorseller ve Sprite Temelleri
Calisma: 4 - Boyut Degistirme

Calistirma: uv run python calisma4.py
"""

# --- Lab foyundeki ornek kod ---

import pygame

pygame.init()
GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Boyut Degistirme")
saat = pygame.time.Clock()

# Yedek gorsel olustur (64x64 kare)
orijinal = pygame.Surface((64, 64), pygame.SRCALPHA)
pygame.draw.polygon(orijinal, (0, 150, 255),
                    [(32, 4), (4, 60), (60, 60)])

# Farkli boyutlarda kopyalar
kucuk = pygame.transform.scale(orijinal, (32, 32))
buyuk = pygame.transform.scale(orijinal, (128, 128))
smooth = pygame.transform.smoothscale(orijinal, (128, 128))

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    ekran.fill((20, 20, 40))

    ekran.blit(kucuk, (100, 250))
    ekran.blit(orijinal, (250, 220))
    ekran.blit(buyuk, (400, 190))
    ekran.blit(smooth, (600, 190))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 4.1 - Boyut Etiketleri ===
# TODO: a) Her gorselin altina boyutunu gosteren metin ekleyin
# TODO: b) pygame.font.SysFont("Arial", 16) ile yazi tipi
#          olusturun
# TODO: c) Ornegin kucuk gorselin altina "32x32" yazin
# ============================================


# === GOREV 4.2 - En-Boy Orani Koruma ===
# TODO: a) Asagidaki fonksiyonu programiniza ekleyin
# TODO: b) Dikdortgen bir gorsel (100x50) olusturup en-boy
#          oranini koruyarak genisligi 200'e olceklendirin
# TODO: c) Sonucu orani bozulmus bir versiyonla (200x200)
#          yan yana gosterin
# Ipucu kodu:
#
#   def boyut_oranli(surface, hedef_genislik):
#       oran = hedef_genislik / surface.get_width()
#       yeni_yuk = int(surface.get_height() * oran)
#       return pygame.transform.scale(
#           surface, (hedef_genislik, yeni_yuk))
# ============================================


# === GOREV 4.3 - Dinamik Boyutlandirma ===
# TODO: a) Fare tekerlegi ile (MOUSEWHEEL olayi) gorselin
#          boyutunu artirip azaltin
# TODO: b) olay.y yukari kaydirmada +1, asagida -1 doner
# TODO: c) Minimum 16, maksimum 256 piksel siniri koyun
# TODO: d) Her boyut degisikliginde ORIJINALDEN olcekleme yapin
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Soldan saga: kucuk (32x32), orijinal (64x64),
buyuk-scale (128x128) ve buyuk-smoothscale (128x128)
ucgen gorselleri gorulur.
"""
