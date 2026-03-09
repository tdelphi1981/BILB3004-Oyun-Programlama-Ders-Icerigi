"""
Lab 05 - Calisma 7 Baslangic Kodu
Mini Proje -- Uzay Sahnesi

Bu dosya Lab 05 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Oyuncu Sprite sinifi (klavye kontrollu)
- Yildiz Sprite sinifi (otomatik hareket)
- Coklu grup stratejisi (tum_spritelar, yildizlar)
- clamp_ip() ile ekran siniri
- Egzoz efekti (gecici Sprite)
- HUD bilgi paneli (FPS, sure)

Lab: 05 - Gorseller ve Sprite Temelleri
Calisma: 7 - Mini Proje: Uzay Sahnesi

Calistirma: uv run python calisma7.py
"""

# --- Baslangic Kodu ---

import pygame
import random
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
KOYU_MAVI = (5, 10, 30)
BEYAZ = (255, 255, 255)

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Uzay Sahnesi")
saat = pygame.time.Clock()
font = pygame.font.Font(None, 24)


def gorsel_yukle(yol, boyut=None):
    """Gorsel yukle, bulunamazsa placeholder dondur."""
    try:
        g = pygame.image.load(yol).convert_alpha()
        if boyut:
            g = pygame.transform.scale(g, boyut)
        return g
    except (FileNotFoundError, pygame.error):
        b = boyut or (40, 40)
        s = pygame.Surface(b, pygame.SRCALPHA)
        s.fill((100, 150, 255, 200))
        return s


class Yildiz(pygame.sprite.Sprite):
    """Kayan yildiz arka plani icin Sprite."""
    def __init__(self):
        super().__init__()
        self.boyut = random.randint(1, 3)
        cap = self.boyut * 2
        self.image = pygame.Surface((cap, cap), pygame.SRCALPHA)
        parlaklik = 100 + self.boyut * 50
        renk = (parlaklik, parlaklik, parlaklik)
        pygame.draw.circle(self.image, renk,
                          (self.boyut, self.boyut), self.boyut)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK)
        self.rect.y = random.randint(-YUKSEKLIK, YUKSEKLIK)
        self.hiz = self.boyut * 0.8 + random.uniform(0, 1.5)

    def update(self):
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.rect.x = random.randint(0, GENISLIK)
            self.rect.bottom = 0


# === GOREV 7.1 - Temel Yapi ===
# TODO: a) Oyuncu sinifi olusturun:
#          - super().__init__()
#          - self.image = gorsel_yukle(...) veya Surface
#          - self.rect = self.image.get_rect(midbottom=(400, 580))
#          - self.hiz = 5
#          - update() metodu: WASD + ok tuslari, clamp_ip()
# TODO: b) Gruplari olusturun:
#          - tum_spritelar = pygame.sprite.Group()
#          - yildizlar = pygame.sprite.Group()
# TODO: c) 60 adet Yildiz + 1 Oyuncu olusturup gruplara ekleyin
# TODO: d) Ana donguyu yazin:
#          - tum_spritelar.update()
#          - ekran.fill(KOYU_MAVI)
#          - tum_spritelar.draw(ekran)
# ============================================


# === GOREV 7.2 - FPS ve HUD ===
# TODO: a) Sag ust koseye FPS degerini gosterin
#          (saat.get_fps() kullanin)
# TODO: b) Sol ust koseye hayatta kalma suresini gosterin
#          (pygame.time.get_ticks() // 1000)
# Ipucu kodu:
#
#   fps_yazi = font.render(
#       f"FPS: {saat.get_fps():.0f}", True, BEYAZ)
#   ekran.blit(fps_yazi, (GENISLIK - 100, 10))
# ============================================


# === GOREV 7.3 - Egzoz Efekti ===
# TODO: a) Egzoz sinifi olusturun:
#          - Kucuk turuncu/sari daire
#          - Her karede alfa degeri azalsin
#          - Alfa 0 olunca kill()
# TODO: b) Her karede geminin altinda yeni Egzoz olusturun
# Ipucu kodu:
#
#   class Egzoz(pygame.sprite.Sprite):
#       def __init__(self, x, y):
#           super().__init__()
#           self.image = pygame.Surface((6, 6), pygame.SRCALPHA)
#           pygame.draw.circle(self.image,
#               (255, 180, 50, 200), (3, 3), 3)
#           self.rect = self.image.get_rect(center=(x, y))
#           self.alfa = 200
#
#       def update(self):
#           self.alfa -= 15
#           if self.alfa <= 0:
#               self.kill()
#           else:
#               self.image.set_alpha(self.alfa)
#               self.rect.y += 2
# ============================================


# BONUS: Meteor Engellerinden Kacis
# TODO: a) Meteor sinifi olusturun (farkli boyut ve hiz)
# TODO: b) Her 2 saniyede bir yeni meteor ekleyin
# TODO: c) 3 farkli boyut: kucuk (hizli), orta, buyuk (yavas)
# TODO: d) Ekran disina cikan meteorlar kill() ile silinsin
# TODO: e) Meteor grubunu ayri tutun
# ============================================


"""
BEKLENEN CIKTI (gorevler tamamlaninca):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Yildizlar yukariTRdan asagi kayar (paralaks efekti).
Oyuncu gemisi WASD/ok tuslariyla hareket eder.
Sol ustte sure, sag ustte FPS gorunur.
Geminin arkasindan egzoz parcaciklari cikar.
"""
