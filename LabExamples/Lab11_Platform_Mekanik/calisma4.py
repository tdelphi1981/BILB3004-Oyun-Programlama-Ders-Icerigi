"""
Lab 11 - Çalışma 4 Başlangıç Kodu (Bonus)
Power-Up Sistemi

Bu dosya Lab 11 föyü Bonus görevi için başlangıç kodudur.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- PowerUp (Sprite) sınıfı
- Efekt sözlüğü yönetimi
- HUD'da süre çubuğu

Lab: 11 - Platform Oyunu Mekaniği
Çalışma: Bonus - Power-Up Sistemi

Çalıştırma: uv run python calisma4.py
"""

import math

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480


class PowerUp(pygame.sprite.Sprite):
    RENKLER = {
        "hiz": (80, 220, 240),
        "zipla": (240, 180, 60),
        "kalkan": (180, 80, 220),
    }

    def __init__(self, x, y, tur="hiz"):
        super().__init__()
        self.tur = tur
        self.image = pygame.Surface((24, 24))
        self.image.fill(PowerUp.RENKLER.get(tur, (200, 200, 200)))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.anim_faz = 0.0

    def update(self):
        self.anim_faz += 0.08


class Oyuncu:
    BASE_MAX_HIZ = 4

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0.0
        self.vy = 0.0
        self.yerde = False
        self.efektler = {}   # {"hiz": sure_kare}

    def power_up_al(self, tur):
        # GOREV 1: tur'a göre self.efektler[tur] = uygun süre
        # hız/zıpla = 600 kare (10s), kalkan = 900 kare (15s)
        pass

    @property
    def hiz_aktif(self):
        return "hiz" in self.efektler

    def zipla(self):
        if self.yerde:
            self.vy = -11

    def guncelle(self, tuslar, katilar):
        # GOREV 2: Her karede tüm efektleri 1 azalt
        # <= 0 olanları sözlükten sil
        # İpucu: for t in list(self.efektler.keys()): ...

        # Hareket (hız efekti varsa 2 katı)
        max_hiz = self.BASE_MAX_HIZ * (2.0 if self.hiz_aktif else 1.0)
        self.vx = 0
        if tuslar[pygame.K_LEFT]:
            self.vx = -max_hiz
        elif tuslar[pygame.K_RIGHT]:
            self.vx = max_hiz

        self.rect.x += int(self.vx)
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vx > 0:
                    self.rect.right = k.left
                elif self.vx < 0:
                    self.rect.left = k.right

        self.vy = min(self.vy + 0.5, 10)
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


def ciz_efekt_hud(ekran, oyuncu, font):
    # GOREV 3: HUD'da her aktif efekt için
    # 120px bar arkasında (gri) + oran kadar renkli doldur
    # Yanına efekt adını yaz
    pass


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 11 - Calisma 4 (Power-Up Bonus)")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    katilar = [
        pygame.Rect(0, YUKSEKLIK - TILE, GENISLIK, TILE),
        pygame.Rect(0, 0, TILE, YUKSEKLIK),
        pygame.Rect(GENISLIK - TILE, 0, TILE, YUKSEKLIK),
    ]
    powerups = pygame.sprite.Group(
        PowerUp(200, 400, "hiz"),
        PowerUp(300, 400, "zipla"),
        PowerUp(400, 400, "kalkan"),
    )
    oyuncu = Oyuncu(80, 400)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP):
                    oyuncu.zipla()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)
        powerups.update()

        # GOREV 4: Power-up toplama
        # Dummy sprite oluştur (oyuncu.rect ile) veya pygame.sprite.spritecollide
        # Toplanan PowerUp için oyuncu.power_up_al(pu.tur) çağır
        # Örnek:
        # dummy = type("S", (), {"rect": oyuncu.rect})()
        # for pu in pygame.sprite.spritecollide(dummy, powerups, True):
        #     oyuncu.power_up_al(pu.tur)

        ekran.fill((30, 30, 60))
        for k in katilar:
            pygame.draw.rect(ekran, (120, 120, 120), k)

        # Salınımlı çiz
        for pu in powerups:
            offset = int(math.sin(pu.anim_faz) * 3)
            r = pu.rect.copy()
            r.y += offset
            ekran.blit(pu.image, r)

        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)

        ekran.blit(font.render(
            f"Aktif efektler: {list(oyuncu.efektler.keys())}",
            True, (220, 220, 220)), (10, 10))

        ciz_efekt_hud(ekran, oyuncu, font)

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
