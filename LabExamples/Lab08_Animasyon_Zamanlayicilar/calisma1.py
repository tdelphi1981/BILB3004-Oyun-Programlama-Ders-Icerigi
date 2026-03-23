"""
Lab 08 - Calisma 1 Baslangic Kodu
Sprite Sheet Frame Kesme ve Basit Animasyon

Bu dosya Lab 08 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Programatik sprite sheet olusturma
- subsurface ile frame kesme
- Zamana bagli frame degisimi (animasyon)

Lab: 08 - Animasyon ve Zamanlayicilar
Calisma: 1 - Sprite Sheet Frame Kesme ve Basit Animasyon

Calistirma: uv run python calisma1.py
"""

# --- Lab foyundeki ornek kod ---

import pygame
import math

pygame.init()
ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Sprite Sheet Animasyon")
saat = pygame.time.Clock()

# Programatik sprite sheet olustur (4 frame, 64x64 piksel)
FRAME_W, FRAME_H = 64, 64
FRAME_SAYISI = 4
sheet = pygame.Surface((FRAME_W * FRAME_SAYISI, FRAME_H))
sheet.fill((0, 0, 0))
sheet.set_colorkey((0, 0, 0))

for i in range(FRAME_SAYISI):
    x = i * FRAME_W
    # Her frame'de farkli boyutta daire (nabiz efekti)
    yaricap = 15 + i * 5
    pygame.draw.circle(sheet, (50, 200, 255), (x + 32, 32), yaricap)
    # Goz pozisyonlari frame'e gore degisir
    goz_x = 22 + i * 2
    pygame.draw.circle(sheet, (255, 255, 255), (x + goz_x, 24), 5)
    pygame.draw.circle(sheet, (255, 255, 255), (x + goz_x + 18, 24), 5)
    pygame.draw.circle(sheet, (0, 0, 100), (x + goz_x + 1, 24), 2)
    pygame.draw.circle(sheet, (0, 0, 100), (x + goz_x + 19, 24), 2)

# subsurface ile frame'leri kes
frameler = []
for i in range(FRAME_SAYISI):
    cerceve = sheet.subsurface(pygame.Rect(i * FRAME_W, 0, FRAME_W, FRAME_H))
    frameler.append(cerceve)

# Animasyon degiskenleri
aktif_frame = 0
animasyon_hizi = 150  # milisaniye
son_guncelleme = pygame.time.get_ticks()
karakter_x, karakter_y = 268, 168

# GOREV 2: Hareket durumu icin degisken
# Ipucu: hareket_ediyor = False

# GOREV 3: Ping-pong animasyon icin yon degiskeni
# Ipucu: yon = 1  # 1: ileri, -1: geri

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

        # GOREV 1: Animasyon hizi kontrolu
        # Yukari/Asagi ok tuslari ile animasyon_hizi degerini
        # 50-500ms araliginda degistirin.
        # Ipucu:
        #   elif olay.type == pygame.KEYDOWN:
        #       if olay.key == pygame.K_UP:
        #           animasyon_hizi = max(50, animasyon_hizi - 25)
        #       elif olay.key == pygame.K_DOWN:
        #           animasyon_hizi = min(500, animasyon_hizi + 25)

    # GOREV 2: Sol/Sag ok tuslari ile yatay hareket
    # Karakter hareket ederken animasyon calsin,
    # durdigunda yalnizca ilk frame gosterilsin.
    # Ipucu:
    #   tuslar = pygame.key.get_pressed()
    #   hareket_ediyor = False
    #   if tuslar[pygame.K_LEFT]:
    #       karakter_x -= 4
    #       hareket_ediyor = True
    #   if tuslar[pygame.K_RIGHT]:
    #       karakter_x += 4
    #       hareket_ediyor = True

    # Zamana bagli frame degisimi
    simdi = pygame.time.get_ticks()
    if simdi - son_guncelleme >= animasyon_hizi:
        # GOREV 3: Ping-pong animasyon
        # Frame sirasi: 0->1->2->3->2->1->0 seklinde
        # ileri-geri donsun.
        # Ipucu:
        #   aktif_frame += yon
        #   if aktif_frame >= FRAME_SAYISI - 1:
        #       yon = -1
        #   elif aktif_frame <= 0:
        #       yon = 1

        # Normal dongusal animasyon (GOREV 3 yapilinca bu satir kaldirilir)
        aktif_frame = (aktif_frame + 1) % FRAME_SAYISI

        son_guncelleme = simdi

    # GOREV 2: Hareket etmiyorsa ilk frame'i goster
    # Ipucu:
    #   if not hareket_ediyor:
    #       aktif_frame = 0

    ekran.fill((30, 30, 50))

    # Sprite sheet onizleme (ust kisim)
    ekran.blit(sheet, (44, 20))
    for i in range(FRAME_SAYISI):
        renk = (255, 255, 0) if i == aktif_frame else (100, 100, 100)
        pygame.draw.rect(ekran, renk,
                         (44 + i * FRAME_W, 20, FRAME_W, FRAME_H), 2)

    # Aktif frame'i buyuk ciz
    buyuk = pygame.transform.scale(frameler[aktif_frame], (128, 128))
    ekran.blit(buyuk, (karakter_x - 64, karakter_y - 64))

    font = pygame.font.SysFont("Arial", 16)
    bilgi = font.render(f"Frame: {aktif_frame} | Hiz: {animasyon_hizi}ms",
                        True, (200, 200, 200))
    ekran.blit(bilgi, (20, 350))

    gorev_bilgi = font.render(
        "Yukari/Asagi: Hiz | Sol/Sag: Hareket (GOREV 1-2)",
        True, (150, 150, 170))
    ekran.blit(gorev_bilgi, (20, 370))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
600x400 piksel boyutunda koyu pencere acilir.
Ust kisimda 4 frame'lik sprite sheet onizlemesi gorulur.
Aktif frame sari cerceve ile isaretlenir.
Ortada buyutulmus karakter animasyonu oynar.

Frame'ler otomatik olarak 0->1->2->3->0 seklinde doner.
Ekranda aktif frame numarasi ve animasyon hizi gosterilir.

GOREV tamamlandiktan sonra:
Yukari/Asagi ok tuslari ile animasyon hizi degisir (50-500ms).
Sol/Sag ok tuslari ile karakter yatay hareket eder.
Hareket ederken animasyon calar, durunda ilk frame gosterilir.
Ping-pong modu ile frame'ler ileri-geri doner.
"""
