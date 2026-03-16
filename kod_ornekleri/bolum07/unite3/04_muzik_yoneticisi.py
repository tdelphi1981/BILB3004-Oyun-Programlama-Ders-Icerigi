"""
MusicManager Sinifi - Sahne Bazli Muzik Yonetimi

Bu program profesyonel bir MusicManager sinifi tasarlar.
Farkli sahneler icin farkli muzikler atar ve fade
efektleriyle akici gecisler yapar.

Ogrenilecek kavramlar:
- Sahne bazli muzik yonetimi
- MusicManager sinifi tasarimi
- Otomatik fade gecisleri
- Merkezi ses seviyesi kontrolu

Bolum: 07 - Ses ve Muzik
Unite: 3 - Arka Plan Muzigi

Calistirma: python 04_muzik_yoneticisi.py
Gereksinimler: pygame
"""

import pygame
import os
import math
import struct
import wave

# Sabitler
GENISLIK = 750
YUKSEKLIK = 550
BASLIK = "MusicManager - Sahne Bazli Muzik Yonetimi"
FPS = 60

# Ozel olaylar
MUZIK_BITTI = pygame.USEREVENT + 1

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
MAVI = (70, 130, 180)
YESIL = (50, 200, 100)
KIRMIZI = (200, 60, 60)
SARI = (255, 200, 50)
MOR = (150, 100, 200)
TURUNCU = (255, 160, 50)
GRI = (120, 120, 120)
KOYU_GRI = (40, 40, 40)

# Sahne renkleri
SAHNE_RENKLERI = {
    "menu": MAVI,
    "oyun": YESIL,
    "boss": KIRMIZI,
    "bitis": MOR,
}


def test_muzik_olustur(dosya_adi, frekans=440, sure=15):
    """Farkli frekanslarda test muzik dosyalari olusturur."""
    if not os.path.exists(dosya_adi):
        ornekleme = 22050
        with wave.open(dosya_adi, "w") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(ornekleme)
            for i in range(sure * ornekleme):
                t = i / ornekleme
                # Her sahne icin farkli karakter
                mod = 30 * math.sin(2 * math.pi * 0.2 * t)
                deger = int(10000 * math.sin(2 * math.pi * (frekans + mod) * t))
                wav.writeframes(struct.pack("<h", deger))
    return dosya_adi


class MusicManager:
    """Sahne bazli muzik yonetici sinifi.

    Bu sinif, oyundaki farkli sahneler icin muzik dosyalarini
    yonetir. Fade efektleriyle akici gecisler yapar ve ses
    seviyesini merkezi olarak kontrol eder.
    """

    def __init__(self, varsayilan_ses=0.5, varsayilan_fade=1500):
        """Muzik yoneticisini baslat.

        Args:
            varsayilan_ses: Baslangic ses seviyesi (0.0-1.0)
            varsayilan_fade: Varsayilan fade suresi (milisaniye)
        """
        self.muzikler = {}
        self.mevcut_sahne = None
        self.hedef_sahne = None
        self.ses_seviyesi = varsayilan_ses
        self.varsayilan_fade = varsayilan_fade
        self.gecis_aktif = False

        pygame.mixer.music.set_volume(self.ses_seviyesi)
        pygame.mixer.music.set_endevent(MUZIK_BITTI)

    def muzik_ekle(self, sahne_adi, dosya_yolu):
        """Bir sahneye muzik dosyasi ata.

        Args:
            sahne_adi: Sahne tanimlayicisi (orn: "menu", "boss")
            dosya_yolu: Muzik dosyasinin yolu
        """
        self.muzikler[sahne_adi] = dosya_yolu

    def sahne_degistir(self, yeni_sahne, fade_suresi=None):
        """Sahneyi degistir ve muzigi akici gecis yap.

        Eger ayni sahne zaten caliyorsa hicbir sey yapmaz.
        Fade suresi belirtilmezse varsayilan deger kullanilir.

        Args:
            yeni_sahne: Gecilecek sahne adi
            fade_suresi: Fade suresi (ms), None ise varsayilan
        """
        # Ayni sahneye gecis yapma
        if yeni_sahne == self.mevcut_sahne and not self.gecis_aktif:
            return

        # Tanimlanmamis sahne kontrolu
        if yeni_sahne not in self.muzikler:
            return

        if fade_suresi is None:
            fade_suresi = self.varsayilan_fade

        self.hedef_sahne = yeni_sahne

        # Mevcut muzik caliyorsa fade out yap
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_suresi)
            self.gecis_aktif = True
        else:
            # Muzik calmiyorsa dogrudan baslat
            self._muzik_baslat(yeni_sahne, fade_suresi)

    def _muzik_baslat(self, sahne_adi, fade_suresi):
        """Belirtilen sahnenin muzigini fade-in ile baslatir."""
        dosya = self.muzikler[sahne_adi]
        pygame.mixer.music.load(dosya)
        pygame.mixer.music.set_volume(self.ses_seviyesi)
        pygame.mixer.music.play(loops=-1, fade_ms=fade_suresi)
        self.mevcut_sahne = sahne_adi
        self.hedef_sahne = None
        self.gecis_aktif = False

    def guncelle(self, olay_listesi):
        """Oyun dongusunde her frame cagrilmali.

        Fade gecislerini ve muzik bitis olaylarini yonetir.

        Args:
            olay_listesi: pygame.event.get() ile alinan olaylar
        """
        for olay in olay_listesi:
            if olay.type == MUZIK_BITTI:
                if self.gecis_aktif and self.hedef_sahne:
                    self._muzik_baslat(
                        self.hedef_sahne, self.varsayilan_fade
                    )

    def ses_ayarla(self, seviye):
        """Ses seviyesini ayarla.

        Args:
            seviye: Yeni ses seviyesi (0.0-1.0)
        """
        self.ses_seviyesi = max(0.0, min(1.0, seviye))
        pygame.mixer.music.set_volume(self.ses_seviyesi)

    def ses_artir(self, miktar=0.1):
        """Ses seviyesini artir."""
        self.ses_ayarla(self.ses_seviyesi + miktar)

    def ses_azalt(self, miktar=0.1):
        """Ses seviyesini azalt."""
        self.ses_ayarla(self.ses_seviyesi - miktar)

    def duraklat(self):
        """Muzigi duraklat."""
        pygame.mixer.music.pause()

    def devam_et(self):
        """Duraklatilmis muzige devam et."""
        pygame.mixer.music.unpause()

    @property
    def caliyor_mu(self):
        """Muzik caliyor mu?"""
        return pygame.mixer.music.get_busy()

    @property
    def durum_bilgisi(self):
        """Mevcut durum bilgisini sozluk olarak doner."""
        return {
            "sahne": self.mevcut_sahne or "Yok",
            "hedef": self.hedef_sahne or "-",
            "ses": self.ses_seviyesi,
            "caliyor": self.caliyor_mu,
            "gecis": self.gecis_aktif,
        }


def main():
    """Ana fonksiyon."""
    pygame.init()
    pygame.mixer.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 17)
    baslik_font = pygame.font.SysFont("Arial", 24, bold=True)
    tus_font = pygame.font.SysFont("Arial", 15, bold=True)

    # Test muzik dosyalarini olustur
    muzik_dosyalari = {
        "menu": test_muzik_olustur("test_menu.wav", frekans=262, sure=15),
        "oyun": test_muzik_olustur("test_oyun.wav", frekans=392, sure=15),
        "boss": test_muzik_olustur("test_boss.wav", frekans=523, sure=15),
        "bitis": test_muzik_olustur("test_bitis.wav", frekans=196, sure=15),
    }

    # MusicManager olustur ve muzikleri ekle
    yonetici = MusicManager(varsayilan_ses=0.5, varsayilan_fade=1500)
    for sahne, dosya in muzik_dosyalari.items():
        yonetici.muzik_ekle(sahne, dosya)

    # Menu muzigini baslat
    yonetici.sahne_degistir("menu")

    log_mesajlari = ["[OK] MusicManager baslatildi", "[OK] Menu muzigi caliniyor"]
    duraklatildi = False

    def log_ekle(mesaj):
        log_mesajlari.append(mesaj)
        if len(log_mesajlari) > 8:
            log_mesajlari.pop(0)

    calistir = True
    while calistir:
        olaylar = pygame.event.get()

        for olay in olaylar:
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                # 1: Menu sahnesi
                elif olay.key == pygame.K_1:
                    yonetici.sahne_degistir("menu")
                    log_ekle("[->] Sahne degistiriliyor: Menu")

                # 2: Oyun sahnesi
                elif olay.key == pygame.K_2:
                    yonetici.sahne_degistir("oyun")
                    log_ekle("[->] Sahne degistiriliyor: Oyun")

                # 3: Boss sahnesi
                elif olay.key == pygame.K_3:
                    yonetici.sahne_degistir("boss")
                    log_ekle("[->] Sahne degistiriliyor: Boss")

                # 4: Bitis sahnesi
                elif olay.key == pygame.K_4:
                    yonetici.sahne_degistir("bitis")
                    log_ekle("[->] Sahne degistiriliyor: Bitis")

                # YUKARI/ASAGI: Ses seviyesi
                elif olay.key == pygame.K_UP:
                    yonetici.ses_artir()
                    log_ekle(f"[~] Ses: {yonetici.ses_seviyesi:.1f}")

                elif olay.key == pygame.K_DOWN:
                    yonetici.ses_azalt()
                    log_ekle(f"[~] Ses: {yonetici.ses_seviyesi:.1f}")

                # BOSLUK: Duraklat/Devam
                elif olay.key == pygame.K_SPACE:
                    if duraklatildi:
                        yonetici.devam_et()
                        duraklatildi = False
                        log_ekle("[OK] Devam ediliyor")
                    else:
                        yonetici.duraklat()
                        duraklatildi = True
                        log_ekle("[||] Duraklatildi")

        # MusicManager guncelle (fade gecislerini yonet)
        yonetici.guncelle(olaylar)

        # --- CIZIM ---
        ekran.fill(SIYAH)

        # Sahne gostergesi (ust bar)
        bilgi = yonetici.durum_bilgisi
        sahne_renk = SAHNE_RENKLERI.get(bilgi["sahne"], GRI)
        pygame.draw.rect(ekran, sahne_renk, (0, 0, GENISLIK, 50))
        sahne_metin = baslik_font.render(
            f"Sahne: {bilgi['sahne'].upper()}", True, BEYAZ
        )
        ekran.blit(sahne_metin, (GENISLIK // 2 - sahne_metin.get_width() // 2, 12))

        y_pos = 65

        # Durum paneli
        ekran.blit(baslik_font.render("MusicManager Durumu:", True, BEYAZ), (30, y_pos))
        y_pos += 30

        durum_satirlari = [
            (f"Mevcut Sahne: {bilgi['sahne']}", sahne_renk),
            (f"Hedef Sahne: {bilgi['hedef']}", TURUNCU if bilgi["gecis"] else GRI),
            (f"Ses Seviyesi: {bilgi['ses']:.1f}", BEYAZ),
            (f"Caliyor: {'Evet' if bilgi['caliyor'] else 'Hayir'}", YESIL if bilgi["caliyor"] else KIRMIZI),
            (f"Gecis Aktif: {'Evet' if bilgi['gecis'] else 'Hayir'}", SARI if bilgi["gecis"] else GRI),
        ]

        for metin, renk in durum_satirlari:
            ekran.blit(font.render(metin, True, renk), (50, y_pos))
            y_pos += 22

        y_pos += 10

        # Sahne butonlari (gorsel gosterge)
        ekran.blit(baslik_font.render("Sahneler:", True, BEYAZ), (30, y_pos))
        y_pos += 28

        sahneler = [
            ("1", "Menu", MAVI, "Sakin melodi (262 Hz)"),
            ("2", "Oyun", YESIL, "Aksiyon ritmi (392 Hz)"),
            ("3", "Boss", KIRMIZI, "Epik savas (523 Hz)"),
            ("4", "Bitis", MOR, "Huzunlu kapanıs (196 Hz)"),
        ]

        for tus, isim, renk, aciklama in sahneler:
            aktif = bilgi["sahne"] == isim.lower()
            # Aktif sahne vurgulama
            if aktif:
                pygame.draw.rect(ekran, renk, (40, y_pos - 2, GENISLIK - 80, 24),
                                 border_radius=4)
                metin_renk = BEYAZ
            else:
                metin_renk = renk

            tus_metin = tus_font.render(tus, True, SIYAH if aktif else BEYAZ)
            tus_gen = 24
            if not aktif:
                pygame.draw.rect(ekran, renk, (50, y_pos, tus_gen, 20), border_radius=3)
            ekran.blit(tus_metin, (56, y_pos + 1))
            ekran.blit(font.render(f"{isim} - {aciklama}", True, metin_renk),
                       (50 + tus_gen + 10, y_pos + 1))
            y_pos += 28

        y_pos += 5

        # Diger kontroller
        ekran.blit(font.render("YUKARI/ASAGI: Ses | BOSLUK: Duraklat | ESC: Cikis",
                               True, GRI), (30, y_pos))
        y_pos += 30

        # Log
        pygame.draw.line(ekran, GRI, (30, y_pos), (GENISLIK - 30, y_pos))
        y_pos += 8
        ekran.blit(baslik_font.render("Log:", True, SARI), (30, y_pos))
        y_pos += 25

        for mesaj in log_mesajlari:
            if "[OK]" in mesaj:
                renk = YESIL
            elif "[->]" in mesaj:
                renk = TURUNCU
            elif "[!]" in mesaj:
                renk = KIRMIZI
            elif "[||]" in mesaj:
                renk = SARI
            else:
                renk = GRI
            ekran.blit(font.render(mesaj, True, renk), (40, y_pos))
            y_pos += 20

        pygame.display.flip()
        saat.tick(FPS)

    # Temizlik
    pygame.mixer.music.stop()
    pygame.quit()
    for dosya in muzik_dosyalari.values():
        if os.path.exists(dosya):
            os.remove(dosya)


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
750x550 piksel boyutunda bir pencere acilir.
Ust barda mevcut sahne gorsel olarak gosterilir (renkli bar).
MusicManager durum bilgileri (sahne, ses, gecis) gosterilir.
1/2/3/4 tuslariyla farkli sahnelere fade gecisleriyle gecilir.
YUKARI/ASAGI ile ses, BOSLUK ile duraklat, ESC ile cikis.
"""
