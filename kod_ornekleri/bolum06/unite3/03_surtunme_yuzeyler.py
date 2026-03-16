"""
Surtunme ve Yuzey Tipleri

Farkli yuzey tiplerinin (normal, buz, kum) surtunme katsayilarini
gosteren ornek. Karakter farkli renkteki bolgelerden gecerken
hareket hissiyati degisir.

Ogrenilecek kavramlar:
- Surtunme katsayisi
- Yuzey tabanli surtunme
- Ivme ve surtunme dengesi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 3 - Temel Fizik Simulasyonu

Calistirma: python 03_surtunme_yuzeyler.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
ZEMIN_Y = 500

# Yuzey tipleri: (renk, surtunme katsayisi, isim)
YUZEYLER = [
    {"x_baslangic": 0, "x_bitis": 250, "renk": (80, 60, 40),
     "surtunme": 0.60, "isim": "Kum"},
    {"x_baslangic": 250, "x_bitis": 550, "renk": (100, 100, 100),
     "surtunme": 0.80, "isim": "Normal"},
    {"x_baslangic": 550, "x_bitis": 800, "renk": (180, 220, 255),
     "surtunme": 0.98, "isim": "Buz"},
]


class SurtunmeKarakter(pygame.sprite.Sprite):
    """Surtunme etkisi altinda hareket eden karakter."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.hiz_x = 0
        self.ivme = 0.5
        self.max_hiz = 8.0
        self.aktif_surtunme = 0.80
        self.aktif_yuzey_isim = "Normal"

    def update(self):
        tuslar = pygame.key.get_pressed()

        if tuslar[pygame.K_RIGHT]:
            self.hiz_x += self.ivme
        elif tuslar[pygame.K_LEFT]:
            self.hiz_x -= self.ivme

        # Hiz siniri
        if self.hiz_x > self.max_hiz:
            self.hiz_x = self.max_hiz
        elif self.hiz_x < -self.max_hiz:
            self.hiz_x = -self.max_hiz

        # Aktif yuzeyin surtunmesini uygula
        self.hiz_x *= self.aktif_surtunme

        # Cok kucuk hizlari sifirla
        if abs(self.hiz_x) < 0.1:
            self.hiz_x = 0

        # Konum guncelle
        self.rect.x += int(self.hiz_x)

        # Ekran siniri
        if self.rect.left < 0:
            self.rect.left = 0
            self.hiz_x = 0
        elif self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = 0

        # Hangi yuzeyde oldugumuzu belirle
        for yuzey in YUZEYLER:
            if yuzey["x_baslangic"] <= self.rect.centerx < yuzey["x_bitis"]:
                self.aktif_surtunme = yuzey["surtunme"]
                self.aktif_yuzey_isim = yuzey["isim"]
                break


def main():
    """Ana fonksiyon."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Surtunme ve Yuzey Tipleri")
    saat = pygame.time.Clock()

    karakter = SurtunmeKarakter(400, ZEMIN_Y)
    tum_nesneler = pygame.sprite.Group(karakter)

    font = pygame.font.Font(None, 28)
    baslik_font = pygame.font.Font(None, 36)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        tum_nesneler.update()

        # Cizim
        ekran.fill((30, 30, 50))

        # Yuzeyleri ciz
        for yuzey in YUZEYLER:
            genislik = yuzey["x_bitis"] - yuzey["x_baslangic"]
            pygame.draw.rect(ekran, yuzey["renk"],
                             (yuzey["x_baslangic"], ZEMIN_Y,
                              genislik, YUKSEKLIK - ZEMIN_Y))

            # Yuzey etiketi
            etiket = font.render(yuzey["isim"], True, (255, 255, 255))
            etiket_x = yuzey["x_baslangic"] + genislik // 2 - etiket.get_width() // 2
            ekran.blit(etiket, (etiket_x, ZEMIN_Y + 20))

            # Katsayi bilgisi
            katsayi = font.render(f"k={yuzey['surtunme']}", True, (200, 200, 200))
            katsayi_x = yuzey["x_baslangic"] + genislik // 2 - katsayi.get_width() // 2
            ekran.blit(katsayi, (katsayi_x, ZEMIN_Y + 50))

        tum_nesneler.draw(ekran)

        # Bilgi paneli
        bilgi = font.render(
            f"Hiz: {karakter.hiz_x:.1f} | "
            f"Yuzey: {karakter.aktif_yuzey_isim} | "
            f"Surtunme: {karakter.aktif_surtunme}",
            True, (200, 200, 200)
        )
        ekran.blit(bilgi, (10, 10))

        kontrol = font.render(
            "Ok Tuslari: Hareket",
            True, (150, 150, 150)
        )
        ekran.blit(kontrol, (10, 40))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
Ekranin alt kismi uc farkli renkli bolgeden olusur:
- Kahverengi (Kum): Yuksek surtunme, karakter hizla yavastar
- Gri (Normal): Standart surtunme
- Acik mavi (Buz): Dusuk surtunme, karakter uzun sure kayar

Karakter ok tuslariyla hareket eder ve farkli yuzeylerden gecerken
hareket hissiyati belirgin sekilde degisir.
"""
