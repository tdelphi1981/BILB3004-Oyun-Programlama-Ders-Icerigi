"""
Gorsel Yukleme - Temel gorsel yukleme ve fallback stratejisi

Bu program, pygame.image.load() fonksiyonuyla gorsel dosyalarini
yuklemeyi, os.path ile platform bagimsiz dosya yolu olusturmayi
ve hata durumunda fallback (yer tutucu) gorsel kullanmayi gosterir.

Ogrenilecek kavramlar:
- pygame.image.load() ile gorsel yukleme
- os.path.join() ile platform bagimsiz yol
- os.path.dirname(__file__) ile goreceli yol
- try-except ile hata yakalama
- Fallback (placeholder) stratejisi

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 1 - Gorsel Dosyalari

Calistirma: python 01_gorsel_yukleme.py
Gereksinimler: pygame
"""

import os
import pygame

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Gorsel Yukleme Ornegi"

# Renkler
KOYU_MAVI = (10, 10, 40)
BEYAZ = (255, 255, 255)
MAGENTA = (255, 0, 255)

# Bu dosyanin bulundugu dizin
DOSYA_DIZINI = os.path.dirname(os.path.abspath(__file__))
GORSEL_DIZINI = os.path.join(DOSYA_DIZINI, "..", "..", "..",
                              "assets", "images")


def gorsel_yukle(dosya_adi, boyut=None):
    """Gorseli yukle, bulunamazsa placeholder olustur.

    Args:
        dosya_adi: Yuklenecek gorsel dosyasinin adi
        boyut: (genislik, yukseklik) tuple veya None

    Returns:
        pygame.Surface: Yuklenen gorsel veya yer tutucu
    """
    dosya_yolu = os.path.join(GORSEL_DIZINI, dosya_adi)
    try:
        gorsel = pygame.image.load(dosya_yolu).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        print(f"[OK] Gorsel yuklendi: {dosya_adi}")
        return gorsel
    except (FileNotFoundError, pygame.error) as hata:
        print(f"[UYARI] Gorsel yuklenemedi: {dosya_adi}")
        print(f"  Hata: {hata}")
        # Fallback: magenta yer tutucu
        genislik = boyut[0] if boyut else 64
        yukseklik = boyut[1] if boyut else 64
        yer_tutucu = pygame.Surface((genislik, yukseklik),
                                     pygame.SRCALPHA)
        yer_tutucu.fill((MAGENTA[0], MAGENTA[1], MAGENTA[2], 180))
        # Carpraz cizgiler ekle (gorsel bozuk isaretcisi)
        pygame.draw.line(yer_tutucu, BEYAZ,
                         (0, 0), (genislik, yukseklik), 2)
        pygame.draw.line(yer_tutucu, BEYAZ,
                         (genislik, 0), (0, yukseklik), 2)
        return yer_tutucu


def main():
    """Ana fonksiyon."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # --- Gorselleri yukle ---
    # Var olan bir gorsel (basarili yukleme)
    gemi = gorsel_yukle("playerShip1_blue.png", boyut=(64, 64))

    # Var olmayan bir gorsel (fallback testi)
    kayip_gorsel = gorsel_yukle("bu_dosya_yok.png", boyut=(48, 48))

    # Bilgilendirme yazisi icin font
    font = pygame.font.Font(None, 28)

    # --- Ana oyun dongusu ---
    calistir = True
    while calistir:
        # Olaylari isle
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # Ekrani temizle
        ekran.fill(KOYU_MAVI)

        # Basarili yuklenen gorseli ciz
        ekran.blit(gemi, (200, 250))
        basarili_yazi = font.render("Basarili yukleme", True, BEYAZ)
        ekran.blit(basarili_yazi, (160, 330))

        # Fallback gorseli ciz
        ekran.blit(kayip_gorsel, (500, 250))
        fallback_yazi = font.render("Fallback (yer tutucu)", True,
                                     MAGENTA)
        ekran.blit(fallback_yazi, (440, 330))

        # Baslik yazisi
        baslik_yazi = font.render(
            "gorsel_yukle() fonksiyonu demo", True, BEYAZ
        )
        ekran.blit(baslik_yazi, (GENISLIK // 2
                                  - baslik_yazi.get_width() // 2, 50))

        # Ekrani guncelle
        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
[OK] Gorsel yuklendi: playerShip1_blue.png
  (Eger assets/images klasorunde bu dosya varsa)

[UYARI] Gorsel yuklenemedi: bu_dosya_yok.png
  Hata: No file 'bu_dosya_yok.png' found ...

Ekranda iki gorsel gorunur:
- Soldaki: Yuklenen uzay gemisi gorseli (veya magenta yer tutucu)
- Sagdaki: Magenta renkli, capraz cizgili yer tutucu

ESC ile cikis.
"""
