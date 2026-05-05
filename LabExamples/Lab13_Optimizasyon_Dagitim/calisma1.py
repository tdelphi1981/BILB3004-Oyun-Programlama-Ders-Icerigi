"""
Lab 13 - Çalışma 1 Başlangıç Kodu
cProfile ile Profil Çıkarma

Bu dosya Lab 13 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- cProfile.Profile() ile profile alma
- pstats.Stats(...).sort_stats("cumulative") ile sıralama
- Darboğaz tespit ve hızlandırma

Lab: 13 - Optimizasyon ve Dağıtım
Çalışma: 1 - cProfile ile Profil Çıkarma

Çalıştırma: uv run python calisma1.py

==============================================================
GÖREV 1.2 -- En yavaş 3 fonksiyonu çalıştırdıktan sonra buraya yaz:
1. <fonksiyon adı>  (cumtime: <saniye>)
2. <fonksiyon adı>  (cumtime: <saniye>)
3. <fonksiyon adı>  (cumtime: <saniye>)
==============================================================
"""

import math
import cProfile   # GOREV 1.1: Bu modülü kullanacaksın
import pstats     # GOREV 1.2: pstats raporu için

import pygame

GENISLIK, YUKSEKLIK = 800, 600


def agir_islem(n=2000):
    """Yapay olarak yavaşlatılmış işlem.

    Her karede çağrılır. Görevin: bu fonksiyonun darboğaz olduğunu
    profile ile keşfetmek ve GÖREV 1.3'te hızlandırmak.
    """
    toplam = 0.0
    for i in range(n):
        toplam += math.sin(i) * math.cos(i)
    return toplam


def cizimleri_yap(ekran, daireler):
    """80 daire çizer --- ikincil maliyet."""
    for (x, y, r) in daireler:
        pygame.draw.circle(ekran, (255, 215, 0), (int(x), int(y)), r)


def hud_ciz(ekran, font, fps):
    """FPS göstergesi --- ucuz ama profil için hâlâ ölçülür."""
    yazi = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
    ekran.blit(yazi, (10, 10))


def oyun_dongusu(ekran, saat, font):
    """Yaklaşık 3 saniye çalışan örnek oyun döngüsü."""
    daireler = [(40 + i * 8, 300 + math.sin(i) * 30, 6) for i in range(80)]
    sure = 0.0
    while sure < 3.0:
        dt = saat.tick(60) / 1000.0
        sure += dt

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                return

        # Her kare yapılan iş
        agir_islem()
        ekran.fill((20, 30, 40))
        cizimleri_yap(ekran, daireler)
        hud_ciz(ekran, font, saat.get_fps())
        pygame.display.flip()


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 13 - Calisma 1: cProfile")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # === GOREV 1.1 - Profile'ı Başlat ===
    # cProfile.Profile() nesnesi oluştur ve enable() ile başlat.
    # TODO: a) p = cProfile.Profile()
    # TODO: b) p.enable()

    # Ana oyun döngüsü (~3 saniye)
    oyun_dongusu(ekran, saat, font)

    # === GOREV 1.1 - Profile'ı Durdur ===
    # TODO: c) p.disable()

    pygame.quit()

    # === GOREV 1.2 - Sonuçları Yazdır ===
    # pstats.Stats(p) ile en yavaş 10 fonksiyonu cumulative time'a göre
    # sırala ve yazdır. Ayrıca diske bir .prof dosyası yaz (snakeviz için).
    # TODO: a) istatistik = pstats.Stats(p).sort_stats("cumulative")
    # TODO: b) istatistik.print_stats(10)
    # TODO: c) p.dump_stats("rapor.prof")

    # === GOREV 1.3 - Darboğazı Hızlandır ===
    # agir_islem fonksiyonunu hızlandırmak için aşağıdaki seçeneklerden
    # birini seç:
    #   1) n parametresini 2000 -> 200 yap
    #   2) functools.lru_cache ile sonucu cache'le
    #   3) numpy ile vektörel hesapla:
    #        a = np.arange(n); return float((np.sin(a) * np.cos(a)).sum())
    # Ardından bu dosyayı tekrar çalıştır ve eski/yeni cumulative süreleri
    # yorum bloğuna ekle. Hangi yöntemi seçtin?


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI (temel kod, GÖREV'ler tamamlanınca):
---------------------------------------------------
~3 saniye boyunca sarı dairelerle dolu pencere.
Pencere kapandıktan sonra terminale şuna benzer bir tablo basılır:

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      180    0.840    0.005    1.620    0.009 calisma1.py:25(agir_islem)
      180    0.220    0.001    0.380    0.002 calisma1.py:39(cizimleri_yap)
      ...

GÖREV 1.3 sonrası agir_islem cumtime'ı belirgin biçimde düşmeli.
"""
