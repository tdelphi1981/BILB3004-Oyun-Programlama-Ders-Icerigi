"""
Ses Yukle ve Cal - Ses dosyasi yukleme ve calma ornegi

Bu program ses dosyalarinin nasil yuklendigini ve calindigini
gosterir. Gercek ses dosyasi olmadan da calisabilmesi icin
programatik ses olusturma ornegi de icerir.

Ogrenilecek kavramlar:
- pygame.mixer.Sound ile ses yukleme
- Hata yonetimi ile guvenli yukleme
- Programatik ses olusturma (buffer ile)

Bolum: 07 - Ses ve Muzik
Unite: 1 - Ses Sistemi Temelleri

Calistirma: python 02_ses_yukle_cal.py
Gereksinimler: pygame, numpy (opsiyonel)
"""

import pygame
import array
import math


def programatik_ses_olustur(frekans=440, sure=0.5, ornek_hizi=44100):
    """Belirli frekansta bir sinusoidal ses dalgasi olusturur.

    Args:
        frekans: Ses frekansi (Hz). 440 = La notasi.
        sure: Ses suresi (saniye).
        ornek_hizi: Ornekleme hizi (Hz).

    Returns:
        pygame.mixer.Sound nesnesi.
    """
    # Orneklerin sayisi
    ornek_sayisi = int(ornek_hizi * sure)

    # 16-bit isaretli ses verisi olustur
    tampon = array.array("h")  # 'h' = signed short (16-bit)
    genlik = 16000  # Maksimum genlik (32767'nin yarisi)

    for i in range(ornek_sayisi):
        # Sinusoidal dalga: sin(2 * pi * frekans * zaman)
        zaman = i / ornek_hizi
        deger = int(genlik * math.sin(2.0 * math.pi * frekans * zaman))
        # Stereo: ayni degeri iki kez ekle (sol ve sag kanal)
        tampon.append(deger)
        tampon.append(deger)

    # Buffer'dan Sound nesnesi olustur
    ses = pygame.mixer.Sound(buffer=tampon)
    return ses


def guvenli_ses_yukle(dosya_yolu):
    """Ses dosyasini guvenli sekilde yukler.

    Args:
        dosya_yolu: Ses dosyasinin yolu.

    Returns:
        Sound nesnesi veya None.
    """
    try:
        ses = pygame.mixer.Sound(dosya_yolu)
        sure = ses.get_length()
        print(f"[OK] '{dosya_yolu}' yuklendi ({sure:.2f} sn)")
        return ses
    except FileNotFoundError:
        print(f"[!] '{dosya_yolu}' bulunamadi!")
        return None
    except pygame.error as hata:
        print(f"[!] Ses yukleme hatasi: {hata}")
        return None


def main():
    """Ana fonksiyon."""
    pygame.mixer.init()
    print("[BILGI] Mixer baslatildi.\n")

    # --- Dosyadan yukleme denemesi ---
    print("--- Dosyadan Ses Yukleme ---")
    ses1 = guvenli_ses_yukle("assets/sounds/ates.wav")
    ses2 = guvenli_ses_yukle("olmayan_dosya.wav")
    print()

    # --- Programatik ses olusturma ---
    print("--- Programatik Ses Olusturma ---")

    # La notasi (440 Hz)
    la_notasi = programatik_ses_olustur(frekans=440, sure=0.3)
    print(f"[OK] La notasi (440 Hz) olusturuldu, "
          f"sure: {la_notasi.get_length():.2f} sn")

    # Do notasi (262 Hz)
    do_notasi = programatik_ses_olustur(frekans=262, sure=0.3)
    print(f"[OK] Do notasi (262 Hz) olusturuldu, "
          f"sure: {do_notasi.get_length():.2f} sn")

    # Mi notasi (330 Hz)
    mi_notasi = programatik_ses_olustur(frekans=330, sure=0.3)
    print(f"[OK] Mi notasi (330 Hz) olusturuldu, "
          f"sure: {mi_notasi.get_length():.2f} sn")
    print()

    # --- Sesleri cal ---
    print("--- Sesleri Calma ---")
    print("La notasi caliniyor...")
    la_notasi.play()
    pygame.time.wait(500)

    print("Do notasi caliniyor...")
    do_notasi.play()
    pygame.time.wait(500)

    print("Mi notasi caliniyor...")
    mi_notasi.play()
    pygame.time.wait(500)

    print()
    print("[OK] Tum sesler calindi.")

    pygame.mixer.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
[BILGI] Mixer baslatildi.

--- Dosyadan Ses Yukleme ---
[!] 'assets/sounds/ates.wav' bulunamadi!
[!] 'olmayan_dosya.wav' bulunamadi!

--- Programatik Ses Olusturma ---
[OK] La notasi (440 Hz) olusturuldu, sure: 0.30 sn
[OK] Do notasi (262 Hz) olusturuldu, sure: 0.30 sn
[OK] Mi notasi (330 Hz) olusturuldu, sure: 0.30 sn

--- Sesleri Calma ---
La notasi caliniyor...
Do notasi caliniyor...
Mi notasi caliniyor...

[OK] Tum sesler calindi.

NOT: Programatik olarak olusturulan sesler hoparlorden duyulur.
"""
