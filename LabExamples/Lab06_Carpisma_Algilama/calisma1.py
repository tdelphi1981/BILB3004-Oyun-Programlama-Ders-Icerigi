"""
Lab 06 - Calisma 1 Baslangic Kodu
Rect Carpismasi ve collidepoint()

Bu dosya Lab 06 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- colliderect() ile dikdortgen carpisma kontrolu
- collidepoint() ile nokta kontrolu
- Carpisma durumuna gore renk degisimi
- Fare etkilesimi

Lab: 06 - Carpisma Algilama ve Fizik Temelleri
Calisma: 1 - Rect Carpismasi ve collidepoint()

Calistirma: uv run python calisma1.py
"""

# --- Lab foyundeki ornek kod ---

import pygame

pygame.init()
GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Rect Carpisma Testi")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Iki dikdortgen
oyuncu = pygame.Rect(100, 250, 60, 60)
engel = pygame.Rect(350, 250, 80, 80)
hiz = 4

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

    # Hareket
    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_LEFT]:
        oyuncu.x -= hiz
    if tuslar[pygame.K_RIGHT]:
        oyuncu.x += hiz
    if tuslar[pygame.K_UP]:
        oyuncu.y -= hiz
    if tuslar[pygame.K_DOWN]:
        oyuncu.y += hiz

    # Carpisma kontrolu
    carpisma = oyuncu.colliderect(engel)

    # Fare nokta kontrolu
    fare_x, fare_y = pygame.mouse.get_pos()
    fare_engelde = engel.collidepoint(fare_x, fare_y)

    # Cizim
    ekran.fill((20, 20, 40))

    renk_engel = (231, 76, 60) if carpisma else (46, 204, 113)
    renk_oyuncu = (231, 76, 60) if carpisma else (52, 152, 219)

    pygame.draw.rect(ekran, renk_engel, engel)
    pygame.draw.rect(ekran, renk_oyuncu, oyuncu)

    # Fare engelin uzerinde mi?
    if fare_engelde:
        pygame.draw.rect(ekran, (241, 196, 15), engel, 3)

    # Bilgi metni
    durum = "CARPISMA VAR!" if carpisma else "Carpisma yok"
    yazi = font.render(durum, True, (255, 255, 255))
    ekran.blit(yazi, (10, 10))

    fare_durum = "Fare engelin uzerinde" if fare_engelde else ""
    if fare_durum:
        yazi2 = font.render(fare_durum, True, (241, 196, 15))
        ekran.blit(yazi2, (10, 40))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 1.1 - Uc Engel Listesi ===
# TODO: a) Tek engel yerine 3 farkli konumda ve boyutta engel
#          olusturun ve bir listeye ekleyin
# TODO: b) for dongusuyle tum engellere karsi carpisma kontrolu
#          yapin
# TODO: c) Carpisilan engelin rengi kirmiziya donsun, digerleri
#          yesil kalsin
# Ipucu:
#   engeller = [
#       pygame.Rect(200, 150, 60, 60),
#       pygame.Rect(400, 300, 100, 50),
#       pygame.Rect(550, 200, 70, 70),
#   ]
#   for e in engeller:
#       if oyuncu.colliderect(e):
#           # kirmizi ciz
# ============================================


# === GOREV 1.2 - Carpisma Sayaci ===
# TODO: a) Her yeni carpisma oldugunda bir sayac artsın
#          (ayni engele tekrar tekrar degmek sayilmamali)
# TODO: b) Sag ust kosede "Carpisma: 5" seklinde toplam
#          carpisma sayisini gosterin
# TODO: c) onceki_carpisma adli bir degiskenle onceki karenin
#          durumunu takip edin
# Ipucu:
#   carpisma_sayisi = 0
#   onceki_carpisma = False
#   # Dongude:
#   if carpisma and not onceki_carpisma:
#       carpisma_sayisi += 1
#   onceki_carpisma = carpisma
# ============================================


# === GOREV 1.3 - Fare ile Engel Ekleme/Silme ===
# TODO: a) MOUSEBUTTONDOWN olayi ile sol tikla yeni engel ekleyin
# TODO: b) Yeni engelin boyutu 40-100 piksel arasi rastgele olsun
# TODO: c) Sag tikla ile fare pozisyonundaki engeli silin
#          (collidepoint() ile hangi engele tiklandigini bulun)
# Ipucu:
#   import random
#   elif olay.type == pygame.MOUSEBUTTONDOWN:
#       if olay.button == 1:  # Sol tik
#           boyut = random.randint(40, 100)
#           yeni = pygame.Rect(olay.pos[0], olay.pos[1],
#                              boyut, boyut)
#           engeller.append(yeni)
#       elif olay.button == 3:  # Sag tik
#           for e in engeller[:]:
#               if e.collidepoint(olay.pos):
#                   engeller.remove(e)
#                   break
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Mavi bir oyuncu karesi ve yesil bir engel karesi gorulur.

Ok tuslari ile oyuncu hareket ettirilir.
Oyuncu engele degdiginde her ikisi de kirmiziya doner
ve sol ustte "CARPISMA VAR!" yazar.

Fare engelin uzerindeyken sari kenarlık belirir ve
"Fare engelin uzerinde" mesaji gosterilir.
"""
