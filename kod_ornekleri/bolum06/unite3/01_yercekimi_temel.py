"""
Temel Yercekimi Simulasyonu

Bir nesnenin yercekimi etkisiyle dusmesini ve zere carptiginda
durmasini gosteren basit bir ornek.

Ogrenilecek kavramlar:
- Yercekimi sabiti ve dikey hiz
- Her karede hiz guncelleme
- Zemin carpisma kontrolu

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 3 - Temel Fizik Simulasyonu

Calistirma: python 01_yercekimi_temel.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
ZEMIN_Y = 550
YERCEKIMI = 0.5


class DusenNesne(pygame.sprite.Sprite):
    """Yercekimine tabi dusen nesne."""

    def __init__(self, x, y, renk=(255, 100, 100)):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(renk)
        self.rect = self.image.get_rect(center=(x, y))

        # Fizik degiskenleri
        self.hiz_y = 0

    def update(self):
        # Yercekimi hizi etkiler
        self.hiz_y += YERCEKIMI

        # Konum guncellenir
        self.rect.y += self.hiz_y

        # Zemin kontrolu
        if self.rect.bottom >= ZEMIN_Y:
            self.rect.bottom = ZEMIN_Y
            self.hiz_y = 0


def main():
    """Ana fonksiyon."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Temel Yercekimi Simulasyonu")
    saat = pygame.time.Clock()

    # Farkli yuksekliklerden nesneler olustur
    nesneler = pygame.sprite.Group()
    nesneler.add(DusenNesne(200, 50, (255, 100, 100)))
    nesneler.add(DusenNesne(400, 150, (100, 255, 100)))
    nesneler.add(DusenNesne(600, 250, (100, 100, 255)))

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        nesneler.update()

        # Cizim
        ekran.fill((30, 30, 50))

        # Zemin cizgisi
        pygame.draw.line(ekran, (100, 100, 100),
                         (0, ZEMIN_Y), (GENISLIK, ZEMIN_Y), 2)

        nesneler.draw(ekran)
        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
Uc farkli renkte kare, farkli yuksekliklerden yercekimi etkisiyle
duser. Her biri baslagicta yavas, giderek hizlanarak duser.
Zemine ulastiklarinda dururlar.
"""
