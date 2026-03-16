"""
Muzik Kontrolleri - Dongu, Duraklatma, Durdurma

Bu program muzik kontrollerini interaktif olarak gosterir.
Klavye tuslariyla muzigi duraklat, devam ettir, durdur ve
ses seviyesini ayarla.

Ogrenilecek kavramlar:
- music.pause() / music.unpause()
- music.stop() / music.rewind()
- music.set_volume() / music.get_volume()
- music.get_busy() ile durum kontrolu

Bolum: 07 - Ses ve Muzik
Unite: 3 - Arka Plan Muzigi

Calistirma: python 02_muzik_kontrol.py
Gereksinimler: pygame
"""

import pygame
import os
import math
import struct
import wave

# Sabitler
GENISLIK = 700
YUKSEKLIK = 480
BASLIK = "Muzik Kontrolleri"
FPS = 60

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
MAVI = (70, 130, 180)
YESIL = (50, 200, 100)
KIRMIZI = (200, 60, 60)
SARI = (255, 200, 50)
GRI = (120, 120, 120)


def test_muzik_olustur():
    """Test icin basit bir muzik dosyasi olusturur."""
    dosya_yolu = "test_kontrol_muzik.wav"
    if not os.path.exists(dosya_yolu):
        sure = 10
        ornekleme = 22050
        with wave.open(dosya_yolu, "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(ornekleme)
            for i in range(sure * ornekleme):
                # Basit bir melodi (frekans degisimi)
                frekans = 330 + 110 * math.sin(2 * math.pi * 0.5 * i / ornekleme)
                deger = int(12000 * math.sin(2 * math.pi * frekans * i / ornekleme))
                wav.writeframes(struct.pack("<h", deger))
    return dosya_yolu


def ses_cubugu_ciz(ekran, x, y, genislik, yukseklik, deger, renk):
    """Ses seviyesi cubugu cizer."""
    # Arka plan (bos cubuk)
    pygame.draw.rect(ekran, GRI, (x, y, genislik, yukseklik), 2)
    # Dolu kisim
    dolu_gen = int(genislik * deger)
    if dolu_gen > 0:
        pygame.draw.rect(ekran, renk, (x, y, dolu_gen, yukseklik))


def main():
    """Ana fonksiyon."""
    pygame.init()
    pygame.mixer.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    baslik_font = pygame.font.SysFont("Arial", 26, bold=True)
    tus_font = pygame.font.SysFont("Arial", 16, bold=True)

    # Muzik yukle ve cal
    muzik_dosyasi = test_muzik_olustur()
    pygame.mixer.music.load(muzik_dosyasi)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    duraklatildi = False
    ses_seviyesi = 0.5
    durum_mesaji = "Muzik caliniyor"

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                # BOSLUK: Duraklat / Devam
                elif olay.key == pygame.K_SPACE:
                    if duraklatildi:
                        pygame.mixer.music.unpause()
                        duraklatildi = False
                        durum_mesaji = "Devam ediliyor"
                    else:
                        pygame.mixer.music.pause()
                        duraklatildi = True
                        durum_mesaji = "Duraklatildi"

                # S: Durdur
                elif olay.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    duraklatildi = False
                    durum_mesaji = "Durduruldu"

                # R: Yeniden baslat
                elif olay.key == pygame.K_r:
                    pygame.mixer.music.play(loops=-1)
                    duraklatildi = False
                    durum_mesaji = "Bastan baslatildi"

                # YUKARI: Sesi artir
                elif olay.key == pygame.K_UP:
                    ses_seviyesi = min(1.0, ses_seviyesi + 0.1)
                    pygame.mixer.music.set_volume(ses_seviyesi)
                    durum_mesaji = f"Ses: {ses_seviyesi:.1f}"

                # ASAGI: Sesi azalt
                elif olay.key == pygame.K_DOWN:
                    ses_seviyesi = max(0.0, ses_seviyesi - 0.1)
                    pygame.mixer.music.set_volume(ses_seviyesi)
                    durum_mesaji = f"Ses: {ses_seviyesi:.1f}"

                # M: Sessize al / Sesi ac
                elif olay.key == pygame.K_m:
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0.0)
                        durum_mesaji = "Sessiz"
                    else:
                        pygame.mixer.music.set_volume(ses_seviyesi)
                        durum_mesaji = "Ses acildi"

        # --- CIZIM ---
        ekran.fill(SIYAH)

        # Baslik
        baslik = baslik_font.render("Muzik Kontrolleri", True, MAVI)
        ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 20))

        # Durum bilgileri
        y_pos = 80
        caliyor = pygame.mixer.music.get_busy()
        durum_renk = YESIL if caliyor else KIRMIZI
        durum_text = "Caliyor" if caliyor and not duraklatildi else (
            "Duraklatildi" if duraklatildi else "Durdu"
        )

        ekran.blit(font.render(f"Durum: {durum_text}", True, durum_renk), (50, y_pos))
        y_pos += 30

        # Ses seviyesi cubugu
        ekran.blit(font.render("Ses Seviyesi:", True, BEYAZ), (50, y_pos))
        mevcut_ses = pygame.mixer.music.get_volume()
        ses_cubugu_ciz(ekran, 200, y_pos + 2, 200, 20, mevcut_ses, YESIL)
        ekran.blit(font.render(f"{mevcut_ses:.1f}", True, BEYAZ), (410, y_pos))
        y_pos += 30

        # Durum mesaji
        ekran.blit(font.render(f"Son islem: {durum_mesaji}", True, SARI), (50, y_pos))
        y_pos += 50

        # Kontrol tuslari
        ekran.blit(baslik_font.render("Kontroller:", True, BEYAZ), (50, y_pos))
        y_pos += 35

        kontroller = [
            ("BOSLUK", "Duraklat / Devam"),
            ("S", "Durdur"),
            ("R", "Yeniden Baslat"),
            ("YUKARI", "Sesi Artir (+0.1)"),
            ("ASAGI", "Sesi Azalt (-0.1)"),
            ("M", "Sessize Al / Ses Ac"),
            ("ESC", "Cikis"),
        ]

        for tus, aciklama in kontroller:
            # Tus kutusu
            tus_metin = tus_font.render(tus, True, SIYAH)
            tus_gen = tus_metin.get_width() + 16
            pygame.draw.rect(ekran, BEYAZ, (60, y_pos, tus_gen, 24), border_radius=4)
            ekran.blit(tus_metin, (68, y_pos + 3))
            # Aciklama
            ekran.blit(font.render(aciklama, True, GRI), (60 + tus_gen + 15, y_pos + 2))
            y_pos += 30

        pygame.display.flip()
        saat.tick(FPS)

    # Temizlik
    pygame.mixer.music.stop()
    pygame.quit()
    if os.path.exists("test_kontrol_muzik.wav"):
        os.remove("test_kontrol_muzik.wav")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
700x480 piksel boyutunda bir pencere acilir.
Ekranda muzik durumu, ses seviyesi cubugu ve kontrol tuslari gosterilir.
BOSLUK ile duraklat/devam, S ile durdur, R ile yeniden baslat,
YUKARI/ASAGI ile ses seviyesi ayarla, M ile sessize al.
ESC ile cikis.
"""
