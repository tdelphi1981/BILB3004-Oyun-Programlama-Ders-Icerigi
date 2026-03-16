"""
Lab 07 - Calisma 1 Baslangic Kodu
Ses Dosyasi Yukleme ve Calma

Bu dosya Lab 07 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.mixer ile ses olusturma
- Sound.play() parametreleri (loops, maxtime, fade_ms)
- Programatik ses uretimi (kare dalga)

Lab: 07 - Ses ve Muzik
Calisma: 1 - Ses Dosyasi Yukleme ve Calma

Calistirma: uv run python calisma1.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import array

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

GENISLIK = 500
YUKSEKLIK = 300

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Ses Testi")
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


# Mevcut sesler
ses1 = ses_olustur(440, 300)   # La notasi, 300ms
ses2 = ses_olustur(660, 500)   # Mi notasi, 500ms

# GOREV 1: Ucuncu bir ses olusturun (880 Hz, 200ms) ve ses3 degiskenine atayin
# Ipucu: ses3 = ses_olustur(...)

# GOREV 2: Sonsuz dongu icin uzun sureli bir ses olusturun (ornegin 1000ms)
# Ipucu: ses_dongu = ses_olustur(...)

# GOREV 3: maxtime ve fade_ms testi icin uzun sureli bir ses olusturun
# Ipucu: ses_uzun = ses_olustur(...)

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_1:
                ses1.play()
            elif olay.key == pygame.K_2:
                ses2.play(loops=2)

            # GOREV 1: 3 tusuna basildiginda ses3 calsin
            # Ipucu: elif olay.key == pygame.K_3: ses3.play()

            # GOREV 2: 4 tusuna basildiginda sonsuz dongu (loops=-1)
            #          S tusuna basildiginda tum sesler dursun
            # Ipucu:
            #   elif olay.key == pygame.K_4:
            #       ses_dongu.play(loops=-1)
            #   elif olay.key == pygame.K_s:
            #       pygame.mixer.stop()

            # GOREV 3: 5 tusuna basildiginda maxtime=400 ile kisa kes
            #          6 tusuna basildiginda fade_ms=500 ile yumusak baslat
            # Ipucu:
            #   elif olay.key == pygame.K_5:
            #       ses_uzun.play(maxtime=400)
            #   elif olay.key == pygame.K_6:
            #       ses_uzun.play(fade_ms=500)

    # Cizim
    ekran.fill((30, 30, 50))

    satirlar = [
        "1: Tek ses | 2: 3x tekrar",
        "3: Ucuncu ses (GOREV 1)",
        "4: Sonsuz dongu | S: Durdur (GOREV 2)",
        "5: maxtime | 6: fade_ms (GOREV 3)",
    ]
    for i, satir in enumerate(satirlar):
        yazi = font.render(satir, True, (200, 200, 200))
        ekran.blit(yazi, (20, 20 + i * 30))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
500x300 piksel boyutunda koyu pencere acilir.
Ekranda tus bilgileri gosterilir.

1 tusuna basildiginda kisa bir "bip" sesi duyulur (La notasi).
2 tusuna basildiginda ses 3 kez tekrar eder.

GOREV tamamlandiktan sonra:
3 tusuna basildiginda daha yuksek frekansta ses duyulur.
4 tusuna basildiginda ses surekli calar, S ile durur.
5 tusuna basildiginda ses 400ms sonra kesilir.
6 tusuna basildiginda ses yavasca yukselir.
"""
