"""
Kamera Temeli - World-Space vs Screen-Space

Bu program, dünya koordinatları (harita üzerindeki gerçek konum) ile
ekran koordinatları (ekranda çizilen konum) arasındaki farkı gösterir.
Klavye oklarıyla "kamera" offsetini elle değiştirirsin; dünyadaki
sabit nesneler ekranda hareket ediyor gibi gözükür.

Öğrenilecek kavramlar:
- world_x, world_y: dünyadaki sabit konum
- offset_x, offset_y: kamera kayması
- ekran_konum = dunya_konum - offset

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 3 - Kamera ve Scrolling

Çalıştırma: python 01_kamera_temel.py
Gereksinimler: pygame
"""

import pygame

GENISLIK = 800
YUKSEKLIK = 600


class Kutu:
    """Dünyada sabit bir renkli kutu."""

    def __init__(self, x, y, gen, yuk, renk):
        self.rect = pygame.Rect(x, y, gen, yuk)
        self.renk = renk

    def ciz(self, ekran, offset):
        cizim = self.rect.move(-offset[0], -offset[1])
        pygame.draw.rect(ekran, self.renk, cizim)
        pygame.draw.rect(ekran, (255, 255, 255), cizim, 2)


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Kamera Temeli")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    # Dünyada sabit nesneler
    nesneler = [
        Kutu(100, 100, 120, 80, (200, 80, 80)),
        Kutu(400, 300, 100, 100, (80, 200, 80)),
        Kutu(800, 150, 150, 150, (80, 80, 200)),
        Kutu(1200, 500, 100, 120, (220, 200, 60)),
        Kutu(200, 700, 200, 80, (200, 120, 200)),
    ]

    kamera_x, kamera_y = 0, 0
    hiz = 5

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]:
            kamera_x -= hiz
        if tuslar[pygame.K_RIGHT]:
            kamera_x += hiz
        if tuslar[pygame.K_UP]:
            kamera_y -= hiz
        if tuslar[pygame.K_DOWN]:
            kamera_y += hiz

        ekran.fill((30, 30, 50))
        for n in nesneler:
            n.ciz(ekran, (kamera_x, kamera_y))

        # Ekran merkezi işaretleyici (kamerayla hareket etmez, HUD)
        pygame.draw.line(ekran, (255, 255, 0),
                         (GENISLIK // 2 - 10, YUKSEKLIK // 2),
                         (GENISLIK // 2 + 10, YUKSEKLIK // 2))
        pygame.draw.line(ekran, (255, 255, 0),
                         (GENISLIK // 2, YUKSEKLIK // 2 - 10),
                         (GENISLIK // 2, YUKSEKLIK // 2 + 10))

        # HUD
        ekran.blit(font.render(
            f"Kamera (world offset): ({kamera_x}, {kamera_y})",
            True, (255, 255, 255)), (10, 10))
        ekran.blit(font.render(
            "Ok tuşları: kamerayı hareket ettir",
            True, (180, 180, 180)), (10, 34))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Ok tuşlarıyla kamera offsetini değiştirebileceğin bir pencere açılır.
Kutular dünyada sabit dursa da ekrandaki konumları kamerayla ters yönde
hareket eder (örnek: kamera sağa giderse kutular sola kayar).
"""
