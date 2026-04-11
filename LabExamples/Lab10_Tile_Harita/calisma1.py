"""
Lab 10 - Çalışma 1 Başlangıç Kodu
İlk Tile Haritası

Bu dosya Lab 10 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- 2B liste ile harita temsili
- Tile ID -> renk eşlemesi
- İç içe for döngüsü ile tile çizimi

Lab: 10 - Tile-Based Oyun Dünyası
Çalışma: 1 - İlk Tile Haritası

Çalıştırma: uv run python calisma1.py
"""

import pygame

TILE = 32

# GOREV 1: Yeni tile ID ekle (4 = kum, açık kahverengi)
RENKLER = {
    0: (30, 30, 50),     # boş
    1: (80, 180, 80),    # çim
    2: (120, 120, 120),  # taş
    3: (60, 120, 220),   # su
    # 4: (???, ???, ???),  # kum - buraya ekle
}

HARITA = [
    [2] * 20,
    [2] + [1] * 18 + [2],
    [2] + [1, 1, 2, 2, 2] + [1] * 13 + [2],
    [2] + [1] * 7 + [3, 3, 3, 3] + [1] * 7 + [2],
    [2] + [1] * 7 + [3, 3, 3, 3] + [1] * 7 + [2],
    [2] + [1] * 18 + [2],
    [2] * 20,
]


def tile_sayaclari(harita):
    """Her tile ID'sinin kaç kere kullanıldığını sayar.

    GOREV 2: Bu fonksiyonu tamamla.
    Dönüş: dict - {tile_id: sayı}
    Örnek: {0: 0, 1: 112, 2: 68, 3: 8}
    """
    sayaclar = {}
    # ... buraya kodu yaz
    return sayaclar


def main():
    pygame.init()
    ekran = pygame.display.set_mode((20 * TILE, 7 * TILE))
    pygame.display.set_caption("Lab 10 - Çalışma 1")
    saat = pygame.time.Clock()

    # Başlangıçta sayaçları yazdır (GOREV 2)
    print("Tile sayaçları:", tile_sayaclari(HARITA))

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        for r, satir in enumerate(HARITA):
            for c, tid in enumerate(satir):
                renk = RENKLER.get(tid, (0, 0, 0))
                pygame.draw.rect(ekran, renk,
                                 (c * TILE, r * TILE, TILE, TILE))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
