"""
groupcollide ile Mermi-Hedef Oyunu

Ekranin ustunde rastgele hedefler belirir ve oyuncu
Space tusuyla mermi atar. groupcollide() fonksiyonu
ile mermi-hedef carpismalari tespit edilir.

Ogrenilecek kavramlar:
- pygame.sprite.groupcollide() kullanimi
- Iki grup arasi carpisma sozlugu
- dokill1 ve dokill2 parametreleri
- Mermi atesleme mekanigi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 2 - Sprite Carpisma Fonksiyonlari

Calistirma: python 02_groupcollide_hedef.py
Gereksinimler: pygame
"""

import pygame
import random
import sys


# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "groupcollide - Mermi ve Hedef"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (220, 50, 50)
YESIL = (50, 200, 50)
SARI = (255, 220, 50)
ACIK_MAVI = (100, 180, 255)
KOYU_MAVI = (8, 8, 32)
GRI = (150, 150, 150)
TURUNCU = (255, 150, 50)

# Oyun ayarlari
HEDEF_SAYISI = 8
MERMI_HIZ = -7
OYUNCU_HIZ = 5


# --- Sprite Siniflari ---
class Oyuncu(pygame.sprite.Sprite):
    """Klavye ile kontrol edilen oyuncu Sprite'i."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        # Ucgen gemi sekli
        pygame.draw.polygon(
            self.image, ACIK_MAVI,
            [(25, 0), (50, 40), (0, 40)]
        )
        pygame.draw.polygon(
            self.image, BEYAZ,
            [(25, 0), (50, 40), (0, 40)], 2
        )
        # Kokpit
        pygame.draw.circle(self.image, SARI, (25, 22), 4)
        self.rect = self.image.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 20
        )
        self.hiz = OYUNCU_HIZ
        self.sinir = pygame.Rect(0, 0, GENISLIK, YUKSEKLIK)

    def update(self):
        """Klavye ile yatay hareket."""
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += self.hiz
        self.rect.clamp_ip(self.sinir)


class Mermi(pygame.sprite.Sprite):
    """Yukari dogru hareket eden mermi."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12), pygame.SRCALPHA)
        pygame.draw.rect(self.image, SARI, (0, 0, 4, 12))
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz = MERMI_HIZ

    def update(self):
        """Yukari dogru hareket et."""
        self.rect.y += self.hiz
        if self.rect.bottom < 0:
            self.kill()


class Hedef(pygame.sprite.Sprite):
    """Ekranin ustunde yatay hareket eden hedef."""

    def __init__(self):
        super().__init__()
        self.boyut = random.choice([30, 40, 50])
        self.image = pygame.Surface(
            (self.boyut, self.boyut), pygame.SRCALPHA
        )
        # Kirmizi daire hedef
        yaricap = self.boyut // 2
        pygame.draw.circle(
            self.image, KIRMIZI, (yaricap, yaricap), yaricap
        )
        pygame.draw.circle(
            self.image, BEYAZ, (yaricap, yaricap), yaricap, 2
        )
        # Ic halka
        pygame.draw.circle(
            self.image, TURUNCU, (yaricap, yaricap), yaricap // 2
        )

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, GENISLIK - self.boyut - 10)
        self.rect.y = random.randint(30, YUKSEKLIK // 3)
        self.hiz_x = random.choice([-2, -1, 1, 2])
        # Kucuk hedefler daha cok puan
        self.puan = 30 if self.boyut == 30 else (
            20 if self.boyut == 40 else 10
        )

    def update(self):
        """Yatay hareket et, kenarlarda sekme."""
        self.rect.x += self.hiz_x
        if self.rect.left < 0 or self.rect.right > GENISLIK:
            self.hiz_x = -self.hiz_x


def hedefleri_olustur(tum_spritelar, hedefler, adet):
    """Belirtilen sayida hedef olustur ve gruplara ekle."""
    for _ in range(adet):
        hedef = Hedef()
        tum_spritelar.add(hedef)
        hedefler.add(hedef)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # --- Sprite Gruplari ---
    tum_spritelar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()
    hedefler = pygame.sprite.Group()

    # Oyuncuyu olustur
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Hedefleri olustur
    hedefleri_olustur(tum_spritelar, hedefler, HEDEF_SAYISI)

    # Skor
    skor = 0
    tur = 1

    # --- Ana Oyun Dongusu ---
    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olay isleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_SPACE:
                    # Mermi olustur (geminin burnundan)
                    mermi = Mermi(
                        oyuncu.rect.centerx, oyuncu.rect.top
                    )
                    tum_spritelar.add(mermi)
                    mermiler.add(mermi)

        # --- Guncelleme ---
        tum_spritelar.update()

        # --- Carpisma kontrolu ---
        # groupcollide: mermiler ile hedefler arasinda
        # (True, True): carpisan mermi ve hedef ikisi de silinir
        carpismalar = pygame.sprite.groupcollide(
            mermiler, hedefler, True, True
        )

        # Carpismalar sozlugunu isle
        for mermi, vurulan_hedefler in carpismalar.items():
            for hedef in vurulan_hedefler:
                skor += hedef.puan

        # Tum hedefler vurulduysa yeni tur
        if len(hedefler) == 0:
            tur += 1
            hedefleri_olustur(
                tum_spritelar, hedefler, HEDEF_SAYISI + tur
            )

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        # HUD
        skor_yazi = font.render(f"Skor: {skor}", True, BEYAZ)
        ekran.blit(skor_yazi, (15, 15))

        tur_yazi = font.render(f"Tur: {tur}", True, SARI)
        ekran.blit(tur_yazi, (15, 50))

        hedef_yazi = font.render(
            f"Hedef: {len(hedefler)}", True, GRI
        )
        ekran.blit(hedef_yazi, (GENISLIK - 150, 15))

        bilgi = font.render(
            "A/D: Hareket | Space: Ates | ESC: Cikis", True, GRI
        )
        bilgi_rect = bilgi.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 10
        )
        ekran.blit(bilgi, bilgi_rect)

        pygame.display.flip()

    # --- Temizlik ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
Koyu mavi arka plan uzerinde ekranin ust yarisinda
farkli boyutlarda kirmizi hedef daireleri yatay olarak
hareket eder. Ekranin altinda mavi ucgen gemi A/D veya
ok tuslari ile hareket ettirilir.

Space tusuna basinca sari mermiler yukari firlar.
Mermi hedefe isabet edince ikisi de yok olur ve
puan kazanilir (kucuk hedefler daha cok puan verir).
Tum hedefler vurulunca yeni tur baslar ve bir fazla
hedef eklenir.

Sol ustte skor ve tur numarasi, sag ustte kalan
hedef sayisi gosterilir.
"""
