"""
Temel Carpisma Kontrolu - colliderect() Ornegi

Bir oyuncu kutusunu ok tuslariyla hareket ettir ve
ekrandaki engelle carpisma kontrolu yap.

Ogrenilecek kavramlar:
- pygame.Rect olusturma ve hareket
- colliderect() ile carpisma kontrolu
- Gorsel geri bildirim (renk degisimi)

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 1 - Rect Sinifi ve Carpisma

Calistirma: python 01_temel_carpisma.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
EKRAN_GENISLIK = 800
EKRAN_YUKSEKLIK = 600
FPS = 60
OYUNCU_HIZ = 5

# Renkler
BEYAZ = (255, 255, 255)
MAVI = (50, 100, 200)
KIRMIZI = (200, 50, 50)
YESIL = (50, 200, 50)
GRI = (40, 40, 40)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
    pygame.display.set_caption("Temel Carpisma Kontrolu")
    saat = pygame.time.Clock()

    # Oyuncu ve engel Rect'leri olustur
    oyuncu = pygame.Rect(100, 300, 40, 40)
    engel = pygame.Rect(350, 250, 100, 100)

    calistir = True
    while calistir:
        # -- Olaylari isle --
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        # -- Guncelle --
        # Klavye ile hareket
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]:
            oyuncu.x -= OYUNCU_HIZ
        if tuslar[pygame.K_RIGHT]:
            oyuncu.x += OYUNCU_HIZ
        if tuslar[pygame.K_UP]:
            oyuncu.y -= OYUNCU_HIZ
        if tuslar[pygame.K_DOWN]:
            oyuncu.y += OYUNCU_HIZ

        # Ekran sinirlarinda tut
        ekran_rect = pygame.Rect(0, 0, EKRAN_GENISLIK, EKRAN_YUKSEKLIK)
        oyuncu.clamp_ip(ekran_rect)

        # Carpisma kontrolu
        carpisma_var = oyuncu.colliderect(engel)

        # -- Ciz --
        ekran.fill(GRI)

        # Engeli ciz (her zaman kirmizi)
        pygame.draw.rect(ekran, KIRMIZI, engel)

        # Oyuncuyu ciz (carpisma varsa yesil, yoksa mavi)
        if carpisma_var:
            oyuncu_renk = YESIL
        else:
            oyuncu_renk = MAVI
        pygame.draw.rect(ekran, oyuncu_renk, oyuncu)

        # Durum metni
        font = pygame.font.Font(None, 36)
        if carpisma_var:
            metin = font.render("CARPISMA!", True, YESIL)
        else:
            metin = font.render("Engele dogru hareket et", True, BEYAZ)
        ekran.blit(metin, (10, 10))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda bir pencere acilir.
Mavi bir kare ok tuslariyla hareket ettirilir.
Ortadaki kirmizi engele degdiginde mavi kare yesile doner
ve ekranda "CARPISMA!" yazisi belirir.
"""
