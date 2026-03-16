"""
Ziplama Mekanigi

Yercekimi ve ziplama mekanigini birlestiren bir karakter kontrolu
ornegi. Bosluk tusu ile ziplama, ok tuslari ile yatay hareket.

Ogrenilecek kavramlar:
- Ziplama gucu (negatif dikey hiz)
- Yerde mi kontrolu
- Cift ziplama korumasi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 3 - Temel Fizik Simulasyonu

Calistirma: python 02_ziplama_mekanigi.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
ZEMIN_Y = 550
YERCEKIMI = 0.5
ZIPLAMA_GUCU = -12
HIZ = 5


class ZiplayanKarakter(pygame.sprite.Sprite):
    """Ziplama yapabilen karakter."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((100, 200, 100))
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.hiz_x = 0
        self.hiz_y = 0
        self.yerde_mi = False

    def zipla(self):
        """Sadece yerdeyken ziplama yapar."""
        if self.yerde_mi:
            self.hiz_y = ZIPLAMA_GUCU
            self.yerde_mi = False

    def update(self):
        # Klavye girdisi
        tuslar = pygame.key.get_pressed()
        self.hiz_x = 0

        if tuslar[pygame.K_RIGHT]:
            self.hiz_x = HIZ
        elif tuslar[pygame.K_LEFT]:
            self.hiz_x = -HIZ

        # Yercekimi
        self.hiz_y += YERCEKIMI

        # Konum guncelle
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Zemin kontrolu
        if self.rect.bottom >= ZEMIN_Y:
            self.rect.bottom = ZEMIN_Y
            self.hiz_y = 0
            self.yerde_mi = True

        # Ekran sinir kontrolu
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > GENISLIK:
            self.rect.right = GENISLIK


def main():
    """Ana fonksiyon."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Ziplama Mekanigi")
    saat = pygame.time.Clock()

    karakter = ZiplayanKarakter(400, ZEMIN_Y)
    tum_nesneler = pygame.sprite.Group(karakter)

    # Bilgi fontu
    font = pygame.font.Font(None, 28)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_SPACE:
                    karakter.zipla()

        tum_nesneler.update()

        # Cizim
        ekran.fill((30, 30, 50))

        # Zemin
        pygame.draw.line(ekran, (100, 100, 100),
                         (0, ZEMIN_Y), (GENISLIK, ZEMIN_Y), 2)

        tum_nesneler.draw(ekran)

        # Bilgi metni
        durum = "Yerde" if karakter.yerde_mi else "Havada"
        bilgi = font.render(
            f"Hiz Y: {karakter.hiz_y:.1f} | Durum: {durum}",
            True, (200, 200, 200)
        )
        ekran.blit(bilgi, (10, 10))

        kontrol = font.render(
            "Ok Tuslari: Hareket | Bosluk: Zipla",
            True, (150, 150, 150)
        )
        ekran.blit(kontrol, (10, 40))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
Yesil bir dikdortgen karakter zemin uzerinde durur.
Ok tuslari ile saga/sola hareket eder.
Bosluk tusu ile ziplar ve yercekimi etkisiyle yere doner.
Havadayken tekrar ziplama yapilamaz.
Ekranin ust kisminda hiz ve durum bilgisi gosterilir.
"""
