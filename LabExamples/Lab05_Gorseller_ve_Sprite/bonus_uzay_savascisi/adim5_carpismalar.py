"""
Uzay Savaşçısı - Adım 5: Çarpışmalar ve Skor

Mermi-düşman ve düşman-oyuncu çarpışması ekler.
Her vurulan düşman puan kazandırır, düşmanla
temas eden oyuncu can kaybeder.

Öğrenilecek kavramlar:
- pygame.sprite.groupcollide() ile grup çarpışmaları
- pygame.sprite.spritecollide() ile tekli çarpışmalar
- Skor ve can sistemi
- pygame.font ile HUD (başlık ekranı) gösterimi
- Oyun durumu yönetimi (can = 0 -> oyun durur)

Bölüm: 05 - Görseller ve Sprite Temelleri
Lab: 05 - Bonus: Uzay Savaşçısı (Adım 5/7)

Çalıştırma: uv run python adim5_carpismalar.py
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
BASLIK = "Uzay Savaşçısı - Adım 5"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (8, 8, 32)
ACIK_MAVI = (100, 180, 255)
SARI = (255, 220, 50)
GRI = (150, 150, 160)
KOYU_GRI = (80, 80, 90)
KIRMIZI = (220, 50, 50)
KOYU_KIRMIZI = (150, 30, 30)
YESIL = (50, 220, 50)

# Oyuncu ayarları
OYUNCU_HIZ = 5
OYUNCU_BOYUT = (50, 40)
OYUNCU_CAN = 3

# Mermi ayarları
MERMI_HIZ = 8
MERMI_BOYUT = (9, 37)
MERMI_BEKLEME = 250

# Düşman ayarları
DUSMAN_SPAWN_ARASI = 1000
DUSMAN_PUAN = 100
DUSMAN_TIPLERI = [
    {"dosya": "PNG/Enemies/enemyRed1.png", "boyut": (40, 30), "hiz": (2, 4)},
    {"dosya": "PNG/Enemies/enemyRed2.png", "boyut": (50, 35), "hiz": (1, 3)},
    {"dosya": "PNG/Enemies/enemyRed3.png", "boyut": (60, 40), "hiz": (1, 2)},
]

# Asset dizini
ASSET_DIZIN = os.path.join(
    os.path.dirname(__file__), "..", "assets", "kenney_space-shooter-redux"
)


def gorsel_yukle(dosya_adi, boyut=None):
    """Görsel dosyasını yükle, bulunamazsa None döndür."""
    try:
        yol = os.path.join(ASSET_DIZIN, dosya_adi)
        gorsel = pygame.image.load(yol).convert_alpha()
        if boyut:
            gorsel = pygame.transform.smoothscale(gorsel, boyut)
        gorsel.set_colorkey(SIYAH)
        return gorsel
    except (pygame.error, FileNotFoundError):
        return None


def arkaplan_olustur():
    """Döşemeli arka plan Surface'i oluştur."""
    arkaplan = pygame.Surface((GENISLIK, YUKSEKLIK * 2))
    gorsel = gorsel_yukle("Backgrounds/darkPurple.png")

    if gorsel:
        g_gen = gorsel.get_width()
        g_yuk = gorsel.get_height()
        for x in range(0, GENISLIK, g_gen):
            for y in range(0, YUKSEKLIK * 2, g_yuk):
                arkaplan.blit(gorsel, (x, y))
    else:
        arkaplan.fill(KOYU_MAVI)
        for _ in range(200):
            x = random.randint(0, GENISLIK - 1)
            y = random.randint(0, YUKSEKLIK * 2 - 1)
            boyut = random.randint(1, 3)
            if boyut == 3:
                renk = BEYAZ
            elif boyut == 2:
                renk = GRI
            else:
                renk = KOYU_GRI
            pygame.draw.circle(arkaplan, renk, (x, y), boyut)

    return arkaplan


# --- Sprite Sınıfları ---

class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi."""

    def __init__(self):
        super().__init__()
        gorsel = gorsel_yukle("PNG/playerShip1_blue.png", OYUNCU_BOYUT)
        if gorsel:
            self.image = gorsel
        else:
            self.image = pygame.Surface(OYUNCU_BOYUT, pygame.SRCALPHA)
            orta_x = OYUNCU_BOYUT[0] // 2
            govde = [
                (orta_x, 2),
                (OYUNCU_BOYUT[0] - 4, OYUNCU_BOYUT[1] - 2),
                (4, OYUNCU_BOYUT[1] - 2),
            ]
            pygame.draw.polygon(self.image, ACIK_MAVI, govde)
            pygame.draw.polygon(self.image, BEYAZ, govde, 2)
            pygame.draw.circle(self.image, SARI,
                              (orta_x, OYUNCU_BOYUT[1] // 2), 4)

        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.hiz = OYUNCU_HIZ
        self.sinir = pygame.Rect(0, 0, GENISLIK, YUKSEKLIK)
        self.son_ates = 0
        self.can = OYUNCU_CAN

    def update(self):
        """Klavye girdilerine göre hareket et."""
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

    def ates_et(self, mermi_grubu, tum_grup):
        """Cooldown süresi dolduysa mermi oluştur."""
        simdi = pygame.time.get_ticks()
        if simdi - self.son_ates >= MERMI_BEKLEME:
            mermi = Mermi(self.rect.centerx, self.rect.top)
            mermi_grubu.add(mermi)
            tum_grup.add(mermi)
            self.son_ates = simdi


class Mermi(pygame.sprite.Sprite):
    """Oyuncu mermisi."""

    def __init__(self, x, y):
        super().__init__()
        gorsel = gorsel_yukle("PNG/Lasers/laserBlue01.png", MERMI_BOYUT)
        if gorsel:
            self.image = gorsel
        else:
            self.image = pygame.Surface(MERMI_BOYUT, pygame.SRCALPHA)
            pygame.draw.rect(self.image, SARI, (2, 0, 5, 37))
            pygame.draw.rect(self.image, BEYAZ, (3, 0, 3, 10))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.hiz = MERMI_HIZ

    def update(self):
        """Mermiyi yukarı hareket ettir."""
        self.rect.y -= self.hiz
        if self.rect.bottom < 0:
            self.kill()


class Dusman(pygame.sprite.Sprite):
    """Düşman uzay gemisi."""

    def __init__(self):
        super().__init__()
        tip = random.choice(DUSMAN_TIPLERI)

        gorsel = gorsel_yukle(tip["dosya"], tip["boyut"])
        if gorsel:
            self.image = gorsel
        else:
            self.image = pygame.Surface(tip["boyut"], pygame.SRCALPHA)
            pygame.draw.rect(
                self.image, KIRMIZI,
                (0, 0, tip["boyut"][0], tip["boyut"][1]),
                border_radius=4
            )
            pygame.draw.rect(
                self.image, KOYU_KIRMIZI,
                (3, 3, tip["boyut"][0] - 6, tip["boyut"][1] - 6),
                border_radius=3
            )

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - self.rect.width)
        self.rect.bottom = 0

        min_hiz, max_hiz = tip["hiz"]
        self.hiz = random.uniform(min_hiz, max_hiz)

    def update(self):
        """Düşmanı aşağı hareket ettir."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


def hud_ciz(ekran, font, skor, can):
    """Skor ve can bilgisini ekrana çiz.

    Args:
        ekran: Çizdirme yapılacak yüzey.
        font: Yazı fontu.
        skor: Oyuncu skoru.
        can: Kalan can sayısı.
    """
    # Skor (sol üst)
    skor_yazi = font.render(f"Skor: {skor}", True, SARI)
    ekran.blit(skor_yazi, (15, 15))

    # Can (sağ üst)
    can_yazi = font.render(f"Can: {can}", True, YESIL)
    can_rect = can_yazi.get_rect(right=GENISLIK - 15, top=15)
    ekran.blit(can_yazi, can_rect)

    # Kontrol bilgisi (alt orta)
    kontrol = font.render(
        "WASD: Hareket | SPACE: Ateş | ESC: Çıkış",
        True, KOYU_GRI
    )
    kontrol_rect = kontrol.get_rect(
        centerx=GENISLIK // 2, bottom=YUKSEKLIK - 8
    )
    ekran.blit(kontrol, kontrol_rect)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # Arka plan
    arkaplan = arkaplan_olustur()
    arkaplan_y = 0

    # --- Sprite Grupları ---
    tum_spritelar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()

    # --- Oyuncuyu oluştur ---
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # --- Oyun durumu ---
    skor = 0
    oyun_bitti = False
    son_dusman_zamani = pygame.time.get_ticks()

    # --- Ana Oyun Döngüsü ---
    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olay işleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_SPACE and not oyun_bitti:
                    oyuncu.ates_et(mermiler, tum_spritelar)

        # --- Güncelle ---
        if not oyun_bitti:
            arkaplan_y += 1
            if arkaplan_y >= YUKSEKLIK:
                arkaplan_y = 0

            # Düşman spawn
            simdi = pygame.time.get_ticks()
            if simdi - son_dusman_zamani >= DUSMAN_SPAWN_ARASI:
                dusman = Dusman()
                dusmanlar.add(dusman)
                tum_spritelar.add(dusman)
                son_dusman_zamani = simdi

            tum_spritelar.update()

            # --- Çarpışmalar ---

            # Mermi - Düşman çarpışmaları
            # Her iki grup da True: hem mermi hem düşman silinir
            vurulanlar = pygame.sprite.groupcollide(
                mermiler, dusmanlar, True, True
            )
            for mermi, dusman_listesi in vurulanlar.items():
                skor += DUSMAN_PUAN * len(dusman_listesi)

            # Düşman - Oyuncu çarpışmaları
            # Düşman silinir (True), oyuncu silinmez (elle yönetilir)
            carpanlar = pygame.sprite.spritecollide(
                oyuncu, dusmanlar, True
            )
            if carpanlar:
                oyuncu.can -= len(carpanlar)
                if oyuncu.can <= 0:
                    oyuncu.can = 0
                    oyun_bitti = True

        # --- Çizim ---
        ekran.blit(arkaplan, (0, arkaplan_y - YUKSEKLIK))
        ekran.blit(arkaplan, (0, arkaplan_y))

        tum_spritelar.draw(ekran)

        # HUD
        hud_ciz(ekran, font, skor, oyuncu.can)

        # Oyun bitti mesajı
        if oyun_bitti:
            buyuk_font = pygame.font.Font(None, 64)
            go_yazi = buyuk_font.render("OYUN BİTTİ", True, KIRMIZI)
            go_rect = go_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2)
            )
            ekran.blit(go_yazi, go_rect)

            skor_yazi = font.render(
                f"Final Skor: {skor}", True, BEYAZ
            )
            skor_rect = skor_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 + 40)
            )
            ekran.blit(skor_yazi, skor_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

"""
BEKLENEN ÇIKTI:
---------------
800x600 piksel kayan uzay arka planlı pencere açılır.
Mavi oyuncu gemisi ve üstten gelen kırmızı düşmanlar görülür.

SPACE ile atılan mermiler düşmanlara isabet ederse:
- Hem mermi hem düşman yok olur
- Skor 100 puan artar

Düşman gemisi oyuncuya çarparsa:
- Düşman yok olur
- Oyuncunun canı 1 azalır

Can 0 olunca ekranın ortasında "OYUN BİTTİ" yazar
ve final skor gösterilir.

Sol üst: Skor, sağ üst: Can bilgisi.
ESC ile program kapanır.
"""
