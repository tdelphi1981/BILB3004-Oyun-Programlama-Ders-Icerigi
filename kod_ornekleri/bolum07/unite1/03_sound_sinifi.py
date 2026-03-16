"""
Sound Sinifi Demo - pygame.mixer.Sound sinifinin temel metotlari

Bu program bir oyun penceresi acar ve tus basildiginda farkli
sesler calar. Sound sinifinin play(), stop(), set_volume() ve
get_length() metotlarini gosterir.

Ogrenilecek kavramlar:
- Sound nesnesi olusturma ve ses calma
- Ses seviyesi kontrolu (set_volume / get_volume)
- Ses durdurma (stop)
- Oyun dongusu icinde ses yonetimi

Bolum: 07 - Ses ve Muzik
Unite: 1 - Ses Sistemi Temelleri

Calistirma: python 03_sound_sinifi.py
Gereksinimler: pygame
"""

import pygame
import array
import math

# Sabitler
GENISLIK = 640
YUKSEKLIK = 400
FPS = 60
BASLIK = "Sound Sinifi Demo - Tusa Bas!"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
MAVI = (70, 130, 180)
YESIL = (50, 180, 100)
KIRMIZI = (200, 60, 60)
GRI = (100, 100, 100)


def sinusoidal_ses(frekans=440, sure=0.3, ornek_hizi=44100):
    """Programatik olarak bir sinusoidal ses olusturur."""
    ornek_sayisi = int(ornek_hizi * sure)
    tampon = array.array("h")
    genlik = 12000

    for i in range(ornek_sayisi):
        zaman = i / ornek_hizi
        deger = int(genlik * math.sin(2.0 * math.pi * frekans * zaman))
        # Fade out efekti (son %20'de ses azalir)
        if i > ornek_sayisi * 0.8:
            oran = (ornek_sayisi - i) / (ornek_sayisi * 0.2)
            deger = int(deger * oran)
        tampon.append(deger)  # Sol kanal
        tampon.append(deger)  # Sag kanal

    return pygame.mixer.Sound(buffer=tampon)


def main():
    """Ana oyun fonksiyonu."""
    # PyGame ve mixer'i baslat
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    kucuk_font = pygame.font.Font(None, 22)

    # Sesleri olustur (programatik)
    sesler = {
        "ates":    sinusoidal_ses(frekans=880, sure=0.15),
        "patlama": sinusoidal_ses(frekans=150, sure=0.5),
        "ziplama": sinusoidal_ses(frekans=520, sure=0.2),
    }

    # Ses seviyelerini ayarla
    sesler["ates"].set_volume(0.6)
    sesler["patlama"].set_volume(0.8)
    sesler["ziplama"].set_volume(0.5)

    # Durum bilgisi
    son_calanan = ""
    ses_seviyesi = 0.5

    # Tus-ses eslemesi
    tus_haritasi = {
        pygame.K_1: ("ates", "1: Ates sesi"),
        pygame.K_2: ("patlama", "2: Patlama sesi"),
        pygame.K_3: ("ziplama", "3: Ziplama sesi"),
    }

    calistir = True
    while calistir:
        # --- Olaylari isle ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                # Ses calma tuslari
                if olay.key in tus_haritasi:
                    anahtar, aciklama = tus_haritasi[olay.key]
                    sesler[anahtar].play()
                    son_calanan = aciklama

                # Ses seviyesi artir
                elif olay.key == pygame.K_UP:
                    ses_seviyesi = min(1.0, ses_seviyesi + 0.1)
                    for ses in sesler.values():
                        ses.set_volume(ses_seviyesi)
                    son_calanan = f"Ses seviyesi: {ses_seviyesi:.1f}"

                # Ses seviyesi azalt
                elif olay.key == pygame.K_DOWN:
                    ses_seviyesi = max(0.0, ses_seviyesi - 0.1)
                    for ses in sesler.values():
                        ses.set_volume(ses_seviyesi)
                    son_calanan = f"Ses seviyesi: {ses_seviyesi:.1f}"

                # Tum sesleri durdur
                elif olay.key == pygame.K_s:
                    pygame.mixer.stop()
                    son_calanan = "Tum sesler durduruldu"

                # Cikis
                elif olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- Cizim ---
        ekran.fill(SIYAH)

        # Baslik
        baslik = font.render("Sound Sinifi Demo", True, MAVI)
        ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 20))

        # Tus bilgileri
        bilgiler = [
            ("[1] Ates sesi", YESIL),
            ("[2] Patlama sesi", YESIL),
            ("[3] Ziplama sesi", YESIL),
            ("", BEYAZ),
            ("[Yukari/Asagi] Ses seviyesi", GRI),
            ("[S] Tum sesleri durdur", GRI),
            ("[ESC] Cikis", GRI),
        ]

        y_konum = 80
        for metin, renk in bilgiler:
            if metin:
                satir = kucuk_font.render(metin, True, renk)
                ekran.blit(satir, (40, y_konum))
            y_konum += 28

        # Ses seviyesi gostergesi
        seviye_metin = font.render(
            f"Ses Seviyesi: {ses_seviyesi:.1f}", True, BEYAZ
        )
        ekran.blit(seviye_metin, (40, 320))

        # Seviye cubugu
        pygame.draw.rect(ekran, GRI, (40, 355, 200, 15))
        pygame.draw.rect(
            ekran, YESIL, (40, 355, int(200 * ses_seviyesi), 15)
        )

        # Son calanan ses bilgisi
        if son_calanan:
            durum = kucuk_font.render(
                f"Son: {son_calanan}", True, KIRMIZI
            )
            ekran.blit(durum, (300, 355))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
640x400 piksel boyutunda bir pencere acilir.
- [1] tusuna basinca ates sesi duyulur
- [2] tusuna basinca patlama sesi duyulur
- [3] tusuna basinca ziplama sesi duyulur
- Yukari/Asagi oklari ses seviyesini ayarlar
- [S] tusu tum sesleri durdurur
- [ESC] tusu programi kapatir
"""
