"""
Surekli Hareket - get_pressed() ile dort yone nesne hareketi

Bu program ekranda bir kareyi ok tuslariyla hareket ettirir.
key.get_pressed() ve delta time kullanarak kare hizindan
bagimsiz, puruzsuz hareket saglar. Nesne ekran disina cikamaz.

Ogrenilecek kavramlar:
- pygame.key.get_pressed() ile surekli tus durumu sorgulama
- Delta time (dt) ile kare hizindan bagimsiz hareket
- Dort yone bagimsiz hareket (capraz dahil)
- max/min ile ekran sinir kontrolu

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 2 - Klavye Girdileri

Calistirma: python 02_surekli_hareket.py
Gereksinimler: pygame
"""

import pygame

# Pencere sabitleri
GENISLIK = 800
YUKSEKLIK = 600
BASLIK = "Ok Tuslariyla Hareket"
ARKA_PLAN = (25, 25, 55)  # Koyu lacivert

# Nesne sabitleri
BOYUT = 40            # Kare boyutu (piksel)
RENK = (80, 150, 255) # Mavi
HIZ = 300             # piksel/saniye
FPS = 60


def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Nesnenin baslangic konumu (ekran ortasi)
    x = float(GENISLIK // 2 - BOYUT // 2)
    y = float(YUKSEKLIK // 2 - BOYUT // 2)

    print("Ok tuslari ile kareyi hareket ettirin.")
    print("ESC ile cikis yapabilirsiniz.")

    # Ana oyun dongusu
    calistir = True
    while calistir:
        # Delta time hesapla (saniye cinsinden)
        dt = saat.tick(FPS) / 1000.0

        # --- OLAY ISLEME ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- GUNCELLEME ---
        # Surekli tus durumunu sorgula
        tuslar = pygame.key.get_pressed()

        if tuslar[pygame.K_UP]:
            y -= HIZ * dt
        if tuslar[pygame.K_DOWN]:
            y += HIZ * dt
        if tuslar[pygame.K_LEFT]:
            x -= HIZ * dt
        if tuslar[pygame.K_RIGHT]:
            x += HIZ * dt

        # Ekran sinir kontrolu (clamp)
        x = max(0.0, min(x, float(GENISLIK - BOYUT)))
        y = max(0.0, min(y, float(YUKSEKLIK - BOYUT)))

        # --- CIZIM ---
        ekran.fill(ARKA_PLAN)
        pygame.draw.rect(ekran, RENK, (int(x), int(y), BOYUT, BOYUT))
        pygame.display.flip()

    # PyGame'i kapat
    pygame.quit()
    print("Program sonlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu lacivert bir pencere acilir.
Ekranin ortasinda 40x40 mavi bir kare goruntulenir.
Ok tuslariyla kare dort yone hareket eder:
  - Yukari ok: kare yukari gider
  - Asagi ok: kare asagi gider
  - Sol ok: kare sola gider
  - Sag ok: kare saga gider
  - Iki tus ayni anda: capraz hareket
Kare ekran kenarlarindan disari cikamaz.
ESC tusu ile program kapatilir.
"""
