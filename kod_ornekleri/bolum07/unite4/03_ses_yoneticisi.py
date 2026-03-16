"""
SoundManager - Merkezi Ses Yonetim Sinifi

Bu program oyunlarda kullanilabilecek tam kapsamli bir
SoundManager sinifi icermektedir. SFX, muzik ve ses ayarlari
tek bir sinifta yonetilir.

Ogrenilecek kavramlar:
- Merkezi ses yonetim mimarisi
- Katman bazli volume kontrolu
- Master volume ile oransal ayarlama
- Sessiz modu (toggle)
- Muzik fade in/out

Bolum: 07 - Ses ve Muzik
Unite: 4 - Ses Tasarimi Prensipleri

Calistirma: python 03_ses_yoneticisi.py
Gereksinimler: pygame
"""

import os
import pygame


class SoundManager:
    """Merkezi ses yonetim sinifi.

    Tum ses islemlerini (SFX, muzik, volume) tek noktadan yonetir.
    Oyun icinde tek bir ornek (instance) olusturulup paylasilir.
    """

    def __init__(self, ses_dizini="assets/sounds"):
        """Ses sistemini baslat ve sesleri yukle.

        Args:
            ses_dizini: Ses dosyalarinin bulundugu ana dizin.
        """
        # Volume seviyeleri (0.0 - 1.0)
        self.master_volume = 1.0
        self.sfx_volume = 0.75
        self.bgm_volume = 0.40
        self._onceki_volume = 1.0

        # Ses sozlukleri
        self.sesler = {}
        self.ses_dizini = ses_dizini

        # Sesleri yukle
        self._sesleri_yukle()

    def _sesleri_yukle(self):
        """SFX seslerini bellege yukle."""
        sfx_dosyalari = {
            "ates": "sfx/ates.ogg",
            "patlama": "sfx/patlama.ogg",
            "hasar": "sfx/hasar.ogg",
            "bonus": "sfx/bonus.ogg",
            "menu_tikla": "sfx/menu_tikla.ogg",
            "oyun_bitti": "sfx/oyun_bitti.ogg",
        }
        yuklenen = 0
        for ad, dosya in sfx_dosyalari.items():
            yol = os.path.join(self.ses_dizini, dosya)
            if os.path.exists(yol):
                try:
                    self.sesler[ad] = pygame.mixer.Sound(yol)
                    self.sesler[ad].set_volume(
                        self.sfx_volume * self.master_volume
                    )
                    yuklenen += 1
                except pygame.error as hata:
                    print(f"[X] Ses yuklenemedi: {ad} - {hata}")
        print(f"[OK] {yuklenen}/{len(sfx_dosyalari)} SFX sesi yuklendi")

    def cal(self, ad, dongu=0):
        """Isimle SFX sesi cal.

        Args:
            ad: Ses adi (ornek: "ates", "patlama")
            dongu: Tekrar sayisi (0 = bir kez, -1 = sonsuz)
        """
        ses = self.sesler.get(ad)
        if ses:
            ses.play(loops=dongu)
        else:
            pass  # Ses bulunamazsa sessizce devam et

    def muzik_cal(self, dosya, dongu=-1, fade_ms=1000):
        """Arka plan muzigini cal.

        Args:
            dosya: Muzik dosya adi (ornek: "uzay_temasi.ogg")
            dongu: Tekrar sayisi (-1 = sonsuz)
            fade_ms: Fade in suresi (milisaniye)
        """
        yol = os.path.join(self.ses_dizini, "muzik", dosya)
        if os.path.exists(yol):
            try:
                pygame.mixer.music.load(yol)
                pygame.mixer.music.set_volume(
                    self.bgm_volume * self.master_volume
                )
                pygame.mixer.music.play(loops=dongu, fade_ms=fade_ms)
                print(f"[OK] Muzik baslatildi: {dosya}")
            except pygame.error as hata:
                print(f"[X] Muzik yuklenemedi: {hata}")
        else:
            print(f"[UYARI] Muzik dosyasi bulunamadi: {yol}")

    def muzik_durdur(self, fade_ms=500):
        """Muzigi fade out ile durdur.

        Args:
            fade_ms: Fade out suresi (milisaniye)
        """
        pygame.mixer.music.fadeout(fade_ms)

    def muzik_duraklat(self):
        """Muzigi duraklat."""
        pygame.mixer.music.pause()

    def muzik_devam(self):
        """Duraklatilmis muzige devam et."""
        pygame.mixer.music.unpause()

    def master_ayarla(self, deger):
        """Master volume degistir ve tum sesleri guncelle.

        Args:
            deger: Volume seviyesi (0.0 - 1.0)
        """
        self.master_volume = max(0.0, min(1.0, deger))
        # SFX seslerini guncelle
        for ses in self.sesler.values():
            ses.set_volume(self.sfx_volume * self.master_volume)
        # Muzik volume guncelle
        pygame.mixer.music.set_volume(
            self.bgm_volume * self.master_volume
        )

    def sfx_ayarla(self, deger):
        """SFX volume degistir.

        Args:
            deger: Volume seviyesi (0.0 - 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, deger))
        for ses in self.sesler.values():
            ses.set_volume(self.sfx_volume * self.master_volume)

    def bgm_ayarla(self, deger):
        """BGM volume degistir.

        Args:
            deger: Volume seviyesi (0.0 - 1.0)
        """
        self.bgm_volume = max(0.0, min(1.0, deger))
        pygame.mixer.music.set_volume(
            self.bgm_volume * self.master_volume
        )

    def sessiz_mi(self):
        """Master volume sifir mi kontrol et.

        Returns:
            bool: Sessiz modda ise True
        """
        return self.master_volume == 0.0

    def sessize_al(self):
        """Tum sesleri kapat/ac (toggle)."""
        if self.master_volume > 0:
            self._onceki_volume = self.master_volume
            self.master_ayarla(0.0)
        else:
            self.master_ayarla(self._onceki_volume)

    def durum_yazdir(self):
        """Ses sistemi durumunu konsola yazdir."""
        durum = "SESSIZ" if self.sessiz_mi() else "ACIK"
        print(f"\n--- Ses Durumu [{durum}] ---")
        print(f"  Master:  {self.master_volume:.0%}")
        print(f"  SFX:     {self.sfx_volume:.0%}"
              f" (gercek: {self.sfx_volume * self.master_volume:.0%})")
        print(f"  BGM:     {self.bgm_volume:.0%}"
              f" (gercek: {self.bgm_volume * self.master_volume:.0%})")
        print(f"  Yuklenen: {len(self.sesler)} ses")


def main():
    """Ana fonksiyon - SoundManager demo."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    ekran = pygame.display.set_mode((600, 300))
    pygame.display.set_caption("SoundManager Demo")
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    # SoundManager olustur
    ses = SoundManager("assets/sounds")
    ses.durum_yazdir()

    print("\n[BILGI] Tuslar:")
    print("  M: Sessiz modu (toggle)")
    print("  Yukari/Asagi: Master volume")
    print("  Sol/Sag: SFX volume")
    print("  ESC: Cikis")

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_m:
                    ses.sessize_al()
                    ses.durum_yazdir()
                elif olay.key == pygame.K_UP:
                    ses.master_ayarla(ses.master_volume + 0.1)
                    ses.durum_yazdir()
                elif olay.key == pygame.K_DOWN:
                    ses.master_ayarla(ses.master_volume - 0.1)
                    ses.durum_yazdir()
                elif olay.key == pygame.K_RIGHT:
                    ses.sfx_ayarla(ses.sfx_volume + 0.1)
                    ses.durum_yazdir()
                elif olay.key == pygame.K_LEFT:
                    ses.sfx_ayarla(ses.sfx_volume - 0.1)
                    ses.durum_yazdir()

        ekran.fill((30, 30, 50))

        bilgiler = [
            f"Master: {ses.master_volume:.0%}",
            f"SFX:    {ses.sfx_volume:.0%} "
            f"(gercek: {ses.sfx_volume * ses.master_volume:.0%})",
            f"BGM:    {ses.bgm_volume:.0%} "
            f"(gercek: {ses.bgm_volume * ses.master_volume:.0%})",
            f"Durum:  {'SESSIZ' if ses.sessiz_mi() else 'ACIK'}",
            "",
            "M: Sessiz | Yukari/Asagi: Master | Sol/Sag: SFX",
        ]

        y = 40
        for satir in bilgiler:
            renk = (255, 100, 100) if "SESSIZ" in satir else (200, 200, 200)
            metin = font.render(satir, True, renk)
            ekran.blit(metin, (40, y))
            y += 28

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
[OK] 0/6 SFX sesi yuklendi

--- Ses Durumu [ACIK] ---
  Master:  100%
  SFX:     75% (gercek: 75%)
  BGM:     40% (gercek: 40%)
  Yuklenen: 0 ses

(Gercek ses dosyalari olmadan yuklenen ses sayisi 0 olur.
Ses dosyalari assets/sounds/sfx/ altina eklendiginde otomatik yuklenir.)
"""
