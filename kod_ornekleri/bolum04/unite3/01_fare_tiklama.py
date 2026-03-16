"""
Fare Tiklama ile Daire Olusturma

Sol tiklama ile ekrana rastgele renkli daireler eklenir.
Sag tiklama ile son eklenen daire silinir.

Ogrenilecek kavramlar:
- MOUSEBUTTONDOWN olayi
- olay.pos ve olay.button ozellikleri
- Fare dugme numaralari (1=sol, 3=sag)
- Liste ile nesne yonetimi

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 3 - Fare Girdileri

Calistirma: python 01_fare_tiklama.py
Gereksinimler: pygame
"""

import pygame
import random

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
BASLIK = "Fare Tiklama - Daire Olusturma"
FPS = 60

ARKA_PLAN = (20, 20, 35)
MIN_YARICAP = 10
MAX_YARICAP = 30


def rastgele_renk():
    """Rastgele bir RGB renk tuple dondurur."""
    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255),
    )


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Daireleri saklayan liste
    # Her eleman: {"konum": (x, y), "renk": (r, g, b), "yaricap": int}
    daireler = []

    calistir = True
    while calistir:
        # --- Olay isleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if olay.button == 1:
                    # Sol tiklama: yeni daire ekle
                    yeni_daire = {
                        "konum": olay.pos,
                        "renk": rastgele_renk(),
                        "yaricap": random.randint(MIN_YARICAP, MAX_YARICAP),
                    }
                    daireler.append(yeni_daire)

                elif olay.button == 3:
                    # Sag tiklama: son daireyi sil
                    if daireler:
                        daireler.pop()

        # --- Cizim ---
        ekran.fill(ARKA_PLAN)

        # Tum daireleri ciz
        for daire in daireler:
            pygame.draw.circle(
                ekran,
                daire["renk"],
                daire["konum"],
                daire["yaricap"],
            )

        # Bilgi metni
        font = pygame.font.Font(None, 24)
        bilgi = f"Daire sayisi: {len(daireler)} | Sol: Ekle | Sag: Sil"
        metin = font.render(bilgi, True, (200, 200, 200))
        ekran.blit(metin, (10, 10))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu bir pencere acilir.
Sol tiklama yapildiginda tiklanan konumda rastgele renkli
ve boyutlu bir daire belirir.
Sag tiklama yapildiginda en son eklenen daire kaybolur.
Sol ust kosede daire sayisi ve kontrol bilgisi gosterilir.
"""
