"""
Uzay Kacisi v2 - Adim 6: Game Over + Polish

Oyun bitis durumu ekliyoruz. Can sifira dusunce oyun durur,
yari saydam siyah overlay gosterilir ve Game Over ekrani cikar.
R tusu ile oyun basarilan sifirlanir.

Ogrenilecek kavramlar:
- Oyun durumu yonetimi (oyun_aktif flag)
- Yari saydam overlay cizimi (Surface + alpha)
- Oyunu sifirlama (restart) mantigi
- Kullanici deneyimi iyilestirmeleri

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Uzay Kacisi v2 (Adim 6/7)

Calistirma: uv run python adim6_tam_oyun.py
Gereksinimler: pygame

Kontroller:
- WASD / Ok tuslari: Hareket
- Space: Ates
- R: Tekrar basla (Game Over ekraninda)
- ESC: Cikis
"""

import pygame
import random
import sys

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60

# --- Renkler ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (10, 10, 40)
ACIK_MAVI = (100, 150, 255)
MAVI = (50, 100, 200)
KIRMIZI = (220, 50, 50)
KOYU_KIRMIZI = (150, 30, 30)
SARI = (255, 255, 0)
YESIL = (50, 200, 50)
TURUNCU = (255, 165, 0)
GUMI = (200, 200, 220)
KOYU_GRI = (40, 40, 50)

# --- Oyuncu ---
OYUNCU_HIZ = 5
OYUNCU_CAN = 100
DUSMAN_HASAR = 25

# --- Mermi ---
MERMI_HIZ = 8
MERMI_COOLDOWN = 250

# --- Dusman ---
DUSMAN_OLAY = pygame.USEREVENT + 1
DUSMAN_ARALIK = 800
DUSMAN_PUAN = 10


class Yildiz(pygame.sprite.Sprite):
    """Parallax kayan yildiz."""

    def __init__(self):
        super().__init__()
        self.katman = random.choice([1, 2, 3])

        if self.katman == 1:
            self.boyut = 1
            self.hiz = random.uniform(0.5, 1.0)
            self.renk = (100, 100, 120)
        elif self.katman == 2:
            self.boyut = 2
            self.hiz = random.uniform(1.5, 2.5)
            self.renk = (180, 180, 200)
        else:
            self.boyut = 3
            self.hiz = random.uniform(3.0, 4.5)
            self.renk = BEYAZ

        self.image = pygame.Surface((self.boyut, self.boyut))
        self.image.fill(self.renk)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK)
        self.rect.y = random.randint(0, YUKSEKLIK)
        self.y_float = float(self.rect.y)

    def update(self):
        self.y_float += self.hiz
        self.rect.y = int(self.y_float)
        if self.rect.top > YUKSEKLIK:
            self.rect.x = random.randint(0, GENISLIK)
            self.rect.y = -self.boyut
            self.y_float = float(self.rect.y)


class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi."""

    def __init__(self):
        super().__init__()
        self.genislik = 40
        self.yukseklik = 50
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        self._gemi_ciz()
        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.son_atis_zamani = 0
        self.can = OYUNCU_CAN

    def _gemi_ciz(self):
        noktalar = [
            (self.genislik // 2, 0),
            (0, self.yukseklik),
            (self.genislik, self.yukseklik),
        ]
        pygame.draw.polygon(self.image, ACIK_MAVI, noktalar)
        ic_noktalar = [
            (self.genislik // 2, 10),
            (8, self.yukseklik - 5),
            (self.genislik - 8, self.yukseklik - 5),
        ]
        pygame.draw.polygon(self.image, MAVI, ic_noktalar)
        alev_noktalar = [
            (self.genislik // 2 - 6, self.yukseklik),
            (self.genislik // 2, self.yukseklik - 8),
            (self.genislik // 2 + 6, self.yukseklik),
        ]
        pygame.draw.polygon(self.image, SARI, alev_noktalar)

    def update(self):
        tuslar = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            dx = -OYUNCU_HIZ
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            dx = OYUNCU_HIZ
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            dy = -OYUNCU_HIZ
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            dy = OYUNCU_HIZ

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > YUKSEKLIK:
            self.rect.bottom = YUKSEKLIK

    def ates_edebilir_mi(self):
        simdi = pygame.time.get_ticks()
        if simdi - self.son_atis_zamani >= MERMI_COOLDOWN:
            self.son_atis_zamani = simdi
            return True
        return False

    def hasar_al(self, miktar):
        self.can -= miktar
        if self.can < 0:
            self.can = 0


class Dusman(pygame.sprite.Sprite):
    """Dusman gemisi."""

    def __init__(self):
        super().__init__()
        self.genislik = 35
        self.yukseklik = 30
        self.hiz = random.uniform(2, 5)
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        self._gemi_ciz()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - self.genislik)
        self.rect.y = -self.yukseklik
        self.y_float = float(self.rect.y)

    def _gemi_ciz(self):
        noktalar = [
            (0, 0),
            (self.genislik, 0),
            (self.genislik // 2, self.yukseklik),
        ]
        pygame.draw.polygon(self.image, KIRMIZI, noktalar)
        ic_noktalar = [
            (6, 4),
            (self.genislik - 6, 4),
            (self.genislik // 2, self.yukseklik - 6),
        ]
        pygame.draw.polygon(self.image, KOYU_KIRMIZI, ic_noktalar)

    def update(self):
        self.y_float += self.hiz
        self.rect.y = int(self.y_float)
        if self.rect.top > YUKSEKLIK:
            self.kill()


class Mermi(pygame.sprite.Sprite):
    """Oyuncu mermisi."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(SARI)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= MERMI_HIZ
        if self.rect.bottom < 0:
            self.kill()


def hud_ciz(ekran, font, skor, oyuncu, dusmanlar):
    """HUD ciz: skor, dusman sayisi, can cubugu, kontrol bilgisi."""
    # Sol ust: Skor
    skor_metin = font.render(f"Skor: {skor}", True, SARI)
    ekran.blit(skor_metin, (10, 10))

    # Sol ust ikinci satir: Dusman sayisi
    dusman_metin = font.render(
        f"Dusmanlar: {len(dusmanlar)}", True, KIRMIZI
    )
    ekran.blit(dusman_metin, (10, 36))

    # Sag ust: Can cubugu
    cubuk_genislik = 200
    cubuk_yukseklik = 20
    cubuk_x = GENISLIK - cubuk_genislik - 10
    cubuk_y = 10

    can_yuzde = oyuncu.can / OYUNCU_CAN

    if can_yuzde > 0.6:
        cubuk_renk = YESIL
    elif can_yuzde > 0.3:
        cubuk_renk = TURUNCU
    else:
        cubuk_renk = KIRMIZI

    pygame.draw.rect(
        ekran, KOYU_GRI,
        (cubuk_x, cubuk_y, cubuk_genislik, cubuk_yukseklik)
    )
    dolu_genislik = int(cubuk_genislik * can_yuzde)
    if dolu_genislik > 0:
        pygame.draw.rect(
            ekran, cubuk_renk,
            (cubuk_x, cubuk_y, dolu_genislik, cubuk_yukseklik)
        )
    pygame.draw.rect(
        ekran, BEYAZ,
        (cubuk_x, cubuk_y, cubuk_genislik, cubuk_yukseklik), 2
    )

    can_metin = font.render(f"Can: {oyuncu.can}/{OYUNCU_CAN}", True, BEYAZ)
    can_rect = can_metin.get_rect()
    can_rect.right = GENISLIK - 10
    can_rect.top = cubuk_y + cubuk_yukseklik + 4
    ekran.blit(can_metin, can_rect)

    # Alt: Kontrol bilgisi
    kontrol_metin = font.render(
        "WASD: Hareket | Space: Ates | ESC: Cikis", True, GUMI
    )
    ekran.blit(kontrol_metin, (10, YUKSEKLIK - 30))


def game_over_ciz(ekran, skor):
    """Game Over ekranini ciz."""
    # Yari saydam siyah overlay
    overlay = pygame.Surface((GENISLIK, YUKSEKLIK))
    overlay.set_alpha(160)
    overlay.fill(SIYAH)
    ekran.blit(overlay, (0, 0))

    # "GAME OVER" metni
    buyuk_font = pygame.font.SysFont(None, 80)
    orta_font = pygame.font.SysFont(None, 40)
    kucuk_font = pygame.font.SysFont(None, 30)

    go_metin = buyuk_font.render("GAME OVER", True, KIRMIZI)
    go_rect = go_metin.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 - 50))
    ekran.blit(go_metin, go_rect)

    # Skor metni
    skor_metin = orta_font.render(f"Skor: {skor}", True, SARI)
    skor_rect = skor_metin.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 10))
    ekran.blit(skor_metin, skor_rect)

    # Tekrar / Cikis bilgisi
    bilgi_metin = kucuk_font.render(
        "R: Tekrar | ESC: Cikis", True, GUMI
    )
    bilgi_rect = bilgi_metin.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 60))
    ekran.blit(bilgi_metin, bilgi_rect)


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Uzay Kacisi v2 - Adim 6: Tam Oyun")
    saat = pygame.time.Clock()

    def oyunu_sifirla():
        """Tum oyun durumunu sifirla ve yeni oyun baslat."""
        nonlocal skor, oyun_aktif

        # Gruplari temizle
        tum_spritelar.empty()
        yildizlar.empty()
        dusmanlar.empty()
        mermiler.empty()

        # Yildizlari yeniden olustur
        for _ in range(100):
            y = Yildiz()
            tum_spritelar.add(y)
            yildizlar.add(y)

        # Yeni oyuncu
        yeni_oyuncu = Oyuncu()
        tum_spritelar.add(yeni_oyuncu)

        skor = 0
        oyun_aktif = True

        return yeni_oyuncu

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()

    skor = 0
    oyun_aktif = True

    # Yildizlari olustur
    for _ in range(100):
        y = Yildiz()
        tum_spritelar.add(y)
        yildizlar.add(y)

    # Oyuncuyu olustur
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Dusman zamanlayicisi
    pygame.time.set_timer(DUSMAN_OLAY, DUSMAN_ARALIK)

    # Font
    font = pygame.font.SysFont(None, 28)

    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- Olaylar ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_r and not oyun_aktif:
                    oyuncu = oyunu_sifirla()
            elif olay.type == DUSMAN_OLAY and oyun_aktif:
                d = Dusman()
                tum_spritelar.add(d)
                dusmanlar.add(d)

        if oyun_aktif:
            # Space ile ates
            tuslar = pygame.key.get_pressed()
            if tuslar[pygame.K_SPACE] and oyuncu.ates_edebilir_mi():
                m = Mermi(oyuncu.rect.centerx, oyuncu.rect.top)
                tum_spritelar.add(m)
                mermiler.add(m)

            # --- Guncelleme ---
            tum_spritelar.update()

            # --- Carpisma Algilama ---
            carpismalar = pygame.sprite.groupcollide(
                mermiler, dusmanlar, True, True
            )
            for mermi, vurulan_dusmanlar in carpismalar.items():
                skor += DUSMAN_PUAN * len(vurulan_dusmanlar)

            dusman_carpismalari = pygame.sprite.spritecollide(
                oyuncu, dusmanlar, True
            )
            for dusman in dusman_carpismalari:
                oyuncu.hasar_al(DUSMAN_HASAR)

            # Can kontrolu
            if oyuncu.can <= 0:
                oyuncu.kill()
                oyun_aktif = False
        else:
            # Game over durumunda sadece yildizlar hareket etsin
            yildizlar.update()

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        if oyun_aktif:
            hud_ciz(ekran, font, skor, oyuncu, dusmanlar)
        else:
            game_over_ciz(ekran, skor)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# ============================================================
# BEKLENEN CIKTI
# ============================================================
# - Adim 5'teki her sey (HUD, carpismalar, skor, can)
# - Can sifira dusunce:
#   - Oyuncu yok olur
#   - Yari saydam siyah overlay
#   - "GAME OVER" kirmizi buyuk metin
#   - Skor sari metin
#   - "R: Tekrar | ESC: Cikis" gri metin
# - R tusuna basinca oyun basarilan sifirlanir
# - Game over durumunda yildizlar kaymaya devam eder
# - [OK] Game Over ekrani calisiyor
# - [OK] R ile tekrar baslatma calisiyor
# - [OK] Tam oyun deneyimi
