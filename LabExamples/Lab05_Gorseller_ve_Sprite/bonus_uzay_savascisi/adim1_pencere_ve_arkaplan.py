"""
Uzay Savaşçısı - Adım 1: Pencere, Sabitler ve Kayan Arka Plan

Oyun penceresini oluşturur ve döşemeli (tiled) kayan uzay
arka planı ekler. Henüz oyuncu veya düşman yok, sadece
sürekli aşağı kayan bir uzay görüntüsü.

Öğrenilecek kavramlar:
- pygame.image.load() ile görsel yükleme
- convert() ile performans optimizasyonu
- Döşemeli (tiled) arka plan oluşturma
- Kayan arka plan (scrolling background) tekniği

Bölüm: 05 - Görseller ve Sprite Temelleri
Lab: 05 - Bonus: Uzay Savaşçısı (Adım 1/7)

Çalıştırma: uv run python adim1_pencere_ve_arkaplan.py
Gereksinimler: pygame
"""

import pygame
import random
import os
import sys

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Savaşçısı - Adım 1"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (8, 8, 32)
ACIK_MAVI = (100, 180, 255)
SARI = (255, 220, 50)
GRI = (150, 150, 160)
KOYU_GRI = (80, 80, 90)
KIRMIZI = (220, 50, 50)

# Asset dizini (bonus_uzay_savascisi/ klasörünün üst dizininden)
ASSET_DIZIN = os.path.join(
    os.path.dirname(__file__), "..", "assets", "kenney_space-shooter-redux"
)


def gorsel_yukle(dosya_adi, boyut=None):
    """Görsel dosyasını yükle, bulunamazsa None döndür.

    Args:
        dosya_adi: ASSET_DIZIN içerisindeki görsel yolu.
        boyut: (genişlik, yükseklik) demeti. None ise orijinal boyut.

    Returns:
        pygame.Surface veya None (dosya bulunamazsa).
    """
    try:
        yol = os.path.join(ASSET_DIZIN, dosya_adi)
        gorsel = pygame.image.load(yol).convert_alpha()
        if boyut:
            gorsel = pygame.transform.smoothscale(gorsel, boyut)
        gorsel.set_colorkey(SIYAH)
        return gorsel
    except (pygame.error, FileNotFoundError):
        return None


def arkaplan_olustur():
    """Döşemeli arka plan Surface'i oluştur.

    Kenney arka plan görseli (256x256) tüm ekranı kaplayacak
    şekilde döşenir. Görsel yoksa yıldızlı koyu mavi yüzey oluşturur.

    Returns:
        pygame.Surface: Ekran boyutunda arka plan yüzey.
    """
    # Arka plan iki ekran yüksekliğinde (kayma için)
    arkaplan = pygame.Surface((GENISLIK, YUKSEKLIK * 2))

    gorsel = gorsel_yukle("Backgrounds/darkPurple.png")

    if gorsel:
        # Döşemeli yerleştir (tile)
        g_gen = gorsel.get_width()
        g_yuk = gorsel.get_height()
        for x in range(0, GENISLIK, g_gen):
            for y in range(0, YUKSEKLIK * 2, g_yuk):
                arkaplan.blit(gorsel, (x, y))
    else:
        # Fallback: yıldızlı koyu mavi arka plan
        arkaplan.fill(KOYU_MAVI)
        for _ in range(200):
            x = random.randint(0, GENISLIK - 1)
            y = random.randint(0, YUKSEKLIK * 2 - 1)
            boyut = random.randint(1, 3)
            if boyut == 3:
                renk = BEYAZ
            elif boyut == 2:
                renk = GRI
            else:
                renk = KOYU_GRI
            pygame.draw.circle(arkaplan, renk, (x, y), boyut)

    return arkaplan


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Arka plan oluştur
    arkaplan = arkaplan_olustur()
    arkaplan_y = 0  # Kayma konumu

    # --- Ana Oyun Döngüsü ---
    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olay işleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- Güncelle ---
        # Arka planı aşağı kaydır
        arkaplan_y += 1
        if arkaplan_y >= YUKSEKLIK:
            arkaplan_y = 0

        # --- Çizim ---
        # Kayan arka planı çiz (iki parça halinde)
        ekran.blit(arkaplan, (0, arkaplan_y - YUKSEKLIK))
        ekran.blit(arkaplan, (0, arkaplan_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu mor/mavi uzay arka planlı
bir pencere açılır. Arka plan sürekli aşağı doğru kayar
ve döşemeli (tiled) şekilde tekrar eder.

Asset dosyaları varsa Kenney'nin koyu mor uzay görseli
kullanılır. Yoksa rastgele yıldızlarla dolu koyu mavi
bir arka plan görünür.

ESC ile program kapanır.
"""
