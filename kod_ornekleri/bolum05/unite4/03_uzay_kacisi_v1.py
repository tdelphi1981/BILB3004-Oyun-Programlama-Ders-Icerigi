"""
Uzay Kacisi v1 - Oyuncu Gemisi ve Kayan Yildiz Arka Plani

Bu program, Uzay Kacisi serisinin ilk versiyonudur.
Sprite gruplari kullanarak bir uzay gemisini kontrol
ederken kayan yildiz arka plani ile uzay atmosferi
olusturur. Hayatta kalma suresi skorlama sistemi icerir.

Ogrenilecek kavramlar:
- Sprite alt siniflari: Oyuncu ve Yildiz
- Sprite gruplari ile toplu yonetim
- clamp_ip ile ekran siniri kontrolu
- Kayan arka plan (parallax) etkisi
- Basit font ile skor gosterimi
- gorsel_yukle() fallback fonksiyonu

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 4 - Sprite Gruplari

Calistirma: python 03_uzay_kacisi_v1.py
Gereksinimler: pygame
"""

import pygame
import random
import os
import sys


# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Kacisi v1"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (8, 8, 32)
ACIK_MAVI = (100, 180, 255)
SARI = (255, 220, 50)
GRI = (150, 150, 160)
KOYU_GRI = (80, 80, 90)

# Oyuncu ayarlari
OYUNCU_HIZ = 5
OYUNCU_BOYUT = (50, 40)

# Yildiz ayarlari
YILDIZ_SAYISI = 80
YILDIZ_SPAWN_ARASI = 500  # ms (yeni yildiz ekleme araligi)


def gorsel_yukle(dosya_adi, boyut=None):
    """Gorsel dosyasini yukle, bulunamazsa renkli yedek olustur.

    Args:
        dosya_adi: Yuklenecek gorsel dosyasinin adi.
        boyut: (genislik, yukseklik) demeti. None ise orijinal boyut.

    Returns:
        pygame.Surface: Yuklenen veya olusturulan yuzey.
    """
    try:
        yol = os.path.join("kod_ornekleri", "bolum05", "assets", dosya_adi)
        gorsel = pygame.image.load(yol).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        return gorsel
    except (pygame.error, FileNotFoundError):
        # Yedek gemi gorunumu olustur
        genislik = boyut[0] if boyut else 50
        yukseklik = boyut[1] if boyut else 40
        yuzey = pygame.Surface((genislik, yukseklik), pygame.SRCALPHA)

        # Basit gemi sekli ciz (ucgen govde + kanatlar)
        orta_x = genislik // 2
        # Ana govde (ucgen)
        govde = [
            (orta_x, 2),
            (genislik - 4, yukseklik - 2),
            (4, yukseklik - 2),
        ]
        pygame.draw.polygon(yuzey, ACIK_MAVI, govde)
        pygame.draw.polygon(yuzey, BEYAZ, govde, 2)

        # Kokpit (kucuk daire)
        pygame.draw.circle(yuzey, SARI,
                          (orta_x, yukseklik // 2), 4)
        return yuzey


# --- Sprite Siniflari ---
class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi.

    WASD veya ok tuslari ile dort yonde hareket eder.
    clamp_ip ile ekran sinirlarini asmaz.
    """

    def __init__(self):
        super().__init__()
        self.image = gorsel_yukle("gemi.png", OYUNCU_BOYUT)
        self.rect = self.image.get_rect()
        # Baslangic konumu: ekranin alt ortasi
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.hiz = OYUNCU_HIZ
        # Ekran sinir dikdortgeni (clamp_ip icin)
        self.sinir = pygame.Rect(0, 0, GENISLIK, YUKSEKLIK)

    def update(self):
        """Klavye girdilerine gore hareket et."""
        tuslar = pygame.key.get_pressed()

        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += self.hiz
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            self.rect.y -= self.hiz
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            self.rect.y += self.hiz

        # Ekran sinirlari icinde tut
        self.rect.clamp_ip(self.sinir)


class Yildiz(pygame.sprite.Sprite):
    """Kayan yildiz arka plan etkisi.

    Farkli boyut ve hizlarda asagiya dogru kayar.
    Buyuk yildizlar daha parlak ve hizli (yakin gorunur),
    kucuk yildizlar daha soluk ve yavas (uzak gorunur).
    """

    def __init__(self, ustten_baslat=False):
        """Yildiz olustur.

        Args:
            ustten_baslat: True ise ekranin ust kenarinda baslar.
                          False ise rastgele y konumunda baslar.
        """
        super().__init__()

        # Rastgele boyut belirleme (1, 2 veya 3 piksel yaricap)
        self.boyut = random.randint(1, 3)

        # Boyuta gore renk (parlaklik) ayarla
        if self.boyut == 3:
            self.renk = BEYAZ        # Yakin: parlak beyaz
        elif self.boyut == 2:
            self.renk = GRI          # Orta: gri
        else:
            self.renk = KOYU_GRI     # Uzak: koyu gri

        # Gorsel olustur (kucuk daire)
        cap = self.boyut * 2
        self.image = pygame.Surface((cap, cap), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.renk,
                          (self.boyut, self.boyut), self.boyut)

        # Konum
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - cap)
        if ustten_baslat:
            self.rect.bottom = 0
        else:
            self.rect.y = random.randint(-YUKSEKLIK, YUKSEKLIK)

        # Hiz: boyuta orantili (buyuk = hizli = yakin)
        taban_hiz = self.boyut * 0.8
        self.hiz = taban_hiz + random.uniform(0, 1.5)

    def update(self):
        """Yildizi asagi kaydir, ekranin altindan cikinca ustten sok."""
        self.rect.y += self.hiz

        if self.rect.top > YUKSEKLIK:
            self.rect.x = random.randint(0, GENISLIK)
            self.rect.bottom = 0
            # Her dongude hizi biraz rastgelestir (dogallik)
            taban_hiz = self.boyut * 0.8
            self.hiz = taban_hiz + random.uniform(0, 1.5)


def skor_ciz(ekran, font, skor, yildiz_sayisi):
    """Skor ve bilgi yazilarini ekrana ciz.

    Args:
        ekran: Cizdirme yapilacak yuzey.
        font: Yazi fontu.
        skor: Hayatta kalma suresi (saniye).
        yildiz_sayisi: Aktif yildiz sayisi.
    """
    # Skor (sol ust)
    skor_yazi = font.render(f"Sure: {skor}s", True, SARI)
    ekran.blit(skor_yazi, (15, 15))

    # Yildiz sayisi (sol ust, ikinci satir)
    yildiz_yazi = font.render(f"Yildiz: {yildiz_sayisi}", True, GRI)
    ekran.blit(yildiz_yazi, (15, 42))

    # Kontrol bilgisi (alt orta)
    kontrol = font.render("WASD / Ok Tuslari: Hareket | ESC: Cikis",
                          True, KOYU_GRI)
    kontrol_rect = kontrol.get_rect(centerx=GENISLIK // 2,
                                     bottom=YUKSEKLIK - 8)
    ekran.blit(kontrol, kontrol_rect)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # --- Sprite Gruplari ---
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()

    # --- Yildizlari olustur ---
    for _ in range(YILDIZ_SAYISI):
        yildiz = Yildiz(ustten_baslat=False)
        tum_spritelar.add(yildiz)
        yildizlar.add(yildiz)

    # --- Oyuncuyu olustur ---
    # Oyuncu en son eklenir ki yildizlarin ustunde cizilsin
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # --- Skor ve zamanlama ---
    skor = 0
    baslangic_zamani = pygame.time.get_ticks()
    son_yildiz_zamani = pygame.time.get_ticks()

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

        # --- Yeni yildiz ekleme (spawn) ---
        simdi = pygame.time.get_ticks()
        if simdi - son_yildiz_zamani > YILDIZ_SPAWN_ARASI:
            yeni_yildiz = Yildiz(ustten_baslat=True)
            tum_spritelar.add(yeni_yildiz)
            yildizlar.add(yeni_yildiz)
            son_yildiz_zamani = simdi

            # Cok fazla yildiz birikmesini engelle
            if len(yildizlar) > 150:
                en_eski = yildizlar.sprites()[0]
                en_eski.kill()

        # --- Toplu guncelleme ---
        tum_spritelar.update()

        # --- Skor hesaplama ---
        gecen_ms = simdi - baslangic_zamani
        skor = gecen_ms // 1000

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)

        # Tum Sprite'lari tek satirda ciz
        tum_spritelar.draw(ekran)

        # HUD (skor ve bilgi)
        skor_ciz(ekran, font, skor, len(yildizlar))

        # Ekrani guncelle
        pygame.display.flip()

    # --- Temizlik ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
Koyu mavi uzay arka planinda farkli boyut ve hizlarda
kayan yildizlar gorulur. Buyuk yildizlar parlak beyaz
ve hizli, kucuk yildizlar gri ve yavas hareket eder.

Ekranin alt ortasinda mavi bir uzay gemisi bulunur ve
WASD veya ok tuslari ile dort yonde hareket ettirilebilir.
Gemi ekran sinirlari disina cikamaz (clamp_ip).

Sol ust kosede hayatta kalma suresi (saniye) ve aktif
yildiz sayisi gosterilir. Her 500 ms'de yeni yildiz
eklenir ve toplam 150'yi gecindiginde eski yildizlar
temizlenir.

Ilerleyen bolumlerde (v2) dusman gemileri, mermiler ve
carpisme algilama eklenecektir.
"""
