"""
PyGame Kurulum Kontrolu - Kurulumu dogrulama ve test

Bu program PyGame'in dogru kurulup kurulmadigini kontrol eder.
pygame.init() cagirilarak modul durumu yazdilir, versiyon bilgisi
gosterilir ve kisa bir pencere aci-kapa testi yapilir.

Ogrenilecek kavramlar:
- pygame.init() ile modulleri baslatma
- pygame.get_sdl_version() ile SDL versiyonu
- pygame.version.ver ile PyGame versiyonu
- Basit pencere aci-kapa testi

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 1 - PyGame Kurulumu ve Yapilandirma

Calistirma: python 01_pygame_kontrol.py
Gereksinimler: pygame
"""

import sys

def pygame_kurulum_kontrol():
    """PyGame'in kurulu olup olmadigini kontrol eder."""
    print("=" * 50)
    print("  PyGame Kurulum Kontrol Araci")
    print("=" * 50)
    print()

    # Adim 1: pygame import edilebilir mi?
    print("[1] PyGame import kontrolu...")
    try:
        import pygame
        print(f"    [OK] PyGame basariyla import edildi!")
    except ImportError:
        print("    [HATA] PyGame bulunamadi!")
        print("    Kurulum icin: pip install pygame")
        print("    veya: uv add pygame")
        sys.exit(1)

    # Adim 2: Versiyon bilgileri
    print()
    print("[2] Versiyon bilgileri:")
    print(f"    Python versiyonu  : {sys.version.split()[0]}")
    print(f"    PyGame versiyonu  : {pygame.version.ver}")
    print(f"    SDL versiyonu     : {'.'.join(map(str, pygame.get_sdl_version()))}")

    # Adim 3: pygame.init() testi
    print()
    print("[3] pygame.init() testi...")
    basarili, basarisiz = pygame.init()
    print(f"    Baslatilan moduller : {basarili}")
    print(f"    Basarisiz moduller  : {basarisiz}")

    if basarisiz > 0:
        print(f"    [UYARI] {basarisiz} modul baslatilamadi.")
    else:
        print("    [OK] Tum moduller basariyla baslatildi!")

    # Adim 4: Basit pencere aci-kapa testi
    print()
    print("[4] Pencere aci-kapa testi...")
    try:
        ekran = pygame.display.set_mode((320, 240))
        pygame.display.set_caption("PyGame Test Penceresi")
        # Ekrani bir kez boyayip guncelle
        ekran.fill((0, 100, 0))  # Yesil arka plan
        pygame.display.flip()
        print("    [OK] Pencere basariyla olusturuldu!")

        # Kisa bir sure bekle (1 saniye)
        pygame.time.delay(1000)

    except Exception as hata:
        print(f"    [HATA] Pencere olusturulamadi: {hata}")
    finally:
        pygame.quit()
        print("    [OK] PyGame duzgun sekilde kapatildi.")

    # Sonuc
    print()
    print("=" * 50)
    if basarisiz == 0:
        print("  SONUC: PyGame kurulumu basarili!")
        print("  Oyun gelistirmeye hazirsiniz.")
    else:
        print("  SONUC: PyGame kurulumunda sorunlar var.")
        print("  Yeniden kurmayı deneyin: pip install --upgrade pygame")
    print("=" * 50)


if __name__ == "__main__":
    pygame_kurulum_kontrol()

"""
BEKLENEN CIKTI:
---------------
==================================================
  PyGame Kurulum Kontrol Araci
==================================================

[1] PyGame import kontrolu...
    [OK] PyGame basariyla import edildi!

[2] Versiyon bilgileri:
    Python versiyonu  : 3.12.0
    PyGame versiyonu  : 2.6.0
    SDL versiyonu     : 2.28.5

[3] pygame.init() testi...
    Baslatilan moduller : 6
    Basarisiz moduller  : 0
    [OK] Tum moduller basariyla baslatildi!

[4] Pencere aci-kapa testi...
    [OK] Pencere basariyla olusturuldu!
    [OK] PyGame duzgun sekilde kapatildi.

==================================================
  SONUC: PyGame kurulumu basarili!
  Oyun gelistirmeye hazirsiniz.
==================================================
"""
