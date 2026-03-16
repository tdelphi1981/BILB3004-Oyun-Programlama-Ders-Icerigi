"""
Tum Girdiler Demo - Klavye ve Fare Birlestirme

Bu program, Bolum 4'te ogrenilen tum girdi yontemlerini
tek bir ornekte birlestirir. Ekrandaki bir kareyi ok tuslari
ile hareket ettirebilir, fare ile yeni konuma isinlayabilir
ve cesitli tus kombinasyonlari ile kontrol edebilirsin.

Kontroller:
- Ok tuslari / WASD: Kareyi hareket ettir
- Sol fare tiklama: Kareyi tiklanan konuma isinla
- Sag fare tiklama: Kare rengini degistir
- Space: Orijinal konuma don
- ESC: Cikis

Ogrenilecek kavramlar:
- key.get_pressed() ile surekli klavye girdisi
- KEYDOWN ile ayrik klavye girdisi
- MOUSEBUTTONDOWN ile fare tiklama
- mouse.get_pos() ile fare konumu
- Tum girdi turlerini birlestirme

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: Genel (tum uniteler)

Calistirma: python tum_girdiler.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 500
FPS = 60
ARKA_PLAN = (20, 20, 35)
KARE_BOYUT = 40
HIZ = 300  # piksel/saniye

# Renkler
RENKLER = [
    (0, 180, 255),    # Mavi
    (255, 100, 80),   # Kirmizi
    (80, 220, 100),   # Yesil
    (255, 200, 60),   # Sari
    (200, 100, 255),  # Mor
]
BEYAZ = (220, 220, 220)
GRI = (100, 100, 100)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Tum Girdiler Demo")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    # Kare baslangic konumu
    baslangic_x = float(GENISLIK // 2 - KARE_BOYUT // 2)
    baslangic_y = float(YUKSEKLIK // 2 - KARE_BOYUT // 2)
    x = baslangic_x
    y = baslangic_y

    renk_index = 0
    son_eylem = "Hazir"

    calistir = True
    while calistir:
        dt = saat.tick(FPS) / 1000.0

        # --- Olaylari isle (ayrik girdi) ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_SPACE:
                    # Orijinal konuma don
                    x = baslangic_x
                    y = baslangic_y
                    son_eylem = "Space: Orijinal konum"

            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if olay.button == 1:
                    # Sol tiklama: tiklanan konuma isinla
                    fare_x, fare_y = olay.pos
                    x = float(fare_x - KARE_BOYUT // 2)
                    y = float(fare_y - KARE_BOYUT // 2)
                    son_eylem = f"Sol tik: ({fare_x}, {fare_y})"
                elif olay.button == 3:
                    # Sag tiklama: renk degistir
                    renk_index = (renk_index + 1) % len(RENKLER)
                    son_eylem = "Sag tik: Renk degisti"

        # --- Surekli girdi (klavye) ---
        tuslar = pygame.key.get_pressed()
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

        if dx != 0 or dy != 0:
            x += dx * HIZ * dt
            y += dy * HIZ * dt
            son_eylem = "Klavye: Hareket"

        # Sinir kontrolu (clamp)
        x = max(0, min(x, GENISLIK - KARE_BOYUT))
        y = max(0, min(y, YUKSEKLIK - KARE_BOYUT))

        # --- Ciz ---
        ekran.fill(ARKA_PLAN)

        # Kareyi ciz
        renk = RENKLER[renk_index]
        pygame.draw.rect(
            ekran, renk,
            (int(x), int(y), KARE_BOYUT, KARE_BOYUT)
        )

        # Bilgi paneli
        bilgiler = [
            "Ok / WASD: Hareket",
            "Sol Tik: Isinla",
            "Sag Tik: Renk Degistir",
            "Space: Orijinal Konum",
            "ESC: Cikis",
        ]
        for i, bilgi in enumerate(bilgiler):
            yazi = font.render(bilgi, True, GRI)
            ekran.blit(yazi, (10, YUKSEKLIK - 120 + i * 22))

        # Son eylem
        eylem_yazi = font.render(f"Son eylem: {son_eylem}", True, BEYAZ)
        ekran.blit(eylem_yazi, (10, 10))

        # Konum bilgisi
        konum_yazi = font.render(
            f"Konum: ({int(x)}, {int(y)})", True, GRI
        )
        ekran.blit(konum_yazi, (GENISLIK - 200, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x500 piksel boyutunda koyu bir pencere acilir.
Ortada mavi bir kare goruntulenir.

- Ok tuslari veya WASD ile kareyi hareket ettir
- Sol fare tiklamasiyla kare tiklanan konuma isinlanir
- Sag fare tiklamasiyla kare rengi degisir (5 renk arasindan)
- Space tusuyla kare orijinal konumuna doner
- ESC ile program kapanir

Sol ust kosede son eylem bilgisi, sag ust kosede konum bilgisi,
alt sol kosede kontrol rehberi gosterilir.
"""
