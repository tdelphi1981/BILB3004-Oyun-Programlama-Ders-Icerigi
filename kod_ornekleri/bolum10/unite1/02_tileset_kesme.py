"""
Tileset Kesme - subsurface() ile Frame Çıkarma

Bu program, tek bir PNG tileset'inden tek tek tile yüzeylerini
nasıl keseceğini öğretir. Gerçek bir sprite sheet olmadan demo için
programatik bir tileset (Surface üzerinde renkli kutular) oluştururuz.

Öğrenilecek kavramlar:
- pygame.Surface ile programatik tileset
- subsurface((x, y, w, h)) ile frame kesme
- Tileset'i 2B listeye (tiles[row][col]) çevirme
- Grid ID -> Surface eşleşmesi

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 1 - Tile Sistemi Temelleri

Çalıştırma: python 02_tileset_kesme.py
Gereksinimler: pygame
"""

import pygame

TILE = 32
TILESET_SUTUN = 4
TILESET_SATIR = 2


def tileset_olustur():
    """Programatik olarak 4x2 tile içeren bir tileset Surface'i üretir."""
    yuzeyi = pygame.Surface((TILE * TILESET_SUTUN, TILE * TILESET_SATIR))
    renkler = [
        (80, 180, 80),   # çim
        (120, 120, 120), # taş
        (60, 120, 220),  # su
        (200, 160, 80),  # kum
        (140, 80, 40),   # topraksı
        (60, 60, 60),    # asfalt
        (200, 60, 60),   # tuğla
        (240, 230, 140), # altın
    ]
    for i, renk in enumerate(renkler):
        col = i % TILESET_SUTUN
        row = i // TILESET_SUTUN
        pygame.draw.rect(yuzeyi, renk, (col * TILE, row * TILE, TILE, TILE))
        pygame.draw.rect(yuzeyi, (0, 0, 0),
                         (col * TILE, row * TILE, TILE, TILE), 1)
    return yuzeyi


def tileset_parcala(tileset):
    """Tileset Surface'ini tek tek Surface'lere böler ve listede döndürür.

    Dönüş: tiles[id] = Surface
    """
    tiles = []
    for row in range(TILESET_SATIR):
        for col in range(TILESET_SUTUN):
            rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
            # subsurface: ana Surface'in bir bölümüne referans veren Surface
            tiles.append(tileset.subsurface(rect))
    return tiles


def main():
    pygame.init()
    ekran = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Tileset Kesme Demo")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    # Programatik tileset
    tileset = tileset_olustur()

    # Tileset'i kes
    tiles = tileset_parcala(tileset)
    print(f"[OK] Tileset parçalandı: {len(tiles)} tile")

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        ekran.fill((30, 30, 50))

        # Sol: Orijinal tileset (2x büyütülmüş)
        buyuk = pygame.transform.scale(
            tileset, (TILESET_SUTUN * TILE * 2, TILESET_SATIR * TILE * 2)
        )
        ekran.blit(buyuk, (20, 60))
        ekran.blit(font.render("Tileset (orijinal)", True, (255, 255, 255)),
                   (20, 30))

        # Sağ: Her bir kesilmiş tile (ID ile)
        ekran.blit(font.render("Kesilen Tile'lar (ID)", True, (255, 255, 255)),
                   (320, 30))
        for i, tile in enumerate(tiles):
            x = 320 + (i % 4) * (TILE + 10)
            y = 60 + (i // 4) * (TILE + 24)
            buyutulmus = pygame.transform.scale(tile, (TILE * 2, TILE * 2))
            ekran.blit(buyutulmus, (x, y))
            id_metin = font.render(str(i), True, (255, 255, 0))
            ekran.blit(id_metin, (x + TILE, y + TILE * 2 + 2))

        # Açıklama
        aciklama = [
            "subsurface((x, y, w, h)) ile tileset'ten tek tile kesilir.",
            "Her kesim orijinal Surface'in bir bölümüne referanstır.",
            "tiles[id] erişimi ile haritayı çizerken kullanılır.",
        ]
        for i, metin in enumerate(aciklama):
            ekran.blit(font.render(metin, True, (200, 200, 200)),
                       (20, 360 + i * 22))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
Sol tarafta orijinal 4x2 tileset görülür. Sağ tarafta ise
subsurface ile kesilmiş 8 tile ID numaralarıyla birlikte listelenir.
Terminalde "[OK] Tileset parçalandı: 8 tile" yazısı görünür.
"""
