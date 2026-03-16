"""
Muzik Yukleme ve Calma - Arka Plan Muzigi Temelleri

Bu program pygame.mixer.music modulunu kullanarak
bir muzik dosyasini yukler ve arka planda calar.

Ogrenilecek kavramlar:
- pygame.mixer.music.load()
- pygame.mixer.music.play()
- music.get_busy() ile durum kontrolu
- Sound vs music farki

Bolum: 07 - Ses ve Muzik
Unite: 3 - Arka Plan Muzigi

Calistirma: python 01_muzik_yukleme.py
Gereksinimler: pygame
"""

import pygame
import os

# Sabitler
GENISLIK = 640
YUKSEKLIK = 400
BASLIK = "Muzik Yukleme Ornegi"
FPS = 60

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
MAVI = (70, 130, 180)
YESIL = (50, 200, 100)
KIRMIZI = (200, 60, 60)


def muzik_dosyasi_olustur():
    """Test icin basit bir ses dosyasi olusturur (gercek projede gerekli degil)."""
    # Not: Gercek projede hazir muzik dosyalari kullanilir.
    # Bu fonksiyon sadece ornek kodun hatasiz calismasini saglar.
    dosya_yolu = "test_muzik.wav"
    if not os.path.exists(dosya_yolu):
        # Basit bir sinuzoidal ses olustur
        import array
        import struct
        import wave

        sure = 5  # saniye
        ornekleme = 22050
        frekans = 440  # Hz (La notasi)
        ornekler = []
        for i in range(sure * ornekleme):
            import math
            deger = int(16000 * math.sin(2 * math.pi * frekans * i / ornekleme))
            ornekler.append(deger)

        with wave.open(dosya_yolu, "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(ornekleme)
            for ornek in ornekler:
                wav.writeframes(struct.pack("<h", ornek))

    return dosya_yolu


def main():
    """Ana fonksiyon."""
    # PyGame ve mixer baslatma
    pygame.init()
    pygame.mixer.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    baslik_font = pygame.font.SysFont("Arial", 28, bold=True)

    # Muzik dosyasini hazirla
    muzik_dosyasi = muzik_dosyasi_olustur()

    # Muzik dosyasini yukle (streaming icin hazirla)
    pygame.mixer.music.load(muzik_dosyasi)
    print(f"[OK] Muzik yuklendi: {muzik_dosyasi}")

    # Muzigi sonsuz dongude cal
    pygame.mixer.music.play(loops=-1)
    print("[OK] Muzik caliniyor (sonsuz dongu)")

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Ekrani temizle
        ekran.fill(SIYAH)

        # Baslik
        baslik = baslik_font.render("Muzik Yukleme Ornegi", True, MAVI)
        ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 30))

        # Muzik durumu
        caliyor = pygame.mixer.music.get_busy()
        durum_renk = YESIL if caliyor else KIRMIZI
        durum_metin = "Caliyor" if caliyor else "Durdu"
        durum = font.render(f"Muzik Durumu: {durum_metin}", True, durum_renk)
        ekran.blit(durum, (50, 100))

        # Ses seviyesi
        seviye = pygame.mixer.music.get_volume()
        seviye_metin = font.render(f"Ses Seviyesi: {seviye:.1f}", True, BEYAZ)
        ekran.blit(seviye_metin, (50, 140))

        # Dosya bilgisi
        dosya_metin = font.render(f"Dosya: {muzik_dosyasi}", True, BEYAZ)
        ekran.blit(dosya_metin, (50, 180))

        # Talimatlar
        talimat = font.render("ESC: Cikis", True, (150, 150, 150))
        ekran.blit(talimat, (50, YUKSEKLIK - 50))

        pygame.display.flip()
        saat.tick(FPS)

    # Temizlik
    pygame.mixer.music.stop()
    pygame.quit()

    # Test dosyasini sil
    if os.path.exists("test_muzik.wav"):
        os.remove("test_muzik.wav")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
[OK] Muzik yuklendi: test_muzik.wav
[OK] Muzik caliniyor (sonsuz dongu)

640x400 piksel boyutunda bir pencere acilir.
Ekranda muzik durumu (Caliyor/Durdu) ve ses seviyesi gosterilir.
Arka planda surekli muzik calar.
ESC ile program kapatilir.
"""
