"""
Temel Sekil Cizimleri - pygame.draw fonksiyonlari

Bu program pygame.draw modulundeki temel cizim fonksiyonlarini
gosterir: dikdortgen, daire, cizgi, elips ve cokgen. Her sekil
hem dolu hem de cerceve (outline) olarak cizilir.

Ogrenilecek kavramlar:
- pygame.draw.rect() ile dikdortgen cizme
- pygame.draw.circle() ile daire cizme
- pygame.draw.line() ve lines() ile cizgi cizme
- pygame.draw.ellipse() ile elips cizme
- pygame.draw.polygon() ile cokgen cizme
- Dolu vs cerceve (width parametresi)
- pygame.draw.aaline() ile yumusatilmis cizgi

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 4 - Temel Cizim Islemleri

Calistirma: python 02_temel_sekiller.py
Gereksinimler: pygame
"""

import pygame
import math

# ============================================================
# Sabitler
# ============================================================
GENISLIK = 900
YUKSEKLIK = 650
BASLIK = "Temel Sekil Cizimleri - pygame.draw"
FPS = 60

# Renkler
ARKAPLAN = (20, 20, 35)
BEYAZ = (255, 255, 255)
KIRMIZI = (230, 60, 60)
YESIL = (60, 200, 80)
MAVI = (60, 120, 230)
SARI = (240, 220, 50)
TURUNCU = (240, 150, 30)
MOR = (160, 60, 210)
CAMGOBEGI = (60, 210, 210)
ACIK_GRI = (180, 180, 180)


def baslik_yaz(ekran, font, metin, x, y):
    """Bir bolum basligi yazar.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
        metin: Yazdirilacak baslik metni
        x: Yatay konum
        y: Dikey konum
    """
    yazi = font.render(metin, True, BEYAZ)
    ekran.blit(yazi, (x, y))


def dikdortgenler_ciz(ekran, font):
    """Dikdortgen cizim orneklerini gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik_yaz(ekran, font, "rect() - Dikdortgen", 30, 10)

    # Dolu dikdortgen
    pygame.draw.rect(ekran, KIRMIZI, (30, 40, 100, 60))

    # Cerceveli dikdortgen (width=3)
    pygame.draw.rect(ekran, KIRMIZI, (150, 40, 100, 60), 3)

    # Yuvarlatilmis koseli dikdortgen
    pygame.draw.rect(ekran, KIRMIZI, (270, 40, 100, 60), 0, 15)

    # Etiketler
    kucuk_font = pygame.font.Font(None, 18)
    etiketler = [
        ("Dolu", 55, 108),
        ("Cerceve (w=3)", 152, 108),
        ("Yuvarlak (r=15)", 272, 108),
    ]
    for metin, x, y in etiketler:
        yazi = kucuk_font.render(metin, True, ACIK_GRI)
        ekran.blit(yazi, (x, y))


def daireler_ciz(ekran, font):
    """Daire cizim orneklerini gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik_yaz(ekran, font, "circle() - Daire", 30, 135)

    # Dolu daire
    pygame.draw.circle(ekran, YESIL, (80, 195), 35)

    # Cerceveli daire (width=3)
    pygame.draw.circle(ekran, YESIL, (195, 195), 35, 3)

    # Farkli boyutlarda daireler (ic ice)
    for yaricap in range(40, 5, -8):
        kalinlik = 0 if yaricap == 40 else 1
        renk_deger = int(255 * (yaricap / 40))
        renk = (0, renk_deger, 0)
        pygame.draw.circle(ekran, renk, (320, 195), yaricap, kalinlik)

    # Etiketler
    kucuk_font = pygame.font.Font(None, 18)
    etiketler = [
        ("Dolu (r=35)", 42, 238),
        ("Cerceve (w=3)", 152, 238),
        ("Ic ice", 296, 238),
    ]
    for metin, x, y in etiketler:
        yazi = kucuk_font.render(metin, True, ACIK_GRI)
        ekran.blit(yazi, (x, y))


def cizgiler_ciz(ekran, font):
    """Cizgi cizim orneklerini gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik_yaz(ekran, font, "line() / aaline() - Cizgi", 30, 265)

    # Temel cizgi
    pygame.draw.line(ekran, MAVI, (30, 300), (160, 350), 3)

    # Anti-aliased (yumusatilmis) cizgi
    pygame.draw.aaline(ekran, MAVI, (30, 360), (160, 310))

    # Coklu cizgi (lines) - zigzag deseni
    noktalar = [
        (190, 340), (220, 300), (250, 340),
        (280, 300), (310, 340), (340, 300), (370, 340)
    ]
    pygame.draw.lines(ekran, MAVI, False, noktalar, 2)

    # Etiketler
    kucuk_font = pygame.font.Font(None, 18)
    etiketler = [
        ("line (w=3)", 60, 358),
        ("aaline (yumusak)", 40, 370),
        ("lines (zigzag)", 230, 348),
    ]
    for metin, x, y in etiketler:
        yazi = kucuk_font.render(metin, True, ACIK_GRI)
        ekran.blit(yazi, (x, y))


def elipsler_ciz(ekran, font):
    """Elips cizim orneklerini gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik_yaz(ekran, font, "ellipse() - Elips", 480, 10)

    # Dolu elips (yatay)
    pygame.draw.ellipse(ekran, SARI, (480, 40, 120, 60))

    # Cerceveli elips (dikey)
    pygame.draw.ellipse(ekran, SARI, (620, 40, 60, 80), 3)

    # Farkli boyutlarda elipsler
    pygame.draw.ellipse(ekran, TURUNCU, (710, 45, 150, 40))
    pygame.draw.ellipse(ekran, TURUNCU, (710, 45, 150, 40), 2)

    # Etiketler
    kucuk_font = pygame.font.Font(None, 18)
    etiketler = [
        ("Dolu (yatay)", 497, 108),
        ("Cerceve (dikey)", 607, 128),
        ("Genis elips", 745, 93),
    ]
    for metin, x, y in etiketler:
        yazi = kucuk_font.render(metin, True, ACIK_GRI)
        ekran.blit(yazi, (x, y))


def cokgenler_ciz(ekran, font):
    """Cokgen cizim orneklerini gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik_yaz(ekran, font, "polygon() - Cokgen", 480, 150)

    # Ucgen (dolu)
    ucgen = [(530, 230), (480, 270), (580, 270)]
    pygame.draw.polygon(ekran, MOR, ucgen)

    # Besgen (cerceveli)
    merkez_x, merkez_y = 660, 240
    yaricap = 40
    besgen = []
    for i in range(5):
        aci = math.radians(90 + i * 72)  # 90 dereceden basla (tepe noktasi)
        x = merkez_x + yaricap * math.cos(aci)
        y = merkez_y - yaricap * math.sin(aci)
        besgen.append((x, y))
    pygame.draw.polygon(ekran, MOR, besgen, 3)

    # Yildiz sekli
    merkez_x, merkez_y = 790, 240
    dis_yaricap = 42
    ic_yaricap = 18
    yildiz = []
    for i in range(10):
        aci = math.radians(90 + i * 36)
        r = dis_yaricap if i % 2 == 0 else ic_yaricap
        x = merkez_x + r * math.cos(aci)
        y = merkez_y - r * math.sin(aci)
        yildiz.append((x, y))
    pygame.draw.polygon(ekran, SARI, yildiz)

    # Etiketler
    kucuk_font = pygame.font.Font(None, 18)
    etiketler = [
        ("Ucgen (dolu)", 492, 278),
        ("Besgen (w=3)", 622, 288),
        ("Yildiz", 770, 288),
    ]
    for metin, x, y in etiketler:
        yazi = kucuk_font.render(metin, True, ACIK_GRI)
        ekran.blit(yazi, (x, y))


def karisik_ornekler_ciz(ekran, font):
    """Karisik cizim ornekleri: kalinlik, renk cesitliligi.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik_yaz(ekran, font, "Kalinlik ve Renk Ornekleri", 480, 320)

    # Farkli kalinliklarda cizgiler
    kalinliklar = [1, 2, 4, 6, 8, 10]
    for i, kalinlik in enumerate(kalinliklar):
        y = 355 + i * 20
        pygame.draw.line(ekran, CAMGOBEGI, (480, y), (620, y), kalinlik)
        kucuk_font = pygame.font.Font(None, 18)
        yazi = kucuk_font.render(f"w={kalinlik}", True, ACIK_GRI)
        ekran.blit(yazi, (630, y - 6))

    # Gkkusagi daireler
    gokkusagi = [
        (230, 50, 50),   # Kirmizi
        (255, 140, 0),   # Turuncu
        (255, 230, 0),   # Sari
        (50, 205, 50),   # Yesil
        (30, 144, 255),  # Mavi
        (75, 0, 130),    # Indigo
        (148, 0, 211),   # Mor
    ]
    for i, renk in enumerate(gokkusagi):
        yaricap = 70 - i * 8
        pygame.draw.circle(ekran, renk, (790, 420), yaricap, 4)


def bilgi_paneli_ciz(ekran, font):
    """Ekranin alt kisminda bilgi paneli gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    # Alt bilgi paneli
    pygame.draw.rect(ekran, (30, 30, 50), (0, 560, GENISLIK, 90))
    pygame.draw.line(ekran, ACIK_GRI, (0, 560), (GENISLIK, 560), 1)

    kucuk_font = pygame.font.Font(None, 20)
    bilgiler = [
        "pygame.draw ozeti: rect(yuzey, renk, rect, [width]) | "
        "circle(yuzey, renk, merkez, yaricap, [width])",
        "line(yuzey, renk, baslangic, bitis, [width]) | "
        "ellipse(yuzey, renk, rect, [width]) | "
        "polygon(yuzey, renk, noktalar, [width])",
        "width=0 -> dolu sekil | width>0 -> cerceve kalinligi | "
        "aaline/aalines -> anti-aliased (yumusak kenarli) cizgi",
    ]

    for i, bilgi in enumerate(bilgiler):
        yazi = kucuk_font.render(bilgi, True, ACIK_GRI)
        ekran.blit(yazi, (15, 570 + i * 22))


def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)

    # Font olustur
    font = pygame.font.Font(None, 26)

    # Saat nesnesi
    saat = pygame.time.Clock()

    # Konsola cizim fonksiyonu listesi
    print("pygame.draw Modulu - Temel Fonksiyonlar:")
    print("-" * 45)
    print("  rect()    - Dikdortgen")
    print("  circle()  - Daire")
    print("  line()    - Cizgi")
    print("  aaline()  - Yumusatilmis cizgi")
    print("  lines()   - Coklu cizgi")
    print("  ellipse() - Elips")
    print("  polygon() - Cokgen")
    print("-" * 45)
    print("width=0: dolu sekil, width>0: cerceve")
    print()

    # Ana oyun dongusu
    calistir = True

    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Ekrani temizle
        ekran.fill(ARKAPLAN)

        # Tum cizim bolumlerini goster
        dikdortgenler_ciz(ekran, font)
        daireler_ciz(ekran, font)
        cizgiler_ciz(ekran, font)
        elipsler_ciz(ekran, font)
        cokgenler_ciz(ekran, font)
        karisik_ornekler_ciz(ekran, font)
        bilgi_paneli_ciz(ekran, font)

        # Ekrani guncelle
        pygame.display.flip()
        saat.tick(FPS)

    # PyGame'i kapat
    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
900x650 piksel boyutunda koyu lacivert arkaplanli bir pencere acilir.

Sol ustte: Dikdortgen ornekleri (dolu, cerceveli, yuvarlak koseli)
Sol ortada: Daire ornekleri (dolu, cerceveli, ic ice)
Sol altta: Cizgi ornekleri (temel, yumusatilmis, zigzag)

Sag ustte: Elips ornekleri (yatay, dikey, genis)
Sag ortada: Cokgen ornekleri (ucgen, besgen, yildiz)
Sag altta: Kalinlik ornekleri ve gokkusagi daireler

En altta: pygame.draw fonksiyon ozeti

ESC tusuna basinca program kapanir.
"""
