"""
Kamera Sınırları - clamp ile Harita Dışına Taşma

Oyuncu haritanın köşelerine gittiğinde kameranın haritanın dışını
göstermesini engellemek için offset'i clamp (sınırlandırma) ederiz.

Öğrenilecek kavramlar:
- max(0, min(ofset, dunya_boyut - ekran_boyut))
- Dünya boyutu < ekran boyutu durumu
- Kenar (edge) takip davranışı

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 3 - Kamera ve Scrolling

Çalıştırma: python 03_kamera_clamp.py
Gereksinimler: pygame
"""

import pygame

GENISLIK = 800
YUKSEKLIK = 600
DUNYA_GEN = 1400
DUNYA_YUK = 900
TILE = 32


class Camera:
    def __init__(self, ekran_gen, ekran_yuk, dunya_gen, dunya_yuk, lerp=0.1):
        self.offset = pygame.Vector2(0, 0)
        self.ekran_gen = ekran_gen
        self.ekran_yuk = ekran_yuk
        self.dunya_gen = dunya_gen
        self.dunya_yuk = dunya_yuk
        self.lerp = lerp

    def apply(self, rect):
        return rect.move(-int(self.offset.x), -int(self.offset.y))

    def update(self, hedef_rect):
        istenen = pygame.Vector2(
            hedef_rect.centerx - self.ekran_gen // 2,
            hedef_rect.centery - self.ekran_yuk // 2,
        )
        self.offset += (istenen - self.offset) * self.lerp
        self._clamp()

    def _clamp(self):
        max_x = max(0, self.dunya_gen - self.ekran_gen)
        max_y = max(0, self.dunya_yuk - self.ekran_yuk)
        if self.offset.x < 0:
            self.offset.x = 0
        if self.offset.y < 0:
            self.offset.y = 0
        if self.offset.x > max_x:
            self.offset.x = max_x
        if self.offset.y > max_y:
            self.offset.y = max_y


def izgara_ciz(ekran, kamera):
    baslangic_x = -int(kamera.offset.x) % TILE
    baslangic_y = -int(kamera.offset.y) % TILE
    for x in range(baslangic_x, GENISLIK, TILE):
        pygame.draw.line(ekran, (50, 50, 80), (x, 0), (x, YUKSEKLIK))
    for y in range(baslangic_y, YUKSEKLIK, TILE):
        pygame.draw.line(ekran, (50, 50, 80), (0, y), (GENISLIK, y))


def dunya_sinirlari_ciz(ekran, kamera):
    """Dünyanın 4 kenarını renkli duvarlar olarak gösterir."""
    duvarlar = [
        pygame.Rect(0, 0, DUNYA_GEN, 8),
        pygame.Rect(0, DUNYA_YUK - 8, DUNYA_GEN, 8),
        pygame.Rect(0, 0, 8, DUNYA_YUK),
        pygame.Rect(DUNYA_GEN - 8, 0, 8, DUNYA_YUK),
    ]
    for d in duvarlar:
        pygame.draw.rect(ekran, (200, 60, 60), kamera.apply(d))


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Kamera Clamp")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    oyuncu = pygame.Rect(DUNYA_GEN // 2, DUNYA_YUK // 2, 32, 48)
    kamera = Camera(GENISLIK, YUKSEKLIK, DUNYA_GEN, DUNYA_YUK, lerp=0.12)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        tuslar = pygame.key.get_pressed()
        hiz = 5
        if tuslar[pygame.K_LEFT]:
            oyuncu.x -= hiz
        if tuslar[pygame.K_RIGHT]:
            oyuncu.x += hiz
        if tuslar[pygame.K_UP]:
            oyuncu.y -= hiz
        if tuslar[pygame.K_DOWN]:
            oyuncu.y += hiz

        # Oyuncuyu da dünya içinde tut
        oyuncu.clamp_ip(pygame.Rect(0, 0, DUNYA_GEN, DUNYA_YUK))

        kamera.update(oyuncu)

        ekran.fill((30, 30, 50))
        izgara_ciz(ekran, kamera)
        dunya_sinirlari_ciz(ekran, kamera)

        pygame.draw.rect(ekran, (220, 80, 80), kamera.apply(oyuncu))
        pygame.draw.rect(ekran, (255, 255, 255), kamera.apply(oyuncu), 2)

        ekran.blit(font.render(
            f"Oyuncu: ({oyuncu.x}, {oyuncu.y})",
            True, (255, 255, 255)), (10, 10))
        ekran.blit(font.render(
            f"Kamera offset: "
            f"({int(kamera.offset.x)}, {int(kamera.offset.y)})  "
            f"max: ({DUNYA_GEN - GENISLIK}, {DUNYA_YUK - YUKSEKLIK})",
            True, (255, 255, 255)), (10, 32))
        ekran.blit(font.render(
            "Oklar: hareket. Kırmızı kenarlar = dünya sınırları",
            True, (180, 180, 180)), (10, 54))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Kırmızı kenarlı dikdörtgen bir dünya içinde oyuncuyu hareket ettirirsin.
Oyuncu ortadayken kamera onu ortalar; dünya köşelerine gittiğinde kamera
sınırı aşmaz ve oyuncu ekranın köşe tarafında görünür.
"""
