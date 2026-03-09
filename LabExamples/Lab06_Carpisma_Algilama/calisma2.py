"""
Lab 06 - Calisma 2 Baslangic Kodu
Sprite Carpisma Fonksiyonlari

Bu dosya Lab 06 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- pygame.sprite.spritecollide() ile sprite-grup carpismasi
- pygame.sprite.groupcollide() ile grup-grup carpismasi
- dokill parametresi
- USEREVENT ile zamanlayici

Lab: 06 - Carpisma Algilama ve Fizik Temelleri
Calisma: 2 - Sprite Carpisma Fonksiyonlari

Calistirma: uv run python calisma2.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import random

pygame.init()
GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Sprite Carpisma")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


class Oyuncu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (52, 152, 219),
                         (0, 0, 50, 50), border_radius=5)
        self.rect = self.image.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK - 80))

    def update(self):
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]:
            self.rect.x -= 5
        if tuslar[pygame.K_RIGHT]:
            self.rect.x += 5
        if tuslar[pygame.K_UP]:
            self.rect.y -= 5
        if tuslar[pygame.K_DOWN]:
            self.rect.y += 5
        self.rect.clamp_ip(ekran.get_rect())


class Dusman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (231, 76, 60),
                         (0, 0, 30, 30), border_radius=3)
        self.rect = self.image.get_rect(
            center=(random.randint(50, 750),
                    random.randint(-200, -30)))
        self.hiz = random.uniform(1.5, 4.0)

    def update(self):
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


class Mermi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12), pygame.SRCALPHA)
        self.image.fill((241, 196, 15))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 8
        if self.rect.bottom < 0:
            self.kill()


# Gruplar
tum_spritelar = pygame.sprite.Group()
dusmanlar = pygame.sprite.Group()
mermiler = pygame.sprite.Group()

oyuncu = Oyuncu()
tum_spritelar.add(oyuncu)

# Dusman zamanlayici
DUSMAN_OLAY = pygame.USEREVENT + 1
pygame.time.set_timer(DUSMAN_OLAY, 800)

skor = 0

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == DUSMAN_OLAY:
            d = Dusman()
            tum_spritelar.add(d)
            dusmanlar.add(d)
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_SPACE:
                m = Mermi(oyuncu.rect.centerx,
                          oyuncu.rect.top)
                tum_spritelar.add(m)
                mermiler.add(m)

    tum_spritelar.update()

    # Mermi-dusman carpisma (ikisini de sil)
    vurulanlar = pygame.sprite.groupcollide(
        mermiler, dusmanlar, True, True
    )
    skor += len(vurulanlar)

    # Oyuncu-dusman carpisma (sadece dusmani sil)
    carpisan = pygame.sprite.spritecollide(
        oyuncu, dusmanlar, True
    )
    if carpisan:
        skor = max(0, skor - 2)

    ekran.fill((10, 10, 30))
    tum_spritelar.draw(ekran)

    yazi = font.render(f"Skor: {skor}", True, (255, 255, 255))
    ekran.blit(yazi, (10, 10))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 2.1 - Can Sistemi ===
# TODO: a) Oyuncuya 3 can verin (degisken olarak)
# TODO: b) Dusmana carpinca 1 can kaybedin (skor dusurme yerine)
# TODO: c) Canlar bitince "GAME OVER" yazisi gosterin ve
#          oyunu durdurun (donguyu devam ettirin ama guncelleme
#          yapmayin)
# TODO: d) Ekranin sag ust kosesine kalan canlari gosterin
# Ipucu:
#   can = 3
#   oyun_aktif = True
#   # Carpisma kontrolunde:
#   if carpisan and oyun_aktif:
#       can -= 1
#       if can <= 0:
#           oyun_aktif = False
#   # Cizimde:
#   if not oyun_aktif:
#       go = font.render("GAME OVER", True, (231, 76, 60))
#       ekran.blit(go, (GENISLIK//2 - 80, YUKSEKLIK//2))
# ============================================


# === GOREV 2.2 - Mermi Cooldown ===
# TODO: a) Space tusuna basili tutunca surekli mermi atilmasini
#          engelleyin
# TODO: b) pygame.time.get_ticks() kullanarak 250 ms'lik bir
#          bekleme suresi ekleyin
# TODO: c) Son mermi zamanini son_mermi degiskeninde saklayin
# Ipucu:
#   son_mermi = 0
#   # Mermi atma kontrolunde:
#   simdiki_zaman = pygame.time.get_ticks()
#   if simdiki_zaman - son_mermi > 250:
#       # Mermi olustur
#       son_mermi = simdiki_zaman
# ============================================


# === GOREV 2.3 - Farkli Dusman Turleri ===
# TODO: a) Iki farkli dusman turu olusturun:
#          - Buyuk/yavas: 50x50, hiz 1-2, kirmizi, 3 puan
#          - Kucuk/hizli: 20x20, hiz 3-5, turuncu, 1 puan
# TODO: b) Her dusman olusturulurken rastgele tur secin
# TODO: c) Dusman turune gore farkli renk ve puan verin
# Ipucu:
#   class BuyukDusman(pygame.sprite.Sprite):
#       def __init__(self):
#           super().__init__()
#           self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
#           pygame.draw.rect(self.image, (200, 50, 50),
#                            (0, 0, 50, 50), border_radius=5)
#           self.rect = self.image.get_rect(...)
#           self.hiz = random.uniform(1, 2)
#           self.puan = 3
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu lacivert bir pencere acilir.
Alt ortada mavi oyuncu karesi, ustten kirmizi dusmanlar iner.

Ok tuslari ile hareket, SPACE ile sari mermiler atesledilir.
Mermi dusmana isabet edince ikisi de silinir ve skor 1 artar.
Dusman oyuncuya carparsa skor 2 duser (minimum 0).

Sol ustte "Skor: X" gosterilir.
"""
