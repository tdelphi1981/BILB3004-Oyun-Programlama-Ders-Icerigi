"""
Yilan Oyunu (Snake) - Tam Oyun

Klasik Snake oyununun PyGame ile uygulamasi. Izgara tabanli
hareket sistemi, yem toplama, buyume mekanigi ve carpma
kontrolu icerir. Bu proje, Bolum 4'te ogrenilen tum
kavramlari (olay sistemi, klavye girdisi, hareket mekanigi,
sinir kontrolu) birlestirir.

Ogrenilecek kavramlar:
- Izgara tabanli (grid-based) hareket
- KEYDOWN olayi ile ayrik yon degistirme
- Liste veri yapisi ile yilan govdesi yonetimi
- random modulu ile yem olusturma
- Carpma algilama (duvar + kendine)
- pygame.font ile skor gosterimi (temel kullanim)
- Game Over ve yeniden baslatma

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 4 - Hareket Mekanigi

Calistirma: python 03_yilan_oyunu.py
Gereksinimler: pygame

Kontroller:
- Ok tuslari: Yon degistir
- R: Yeniden basla (Game Over sonrasi)
- ESC: Cikis
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


def oyunu_sifirla():
    """Oyun durumunu baslangic degerlerine dondur."""
    baslangic_x = IZGARA_GENISLIK // 2
    baslangic_y = IZGARA_YUKSEKLIK // 2
    yilan = [
        (baslangic_x, baslangic_y),
        (baslangic_x - 1, baslangic_y),
        (baslangic_x - 2, baslangic_y),
    ]
    yon = SAG
    skor = 0
    yem = yem_olustur(yilan)
    oyun_bitti = False
    return yilan, yon, skor, yem, oyun_bitti


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Yilan Oyunu")
    saat = pygame.time.Clock()

    # Font nesneleri
    # Not: pygame.font detayli kullanimi Bolum 9'da anlatilacak
    font = pygame.font.Font(None, 28)
    buyuk_font = pygame.font.Font(None, 48)

    # Oyunu baslat
    yilan, yon, skor, yem, oyun_bitti = oyunu_sifirla()

    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olaylari isle ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                # Cikis
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                # Oyun bittiyse yeniden basla
                if oyun_bitti:
                    if olay.key == pygame.K_r:
                        yilan, yon, skor, yem, oyun_bitti = oyunu_sifirla()
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
            # Yeni bas konumunu hesapla
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
                # Basi ekle
                yilan.insert(0, yeni_bas)

                # Yem kontrolu
                if yeni_bas == yem:
                    # Yem yedi: kuyruk silinmez -> yilan buyur
                    skor += 1
                    yem = yem_olustur(yilan)
                else:
                    # Yem yemedi: kuyrugu sil -> ayni uzunluk
                    yilan.pop()

        # --- Ciz ---
        ekran.fill(SIYAH)
        izgara_ciz(ekran)

        # Yemi ciz
        hucre_ciz(ekran, yem, KIRMIZI, (255, 100, 100))

        # Yilani ciz
        for i, parca in enumerate(yilan):
            if i == 0:
                # Bas koyu yesil
                hucre_ciz(ekran, parca, KOYU_YESIL, YESIL)
            else:
                # Govde yesil tonlari
                hucre_ciz(ekran, parca, YESIL, KOYU_YESIL)

        # Skoru goster
        skor_yazi = font.render(f"Skor: {skor}", True, BEYAZ)
        ekran.blit(skor_yazi, (10, 10))

        # Yilan uzunlugu goster
        uzunluk_yazi = font.render(
            f"Uzunluk: {len(yilan)}", True, GRI
        )
        ekran.blit(uzunluk_yazi, (GENISLIK - 150, 10))

        # Game Over ekrani
        if oyun_bitti:
            # Yari saydam siyah katman
            katman = pygame.Surface((GENISLIK, YUKSEKLIK))
            katman.set_alpha(150)
            katman.fill(SIYAH)
            ekran.blit(katman, (0, 0))

            # GAME OVER yazisi
            go_yazi = buyuk_font.render("GAME OVER", True, KIRMIZI)
            go_rect = go_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 - 20)
            )
            ekran.blit(go_yazi, go_rect)

            # Skor bilgisi
            skor_bilgi = font.render(
                f"Skor: {skor} | Uzunluk: {len(yilan)}", True, BEYAZ
            )
            skor_rect = skor_bilgi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 + 20)
            )
            ekran.blit(skor_bilgi, skor_rect)

            # Yeniden baslatma bilgisi
            tekrar_yazi = font.render(
                "R: Tekrar | ESC: Cikis", True, GRI
            )
            tekrar_rect = tekrar_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 + 55)
            )
            ekran.blit(tekrar_yazi, tekrar_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
600x400 piksel boyutunda siyah bir pencere acilir.
Arka planda hafif bir izgara gosterilir.
Yesil bir yilan (3 hucre) ekranin ortasindan saga dogru hareket eder.
Rastgele bir konumda kirmizi yem goruntulenir.

Kontroller:
- Ok tuslari ile yilanin yonunu degistir
- Yem yediginde yilan bir hucre buyur ve skor artar
- Duvara veya kendi govdesine carparsa oyun biter
- Game Over ekraninda R ile yeniden basla
- ESC ile programi kapat

Sol ust kosede skor, sag ust kosede yilan uzunlugu gosterilir.
"""
