"""
Mixer Baslat - pygame.mixer modulunu baslatma ve yapilandirma

Bu program PyGame ses sisteminin farkli yontemlerle nasil
baslatildigini gosterir.

Ogrenilecek kavramlar:
- pygame.mixer.init() ile ses sistemini baslatma
- pygame.mixer.pre_init() ile onceden yapilandirma
- Mixer ayarlarini sorgulama

Bolum: 07 - Ses ve Muzik
Unite: 1 - Ses Sistemi Temelleri

Calistirma: python 01_mixer_baslat.py
Gereksinimler: pygame
"""

import pygame


def temel_baslatma():
    """Mixer'i varsayilan ayarlarla baslat."""
    # Sadece mixer'i baslat
    pygame.mixer.init()

    # Mevcut ayarlari sorgula
    frekans, boyut, kanal = pygame.mixer.get_init()
    print("[BILGI] Mixer baslatildi!")
    print(f"  Ornekleme hizi : {frekans} Hz")
    print(f"  Bit derinligi  : {boyut}")
    print(f"  Kanal sayisi   : {kanal} ({'stereo' if kanal == 2 else 'mono'})")
    print(f"  Toplam kanal   : {pygame.mixer.get_num_channels()}")

    # Mixer'i kapat
    pygame.mixer.quit()
    print("[OK] Mixer kapatildi.\n")


def ozel_baslatma():
    """Mixer'i ozel ayarlarla baslat."""
    # Baslatmadan ONCE ayarlari belirle
    pygame.mixer.pre_init(
        frequency=44100,  # CD kalitesi
        size=-16,         # 16-bit isaretli
        channels=2,       # Stereo
        buffer=512        # Dusuk gecikme
    )

    # Simdi baslat -- pre_init ayarlari kullanilir
    pygame.mixer.init()

    frekans, boyut, kanal = pygame.mixer.get_init()
    print("[BILGI] Ozel ayarlarla mixer baslatildi!")
    print(f"  Ornekleme hizi : {frekans} Hz")
    print(f"  Bit derinligi  : {boyut}")
    print(f"  Kanal sayisi   : {kanal}")

    # Kanal sayisini degistir
    pygame.mixer.set_num_channels(16)
    print(f"  Yeni kanal sayisi: {pygame.mixer.get_num_channels()}")

    pygame.mixer.quit()
    print("[OK] Mixer kapatildi.\n")


def main():
    """Ana fonksiyon."""
    print("=" * 50)
    print("PyGame Mixer Baslatma Ornegi")
    print("=" * 50)
    print()

    print("--- Yontem 1: Varsayilan Baslatma ---")
    temel_baslatma()

    print("--- Yontem 2: Ozel Ayarlarla Baslatma ---")
    ozel_baslatma()

    print("[OK] Tum testler tamamlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
==================================================
PyGame Mixer Baslatma Ornegi
==================================================

--- Yontem 1: Varsayilan Baslatma ---
[BILGI] Mixer baslatildi!
  Ornekleme hizi : 44100 Hz
  Bit derinligi  : -16
  Kanal sayisi   : 2 (stereo)
  Toplam kanal   : 8
[OK] Mixer kapatildi.

--- Yontem 2: Ozel Ayarlarla Baslatma ---
[BILGI] Ozel ayarlarla mixer baslatildi!
  Ornekleme hizi : 44100 Hz
  Bit derinligi  : -16
  Kanal sayisi   : 2
  Yeni kanal sayisi: 16
[OK] Mixer kapatildi.

[OK] Tum testler tamamlandi.
"""
