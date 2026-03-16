"""
Ses Miksaji - Katman Bazli Volume Yonetimi

Bu program ses katmanlarini (SFX, BGM, UI, Ambient) ve
master volume ile katman bazli ses seviyesi yonetimini gosterir.

Ogrenilecek kavramlar:
- Ses katmanlari ve volume hiyerarsisi
- Master volume ile oransal kontrol
- Kanal bazli ses onceligi
- set_num_channels() ile kanal yonetimi

Bolum: 07 - Ses ve Muzik
Unite: 4 - Ses Tasarimi Prensipleri

Calistirma: python 01_ses_miksaji.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60


class SesMiksaji:
    """Katman bazli ses miksaji yonetimi."""

    def __init__(self):
        """Ses katmanlarini ve volume seviyelerini baslat."""
        self.katmanlar = {
            "master": 1.0,
            "sfx": 0.75,
            "bgm": 0.40,
            "ui": 0.55,
            "ambient": 0.30,
        }
        # Kanal sayisini artir
        pygame.mixer.set_num_channels(16)

        # Oncelikli kanallar
        self.kanal_oyuncu = pygame.mixer.Channel(0)
        self.kanal_dusman = pygame.mixer.Channel(1)
        self.kanal_ui = pygame.mixer.Channel(2)

    def gercek_volume(self, katman_adi):
        """Katmanin master volume ile carpilmis gercek seviyesini dondur."""
        if katman_adi not in self.katmanlar:
            return 0.0
        return self.katmanlar[katman_adi] * self.katmanlar["master"]

    def katman_ayarla(self, katman_adi, deger):
        """Belirli bir katmanin volume seviyesini ayarla."""
        deger = max(0.0, min(1.0, deger))
        self.katmanlar[katman_adi] = deger

    def master_ayarla(self, deger):
        """Master volume degistir."""
        deger = max(0.0, min(1.0, deger))
        self.katmanlar["master"] = deger

    def durum_yazdir(self):
        """Tum katmanlarin durumunu yazdir."""
        print("\n--- Ses Miksaj Durumu ---")
        for ad, seviye in self.katmanlar.items():
            gercek = self.gercek_volume(ad) if ad != "master" else seviye
            bar_uzunluk = int(gercek * 20)
            bar = "#" * bar_uzunluk + "." * (20 - bar_uzunluk)
            print(f"  {ad:10s}: {seviye:.0%} [Gercek: {gercek:.0%}] [{bar}]")


def main():
    """Ana fonksiyon."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Ses Miksaji Ornegi")
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    miksaj = SesMiksaji()

    # Secili katman
    katman_adlari = ["master", "sfx", "bgm", "ui", "ambient"]
    secili_index = 0

    print("[BILGI] Yukari/Asagi: Katman sec")
    print("[BILGI] Sol/Sag: Volume ayarla")
    print("[BILGI] ESC: Cikis")

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_UP:
                    secili_index = (secili_index - 1) % len(katman_adlari)
                elif olay.key == pygame.K_DOWN:
                    secili_index = (secili_index + 1) % len(katman_adlari)
                elif olay.key == pygame.K_RIGHT:
                    ad = katman_adlari[secili_index]
                    yeni = miksaj.katmanlar[ad] + 0.05
                    if ad == "master":
                        miksaj.master_ayarla(yeni)
                    else:
                        miksaj.katman_ayarla(ad, yeni)
                    miksaj.durum_yazdir()
                elif olay.key == pygame.K_LEFT:
                    ad = katman_adlari[secili_index]
                    yeni = miksaj.katmanlar[ad] - 0.05
                    if ad == "master":
                        miksaj.master_ayarla(yeni)
                    else:
                        miksaj.katman_ayarla(ad, yeni)
                    miksaj.durum_yazdir()

        # Cizim
        ekran.fill((30, 30, 50))

        # Baslik
        baslik = font.render("Ses Miksaji - Katman Kontrol", True, (255, 255, 255))
        ekran.blit(baslik, (GENISLIK // 2 - baslik.get_width() // 2, 30))

        # Katmanlari ciz
        renkler = {
            "master": (70, 130, 180),
            "sfx": (180, 30, 30),
            "bgm": (21, 122, 81),
            "ui": (255, 138, 88),
            "ambient": (100, 149, 237),
        }

        y_baslangic = 100
        for i, ad in enumerate(katman_adlari):
            seviye = miksaj.katmanlar[ad]
            gercek = miksaj.gercek_volume(ad) if ad != "master" else seviye
            renk = renkler[ad]
            secili = i == secili_index

            # Secili gosterge
            if secili:
                pygame.draw.rect(ekran, (60, 60, 80),
                                 (50, y_baslangic + i * 80 - 5, 700, 70),
                                 border_radius=5)

            # Katman adi
            ad_metin = font.render(f"{ad.upper()}", True, renk)
            ekran.blit(ad_metin, (80, y_baslangic + i * 80))

            # Volume bar (arka plan)
            bar_x = 200
            bar_y = y_baslangic + i * 80 + 5
            bar_genislik = 400
            bar_yukseklik = 25
            pygame.draw.rect(ekran, (50, 50, 70),
                             (bar_x, bar_y, bar_genislik, bar_yukseklik),
                             border_radius=3)

            # Volume bar (dolu)
            dolu_genislik = int(seviye * bar_genislik)
            if dolu_genislik > 0:
                pygame.draw.rect(ekran, renk,
                                 (bar_x, bar_y, dolu_genislik, bar_yukseklik),
                                 border_radius=3)

            # Gercek volume bar (kucuk)
            if ad != "master":
                gercek_genislik = int(gercek * bar_genislik)
                pygame.draw.rect(ekran, (255, 255, 255),
                                 (bar_x, bar_y + 30, gercek_genislik, 5),
                                 border_radius=2)

            # Yuzde
            yuzde = font.render(f"{seviye:.0%}", True, (200, 200, 200))
            ekran.blit(yuzde, (bar_x + bar_genislik + 20, y_baslangic + i * 80))

        # Talimatlar
        talimat = font.render(
            "Yukari/Asagi: Sec | Sol/Sag: Ayarla | ESC: Cikis",
            True, (150, 150, 150)
        )
        ekran.blit(talimat, (GENISLIK // 2 - talimat.get_width() // 2, YUKSEKLIK - 40))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 boyutunda bir pencere acilir.
Ekranda 5 ses katmani (Master, SFX, BGM, UI, Ambient)
renkli volume barlariyla gosterilir.
Yukari/Asagi tuslariyla katman secilir.
Sol/Sag tuslariyla volume ayarlanir.
Konsola miksaj durumu yazdirilir.
"""
