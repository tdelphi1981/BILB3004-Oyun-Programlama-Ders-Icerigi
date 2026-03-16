"""
Sahne Cizimi - Painter's Algorithm ile tam sahne olusturma

Bu program tum pygame.draw fonksiyonlarini bir arada kullanarak
tam bir sahne cizer: gokyuzu, gunes, bulutlar, daglar, zemin,
ev ve agaclar. Painter's algorithm (arkadan one cizim sirasi)
prensibini gosterir.

Ogrenilecek kavramlar:
- Painter's algorithm: arkadaki nesneler once cizilir
- Birden fazla draw fonksiyonunu birlestirme
- Sahne katmanlari (arka plan, orta plan, on plan)
- Basit oyun sahnesi tasarimi
- Renk ve konum sabitleri ile duzenli kod yazimi

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 4 - Temel Cizim Islemleri

Calistirma: python 03_sahne_cizimi.py
Gereksinimler: pygame
"""

import pygame
import math

# ============================================================
# Sabitler
# ============================================================
GENISLIK = 900
YUKSEKLIK = 600
BASLIK = "Sahne Cizimi - Painter's Algorithm"
FPS = 60

# Renk paleti - Gokyuzu
GOKYUZU_UST = (70, 130, 200)
GOKYUZU_ALT = (150, 200, 240)

# Renk paleti - Gunes
GUNES_RENK = (255, 220, 50)
GUNES_ISIK = (255, 240, 150)

# Renk paleti - Bulut
BULUT_RENK = (240, 240, 250)
BULUT_GOLGE = (210, 210, 225)

# Renk paleti - Dag
DAG_UZAK = (120, 140, 170)       # Uzak dag (soluk)
DAG_YAKIN = (80, 110, 80)        # Yakin dag (yesil)

# Renk paleti - Zemin
CIMEN_ACIK = (80, 160, 60)
CIMEN_KOYU = (60, 130, 45)
TOPRAK = (139, 105, 65)

# Renk paleti - Ev
EV_DUVAR = (210, 180, 140)
EV_CATI = (160, 50, 40)
EV_CATI_KOYU = (130, 40, 30)
EV_KAPI = (100, 60, 30)
EV_PENCERE = (180, 220, 240)
EV_PENCERE_ISIK = (255, 255, 200)
BACA = (120, 100, 90)

# Renk paleti - Agac
AGAC_GOVDE = (100, 70, 40)
AGAC_YAPRAK = (40, 140, 50)
AGAC_YAPRAK_ACIK = (70, 170, 60)

# Renk paleti - Diger
COL_RENK = (60, 50, 40)
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)


def gokyuzu_ciz(ekran):
    """Gokyuzu gradyanini cizer (ust koyu, alt acik).

    Painter's Algorithm - Katman 1 (en arkada).

    Args:
        ekran: PyGame ekran nesnesi
    """
    # Yatay seritler ile gradyan efekti
    ufuk_y = 350  # Ufuk cizgisi
    for y in range(ufuk_y):
        oran = y / ufuk_y
        r = int(GOKYUZU_UST[0] + (GOKYUZU_ALT[0] - GOKYUZU_UST[0]) * oran)
        g = int(GOKYUZU_UST[1] + (GOKYUZU_ALT[1] - GOKYUZU_UST[1]) * oran)
        b = int(GOKYUZU_UST[2] + (GOKYUZU_ALT[2] - GOKYUZU_UST[2]) * oran)
        pygame.draw.line(ekran, (r, g, b), (0, y), (GENISLIK, y))


def gunes_ciz(ekran):
    """Gunesi ve isik halesini cizer.

    Painter's Algorithm - Katman 2.

    Args:
        ekran: PyGame ekran nesnesi
    """
    gunes_x, gunes_y = 720, 80
    gunes_yaricap = 45

    # Isik halesi (dis daireler, seffaf efekt)
    for i in range(5, 0, -1):
        alfa_yaricap = gunes_yaricap + i * 12
        # Seffaflik icin rengi kademeli olarak aciyoruz
        oran = i / 5
        r = int(255 - (255 - GOKYUZU_UST[0]) * oran * 0.3)
        g = int(240 - (240 - GOKYUZU_UST[1]) * oran * 0.3)
        b = int(150 - (150 - GOKYUZU_UST[2]) * oran * 0.3)
        pygame.draw.circle(ekran, (r, g, b), (gunes_x, gunes_y), alfa_yaricap)

    # Ana gunes
    pygame.draw.circle(ekran, GUNES_RENK, (gunes_x, gunes_y), gunes_yaricap)
    # Parlak merkez
    pygame.draw.circle(ekran, GUNES_ISIK, (gunes_x - 8, gunes_y - 8), 20)


def bulut_ciz(ekran, x, y, boyut=1.0):
    """Bir bulut cizer (ust uste dairelerle).

    Args:
        ekran: PyGame ekran nesnesi
        x: Bulutun merkez x konumu
        y: Bulutun merkez y konumu
        boyut: Olcek carpani (varsayilan 1.0)
    """
    r = int(25 * boyut)
    # Alt golge
    pygame.draw.circle(ekran, BULUT_GOLGE, (x, y + 4), r)
    pygame.draw.circle(ekran, BULUT_GOLGE, (x - int(28 * boyut), y + 6), int(20 * boyut))
    pygame.draw.circle(ekran, BULUT_GOLGE, (x + int(28 * boyut), y + 6), int(20 * boyut))

    # Ust beyaz kisim
    pygame.draw.circle(ekran, BULUT_RENK, (x, y - 5), int(30 * boyut))
    pygame.draw.circle(ekran, BULUT_RENK, (x - int(25 * boyut), y), int(22 * boyut))
    pygame.draw.circle(ekran, BULUT_RENK, (x + int(25 * boyut), y), int(22 * boyut))
    pygame.draw.circle(ekran, BULUT_RENK, (x - int(45 * boyut), y + 3), int(18 * boyut))
    pygame.draw.circle(ekran, BULUT_RENK, (x + int(45 * boyut), y + 3), int(18 * boyut))


def bulutlar_ciz(ekran):
    """Birden fazla bulutu farkli konumlarda cizer.

    Painter's Algorithm - Katman 3.

    Args:
        ekran: PyGame ekran nesnesi
    """
    bulut_ciz(ekran, 150, 100, 1.2)
    bulut_ciz(ekran, 400, 70, 0.9)
    bulut_ciz(ekran, 580, 130, 1.0)


def daglar_ciz(ekran):
    """Uzak ve yakin dag siluetlerini cizer.

    Painter's Algorithm - Katman 4.

    Args:
        ekran: PyGame ekran nesnesi
    """
    ufuk_y = 350

    # Uzak daglar (soluk mavi-gri)
    uzak_dag_noktalari = [
        (0, ufuk_y),
        (80, 260), (160, 290), (250, 230),
        (350, 270), (450, 210), (550, 260),
        (650, 240), (750, 280), (850, 250),
        (GENISLIK, 290), (GENISLIK, ufuk_y),
    ]
    pygame.draw.polygon(ekran, DAG_UZAK, uzak_dag_noktalari)

    # Yakin daglar (koyu yesil)
    yakin_dag_noktalari = [
        (0, ufuk_y),
        (50, 310), (130, 280), (220, 320),
        (320, 290), (430, 330), (520, 300),
        (620, 340), (700, 310), (800, 330),
        (GENISLIK, 320), (GENISLIK, ufuk_y),
    ]
    pygame.draw.polygon(ekran, DAG_YAKIN, yakin_dag_noktalari)


def zemin_ciz(ekran):
    """Zemin alanini (cimen ve toprak yol) cizer.

    Painter's Algorithm - Katman 5.

    Args:
        ekran: PyGame ekran nesnesi
    """
    ufuk_y = 350

    # Ana cimen alani
    pygame.draw.rect(ekran, CIMEN_ACIK, (0, ufuk_y, GENISLIK, YUKSEKLIK - ufuk_y))

    # Koyu cimen seridi (derinlik hissi)
    pygame.draw.rect(ekran, CIMEN_KOYU, (0, ufuk_y, GENISLIK, 30))

    # Toprak yol
    yol_noktalari = [
        (350, YUKSEKLIK),
        (380, ufuk_y + 100),
        (400, ufuk_y + 50),
        (420, ufuk_y + 30),
        (480, ufuk_y + 30),
        (500, ufuk_y + 50),
        (520, ufuk_y + 100),
        (550, YUKSEKLIK),
    ]
    pygame.draw.polygon(ekran, TOPRAK, yol_noktalari)


def agac_ciz(ekran, x, y, boyut=1.0):
    """Bir agac cizer (govde + yaprak kumeleri).

    Args:
        ekran: PyGame ekran nesnesi
        x: Agacin taban merkezi x konumu
        y: Agacin taban y konumu
        boyut: Olcek carpani
    """
    govde_gen = int(12 * boyut)
    govde_yuk = int(50 * boyut)
    yaprak_r = int(30 * boyut)

    # Govde
    pygame.draw.rect(
        ekran, AGAC_GOVDE,
        (x - govde_gen // 2, y - govde_yuk, govde_gen, govde_yuk)
    )

    # Yaprak kumeleri (ust uste daireler)
    yaprak_merkez_y = y - govde_yuk - int(10 * boyut)
    pygame.draw.circle(ekran, AGAC_YAPRAK, (x, yaprak_merkez_y), yaprak_r)
    pygame.draw.circle(
        ekran, AGAC_YAPRAK,
        (x - int(20 * boyut), yaprak_merkez_y + int(10 * boyut)),
        int(25 * boyut)
    )
    pygame.draw.circle(
        ekran, AGAC_YAPRAK,
        (x + int(20 * boyut), yaprak_merkez_y + int(10 * boyut)),
        int(25 * boyut)
    )
    # Acik yesil vurgular
    pygame.draw.circle(
        ekran, AGAC_YAPRAK_ACIK,
        (x - int(5 * boyut), yaprak_merkez_y - int(8 * boyut)),
        int(15 * boyut)
    )


def agaclar_ciz(ekran):
    """Sahneye birden fazla agac ekler.

    Painter's Algorithm - Katman 6.

    Args:
        ekran: PyGame ekran nesnesi
    """
    # Arka plandaki agaclar (kucuk)
    agac_ciz(ekran, 100, 380, 0.7)
    agac_ciz(ekran, 780, 375, 0.6)

    # On plandaki agaclar (buyuk)
    agac_ciz(ekran, 60, 480, 1.2)
    agac_ciz(ekran, 820, 490, 1.3)
    agac_ciz(ekran, 700, 460, 1.0)


def ev_ciz(ekran):
    """Bir ev cizer (duvar, cati, kapi, pencereler, baca).

    Painter's Algorithm - Katman 7.

    Args:
        ekran: PyGame ekran nesnesi
    """
    ev_x = 430
    ev_y = 380
    ev_gen = 140
    ev_yuk = 100

    # Duvar
    pygame.draw.rect(ekran, EV_DUVAR, (ev_x, ev_y, ev_gen, ev_yuk))

    # Duvar cercevesi
    pygame.draw.rect(ekran, COL_RENK, (ev_x, ev_y, ev_gen, ev_yuk), 2)

    # Baca (catidan once cizelim ki arkada kalsin)
    baca_x = ev_x + ev_gen - 35
    baca_y = ev_y - 70
    pygame.draw.rect(ekran, BACA, (baca_x, baca_y, 18, 45))
    pygame.draw.rect(ekran, COL_RENK, (baca_x, baca_y, 18, 45), 1)
    # Baca ustu
    pygame.draw.rect(ekran, COL_RENK, (baca_x - 2, baca_y - 3, 22, 6))

    # Cati (ucgen)
    cati_noktalar = [
        (ev_x - 15, ev_y),
        (ev_x + ev_gen // 2, ev_y - 70),
        (ev_x + ev_gen + 15, ev_y),
    ]
    pygame.draw.polygon(ekran, EV_CATI, cati_noktalar)
    pygame.draw.polygon(ekran, EV_CATI_KOYU, cati_noktalar, 3)

    # Kapi
    kapi_gen = 28
    kapi_yuk = 50
    kapi_x = ev_x + ev_gen // 2 - kapi_gen // 2
    kapi_y = ev_y + ev_yuk - kapi_yuk
    pygame.draw.rect(ekran, EV_KAPI, (kapi_x, kapi_y, kapi_gen, kapi_yuk))
    pygame.draw.rect(ekran, COL_RENK, (kapi_x, kapi_y, kapi_gen, kapi_yuk), 2)
    # Kapi kolu
    pygame.draw.circle(ekran, GUNES_RENK, (kapi_x + 22, kapi_y + 28), 3)

    # Sol pencere
    pencere_boyut = 25
    pygame.draw.rect(
        ekran, EV_PENCERE_ISIK,
        (ev_x + 18, ev_y + 20, pencere_boyut, pencere_boyut)
    )
    pygame.draw.rect(
        ekran, COL_RENK,
        (ev_x + 18, ev_y + 20, pencere_boyut, pencere_boyut), 2
    )
    # Pencere carpraz cizgileri
    pygame.draw.line(
        ekran, COL_RENK,
        (ev_x + 18 + pencere_boyut // 2, ev_y + 20),
        (ev_x + 18 + pencere_boyut // 2, ev_y + 20 + pencere_boyut), 1
    )
    pygame.draw.line(
        ekran, COL_RENK,
        (ev_x + 18, ev_y + 20 + pencere_boyut // 2),
        (ev_x + 18 + pencere_boyut, ev_y + 20 + pencere_boyut // 2), 1
    )

    # Sag pencere
    pygame.draw.rect(
        ekran, EV_PENCERE_ISIK,
        (ev_x + ev_gen - 43, ev_y + 20, pencere_boyut, pencere_boyut)
    )
    pygame.draw.rect(
        ekran, COL_RENK,
        (ev_x + ev_gen - 43, ev_y + 20, pencere_boyut, pencere_boyut), 2
    )
    pygame.draw.line(
        ekran, COL_RENK,
        (ev_x + ev_gen - 43 + pencere_boyut // 2, ev_y + 20),
        (ev_x + ev_gen - 43 + pencere_boyut // 2, ev_y + 20 + pencere_boyut), 1
    )
    pygame.draw.line(
        ekran, COL_RENK,
        (ev_x + ev_gen - 43, ev_y + 20 + pencere_boyut // 2),
        (ev_x + ev_gen - 43 + pencere_boyut, ev_y + 20 + pencere_boyut // 2), 1
    )


def cit_ciz(ekran):
    """Evin onune basit bir cit cizer.

    Painter's Algorithm - Katman 8.

    Args:
        ekran: PyGame ekran nesnesi
    """
    cit_y = 475
    cit_yuk = 30

    # Yatay cit cizgileri
    for baslangic_x, bitis_x in [(300, 420), (580, 700)]:
        # Ust cizgi
        pygame.draw.line(
            ekran, AGAC_GOVDE,
            (baslangic_x, cit_y), (bitis_x, cit_y), 3
        )
        # Alt cizgi
        pygame.draw.line(
            ekran, AGAC_GOVDE,
            (baslangic_x, cit_y + cit_yuk - 5), (bitis_x, cit_y + cit_yuk - 5), 3
        )
        # Dikey cubuklar
        for x in range(baslangic_x, bitis_x + 1, 20):
            pygame.draw.line(
                ekran, AGAC_GOVDE,
                (x, cit_y - 5), (x, cit_y + cit_yuk), 2
            )


def bilgi_paneli_ciz(ekran, font):
    """Ekranin altinda painter's algorithm bilgisini gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    # Yari seffaf panel
    pygame.draw.rect(ekran, (0, 0, 0), (0, YUKSEKLIK - 55, GENISLIK, 55))
    pygame.draw.line(
        ekran, BEYAZ, (0, YUKSEKLIK - 55), (GENISLIK, YUKSEKLIK - 55), 1
    )

    bilgiler = [
        "Painter's Algorithm: Arkadaki nesneler once cizilir, ondekiler uzerine biner.",
        "Cizim sirasi: Gokyuzu -> Gunes -> Bulut -> Dag -> Zemin -> Agac -> Ev -> Cit",
    ]

    kucuk_font = pygame.font.Font(None, 20)
    for i, bilgi in enumerate(bilgiler):
        yazi = kucuk_font.render(bilgi, True, BEYAZ)
        ekran.blit(yazi, (15, YUKSEKLIK - 48 + i * 22))


def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)

    # Font olustur
    font = pygame.font.Font(None, 24)

    # Saat nesnesi
    saat = pygame.time.Clock()

    # Konsola bilgi yazdir
    print("Sahne Cizimi - Painter's Algorithm")
    print("=" * 45)
    print()
    print("Cizim sirasi (arkadan one):")
    print("  1. Gokyuzu (gradyan)")
    print("  2. Gunes (daireler)")
    print("  3. Bulutlar (daire kumeleri)")
    print("  4. Daglar (cokgenler)")
    print("  5. Zemin (dikdortgen + yol)")
    print("  6. Agaclar (govde + yapraklar)")
    print("  7. Ev (duvar, cati, pencere, kapi)")
    print("  8. Cit (cizgiler)")
    print()
    print("ESC ile cikis yapin.")

    # Ana oyun dongusu
    calistir = True

    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # ============================================
        # PAINTER'S ALGORITHM - Arkadan one cizim
        # ============================================

        # Katman 1: Gokyuzu (en arkada)
        gokyuzu_ciz(ekran)

        # Katman 2: Gunes
        gunes_ciz(ekran)

        # Katman 3: Bulutlar
        bulutlar_ciz(ekran)

        # Katman 4: Daglar
        daglar_ciz(ekran)

        # Katman 5: Zemin
        zemin_ciz(ekran)

        # Katman 6: Agaclar (arka plan)
        agaclar_ciz(ekran)

        # Katman 7: Ev
        ev_ciz(ekran)

        # Katman 8: Cit (en onde)
        cit_ciz(ekran)

        # Bilgi paneli
        bilgi_paneli_ciz(ekran, font)

        # Ekrani guncelle
        pygame.display.flip()
        saat.tick(FPS)

    # PyGame'i kapat
    pygame.quit()
    print("\nProgram sonlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
900x600 piksel boyutunda tam bir doga sahnesi goruntulenir:

- Gokyuzu: Ustten alta mavi gradyan
- Gunes: Sag ust kosede parlak sari daire ve isik halesi
- Bulutlar: Uc adet farkli boyutta beyaz bulut
- Daglar: Uzak (mavi-gri) ve yakin (yesil) dag siluetleri
- Zemin: Yesil cimen alani ve kahverengi toprak yol
- Agaclar: 5 adet farkli boyutta agac
- Ev: Bej duvarlar, kirmizi cati, sari isikli pencereler, kahverengi kapi
- Cit: Evin her iki yaninda ahsap cit

Alt panelde Painter's Algorithm aciklamasi ve cizim sirasi gosterilir.
ESC tusuna basinca program kapanir.
"""
