"""
Uzay Gemisi Hareket - Tam uygulama

Bu program Bolum 5 Unite 2'nin tum kavramlarini birlestiren
bir uygulamadir. Uzay gemisi ok tuslari / WASD ile hareket eder,
fareye dogru doner ve ekran sinirlarindan cikmaz.

Ogrenilecek kavramlar:
- pygame.transform.rotate() ile fareye dondurme
- pygame.key.get_pressed() ile surekli hareket
- Ekran siniri kontrolu (clamp)
- gorsel_yukle() ile guvenli gorsel yukleme
- Tum transform islemlerini birlestirme

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 2 - Gorsel Manipulasyonu

Calistirma: python 03_gemi_hareket.py
Gereksinimler: pygame
"""

import pygame
import math

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Gemisi - Hareket ve Dondurme"
ARKA_PLAN = (10, 10, 30)

# Hareket sabitleri
HIZ = 5
GEMI_BOYUT = (48, 48)

# Renkler
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 80, 80)
YESIL = (80, 255, 80)
MAVI = (80, 150, 255)
SARI = (255, 220, 80)
GRI = (120, 120, 120)
KOYU_MAVI = (20, 30, 60)


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
        # Yedek: yukari bakan bir uzay gemisi olustur
        gen = boyut[0] if boyut else 64
        yuk = boyut[1] if boyut else 64
        gorsel = pygame.Surface((gen, yuk), pygame.SRCALPHA)

        # Ana govde (ucgen)
        pygame.draw.polygon(gorsel, MAVI, [
            (gen // 2, 2),
            (4, yuk - 4),
            (gen - 4, yuk - 4)
        ])
        # Ic govde
        pygame.draw.polygon(gorsel, (60, 120, 220), [
            (gen // 2, gen // 4),
            (gen // 4, yuk - gen // 4),
            (gen * 3 // 4, yuk - gen // 4)
        ])
        # Kokpit (parlak daire)
        pygame.draw.circle(gorsel, (180, 220, 255),
                           (gen // 2, yuk // 3), gen // 8)
        # Motor alevi
        pygame.draw.polygon(gorsel, SARI, [
            (gen // 3, yuk - 4),
            (gen // 2, yuk + 2),
            (gen * 2 // 3, yuk - 4)
        ])

        if boyut:
            return gorsel  # Zaten istenen boyutta olusturuldu
        return gorsel

    if boyut:
        gorsel = pygame.transform.scale(gorsel, boyut)
    return gorsel


def yildiz_olustur(adet=80):
    """Arka plan icin rastgele yildiz konumlari olusturur.

    Args:
        adet: Yildiz sayisi.

    Returns:
        Yildiz listesi: [(x, y, parlaklik, boyut), ...]
    """
    import random
    yildizlar = []
    for _ in range(adet):
        x = random.randint(0, GENISLIK)
        y = random.randint(0, YUKSEKLIK)
        parlaklik = random.randint(80, 255)
        boyut = random.choice([1, 1, 1, 2])
        yildizlar.append((x, y, parlaklik, boyut))
    return yildizlar


def yildizlari_ciz(ekran, yildizlar):
    """Yildizlari ekrana cizer.

    Args:
        ekran: Hedef Surface.
        yildizlar: Yildiz listesi.
    """
    for x, y, parlaklik, boyut in yildizlar:
        renk = (parlaklik, parlaklik, parlaklik)
        if boyut == 1:
            ekran.set_at((x, y), renk)
        else:
            pygame.draw.circle(ekran, renk, (x, y), boyut)


def metin_ciz(ekran, yazi_tipi, metin, x, y, renk=BEYAZ):
    """Ekrana metin cizer (sol hizali)."""
    yuzey = yazi_tipi.render(metin, True, renk)
    ekran.blit(yuzey, (x, y))


def main():
    """Ana program fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Yazi tipi
    bilgi_font = pygame.font.SysFont("Arial", 14)

    # Gemi gorseli
    gemi_orijinal = gorsel_yukle("assets/images/gemi.png", GEMI_BOYUT)

    # Gemi konumu (ekranin ortasi)
    gemi_x = float(GENISLIK // 2)
    gemi_y = float(YUKSEKLIK // 2)
    gemi_aci = 0.0

    # Arka plan yildizlari
    yildizlar = yildiz_olustur(100)

    # HUD arka plan kutusu
    hud_yuzey = pygame.Surface((220, 90), pygame.SRCALPHA)
    hud_yuzey.fill((0, 0, 0, 140))

    print("=" * 50)
    print("  Uzay Gemisi Hareket Demo")
    print("  Ok tuslari / WASD ile hareket et")
    print("  Fare ile yonu degistir")
    print("  ESC ile cikis")
    print("=" * 50)

    calistir = True
    while calistir:
        dt = saat.tick(FPS) / 1000.0  # Delta time (saniye)

        # --- Olaylari isle ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- Klavye ile hareket ---
        tuslar = pygame.key.get_pressed()

        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            gemi_x -= HIZ
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            gemi_x += HIZ
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            gemi_y -= HIZ
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            gemi_y += HIZ

        # --- Ekran siniri kontrolu ---
        gemi_x = max(0, min(gemi_x, GENISLIK))
        gemi_y = max(0, min(gemi_y, YUKSEKLIK))

        # --- Fareye dogru dondurme ---
        fare_x, fare_y = pygame.mouse.get_pos()
        dx = fare_x - gemi_x
        dy = fare_y - gemi_y
        radyan = math.atan2(-dy, dx)
        gemi_aci = math.degrees(radyan) - 90

        # Orijinalden dondur, center koru
        donmus_gemi = pygame.transform.rotate(gemi_orijinal, gemi_aci)
        gemi_rect = donmus_gemi.get_rect(
            center=(int(gemi_x), int(gemi_y))
        )

        # --- Cizim ---
        ekran.fill(ARKA_PLAN)

        # Yildizlar
        yildizlari_ciz(ekran, yildizlar)

        # Fare hedef isareti
        pygame.draw.circle(ekran, KIRMIZI, (fare_x, fare_y), 8, 1)
        pygame.draw.circle(ekran, KIRMIZI, (fare_x, fare_y), 2)

        # Gemi
        ekran.blit(donmus_gemi, gemi_rect)

        # HUD (bilgi paneli)
        ekran.blit(hud_yuzey, (10, 10))
        metin_ciz(ekran, bilgi_font,
                  f"Konum: ({int(gemi_x)}, {int(gemi_y)})",
                  18, 15, BEYAZ)
        metin_ciz(ekran, bilgi_font,
                  f"Aci: {gemi_aci:.1f} derece",
                  18, 35, BEYAZ)
        metin_ciz(ekran, bilgi_font,
                  f"Fare: ({fare_x}, {fare_y})",
                  18, 55, GRI)
        metin_ciz(ekran, bilgi_font,
                  f"FPS: {saat.get_fps():.0f}",
                  18, 75, GRI)

        # Kontrol bilgisi (alt kisim)
        metin_ciz(ekran, bilgi_font,
                  "WASD / Ok tuslari: Hareket  |  Fare: Yon",
                  GENISLIK // 2 - 160, YUKSEKLIK - 25, GRI)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda uzay temasinda bir pencere acilir.
Arka planda yildizlar gorulur.
Merkezde bir uzay gemisi bulunur.
Ok tuslari veya WASD ile gemi ekranda hareket eder.
Fare imleci neredeyse gemi o yone doner.
Gemi ekran sinirlarindan cikmaz.
Sol ust kosede konum, aci ve FPS bilgisi gosterilir.
ESC ile programdan cikilir.
"""
