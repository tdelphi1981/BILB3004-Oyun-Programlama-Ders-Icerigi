"""
Uzay Savaşçısı - Adım 6: Tam Oyun

Game Over ekranı, yeniden başlatma, zorluk artışı ve
en yüksek skor takibi ile tam bir oyun deneyimi sunar.
Zaman geçtikçe düşmanlar daha sık ve hızlı gelir.

Öğrenilecek kavramlar:
- Oyun durumu yönetimi (aktif / bitti)
- Yarı saydam overlay Surface oluşturma
- oyunu_sifirla() ile temiz yeniden başlatma
- Zamanla artan zorluk (dinamik spawn aralığı)
- En yüksek skor takibi (oturum içi)

Bölüm: 05 - Görseller ve Sprite Temelleri
Lab: 05 - Bonus: Uzay Savaşçısı (Adım 6/7)

Çalıştırma: uv run python adim6_tam_oyun.py
Gereksinimler: pygame

Kontroller:
- WASD / Ok tuşları: Hareket
- SPACE: Ateş
- R: Yeniden başla (Game Over sonrası)
- ESC: Çıkış
"""

import pygame
import random
import os
import sys

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Savaşçısı - Adım 6"

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
DUSMAN_SPAWN_BASLANGIC = 1000  # ms (başlangıç aralığı)
DUSMAN_SPAWN_MIN = 300         # ms (minimum aralık)
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

    def __init__(self, hiz_carpani=1.0):
        """Düşman oluştur.

        Args:
            hiz_carpani: Hızı artırmak için çarpan (zorluk için).
        """
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
        self.hiz = random.uniform(min_hiz, max_hiz) * hiz_carpani

    def update(self):
        """Düşmanı aşağı hareket ettir."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


def oyunu_sifirla():
    """Oyun durumunu başlangıç değerlerine döndür.

    Returns:
        Yeni sprite grupları ve oyuncu içeren demet.
    """
    tum_spritelar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()

    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    skor = 0
    oyun_bitti = False
    baslangic_zamani = pygame.time.get_ticks()
    son_dusman_zamani = pygame.time.get_ticks()

    return (tum_spritelar, mermiler, dusmanlar, oyuncu,
            skor, oyun_bitti, baslangic_zamani, son_dusman_zamani)


def hud_ciz(ekran, font, skor, can, en_yuksek):
    """Skor, can ve en yüksek skor bilgisini çiz."""
    # Skor (sol üst)
    skor_yazi = font.render(f"Skor: {skor}", True, SARI)
    ekran.blit(skor_yazi, (15, 15))

    # En yüksek skor (sol üst, ikinci satır)
    ey_yazi = font.render(f"En Yüksek: {en_yuksek}", True, GRI)
    ekran.blit(ey_yazi, (15, 42))

    # Can (sağ üst)
    can_yazi = font.render(f"Can: {can}", True, YESIL)
    can_rect = can_yazi.get_rect(right=GENISLIK - 15, top=15)
    ekran.blit(can_yazi, can_rect)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    buyuk_font = pygame.font.Font(None, 64)

    # Arka plan
    arkaplan = arkaplan_olustur()
    arkaplan_y = 0

    # En yüksek skor (oturum içi)
    en_yuksek_skor = 0

    # Oyunu başlat
    (tum_spritelar, mermiler, dusmanlar, oyuncu,
     skor, oyun_bitti, baslangic_zamani, son_dusman_zamani) = oyunu_sifirla()

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

                if oyun_bitti:
                    if olay.key == pygame.K_r:
                        (tum_spritelar, mermiler, dusmanlar, oyuncu,
                         skor, oyun_bitti, baslangic_zamani,
                         son_dusman_zamani) = oyunu_sifirla()
                    continue

                if olay.key == pygame.K_SPACE:
                    oyuncu.ates_et(mermiler, tum_spritelar)

        # --- Güncelle ---
        if not oyun_bitti:
            arkaplan_y += 1
            if arkaplan_y >= YUKSEKLIK:
                arkaplan_y = 0

            simdi = pygame.time.get_ticks()

            # Zorluk hesapla: geçen süre ile spawn aralığı kısalır
            gecen_sure = (simdi - baslangic_zamani) / 1000  # saniye
            # Her 10 saniyede 50ms azalt, minimum DUSMAN_SPAWN_MIN
            spawn_arasi = max(
                DUSMAN_SPAWN_MIN,
                DUSMAN_SPAWN_BASLANGIC - int(gecen_sure / 10) * 50
            )
            # Hız çarpanı: her 15 saniyede %10 artış
            hiz_carpani = 1.0 + (gecen_sure / 15) * 0.1

            # Düşman spawn
            if simdi - son_dusman_zamani >= spawn_arasi:
                dusman = Dusman(hiz_carpani)
                dusmanlar.add(dusman)
                tum_spritelar.add(dusman)
                son_dusman_zamani = simdi

            tum_spritelar.update()

            # Çarpışmalar
            vurulanlar = pygame.sprite.groupcollide(
                mermiler, dusmanlar, True, True
            )
            for mermi, dusman_listesi in vurulanlar.items():
                skor += DUSMAN_PUAN * len(dusman_listesi)

            carpanlar = pygame.sprite.spritecollide(
                oyuncu, dusmanlar, True
            )
            if carpanlar:
                oyuncu.can -= len(carpanlar)
                if oyuncu.can <= 0:
                    oyuncu.can = 0
                    oyun_bitti = True
                    # En yüksek skoru güncelle
                    if skor > en_yuksek_skor:
                        en_yuksek_skor = skor

        # --- Çizim ---
        ekran.blit(arkaplan, (0, arkaplan_y - YUKSEKLIK))
        ekran.blit(arkaplan, (0, arkaplan_y))

        tum_spritelar.draw(ekran)

        # HUD
        hud_ciz(ekran, font, skor, oyuncu.can, en_yuksek_skor)

        # Game Over ekranı
        if oyun_bitti:
            # Yarı saydam siyah katman
            katman = pygame.Surface((GENISLIK, YUKSEKLIK))
            katman.set_alpha(150)
            katman.fill(SIYAH)
            ekran.blit(katman, (0, 0))

            # OYUN BİTTİ yazısı
            go_yazi = buyuk_font.render("OYUN BİTTİ", True, KIRMIZI)
            go_rect = go_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 - 30)
            )
            ekran.blit(go_yazi, go_rect)

            # Skor bilgisi
            skor_bilgi = font.render(
                f"Skor: {skor} | En Yüksek: {en_yuksek_skor}",
                True, BEYAZ
            )
            skor_rect = skor_bilgi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 + 15)
            )
            ekran.blit(skor_bilgi, skor_rect)

            # Yeniden başlatma bilgisi
            tekrar_yazi = font.render(
                "R: Tekrar | ESC: Çıkış", True, GRI
            )
            tekrar_rect = tekrar_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 + 50)
            )
            ekran.blit(tekrar_yazi, tekrar_rect)

        # Kontrol bilgisi (oyun aktifken)
        if not oyun_bitti:
            kontrol = font.render(
                "WASD: Hareket | SPACE: Ateş | ESC: Çıkış",
                True, KOYU_GRI
            )
            kontrol_rect = kontrol.get_rect(
                centerx=GENISLIK // 2, bottom=YUKSEKLIK - 8
            )
            ekran.blit(kontrol, kontrol_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

"""
BEKLENEN ÇIKTI:
---------------
800x600 piksel kayan uzay arka planlı tam bir uzay savaşı
oyunu açılır.

Oyun mekanikleri:
- WASD/Ok tuşları ile hareket, SPACE ile ateş
- Düşmanlar üstten gelir, mermilerle vurulabilir (+100 puan)
- Düşmana temas edince 1 can kaybı (toplam 3 can)
- Zaman geçtikçe düşmanlar daha sık ve hızlı gelir

Can 0 olunca:
- Yarı saydam siyah overlay belirir
- "OYUN BİTTİ" yazısı, skor ve en yüksek skor gösterilir
- R tuşuna basarak yeniden başla
- En yüksek skor oturum boyunca takip edilir

Sol üst: Skor ve en yüksek skor
Sağ üst: Can bilgisi
ESC ile program kapanır.
"""
