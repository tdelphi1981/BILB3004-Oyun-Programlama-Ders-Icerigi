"""
Lab 05 - Calisma 5 Baslangic Kodu
Dondurme ve Cevirme

Bu dosya Lab 05 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.transform.rotate() ile dondurme
- pygame.transform.flip() ile cevirme
- Birikimli dondurme hatasi
- math.atan2() ile fareye dondurme
- Karakter yon degistirme

Lab: 05 - Gorseller ve Sprite Temelleri
Calisma: 5 - Dondurme ve Cevirme

Calistirma: uv run python calisma5.py
"""

# --- Lab foyundeki ornek kod ---

import pygame

pygame.init()
ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Dondurme Demo")
saat = pygame.time.Clock()

# Ucgen seklinde gorsel
orijinal = pygame.Surface((64, 64), pygame.SRCALPHA)
pygame.draw.polygon(orijinal, (255, 200, 0),
                    [(32, 4), (4, 60), (60, 60)])
aci = 0

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    aci += 2
    if aci >= 360:
        aci -= 360

    # Orijinalden dondur, center koru
    donmus = pygame.transform.rotate(orijinal, aci)
    rect = donmus.get_rect(center=(300, 200))

    ekran.fill((20, 20, 40))
    ekran.blit(donmus, rect)
    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 5.1 - Dondurme Hizi Kontrolu ===
# TODO: a) Yukari/asagi ok tuslariyla dondurme hizini
#          artirip azaltin
# TODO: b) hiz degiskeni olusturun (baslangic: 2)
# TODO: c) Hiz degerini ekranda gosterin
# ============================================


# === GOREV 5.2 - Fareye Dondurme ===
# TODO: a) math.atan2() kullanarak gorseli farenin konumuna
#          dogru dondurun
# TODO: b) Gemi ile fare arasina ince bir cizgi cizin
# TODO: c) Aciyi ekranda gosterin
# Ipucu kodu:
#
#   import math
#   dx = fare_x - nesne_x
#   dy = fare_y - nesne_y
#   aci = math.degrees(math.atan2(-dy, dx)) - 90
# ============================================


# === GOREV 5.3 - Karakter Yon Degistirme ===
# TODO: a) cevirme_demo.py dosyasi olusturun
# TODO: b) Saga bakan bir ucgen cizin
# TODO: c) pygame.transform.flip() ile sol yonlu versiyonunu
#          olusturun
# TODO: d) Ok tuslariyla hareket ederken yone gore dogru
#          gorseli gosterin
# TODO: e) Karakterin altina yari saydam bir yansimasi ekleyin
# Ipucu kodu:
#
#   yansima = pygame.transform.flip(gorsel, False, True)
#   yansima.set_alpha(80)
#   ekran.blit(yansima, (x, y + gorsel.get_height()))
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
600x400 piksel boyutunda koyu mavi bir pencere acilir.
Ekranin ortasinda sari bir ucgen surekli olarak
saat yonunun tersine doner.
"""
