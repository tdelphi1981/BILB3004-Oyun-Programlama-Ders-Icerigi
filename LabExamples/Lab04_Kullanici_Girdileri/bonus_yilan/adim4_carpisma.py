"""
Yilan Oyunu - Adim 4: Carpma Kontrolu

Duvar ve kendine carpma kontrolu ekler. Wrap-around
kaldirilir; yilan duvara veya kendi govdesine carparsa
oyun durur (basit cikis).

Ogrenilecek kavramlar:
- Sinir kontrolu (duvar carpmasi)
- Kendine carpma algilama
- Oyun durumu yonetimi (oyun_bitti)

Bolum: 04 - Kullanici Girdileri ve Hareket
Lab: 04 - Bonus: Yilan Oyunu (Adim 4/6)

Calistirma: uv run python adim4_carpisma.py
Gereksinimler: pygame
"""

import pygame
import random

# --- Sabitler ---
HUCRE_BOYUTU = 20
IZGARA_GENISLIK = 30    # 30 hucre yatay
IZGARA_YUKSEKLIK = 20   # 20 hucre dikey
GENISLIK = IZGARA_GENISLIK * HUCRE_BOYUTU    # 600 piksel
YUKSEKLIK = IZGARA_YUKSEKLIK * HUCRE_BOYUTU  # 400 piksel
FPS = 10  # Yilan hizi (kare/saniye)

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
YESIL = (0, 200, 0)
KOYU_YESIL = (0, 140, 0)
KIRMIZI = (220, 50, 50)
GRI = (40, 40, 40)
KOYU_GRI = (25, 25, 25)

# Yon sabitleri (izgara birimleri)
YUKARI = (0, -1)
ASAGI = (0, 1)
SOL = (-1, 0)
SAG = (1, 0)


def yem_olustur(yilan):
    """Yilanin uzerinde olmayan rastgele bir konum sec."""
    while True:
        konum = (
            random.randint(0, IZGARA_GENISLIK - 1),
            random.randint(0, IZGARA_YUKSEKLIK - 1)
        )
        if konum not in yilan:
            return konum


def izgara_ciz(ekran):
    """Arka plana hafif izgara cizgileri ciz."""
    for x in range(0, GENISLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, KOYU_GRI, (x, 0), (x, YUKSEKLIK))
    for y in range(0, YUKSEKLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, KOYU_GRI, (0, y), (GENISLIK, y))


def hucre_ciz(ekran, konum, renk, ic_renk=None):
    """Izgara konumundaki bir hucreyi ciz."""
    x = konum[0] * HUCRE_BOYUTU
    y = konum[1] * HUCRE_BOYUTU
    # Dis cerceve
    pygame.draw.rect(ekran, renk, (x, y, HUCRE_BOYUTU, HUCRE_BOYUTU))
    # Ic renk (kenarligi belli etmek icin)
    if ic_renk:
        pygame.draw.rect(
            ekran, ic_renk,
            (x + 2, y + 2, HUCRE_BOYUTU - 4, HUCRE_BOYUTU - 4)
        )


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Yilan Oyunu - Adim 4")
    saat = pygame.time.Clock()

    # Yilan baslangic durumu
    baslangic_x = IZGARA_GENISLIK // 2
    baslangic_y = IZGARA_YUKSEKLIK // 2
    yilan = [
        (baslangic_x, baslangic_y),
        (baslangic_x - 1, baslangic_y),
        (baslangic_x - 2, baslangic_y),
    ]
    yon = SAG
    yem = yem_olustur(yilan)
    oyun_bitti = False

    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olaylari isle ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                if oyun_bitti:
                    continue
                # Yon degistir (ters yone donmeyi engelle)
                if olay.key == pygame.K_UP and yon != ASAGI:
                    yon = YUKARI
                elif olay.key == pygame.K_DOWN and yon != YUKARI:
                    yon = ASAGI
                elif olay.key == pygame.K_LEFT and yon != SAG:
                    yon = SOL
                elif olay.key == pygame.K_RIGHT and yon != SOL:
                    yon = SAG

        # --- Guncelle ---
        if not oyun_bitti:
            bas_x, bas_y = yilan[0]
            yeni_bas = (bas_x + yon[0], bas_y + yon[1])

            # Duvar carpismasi kontrolu
            yb_x, yb_y = yeni_bas
            if yb_x < 0 or yb_x >= IZGARA_GENISLIK:
                oyun_bitti = True
            elif yb_y < 0 or yb_y >= IZGARA_YUKSEKLIK:
                oyun_bitti = True
            # Kendine carpma kontrolu
            elif yeni_bas in yilan:
                oyun_bitti = True

            if not oyun_bitti:
                yilan.insert(0, yeni_bas)

                # Yem kontrolu
                if yeni_bas == yem:
                    yem = yem_olustur(yilan)
                else:
                    yilan.pop()

        # --- Ciz ---
        ekran.fill(SIYAH)
        izgara_ciz(ekran)

        # Yemi ciz
        hucre_ciz(ekran, yem, KIRMIZI, (255, 100, 100))

        # Yilani ciz
        for i, parca in enumerate(yilan):
            if i == 0:
                hucre_ciz(ekran, parca, KOYU_YESIL, YESIL)
            else:
                hucre_ciz(ekran, parca, YESIL, KOYU_YESIL)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
600x400 piksel boyutunda siyah bir pencere acilir.
Yesil bir yilan (3 hucre) ekranin ortasindan saga dogru hareket eder.
Rastgele bir konumda kirmizi yem goruntulenir.
Yilan yemi yediginde buyur ve yeni yem belirir.
Yilan duvara veya kendi govdesine carparsa oyun durur.
ESC ile program kapanir.
"""
