"""
Lab 07 - Calisma 3 Baslangic Kodu
Kanal Yonetimi

Bu dosya Lab 07 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.mixer.Channel ile kanal yonetimi
- Bireysel kanal durdurma ve volume kontrolu
- set_endevent() ile kanal olaylari

Lab: 07 - Ses ve Muzik
Calisma: 3 - Kanal Yonetimi

Calistirma: uv run python calisma3.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import array

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.set_num_channels(4)

GENISLIK = 600
YUKSEKLIK = 400

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Kanal Yonetimi")
font = pygame.font.SysFont("Arial", 16)
saat = pygame.time.Clock()


def ses_olustur(frekans, sure_ms=1500):
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


# 4 farkli nota
sesler = [
    ses_olustur(262),   # Do
    ses_olustur(330),   # Mi
    ses_olustur(392),   # Sol
    ses_olustur(440),   # La
]
kanallar = [pygame.mixer.Channel(i) for i in range(4)]

# GOREV 2: Her kanal icin volume degiskenleri ve secili kanal
# Ipucu:
#   kanal_volumeler = [1.0, 1.0, 1.0, 1.0]
#   secili_kanal = 0

# GOREV 3: Kanal 0 icin endevent ayarla
# Ipucu:
#   KANAL0_BITTI = pygame.USEREVENT + 1
#   kanallar[0].set_endevent(KANAL0_BITTI)
#   siradaki_ses = 0  # Hangi sesin calnacagini takip et

mesaj = ""
mesaj_zamani = 0

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            # 1-4 tuslari ile kanallarda ses cal
            if olay.key == pygame.K_1:
                kanallar[0].play(sesler[0], loops=-1)
            elif olay.key == pygame.K_2:
                kanallar[1].play(sesler[1], loops=-1)
            elif olay.key == pygame.K_3:
                kanallar[2].play(sesler[2], loops=-1)
            elif olay.key == pygame.K_4:
                kanallar[3].play(sesler[3], loops=-1)
            elif olay.key == pygame.K_s:
                pygame.mixer.stop()

            # GOREV 1: Q/W/E/R ile bireysel kanal durdurma
            # Ipucu:
            #   elif olay.key == pygame.K_q:
            #       kanallar[0].stop()
            #   elif olay.key == pygame.K_w:
            #       kanallar[1].stop()
            #   elif olay.key == pygame.K_e:
            #       kanallar[2].stop()
            #   elif olay.key == pygame.K_r:
            #       kanallar[3].stop()

            # GOREV 2: Sayi tuslari ile kanal sec,
            #          Yukari/Asagi ok ile secili kanalin volume'unu degistir
            # Ipucu:
            #   # Sayi tuslarina basildiginda secili_kanal'i guncelle
            #   # (1-4 tuslarinda hem cal hem sec)
            #   if olay.key == pygame.K_1:
            #       secili_kanal = 0
            #   ...
            #   elif olay.key == pygame.K_UP:
            #       kanal_volumeler[secili_kanal] = min(
            #           1.0, kanal_volumeler[secili_kanal] + 0.1)
            #       kanallar[secili_kanal].set_volume(
            #           kanal_volumeler[secili_kanal])
            #   elif olay.key == pygame.K_DOWN:
            #       kanal_volumeler[secili_kanal] = max(
            #           0.0, kanal_volumeler[secili_kanal] - 0.1)
            #       kanallar[secili_kanal].set_volume(
            #           kanal_volumeler[secili_kanal])

        # GOREV 3: Kanal 0 bitis olayini yakala
        # Ipucu:
        #   elif olay.type == KANAL0_BITTI:
        #       siradaki_ses = (siradaki_ses + 1) % len(sesler)
        #       kanallar[0].play(sesler[siradaki_ses])
        #       mesaj = f"Kanal 0 bitti! Siradaki ses: {siradaki_ses}"
        #       mesaj_zamani = pygame.time.get_ticks()

    # --- Cizim ---
    ekran.fill((20, 20, 35))

    bilgi = font.render(
        "1-4: Kanallarda cal | S: Tumu durdur",
        True, (180, 180, 180)
    )
    ekran.blit(bilgi, (20, 10))

    gorev_bilgi = font.render(
        "Q/W/E/R: Bireysel durdur (GOREV 1)",
        True, (150, 150, 170)
    )
    ekran.blit(gorev_bilgi, (20, 30))

    # Kanal durum gostergeleri
    for i, kanal in enumerate(kanallar):
        aktif = kanal.get_busy()
        renk = (50, 200, 50) if aktif else (80, 80, 80)
        pygame.draw.rect(
            ekran, renk, (20, 70 + i * 70, 560, 50),
            border_radius=5
        )

        durum_metin = "AKTIF" if aktif else "BOS"
        metin = font.render(
            f"Kanal {i}: {durum_metin}",
            True, (255, 255, 255)
        )
        ekran.blit(metin, (35, 78 + i * 70))

        # GOREV 2: Secili kanal gostergesi ve volume bilgisi
        # Ipucu:
        #   if i == secili_kanal:
        #       pygame.draw.rect(ekran, (255, 255, 50),
        #                        (20, 70 + i * 70, 560, 50),
        #                        width=2, border_radius=5)
        #   vol_metin = font.render(
        #       f"Vol: {kanal_volumeler[i]:.1f}",
        #       True, (200, 200, 200))
        #   ekran.blit(vol_metin, (480, 78 + i * 70))

    # Mesaj gosterimi (GOREV 3 icin)
    if mesaj and pygame.time.get_ticks() - mesaj_zamani < 3000:
        mesaj_yazi = font.render(mesaj, True, (255, 200, 50))
        ekran.blit(mesaj_yazi, (20, YUKSEKLIK - 30))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
600x400 piksel boyutunda koyu pencere acilir.
4 adet kanal gostergesi gorulur (baslangicta gri/BOS).

1-4 tuslarina basildiginda ilgili kanal yesile doner
ve surekli ses calar.
S tusu tum sesleri durdurur.

GOREV tamamlandiktan sonra:
Q/W/E/R ile bireysel kanallar durdurulur.
Secili kanal sari cerceve ile isaretlenir,
ok tuslari ile volume ayarlanir.
Kanal 0 ses bitince otomatik siradaki ses baslar.
"""
