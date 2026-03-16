"""
PyGame Modul Testi - Alt modulleri tek tek test etme

Bu program PyGame'in alt modullerini (display, mixer, font vb.)
tek tek baslatiyor ve durumlarini raporluyor. Hangi modullerin
kullanilabilir oldugunu ve init() donus degerinin ne anlama
geldigini gosterir.

Ogrenilecek kavramlar:
- pygame.init() donus degeri (basarili, basarisiz)
- pygame.display.init() ile tekil modul baslatma
- pygame.mixer.init() ile ses modulu kontrolu
- pygame.font.init() ile yazi tipi modulu kontrolu
- get_init() ile modul durumu sorgulama

Bolum: 03 - PyGame'e Giris ve Oyun Penceresi
Unite: 1 - PyGame Kurulumu ve Yapilandirma

Calistirma: python 02_modul_testi.py
Gereksinimler: pygame
"""

import pygame


def modul_durumu_goster(modul_adi, modul):
    """Bir PyGame modulunun baslatilma durumunu gosterir.

    Args:
        modul_adi: Modulun goruntulenecek adi
        modul: PyGame modul nesnesi (ornek: pygame.display)
    """
    try:
        # Modulu baslat
        modul.init()
        # Baslatildi mi kontrol et
        if modul.get_init():
            print(f"    {modul_adi:<20s} : [OK] Baslatildi")
            return True
        else:
            print(f"    {modul_adi:<20s} : [!] Baslatilamadi")
            return False
    except Exception as hata:
        print(f"    {modul_adi:<20s} : [HATA] {hata}")
        return False


def toplu_init_testi():
    """pygame.init() ile toplu baslatma ve sonucu gosterme."""
    print("=" * 55)
    print("  PyGame Modul Test Araci")
    print("=" * 55)

    # --------------------------------------------------
    # Test 1: Toplu baslatma
    # --------------------------------------------------
    print()
    print("[Test 1] Toplu baslatma: pygame.init()")
    print("-" * 55)

    basarili, basarisiz = pygame.init()
    toplam = basarili + basarisiz

    print(f"    Toplam modul sayisi   : {toplam}")
    print(f"    Basarili baslatilan   : {basarili}")
    print(f"    Basarisiz olan        : {basarisiz}")

    if basarisiz == 0:
        print(f"    Sonuc                 : [OK] Tum moduller hazir!")
    else:
        print(f"    Sonuc                 : [UYARI] {basarisiz} modul sorunlu")

    # Toplu baslatmayi geri al, tekil test icin
    pygame.quit()

    # --------------------------------------------------
    # Test 2: Tekil modul baslatma
    # --------------------------------------------------
    print()
    print("[Test 2] Tekil modul baslatma")
    print("-" * 55)

    moduller = [
        ("display (Ekran)", pygame.display),
        ("font (Yazi Tipi)", pygame.font),
        ("mixer (Ses)", pygame.mixer),
        ("joystick (Oyun Kolu)", pygame.joystick),
    ]

    basarili_sayac = 0
    for modul_adi, modul in moduller:
        if modul_durumu_goster(modul_adi, modul):
            basarili_sayac += 1

    print()
    print(f"    Sonuc: {basarili_sayac}/{len(moduller)} modul baslatildi.")

    # --------------------------------------------------
    # Test 3: Ek bilgiler
    # --------------------------------------------------
    print()
    print("[Test 3] Ek modul bilgileri")
    print("-" * 55)

    # display modulu bilgisi
    if pygame.display.get_init():
        # get_driver icin set_mode gerekli
        ekran = pygame.display.set_mode((1, 1))
        surucu = pygame.display.get_driver()
        print(f"    Display surucusu     : {surucu}")
        bilgi = pygame.display.Info()
        print(f"    Monitor cozunurlugu  : {bilgi.current_w}x{bilgi.current_h}")

    # font modulu bilgisi
    if pygame.font.get_init():
        varsayilan = pygame.font.get_default_font()
        print(f"    Varsayilan font      : {varsayilan}")

    # mixer modulu bilgisi
    if pygame.mixer.get_init():
        frekans, boyut, kanal = pygame.mixer.get_init()
        print(f"    Mixer frekans        : {frekans} Hz")
        print(f"    Mixer bit derinligi  : {boyut}")
        print(f"    Mixer kanal sayisi   : {kanal}")

    # --------------------------------------------------
    # Temizlik
    # --------------------------------------------------
    print()
    print("=" * 55)
    print("  Tum testler tamamlandi.")
    print("=" * 55)

    pygame.quit()


if __name__ == "__main__":
    toplu_init_testi()

"""
BEKLENEN CIKTI:
---------------
=======================================================
  PyGame Modul Test Araci
=======================================================

[Test 1] Toplu baslatma: pygame.init()
-------------------------------------------------------
    Toplam modul sayisi   : 6
    Basarili baslatilan   : 6
    Basarisiz olan        : 0
    Sonuc                 : [OK] Tum moduller hazir!

[Test 2] Tekil modul baslatma
-------------------------------------------------------
    display (Ekran)      : [OK] Baslatildi
    font (Yazi Tipi)     : [OK] Baslatildi
    mixer (Ses)          : [OK] Baslatildi
    joystick (Oyun Kolu) : [OK] Baslatildi

    Sonuc: 4/4 modul baslatildi.

[Test 3] Ek modul bilgileri
-------------------------------------------------------
    Display surucusu     : cocoa
    Monitor cozunurlugu  : 1920x1080
    Varsayilan font      : freesansbold.ttf
    Mixer frekans        : 44100 Hz
    Mixer bit derinligi  : -16
    Mixer kanal sayisi   : 2

=======================================================
  Tum testler tamamlandi.
=======================================================
"""
