"""
Ses Onyukleme ve Havuz Sistemi

Bu program tum sesleri onceden yukleme (preloading) ve
ayni sesin birden fazla kopyasini yoneten havuz (pool) sistemini gosterir.

Ogrenilecek kavramlar:
- Ses dosyalarini toplu yukleme
- SesYukleyici sinifi ile isimle erisim
- SesHavuzu sinifi ile ust uste ses calma
- Bellek verimli ses yonetimi

Bolum: 07 - Ses ve Muzik
Unite: 4 - Ses Tasarimi Prensipleri

Calistirma: python 02_ses_onyukleme.py
Gereksinimler: pygame
"""

import os
import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 400
FPS = 60


class SesYukleyici:
    """Tum sesleri onceden yukleyen yardimci sinif."""

    def __init__(self, ses_dizini):
        """Ses dizinini ayarla ve bos sozluk olustur."""
        self.ses_dizini = ses_dizini
        self.sesler = {}
        self.yuklenen_boyut = 0  # Toplam byte

    def hepsini_yukle(self):
        """Dizindeki tum .ogg ve .wav dosyalarini yukle."""
        if not os.path.isdir(self.ses_dizini):
            print(f"[UYARI] Dizin bulunamadi: {self.ses_dizini}")
            return

        for dosya in sorted(os.listdir(self.ses_dizini)):
            if dosya.endswith((".ogg", ".wav")):
                ad = os.path.splitext(dosya)[0]
                yol = os.path.join(self.ses_dizini, dosya)
                try:
                    self.sesler[ad] = pygame.mixer.Sound(yol)
                    boyut = os.path.getsize(yol)
                    self.yuklenen_boyut += boyut
                    print(f"  [OK] {ad} ({boyut / 1024:.1f} KB)")
                except pygame.error as hata:
                    print(f"  [X] {ad}: {hata}")

        toplam_mb = self.yuklenen_boyut / (1024 * 1024)
        print(f"\nToplam: {len(self.sesler)} ses, {toplam_mb:.2f} MB")

    def al(self, ad):
        """Isimle ses nesnesini dondur."""
        ses = self.sesler.get(ad)
        if ses is None:
            print(f"[UYARI] Ses bulunamadi: {ad}")
        return ses

    def listele(self):
        """Yuklenen seslerin listesini yazdir."""
        print("\n--- Yuklenen Sesler ---")
        for ad in self.sesler:
            print(f"  - {ad}")


class SesHavuzu:
    """Ayni sesin birden fazla kopyasini yoneten havuz."""

    def __init__(self, ses_dosyasi, kopya_sayisi=4):
        """Ses dosyasinin belirtilen sayida kopyasini olustur."""
        self.sesler = []
        self.siradaki = 0
        self.kopya_sayisi = kopya_sayisi

        for _ in range(kopya_sayisi):
            self.sesler.append(pygame.mixer.Sound(ses_dosyasi))

    def cal(self, volume=1.0):
        """Siradaki kopyayi cal ve bir sonrakine gec."""
        ses = self.sesler[self.siradaki]
        ses.set_volume(volume)
        ses.play()
        self.siradaki = (self.siradaki + 1) % self.kopya_sayisi

    def tumu_durdur(self):
        """Tum kopyalari durdur."""
        for ses in self.sesler:
            ses.stop()


def main():
    """Ana fonksiyon - Ses yukleme ve havuz demostrasyon."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Ses Onyukleme ve Havuz Sistemi")
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    # Ses yukleyici ornegi (gercek dosya yoksa demo modu)
    print("=== Ses Onyukleme Sistemi ===")
    print("\n[BILGI] Gercek ses dosyalari olmadan demo modunda calisir.")
    print("[BILGI] 'assets/sounds/sfx/' dizini varsa dosyalar yuklenir.\n")

    yukleyici = SesYukleyici("assets/sounds/sfx")
    yukleyici.hepsini_yukle()

    # Demo: Havuz sistemi aciklamasi
    print("\n=== Ses Havuzu Sistemi ===")
    print("SesHavuzu('ates.ogg', kopya_sayisi=4)")
    print("  Her cal() cagrisi siradaki kopyayi kullanir:")
    print("  cal() -> kopya 0")
    print("  cal() -> kopya 1")
    print("  cal() -> kopya 2")
    print("  cal() -> kopya 3")
    print("  cal() -> kopya 0 (basa doner)")

    bilgiler = [
        "Ses Onyukleme ve Havuz Sistemi",
        "",
        "SesYukleyici: Tum sesleri oyun basinda yukler",
        "  - hepsini_yukle(): Dizindeki tum .ogg/.wav dosyalarini tarar",
        "  - al(ad): Isimle ses nesnesine erisir",
        "",
        "SesHavuzu: Ayni sesin kopyalariyla ust uste calma",
        "  - Kopya sayisi: Genellikle 3-4 yeterli",
        "  - Dairesel indeks ile sirayla kullanir",
        "  - Hizli ates gibi tekrarlayan sesler icin ideal",
        "",
        "Konsol ciktisini kontrol edin.",
        "ESC: Cikis",
    ]

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        ekran.fill((25, 25, 40))

        y = 30
        for satir in bilgiler:
            if satir == "":
                y += 10
                continue
            renk = (255, 200, 100) if satir.startswith("Ses") else (200, 200, 200)
            metin = font.render(satir, True, renk)
            ekran.blit(metin, (40, y))
            y += 24

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
Konsola ses yukleme durumu yazdirilir.
Eger 'assets/sounds/sfx/' dizini varsa dosyalar listelenir.
Havuz sistemi aciklamasi konsola yazdirilir.
800x400 boyutunda bilgi penceresi acilir.
"""
