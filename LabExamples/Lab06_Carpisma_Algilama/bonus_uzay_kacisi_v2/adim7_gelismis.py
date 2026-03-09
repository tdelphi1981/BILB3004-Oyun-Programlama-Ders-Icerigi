"""
Uzay Kacisi v2 - Adim 7: Farkli Dusman Tipleri + Cooldown + Zorluk

Son adim! Uc farkli dusman tipi (kucuk/hizli, orta, buyuk/yavas),
zaman icinde artan zorluk ve gorsel cooldown cubugu ekliyoruz.
Bu, tam ozellikli Uzay Kacisi v2 oyunudur.

Ogrenilecek kavramlar:
- Farkli dusman tipleri ve ozellikler
- Dinamik zorluk artisi (spawn araligi, hiz carpani)
- Cooldown gorsellestirme (cubuk)
- Oyun tasariminda denge ve cilas

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Uzay Kacisi v2 (Adim 7/7)

Calistirma: uv run python adim7_gelismis.py
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
MOR = (180, 50, 220)
KOYU_MOR = (120, 30, 150)
KOYU_TURUNCU = (180, 110, 0)
GUMI = (200, 200, 220)
KOYU_GRI = (40, 40, 50)
ACIK_GRI = (120, 120, 140)

# --- Oyuncu ---
OYUNCU_HIZ = 5
OYUNCU_CAN = 100
DUSMAN_HASAR = 25

# --- Mermi ---
MERMI_HIZ = 8
MERMI_COOLDOWN = 250

# --- Dusman ---
DUSMAN_OLAY = pygame.USEREVENT + 1
BASLANGIC_ARALIK = 1000  # Baslangic spawn araligi (ms)
MIN_ARALIK = 300          # Minimum spawn araligi (ms)

# --- Dusman Tipleri ---
# (ad, genislik, yukseklik, min_hiz, max_hiz, puan, renk, ic_renk)
DUSMAN_TIPLERI = {
    "kucuk": {
        "genislik": 25,
        "yukseklik": 20,
        "min_hiz": 3,
        "max_hiz": 5,
        "puan": 5,
        "renk": KIRMIZI,
        "ic_renk": KOYU_KIRMIZI,
    },
    "orta": {
        "genislik": 40,
        "yukseklik": 35,
        "min_hiz": 2,
        "max_hiz": 4,
        "puan": 10,
        "renk": TURUNCU,
        "ic_renk": KOYU_TURUNCU,
    },
    "buyuk": {
        "genislik": 55,
        "yukseklik": 45,
        "min_hiz": 1,
        "max_hiz": 2,
        "puan": 20,
        "renk": MOR,
        "ic_renk": KOYU_MOR,
    },
}

# --- Zorluk ---
ZORLUK_ARTIS_SURESI = 10000  # Her 10 saniyede zorluk artar
HIZ_CARPANI_ARTIS = 0.1       # Her zorluk adiminda hiz carpani artisi


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

    def cooldown_yuzdesi(self):
        """Cooldown doluluk yuzdesi (0.0 - 1.0). 1.0 = ates edebilir."""
        simdi = pygame.time.get_ticks()
        gecen = simdi - self.son_atis_zamani
        if gecen >= MERMI_COOLDOWN:
            return 1.0
        return gecen / MERMI_COOLDOWN

    def hasar_al(self, miktar):
        self.can -= miktar
        if self.can < 0:
            self.can = 0


class Dusman(pygame.sprite.Sprite):
    """Farkli tiplerde dusman gemisi."""

    def __init__(self, tip="orta", hiz_carpani=1.0):
        super().__init__()
        ozellikler = DUSMAN_TIPLERI[tip]
        self.tip = tip
        self.genislik = ozellikler["genislik"]
        self.yukseklik = ozellikler["yukseklik"]
        self.puan = ozellikler["puan"]
        self.renk = ozellikler["renk"]
        self.ic_renk = ozellikler["ic_renk"]

        # Hiz: temel hiz * zorluk carpani
        temel_hiz = random.uniform(
            ozellikler["min_hiz"], ozellikler["max_hiz"]
        )
        self.hiz = temel_hiz * hiz_carpani

        self.image = pygame.Surface(
            (self.genislik, self.yukseklik), pygame.SRCALPHA
        )
        self._gemi_ciz()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - self.genislik)
        self.rect.y = -self.yukseklik
        self.y_float = float(self.rect.y)

    def _gemi_ciz(self):
        """Dusman gemisini tip renginde ters ucgen olarak ciz."""
        noktalar = [
            (0, 0),
            (self.genislik, 0),
            (self.genislik // 2, self.yukseklik),
        ]
        pygame.draw.polygon(self.image, self.renk, noktalar)
        # Ic detay
        kenar = max(4, self.genislik // 6)
        ic_noktalar = [
            (kenar, kenar - 2),
            (self.genislik - kenar, kenar - 2),
            (self.genislik // 2, self.yukseklik - kenar),
        ]
        pygame.draw.polygon(self.image, self.ic_renk, ic_noktalar)

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


def hud_ciz(ekran, font, skor, oyuncu, dusmanlar, zorluk_seviyesi):
    """Gelismis HUD ciz."""
    # Sol ust: Skor
    skor_metin = font.render(f"Skor: {skor}", True, SARI)
    ekran.blit(skor_metin, (10, 10))

    # Sol ust ikinci satir: Dusman sayisi
    dusman_metin = font.render(
        f"Dusmanlar: {len(dusmanlar)}", True, KIRMIZI
    )
    ekran.blit(dusman_metin, (10, 36))

    # Sol ust ucuncu satir: Zorluk seviyesi
    zorluk_metin = font.render(
        f"Zorluk: {zorluk_seviyesi}", True, TURUNCU
    )
    ekran.blit(zorluk_metin, (10, 62))

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


def cooldown_cubugu_ciz(ekran, oyuncu):
    """Oyuncunun altinda cooldown cubugu ciz."""
    cubuk_genislik = 30
    cubuk_yukseklik = 4
    cubuk_x = oyuncu.rect.centerx - cubuk_genislik // 2
    cubuk_y = oyuncu.rect.bottom + 4

    yuzde = oyuncu.cooldown_yuzdesi()

    # Arka plan
    pygame.draw.rect(
        ekran, KOYU_GRI,
        (cubuk_x, cubuk_y, cubuk_genislik, cubuk_yukseklik)
    )

    # Dolu kisim
    dolu = int(cubuk_genislik * yuzde)
    if dolu > 0:
        renk = YESIL if yuzde >= 1.0 else ACIK_GRI
        pygame.draw.rect(
            ekran, renk,
            (cubuk_x, cubuk_y, dolu, cubuk_yukseklik)
        )


def game_over_ciz(ekran, skor, en_yuksek_skor):
    """Game Over ekranini ciz."""
    overlay = pygame.Surface((GENISLIK, YUKSEKLIK))
    overlay.set_alpha(160)
    overlay.fill(SIYAH)
    ekran.blit(overlay, (0, 0))

    buyuk_font = pygame.font.SysFont(None, 80)
    orta_font = pygame.font.SysFont(None, 40)
    kucuk_font = pygame.font.SysFont(None, 30)

    go_metin = buyuk_font.render("GAME OVER", True, KIRMIZI)
    go_rect = go_metin.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 - 60))
    ekran.blit(go_metin, go_rect)

    skor_metin = orta_font.render(f"Skor: {skor}", True, SARI)
    skor_rect = skor_metin.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2))
    ekran.blit(skor_metin, skor_rect)

    en_yuksek_metin = kucuk_font.render(
        f"En Yuksek Skor: {en_yuksek_skor}", True, TURUNCU
    )
    en_yuksek_rect = en_yuksek_metin.get_rect(
        center=(GENISLIK // 2, YUKSEKLIK // 2 + 40)
    )
    ekran.blit(en_yuksek_metin, en_yuksek_rect)

    bilgi_metin = kucuk_font.render(
        "R: Tekrar | ESC: Cikis", True, GUMI
    )
    bilgi_rect = bilgi_metin.get_rect(
        center=(GENISLIK // 2, YUKSEKLIK // 2 + 80)
    )
    ekran.blit(bilgi_metin, bilgi_rect)


def rastgele_dusman_tipi():
    """Agirlikli rastgele dusman tipi sec."""
    # %50 kucuk, %35 orta, %15 buyuk
    r = random.random()
    if r < 0.50:
        return "kucuk"
    elif r < 0.85:
        return "orta"
    else:
        return "buyuk"


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Uzay Kacisi v2 - Adim 7: Gelismis (Final)")
    saat = pygame.time.Clock()

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()

    # Oyun durumu
    skor = 0
    en_yuksek_skor = 0
    oyun_aktif = True
    zorluk_seviyesi = 1
    hiz_carpani = 1.0
    spawn_araligi = BASLANGIC_ARALIK
    son_zorluk_zamani = pygame.time.get_ticks()

    def yildizlari_olustur():
        for _ in range(100):
            y = Yildiz()
            tum_spritelar.add(y)
            yildizlar.add(y)

    def oyunu_sifirla():
        """Tum oyun durumunu sifirla."""
        nonlocal skor, oyun_aktif, zorluk_seviyesi, hiz_carpani
        nonlocal spawn_araligi, son_zorluk_zamani

        tum_spritelar.empty()
        yildizlar.empty()
        dusmanlar.empty()
        mermiler.empty()

        yildizlari_olustur()

        yeni_oyuncu = Oyuncu()
        tum_spritelar.add(yeni_oyuncu)

        skor = 0
        oyun_aktif = True
        zorluk_seviyesi = 1
        hiz_carpani = 1.0
        spawn_araligi = BASLANGIC_ARALIK
        son_zorluk_zamani = pygame.time.get_ticks()

        pygame.time.set_timer(DUSMAN_OLAY, spawn_araligi)

        return yeni_oyuncu

    # Baslangic olusturma
    yildizlari_olustur()
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Dusman zamanlayicisi
    pygame.time.set_timer(DUSMAN_OLAY, spawn_araligi)

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
                tip = rastgele_dusman_tipi()
                d = Dusman(tip=tip, hiz_carpani=hiz_carpani)
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

            # --- Zorluk Artisi ---
            simdi = pygame.time.get_ticks()
            if simdi - son_zorluk_zamani >= ZORLUK_ARTIS_SURESI:
                son_zorluk_zamani = simdi
                zorluk_seviyesi += 1
                hiz_carpani += HIZ_CARPANI_ARTIS

                # Spawn araligini azalt (ama MIN_ARALIK'in altina dusme)
                spawn_araligi = max(
                    MIN_ARALIK,
                    BASLANGIC_ARALIK - (zorluk_seviyesi - 1) * 100
                )
                pygame.time.set_timer(DUSMAN_OLAY, spawn_araligi)

            # --- Carpisma Algilama ---
            carpismalar = pygame.sprite.groupcollide(
                mermiler, dusmanlar, True, True
            )
            for mermi, vurulan_dusmanlar in carpismalar.items():
                for vurulan in vurulan_dusmanlar:
                    skor += vurulan.puan

            dusman_carpismalari = pygame.sprite.spritecollide(
                oyuncu, dusmanlar, True
            )
            for dusman in dusman_carpismalari:
                oyuncu.hasar_al(DUSMAN_HASAR)

            # Can kontrolu
            if oyuncu.can <= 0:
                oyuncu.kill()
                oyun_aktif = False
                if skor > en_yuksek_skor:
                    en_yuksek_skor = skor
        else:
            # Game over: sadece yildizlar
            yildizlar.update()

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        if oyun_aktif:
            hud_ciz(ekran, font, skor, oyuncu, dusmanlar, zorluk_seviyesi)
            cooldown_cubugu_ciz(ekran, oyuncu)
        else:
            game_over_ciz(ekran, skor, en_yuksek_skor)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# ============================================================
# BEKLENEN CIKTI
# ============================================================
# - Adim 6'daki her sey (tam oyun dongusu)
# - 3 farkli dusman tipi:
#   - Kucuk (kirmizi, 25x20, hizli, 5 puan)
#   - Orta (turuncu, 40x35, normal hiz, 10 puan)
#   - Buyuk (mor, 55x45, yavas, 20 puan)
# - Zorluk her 10 saniyede artar:
#   - Spawn araligi azalir (1000ms -> 300ms minimum)
#   - Dusman hizlari artar (hiz carpani yukselir)
# - Zorluk seviyesi HUD'da gosterilir
# - Oyuncu altinda cooldown cubugu (hazir: yesil, bekleme: gri)
# - En yuksek skor Game Over ekraninda gosterilir
# - [OK] 3 farkli dusman tipi calisiyor
# - [OK] Zorluk artisi aktif
# - [OK] Cooldown cubugu gorsel
# - [OK] Tam ozellikli Uzay Kacisi v2!
