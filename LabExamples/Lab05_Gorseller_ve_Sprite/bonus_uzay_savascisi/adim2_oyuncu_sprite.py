"""
Uzay Savaşçısı - Adım 2: Oyuncu Sprite'ı

Oyuncu uzay gemisini Sprite sınıfı olarak oluşturur.
Ok tuşları veya WASD ile dört yönde hareket eder.
clamp_ip ile ekran sınırları kontrol edilir.

Öğrenilecek kavramlar:
- pygame.sprite.Sprite alt sınıfı oluşturma
- image ve rect nitelikleri
- update() metodu ile hareket
- pygame.key.get_pressed() ile sürekli hareket
- clamp_ip() ile sınır kontrolü
- gorsel_yukle() fallback fonksiyonu

Bölüm: 05 - Görseller ve Sprite Temelleri
Lab: 05 - Bonus: Uzay Savaşçısı (Adım 2/7)

Çalıştırma: uv run python adim2_oyuncu_sprite.py
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
BASLIK = "Uzay Savaşçısı - Adım 2"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (8, 8, 32)
ACIK_MAVI = (100, 180, 255)
SARI = (255, 220, 50)
GRI = (150, 150, 160)
KOYU_GRI = (80, 80, 90)

# Oyuncu ayarları
OYUNCU_HIZ = 5
OYUNCU_BOYUT = (50, 40)

# Asset dizini
ASSET_DIZIN = os.path.join(
    os.path.dirname(__file__), "..", "assets", "kenney_space-shooter-redux"
)


def gorsel_yukle(dosya_adi, boyut=None):
    """Görsel dosyasını yükle, bulunamazsa None döndür."""
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
    """Döşemeli arka plan Surface'i oluştur."""
    arkaplan = pygame.Surface((GENISLIK, YUKSEKLIK * 2))
    gorsel = gorsel_yukle("Backgrounds/darkPurple.png")

    if gorsel:
        g_gen = gorsel.get_width()
        g_yuk = gorsel.get_height()
        for x in range(0, GENISLIK, g_gen):
            for y in range(0, YUKSEKLIK * 2, g_yuk):
                arkaplan.blit(gorsel, (x, y))
    else:
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


# --- Sprite Sınıfları ---

class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi.

    WASD veya ok tuşları ile dört yönde hareket eder.
    clamp_ip ile ekran sınırlarını aşmaz.
    """

    def __init__(self):
        super().__init__()
        # Görseli yükle, yoksa fallback şekil çiz
        gorsel = gorsel_yukle("PNG/playerShip1_blue.png", OYUNCU_BOYUT)
        if gorsel:
            self.image = gorsel
        else:
            # Fallback: mavi üçgen gemi
            self.image = pygame.Surface(OYUNCU_BOYUT, pygame.SRCALPHA)
            orta_x = OYUNCU_BOYUT[0] // 2
            govde = [
                (orta_x, 2),
                (OYUNCU_BOYUT[0] - 4, OYUNCU_BOYUT[1] - 2),
                (4, OYUNCU_BOYUT[1] - 2),
            ]
            pygame.draw.polygon(self.image, ACIK_MAVI, govde)
            pygame.draw.polygon(self.image, BEYAZ, govde, 2)
            pygame.draw.circle(self.image, SARI,
                              (orta_x, OYUNCU_BOYUT[1] // 2), 4)

        self.rect = self.image.get_rect()
        # Başlangıç konumu: ekranın alt ortası
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.hiz = OYUNCU_HIZ
        # Ekran sınır dikdörtgeni
        self.sinir = pygame.Rect(0, 0, GENISLIK, YUKSEKLIK)

    def update(self):
        """Klavye girdilerine göre hareket et."""
        tuslar = pygame.key.get_pressed()

        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += self.hiz
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            self.rect.y -= self.hiz
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            self.rect.y += self.hiz

        # Ekran sınırları içinde tut
        self.rect.clamp_ip(self.sinir)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # Arka plan
    arkaplan = arkaplan_olustur()
    arkaplan_y = 0

    # --- Sprite Grupları ---
    tum_spritelar = pygame.sprite.Group()

    # --- Oyuncuyu oluştur ---
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

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
        arkaplan_y += 1
        if arkaplan_y >= YUKSEKLIK:
            arkaplan_y = 0

        tum_spritelar.update()

        # --- Çizim ---
        ekran.blit(arkaplan, (0, arkaplan_y - YUKSEKLIK))
        ekran.blit(arkaplan, (0, arkaplan_y))

        tum_spritelar.draw(ekran)

        # Kontrol bilgisi
        kontrol = font.render(
            "WASD / Ok Tuşları: Hareket | ESC: Çıkış",
            True, KOYU_GRI
        )
        kontrol_rect = kontrol.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 8
        )
        ekran.blit(kontrol, kontrol_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda kayan uzay arka planlı bir pencere açılır.
Ekranın alt ortasında mavi bir uzay gemisi görülür.

WASD veya ok tuşları ile gemiyi dört yönde hareket ettir.
Gemi ekran sınırlarını aşmaz (clamp_ip).

Asset dosyaları varsa Kenney gemi sprite'ı kullanılır.
Yoksa mavi üçgen şeklinde fallback gemi görünür.

ESC ile program kapanır.
"""
