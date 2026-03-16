"""
Sinir Kontrolu Demo - Clamp, Wrap ve Bounce stratejileri

Bu program, uc farkli sinir kontrol stratejisini ayni anda
gosterir. Uc top otomatik olarak hareket eder:
- Mavi top: Clamp (sinirda durur)
- Yesil top: Wrap (diger taraftan cikar)
- Kirmizi top: Bounce (geri seker)

Ogrenilecek kavramlar:
- Clamp: max/min ile sinir kontrolu
- Wrap: ekranin diger tarafindan cikma
- Bounce: hiz yonunu tersine cevirme
- Uc strateji karsilastirmasi

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 4 - Hareket Mekanigi

Calistirma: python 02_sinir_kontrolu.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 500
FPS = 60
ARKA_PLAN = (20, 20, 40)
TOP_YARICAP = 15

# Top renkleri
MAVI = (60, 140, 255)       # Clamp
YESIL = (60, 220, 100)      # Wrap
KIRMIZI = (255, 80, 80)     # Bounce

# Etiket rengi
BEYAZ = (220, 220, 220)
GRI = (100, 100, 100)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Sinir Kontrolu Demo")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # --- Clamp topu (mavi) ---
    clamp_x = 100.0
    clamp_y = 120.0
    clamp_vx = 180.0
    clamp_vy = 120.0

    # --- Wrap topu (yesil) ---
    wrap_x = 400.0
    wrap_y = 250.0
    wrap_vx = 220.0
    wrap_vy = -100.0

    # --- Bounce topu (kirmizi) ---
    bounce_x = 600.0
    bounce_y = 380.0
    bounce_vx = 160.0
    bounce_vy = 200.0

    calistir = True
    while calistir:
        dt = saat.tick(FPS) / 1000.0

        # Olaylari isle
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- CLAMP guncelle ---
        clamp_x += clamp_vx * dt
        clamp_y += clamp_vy * dt
        clamp_x = max(TOP_YARICAP, min(clamp_x, GENISLIK - TOP_YARICAP))
        clamp_y = max(TOP_YARICAP, min(clamp_y, YUKSEKLIK - TOP_YARICAP))

        # --- WRAP guncelle ---
        wrap_x += wrap_vx * dt
        wrap_y += wrap_vy * dt
        # Yatay sarmalama
        if wrap_x > GENISLIK + TOP_YARICAP:
            wrap_x = -TOP_YARICAP
        elif wrap_x < -TOP_YARICAP:
            wrap_x = GENISLIK + TOP_YARICAP
        # Dikey sarmalama
        if wrap_y > YUKSEKLIK + TOP_YARICAP:
            wrap_y = -TOP_YARICAP
        elif wrap_y < -TOP_YARICAP:
            wrap_y = YUKSEKLIK + TOP_YARICAP

        # --- BOUNCE guncelle ---
        bounce_x += bounce_vx * dt
        bounce_y += bounce_vy * dt
        # Yatay sinir
        if bounce_x <= TOP_YARICAP:
            bounce_x = TOP_YARICAP
            bounce_vx = -bounce_vx
        elif bounce_x >= GENISLIK - TOP_YARICAP:
            bounce_x = GENISLIK - TOP_YARICAP
            bounce_vx = -bounce_vx
        # Dikey sinir
        if bounce_y <= TOP_YARICAP:
            bounce_y = TOP_YARICAP
            bounce_vy = -bounce_vy
        elif bounce_y >= YUKSEKLIK - TOP_YARICAP:
            bounce_y = YUKSEKLIK - TOP_YARICAP
            bounce_vy = -bounce_vy

        # --- Ciz ---
        ekran.fill(ARKA_PLAN)

        # Ekran siniri goster
        pygame.draw.rect(ekran, GRI, (0, 0, GENISLIK, YUKSEKLIK), 2)

        # Toplari ciz
        pygame.draw.circle(ekran, MAVI, (int(clamp_x), int(clamp_y)), TOP_YARICAP)
        pygame.draw.circle(ekran, YESIL, (int(wrap_x), int(wrap_y)), TOP_YARICAP)
        pygame.draw.circle(ekran, KIRMIZI, (int(bounce_x), int(bounce_y)), TOP_YARICAP)

        # Etiketler
        clamp_etiket = font.render("CLAMP (sinirda durur)", True, MAVI)
        wrap_etiket = font.render("WRAP (karsi taraftan cikar)", True, YESIL)
        bounce_etiket = font.render("BOUNCE (geri seker)", True, KIRMIZI)

        ekran.blit(clamp_etiket, (10, YUKSEKLIK - 80))
        ekran.blit(wrap_etiket, (10, YUKSEKLIK - 55))
        ekran.blit(bounce_etiket, (10, YUKSEKLIK - 30))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x500 piksel boyutunda koyu bir pencere acilir.
Uc farkli renkte top otomatik olarak hareket eder:
- Mavi top (CLAMP): Ekran sinirina ulastiginda durur.
- Yesil top (WRAP): Bir kenardan cikip karsi kenardan girer.
- Kirmizi top (BOUNCE): Sinira carptiginda geri seker.
Alt kismda her stratejinin etiketi gosterilir.
ESC ile cikabilirsin.
"""
