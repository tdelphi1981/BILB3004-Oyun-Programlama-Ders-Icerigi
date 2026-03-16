"""
Ses Kontrol - Volume, Fadeout, Durdurma

Bu program ses seviyesi ayarlama, fadeout ve durdurma
islemlerini interaktif olarak gosterir.

Ogrenilecek kavramlar:
- set_volume() / get_volume()
- stop() ile aninda durdurma
- fadeout() ile yumusak kapanis
- get_num_channels() ile durum sorgulama

Bolum: 07 - Ses ve Muzik
Unite: 2 - Ses Efektleri

Calistirma: python 02_ses_kontrol.py
Gereksinimler: pygame
"""

import pygame
import array

# Sabitler
GENISLIK = 600
YUKSEKLIK = 400
BASLIK = "Ses Kontrol Paneli"
FPS = 60


def ses_olustur(frekans=440, sure_ms=3000):
    """Basit test ses dalgasi olustur."""
    ornekleme = 44100
    ornek_sayisi = int(ornekleme * sure_ms / 1000)

    buf = array.array('h')
    ampl = 4096
    periyot = max(1, int(ornekleme / frekans))

    for i in range(ornek_sayisi):
        if (i % periyot) < (periyot // 2):
            buf.append(ampl)
        else:
            buf.append(-ampl)

    return pygame.mixer.Sound(buffer=buf)


def volume_bar_ciz(ekran, x, y, genislik, yukseklik, seviye, etiket, font):
    """Ses seviyesi gostergesi ciz."""
    # Arka plan
    pygame.draw.rect(ekran, (60, 60, 80), (x, y, genislik, yukseklik))
    # Dolu kisim
    dolu_gen = int(genislik * seviye)
    renk = (50, 200, 50) if seviye < 0.7 else (200, 200, 50) if seviye < 0.9 else (200, 50, 50)
    pygame.draw.rect(ekran, renk, (x, y, dolu_gen, yukseklik))
    # Cerceve
    pygame.draw.rect(ekran, (200, 200, 200), (x, y, genislik, yukseklik), 1)
    # Etiket
    metin = font.render(f"{etiket}: {seviye:.1f}", True, (220, 220, 220))
    ekran.blit(metin, (x, y - 22))


def main():
    """Ana fonksiyon."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    font_buyuk = pygame.font.SysFont("Arial", 20)

    # Test sesi olustur (uzun, dongusel kullanim icin)
    test_sesi = ses_olustur(frekans=330, sure_ms=5000)
    ses_seviyesi = 0.5
    test_sesi.set_volume(ses_seviyesi)

    durum = "Hazir. SPACE ile sesi baslat."
    caliniyor = False

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                elif olay.key == pygame.K_SPACE:
                    # Sesi baslat/durdur
                    if test_sesi.get_num_channels() > 0:
                        test_sesi.stop()
                        caliniyor = False
                        durum = "Ses durduruldu (stop)"
                    else:
                        test_sesi.play(loops=-1)
                        caliniyor = True
                        durum = "Ses caliniyor (sonsuz dongu)"

                elif olay.key == pygame.K_UP:
                    # Ses seviyesini artir
                    ses_seviyesi = min(1.0, ses_seviyesi + 0.1)
                    test_sesi.set_volume(ses_seviyesi)
                    durum = f"Volume: {ses_seviyesi:.1f}"

                elif olay.key == pygame.K_DOWN:
                    # Ses seviyesini azalt
                    ses_seviyesi = max(0.0, ses_seviyesi - 0.1)
                    test_sesi.set_volume(ses_seviyesi)
                    durum = f"Volume: {ses_seviyesi:.1f}"

                elif olay.key == pygame.K_f:
                    # Fadeout
                    test_sesi.fadeout(2000)
                    durum = "Fadeout baslatildi (2 saniye)"

                elif olay.key == pygame.K_s:
                    # Aninda durdur
                    test_sesi.stop()
                    caliniyor = False
                    durum = "Ses aninda durduruldu (stop)"

        # Caliniyor durumu guncelle
        caliniyor = test_sesi.get_num_channels() > 0

        # Cizim
        ekran.fill((25, 25, 40))

        # Baslik
        baslik = font_buyuk.render("Ses Kontrol Paneli", True, (255, 200, 50))
        ekran.blit(baslik, (20, 10))

        # Kontroller
        kontroller = [
            "SPACE - Baslat / Durdur",
            "YUKARI/ASAGI - Volume ayarla",
            "F - Fadeout (2 saniye)",
            "S - Aninda durdur (stop)",
            "ESC - Cikis",
        ]
        for i, kontrol in enumerate(kontroller):
            metin = font.render(kontrol, True, (180, 180, 180))
            ekran.blit(metin, (20, 50 + i * 24))

        # Volume bar
        volume_bar_ciz(ekran, 20, 220, 300, 25, ses_seviyesi, "Volume", font)

        # Durum gostergesi
        renk_durum = (100, 255, 100) if caliniyor else (255, 100, 100)
        durum_metni = "CALINIYOR" if caliniyor else "DURDU"
        d_metin = font_buyuk.render(durum_metni, True, renk_durum)
        ekran.blit(d_metin, (350, 220))

        # Aktif kanal bilgisi
        aktif = test_sesi.get_num_channels()
        kanal_metin = font.render(f"Aktif kanal: {aktif}", True, (150, 150, 255))
        ekran.blit(kanal_metin, (20, 270))

        # Ses uzunlugu
        uzunluk = test_sesi.get_length()
        uzunluk_metin = font.render(f"Ses suresi: {uzunluk:.1f}s", True, (150, 150, 255))
        ekran.blit(uzunluk_metin, (20, 295))

        # Durum mesaji
        durum_render = font.render(durum, True, (200, 200, 100))
        ekran.blit(durum_render, (20, YUKSEKLIK - 35))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
600x400 piksel bir pencere acilir.
Kontroller:
- SPACE: Sesi baslatir/durdurur
- Yukari/Asagi ok: Volume ayarlar (0.0-1.0)
- F: 2 saniyede fadeout uygular
- S: Aninda durdurur
Ses seviyesi gorsel bir bar ile gosterilir.
"""
