"""
Pencere Basligi ve Ikonu - Ozellestirme ornegi

Bu program oyun penceresinin basligini ve ikonunu
nasil ayarlayacagini gosterir. Ikon dosyasi yoksa
program hata vermeden devam eder.

Ogrenilecek kavramlar:
- pygame.display.set_caption() ile baslik ayarlama
- pygame.display.set_icon() ile ikon ayarlama
- pygame.image.load() ile gorsel yukleme
- try-except ile hata yonetimi

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 2 - Oyun Penceresi Olusturma

Calistirma: python 02_baslik_ikon.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
OYUN_ADI = "Uzay Kacisi"
IKON_DOSYASI = "ikon.png"
ARKAPLAN_RENGI = (20, 20, 40)

def main():
    """Ana oyun fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Ikon ayarla (set_mode'dan once!)
    try:
        ikon = pygame.image.load(IKON_DOSYASI)
        pygame.display.set_icon(ikon)
        print(f"[OK] Ikon yuklendi: {IKON_DOSYASI}")
    except FileNotFoundError:
        print(f"[!] Ikon dosyasi bulunamadi: {IKON_DOSYASI}")
        print("    Varsayilan PyGame ikonu kullanilacak.")

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))

    # Baslik ayarla
    pygame.display.set_caption(OYUN_ADI)

    # Skor sayaci (baslikta gosterilecek)
    skor = 0

    # Ana oyun dongusu
    saat = pygame.time.Clock()
    calistir = True

    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            # Bosluk tusuna basinca skor artar
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_SPACE:
                    skor += 10
                    # Basligi dinamik olarak guncelle
                    pygame.display.set_caption(
                        f"{OYUN_ADI} - Skor: {skor}"
                    )

        ekran.fill(ARKAPLAN_RENGI)
        pygame.display.flip()
        saat.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu bir pencere acilir.
Pencere basliginda "Uzay Kacisi" yazar.
Bosluk tusuna her basildiginda skor 10 artar ve
baslik "Uzay Kacisi - Skor: 10" seklinde guncellenir.
Ikon dosyasi yoksa konsola uyari mesaji yazilir.
"""
