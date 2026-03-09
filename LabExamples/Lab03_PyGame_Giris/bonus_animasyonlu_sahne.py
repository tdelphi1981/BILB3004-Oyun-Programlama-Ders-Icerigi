"""
Lab 03 - Bonus: Animasyonlu Sahne
Manzara Sahnesi + Hareketli Gunes + Gun Batimi Efekti

Lab 03 Calisma 4'un bonus gorevinin cozumu.
Basit bir manzara sahnesi uzerine gunes hareketi
ve gun batimi renk gecisi efekti ekler.

Ozellikler:
- Gunes sola dogru hareket eder ve ekran disina cikinca
  tekrar baslar (wrap-around)
- Gokyuzu rengi gunesin konumuna gore degisir
  (acik mavi -> turuncu/kirmizi)

Lab: 03 - PyGame'e Giris ve Oyun Penceresi
Bonus: Animasyonlu Sahne

Calistirma: uv run python bonus_animasyonlu_sahne.py
Gereksinimler: pygame
"""

import pygame
import sys

pygame.init()

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Animasyonlu Sahne - Gun Batimi")
saat = pygame.time.Clock()

# Renkler
BEYAZ       = (255, 255, 255)
SARI        = (240, 220, 50)
YESIL       = (50, 180, 50)
KOYU_YESIL  = (30, 120, 30)
KAHVERENGI  = (139, 90, 43)
KIRMIZI     = (180, 50, 50)

# Gunes baslangic konumu
gunes_x = 700
gunes_y = 80

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    # --- Gunes hareketi ---
    gunes_x -= 1  # Her karede 1 piksel sola
    if gunes_x < -50:
        gunes_x = GENISLIK + 50  # Tekrar baslat

    # --- Gokyuzu renk degisimi (gun batimi efekti) ---
    oran = gunes_x / GENISLIK  # 0.0 - 1.0
    r = int(135 + (220 - 135) * (1 - oran))
    g = int(206 - (206 - 100) * (1 - oran))
    b = int(235 - (235 - 80) * (1 - oran))
    gokyuzu_renk = (r, g, b)

    # --- Cizim ---
    ekran.fill(gokyuzu_renk)

    # Gunes
    pygame.draw.circle(ekran, SARI, (gunes_x, gunes_y), 40)

    # Zemin (cim)
    pygame.draw.rect(ekran, YESIL, (0, 450, GENISLIK, 150))

    # Ev - duvar
    pygame.draw.rect(ekran, KIRMIZI, (150, 350, 150, 100))
    # Ev - cati (ucgen)
    pygame.draw.polygon(ekran, KAHVERENGI,
        [(130, 350), (225, 280), (320, 350)])
    # Ev - kapi
    pygame.draw.rect(ekran, KAHVERENGI, (200, 400, 40, 50))

    # Agac - govde
    pygame.draw.rect(ekran, KAHVERENGI, (550, 370, 20, 80))
    # Agac - yaprak
    pygame.draw.circle(ekran, KOYU_YESIL, (560, 350), 45)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
sys.exit()


"""
BEKLENEN CIKTI:
----------------------------
800x600 piksel boyutunda bir pencere acilir.
Sahne basit bir manzara icerir: ev, agac, cim ve gunes.
Gunes sola dogru yavaca hareket eder.
Gunes soldayken gokyuzu turuncu/kirmizi tonlarina doner
(gun batimi efekti).
Gunes ekran disina cikinca sagdan tekrar girer.
"""
