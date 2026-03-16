"""
Uzay Kacisi v2 - Dusmanlar, Mermiler ve Carpisma Algilama

Bolum 5'teki Uzay Kacisi v1'in devami. Bu versiyonda
dusman gemileri, mermi sistemi, carpisma algilama, can
cubugu ve puan sistemi eklenmistir.

Ogrenilecek kavramlar:
- spritecollide() ile oyuncu-dusman carpismalari
- groupcollide() ile mermi-dusman carpismalari
- Coklu Sprite grubu yonetimi
- Zamanlayici ile dusman uretme (spawn)
- Can cubugu ve skor gosterimi (HUD)
- Oyun bitti ekrani ve yeniden baslama

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 2 - Sprite Carpisma Fonksiyonlari

Calistirma: python v2_carpisma_mermi.py
            uv run v2_carpisma_mermi.py
Gereksinimler: pygame-ce
"""

import pygame
import random
import os
import sys


# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Kacisi v2 - Dusmanlar ve Mermiler"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (220, 50, 50)
YESIL = (50, 200, 50)
SARI = (255, 220, 50)
ACIK_MAVI = (100, 180, 255)
KOYU_MAVI = (8, 8, 32)
GRI = (150, 150, 160)
KOYU_GRI = (80, 80, 90)
TURUNCU = (255, 150, 50)

# Oyuncu ayarlari
OYUNCU_HIZ = 5
OYUNCU_BOYUT = (50, 40)
OYUNCU_CAN = 100

# Dusman ayarlari
DUSMAN_BOYUT = (40, 35)
DUSMAN_SPAWN_MS = 800  # milisaniye

# Mermi ayarlari
MERMI_HIZ = -8
MERMI_BEKLEME = 200  # milisaniye (atesler arasi minimum sure)

# Yildiz ayarlari
YILDIZ_SAYISI = 80


# --- Yardimci Fonksiyonlar ---
def gorsel_yukle(dosya_adi, boyut=None, renk=None):
    """Gorsel dosyasini yukle, bulunamazsa renkli yedek olustur."""
    try:
        yol = os.path.join("assets", "images", dosya_adi)
        gorsel = pygame.image.load(yol).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        return gorsel
    except (pygame.error, FileNotFoundError):
        genislik = boyut[0] if boyut else 50
        yukseklik = boyut[1] if boyut else 40
        yuzey = pygame.Surface(
            (genislik, yukseklik), pygame.SRCALPHA
        )
        kullanilacak_renk = renk if renk else ACIK_MAVI

        # Basit gemi sekli ciz (ucgen)
        orta_x = genislik // 2
        govde = [
            (orta_x, 2),
            (genislik - 4, yukseklik - 2),
            (4, yukseklik - 2),
        ]
        pygame.draw.polygon(yuzey, kullanilacak_renk, govde)
        pygame.draw.polygon(yuzey, BEYAZ, govde, 2)
        pygame.draw.circle(
            yuzey, SARI, (orta_x, yukseklik // 2), 4
        )
        return yuzey


# --- Sprite Siniflari ---
class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi.

    WASD veya ok tuslari ile dort yonde hareket eder.
    Space tusu ile mermi atesler. Can sistemi vardir.
    """

    def __init__(self):
        super().__init__()
        self.image = gorsel_yukle("gemi.png", OYUNCU_BOYUT)
        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.hiz = OYUNCU_HIZ
        self.can = OYUNCU_CAN
        self.sinir = pygame.Rect(0, 0, GENISLIK, YUKSEKLIK)
        self.son_ates_zamani = 0

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
        self.rect.clamp_ip(self.sinir)

    def ates_edebilir_mi(self):
        """Mermi bekleme suresi gecti mi kontrol et."""
        simdi = pygame.time.get_ticks()
        if simdi - self.son_ates_zamani > MERMI_BEKLEME:
            self.son_ates_zamani = simdi
            return True
        return False


class Dusman(pygame.sprite.Sprite):
    """Yukaridan asagi inen dusman gemisi."""

    def __init__(self):
        super().__init__()
        self.image = gorsel_yukle(
            "dusman.png", DUSMAN_BOYUT, renk=KIRMIZI
        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(
            0, GENISLIK - self.rect.width
        )
        self.rect.bottom = 0
        self.hiz = random.uniform(2, 5)
        self.puan = 10

    def update(self):
        """Asagi dogru hareket et."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


class Mermi(pygame.sprite.Sprite):
    """Yukari dogru hareket eden oyuncu mermisi."""

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


class Yildiz(pygame.sprite.Sprite):
    """Kayan yildiz arka plan etkisi (v1'den devam)."""

    def __init__(self, ustten_baslat=False):
        super().__init__()
        self.boyut = random.randint(1, 3)
        if self.boyut == 3:
            self.renk = BEYAZ
        elif self.boyut == 2:
            self.renk = GRI
        else:
            self.renk = KOYU_GRI

        cap = self.boyut * 2
        self.image = pygame.Surface((cap, cap), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, self.renk,
            (self.boyut, self.boyut), self.boyut
        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - cap)
        if ustten_baslat:
            self.rect.bottom = 0
        else:
            self.rect.y = random.randint(-YUKSEKLIK, YUKSEKLIK)
        taban_hiz = self.boyut * 0.8
        self.hiz = taban_hiz + random.uniform(0, 1.5)

    def update(self):
        """Asagi kaydir."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.rect.x = random.randint(0, GENISLIK)
            self.rect.bottom = 0
            taban_hiz = self.boyut * 0.8
            self.hiz = taban_hiz + random.uniform(0, 1.5)


# --- HUD Fonksiyonlari ---
def hud_ciz(ekran, font, skor, can, dusman_sayisi):
    """Skor, can cubugu ve bilgileri ekrana ciz."""
    # Skor (sol ust)
    skor_yazi = font.render(f"Skor: {skor}", True, SARI)
    ekran.blit(skor_yazi, (15, 15))

    # Dusman sayisi (sol ust, ikinci satir)
    dusman_yazi = font.render(
        f"Dusman: {dusman_sayisi}", True, GRI
    )
    ekran.blit(dusman_yazi, (15, 45))

    # Can cubugu (sag ust)
    cubuk_x = GENISLIK - 215
    cubuk_y = 15
    cubuk_gen = 200
    cubuk_yuk = 20
    doluluk = max(0, can / OYUNCU_CAN) * cubuk_gen

    # Arka plan (kirmizi)
    pygame.draw.rect(
        ekran, KIRMIZI,
        (cubuk_x, cubuk_y, cubuk_gen, cubuk_yuk)
    )
    # Dolu kisim (yesil -> turuncu -> kirmizi)
    if can > 60:
        renk = YESIL
    elif can > 30:
        renk = TURUNCU
    else:
        renk = KIRMIZI
    pygame.draw.rect(
        ekran, renk,
        (cubuk_x, cubuk_y, doluluk, cubuk_yuk)
    )
    # Cerceve
    pygame.draw.rect(
        ekran, BEYAZ,
        (cubuk_x, cubuk_y, cubuk_gen, cubuk_yuk), 2
    )
    # Can yazisi
    can_yazi = font.render(f"Can: {can}", True, BEYAZ)
    ekran.blit(can_yazi, (cubuk_x, cubuk_y + 22))

    # Kontrol bilgisi (alt orta)
    kontrol = font.render(
        "WASD: Hareket | Space: Ates | ESC: Cikis", True, KOYU_GRI
    )
    kontrol_rect = kontrol.get_rect(
        centerx=GENISLIK // 2, bottom=YUKSEKLIK - 8
    )
    ekran.blit(kontrol, kontrol_rect)


def oyun_bitti_ciz(ekran, font_buyuk, font, skor):
    """Oyun bitti ekranini ciz."""
    # Yari seffaf siyah overlay
    overlay = pygame.Surface((GENISLIK, YUKSEKLIK))
    overlay.fill(SIYAH)
    overlay.set_alpha(180)
    ekran.blit(overlay, (0, 0))

    # GAME OVER yazisi
    go_yazi = font_buyuk.render("GAME OVER", True, KIRMIZI)
    go_rect = go_yazi.get_rect(
        center=(GENISLIK // 2, YUKSEKLIK // 2 - 30)
    )
    ekran.blit(go_yazi, go_rect)

    # Skor yazisi
    skor_yazi = font.render(f"Final Skor: {skor}", True, SARI)
    skor_rect = skor_yazi.get_rect(
        center=(GENISLIK // 2, YUKSEKLIK // 2 + 20)
    )
    ekran.blit(skor_yazi, skor_rect)

    # Devam yazisi
    devam_yazi = font.render(
        "ESC: Cikis | R: Tekrar Oyna", True, GRI
    )
    devam_rect = devam_yazi.get_rect(
        center=(GENISLIK // 2, YUKSEKLIK // 2 + 60)
    )
    ekran.blit(devam_yazi, devam_rect)


def oyunu_baslat():
    """Oyun durumunu sifirla ve gerekli nesneleri olustur."""
    # Sprite Gruplari
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()

    # Yildizlari olustur
    for _ in range(YILDIZ_SAYISI):
        yildiz = Yildiz(ustten_baslat=False)
        tum_spritelar.add(yildiz)
        yildizlar.add(yildiz)

    # Oyuncuyu olustur (yildizlarin ustunde cizilmesi icin
    # en son ekliyoruz)
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    return (tum_spritelar, yildizlar, dusmanlar,
            mermiler, oyuncu)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    font_buyuk = pygame.font.Font(None, 72)

    # Dusman spawn zamanlayicisi
    DUSMAN_OLAY = pygame.USEREVENT + 1
    pygame.time.set_timer(DUSMAN_OLAY, DUSMAN_SPAWN_MS)

    # Oyunu baslat
    (tum_spritelar, yildizlar, dusmanlar,
     mermiler, oyuncu) = oyunu_baslat()
    skor = 0
    oyun_aktif = True

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

                # Oyun aktifken Space ile ates
                elif (olay.key == pygame.K_SPACE
                      and oyun_aktif):
                    if oyuncu.ates_edebilir_mi():
                        mermi = Mermi(
                            oyuncu.rect.centerx,
                            oyuncu.rect.top
                        )
                        tum_spritelar.add(mermi)
                        mermiler.add(mermi)

                # Oyun bittiyse R ile tekrar baslat
                elif (olay.key == pygame.K_r
                      and not oyun_aktif):
                    (tum_spritelar, yildizlar, dusmanlar,
                     mermiler, oyuncu) = oyunu_baslat()
                    skor = 0
                    oyun_aktif = True

            # Dusman spawn olayi
            elif olay.type == DUSMAN_OLAY and oyun_aktif:
                dusman = Dusman()
                tum_spritelar.add(dusman)
                dusmanlar.add(dusman)

        # --- Oyun aktifken guncelleme ---
        if oyun_aktif:
            tum_spritelar.update()

            # --- Carpisma kontrolleri ---

            # 1. Mermi-dusman carpismalari (groupcollide)
            carpismalar = pygame.sprite.groupcollide(
                mermiler, dusmanlar, True, True
            )
            for mermi, vurulan in carpismalar.items():
                for dusman in vurulan:
                    skor += dusman.puan

            # 2. Oyuncu-dusman carpismalari (spritecollide)
            if oyuncu.alive():
                vurulan_dusmanlar = pygame.sprite.spritecollide(
                    oyuncu, dusmanlar, True
                )
                for dusman in vurulan_dusmanlar:
                    oyuncu.can -= 25
                    if oyuncu.can <= 0:
                        oyuncu.can = 0
                        oyuncu.kill()
                        oyun_aktif = False
        else:
            # Oyun bittiyse sadece yildizlari guncelle
            yildizlar.update()

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        # HUD
        hud_ciz(ekran, font, skor, oyuncu.can,
                len(dusmanlar))

        # Oyun bittiyse overlay
        if not oyun_aktif:
            oyun_bitti_ciz(ekran, font_buyuk, font, skor)

        pygame.display.flip()

    # --- Temizlik ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
Koyu mavi uzay arka planinda kayan yildizlar gorulur.
Ekranin altinda mavi oyuncu gemisi WASD/ok tuslari ile
hareket ettirilir.

Yukaridan kirmizi dusman gemileri gelir (her 800 ms'de bir).
Space tusuna basinca sari mermiler yukari firlar.

Carpisma algilama:
- Mermi dusmana isabet edince: ikisi de yok olur, +10 puan
- Dusman oyuncuya carparsa: dusman yok olur, -25 can

Can sifira dusunce "GAME OVER" ekrani cikar.
R tusu ile oyun yeniden baslatilabilir.

Sag ustte can cubugu (yesil->turuncu->kirmizi),
sol ustte skor ve dusman sayisi gosterilir.
"""
