"""
FPS Kontrollu Tam Ornek - Zamanlama ve delta time

Bu program, oyun dongusunde FPS kontrolu ve delta time
kullanimini gosterir. Ekranda yatay hareket eden bir kare
goruntulenir. Pencere basliginda anlik FPS degeri gosterilir.

Ogrenilecek kavramlar:
- pygame.time.Clock() ile FPS sinirlamasi
- saat.tick() ile delta time hesaplama
- Frame-bagimsiz hareket (hiz * dt)
- saat.get_fps() ile FPS izleme

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 3 - Ana Oyun Dongusu (Game Loop)

Calistirma: python 02_fps_kontrolu.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 400
FPS = 60
ARKA_PLAN = (10, 10, 30)      # Koyu lacivert
KARE_RENK = (0, 200, 100)     # Yesil
KARE_BOYUT = 50


def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("FPS Kontrolu")

    # Saat nesnesi olustur
    saat = pygame.time.Clock()

    # Karenin baslangic konumu ve hizi
    kare_x = 50.0
    kare_y = (YUKSEKLIK - KARE_BOYUT) / 2  # Dikey orta
    hiz = 200  # piksel/saniye

    # Ana oyun dongusu
    calistir = True
    while calistir:
        # Delta time hesapla (milisaniye -> saniye)
        dt = saat.tick(FPS) / 1000.0

        # ASAMA 1: Olaylari isle
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        # ASAMA 2: Guncelle
        # Frame-bagimsiz hareket: hiz * dt
        kare_x += hiz * dt

        # Ekranin sagina ulastiginda sola dondur
        if kare_x > GENISLIK:
            kare_x = -KARE_BOYUT

        # ASAMA 3: Ciz
        ekran.fill(ARKA_PLAN)
        pygame.draw.rect(
            ekran,
            KARE_RENK,
            (int(kare_x), int(kare_y), KARE_BOYUT, KARE_BOYUT)
        )
        pygame.display.flip()

        # FPS degerini pencere basliginda goster
        fps_gercek = saat.get_fps()
        pygame.display.set_caption(
            f"FPS Kontrolu | FPS: {fps_gercek:.1f} | "
            f"dt: {dt:.4f}s | X: {kare_x:.1f}"
        )

    # PyGame'i kapat
    pygame.quit()
    print("Program sonlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x400 piksel boyutunda koyu lacivert bir pencere acilir.
Yesil bir kare soldan saga dogru sabit hizla hareket eder.
Kare ekranin sagina ulastiginda sola donerek tekrar baslar.
Pencere basliginda anlik FPS, delta time ve X konumu gosterilir.
Pencere kapatildiginda program duzgun sekilde sonlanir.
"""
