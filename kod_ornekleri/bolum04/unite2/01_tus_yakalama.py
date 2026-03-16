"""
Tus Yakalama - KEYDOWN/KEYUP olay islemesi

Bu program PyGame'in klavye olay sistemini gosterir.
Pencere acilir, basilan ve birakilan tuslar konsola
yazdirilir. Tus adi, unicode degeri ve modifier bilgisi
gosterilir.

Ogrenilecek kavramlar:
- pygame.KEYDOWN ve pygame.KEYUP olaylari
- olay.key, olay.mod, olay.unicode ozellikleri
- pygame.key.name() ile tus adini alma
- Modifier tuslari (KMOD_SHIFT, KMOD_CTRL, KMOD_ALT)

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 2 - Klavye Girdileri

Calistirma: python 01_tus_yakalama.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 640
YUKSEKLIK = 480
BASLIK = "Tus Yakalama Ornegi"
ARKA_PLAN = (20, 20, 50)  # Koyu lacivert


def modifier_metni(mod):
    """Modifier bit maskesini okunabilir metne donusturur."""
    parcalar = []
    if mod & pygame.KMOD_SHIFT:
        parcalar.append("Shift")
    if mod & pygame.KMOD_CTRL:
        parcalar.append("Ctrl")
    if mod & pygame.KMOD_ALT:
        parcalar.append("Alt")
    if not parcalar:
        return "Yok"
    return "+".join(parcalar)


def main():
    """Ana program fonksiyonu."""
    # PyGame'i baslat
    pygame.init()

    # Pencere olustur
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    print("=" * 55)
    print("  Tus Yakalama Ornegi")
    print("  Tuslara basarak olay bilgilerini inceleyin.")
    print("  ESC ile cikis yapabilirsiniz.")
    print("=" * 55)

    # Ana oyun dongusu
    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                tus_adi = pygame.key.name(olay.key)
                mod_str = modifier_metni(olay.mod)
                unicode_str = olay.unicode if olay.unicode else "(yok)"

                print(f"[KEYDOWN] Tus: {tus_adi:12s}  "
                      f"Karakter: {unicode_str:5s}  "
                      f"Modifier: {mod_str}")

                # Pencere basligini guncelle
                pygame.display.set_caption(
                    f"Son tus: {tus_adi} | {BASLIK}"
                )

                # ESC ile cikis
                if olay.key == pygame.K_ESCAPE:
                    print("\n[CIKIS] ESC tusuna basildi, kapaniyor...")
                    calistir = False

            elif olay.type == pygame.KEYUP:
                tus_adi = pygame.key.name(olay.key)
                print(f"[KEYUP]   Tus: {tus_adi:12s}  (birakildi)")

        # Ekrani temizle ve guncelle
        ekran.fill(ARKA_PLAN)
        pygame.display.flip()
        saat.tick(60)

    # PyGame'i kapat
    pygame.quit()
    print("\nProgram sonlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
=======================================================
  Tus Yakalama Ornegi
  Tuslara basarak olay bilgilerini inceleyin.
  ESC ile cikis yapabilirsiniz.
=======================================================
[KEYDOWN] Tus: space         Karakter:        Modifier: Yok
[KEYUP]   Tus: space         (birakildi)
[KEYDOWN] Tus: a             Karakter: a      Modifier: Yok
[KEYUP]   Tus: a             (birakildi)
[KEYDOWN] Tus: a             Karakter: A      Modifier: Shift
[KEYUP]   Tus: a             (birakildi)
[KEYDOWN] Tus: up            Karakter: (yok)  Modifier: Yok
[KEYUP]   Tus: up            (birakildi)
[KEYDOWN] Tus: s             Karakter: s      Modifier: Ctrl
[KEYUP]   Tus: s             (birakildi)

[CIKIS] ESC tusuna basildi, kapaniyor...

Program sonlandi.
"""
