"""
Fare Tiklama ile Buton - collidepoint() Ornegi

Bir buton olustur, fare ile uzerine gelince renk degissin
ve tiklaninca mesaj yazdirilsin.

Ogrenilecek kavramlar:
- collidepoint() ile nokta-dikdortgen kontrolu
- Fare tiklama algilama
- Hover efekti (fare uzerine gelme)

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 1 - Rect Sinifi ve Carpisma

Calistirma: python 02_buton_tiklama.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
EKRAN_GENISLIK = 800
EKRAN_YUKSEKLIK = 600
FPS = 60

# Renkler
BEYAZ = (255, 255, 255)
GRI = (40, 40, 40)
BUTON_NORMAL = (50, 150, 50)
BUTON_HOVER = (100, 200, 100)
BUTON_TIKLANDI = (200, 250, 50)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
    pygame.display.set_caption("Buton Tiklama Ornegi")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    kucuk_font = pygame.font.Font(None, 28)

    # Buton Rect'i
    buton_rect = pygame.Rect(300, 250, 200, 60)
    buton_renk = BUTON_NORMAL
    tiklama_sayisi = 0
    son_mesaj = "Butona tikla!"

    calistir = True
    while calistir:
        # -- Olaylari isle --
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            # Fare tiklama kontrolu
            if olay.type == pygame.MOUSEBUTTONDOWN:
                if buton_rect.collidepoint(olay.pos):
                    tiklama_sayisi += 1
                    son_mesaj = f"Tiklama sayisi: {tiklama_sayisi}"

        # -- Guncelle --
        # Hover kontrolu
        fare_pos = pygame.mouse.get_pos()
        if buton_rect.collidepoint(fare_pos):
            # Fare tikli mi kontrol et
            if pygame.mouse.get_pressed()[0]:
                buton_renk = BUTON_TIKLANDI
            else:
                buton_renk = BUTON_HOVER
        else:
            buton_renk = BUTON_NORMAL

        # -- Ciz --
        ekran.fill(GRI)

        # Butonu ciz
        pygame.draw.rect(ekran, buton_renk, buton_rect, border_radius=8)
        pygame.draw.rect(ekran, BEYAZ, buton_rect, 2, border_radius=8)

        # Buton yazisi
        buton_yazi = font.render("Tikla!", True, BEYAZ)
        yazi_rect = buton_yazi.get_rect(center=buton_rect.center)
        ekran.blit(buton_yazi, yazi_rect)

        # Durum mesaji
        mesaj = kucuk_font.render(son_mesaj, True, BEYAZ)
        ekran.blit(mesaj, (10, 10))

        # Fare konumu bilgisi
        konum_yazi = kucuk_font.render(
            f"Fare: {fare_pos}", True, (150, 150, 150)
        )
        ekran.blit(konum_yazi, (10, EKRAN_YUKSEKLIK - 30))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda bir pencere acilir.
Ortada yuvarlak koseli yesil bir buton bulunur.
Fare butonun uzerine gelince renk degisir (hover efekti).
Butona tiklandiginda tiklama sayaci artar.
"""
