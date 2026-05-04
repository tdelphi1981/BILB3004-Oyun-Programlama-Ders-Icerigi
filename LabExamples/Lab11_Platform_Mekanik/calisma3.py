"""
Lab 11 - Çalışma 3 Başlangıç Kodu
Patrol Dusman + Stomping

Bu dosya Lab 11 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- pygame.sprite.Sprite'tan türeyen Dusman
- Uçurum tespiti
- Stomping (üstten ezme) - yönlü çarpışma

Lab: 11 - Platform Oyunu Mekaniği
Çalışma: 3 - Patrol AI + Stomping

Çalıştırma: uv run python calisma3.py
"""

import pygame

TILE = 32
GENISLIK = 640
YUKSEKLIK = 480


class Dusman(pygame.sprite.Sprite):
    def __init__(self, x, y, sol_x, sag_x, hiz=1.5):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((220, 100, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sol_x = sol_x
        self.sag_x = sag_x
        self.hiz = hiz
        self.vx = hiz
        self.vy = 0.0
        self.oldurulebilir = True

    def _ucurum_var_mi(self, katilar):
        # GOREV 1: Uçurum tespiti
        # - Hareket yönünde (self.vx > 0 ise sağa, <0 ise sola) ayak altında
        #   küçük bir test Rect oluştur (4x6 piksel).
        # - Bu rect bir katı ile çarpışıyorsa False (dolu), yoksa True (uçurum).
        # İpucu:
        #   test_x = self.rect.right + 2 if self.vx > 0 else self.rect.left - 6
        #   test = pygame.Rect(test_x, self.rect.bottom + 2, 4, 6)
        return False  # varsayılan: değiştir

    def guncelle(self, oyuncu, katilar):
        # GOREV 2: Yön değiştirme kuralları
        # - _ucurum_var_mi TRUE ise self.vx = -self.vx
        # - rect.left <= sol_x ve vx < 0 ise vx = self.hiz
        # - rect.right >= sag_x ve vx > 0 ise vx = -self.hiz

        # Fizik
        self.rect.x += int(self.vx)
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vx > 0:
                    self.rect.right = k.left
                    self.vx *= -1
                elif self.vx < 0:
                    self.rect.left = k.right
                    self.vx *= -1
        self.vy = min(self.vy + 0.5, 10)
        self.rect.y += int(self.vy)
        for k in katilar:
            if self.rect.colliderect(k):
                if self.vy > 0:
                    self.rect.bottom = k.top
                elif self.vy < 0:
                    self.rect.top = k.bottom
                self.vy = 0


class Oyuncu:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 32)
        self.vx = 0.0
        self.vy = 0.0
        self.yerde = False
        self.can = 3
        self.iframe_sayac = 0

    def zipla(self):
        if self.yerde:
            self.vy = -11

    def hasar_al(self):
        # GOREV 4: I-frames kontrolü ekle
        # Eğer self.iframe_sayac > 0 ise return
        # Değilse self.can -= 1, self.iframe_sayac = 60
        self.can -= 1

    def guncelle(self, tuslar, katilar):
        # GOREV 4 (devam): iframe_sayac her karede 1 azalsın

        self.vx = 0
        if tuslar[pygame.K_LEFT]:
            self.vx = -4
        elif tuslar[pygame.K_RIGHT]:
            self.vx = 4

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


def oyuncu_dusman_carpismasi(oyuncu, grubu):
    # GOREV 3: Stomping mantığı
    # Her düşman için colliderect kontrolü:
    # - Eğer (vy > 0 VE oyuncu.rect.bottom < d.rect.top + 16 VE d.oldurulebilir):
    #     d.kill()
    #     oyuncu.vy = -9
    # - Değilse oyuncu.hasar_al()
    for d in list(grubu):
        if oyuncu.rect.colliderect(d.rect):
            pass


def harita_ciz(ekran, katilar):
    for k in katilar:
        pygame.draw.rect(ekran, (120, 120, 120), k)
        pygame.draw.rect(ekran, (80, 80, 80), k, 2)


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 11 - Calisma 3 (Patrol + Stomp)")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    katilar = [
        pygame.Rect(0, YUKSEKLIK - TILE, GENISLIK, TILE),
        pygame.Rect(0, 0, TILE, YUKSEKLIK),
        pygame.Rect(GENISLIK - TILE, 0, TILE, YUKSEKLIK),
        pygame.Rect(150, 340, TILE * 5, TILE),
    ]
    dusmanlar = pygame.sprite.Group(
        Dusman(170, 340 - 28, 150, 310),
        Dusman(60, YUKSEKLIK - TILE - 28, 40, 600),
    )
    oyuncu = Oyuncu(80, 200)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key in (pygame.K_SPACE, pygame.K_UP):
                    oyuncu.zipla()

        oyuncu.guncelle(pygame.key.get_pressed(), katilar)
        for d in dusmanlar:
            d.guncelle(oyuncu, katilar)
        oyuncu_dusman_carpismasi(oyuncu, dusmanlar)

        ekran.fill((30, 30, 60))
        harita_ciz(ekran, katilar)
        dusmanlar.draw(ekran)
        pygame.draw.rect(ekran, (220, 80, 80), oyuncu.rect)

        ekran.blit(font.render(
            f"Can: {oyuncu.can}  Dusman: {len(dusmanlar)}  iframe: {oyuncu.iframe_sayac}",
            True, (220, 220, 220)), (10, 10))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
