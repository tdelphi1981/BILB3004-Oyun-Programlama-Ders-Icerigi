"""
Boyut Degistirme Demo - scale() ve smoothscale() karsilastirmasi

Bu program PyGame'in transform.scale() ve transform.smoothscale()
fonksiyonlarini gosterir. Ayni gorsel uc farkli boyutta yan yana
gosterilir. Aspect ratio koruma ornegi de yer alir.

Ogrenilecek kavramlar:
- pygame.transform.scale() ile boyut degistirme
- pygame.transform.smoothscale() ile kaliteli boyut degistirme
- Aspect ratio (en-boy orani) koruma
- Orijinal gorseli saklama onemi

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 2 - Gorsel Manipulasyonu

Calistirma: python 01_boyut_degistirme.py
Gereksinimler: pygame
"""

import pygame
import os

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Boyut Degistirme Demo"
ARKA_PLAN = (20, 20, 40)

# Renkler
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 80, 80)
YESIL = (80, 255, 80)
MAVI = (80, 150, 255)
GRI = (150, 150, 150)
KOYU_GRI = (80, 80, 80)


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
        # Yedek: renkli bir uzay gemisi sekli olustur
        gorsel = pygame.Surface((128, 128), pygame.SRCALPHA)
        # Gemi govdesi
        pygame.draw.polygon(gorsel, MAVI,
                            [(64, 8), (20, 120), (108, 120)])
        # Kanat detaylari
        pygame.draw.polygon(gorsel, (60, 120, 220),
                            [(64, 30), (40, 100), (88, 100)])
        # Kokpit
        pygame.draw.circle(gorsel, (200, 220, 255), (64, 60), 12)

    if boyut:
        gorsel = pygame.transform.scale(gorsel, boyut)
    return gorsel


def boyut_oranli(surface, hedef_genislik):
    """Gorseli en-boy oranini koruyarak olceklendirir.

    Args:
        surface: Olceklendirilecek Surface.
        hedef_genislik: Istenen genislik (piksel).

    Returns:
        Oranli olceklenmis yeni Surface.
    """
    orijinal_gen = surface.get_width()
    orijinal_yuk = surface.get_height()
    oran = hedef_genislik / orijinal_gen
    yeni_yukseklik = int(orijinal_yuk * oran)
    return pygame.transform.scale(surface, (hedef_genislik, yeni_yukseklik))


def metin_ciz(ekran, yazi_tipi, metin, x, y, renk=BEYAZ):
    """Ekrana ortalanmis metin cizer.

    Args:
        ekran: Hedef Surface.
        yazi_tipi: pygame.font.Font nesnesi.
        metin: Gosterilecek metin.
        x: Merkez x koordinati.
        y: Merkez y koordinati.
        renk: Metin rengi.
    """
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
    baslik_font = pygame.font.SysFont("Arial", 24, bold=True)
    bilgi_font = pygame.font.SysFont("Arial", 16)

    # Orijinal gorseli yukle (128x128)
    orijinal = gorsel_yukle("assets/images/gemi.png")
    orijinal_boyut = (orijinal.get_width(), orijinal.get_height())

    # Farkli boyutlarda kopyalar olustur (orijinalden!)
    kucuk = pygame.transform.scale(orijinal, (48, 48))
    orta = pygame.transform.scale(orijinal, (96, 96))
    buyuk = pygame.transform.scale(orijinal, (192, 192))

    # smoothscale ile ayni boyutlar
    kucuk_smooth = pygame.transform.smoothscale(orijinal, (48, 48))
    orta_smooth = pygame.transform.smoothscale(orijinal, (96, 96))
    buyuk_smooth = pygame.transform.smoothscale(orijinal, (192, 192))

    # Oranli olceklendirme ornegi
    oranli = boyut_oranli(orijinal, 200)

    print("=" * 50)
    print("  Boyut Degistirme Demo")
    print(f"  Orijinal boyut: {orijinal_boyut[0]}x{orijinal_boyut[1]}")
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

        # --- Ust bolum: scale() ornekleri ---
        metin_ciz(ekran, baslik_font, "scale() - Standart", 200, 30, MAVI)

        # Kucuk
        kucuk_rect = kucuk.get_rect(center=(100, 130))
        ekran.blit(kucuk, kucuk_rect)
        metin_ciz(ekran, bilgi_font, "48x48", 100, 180, GRI)

        # Orta
        orta_rect = orta.get_rect(center=(220, 130))
        ekran.blit(orta, orta_rect)
        metin_ciz(ekran, bilgi_font, "96x96", 220, 200, GRI)

        # Buyuk
        buyuk_rect = buyuk.get_rect(center=(380, 150))
        ekran.blit(buyuk, buyuk_rect)
        metin_ciz(ekran, bilgi_font, "192x192", 380, 265, GRI)

        # --- Ust bolum: smoothscale() ornekleri ---
        metin_ciz(ekran, baslik_font, "smoothscale() - Kaliteli",
                  620, 30, YESIL)

        # Kucuk smooth
        kucuk_s_rect = kucuk_smooth.get_rect(center=(530, 130))
        ekran.blit(kucuk_smooth, kucuk_s_rect)
        metin_ciz(ekran, bilgi_font, "48x48", 530, 180, GRI)

        # Orta smooth
        orta_s_rect = orta_smooth.get_rect(center=(640, 130))
        ekran.blit(orta_smooth, orta_s_rect)
        metin_ciz(ekran, bilgi_font, "96x96", 640, 200, GRI)

        # Buyuk smooth
        buyuk_s_rect = buyuk_smooth.get_rect(center=(770, 150))
        ekran.blit(buyuk_smooth, buyuk_s_rect)
        metin_ciz(ekran, bilgi_font, "192x192", 770, 265, GRI)

        # --- Alt bolum: Oranli olceklendirme ---
        ayirici_y = 310
        pygame.draw.line(ekran, KOYU_GRI, (20, ayirici_y),
                         (GENISLIK - 20, ayirici_y), 1)

        metin_ciz(ekran, baslik_font, "En-Boy Orani Koruma",
                  GENISLIK // 2, 340, KIRMIZI)

        # Orijinal
        orj_rect = orijinal.get_rect(center=(200, 450))
        ekran.blit(orijinal, orj_rect)
        metin_ciz(ekran, bilgi_font,
                  f"Orijinal: {orijinal_boyut[0]}x{orijinal_boyut[1]}",
                  200, 530, GRI)

        # Oranli
        oranli_rect = oranli.get_rect(center=(500, 450))
        ekran.blit(oranli, oranli_rect)
        metin_ciz(ekran, bilgi_font,
                  f"Oranli: {oranli.get_width()}x{oranli.get_height()}",
                  500, 530, GRI)

        # Bozuk (orani korunmamis)
        bozuk = pygame.transform.scale(orijinal, (200, 80))
        bozuk_rect = bozuk.get_rect(center=(730, 450))
        ekran.blit(bozuk, bozuk_rect)
        metin_ciz(ekran, bilgi_font, "Bozuk: 200x80", 730, 530, KIRMIZI)

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda bir pencere acilir.
Ust kisimda scale() ve smoothscale() ile olceklenmis
gemi gorselleri yan yana gosterilir (48x48, 96x96, 192x192).
Alt kisimda en-boy orani korunan ve bozulan ornekler gosterilir.
ESC ile programdan cikilir.
"""
