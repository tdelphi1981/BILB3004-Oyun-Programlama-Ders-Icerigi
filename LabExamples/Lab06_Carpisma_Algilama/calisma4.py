"""
Lab 06 - Calisma 4 Baslangic Kodu
Breakout (Tugla Kirma) Mini Proje

Bu dosya Lab 06 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Bu calisma bir mini projedir. Asagida sinif iskeletleri
verilmistir, gorevleri tamamlayarak tam bir Breakout
oyunu olusturun.

Ogrenilecek kavramlar:
- Sprite siniflarini tasarlama (Raket, Top, Tugla)
- spritecollide() ile top-tugla carpismasi
- Aci hesabi ile top yonu degistirme
- Oyun durumu yonetimi (can, skor, game over)

Lab: 06 - Carpisma Algilama ve Fizik Temelleri
Calisma: 4 - Mini Proje: Breakout (Tugla Kirma)

Calistirma: uv run python calisma4.py
"""

import pygame
import math

pygame.init()
GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Breakout - Tugla Kirma")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Renkler
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
KOYU_MAVI = (15, 15, 40)
ACIK_MAVI = (52, 152, 219)
KIRMIZI = (231, 76, 60)
YESIL = (46, 204, 113)
SARI = (241, 196, 15)
TURUNCU = (243, 156, 18)
MOR = (155, 89, 182)

# Tugla renkleri (satirlara gore)
TUGLA_RENKLERI = [KIRMIZI, TURUNCU, SARI, YESIL]


class Raket(pygame.sprite.Sprite):
    """Oyuncu kontrollü raket.

    Ok tuslari ile saga-sola hareket eder.
    Ekranin altinda yer alir (120x15 piksel).
    """

    def __init__(self):
        super().__init__()
        self.genislik = 120
        self.yukseklik = 15
        self.image = pygame.Surface(
            (self.genislik, self.yukseklik), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.image, ACIK_MAVI,
            (0, 0, self.genislik, self.yukseklik),
            border_radius=4
        )
        self.rect = self.image.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 30
        )
        self.hiz = 7

    def update(self):
        pass  # GOREV 4.1'de tamamlanacak


class Top(pygame.sprite.Sprite):
    """Ziplayan top.

    Duvarlardan ve raketten seker.
    Yaricap 8 piksel.
    """

    def __init__(self):
        super().__init__()
        self.yaricap = 8
        cap = self.yaricap * 2
        self.image = pygame.Surface((cap, cap), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, BEYAZ,
            (self.yaricap, self.yaricap), self.yaricap
        )
        self.rect = self.image.get_rect(
            centerx=GENISLIK // 2, centery=YUKSEKLIK // 2
        )
        self.hiz = 5
        self.hiz_x = 3.0
        self.hiz_y = -4.0

    def update(self):
        pass  # GOREV 4.1'de tamamlanacak


class Tugla(pygame.sprite.Sprite):
    """Kirilan tugla.

    Farkli renklerde olabilir. Top carpinca kirilir.
    Boyut: 70x25 piksel.
    """

    def __init__(self, x, y, renk=KIRMIZI):
        super().__init__()
        self.genislik = 70
        self.yukseklik = 25
        self.image = pygame.Surface(
            (self.genislik, self.yukseklik), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.image, renk,
            (0, 0, self.genislik, self.yukseklik),
            border_radius=3
        )
        # Ince parlak kenarlık
        pygame.draw.rect(
            self.image, BEYAZ,
            (0, 0, self.genislik, self.yukseklik),
            width=1, border_radius=3
        )
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass  # Tuglalar hareket etmez


# --- Sprite Gruplari ---
tum_spritelar = pygame.sprite.Group()
tuglalar = pygame.sprite.Group()

raket = Raket()
top = Top()
tum_spritelar.add(raket, top)

# Bilgi yazisi (baslangic)
bilgi_font = pygame.font.SysFont("Arial", 18)

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_ESCAPE:
                calistir = False

    tum_spritelar.update()

    # Cizim
    ekran.fill(KOYU_MAVI)
    tum_spritelar.draw(ekran)

    # Baslangic bilgi yazisi
    bilgi = bilgi_font.render(
        "GOREV 4.1-4.3'u tamamlayarak Breakout oyununu olusturun!",
        True, SARI
    )
    bilgi_rect = bilgi.get_rect(
        centerx=GENISLIK // 2, centery=YUKSEKLIK // 2 + 50
    )
    ekran.blit(bilgi, bilgi_rect)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 4.1 - Temel Yapiyi Olusturun ===
# TODO: a) Raket.update(): Ok tuslariyla saga-sola hareket
#          (ekran sinirlarini kontrol edin)
# TODO: b) Top.update(): Topu hiz_x ve hiz_y ile hareket
#          ettirin, duvarlara ve tavana carpinca yonu cevirin
# TODO: c) Tugla dizimi: 5 sutun x 4 satir = 20 tugla olusturun
#          ve tuglalar grubuna ekleyin
# Ipucu (Raket hareket):
#   def update(self):
#       tuslar = pygame.key.get_pressed()
#       if tuslar[pygame.K_LEFT]:
#           self.rect.x -= self.hiz
#       if tuslar[pygame.K_RIGHT]:
#           self.rect.x += self.hiz
#       self.rect.clamp_ip(ekran.get_rect())
#
# Ipucu (Tugla dizimi):
#   for satir in range(4):
#       for sutun in range(5):
#           x = 90 + sutun * 130
#           y = 60 + satir * 35
#           renk = TUGLA_RENKLERI[satir]
#           t = Tugla(x, y, renk)
#           tum_spritelar.add(t)
#           tuglalar.add(t)
# ============================================


# === GOREV 4.2 - Carpisma ve Skor ===
# TODO: a) Top-tugla carpismasini spritecollide() ile ekleyin
#          (carpisan tugla silinsin, skor 10 artsin)
# TODO: b) Top-raket carpismasini colliderect() ile yapin
# TODO: c) Topun rakete carpisma noktasina gore acisini
#          degistirin (asagidaki formulu kullanin)
# Ipucu (aci hesabi):
#   if top.rect.colliderect(raket.rect):
#       vurun_x = top.rect.centerx - raket.rect.left
#       oran = vurun_x / raket.rect.width  # 0.0 - 1.0
#       aci = (oran - 0.5) * 120
#       top.hiz_x = math.sin(math.radians(aci)) * top.hiz
#       top.hiz_y = -abs(math.cos(math.radians(aci)) * top.hiz)
#       top.rect.bottom = raket.rect.top
# ============================================


# === GOREV 4.3 - Can Sistemi ve Oyun Durumu ===
# TODO: a) Oyuncuya 3 can verin
# TODO: b) Top ekranin altindan duserse 1 can azalsin ve
#          top raketin ustunde yeniden baslasin
#          (Space ile firlatma)
# TODO: c) Canlar bitince "GAME OVER" ekrani gosterin
# TODO: d) Tum tuglalar kirilinca "KAZANDINIZ!" mesaji gosterin
# Ipucu:
#   can = 3
#   top_aktif = True  # False ise raketin ustunde bekler
#   # Top ekranin altindan dustuyse:
#   if top.rect.top > YUKSEKLIK:
#       can -= 1
#       if can > 0:
#           top_aktif = False
#           top.rect.centerx = raket.rect.centerx
#           top.rect.bottom = raket.rect.top - 5
#       else:
#           oyun_bitti = True
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Ekranin alt kisminda mavi bir raket, ortasinda beyaz
bir top gorulur.

Gorevler tamamlaninca:
- Ustte 4 satir x 5 sutun renkli tuglalar dizilir
- Top duvarlardan ve raketten seker
- Tuglalara carpinca tuglalar kirilir ve skor artar
- Top alttan duserse can kaybolur
- Tum tuglalar kirilinca "KAZANDINIZ!" yazar
"""
