"""
Ses Calma Parametreleri - Sound.play() Kullanimi

Bu program pygame.mixer.Sound.play() fonksiyonunun
loops, maxtime ve fade_ms parametrelerini gosterir.

Ogrenilecek kavramlar:
- Sound.play() temel kullanim
- loops ile tekrar sayisi
- maxtime ile sure siniri
- fade_ms ile yumusak baslangic

Bolum: 07 - Ses ve Muzik
Unite: 2 - Ses Efektleri

Calistirma: python 01_ses_calma_parametreleri.py
Gereksinimler: pygame
"""

import pygame
import time

# Sabitler
GENISLIK = 600
YUKSEKLIK = 400
BASLIK = "Ses Calma Parametreleri"
FPS = 60


def ses_olustur(frekans=440, sure_ms=200):
    """Basit bir test ses dalgasi olustur (sine wave benzeri)."""
    # pygame.mixer ayarlari
    ornekleme = 44100
    bit_derinlik = -16
    kanal_sayisi = 1

    ornek_sayisi = int(ornekleme * sure_ms / 1000)

    # Basit kare dalga olustur
    import array
    buf = array.array('h')
    ampl = 4096
    periyot = int(ornekleme / frekans)

    for i in range(ornek_sayisi):
        if (i % periyot) < (periyot // 2):
            buf.append(ampl)
        else:
            buf.append(-ampl)

    ses = pygame.mixer.Sound(buffer=buf)
    return ses


def main():
    """Ana fonksiyon."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    # Test sesleri olustur (farkli frekanslarda)
    ses_do = ses_olustur(frekans=262, sure_ms=500)   # Do notasi
    ses_mi = ses_olustur(frekans=330, sure_ms=500)   # Mi notasi
    ses_sol = ses_olustur(frekans=392, sure_ms=500)  # Sol notasi
    ses_uzun = ses_olustur(frekans=440, sure_ms=2000)  # Uzun La notasi

    # Bilgi metinleri
    bilgiler = [
        "1 - Tek sefer cal (loops=0)",
        "2 - 3 kez tekrar cal (loops=2)",
        "3 - Sonsuz dongu (loops=-1)",
        "4 - Maksimum 300ms cal (maxtime=300)",
        "5 - 1sn fade-in ile cal (fade_ms=1000)",
        "6 - Tum sesleri durdur",
        "",
        "ESC - Cikis",
    ]

    durum_mesaji = "Bir tusa basin..."

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                elif olay.key == pygame.K_1:
                    ses_do.play()
                    durum_mesaji = "[OK] Ses bir kez caliniyor (loops=0)"

                elif olay.key == pygame.K_2:
                    ses_mi.play(loops=2)
                    durum_mesaji = "[OK] Ses 3 kez caliniyor (1+2 tekrar)"

                elif olay.key == pygame.K_3:
                    ses_sol.play(loops=-1)
                    durum_mesaji = "[OK] Sonsuz dongu baslatildi (6 ile durdur)"

                elif olay.key == pygame.K_4:
                    ses_uzun.play(maxtime=300)
                    durum_mesaji = "[OK] Uzun ses 300ms ile sinirlandirildi"

                elif olay.key == pygame.K_5:
                    ses_uzun.play(loops=-1, fade_ms=1000)
                    durum_mesaji = "[OK] 1sn fade-in ile sonsuz dongu"

                elif olay.key == pygame.K_6:
                    pygame.mixer.stop()
                    durum_mesaji = "[OK] Tum sesler durduruldu"

        # Cizim
        ekran.fill((30, 30, 50))

        # Baslik
        baslik = font.render("Ses Calma Parametreleri Testi", True, (255, 200, 50))
        ekran.blit(baslik, (20, 15))

        # Bilgi satirlari
        for i, bilgi in enumerate(bilgiler):
            renk = (200, 200, 200) if bilgi else (100, 100, 100)
            metin = font.render(bilgi, True, renk)
            ekran.blit(metin, (20, 60 + i * 28))

        # Durum mesaji
        durum = font.render(durum_mesaji, True, (100, 255, 100))
        ekran.blit(durum, (20, YUKSEKLIK - 40))

        # Aktif kanal sayisi
        aktif = sum(1 for i in range(pygame.mixer.get_num_channels())
                    if pygame.mixer.Channel(i).get_busy())
        kanal_metin = font.render(
            f"Aktif kanallar: {aktif}/{pygame.mixer.get_num_channels()}",
            True, (150, 150, 255)
        )
        ekran.blit(kanal_metin, (20, YUKSEKLIK - 70))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
600x400 piksel bir pencere acilir.
Klavye tuslariyla farkli ses calma parametreleri test edilir:
- 1: Tek sefer ses calma
- 2: 3 kez tekrarli calma
- 3: Sonsuz dongu
- 4: 300ms sure sinirli calma
- 5: 1 saniye fade-in ile calma
- 6: Tum sesleri durdurma
Aktif kanal sayisi ekranda gosterilir.
"""
