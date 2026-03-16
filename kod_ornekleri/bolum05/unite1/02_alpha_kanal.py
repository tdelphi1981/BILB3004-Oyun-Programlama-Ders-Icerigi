"""
Alpha Kanali - convert() vs convert_alpha() karsilastirmasi

Bu program, ayni gorseli convert() ve convert_alpha() ile yukler,
farkini gorsel olarak gosterir. Ayrica set_colorkey() kullanimi
ve basit bir performans olcumu icerir.

Ogrenilecek kavramlar:
- convert() ve convert_alpha() farki
- set_colorkey() ile sahte seffaflik
- Performans olcumu (time.time ile)
- Alpha kanalinin gorsel etkisi

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 1 - Gorsel Dosyalari

Calistirma: python 02_alpha_kanal.py
Gereksinimler: pygame
"""

import os
import time
import pygame

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Alpha Kanali Karsilastirmasi"

# Renkler
KOYU_MAVI = (10, 10, 40)
BEYAZ = (255, 255, 255)
KIRMIZI = (200, 50, 50)
YESIL = (50, 200, 50)
MAGENTA = (255, 0, 255)
DAMA_ACIK = (180, 180, 180)
DAMA_KOYU = (120, 120, 120)

# Dosya dizini
DOSYA_DIZINI = os.path.dirname(os.path.abspath(__file__))
GORSEL_DIZINI = os.path.join(DOSYA_DIZINI, "..", "..", "..",
                              "assets", "images")


def dama_arkaplan_olustur(genislik, yukseklik, kare_boyutu=16):
    """Seffafligi gormek icin dama deseni arkaplan olustur."""
    arkaplan = pygame.Surface((genislik, yukseklik))
    for y in range(0, yukseklik, kare_boyutu):
        for x in range(0, genislik, kare_boyutu):
            renk = DAMA_ACIK if (x // kare_boyutu + y // kare_boyutu) % 2 == 0 else DAMA_KOYU
            pygame.draw.rect(arkaplan, renk,
                             (x, y, kare_boyutu, kare_boyutu))
    return arkaplan


def test_gorseli_olustur(boyut=128):
    """Alpha kanalli test gorseli olustur (daire)."""
    surface = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
    # Yari saydam daire ciz
    merkez = boyut // 2
    pygame.draw.circle(surface, (100, 150, 255, 200),
                       (merkez, merkez), merkez - 4)
    # Ortasina opak bir yildiz simgesi
    pygame.draw.circle(surface, (255, 255, 100, 255),
                       (merkez, merkez), merkez // 3)
    return surface


def performans_testi(ekran, gorsel, tekrar=5000):
    """Blit isleminin suresini olc."""
    baslangic = time.time()
    for _ in range(tekrar):
        ekran.blit(gorsel, (0, 0))
    bitis = time.time()
    return (bitis - baslangic) * 1000  # milisaniye


def main():
    """Ana fonksiyon."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Dama deseni arkaplan
    dama = dama_arkaplan_olustur(GENISLIK, YUKSEKLIK)

    # Test gorseli olustur
    orijinal = test_gorseli_olustur(128)

    # 3 farkli donusum yontemi
    # 1. convert() - alpha kanali kaybolur
    gorsel_convert = orijinal.copy().convert()

    # 2. convert_alpha() - alpha kanali korunur
    gorsel_alpha = orijinal.copy().convert_alpha()

    # 3. convert() + set_colorkey() - sahte seffaflik
    gorsel_colorkey = pygame.Surface((128, 128))
    gorsel_colorkey.fill(MAGENTA)
    pygame.draw.circle(gorsel_colorkey, (100, 150, 255),
                       (64, 64), 60)
    pygame.draw.circle(gorsel_colorkey, (255, 255, 100),
                       (64, 64), 21)
    gorsel_colorkey = gorsel_colorkey.convert()
    gorsel_colorkey.set_colorkey(MAGENTA)

    # Performans olcumu
    print("Performans testi (5000 blit islemi):")
    print("-" * 40)

    sure_ham = performans_testi(ekran, orijinal)
    print(f"  Ham (donusumsuz) : {sure_ham:.2f} ms")

    sure_convert = performans_testi(ekran, gorsel_convert)
    print(f"  convert()        : {sure_convert:.2f} ms")

    sure_alpha = performans_testi(ekran, gorsel_alpha)
    print(f"  convert_alpha()  : {sure_alpha:.2f} ms")

    sure_colorkey = performans_testi(ekran, gorsel_colorkey)
    print(f"  set_colorkey()   : {sure_colorkey:.2f} ms")

    print("-" * 40)
    if sure_ham > 0:
        hizlanma = sure_ham / sure_alpha if sure_alpha > 0 else 0
        print(f"  Hizlanma orani   : {hizlanma:.1f}x")

    # Font
    font = pygame.font.Font(None, 24)
    font_baslik = pygame.font.Font(None, 32)

    # --- Ana oyun dongusu ---
    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Dama arkaplan (seffafligi gormek icin)
        ekran.blit(dama, (0, 0))

        # Baslik
        baslik = font_baslik.render(
            "convert() vs convert_alpha() Karsilastirmasi",
            True, BEYAZ
        )
        ekran.blit(baslik, (GENISLIK // 2
                             - baslik.get_width() // 2, 20))

        # --- Sol: convert() ---
        etiket1 = font.render("convert()", True, KIRMIZI)
        ekran.blit(etiket1, (100, 100))
        ekran.blit(gorsel_convert, (90, 140))
        aciklama1 = font.render("Alpha kayip!", True, KIRMIZI)
        ekran.blit(aciklama1, (85, 280))

        # --- Orta: convert_alpha() ---
        etiket2 = font.render("convert_alpha()", True, YESIL)
        ekran.blit(etiket2, (310, 100))
        ekran.blit(gorsel_alpha, (320, 140))
        aciklama2 = font.render("Alpha korunuyor", True, YESIL)
        ekran.blit(aciklama2, (310, 280))

        # --- Sag: set_colorkey() ---
        etiket3 = font.render("set_colorkey()", True, BEYAZ)
        ekran.blit(etiket3, (560, 100))
        ekran.blit(gorsel_colorkey, (560, 140))
        aciklama3 = font.render("Sahte seffaflik", True, BEYAZ)
        ekran.blit(aciklama3, (555, 280))

        # Performans sonuclari
        sonuc_y = 380
        perf_baslik = font.render("Performans (5000 blit):",
                                   True, BEYAZ)
        ekran.blit(perf_baslik, (50, sonuc_y))

        satirlar = [
            f"Ham: {sure_ham:.1f} ms",
            f"convert(): {sure_convert:.1f} ms",
            f"convert_alpha(): {sure_alpha:.1f} ms",
            f"set_colorkey(): {sure_colorkey:.1f} ms",
        ]
        for i, satir in enumerate(satirlar):
            yazi = font.render(satir, True, BEYAZ)
            ekran.blit(yazi, (70, sonuc_y + 30 + i * 25))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
Performans testi (5000 blit islemi):
----------------------------------------
  Ham (donusumsuz) : XX.XX ms
  convert()        : XX.XX ms
  convert_alpha()  : XX.XX ms
  set_colorkey()   : XX.XX ms
----------------------------------------
  Hizlanma orani   : X.Xx

Ekranda 3 gorsel gorunur:
- Sol: convert() ile - siyah arka plan (alpha kayip)
- Orta: convert_alpha() ile - dama deseni gorunur (alpha korunuyor)
- Sag: set_colorkey() ile - magenta pikart rengi kaldirildigi icin
  seffaf gorunur ama kenarlar duz kesilmistir (yari saydamlik yok)

ESC ile cikis.
"""
