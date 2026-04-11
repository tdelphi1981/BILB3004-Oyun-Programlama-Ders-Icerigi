"""
pytmx ile Tiled (.tmx) Harita Yükleme

Bu program, Tiled editöründe hazırlanmış bir .tmx dosyasını pytmx
kütüphanesi ile yükler ve tüm katmanları ekrana çizer.

pytmx kurulu değilse otomatik olarak minimal bir XML parser'a düşer,
böylece örnek her ortamda çalışır.

Öğrenilecek kavramlar:
- pytmx.load_pygame(...) ile harita yükleme
- tmx_data.visible_layers ile katman iterasyonu
- tmx_data.width / tmx_data.tilewidth
- layer.tiles() ile (x, y, image) tuple'ı

Bölüm: 10 - Tile-Based Oyun Dünyası
Ünite: 2 - Harita Oluşturma

Çalıştırma: python 03_pytmx_yukleme.py
Gereksinimler: pygame (opsiyonel: pytmx)
"""

import xml.etree.ElementTree as ET
from pathlib import Path

import pygame

try:
    import pytmx
    PYTMX_VAR = True
except ImportError:
    PYTMX_VAR = False

# pytmx kurulu değilse kullanılacak renk paleti (gid -> renk)
YEDEK_RENKLER = {
    0: (0, 0, 0),
    1: (80, 180, 80),    # çim
    2: (140, 80, 40),    # topraksı
    3: (120, 120, 120),  # taş
    4: (60, 120, 220),   # su
    5: (200, 160, 80),   # kum
    6: (60, 60, 60),     # asfalt
    7: (200, 60, 60),    # tuğla
    8: (240, 230, 140),  # altın
}


def yedek_yukle(yol):
    """pytmx olmadan .tmx dosyasını XML olarak okur."""
    kok = ET.parse(yol).getroot()
    gen = int(kok.attrib["width"])
    yuk = int(kok.attrib["height"])
    tile_gen = int(kok.attrib["tilewidth"])
    katmanlar = []
    for layer in kok.findall("layer"):
        data_text = layer.find("data").text.strip()
        degerler = [int(x) for x in data_text.replace("\n", "").split(",") if x]
        grid = [degerler[i * gen:(i + 1) * gen] for i in range(yuk)]
        katmanlar.append((layer.attrib["name"], grid))
    return {
        "gen": gen,
        "yuk": yuk,
        "tile_gen": tile_gen,
        "katmanlar": katmanlar,
    }


def yedek_ciz(ekran, veri):
    tg = veri["tile_gen"]
    for ad, grid in veri["katmanlar"]:
        for r, satir in enumerate(grid):
            for c, gid in enumerate(satir):
                if gid == 0:
                    continue
                renk = YEDEK_RENKLER.get(gid, (255, 0, 255))
                pygame.draw.rect(ekran, renk, (c * tg, r * tg, tg, tg))


def pytmx_ciz(ekran, tmx_data):
    tg = tmx_data.tilewidth
    for layer in tmx_data.visible_layers:
        if hasattr(layer, "tiles"):
            for x, y, image in layer.tiles():
                if image is None:
                    continue
                ekran.blit(image, (x * tg, y * tg))


def main():
    pygame.init()
    yol = Path(__file__).parent / "harita.tmx"

    if PYTMX_VAR:
        print("[OK] pytmx bulundu, yükleniyor...")
        try:
            tmx_data = pytmx.load_pygame(str(yol))
        except Exception as exc:
            print(f"[!] pytmx yükleme başarısız ({exc}), yedeğe düşelim")
            tmx_data = None
    else:
        print("[!] pytmx yok, yedek XML parser kullanılacak")
        tmx_data = None

    if tmx_data is not None:
        gen = tmx_data.width * tmx_data.tilewidth
        yuk = tmx_data.height * tmx_data.tileheight
    else:
        veri = yedek_yukle(yol)
        gen = veri["gen"] * veri["tile_gen"]
        yuk = veri["yuk"] * veri["tile_gen"]

    ekran = pygame.display.set_mode((gen, yuk))
    pygame.display.set_caption("pytmx Haritası")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        ekran.fill((10, 10, 20))
        if tmx_data is not None:
            pytmx_ciz(ekran, tmx_data)
        else:
            yedek_ciz(ekran, veri)

        mod_metin = "pytmx" if tmx_data is not None else "yedek XML parser"
        bilgi = font.render(f"Mod: {mod_metin}", True, (255, 255, 255))
        ekran.blit(bilgi, (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI:
---------------
harita.tmx dosyasından yüklenmiş 2 katmanlı bir harita görülür:
arkaplan (çim ve etrafında taş duvar) ve nesneler katmanı
(bir oda + altın tile + birkaç taş yapı). Sol üste "Mod: pytmx" ya da
"Mod: yedek XML parser" yazılır.
"""
