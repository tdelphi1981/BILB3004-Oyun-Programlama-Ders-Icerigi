"""
Fade Efektleri ve Muzik Kuyrugu

Bu program fade in/out efektlerini ve muzik kuyrugunu
interaktif olarak gosterir.

Ogrenilecek kavramlar:
- music.fadeout(ms)
- music.play(fade_ms=...)
- music.queue()
- music.set_endevent()

Bolum: 07 - Ses ve Muzik
Unite: 3 - Arka Plan Muzigi

Calistirma: python 03_fade_efektleri.py
Gereksinimler: pygame
"""

import pygame
import os
import math
import struct
import wave

# Sabitler
GENISLIK = 700
YUKSEKLIK = 500
BASLIK = "Fade Efektleri ve Muzik Kuyrugu"
FPS = 60

# Ozel olay: muzik bitti
MUZIK_BITTI = pygame.USEREVENT + 1

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
MAVI = (70, 130, 180)
YESIL = (50, 200, 100)
KIRMIZI = (200, 60, 60)
SARI = (255, 200, 50)
MOR = (150, 100, 200)
GRI = (120, 120, 120)


def test_muzik_olustur(dosya_adi, frekans=440, sure=8):
    """Farkli frekanslarda test muzik dosyalari olusturur."""
    if not os.path.exists(dosya_adi):
        ornekleme = 22050
        with wave.open(dosya_adi, "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(ornekleme)
            for i in range(sure * ornekleme):
                # Hafif frekans modülasyonu ile daha ilginc ses
                mod_frekans = frekans + 50 * math.sin(2 * math.pi * 0.3 * i / ornekleme)
                deger = int(10000 * math.sin(2 * math.pi * mod_frekans * i / ornekleme))
                wav.writeframes(struct.pack("<h", deger))
    return dosya_adi


def main():
    """Ana fonksiyon."""
    pygame.init()
    pygame.mixer.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    baslik_font = pygame.font.SysFont("Arial", 26, bold=True)
    tus_font = pygame.font.SysFont("Arial", 15, bold=True)

    # Farkli muzik dosyalari olustur
    muzik_a = test_muzik_olustur("test_muzik_a.wav", frekans=330, sure=10)
    muzik_b = test_muzik_olustur("test_muzik_b.wav", frekans=440, sure=10)
    muzik_c = test_muzik_olustur("test_muzik_c.wav", frekans=520, sure=10)

    # Muzik bitti olayini ayarla
    pygame.mixer.music.set_endevent(MUZIK_BITTI)

    # Ilk muzigi yukle ve cal
    pygame.mixer.music.load(muzik_a)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    mevcut_muzik = "Muzik A (330 Hz)"
    durum_mesaji = "Muzik A caliniyor"
    fade_durumu = ""
    log_mesajlari = []
    beklenen_muzik = None  # Fade sonrasi yuklenecek muzik

    def log_ekle(mesaj):
        """Log mesaji ekler (en fazla 6 satir tutar)."""
        log_mesajlari.append(mesaj)
        if len(log_mesajlari) > 6:
            log_mesajlari.pop(0)

    log_ekle("[OK] Muzik A baslatildi")

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == MUZIK_BITTI:
                log_ekle("[!] Muzik parcasi bitti")
                fade_durumu = ""
                # Fade sonrasi beklenen muzik varsa baslat
                if beklenen_muzik is not None:
                    dosya, isim = beklenen_muzik
                    pygame.mixer.music.load(dosya)
                    pygame.mixer.music.play(loops=-1, fade_ms=2000)
                    mevcut_muzik = isim
                    durum_mesaji = f"{isim} fade-in ile baslatildi"
                    log_ekle(f"[OK] {isim} fade-in ile baslatildi (2s)")
                    beklenen_muzik = None

            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                # F: Fade out (3 saniye)
                elif olay.key == pygame.K_f:
                    pygame.mixer.music.fadeout(3000)
                    fade_durumu = "Fade out (3s)..."
                    durum_mesaji = "Fade out baslatildi"
                    log_ekle("[->] Fade out baslatildi (3s)")

                # G: Yeni muzik fade-in ile baslat
                elif olay.key == pygame.K_g:
                    pygame.mixer.music.load(muzik_b)
                    pygame.mixer.music.play(loops=-1, fade_ms=3000)
                    mevcut_muzik = "Muzik B (440 Hz)"
                    fade_durumu = "Fade in (3s)..."
                    durum_mesaji = "Muzik B fade-in ile basladi"
                    log_ekle("[OK] Muzik B fade-in baslatildi (3s)")

                # Q: Kuyruga muzik ekle
                elif olay.key == pygame.K_q:
                    # Once donguyu kapat ki muzik bitebilsin
                    pygame.mixer.music.play(loops=0)
                    pygame.mixer.music.queue(muzik_c)
                    durum_mesaji = "Muzik C kuyruga eklendi"
                    log_ekle("[+] Muzik C kuyruga eklendi")

                # T: Gecis efekti (fade out + fade in)
                elif olay.key == pygame.K_t:
                    beklenen_muzik = (muzik_a, "Muzik A (330 Hz)")
                    pygame.mixer.music.fadeout(2000)
                    fade_durumu = "Gecis: fade out..."
                    durum_mesaji = "Akici gecis baslatildi"
                    log_ekle("[->] Akici gecis: fade out (2s)")

                # 1, 2, 3: Dogrudan muzik degistir
                elif olay.key == pygame.K_1:
                    pygame.mixer.music.load(muzik_a)
                    pygame.mixer.music.play(loops=-1)
                    mevcut_muzik = "Muzik A (330 Hz)"
                    log_ekle("[OK] Muzik A baslatildi")

                elif olay.key == pygame.K_2:
                    pygame.mixer.music.load(muzik_b)
                    pygame.mixer.music.play(loops=-1)
                    mevcut_muzik = "Muzik B (440 Hz)"
                    log_ekle("[OK] Muzik B baslatildi")

                elif olay.key == pygame.K_3:
                    pygame.mixer.music.load(muzik_c)
                    pygame.mixer.music.play(loops=-1)
                    mevcut_muzik = "Muzik C (520 Hz)"
                    log_ekle("[OK] Muzik C baslatildi")

        # --- CIZIM ---
        ekran.fill(SIYAH)

        # Baslik
        baslik = baslik_font.render("Fade Efektleri ve Muzik Kuyrugu", True, MAVI)
        ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 15))

        y_pos = 60

        # Durum bilgileri
        caliyor = pygame.mixer.music.get_busy()
        durum_renk = YESIL if caliyor else KIRMIZI
        ekran.blit(font.render(f"Durum: {'Caliyor' if caliyor else 'Durdu'}", True, durum_renk), (50, y_pos))
        y_pos += 25
        ekran.blit(font.render(f"Mevcut: {mevcut_muzik}", True, BEYAZ), (50, y_pos))
        y_pos += 25

        ses = pygame.mixer.music.get_volume()
        ekran.blit(font.render(f"Ses Seviyesi: {ses:.2f}", True, BEYAZ), (50, y_pos))
        y_pos += 25

        if fade_durumu:
            ekran.blit(font.render(f"Fade: {fade_durumu}", True, MOR), (50, y_pos))
        y_pos += 35

        # Kontroller
        ekran.blit(baslik_font.render("Kontroller:", True, BEYAZ), (50, y_pos))
        y_pos += 30

        kontroller = [
            ("F", "Fade out (3s)"),
            ("G", "Muzik B fade-in ile baslat"),
            ("Q", "Muzik C kuyruga ekle"),
            ("T", "Akici gecis (fade out -> fade in)"),
            ("1/2/3", "Dogrudan muzik degistir (A/B/C)"),
            ("ESC", "Cikis"),
        ]

        for tus, aciklama in kontroller:
            tus_metin = tus_font.render(tus, True, SIYAH)
            tus_gen = tus_metin.get_width() + 14
            pygame.draw.rect(ekran, BEYAZ, (60, y_pos, tus_gen, 22), border_radius=3)
            ekran.blit(tus_metin, (67, y_pos + 2))
            ekran.blit(font.render(aciklama, True, GRI), (60 + tus_gen + 12, y_pos + 1))
            y_pos += 27

        # Log mesajlari
        y_pos += 15
        ekran.blit(baslik_font.render("Log:", True, SARI), (50, y_pos))
        y_pos += 28
        for mesaj in log_mesajlari:
            renk = YESIL if "[OK]" in mesaj else (SARI if "[->]" in mesaj else GRI)
            ekran.blit(font.render(mesaj, True, renk), (60, y_pos))
            y_pos += 22

        pygame.display.flip()
        saat.tick(FPS)

    # Temizlik
    pygame.mixer.music.stop()
    pygame.quit()
    for dosya in ["test_muzik_a.wav", "test_muzik_b.wav", "test_muzik_c.wav"]:
        if os.path.exists(dosya):
            os.remove(dosya)


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
700x500 piksel boyutunda bir pencere acilir.
Ekranda muzik durumu, kontrol tuslari ve log mesajlari gosterilir.
F ile fade out, G ile fade in, Q ile kuyruga ekleme,
T ile akici gecis (fade out -> fade in) yapilabilir.
1/2/3 tuslariyla farkli muzik parcalarina gecis yapilabilir.
"""
