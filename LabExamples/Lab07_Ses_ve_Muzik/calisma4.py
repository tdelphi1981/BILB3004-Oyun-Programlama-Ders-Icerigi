"""
Lab 07 - Calisma 4 Baslangic Kodu
Mini Proje: Hedef Vurma

Bu dosya Lab 07 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Oyun ici ses efektleri kullanimi
- SesYoneticisi sinifi ile ses organizasyonu
- Kanal planlama ve yonetimi
- Mesafe hesabi ile isabet kontrolu

Lab: 07 - Ses ve Muzik
Calisma: 4 - Mini Proje: Hedef Vurma

Calistirma: uv run python calisma4.py
"""

import pygame
import array
import random
import math

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.set_num_channels(8)

GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Hedef Vurma")
font = pygame.font.SysFont("Arial", 20)
buyuk_font = pygame.font.SysFont("Arial", 36)
saat = pygame.time.Clock()


def ses_olustur(frekans=440, sure_ms=300):
    """Verilen frekans ve surede kare dalga ses olusturur."""
    ornekleme = 44100
    ornek_sayisi = int(ornekleme * sure_ms / 1000)
    buf = array.array('h')
    periyot = max(1, int(ornekleme / frekans))
    for i in range(ornek_sayisi):
        zarf = 1.0 - (i / ornek_sayisi)
        deger = int(3000 * zarf)
        buf.append(deger if (i % periyot) < (periyot // 2) else -deger)
    return pygame.mixer.Sound(buffer=buf)


# --- Temel sesler (GOREV 2 ve 3 icin kullanilacak) ---
# Ornek: tek bir ses olustur (temel calisan kod icin)
temel_ses = ses_olustur(600, 200)

# GOREV 2: 3 farkli ses efekti olusturun
# Ipucu:
#   isabet_ses = ses_olustur(800, 150)    # Yuksek ve kisa
#   iskalama_ses = ses_olustur(200, 300)  # Alcak ve uzun
#   combo_ses = ses_olustur(1000, 400)    # Cok yuksek, uzun

# GOREV 3: SesYoneticisi sinifi
# Ipucu:
#   class SesYoneticisi:
#       def __init__(self):
#           self.sesler = {}
#
#       def ekle(self, ad, ses):
#           """Ses sozluge ekler."""
#           self.sesler[ad] = ses
#
#       def cal(self, ad, loops=0):
#           """Adina gore ses calar."""
#           if ad in self.sesler:
#               self.sesler[ad].play(loops=loops)
#
#       def volume_ayarla(self, ad, volume):
#           """Belirli bir sesin volume'unu ayarlar."""
#           if ad in self.sesler:
#               self.sesler[ad].set_volume(volume)
#
#       def tumu_durdur(self):
#           """Tum sesleri durdurur."""
#           pygame.mixer.stop()
#
#   ses_yon = SesYoneticisi()
#   ses_yon.ekle("isabet", isabet_ses)
#   ses_yon.ekle("iskalama", iskalama_ses)
#   ses_yon.ekle("combo", combo_ses)

# GOREV 4: Kanal planlama
# Ipucu:
#   kanal_vurus = [pygame.mixer.Channel(0), pygame.mixer.Channel(1)]
#   kanal_ui = pygame.mixer.Channel(2)
#   kanal_arkaplan = pygame.mixer.Channel(3)
#   vurus_sirasi = 0  # Vurus kanallari arasinda dongusel kullanim
#
#   # Geri sayim sesi ve olay
#   GERISAYIM_BITTI = pygame.USEREVENT + 1
#   kanal_ui.set_endevent(GERISAYIM_BITTI)
#   geri_sayim_ses = ses_olustur(440, 2000)
#   oyun_basladi = False

# --- Oyun degiskenleri ---
HEDEF_YARICAP = 25
skor = 0
art_arda_isabet = 0


def yeni_hedef():
    """Rastgele konumda yeni hedef olusturur."""
    x = random.randint(HEDEF_YARICAP + 50, GENISLIK - HEDEF_YARICAP - 50)
    y = random.randint(HEDEF_YARICAP + 80, YUKSEKLIK - HEDEF_YARICAP - 50)
    return (x, y)


hedef = yeni_hedef()

# GOREV 1: Birden fazla hedef icin liste olusturun
# Ipucu:
#   hedefler = [yeni_hedef() for _ in range(3)]


calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

        elif olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
            fare_x, fare_y = olay.pos

            # Tek hedef icin mesafe kontrolu
            mesafe = math.sqrt(
                (fare_x - hedef[0]) ** 2 + (fare_y - hedef[1]) ** 2
            )

            if mesafe <= HEDEF_YARICAP:
                # Isabet!
                skor += 1
                art_arda_isabet += 1
                hedef = yeni_hedef()
                temel_ses.play()

                # GOREV 2: Farkli ses efektleri cal
                # Ipucu:
                #   if art_arda_isabet >= 3 and art_arda_isabet % 3 == 0:
                #       combo_ses.play()
                #   else:
                #       isabet_ses.play()

                # GOREV 3: SesYoneticisi ile cal
                # Ipucu:
                #   if art_arda_isabet >= 3 and art_arda_isabet % 3 == 0:
                #       ses_yon.cal("combo")
                #   else:
                #       ses_yon.cal("isabet")

                # GOREV 4: Kanal uzerinden cal
                # Ipucu:
                #   kanal_vurus[vurus_sirasi].play(isabet_ses)
                #   vurus_sirasi = (vurus_sirasi + 1) % 2
            else:
                # Iskalama
                art_arda_isabet = 0

                # GOREV 2: Iskalama sesi cal
                # Ipucu: iskalama_ses.play()

                # GOREV 3: SesYoneticisi ile cal
                # Ipucu: ses_yon.cal("iskalama")

        # GOREV 4: Geri sayim bitis olayini yakala
        # Ipucu:
        #   elif olay.type == GERISAYIM_BITTI:
        #       oyun_basladi = True

    # GOREV 1: Birden fazla hedef icin isabet kontrolunu
    #          dongu ile yapin
    # Ipucu:
    #   for i, h in enumerate(hedefler):
    #       mesafe = math.sqrt(
    #           (fare_x - h[0]) ** 2 + (fare_y - h[1]) ** 2)
    #       if mesafe <= HEDEF_YARICAP:
    #           hedefler[i] = yeni_hedef()
    #           skor += 1
    #           break

    # --- Cizim ---
    ekran.fill((15, 15, 30))

    # Baslik
    baslik = buyuk_font.render("Hedef Vurma", True, (255, 255, 255))
    ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 10))

    # Skor
    skor_yazi = font.render(f"Skor: {skor}", True, (255, 255, 255))
    ekran.blit(skor_yazi, (20, 20))

    # Combo gostergesi
    if art_arda_isabet >= 3:
        combo_yazi = font.render(
            f"COMBO x{art_arda_isabet}!", True, (255, 200, 50)
        )
        ekran.blit(combo_yazi, (20, 50))

    # Hedef cizimi
    pygame.draw.circle(ekran, (200, 50, 50), hedef, HEDEF_YARICAP)
    pygame.draw.circle(ekran, (255, 100, 100), hedef, HEDEF_YARICAP - 8)
    pygame.draw.circle(ekran, (255, 200, 200), hedef, 5)

    # GOREV 1: Birden fazla hedefi cizdirin
    # Ipucu:
    #   for h in hedefler:
    #       pygame.draw.circle(ekran, (200, 50, 50), h, HEDEF_YARICAP)
    #       pygame.draw.circle(ekran, (255, 100, 100), h,
    #                          HEDEF_YARICAP - 8)
    #       pygame.draw.circle(ekran, (255, 200, 200), h, 5)

    # Nisan gostergesi (fare pozisyonunda)
    fare_pos = pygame.mouse.get_pos()
    pygame.draw.line(
        ekran, (100, 200, 100),
        (fare_pos[0] - 10, fare_pos[1]),
        (fare_pos[0] + 10, fare_pos[1]), 1
    )
    pygame.draw.line(
        ekran, (100, 200, 100),
        (fare_pos[0], fare_pos[1] - 10),
        (fare_pos[0], fare_pos[1] + 10), 1
    )

    # Alt bilgi
    bilgi = font.render(
        "Fare ile hedeflere tiklayin!", True, (150, 150, 170)
    )
    ekran.blit(bilgi, (GENISLIK // 2 - bilgi.get_width() // 2,
                       YUKSEKLIK - 35))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu pencere acilir.
"Hedef Vurma" basligi ve skor gosterilir.
Kirmizi bir hedef dairesi rastgele konumda belirir.

Fare ile hedefe tiklandiginda:
- "bip" sesi duyulur
- Skor 1 artar
- Hedef yeni konuma gider

Iskalama durumunda ses yoktur (combo sifirlanir).
Art arda 3+ isabet yapildiginda "COMBO" yazisi gosterilir.

GOREV tamamlandiktan sonra:
3 farkli ses efekti (isabet, iskalama, combo) duyulur.
SesYoneticisi sinifi ile sesler yonetilir.
Kanallar kategorize edilir ve geri sayim ile oyun baslar.
"""
