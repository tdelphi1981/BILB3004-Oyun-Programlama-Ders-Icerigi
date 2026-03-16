"""
Lab 07 - Bonus Baslangic Kodu
Mesafeye Bagli Volume

Bu dosya Lab 07 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Mesafe hesabi ile dinamik ses seviyesi
- Fare pozisyonuna bagli volume ayari
- Surekli guncellenen ses parametreleri

Lab: 07 - Ses ve Muzik
Bonus: Mesafeye Bagli Volume

Calistirma: uv run python bonus.py
"""

import pygame
import array
import math
import random

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Mesafeye Bagli Volume - Bonus")
font = pygame.font.SysFont("Arial", 18)
saat = pygame.time.Clock()


def ses_olustur(frekans=440, sure_ms=300):
    """Verilen frekans ve surede kare dalga ses olusturur."""
    ornekleme = 44100
    ornek_sayisi = int(ornekleme * sure_ms / 1000)
    buf = array.array('h')
    periyot = max(1, int(ornekleme / frekans))
    for i in range(ornek_sayisi):
        zarf = 1.0 - (i / ornek_sayisi)
        deger = int(3000 * zarf)
        buf.append(deger if (i % periyot) < (periyot // 2) else -deger)
    return pygame.mixer.Sound(buffer=buf)


# Tehlike sesi - surekli calar, volume mesafeye bagli degisir
tehlike_ses = ses_olustur(150, 5000)
tehlike_ses.set_volume(0.0)
tehlike_ses.play(loops=-1)

# Hedef
HEDEF_YARICAP = 30
MAKS_MESAFE = 400.0  # Bu mesafeden uzakta volume = 0

hedef_x = random.randint(100, GENISLIK - 100)
hedef_y = random.randint(100, YUKSEKLIK - 100)

skor = 0

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
            fare_x, fare_y = olay.pos
            mesafe = math.sqrt(
                (fare_x - hedef_x) ** 2 + (fare_y - hedef_y) ** 2
            )
            if mesafe <= HEDEF_YARICAP:
                skor += 1
                hedef_x = random.randint(100, GENISLIK - 100)
                hedef_y = random.randint(100, YUKSEKLIK - 100)

    # --- Mesafe hesapla ---
    fare_x, fare_y = pygame.mouse.get_pos()
    mesafe = math.sqrt(
        (fare_x - hedef_x) ** 2 + (fare_y - hedef_y) ** 2
    )

    # GOREV: Mesafeye bagli volume hesaplayin
    # - mesafe >= MAKS_MESAFE ise volume = 0.0
    # - mesafe == 0 ise volume = 1.0
    # - Arada oransal azalsin
    # Ipucu:
    #   if mesafe >= MAKS_MESAFE:
    #       volume = 0.0
    #   else:
    #       volume = 1.0 - (mesafe / MAKS_MESAFE)
    #   tehlike_ses.set_volume(volume)

    # Simdilik sabit volume (GOREV tamamlaninca kaldirin)
    volume = 0.0
    tehlike_ses.set_volume(volume)

    # --- Cizim ---
    ekran.fill((15, 15, 30))

    # Mesafe cemberi (gorsel ipucu)
    if mesafe < MAKS_MESAFE:
        alfa = int(255 * (1.0 - mesafe / MAKS_MESAFE))
        tehlike_renk = (alfa, 0, 0)
    else:
        tehlike_renk = (30, 0, 0)

    # Hedef
    pygame.draw.circle(ekran, tehlike_renk, (hedef_x, hedef_y),
                       int(MAKS_MESAFE), 1)
    pygame.draw.circle(ekran, (200, 50, 50), (hedef_x, hedef_y),
                       HEDEF_YARICAP)
    pygame.draw.circle(ekran, (255, 100, 100), (hedef_x, hedef_y),
                       HEDEF_YARICAP - 10)
    pygame.draw.circle(ekran, (255, 200, 200), (hedef_x, hedef_y), 5)

    # Nisan gostergesi
    pygame.draw.line(
        ekran, (100, 200, 100),
        (fare_x - 12, fare_y), (fare_x + 12, fare_y), 1
    )
    pygame.draw.line(
        ekran, (100, 200, 100),
        (fare_x, fare_y - 12), (fare_x, fare_y + 12), 1
    )

    # Bilgiler
    skor_yazi = font.render(f"Skor: {skor}", True, (255, 255, 255))
    ekran.blit(skor_yazi, (20, 20))

    mesafe_yazi = font.render(
        f"Mesafe: {mesafe:.0f} px", True, (180, 180, 180)
    )
    ekran.blit(mesafe_yazi, (20, 50))

    vol_yazi = font.render(
        f"Tehlike Volume: {volume:.2f}", True, (200, 100, 100)
    )
    ekran.blit(vol_yazi, (20, 80))

    # Volume bar
    bar_gen = int(300 * volume)
    pygame.draw.rect(ekran, (60, 30, 30), (20, 110, 300, 20))
    pygame.draw.rect(ekran, (200, 50, 50), (20, 110, bar_gen, 20))
    pygame.draw.rect(ekran, (150, 150, 150), (20, 110, 300, 20), 1)

    bilgi = font.render(
        "Hedefe yaklas -> ses yukselir | Tikla -> vur!",
        True, (150, 150, 170)
    )
    ekran.blit(bilgi, (GENISLIK // 2 - bilgi.get_width() // 2,
                       YUKSEKLIK - 35))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu pencere acilir.
Kirmizi hedef ve mesafe cemberi gosterilir.

Fare hedefe yaklastikca:
- Kirmizi cember parlaklasmaya baslar
- (GOREV tamamlaninca) tehlike sesi yükselir

Hedefe tiklandiginda skor artar ve hedef yeni konuma gider.
Volume bar sol ustte gosterilir.

GOREV tamamlandiktan sonra:
Fare hedefe yaklasiyor -> volume artar (ses yukselir).
Fare uzaklasiyor -> volume azalir (ses azalir).
MAKS_MESAFE disinda ses tamamen sessizdir.
"""
