"""
Lab 08 - Calisma 2 Baslangic Kodu
AnimatedSprite Sinifi

Bu dosya Lab 08 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- AnimatedSprite sinifi ile nesne yonelimli animasyon
- Durum (state) bazli animasyon yonetimi
- durum_degistir() ile gecis kontrolu
- pygame.sprite.Group kullanimi

Lab: 08 - Animasyon ve Zamanlayicilar
Calisma: 2 - AnimatedSprite Sinifi

Calistirma: uv run python calisma2.py
"""

# --- Lab foyundeki ornek kod ---

import pygame

pygame.init()
ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("AnimatedSprite Sinifi")
saat = pygame.time.Clock()


def sheet_olustur(renkler, boyut=48):
    """Her durum icin farkli renkli frame'ler olusturur."""
    frameler = {}
    for durum, renk_listesi in renkler.items():
        durum_frameleri = []
        for renk in renk_listesi:
            yuzey = pygame.Surface((boyut, boyut))
            yuzey.fill((0, 0, 0))
            yuzey.set_colorkey((0, 0, 0))
            pygame.draw.rect(yuzey, renk, (4, 4, boyut - 8, boyut - 8),
                             border_radius=6)
            durum_frameleri.append(yuzey)
        frameler[durum] = durum_frameleri
    return frameler


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, animasyonlar):
        super().__init__()
        self.animasyonlar = animasyonlar
        self.durum = "idle"
        self.frame_index = 0
        self.animasyon_hizi = 150
        self.son_guncelleme = pygame.time.get_ticks()
        self.image = self.animasyonlar[self.durum][0]
        self.rect = self.image.get_rect(center=(x, y))

    def durum_degistir(self, yeni_durum):
        if yeni_durum != self.durum:
            if yeni_durum in self.animasyonlar:
                self.durum = yeni_durum
                self.frame_index = 0
                self.son_guncelleme = pygame.time.get_ticks()

                # GOREV 3: Durum bazli hiz guncelleme
                # Ipucu:
                #   if yeni_durum in self.animasyon_hizlari:
                #       self.animasyon_hizi = self.animasyon_hizlari[yeni_durum]

    def update(self):
        simdi = pygame.time.get_ticks()
        if simdi - self.son_guncelleme >= self.animasyon_hizi:
            frameler = self.animasyonlar[self.durum]

            # GOREV 1: Death durumunda son frame'de kal
            # Ipucu:
            #   if self.durum == "death":
            #       if self.frame_index < len(frameler) - 1:
            #           self.frame_index += 1
            #   else:
            #       self.frame_index = (self.frame_index + 1) % len(frameler)

            # Normal dongusal animasyon (GOREV 1 yapilinca bu satir kaldirilir)
            self.frame_index = (self.frame_index + 1) % len(frameler)

            self.image = frameler[self.frame_index]
            self.son_guncelleme = simdi


# Durum renkleri tanimla
renkler = {
    "idle":   [(80, 80, 200), (100, 100, 220), (80, 80, 200)],
    "walk":   [(80, 200, 80), (100, 220, 100),
               (120, 240, 120), (100, 220, 100)],
    "attack": [(200, 80, 80), (240, 120, 60), (255, 60, 60)],
}

# GOREV 1: "death" durumu ekleyin (kirmizidan siyaha kararma)
# Ipucu:
#   renkler["death"] = [(200, 50, 50), (120, 30, 30), (40, 10, 10)]

animasyonlar = sheet_olustur(renkler)
oyuncu = AnimatedSprite(300, 200, animasyonlar)

# GOREV 3: Durum bazli animasyon hizlari sozlugu ekleyin
# Ipucu:
#   oyuncu.animasyon_hizlari = {
#       "idle": 300,
#       "walk": 100,
#       "attack": 80,
#       "death": 200,
#   }

grup = pygame.sprite.Group(oyuncu)
font = pygame.font.SysFont("Arial", 18)

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_1:
                oyuncu.durum_degistir("idle")
            elif olay.key == pygame.K_2:
                oyuncu.durum_degistir("walk")
            elif olay.key == pygame.K_3:
                oyuncu.durum_degistir("attack")

            # GOREV 1: 4 tusu ile death durumuna gec
            # Ipucu:
            #   elif olay.key == pygame.K_4:
            #       oyuncu.durum_degistir("death")

            # GOREV 2: SPACE ile attack durumuna gec
            # Ipucu:
            #   elif olay.key == pygame.K_SPACE:
            #       oyuncu.durum_degistir("attack")

    # GOREV 2: Ok tuslari ile hareket ve otomatik durum gecisi
    # Hareket ederken "walk", durdigunda "idle" durumuna gec.
    # Ipucu:
    #   tuslar = pygame.key.get_pressed()
    #   hareket = False
    #   if tuslar[pygame.K_LEFT]:
    #       oyuncu.rect.x -= 3
    #       hareket = True
    #   if tuslar[pygame.K_RIGHT]:
    #       oyuncu.rect.x += 3
    #       hareket = True
    #   if tuslar[pygame.K_UP]:
    #       oyuncu.rect.y -= 3
    #       hareket = True
    #   if tuslar[pygame.K_DOWN]:
    #       oyuncu.rect.y += 3
    #       hareket = True
    #
    #   if oyuncu.durum != "attack" and oyuncu.durum != "death":
    #       if hareket:
    #           oyuncu.durum_degistir("walk")
    #       else:
    #           oyuncu.durum_degistir("idle")

    grup.update()

    ekran.fill((30, 30, 50))
    grup.draw(ekran)
    bilgi = font.render(
        f"Durum: {oyuncu.durum} | Frame: {oyuncu.frame_index} "
        f"| 1: idle  2: walk  3: attack",
        True, (200, 200, 200))
    ekran.blit(bilgi, (20, 20))

    gorev_bilgi = font.render(
        "4: death (GOREV 1) | Ok tuslari: Hareket (GOREV 2)",
        True, (150, 150, 170))
    ekran.blit(gorev_bilgi, (20, 45))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
600x400 piksel boyutunda koyu pencere acilir.
Ortada renkli bir kare (sprite) animasyonu oynar.

1 tusuna basildiginda mavi tonlarinda "idle" animasyonu,
2 tusuna basildiginda yesil tonlarinda "walk" animasyonu,
3 tusuna basildiginda kirmizi tonlarinda "attack" animasyonu oynar.

Ekranda aktif durum ve frame numarasi gosterilir.

GOREV tamamlandiktan sonra:
4 tusu ile "death" durumu aktif olur ve son frame'de kalir.
Ok tuslari ile sprite hareket eder, otomatik durum gecisi olur.
Her durumun kendi animasyon hizi vardir (idle yavas, attack hizli).
"""
