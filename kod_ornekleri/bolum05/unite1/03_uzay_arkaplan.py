"""
Uzay Arkaplan - Birden fazla gorsel katmanlama (z-order) demo

Bu program, arka plan gorseli uzerine uzay gemisi ve dusman
gemileri yerlestirir. Oyuncu gemisi fareyle hareket eder.
Katman sirasi (z-order) kavrami pratikte gosterilir.

Ogrenilecek kavramlar:
- Birden fazla gorsel katmanlama
- Z-order (cizim sirasi) kavrami
- Arka plan gorseli yerlestirme
- Fare ile gemi hareketi
- gorsel_yukle() fallback fonksiyonu

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 1 - Gorsel Dosyalari

Calistirma: python 03_uzay_arkaplan.py
Gereksinimler: pygame
"""

import os
import math
import random
import pygame

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Sahnesi - Z-Order Demo"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
SARI = (255, 255, 100)
MAGENTA = (255, 0, 255)
KOYU_MAVI = (5, 5, 25)

# Dosya dizini
DOSYA_DIZINI = os.path.dirname(os.path.abspath(__file__))
GORSEL_DIZINI = os.path.join(DOSYA_DIZINI, "..", "..", "..",
                              "assets", "images")


def gorsel_yukle(dosya_adi, boyut=None):
    """Gorseli yukle, bulunamazsa placeholder olustur.

    Args:
        dosya_adi: Yuklenecek gorsel dosyasinin adi
        boyut: (genislik, yukseklik) tuple veya None

    Returns:
        pygame.Surface: Yuklenen gorsel veya yer tutucu
    """
    dosya_yolu = os.path.join(GORSEL_DIZINI, dosya_adi)
    try:
        gorsel = pygame.image.load(dosya_yolu).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        return gorsel
    except (FileNotFoundError, pygame.error):
        # Fallback: renkli yer tutucu
        gen = boyut[0] if boyut else 64
        yuk = boyut[1] if boyut else 64
        yer_tutucu = pygame.Surface((gen, yuk), pygame.SRCALPHA)
        yer_tutucu.fill((MAGENTA[0], MAGENTA[1], MAGENTA[2], 180))
        pygame.draw.line(yer_tutucu, BEYAZ,
                         (0, 0), (gen, yuk), 2)
        pygame.draw.line(yer_tutucu, BEYAZ,
                         (gen, 0), (0, yuk), 2)
        return yer_tutucu


def yildizli_arkaplan_olustur(genislik, yukseklik, yildiz_sayisi=200):
    """Yildizli uzay arkaplan gorseli olustur.

    Gercek bir arkaplan gorseli bulunamazsa bu fonksiyon
    prosedural olarak yildizli bir gokyuzu olusturur.
    """
    arkaplan = pygame.Surface((genislik, yukseklik))
    arkaplan.fill(KOYU_MAVI)

    for _ in range(yildiz_sayisi):
        x = random.randint(0, genislik - 1)
        y = random.randint(0, yukseklik - 1)
        parlaklik = random.randint(100, 255)
        boyut = random.choice([1, 1, 1, 2])
        renk = (parlaklik, parlaklik, parlaklik)
        if boyut == 1:
            arkaplan.set_at((x, y), renk)
        else:
            pygame.draw.circle(arkaplan, renk, (x, y), boyut)

    return arkaplan


def gemi_olustur(boyut=48, renk=(100, 180, 255)):
    """Basit ucgen gemi gorseli olustur (fallback)."""
    surface = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
    noktalar = [
        (boyut // 2, 4),           # burun
        (4, boyut - 4),            # sol kanat
        (boyut - 4, boyut - 4),    # sag kanat
    ]
    pygame.draw.polygon(surface, renk, noktalar)
    # Motor alevi
    pygame.draw.polygon(surface,
                        (255, 150, 50, 200),
                        [(boyut // 2 - 6, boyut - 4),
                         (boyut // 2, boyut + 2),
                         (boyut // 2 + 6, boyut - 4)])
    return surface


def dusman_olustur(boyut=36, renk=(255, 80, 80)):
    """Basit dusman gorseli olustur (fallback)."""
    surface = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
    noktalar = [
        (boyut // 2, boyut - 4),   # burun (asagi)
        (4, 4),                     # sol kanat
        (boyut - 4, 4),            # sag kanat
    ]
    pygame.draw.polygon(surface, renk, noktalar)
    return surface


def main():
    """Ana fonksiyon."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # --- Gorselleri yukle ---
    # Arka plan
    arkaplan_gorseli = gorsel_yukle("arkaplan_uzay.png",
                                    boyut=(GENISLIK, YUKSEKLIK))
    # Eger gorsel yuklenemezse prosedural arkaplan kullan
    # (Fallback gorselini kontrol et)
    arkaplan_pikseli = arkaplan_gorseli.get_at((0, 0))
    if arkaplan_pikseli[0] == MAGENTA[0]:
        # Fallback aktif, prosedural arkaplan olustur
        arkaplan_gorseli = yildizli_arkaplan_olustur(GENISLIK,
                                                      YUKSEKLIK)

    # Oyuncu gemisi
    gemi_dosya = gorsel_yukle("playerShip1_blue.png",
                               boyut=(64, 64))
    gemi_pikseli = gemi_dosya.get_at((32, 32))
    if gemi_pikseli[0] == MAGENTA[0] and gemi_pikseli[1] == 0:
        gemi_gorseli = gemi_olustur(64, (100, 180, 255))
    else:
        gemi_gorseli = gemi_dosya

    # Dusman gemileri
    dusman_dosya = gorsel_yukle("enemyRed1.png",
                                 boyut=(48, 48))
    dusman_pikseli = dusman_dosya.get_at((24, 24))
    if dusman_pikseli[0] == MAGENTA[0] and dusman_pikseli[1] == 0:
        dusman_gorseli = dusman_olustur(48, (255, 80, 80))
    else:
        dusman_gorseli = dusman_dosya

    # Dusman konumlari
    dusmanlar = []
    for i in range(5):
        x = 100 + i * 140
        y = random.randint(50, 180)
        hiz = random.uniform(0.5, 1.5)
        dusmanlar.append({"x": x, "y": float(y), "hiz": hiz,
                          "baslangic_y": float(y)})

    # Oyuncu konumu
    oyuncu_x = GENISLIK // 2
    oyuncu_y = YUKSEKLIK - 100

    # Font
    font = pygame.font.Font(None, 24)

    # Zaman sayaci
    kare_sayaci = 0

    # --- Ana oyun dongusu ---
    calistir = True
    while calistir:
        dt = saat.tick(FPS) / 1000.0
        kare_sayaci += 1

        # --- Olaylari isle ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- Oyuncu gemisi fareyi takip etsin ---
        fare_x, fare_y = pygame.mouse.get_pos()
        # Geminin merkezi fareye hizalansin
        gemi_gen = gemi_gorseli.get_width()
        gemi_yuk = gemi_gorseli.get_height()
        oyuncu_x = fare_x - gemi_gen // 2
        oyuncu_y = fare_y - gemi_yuk // 2

        # --- Dusmanlari guncelle (yukari-asagi salinim) ---
        for dusman in dusmanlar:
            dusman["y"] = (dusman["baslangic_y"]
                           + math.sin(kare_sayaci * 0.03
                                       * dusman["hiz"]) * 30)

        # =============================================
        # CIZIM SIRASI (Z-ORDER)
        # =============================================

        # Katman 1: Arka plan (en arkada)
        ekran.blit(arkaplan_gorseli, (0, 0))

        # Katman 2: Dusman gemileri
        for dusman in dusmanlar:
            ekran.blit(dusman_gorseli,
                       (int(dusman["x"]), int(dusman["y"])))

        # Katman 3: Oyuncu gemisi (en onde)
        ekran.blit(gemi_gorseli, (oyuncu_x, oyuncu_y))

        # Katman 4: UI elemanlari (her seyin ustunde)
        katman_yazi = font.render(
            "Z-Order: Arkaplan -> Dusmanlar -> Oyuncu -> UI",
            True, SARI
        )
        ekran.blit(katman_yazi, (10, YUKSEKLIK - 30))

        konum_yazi = font.render(
            f"Fare: ({fare_x}, {fare_y})  FPS: {saat.get_fps():.0f}",
            True, BEYAZ
        )
        ekran.blit(konum_yazi, (10, 10))

        # Ekrani guncelle
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
Ekranda yildizli uzay arkaplan gorunur.
5 adet kirmizi dusman gemisi yukari-asagi sallanir.
Mavi oyuncu gemisi fareyle hareket eder.
Altta "Z-Order: Arkaplan -> Dusmanlar -> Oyuncu -> UI" yazisi gorunur.

Fare ile gemiyi hareket ettir.
ESC veya pencere kapatma ile cikis yap.

Not: Eger assets/images klasorunde gorsel dosyalari yoksa,
program prosedural olarak gorseller olusturur ve calisir.
"""
