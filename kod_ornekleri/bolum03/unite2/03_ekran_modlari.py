"""
Ekran Modlari - Pencereli, tam ekran ve gecis

Bu program farkli ekran modlarini gosterir ve
F11 tusu ile tam ekran gecisi yapar.

Ogrenilecek kavramlar:
- pygame.FULLSCREEN bayragi
- pygame.NOFRAME bayragi
- pygame.RESIZABLE bayragi
- pygame.display.toggle_fullscreen()
- pygame.display.Info() ile monitor bilgisi

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 2 - Oyun Penceresi Olusturma

Calistirma: python 03_ekran_modlari.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
BASLIK = "Ekran Modlari Ornegi"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (30, 30, 60)

def main():
    """Ana oyun fonksiyonu."""
    pygame.init()

    # Monitor bilgisini al
    bilgi = pygame.display.Info()
    print(f"Monitor cozunurlugu: {bilgi.current_w}x{bilgi.current_h}")

    # Pencereli modda baslat
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)

    # Durum degiskenleri
    tam_ekran = False
    saat = pygame.time.Clock()
    calistir = True

    # Yazi fontu
    font = pygame.font.Font(None, 36)

    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                # ESC ile cikis
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                # F11 ile tam ekran gecisi
                elif olay.key == pygame.K_F11:
                    tam_ekran = not tam_ekran
                    if tam_ekran:
                        ekran = pygame.display.set_mode(
                            (bilgi.current_w, bilgi.current_h),
                            pygame.FULLSCREEN
                        )
                    else:
                        ekran = pygame.display.set_mode(
                            (GENISLIK, YUKSEKLIK)
                        )

        # Ekrani temizle
        ekran.fill(KOYU_MAVI)

        # Bilgi metinlerini ekrana yaz
        mod_metni = "Tam Ekran" if tam_ekran else "Pencereli"
        boyut = ekran.get_size()

        satirlar = [
            f"Ekran Modu: {mod_metni}",
            f"Pencere Boyutu: {boyut[0]}x{boyut[1]}",
            f"F11: Tam ekran gecisi",
            f"ESC: Cikis",
        ]

        for i, satir in enumerate(satirlar):
            yazi = font.render(satir, True, BEYAZ)
            ekran.blit(yazi, (50, 50 + i * 40))

        pygame.display.flip()
        saat.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x600 boyutunda koyu mavi pencere acilir.
Ekranda mevcut mod ve pencere boyutu bilgisi gosterilir.
F11 tusuna basinca tam ekran / pencereli mod arasinda gecis yapar.
ESC tusuna basinca program kapanir.
"""
