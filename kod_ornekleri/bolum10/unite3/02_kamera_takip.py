"""
Kamera Sınıfı ve Oyuncu Takibi (Lerp)

Bu program bir Camera sınıfı oluşturur, oyuncu ekran ortasında kalacak
şekilde kamerayı günceller ve yumuşak takip için lerp (linear interpolation)
kullanır.

Öğrenilecek kavramlar:
- Camera sınıfı: offset, apply(), update(target)
- Lerp: yeni = eski + (hedef - eski) * faktor
- Oyuncu merkezli takip: offset = oyuncu.center - ekran_merkez

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 3 - Kamera ve Scrolling

Çalıştırma: python 02_kamera_takip.py
Gereksinimler: pygame
"""

import pygame

GENISLIK = 800
YUKSEKLIK = 600
DUNYA_GEN = 2000
DUNYA_YUK = 1500
TILE = 32


class Camera:
    """Oyuncuyu takip eden basit bir 2B kamera."""

    def __init__(self, gen, yuk, lerp=0.1):
        self.offset = pygame.Vector2(0, 0)
        self.gen = gen
        self.yuk = yuk
        self.lerp = lerp

    def apply(self, rect):
        """Dünyadaki rect'i ekran koordinatına çevirir."""
        return rect.move(-int(self.offset.x), -int(self.offset.y))

    def apply_point(self, x, y):
        return x - int(self.offset.x), y - int(self.offset.y)

    def update(self, hedef_rect):
        """Hedefi ekran merkezine doğru yumuşak takip eder."""
        istenen = pygame.Vector2(
            hedef_rect.centerx - self.gen // 2,
            hedef_rect.centery - self.yuk // 2,
        )
        self.offset += (istenen - self.offset) * self.lerp


class Oyuncu:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.hiz = 4

    def guncelle(self, tuslar):
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += self.hiz
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            self.rect.y -= self.hiz
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            self.rect.y += self.hiz


def izgara_ciz(ekran, kamera):
    """Dünya üzerindeki sonsuz görünümlü bir referans izgara çizer."""
    baslangic_x = -int(kamera.offset.x) % TILE
    baslangic_y = -int(kamera.offset.y) % TILE
    for x in range(baslangic_x, GENISLIK, TILE):
        pygame.draw.line(ekran, (50, 50, 80), (x, 0), (x, YUKSEKLIK))
    for y in range(baslangic_y, YUKSEKLIK, TILE):
        pygame.draw.line(ekran, (50, 50, 80), (0, y), (GENISLIK, y))


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Kamera Takibi (Lerp)")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    oyuncu = Oyuncu(DUNYA_GEN // 2, DUNYA_YUK // 2)
    kamera = Camera(GENISLIK, YUKSEKLIK, lerp=0.08)

    # Dünyada referans kutular
    nesneler = [
        pygame.Rect(200, 200, 80, 80),
        pygame.Rect(600, 400, 120, 60),
        pygame.Rect(1200, 700, 200, 80),
        pygame.Rect(1600, 200, 100, 100),
        pygame.Rect(400, 1100, 80, 120),
    ]

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        oyuncu.guncelle(pygame.key.get_pressed())
        kamera.update(oyuncu.rect)

        ekran.fill((30, 30, 50))
        izgara_ciz(ekran, kamera)

        for n in nesneler:
            cizim = kamera.apply(n)
            pygame.draw.rect(ekran, (80, 180, 80), cizim)
            pygame.draw.rect(ekran, (255, 255, 255), cizim, 2)

        # Oyuncu
        pygame.draw.rect(ekran, (220, 80, 80), kamera.apply(oyuncu.rect))
        pygame.draw.rect(ekran, (255, 255, 255), kamera.apply(oyuncu.rect), 2)

        # HUD
        ekran.blit(font.render(
            f"Oyuncu (world): ({oyuncu.rect.x}, {oyuncu.rect.y})",
            True, (255, 255, 255)), (10, 10))
        ekran.blit(font.render(
            f"Kamera offset: ({int(kamera.offset.x)}, {int(kamera.offset.y)})",
            True, (255, 255, 255)), (10, 32))
        ekran.blit(font.render(
            "Oklar / WASD: hareket (lerp faktörü = 0.08)",
            True, (180, 180, 180)), (10, 54))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Ekran ortasında kırmızı bir oyuncu kutusu; etrafında yeşil referans
kutuları ve kaydırılabilen bir izgara. Oyuncu hareket ettikçe kamera
yumuşak bir takip yapar (anlık değil), oyuncu her zaman ekran ortasına
çekilir.
"""
