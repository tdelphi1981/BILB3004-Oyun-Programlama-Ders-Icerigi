"""
Lab 05 - Calisma 6 Baslangic Kodu
Sprite Sinifi ve Gruplar

Bu dosya Lab 05 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.sprite.Sprite alt sinifi olusturma
- self.image ve self.rect zorunlu ozellikleri
- super().__init__() cagrisi
- pygame.sprite.Group ile toplu yonetim
- update() ve draw() metotlari
- kill() ile Sprite silme

Lab: 05 - Gorseller ve Sprite Temelleri
Calisma: 6 - Sprite Sinifi ve Gruplar

Calistirma: uv run python calisma6.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import random
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Temel Sprite")
saat = pygame.time.Clock()

# Basit bir Sprite sinifi
class Kutu(pygame.sprite.Sprite):
    def __init__(self, renk, x, y, boyut=50):
        super().__init__()
        self.image = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
        pygame.draw.rect(self.image, renk,
                         (0, 0, boyut, boyut), border_radius=5)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass  # Simdilik bos

# Sprite olustur
kutu = Kutu((0, 180, 255), GENISLIK // 2, YUKSEKLIK // 2)
grup = pygame.sprite.Group(kutu)

calistir = True
while calistir:
    saat.tick(60)
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    grup.update()
    ekran.fill((20, 20, 30))
    grup.draw(ekran)
    pygame.display.flip()

pygame.quit()
sys.exit()


# === GOREV 6.1 - Birden Fazla Sprite ve Hareket ===
# TODO: a) Uc farkli renkte ve konumda kutu olusturun
# TODO: b) Hepsini ayni gruba ekleyin
# TODO: c) update() metoduna ok tuslariyla hareket ekleyin
# TODO: d) rect.clamp_ip() ile ekran sinirlarinda tutun
# Ipucu kodu:
#
#   def update(self):
#       tuslar = pygame.key.get_pressed()
#       if tuslar[pygame.K_LEFT]:
#           self.rect.x -= 5
#       if tuslar[pygame.K_RIGHT]:
#           self.rect.x += 5
#       ekran_rect = pygame.display.get_surface().get_rect()
#       self.rect.clamp_ip(ekran_rect)
# ============================================


# === GOREV 6.2 - Grup Islemleri ===
# TODO: a) Top sinifini olusturun (asagidaki kodu kullanin)
# TODO: b) 15 adet Top olusturup gruba ekleyin
# TODO: c) Space ile yeni top ekleyin
# TODO: d) R ile rastgele bir topu kill() ile silin
# TODO: e) Eleman sayisini ekranda gosterin
# Ipucu kodu:
#
#   class Top(pygame.sprite.Sprite):
#       def __init__(self):
#           super().__init__()
#           self.renk = (random.randint(100, 255),
#                        random.randint(100, 255),
#                        random.randint(100, 255))
#           self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
#           pygame.draw.circle(self.image, self.renk, (10, 10), 10)
#           self.rect = self.image.get_rect(
#               center=(random.randint(50, 750),
#                       random.randint(50, 550)))
#           self.hiz_x = random.choice([-3, -2, 2, 3])
#           self.hiz_y = random.choice([-3, -2, 2, 3])
#
#       def update(self):
#           self.rect.x += self.hiz_x
#           self.rect.y += self.hiz_y
#           if self.rect.left < 0 or self.rect.right > 800:
#               self.hiz_x *= -1
#           if self.rect.top < 0 or self.rect.bottom > 600:
#               self.hiz_y *= -1
# ============================================


# === GOREV 6.3 - Kayan Yildiz Arka Plani ===
# TODO: a) Yildiz sinifini olusturun (lab foyundeki kodu kullanin)
# TODO: b) 50 adet Yildiz olusturup tum_spritelar ve yildizlar
#          gruplarina ekleyin
# TODO: c) Paralaks derinlik efekti ekleyin:
#          - boyut 1: yavas (uzak yildiz)
#          - boyut 3: hizli (yakin yildiz)
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu pencere acilir.
Ekranin ortasinda mavi, yuvarlatilmis koseli bir
kare gorulur.
"""
