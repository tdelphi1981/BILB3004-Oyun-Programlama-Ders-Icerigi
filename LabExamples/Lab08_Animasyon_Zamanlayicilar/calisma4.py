"""
Lab 08 - Calisma 4 Baslangic Kodu
Gorsel Efektler

Bu dosya Lab 08 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Parcacik sistemi (Parcacik sinifi)
- Patlama efekti olusturma
- Screen shake efekti
- Delta time (dt) ile fizik guncelleme

Lab: 08 - Animasyon ve Zamanlayicilar
Calisma: 4 - Gorsel Efektler

Calistirma: uv run python calisma4.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import random
import math

pygame.init()
GENISLIK, YUKSEKLIK = 600, 400
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Gorsel Efektler")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)


class Parcacik:
    def __init__(self, x, y, renk, hiz_x, hiz_y, omur):
        self.x, self.y = x, y
        self.renk = renk
        self.hiz_x, self.hiz_y = hiz_x, hiz_y
        self.omur = omur         # toplam omur (ms)
        self.kalan = omur
        self.yaricap = random.randint(2, 5)

    def guncelle(self, dt):
        self.x += self.hiz_x * dt
        self.y += self.hiz_y * dt
        self.hiz_y += 80 * dt  # yercekimi
        self.kalan -= dt * 1000
        return self.kalan > 0

    def ciz(self, yuzey):
        oran = max(0, self.kalan / self.omur)
        r = max(1, int(self.yaricap * oran))
        renk = (min(255, self.renk[0]),
                min(255, self.renk[1]),
                min(255, self.renk[2]))
        pygame.draw.circle(yuzey, renk, (int(self.x), int(self.y)), r)


def patlama_olustur(x, y, renk=(255, 150, 50), adet=25):
    parcaciklar = []
    for _ in range(adet):
        aci = random.uniform(0, 2 * math.pi)
        hiz = random.uniform(50, 200)
        hx = math.cos(aci) * hiz
        hy = math.sin(aci) * hiz
        r = (min(255, renk[0] + random.randint(-30, 30)),
             min(255, renk[1] + random.randint(-30, 30)),
             min(255, max(0, renk[2] + random.randint(-30, 30))))
        omur = random.randint(300, 800)
        parcaciklar.append(Parcacik(x, y, r, hx, hy, omur))
    return parcaciklar


# GOREV 2: Kivilcim parcaciklari icin fonksiyon
# Fare hareket ettikce kucuk kivilcimlar biraksin.
# Ipucu:
#   def kivilcim_olustur(x, y, adet=3):
#       parcaciklar = []
#       for _ in range(adet):
#           aci = random.uniform(0, 2 * math.pi)
#           hiz = random.uniform(20, 80)
#           hx = math.cos(aci) * hiz
#           hy = math.sin(aci) * hiz - 30  # hafif yukari
#           renk = (255, random.randint(150, 255), random.randint(0, 100))
#           omur = random.randint(200, 400)
#           p = Parcacik(x, y, renk, hx, hy, omur)
#           p.yaricap = random.randint(1, 3)  # daha kucuk
#           parcaciklar.append(p)
#       return parcaciklar


# Screen shake
shake_suresi = 0
shake_siddet = 0


def shake_baslat(sure_ms=200, siddet=8):
    global shake_suresi, shake_siddet
    shake_suresi = sure_ms
    shake_siddet = siddet


# Oyun nesneleri
parcaciklar = []
kutular = []

# GOREV 1: Renk bazli kutular
# Her kutuya rastgele renk atayin.
# Ipucu:
#   KUTU_RENKLERI = [
#       (200, 60, 60),    # Kirmizi
#       (60, 200, 60),    # Yesil
#       (60, 60, 200),    # Mavi
#       (200, 200, 60),   # Sari
#   ]

for _ in range(5):
    kx = random.randint(50, GENISLIK - 50)
    ky = random.randint(100, YUKSEKLIK - 100)
    kutular.append(pygame.Rect(kx, ky, 30, 30))

# GOREV 1: Kutulari dict olarak saklayin (rect + renk)
# Ipucu:
#   kutular = []
#   for _ in range(5):
#       kx = random.randint(50, GENISLIK - 50)
#       ky = random.randint(100, YUKSEKLIK - 100)
#       kutular.append({
#           "rect": pygame.Rect(kx, ky, 30, 30),
#           "renk": random.choice(KUTU_RENKLERI),
#       })

# GOREV 3: Zincirleme patlama icin gecikme listesi
# Ipucu:
#   gecikmeli_patlamalar = []  # [(patlama_zamani, x, y, renk), ...]

calistir = True
while calistir:
    dt = saat.tick(60) / 1000.0

    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.MOUSEBUTTONDOWN:
            mx, my = olay.pos
            vuruldu = False
            for kutu in kutular[:]:
                # GOREV 1: dict kullanimina gecince kutu["rect"] kullanin
                if kutu.collidepoint(mx, my):
                    parcaciklar.extend(
                        patlama_olustur(kutu.centerx, kutu.centery))
                    kutular.remove(kutu)
                    shake_baslat(150, 6)
                    vuruldu = True

                    # GOREV 1: Kutunun renginde patlama
                    # Ipucu:
                    #   parcaciklar.extend(
                    #       patlama_olustur(kutu["rect"].centerx,
                    #                      kutu["rect"].centery,
                    #                      kutu["renk"]))

                    # GOREV 3: Yakin kutulari bul ve gecikmeli patlama ekle
                    # Ipucu:
                    #   for diger in kutular[:]:
                    #       if diger == kutu:
                    #           continue
                    #       dx = kutu["rect"].centerx - diger["rect"].centerx
                    #       dy = kutu["rect"].centery - diger["rect"].centery
                    #       mesafe = math.sqrt(dx*dx + dy*dy)
                    #       if mesafe < 80:
                    #           gecikmeli_patlamalar.append((
                    #               pygame.time.get_ticks() + 300,
                    #               diger["rect"].centerx,
                    #               diger["rect"].centery,
                    #               diger["renk"],
                    #               diger
                    #           ))

                    break
            if not vuruldu:
                # Kucuk efekt
                parcaciklar.extend(
                    patlama_olustur(mx, my, (100, 100, 255), 8))

        # GOREV 2: Fare hareketi ile kivilcim izi
        # Ipucu:
        #   elif olay.type == pygame.MOUSEMOTION:
        #       mx, my = olay.pos
        #       parcaciklar.extend(kivilcim_olustur(mx, my))

    # GOREV 3: Gecikmeli patlamalari kontrol et
    # Ipucu:
    #   simdi = pygame.time.get_ticks()
    #   for patlama in gecikmeli_patlamalar[:]:
    #       zaman, px, py, prenk, kutu_ref = patlama
    #       if simdi >= zaman:
    #           parcaciklar.extend(patlama_olustur(px, py, prenk, 30))
    #           if kutu_ref in kutular:
    #               kutular.remove(kutu_ref)
    #           shake_baslat(200, 8)  # Artan siddet
    #           gecikmeli_patlamalar.remove(patlama)

    # Parcacik guncelleme
    parcaciklar = [p for p in parcaciklar if p.guncelle(dt)]

    # Kutu yenileme
    if not kutular:
        for _ in range(5):
            kx = random.randint(50, GENISLIK - 50)
            ky = random.randint(100, YUKSEKLIK - 100)
            kutular.append(pygame.Rect(kx, ky, 30, 30))

        # GOREV 1: Dict formatinda yenileme
        # Ipucu:
        #   if not kutular:
        #       for _ in range(5):
        #           kx = random.randint(50, GENISLIK - 50)
        #           ky = random.randint(100, YUKSEKLIK - 100)
        #           kutular.append({
        #               "rect": pygame.Rect(kx, ky, 30, 30),
        #               "renk": random.choice(KUTU_RENKLERI),
        #           })

    # Screen shake guncelle
    offset_x, offset_y = 0, 0
    if shake_suresi > 0:
        shake_suresi -= dt * 1000
        offset_x = random.randint(-shake_siddet, shake_siddet)
        offset_y = random.randint(-shake_siddet, shake_siddet)

    # --- Cizim ---
    ekran.fill((20, 20, 40))
    cizim_yuzey = pygame.Surface((GENISLIK, YUKSEKLIK))
    cizim_yuzey.fill((20, 20, 40))

    # Kutular
    for kutu in kutular:
        # GOREV 1: Dict formatinda cizim
        # Ipucu:
        #   pygame.draw.rect(cizim_yuzey, kutu["renk"], kutu["rect"],
        #                    border_radius=4)
        #   # Parlak kenar
        #   parlak = tuple(min(255, c + 50) for c in kutu["renk"])
        #   pygame.draw.rect(cizim_yuzey, parlak, kutu["rect"], 2,
        #                    border_radius=4)

        # Temel kutu cizimi (GOREV 1 yapilinca bu blok kaldirilir)
        pygame.draw.rect(cizim_yuzey, (200, 60, 60), kutu,
                         border_radius=4)
        pygame.draw.rect(cizim_yuzey, (255, 100, 100), kutu, 2,
                         border_radius=4)

    # Parcaciklar
    for p in parcaciklar:
        p.ciz(cizim_yuzey)

    # Bilgi
    bilgi = font.render(
        f"Tiklayarak kutulari patlat! | Parcacik: {len(parcaciklar)} "
        f"| Kutu: {len(kutular)}", True, (200, 200, 200))
    cizim_yuzey.blit(bilgi, (20, 10))

    gorev_bilgi = font.render(
        "GOREV 1: Renkli kutular | GOREV 2: Kivilcim izi | GOREV 3: Zincir",
        True, (150, 150, 170))
    cizim_yuzey.blit(gorev_bilgi, (20, 30))

    # Shake offset ile ciz
    ekran.blit(cizim_yuzey, (offset_x, offset_y))
    pygame.display.flip()

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
600x400 piksel boyutunda koyu pencere acilir.
5 adet kirmizi kutu rastgele konumlarda gorulur.

Fare ile bir kutuya tiklandiginda:
- Turuncu patlama parcaciklari olusur
- Screen shake efekti hissedilir
- Kutu yok olur

Bos alana tiklandiginda kucuk mavi parcacik efekti olusur.
Tum kutular yok edildiginde 5 yeni kutu belirir.

GOREV tamamlandiktan sonra:
Her kutu farkli renkte olur ve patlama o renkte gerceklesir.
Fare hareket ettikce kivilcim izi birakilir.
Yakin kutular 300ms gecikme ile zincirleme patlar.
"""
