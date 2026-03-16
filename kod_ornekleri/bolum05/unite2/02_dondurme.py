"""
Dondurme Demo - rotate() ile gorsel dondurme

Bu program PyGame'in transform.rotate() fonksiyonunu gosterir.
Surekli donen bir nesne ve fareye dogru donen bir gemi ornegi
yer alir. Dogru dondurme yontemi (orijinal sakla, rect.center
koru) gosterilir.

Ogrenilecek kavramlar:
- pygame.transform.rotate() kullanimi
- Surekli dondurme (her karede aci artirma)
- Fareye dogru dondurme (math.atan2)
- rect.center koruma teknigi
- Yanlis dondurme (birikimli) ile dogru dondurme karsilastirmasi

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 2 - Gorsel Manipulasyonu

Calistirma: python 02_dondurme.py
Gereksinimler: pygame
"""

import pygame
import math

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Dondurme Demo"
ARKA_PLAN = (15, 15, 35)

# Renkler
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 80, 80)
YESIL = (80, 255, 80)
MAVI = (80, 150, 255)
SARI = (255, 220, 80)
GRI = (150, 150, 150)
KOYU_GRI = (60, 60, 60)


def gorsel_yukle(dosya_yolu, boyut=None):
    """Gorseli yukler, bulunamazsa renkli yedek yuzey olusturur.

    Args:
        dosya_yolu: Gorsel dosyasinin yolu.
        boyut: Istege bagli hedef boyut (genislik, yukseklik).

    Returns:
        Yuklenen veya olusturulan Surface nesnesi.
    """
    try:
        gorsel = pygame.image.load(dosya_yolu).convert_alpha()
    except (pygame.error, FileNotFoundError):
        # Yedek: yukari bakan bir uzay gemisi
        gorsel = pygame.Surface((64, 64), pygame.SRCALPHA)
        # Gemi govdesi (ucgen)
        pygame.draw.polygon(gorsel, MAVI,
                            [(32, 4), (8, 60), (56, 60)])
        # Kanat
        pygame.draw.polygon(gorsel, (60, 120, 220),
                            [(32, 16), (18, 48), (46, 48)])
        # Kokpit
        pygame.draw.circle(gorsel, (200, 220, 255), (32, 30), 6)

    if boyut:
        gorsel = pygame.transform.scale(gorsel, boyut)
    return gorsel


def goktas_olustur(boyut=48):
    """Basit bir goktas gorseli olusturur.

    Args:
        boyut: Goktas boyutu (piksel).

    Returns:
        Goktas Surface nesnesi.
    """
    yuzey = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
    merkez = boyut // 2
    yaricap = boyut // 2 - 4
    # Dis cember
    pygame.draw.circle(yuzey, (120, 100, 80), (merkez, merkez), yaricap)
    # Ic detay
    pygame.draw.circle(yuzey, (90, 75, 60), (merkez, merkez),
                       yaricap - 6)
    # Krater
    pygame.draw.circle(yuzey, (70, 55, 45),
                       (merkez + 5, merkez - 3), 4)
    pygame.draw.circle(yuzey, (70, 55, 45),
                       (merkez - 7, merkez + 5), 3)
    return yuzey


def metin_ciz(ekran, yazi_tipi, metin, x, y, renk=BEYAZ):
    """Ekrana ortalanmis metin cizer."""
    yuzey = yazi_tipi.render(metin, True, renk)
    rect = yuzey.get_rect(center=(x, y))
    ekran.blit(yuzey, rect)


def main():
    """Ana program fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Yazi tipleri
    baslik_font = pygame.font.SysFont("Arial", 22, bold=True)
    bilgi_font = pygame.font.SysFont("Arial", 14)

    # --- Surekli donen goktas ---
    goktas_orijinal = goktas_olustur(64)
    goktas_aci = 0.0
    goktas_konum = (200, 250)

    # --- Yanlis dondurme ornegi (birikimli) ---
    yanlis_gorsel = goktas_olustur(64)  # Bu her karede bozulacak
    yanlis_konum = (200, 480)

    # --- Fareye dogru donen gemi ---
    gemi_orijinal = gorsel_yukle("assets/images/gemi.png", (64, 64))
    gemi_konum = [550, 350]
    gemi_aci = 0.0

    print("=" * 50)
    print("  Dondurme Demo")
    print("  Fareyi hareket ettirerek gemiyi yonlendir.")
    print("  ESC ile cikis")
    print("=" * 50)

    calistir = True
    while calistir:
        # Olaylari isle
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        ekran.fill(ARKA_PLAN)

        # --- Sol bolum: Surekli donen goktas ---
        metin_ciz(ekran, baslik_font, "Dogru Dondurme",
                  200, 60, YESIL)
        metin_ciz(ekran, bilgi_font,
                  "Orijinalden dondur, center koru",
                  200, 85, GRI)

        # Surekli dondurme: Her karede aci artir, orijinalden dondur
        goktas_aci += 1.5  # Her karede 1.5 derece
        if goktas_aci >= 360:
            goktas_aci -= 360

        # [DOGRU] Orijinalden dondur
        donmus_goktas = pygame.transform.rotate(goktas_orijinal,
                                                 goktas_aci)
        goktas_rect = donmus_goktas.get_rect(center=goktas_konum)
        ekran.blit(donmus_goktas, goktas_rect)

        # Aci bilgisi
        metin_ciz(ekran, bilgi_font,
                  f"Aci: {goktas_aci:.0f} derece", 200, 330, GRI)
        metin_ciz(ekran, bilgi_font,
                  f"Boyut: {donmus_goktas.get_width()}x"
                  f"{donmus_goktas.get_height()}",
                  200, 350, GRI)

        # --- Sol alt: Yanlis dondurme ornegi ---
        metin_ciz(ekran, baslik_font, "Yanlis Dondurme",
                  200, 400, KIRMIZI)
        metin_ciz(ekran, bilgi_font,
                  "Birikimli dondurme -> kalite kaybi",
                  200, 425, GRI)

        # [YANLIS] Onceki sonucu dondur (birikmeli bozulma)
        yanlis_gorsel = pygame.transform.rotate(yanlis_gorsel, 1.5)
        yanlis_rect = yanlis_gorsel.get_rect(center=yanlis_konum)
        ekran.blit(yanlis_gorsel, yanlis_rect)

        metin_ciz(ekran, bilgi_font,
                  f"Boyut: {yanlis_gorsel.get_width()}x"
                  f"{yanlis_gorsel.get_height()}",
                  200, 545, KIRMIZI)

        # --- Sag bolum: Fareye dogru donen gemi ---
        ayirici_x = 400
        pygame.draw.line(ekran, KOYU_GRI, (ayirici_x, 20),
                         (ayirici_x, YUKSEKLIK - 20), 1)

        metin_ciz(ekran, baslik_font, "Fareye Dogru Donme",
                  600, 60, SARI)
        metin_ciz(ekran, bilgi_font,
                  "math.atan2() ile aci hesaplama",
                  600, 85, GRI)

        # Fare konumu
        fare_x, fare_y = pygame.mouse.get_pos()

        # Fareye dogru aciyi hesapla
        dx = fare_x - gemi_konum[0]
        dy = fare_y - gemi_konum[1]
        radyan = math.atan2(-dy, dx)
        # -90 duzeltmesi: gorsel yukari bakiyor, atan2 saga bakar
        gemi_aci = math.degrees(radyan) - 90

        # Orijinalden dondur, center koru
        donmus_gemi = pygame.transform.rotate(gemi_orijinal, gemi_aci)
        gemi_rect = donmus_gemi.get_rect(center=gemi_konum)
        ekran.blit(donmus_gemi, gemi_rect)

        # Fare isareti (kucuk hedef daire)
        pygame.draw.circle(ekran, KIRMIZI, (fare_x, fare_y), 6, 1)
        pygame.draw.line(ekran, KIRMIZI,
                         (fare_x - 8, fare_y), (fare_x + 8, fare_y), 1)
        pygame.draw.line(ekran, KIRMIZI,
                         (fare_x, fare_y - 8), (fare_x, fare_y + 8), 1)

        # Gemi ile fare arasi cizgi
        pygame.draw.line(ekran, KOYU_GRI,
                         gemi_konum, (fare_x, fare_y), 1)

        # Bilgi
        metin_ciz(ekran, bilgi_font,
                  f"Gemi aci: {gemi_aci:.1f} derece",
                  600, 550, GRI)
        metin_ciz(ekran, bilgi_font,
                  f"Fare: ({fare_x}, {fare_y})",
                  600, 570, GRI)

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda bir pencere acilir.
Sol ust: Surekli donen goktas (orijinalden dondurme - dogru yontem).
Sol alt: Birikimli dondurme ornegi (her karede bozularak buyur).
Sag: Fareye dogru donen uzay gemisi (math.atan2 ile aci hesaplama).
Fare hareket ettikce gemi fareye dogru doner.
ESC ile programdan cikilir.
"""
