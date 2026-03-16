"""
Hiz Tabanli Hareket - Delta time ve hiz vektoru ornegi

Bu program, ok tuslariyla kontrol edilen bir topu ekranda
hareket ettirir. Hiz piksel/saniye cinsinden tanimlanir ve
delta time ile carpilarak frame-bagimsiz hareket saglanir.
Capraz hareket normalizasyonu uygulanir.

Ogrenilecek kavramlar:
- Hiz vektoru (vx, vy) bilesenleri
- Delta time ile frame-bagimsiz hareket
- Capraz hareket normalizasyonu
- key.get_pressed() ile surekli girdi

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 4 - Hareket Mekanigi

Calistirma: python 01_hiz_hareket.py
Gereksinimler: pygame
"""

import pygame
import math

# Sabitler
GENISLIK = 800
YUKSEKLIK = 500
FPS = 60
ARKA_PLAN = (15, 15, 35)
TOP_RENK = (0, 180, 255)
TOP_YARICAP = 20
HIZ = 250  # piksel/saniye


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Hiz Tabanli Hareket")
    saat = pygame.time.Clock()

    # Topun baslangic konumu (ekran ortasi)
    x = float(GENISLIK // 2)
    y = float(YUKSEKLIK // 2)

    calistir = True
    while calistir:
        # Delta time hesapla
        dt = saat.tick(FPS) / 1000.0

        # Olaylari isle
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Surekli tus durumunu oku
        tuslar = pygame.key.get_pressed()

        # Yon vektorunu belirle
        dx = 0.0
        dy = 0.0
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            dx = -1.0
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            dx = 1.0
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            dy = -1.0
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            dy = 1.0

        # Capraz hareket normalizasyonu
        uzunluk = math.sqrt(dx * dx + dy * dy)
        if uzunluk > 0:
            dx /= uzunluk
            dy /= uzunluk

        # Konum guncelle (hiz * dt)
        x += dx * HIZ * dt
        y += dy * HIZ * dt

        # Sinir kontrolu (clamp)
        x = max(TOP_YARICAP, min(x, GENISLIK - TOP_YARICAP))
        y = max(TOP_YARICAP, min(y, YUKSEKLIK - TOP_YARICAP))

        # Ciz
        ekran.fill(ARKA_PLAN)
        pygame.draw.circle(ekran, TOP_RENK, (int(x), int(y)), TOP_YARICAP)
        pygame.display.flip()

        # Pencere basliginda bilgi goster
        gercek_vx = dx * HIZ
        gercek_vy = dy * HIZ
        pygame.display.set_caption(
            f"Hiz Tabanli Hareket | "
            f"vx: {gercek_vx:.0f} vy: {gercek_vy:.0f} | "
            f"X: {x:.0f} Y: {y:.0f} | "
            f"FPS: {saat.get_fps():.0f}"
        )

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x500 piksel boyutunda koyu bir pencere acilir.
Ortada mavi bir top (daire) goruntulenir.
Ok tuslari veya WASD ile topu hareket ettirebilirsin.
Capraz hareket normalizasyonu sayesinde capraz yonde de
ayni hiz korunur.
Pencere basliginda anlik hiz bilesenleri, konum ve FPS gosterilir.
ESC ile cikabilirsin.
"""
