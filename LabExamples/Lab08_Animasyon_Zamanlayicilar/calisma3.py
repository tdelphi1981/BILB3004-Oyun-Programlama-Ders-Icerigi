"""
Lab 08 - Calisma 3 Baslangic Kodu
Zamanlayicilar ve Cooldown

Bu dosya Lab 08 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Cooldown sinifi ile yetenek zamanlayicilari
- pygame.time.set_timer() ile periyodik olaylar
- USEREVENT tabanli zamanlayici kullanimi
- Gorsel cooldown barlari

Lab: 08 - Animasyon ve Zamanlayicilar
Calisma: 3 - Zamanlayicilar ve Cooldown

Calistirma: uv run python calisma3.py
"""

# --- Lab foyundeki ornek kod ---

import pygame

pygame.init()
ekran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Zamanlayicilar")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)


# Cooldown sinifi
class Cooldown:
    def __init__(self, sure_ms):
        self.sure = sure_ms
        self.son_kullanim = 0

    def hazir_mi(self):
        return pygame.time.get_ticks() - self.son_kullanim >= self.sure

    def kullan(self):
        if self.hazir_mi():
            self.son_kullanim = pygame.time.get_ticks()
            return True
        return False

    def kalan_sure(self):
        gecen = pygame.time.get_ticks() - self.son_kullanim
        kalan = max(0, self.sure - gecen)
        return kalan


# USEREVENT tabanli zamanlayici
DUSMAN_OLAYI = pygame.USEREVENT + 1
dusman_periyot = 2000
pygame.time.set_timer(DUSMAN_OLAYI, dusman_periyot)

# Cooldown'lar
mermi_cd = Cooldown(500)    # 500ms mermi cooldown
kalkan_cd = Cooldown(3000)  # 3s kalkan cooldown

# GOREV 2: Dash cooldown ekleyin
# Ipucu:
#   dash_cd = Cooldown(2000)   # 2s dash cooldown
#   dash_aktif = False
#   dash_bitis = 0
#   NORMAL_HIZ = 4
#   DASH_HIZ = 12  # 3 kati hiz

# GOREV 3: Geri sayim degiskenleri
# Ipucu:
#   geri_sayim = True
#   geri_sayim_baslangic = pygame.time.get_ticks()
#   GERI_SAYIM_SURESI = 3000  # 3 saniye
#   buyuk_font = pygame.font.SysFont("Arial", 72)

# Oyun durumlari
mermiler = []
kalkan_aktif = False
kalkan_bitis = 0
dusman_sayaci = 0
oyuncu_x = 300
oyuncu_hiz = 4

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == DUSMAN_OLAYI:
            dusman_sayaci += 1

            # GOREV 1: Her 5 dalgada bir periyodu azalt
            # 2000ms -> 1500ms -> 1000ms, minimum 500ms
            # Ipucu:
            #   if dusman_sayaci % 5 == 0 and dusman_periyot > 500:
            #       dusman_periyot = max(500, dusman_periyot - 500)
            #       pygame.time.set_timer(DUSMAN_OLAYI, dusman_periyot)

        elif olay.type == pygame.KEYDOWN:

            # GOREV 3: Geri sayim aktifken kontrolleri devre disi birak
            # Ipucu:
            #   if geri_sayim:
            #       continue  # Geri sayim bitene kadar tus girisi yok

            if olay.key == pygame.K_SPACE:
                if mermi_cd.kullan():
                    mermiler.append([oyuncu_x, 340])
            elif olay.key == pygame.K_s:
                if kalkan_cd.kullan():
                    kalkan_aktif = True
                    kalkan_bitis = pygame.time.get_ticks() + 1500

            # GOREV 2: D tusu ile Dash yetenegini aktif edin
            # Dash aktifken oyuncu hizi 3 katina ciksin ve 500ms sursun.
            # Ipucu:
            #   elif olay.key == pygame.K_d:
            #       if dash_cd.kullan():
            #           dash_aktif = True
            #           dash_bitis = pygame.time.get_ticks() + 500

    # GOREV 3: Geri sayim kontrolu
    # Ipucu:
    #   if geri_sayim:
    #       gecen = pygame.time.get_ticks() - geri_sayim_baslangic
    #       if gecen >= GERI_SAYIM_SURESI:
    #           geri_sayim = False
    #
    #       # Geri sayim ekranini ciz
    #       ekran.fill((20, 20, 40))
    #       kalan_sn = 3 - (gecen // 1000)
    #       if kalan_sn > 0:
    #           metin = buyuk_font.render(str(kalan_sn), True, (255, 255, 100))
    #       else:
    #           metin = buyuk_font.render("BASLA!", True, (100, 255, 100))
    #       ekran.blit(metin, (300 - metin.get_width() // 2,
    #                          200 - metin.get_height() // 2))
    #       pygame.display.flip()
    #       saat.tick(60)
    #       continue  # Oyun mantigi ve cizimi atla

    # Ok tuslari ile hareket
    tuslar = pygame.key.get_pressed()

    # GOREV 2: Dash aktifken hizi artir
    # Ipucu:
    #   aktif_hiz = DASH_HIZ if dash_aktif else NORMAL_HIZ

    if tuslar[pygame.K_LEFT]:
        oyuncu_x -= oyuncu_hiz
    if tuslar[pygame.K_RIGHT]:
        oyuncu_x += oyuncu_hiz
    oyuncu_x = max(20, min(580, oyuncu_x))

    # Mermi guncelleme
    for m in mermiler:
        m[1] -= 6
    mermiler = [m for m in mermiler if m[1] > 0]

    # Kalkan suresi kontrolu
    if kalkan_aktif and pygame.time.get_ticks() >= kalkan_bitis:
        kalkan_aktif = False

    # GOREV 2: Dash suresi kontrolu
    # Ipucu:
    #   if dash_aktif and pygame.time.get_ticks() >= dash_bitis:
    #       dash_aktif = False

    # --- Cizim ---
    ekran.fill((20, 20, 40))

    # Oyuncu
    renk = (100, 200, 255) if kalkan_aktif else (50, 150, 255)

    # GOREV 2: Dash aktifken oyuncu rengini degistir
    # Ipucu:
    #   if dash_aktif:
    #       renk = (255, 200, 50)

    pygame.draw.rect(ekran, renk, (oyuncu_x - 15, 340, 30, 30))
    if kalkan_aktif:
        pygame.draw.circle(ekran, (100, 200, 255),
                           (oyuncu_x, 355), 25, 2)

    # Mermiler
    for m in mermiler:
        pygame.draw.rect(ekran, (255, 255, 0), (m[0] - 2, m[1], 4, 10))

    # Bilgi paneli
    mermi_kalan = mermi_cd.kalan_sure()
    kalkan_kalan = kalkan_cd.kalan_sure()
    satirlar = [
        f"SPACE: Mermi ({mermi_kalan}ms) | S: Kalkan ({kalkan_kalan}ms)",
        f"Dusman dalgasi: {dusman_sayaci} | Mermi: {len(mermiler)}",
        f"Kalkan: {'AKTIF' if kalkan_aktif else 'Hazir' if kalkan_cd.hazir_mi() else 'Bekleniyor'}",
    ]

    # GOREV 2: Dash bilgisini panele ekleyin
    # Ipucu:
    #   dash_kalan = dash_cd.kalan_sure()
    #   satirlar.append(
    #       f"D: Dash ({dash_kalan}ms) | "
    #       f"{'AKTIF' if dash_aktif else 'Hazir' if dash_cd.hazir_mi() else 'Bekleniyor'}"
    #   )

    # GOREV 1: Dusman periyot bilgisini ekleyin
    # Ipucu:
    #   satirlar.append(f"Dusman periyodu: {dusman_periyot}ms")

    for i, satir in enumerate(satirlar):
        ekran.blit(font.render(satir, True, (200, 200, 200)),
                   (20, 10 + i * 22))

    # Cooldown barlari
    bar_y = 80

    # Mermi CD
    ekran.blit(font.render("Mermi:", True, (180, 180, 180)), (20, bar_y))
    pygame.draw.rect(ekran, (60, 60, 80), (90, bar_y + 2, 200, 12))
    oran = 1.0 - (mermi_kalan / mermi_cd.sure) if mermi_cd.sure > 0 else 1
    pygame.draw.rect(ekran, (255, 255, 0), (90, bar_y + 2, int(200 * oran), 12))

    # Kalkan CD
    ekran.blit(font.render("Kalkan:", True, (180, 180, 180)), (20, bar_y + 18))
    pygame.draw.rect(ekran, (60, 60, 80), (90, bar_y + 20, 200, 12))
    oran_k = 1.0 - (kalkan_kalan / kalkan_cd.sure) if kalkan_cd.sure > 0 else 1
    pygame.draw.rect(ekran, (100, 200, 255), (90, bar_y + 20, int(200 * oran_k), 12))

    # GOREV 2: Dash cooldown bari ekleyin
    # Ipucu:
    #   ekran.blit(font.render("Dash:", True, (180, 180, 180)),
    #              (20, bar_y + 36))
    #   pygame.draw.rect(ekran, (60, 60, 80), (90, bar_y + 38, 200, 12))
    #   oran_d = 1.0 - (dash_kalan / dash_cd.sure) if dash_cd.sure > 0 else 1
    #   pygame.draw.rect(ekran, (255, 200, 50),
    #                    (90, bar_y + 38, int(200 * oran_d), 12))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN CIKTI (temel kod):
----------------------------
600x400 piksel boyutunda koyu pencere acilir.
Alt kisimda mavi bir oyuncu karesi gorulur.

SPACE: Mermi atar (500ms cooldown).
S: Kalkan aktif eder (1.5s sureli, 3s cooldown).
Sol/Sag ok: Oyuncu hareket eder.

Cooldown barlari mermi ve kalkan icin gorsel gosterge saglar.
Dusman dalgasi sayaci her 2 saniyede bir artar.

GOREV tamamlandiktan sonra:
Her 5 dalgada dusman periyodu azalir (min 500ms).
D tusu ile Dash yetenegini kullanir (3x hiz, 500ms, 2s CD).
Oyun basinda 3 saniyelik geri sayim gorulur.
"""
