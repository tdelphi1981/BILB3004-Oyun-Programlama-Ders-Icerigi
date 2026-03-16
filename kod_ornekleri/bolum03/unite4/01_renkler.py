"""
RGB Renkler ve Renk Yonetimi - Renk tanimlama ve kullanim

Bu program RGB renk sistemini, yaygin renk sabitlerini,
renk karistirma orneklerini ve pygame.Color sinifinin
kullanimini gosterir. Ekranda renkli bir palet goruntulenir.

Ogrenilecek kavramlar:
- RGB renk modeli (0-255 aralik)
- Tuple ile renk tanimlama
- pygame.Color sinifi ve metodlari
- Renk karistirma (lerp) ile gecis
- Ekranda renk paleti gosterimi

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 4 - Temel Cizim Islemleri

Calistirma: python 01_renkler.py
Gereksinimler: pygame
"""

import pygame

# ============================================================
# Sabitler
# ============================================================
GENISLIK = 800
YUKSEKLIK = 600
BASLIK = "RGB Renk Paleti ve Renk Yonetimi"
FPS = 60

# ============================================================
# Yaygin Renk Sabitleri (RGB tuple)
# ============================================================
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)
MAVI = (0, 0, 255)
SARI = (255, 255, 0)
CAMGOBEGI = (0, 255, 255)
MAGENTA = (255, 0, 255)
TURUNCU = (255, 165, 0)
MOR = (128, 0, 128)
GRI = (128, 128, 128)
KOYU_GRI = (64, 64, 64)
ARKAPLAN = (25, 25, 40)

# Oyun gelistirmede sik kullanilan renkler
ALTIN = (255, 215, 0)
GUMUS = (192, 192, 192)
BRONZ = (205, 127, 50)
CAN_KIRMIZI = (220, 20, 60)     # Can barindaki kirmizi
MANA_MAVI = (65, 105, 225)      # Mana barindaki mavi
XP_YESIL = (50, 205, 50)        # Deneyim barindaki yesil
GOKYUZU = (135, 206, 235)       # Gokyuzu rengi


def renk_karistir(renk1, renk2, oran):
    """Iki renk arasinda gecis yapar (lineer interpolasyon).

    Args:
        renk1: Baslangic rengi (R, G, B) tuple
        renk2: Bitis rengi (R, G, B) tuple
        oran: Karistirma orani (0.0 = renk1, 1.0 = renk2)

    Returns:
        Karistirilmis renk (R, G, B) tuple
    """
    r = int(renk1[0] + (renk2[0] - renk1[0]) * oran)
    g = int(renk1[1] + (renk2[1] - renk1[1]) * oran)
    b = int(renk1[2] + (renk2[2] - renk1[2]) * oran)
    return (r, g, b)


def renk_paleti_ciz(ekran, font):
    """Temel renk paletini ekrana cizer.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    # Baslik
    baslik = font.render("Temel RGB Renkler", True, BEYAZ)
    ekran.blit(baslik, (30, 20))

    # Temel renkler listesi
    renkler = [
        ("Siyah (0,0,0)", SIYAH),
        ("Beyaz (255,255,255)", BEYAZ),
        ("Kirmizi (255,0,0)", KIRMIZI),
        ("Yesil (0,255,0)", YESIL),
        ("Mavi (0,0,255)", MAVI),
        ("Sari (255,255,0)", SARI),
        ("Camgobegi (0,255,255)", CAMGOBEGI),
        ("Magenta (255,0,255)", MAGENTA),
        ("Turuncu (255,165,0)", TURUNCU),
        ("Mor (128,0,128)", MOR),
    ]

    kare_boyut = 30
    baslangic_y = 55

    for i, (ad, renk) in enumerate(renkler):
        y = baslangic_y + i * (kare_boyut + 8)
        # Renkli kare ciz
        pygame.draw.rect(ekran, renk, (30, y, kare_boyut, kare_boyut))
        # Siyah cerceve
        pygame.draw.rect(ekran, BEYAZ, (30, y, kare_boyut, kare_boyut), 1)
        # Renk adi
        yazi = font.render(ad, True, BEYAZ)
        ekran.blit(yazi, (70, y + 5))


def oyun_renkleri_ciz(ekran, font):
    """Oyun gelistirmede sik kullanilan renkleri gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik = font.render("Oyun Renkleri", True, BEYAZ)
    ekran.blit(baslik, (400, 20))

    oyun_renkleri = [
        ("Altin", ALTIN),
        ("Gumus", GUMUS),
        ("Bronz", BRONZ),
        ("Can (HP)", CAN_KIRMIZI),
        ("Mana (MP)", MANA_MAVI),
        ("XP", XP_YESIL),
        ("Gokyuzu", GOKYUZU),
    ]

    kare_boyut = 30
    baslangic_y = 55

    for i, (ad, renk) in enumerate(oyun_renkleri):
        y = baslangic_y + i * (kare_boyut + 8)
        pygame.draw.rect(ekran, renk, (400, y, kare_boyut, kare_boyut))
        pygame.draw.rect(ekran, BEYAZ, (400, y, kare_boyut, kare_boyut), 1)
        yazi = font.render(ad, True, BEYAZ)
        ekran.blit(yazi, (440, y + 5))


def renk_gecisi_ciz(ekran, font):
    """Iki renk arasinda yumusak gecis seridini cizer.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik = font.render("Renk Gecisleri (Lerp)", True, BEYAZ)
    ekran.blit(baslik, (30, 440))

    gecisler = [
        ("Kirmizi -> Mavi", KIRMIZI, MAVI),
        ("Siyah -> Beyaz", SIYAH, BEYAZ),
        ("Yesil -> Sari", YESIL, SARI),
    ]

    serit_genislik = 350
    serit_yukseklik = 25
    baslangic_y = 470

    for j, (ad, renk1, renk2) in enumerate(gecisler):
        y = baslangic_y + j * (serit_yukseklik + 18)
        # Gecis adini yaz
        yazi = font.render(ad, True, BEYAZ)
        ekran.blit(yazi, (30, y))
        y += 16
        # Renk gecis seridini ciz
        for i in range(serit_genislik):
            oran = i / serit_genislik
            renk = renk_karistir(renk1, renk2, oran)
            pygame.draw.line(ekran, renk, (30 + i, y), (30 + i, y + serit_yukseklik))


def color_sinifi_ciz(ekran, font):
    """pygame.Color sinifinin ozelliklerini gosterir.

    Args:
        ekran: PyGame ekran nesnesi
        font: PyGame font nesnesi
    """
    baslik = font.render("pygame.Color Sinifi", True, BEYAZ)
    ekran.blit(baslik, (400, 310))

    # pygame.Color nesnesi olustur
    renk = pygame.Color(100, 150, 200)

    bilgiler = [
        f"Color(100, 150, 200)",
        f"  .r = {renk.r}, .g = {renk.g}, .b = {renk.b}",
        f"  .a = {renk.a} (alfa/seffaflik)",
        f"  .cmy = ({renk.cmy[0]:.2f}, {renk.cmy[1]:.2f}, {renk.cmy[2]:.2f})",
    ]

    # Isimle renk olusturma
    kirmizi = pygame.Color("red")
    bilgiler.append(f"Color('red') = ({kirmizi.r}, {kirmizi.g}, {kirmizi.b})")

    # lerp ornegi
    renk_a = pygame.Color(255, 0, 0)
    renk_b = pygame.Color(0, 0, 255)
    orta = renk_a.lerp(renk_b, 0.5)
    bilgiler.append(f"lerp(kirmizi, mavi, 0.5) = ({orta.r}, {orta.g}, {orta.b})")

    baslangic_y = 340
    for i, bilgi in enumerate(bilgiler):
        yazi = font.render(bilgi, True, BEYAZ)
        ekran.blit(yazi, (400, baslangic_y + i * 22))

    # Ornek renk karesini goster
    pygame.draw.rect(ekran, renk, (400, baslangic_y + len(bilgiler) * 22 + 5, 40, 40))
    pygame.draw.rect(ekran, BEYAZ, (400, baslangic_y + len(bilgiler) * 22 + 5, 40, 40), 1)


def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)

    # Font olustur
    font = pygame.font.Font(None, 22)

    # Saat nesnesi
    saat = pygame.time.Clock()

    # Konsola renk bilgisi yazdir
    print("RGB Renk Sistemi:")
    print(f"  Her kanal 0-255 arasi deger alir")
    print(f"  Siyah  = (0, 0, 0)       -> Tum kanallar kapali")
    print(f"  Beyaz  = (255, 255, 255)  -> Tum kanallar acik")
    print(f"  Kirmizi= (255, 0, 0)     -> Sadece R kanali")
    print()

    # pygame.Color sinifi ornekleri
    renk1 = pygame.Color(255, 100, 50)
    print(f"pygame.Color(255, 100, 50):")
    print(f"  R={renk1.r}, G={renk1.g}, B={renk1.b}, A={renk1.a}")
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

        # Renk paletlerini ciz
        renk_paleti_ciz(ekran, font)
        oyun_renkleri_ciz(ekran, font)
        renk_gecisi_ciz(ekran, font)
        color_sinifi_ciz(ekran, font)

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
800x600 piksel boyutunda koyu mavi-mor arkaplanli bir pencere acilir.

Sol tarafta:
  - 10 temel RGB renk karesi ve isimleri (Siyah, Beyaz, Kirmizi...)
  - 3 renk gecis seridi (Kirmizi->Mavi, Siyah->Beyaz, Yesil->Sari)

Sag tarafta:
  - 7 oyun temalı renk (Altin, Gumus, Can, Mana, XP...)
  - pygame.Color sinifi bilgileri (r, g, b, a, cmy, lerp)

Konsola RGB sistemi hakkinda bilgi yazdilir.
ESC tusuna basinca program kapanir.
"""
