"""
Lab 07 - Calisma 2 Baslangic Kodu
Ses Seviyesi Kontrolu

Bu dosya Lab 07 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Sound.set_volume() ile ses seviyesi ayari
- Sound.fadeout() ile yavas sondurme
- Gorsel volume bar olusturma

Lab: 07 - Ses ve Muzik
Calisma: 2 - Ses Seviyesi Kontrolu

Calistirma: uv run python calisma2.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import array

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

GENISLIK = 500
YUKSEKLIK = 300

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Volume Kontrolu")
font = pygame.font.SysFont("Arial", 18)
saat = pygame.time.Clock()


def ses_olustur(frekans=330, sure_ms=2000):
    """Verilen frekans ve surede kare dalga ses olusturur."""
    ornekleme = 44100
    ornek_sayisi = int(ornekleme * sure_ms / 1000)
    buf = array.array('h')
    periyot = max(1, int(ornekleme / frekans))
    for i in range(ornek_sayisi):
        if (i % periyot) < (periyot // 2):
            buf.append(2500)
        else:
            buf.append(-2500)
    return pygame.mixer.Sound(buffer=buf)


ses = ses_olustur()
volume = 0.5
ses.set_volume(volume)
ses.play(loops=-1)

# GOREV 1: Mute/unmute icin degiskenler
# Ipucu:
#   mute = False
#   onceki_volume = volume

# GOREV 3: Ikinci ses olusturun ve volume degiskeni tanimlayin
# Ipucu:
#   ses2 = ses_olustur(440, 2000)
#   volume2 = 0.5
#   ses2.set_volume(volume2)
#   ses2.play(loops=-1)

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_UP:
                volume = min(1.0, volume + 0.1)
                ses.set_volume(volume)
            elif olay.key == pygame.K_DOWN:
                volume = max(0.0, volume - 0.1)
                ses.set_volume(volume)
            elif olay.key == pygame.K_f:
                ses.fadeout(2000)

            # GOREV 1: Hassasiyeti 0.05'e dusur ve M ile mute/unmute ekle
            # - Yukari/Asagi ok tuslari icin artis miktarini 0.05 yapin
            # - M tusuna basildiginda:
            #   - mute degilse: onceki_volume'u kaydet, volume=0 yap
            #   - mute ise: onceki_volume'a geri don
            # Ipucu:
            #   elif olay.key == pygame.K_m:
            #       if not mute:
            #           onceki_volume = volume
            #           volume = 0.0
            #           mute = True
            #       else:
            #           volume = onceki_volume
            #           mute = False
            #       ses.set_volume(volume)

            # GOREV 3: W/S tuslari ile ses2 volume kontrolu
            # Ipucu:
            #   elif olay.key == pygame.K_w:
            #       volume2 = min(1.0, volume2 + 0.05)
            #       ses2.set_volume(volume2)
            #   elif olay.key == pygame.K_s:
            #       volume2 = max(0.0, volume2 - 0.05)
            #       ses2.set_volume(volume2)

    # GOREV 2: Fare X pozisyonu ile volume ayarla
    # Her karede farenin X konumunu pencere genisligine bol
    # Ipucu:
    #   fare_x, _ = pygame.mouse.get_pos()
    #   volume = fare_x / GENISLIK
    #   ses.set_volume(volume)

    # --- Cizim ---
    ekran.fill((30, 30, 50))

    bilgi = font.render(
        f"Volume: {volume:.2f} | Yukari/Asagi ok | F: Fadeout",
        True, (200, 200, 200)
    )
    ekran.blit(bilgi, (20, 20))

    # Gorsel volume bar - Ses 1
    bar_gen = int(400 * volume)
    pygame.draw.rect(ekran, (60, 60, 80), (50, 80, 400, 30))
    renk = (50, 200, 50) if volume < 0.7 else (200, 200, 50)
    pygame.draw.rect(ekran, renk, (50, 80, bar_gen, 30))
    pygame.draw.rect(ekran, (200, 200, 200), (50, 80, 400, 30), 1)

    etiket1 = font.render("Ses 1", True, (180, 180, 180))
    ekran.blit(etiket1, (50, 60))

    # GOREV 3: Ikinci ses icin volume bar cizin
    # Ipucu:
    #   etiket2 = font.render(f"Ses 2: {volume2:.2f} (W/S)",
    #                         True, (180, 180, 180))
    #   ekran.blit(etiket2, (50, 130))
    #   bar_gen2 = int(400 * volume2)
    #   pygame.draw.rect(ekran, (60, 60, 80), (50, 150, 400, 30))
    #   renk2 = (50, 150, 200) if volume2 < 0.7 else (200, 150, 50)
    #   pygame.draw.rect(ekran, renk2, (50, 150, bar_gen2, 30))
    #   pygame.draw.rect(ekran, (200, 200, 200), (50, 150, 400, 30), 1)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
500x300 piksel boyutunda koyu pencere acilir.
Surekli calan bir ses duyulur (330 Hz).
Yesil bir volume bar gosterilir.

Yukari ok: Volume artar (bar buyur).
Asagi ok: Volume azalir (bar kuculur).
F: Ses 2 saniyede solar.

GOREV tamamlandiktan sonra:
Hassasiyet 0.05 olur, M ile mute/unmute calisir.
Fare X pozisyonu volume'u kontrol eder.
Ikinci ses ve ikinci volume bar eklenir.
"""
