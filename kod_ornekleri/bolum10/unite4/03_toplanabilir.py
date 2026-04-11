"""
Toplanabilir Tile'lar - Altın ve Anahtar

Bu program, harita üzerine yerleştirilmiş altın ve anahtar tile'larını
toplamayı gösterir. Toplanan tile listeden çıkarılır ve skor/envanter
HUD'da güncellenir.

Öğrenilecek kavramlar:
- Haritadan dinamik tile çıkarma
- Skor ve envanter yönetimi
- Tile türü -> davranış eşlemesi

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 4 - Seviye Tasarımı

Çalıştırma: python 03_toplanabilir.py
Gereksinimler: pygame
"""

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480

# 2 = solid, A = altın, K = anahtar
HARITA = [
    "                    ",
    "                    ",
    "   A   A     A    A ",
    "  22  22    222   22",
    "                    ",
    "       K            ",
    "      22         A  ",
    "                 22 ",
    " A                  ",
    "222       A         ",
    "          22        ",
    "              K     ",
    "              22    ",
    "22222222222222222222",
    "22222222222222222222",
]


def tile_listelerini_cikar(harita):
    katilar = []
    altinlar = []  # list of Rect
    anahtarlar = []
    for r, satir in enumerate(harita):
        for c, ch in enumerate(satir):
            rect = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
            if ch == "2":
                katilar.append(rect)
            elif ch == "A":
                altinlar.append(rect)
            elif ch == "K":
                anahtarlar.append(rect)
    return katilar, altinlar, anahtarlar


class Oyuncu:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0
        self.vy = 0
        self.yerde = False

    def guncelle(self, tuslar, katilar):
        self.vx = 0
        if tuslar[pygame.K_LEFT]:
            self.vx = -3
        if tuslar[pygame.K_RIGHT]:
            self.vx = 3
        self.rect.x += self.vx
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vx > 0:
                    self.rect.right = k.left
                elif self.vx < 0:
                    self.rect.left = k.right

        self.vy += 0.5
        self.rect.y += int(self.vy)
        self.yerde = False
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vy > 0:
                    self.rect.bottom = k.top
                    self.yerde = True
                elif self.vy < 0:
                    self.rect.top = k.bottom
                self.vy = 0

    def zipla(self):
        if self.yerde:
            self.vy = -10


def altin_ciz(ekran, altinlar):
    for a in altinlar:
        merkez = a.center
        pygame.draw.circle(ekran, (240, 200, 60), merkez, 10)
        pygame.draw.circle(ekran, (255, 240, 120), merkez, 10, 2)


def anahtar_ciz(ekran, anahtarlar):
    for a in anahtarlar:
        merkez = a.center
        pygame.draw.circle(ekran, (200, 200, 220), merkez, 8)
        pygame.draw.rect(
            ekran, (200, 200, 220),
            (merkez[0] - 2, merkez[1], 4, 14),
        )


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Toplanabilir Tile'lar")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    katilar, altinlar, anahtarlar = tile_listelerini_cikar(HARITA)
    oyuncu = Oyuncu(80, 200)
    skor = 0
    anahtar_sayisi = 0

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP):
                    oyuncu.zipla()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)

        # Altın topla
        for a in altinlar[:]:
            if oyuncu.rect.colliderect(a):
                altinlar.remove(a)
                skor += 10
        # Anahtar topla
        for a in anahtarlar[:]:
            if oyuncu.rect.colliderect(a):
                anahtarlar.remove(a)
                anahtar_sayisi += 1

        ekran.fill((30, 30, 60))
        for k in katilar:
            pygame.draw.rect(ekran, (120, 120, 120), k)
            pygame.draw.rect(ekran, (80, 80, 80), k, 2)
        altin_ciz(ekran, altinlar)
        anahtar_ciz(ekran, anahtarlar)

        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)
        pygame.draw.rect(ekran, (255, 255, 255), oyuncu.rect, 2)

        ekran.blit(font.render(f"[ALTIN] {skor}", True, (255, 215, 0)), (10, 10))
        ekran.blit(font.render(f"Anahtar: {anahtar_sayisi}",
                               True, (200, 200, 220)), (10, 36))

        if not altinlar and not anahtarlar:
            mesaj = font.render("Tüm eşyalar toplandı!",
                                True, (120, 255, 120))
            ekran.blit(mesaj, mesaj.get_rect(center=(GENISLIK // 2, 60)))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Haritada altın diskler ve anahtar nesneleri bulunur. Oyuncu bunlara
dokunduğunda toplanır, HUD'da skor ve anahtar sayısı artar. Tüm
eşyalar toplandığında ekrana "Tüm eşyalar toplandı!" yazısı çıkar.
"""
