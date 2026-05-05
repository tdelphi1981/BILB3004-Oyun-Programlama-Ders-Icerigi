"""
Lab 13 - Çalışma 2 Başlangıç Kodu
Spatial Hashing ile Çarpışma Hızlandırma

Bu dosya Lab 13 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- O(n^2) brute force çarpışma
- Sabit hücreli spatial hashing
- defaultdict(list) ile hücre sözlüğü
- FPS karşılaştırması ile ölçüm

Lab: 13 - Optimizasyon ve Dağıtım
Çalışma: 2 - Spatial Hashing

Çalıştırma: uv run python calisma2.py
Tuşlar: SPACE -> Brute force / Spatial hash arasında geçiş
        ESC   -> Çıkış

==============================================================
GÖREV 2.4 -- Karşılaştırma sonuçlarını buraya yaz:
- Brute force FPS: ___
- Spatial hash FPS: ___
- Hızlanma oranı: ___x
==============================================================
"""

import random
from collections import defaultdict

import pygame

GENISLIK, YUKSEKLIK = 800, 600
NESNE_SAYISI = 200
HUCRE_BOYU = 64


class Daire:
    """Dolaşan basit cisim --- rect ve hız tutar."""

    def __init__(self, x, y):
        self.r = random.randint(6, 10)
        self.rect = pygame.Rect(x - self.r, y - self.r, self.r * 2, self.r * 2)
        self.vx = random.uniform(-120, 120)
        self.vy = random.uniform(-120, 120)
        self.vurus = 0   # son 30 karede kaç çarpışma --- görsel rapor

    def guncelle(self, dt):
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)
        if self.rect.left < 0 or self.rect.right > GENISLIK:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > YUKSEKLIK:
            self.vy = -self.vy
        if self.vurus > 0:
            self.vurus -= 1


class SpatialHash:
    """Sabit hücreli mekansal indeks.

    Dünyayı (hucre x hucre) piksel kareler hâlinde böler. Her cisim
    kapsadığı tüm hücrelere eklenir. query(rect) verilen alanı kapsayan
    hücrelerdeki nesneleri verir.
    """

    def __init__(self, hucre=HUCRE_BOYU):
        self.hucre = hucre
        # === GOREV 2.1 - Hücre Sözlüğü ===
        # Hücre indeksi -> nesne listesi sözlüğünü tanımla.
        # TODO: self.cells = defaultdict(list)
        self.cells = None   # GOREV 2.1: doldur

    def clear(self):
        """Her kare başında temizlenir."""
        if self.cells is not None:
            self.cells.clear()

    def _hucre_indeksi(self, x, y):
        """(piksel x, piksel y) -> (hücre cx, hücre cy)."""
        return (int(x) // self.hucre, int(y) // self.hucre)

    def insert(self, obj):
        """obj.rect'in kapsadığı tüm hücrelere obj'i ekle.

        === GOREV 2.2 - insert ===
        Bir rect birden çok hücreye yayılabilir. 4 köşeyi değil,
        sol-üst ve sağ-alt köşeyi indeksleyip aralarındaki tüm
        hücreleri gez.
        """
        # TODO: a) cx0, cy0 = self._hucre_indeksi(obj.rect.left,  obj.rect.top)
        # TODO: b) cx1, cy1 = self._hucre_indeksi(obj.rect.right, obj.rect.bottom)
        # TODO: c) for cx in range(cx0, cx1 + 1):
        # TODO: d)     for cy in range(cy0, cy1 + 1):
        # TODO: e)         self.cells[(cx, cy)].append(obj)
        pass

    def query(self, rect):
        """Verilen rect'in kapsadığı hücrelerdeki nesneleri döndür.

        === GOREV 2.3 - query ===
        Set kullan; aynı nesne birden çok hücrede olabilir.
        """
        # TODO: a) sonuc = set()
        # TODO: b) cx0, cy0 = self._hucre_indeksi(rect.left,  rect.top)
        # TODO: c) cx1, cy1 = self._hucre_indeksi(rect.right, rect.bottom)
        # TODO: d) for cx in range(cx0, cx1 + 1):
        # TODO: e)     for cy in range(cy0, cy1 + 1):
        # TODO: f)         sonuc.update(self.cells.get((cx, cy), []))
        # TODO: g) return list(sonuc)
        return []


def brute_force_carpisma(daireler):
    """Saf O(n^2) çarpışma --- karşılaştırma için."""
    n = len(daireler)
    sayac = 0
    for i in range(n):
        a = daireler[i]
        for j in range(i + 1, n):
            b = daireler[j]
            if a.rect.colliderect(b.rect):
                a.vurus = 30
                b.vurus = 30
                sayac += 1
    return sayac


def spatial_carpisma(daireler, spatial):
    """Spatial hash kullanan O(n) yakın çarpışma."""
    spatial.clear()
    if spatial.cells is None:
        return 0
    for d in daireler:
        spatial.insert(d)
    sayac = 0
    gorulen = set()
    for a in daireler:
        for b in spatial.query(a.rect):
            if a is b:
                continue
            cift = (id(a), id(b)) if id(a) < id(b) else (id(b), id(a))
            if cift in gorulen:
                continue
            gorulen.add(cift)
            if a.rect.colliderect(b.rect):
                a.vurus = 30
                b.vurus = 30
                sayac += 1
    return sayac


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 13 - Calisma 2: Spatial Hashing")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    daireler = [
        Daire(random.randint(50, GENISLIK - 50),
              random.randint(50, YUKSEKLIK - 50))
        for _ in range(NESNE_SAYISI)
    ]
    spatial = SpatialHash(hucre=HUCRE_BOYU)

    # Başlangıçta brute force; SPACE ile spatial hash'e geç
    spatial_modu = False

    calistir = True
    while calistir:
        dt = saat.tick(60) / 1000.0

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_SPACE:
                    spatial_modu = not spatial_modu
                elif olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Hareket
        for d in daireler:
            d.guncelle(dt)

        # === GOREV 2.4 - Karşılaştırma ===
        # Brute force ve spatial modu arasında SPACE ile geç ve FPS'leri
        # gözlemle. Sayıları dosyanın üstündeki yorum bloğuna ekle.
        if spatial_modu:
            sayac = spatial_carpisma(daireler, spatial)
        else:
            sayac = brute_force_carpisma(daireler)

        # Çizim
        ekran.fill((15, 20, 30))
        for d in daireler:
            renk = (255, 80, 80) if d.vurus > 0 else (255, 215, 0)
            pygame.draw.circle(ekran, renk, d.rect.center, d.r)

        mod_metin = "SPATIAL HASH" if spatial_modu else "BRUTE FORCE"
        bilgi = font.render(
            f"Mod: {mod_metin}  |  FPS: {saat.get_fps():.1f}  "
            f"|  Carpisma: {sayac}  |  N: {NESNE_SAYISI}",
            True, (255, 255, 255))
        ekran.blit(bilgi, (10, 10))
        ipucu = font.render(
            "SPACE: Mod degistir   ESC: Cikis",
            True, (180, 180, 200))
        ekran.blit(ipucu, ipucu.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK - 20)))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 pencerede 200 sarı daire dolaşır.
- Çarpışma anında kırmızıya döner, 30 kare sonra geri sararır.
- Üstte mod, FPS ve çarpışma sayısı yazar.
- SPACE ile mod değişir.

GÖREVLER tamamlanınca:
- Brute force modunda FPS düşük (~10-20) olabilir.
- Spatial hash modunda FPS belirgin biçimde yükselir (~50-60).
"""
