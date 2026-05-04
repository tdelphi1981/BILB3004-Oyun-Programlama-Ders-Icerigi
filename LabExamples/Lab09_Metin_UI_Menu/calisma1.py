"""
Lab 09 - Çalışma 1 Başlangıç Kodu
Metin Render ve Hizalama

Bu dosya Lab 09 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- pygame.font.Font ve render()
- get_rect(center=...), get_rect(topright=...) ile hizalama
- Zamana bağlı metin güncelleme (skor, süre, FPS)

Lab: 09 - Metin, UI ve Menü Sistemleri
Çalışma: 1 - Metin Render ve Hizalama

Çalıştırma: uv run python calisma1.py
"""

import pygame

pygame.init()
ekran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 09 - Çalışma 1: Metin Demo")
saat = pygame.time.Clock()

# Farklı boyutta fontlar
buyuk = pygame.font.Font(None, 64)
orta = pygame.font.Font(None, 36)
kucuk = pygame.font.Font(None, 24)

skor = 0
baslangic = pygame.time.get_ticks()

# === GOREV 1.2 - Geri Sayım için sabitler ===
# TODO: GERI_SAYIM_SN = 30 sabiti tanımla
# TODO: KIRMIZI_ESIK = 10 sabiti tanımla (son 10 sn için)
# ============================================

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_SPACE:
                skor += 10

    ekran.fill((30, 30, 50))

    # Başlık - ortaya hizalı
    baslik = buyuk.render("Metin Demo", True, (255, 255, 0))
    baslik_rect = baslik.get_rect(center=(400, 50))
    ekran.blit(baslik, baslik_rect)

    # Skor - sağa hizalı
    skor_metin = orta.render(f"Skor: {skor}", True, (255, 215, 0))
    skor_rect = skor_metin.get_rect(topright=(790, 10))
    ekran.blit(skor_metin, skor_rect)

    # Geçen süre (sol üst)
    gecen = (pygame.time.get_ticks() - baslangic) // 1000
    sure_metin = kucuk.render(f"Sure: {gecen}s", True, (200, 200, 200))
    ekran.blit(sure_metin, (10, 10))

    # FPS (sol alt)
    fps = saat.get_fps()
    fps_metin = kucuk.render(f"FPS: {fps:.0f}", True, (0, 255, 0))
    ekran.blit(fps_metin, (10, 570))

    # Yardım
    yardim = kucuk.render("SPACE: +10 puan", True, (150, 150, 150))
    yardim_rect = yardim.get_rect(center=(400, 580))
    ekran.blit(yardim, yardim_rect)

    # === GOREV 1.1 - Çok Satırlı Metin ===
    # Ekranın ortasına 3 satırlık bir metin yazın.
    # Her satır farklı renkte olsun. Satır aralığı için
    # font.get_linesize() kullanın.
    #
    # TODO: a) satirlar = ["Birinci satir", "Ikinci satir", "Ucuncu satir"]
    # TODO: b) renkler = [(255,80,80), (80,255,80), (80,160,255)]
    # TODO: c) satir_yuksekligi = orta.get_linesize()
    # TODO: d) baslangic_y = 250
    # TODO: e) for i, (s, r) in enumerate(zip(satirlar, renkler)):
    #            yuzey = orta.render(s, True, r)
    #            rect = yuzey.get_rect(center=(400, baslangic_y + i * satir_yuksekligi))
    #            ekran.blit(yuzey, rect)
    # ============================================

    # === GOREV 1.2 - Geri Sayım (MM:SS) ===
    # 30 saniyelik geri sayım. Kalan süreyi MM:SS formatında
    # ekranın üst ortasında gösterin.
    # Son 10 saniyede metin rengi kırmızı olsun.
    #
    # TODO: a) kalan = max(0, GERI_SAYIM_SN - gecen)
    # TODO: b) dakika, saniye = divmod(kalan, 60)
    # TODO: c) renk = (255, 60, 60) if kalan <= KIRMIZI_ESIK else (255, 255, 255)
    # TODO: d) gs_metin = orta.render(f"{dakika:02d}:{saniye:02d}", True, renk)
    # TODO: e) gs_rect = gs_metin.get_rect(midtop=(400, 90))
    # TODO: f) ekran.blit(gs_metin, gs_rect)
    # ============================================

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 piksel boyutunda lacivert bir pencere açılır.
- Üstte sarı renkte "Metin Demo" başlığı görünür.
- Sol üstte geçen süre, sağ üstte skor gösterilir.
- Sol altta gerçek FPS, alt ortada SPACE yardım metni vardır.
- SPACE tuşuna basıldıkça skor 10 artar.

GOREV 1.1 tamamlanınca:
Ekranın ortasına 3 satırlık çok renkli yazı gelir.

GOREV 1.2 tamamlanınca:
Üst orta bölgede MM:SS formatında geri sayım çalışır,
son 10 saniye kırmızı renge geçer.
"""
