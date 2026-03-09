"""
Tugla Kirma (Breakout) - Adim 6: Guclendirme Sistemi (Power-up)

Tuglalar kirildikca rastgele guclendirmeler duser. Genis raket,
ekstra can ve hizli top guclendirmeleri vardir.

Ogrenilecek kavramlar:
- Guclendirme (power-up) sprite sinifi
- Rastgele olasilik ile nesne uretme
- Zamanlayici ile gecici efekt yonetimi
- Sprite gorunumunu dinamik degistirme

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Tugla Kirma (Adim 6/7)

Calistirma: uv run python adim6_powerup.py
Gereksinimler: pygame
"""

import pygame
import sys
import math
import random

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
TOP_HIZ = 5
RAKET_HIZ = 7
GUCLENDIRME_HIZ = 2
GUCLENDIRME_SANS = 0.20  # %20 olasilik

# --- Renkler ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (0, 0, 139)
ACIK_MAVI = (100, 149, 237)
KIRMIZI = (220, 50, 50)
YESIL = (50, 200, 50)
SARI = (240, 220, 50)
TURUNCU = (240, 150, 30)
MOR = (160, 50, 200)

TUGLA_RENKLERI = [KIRMIZI, TURUNCU, SARI, YESIL]

# --- Tugla sabitleri ---
TUGLA_GENISLIK = 70
TUGLA_YUKSEKLIK = 25
TUGLA_BASLANGIC_X = 90
TUGLA_BASLANGIC_Y = 60
TUGLA_SATIR_YUKSEKLIK = 35
TUGLA_SUTUN_SAYISI = 5
TUGLA_SUTUN_BOSLUK = 5

# --- Guclendirme tipleri ---
GUCLENDIRME_TIPLERI = [
    {"tip": "genis", "renk": YESIL, "etiket": "G"},
    {"tip": "ekstra_can", "renk": ACIK_MAVI, "etiket": "+"},
    {"tip": "hizli_top", "renk": KIRMIZI, "etiket": "H"},
]


class Raket(pygame.sprite.Sprite):
    """Oyuncunun kontrol ettigi raket."""

    def __init__(self):
        super().__init__()
        self.normal_genislik = 120
        self.genislik = self.normal_genislik
        self.yukseklik = 15
        self._gorsel_olustur()
        self.rect.centerx = GENISLIK // 2
        self.rect.y = YUKSEKLIK - 30

    def _gorsel_olustur(self):
        """Raket gorselini yeniden olusturur (boyut degisimlerinde)."""
        eski_center = getattr(self, 'rect', None)
        eski_centerx = eski_center.centerx if eski_center else GENISLIK // 2
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image, ACIK_MAVI,
            (0, 0, self.genislik, self.yukseklik),
            border_radius=7
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = eski_centerx
        self.rect.y = YUKSEKLIK - 30

    def genislet(self):
        """Raketi 2 katina genisletir."""
        self.genislik = self.normal_genislik * 2
        self._gorsel_olustur()

    def normal_boyut(self):
        """Raketi normal boyutuna dondurur."""
        self.genislik = self.normal_genislik
        self._gorsel_olustur()

    def update(self):
        """Klavye ile raket hareketi."""
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]:
            self.rect.x -= RAKET_HIZ
        if tuslar[pygame.K_RIGHT]:
            self.rect.x += RAKET_HIZ
        self.rect.clamp_ip(pygame.Rect(0, 0, GENISLIK, YUKSEKLIK))


class Top(pygame.sprite.Sprite):
    """Oyun topu."""

    def __init__(self):
        super().__init__()
        self.yaricap = 8
        boyut = self.yaricap * 2
        self.image = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BEYAZ, (self.yaricap, self.yaricap), self.yaricap)
        self.rect = self.image.get_rect()
        self.hiz_x = 3.0
        self.hiz_y = -4.0
        self.aktif = False
        self.hiz_carpani = 1.0  # Guclendirme ile degisir

    def update(self, raket):
        """Top hareketi."""
        if not self.aktif:
            self.rect.centerx = raket.rect.centerx
            self.rect.bottom = raket.rect.top
            return

        self.rect.x += self.hiz_x * self.hiz_carpani
        self.rect.y += self.hiz_y * self.hiz_carpani

        if self.rect.left <= 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x)
        elif self.rect.right >= GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.hiz_y = abs(self.hiz_y)

    def raket_sekmesi(self, raket):
        """Raket ile carpisma ve aci hesabi."""
        if not self.aktif:
            return
        if self.rect.colliderect(raket.rect) and self.hiz_y > 0:
            vurun_x = self.rect.centerx - raket.rect.left
            oran = vurun_x / raket.rect.width
            aci = (oran - 0.5) * 120

            self.hiz_x = math.sin(math.radians(aci)) * TOP_HIZ
            self.hiz_y = -abs(math.cos(math.radians(aci)) * TOP_HIZ)
            self.rect.bottom = raket.rect.top

    def firlat(self):
        """Topu firlatir."""
        if not self.aktif:
            self.aktif = True
            self.hiz_x = 3.0
            self.hiz_y = -4.0

    def sifirla(self, raket):
        """Topu raketin ustune sifirlar."""
        self.aktif = False
        self.hiz_carpani = 1.0
        self.rect.centerx = raket.rect.centerx
        self.rect.bottom = raket.rect.top


class Tugla(pygame.sprite.Sprite):
    """Kirilan tugla nesnesi."""

    def __init__(self, x, y, renk):
        super().__init__()
        self.renk = renk
        self.image = pygame.Surface((TUGLA_GENISLIK, TUGLA_YUKSEKLIK))
        self.image.fill(renk)
        pygame.draw.rect(
            self.image, BEYAZ,
            (0, 0, TUGLA_GENISLIK, TUGLA_YUKSEKLIK), 1
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Guclendirme(pygame.sprite.Sprite):
    """Tuglalardan dusen guclendirme nesnesi."""

    def __init__(self, x, y):
        super().__init__()
        bilgi = random.choice(GUCLENDIRME_TIPLERI)
        self.tip = bilgi["tip"]
        renk = bilgi["renk"]
        etiket = bilgi["etiket"]

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, renk, (0, 0, 20, 20), border_radius=4)
        # Etiket harfini ciz
        kucuk_font = pygame.font.SysFont("Arial", 14, bold=True)
        harf = kucuk_font.render(etiket, True, BEYAZ)
        harf_rect = harf.get_rect(center=(10, 10))
        self.image.blit(harf, harf_rect)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        """Guclendirme asagi duser."""
        self.rect.y += GUCLENDIRME_HIZ
        if self.rect.top > YUKSEKLIK:
            self.kill()


def tugla_olustur():
    """5 sutun x 4 satir tugla izgara duzeni olusturur."""
    tuglalar = pygame.sprite.Group()
    for satir in range(4):
        renk = TUGLA_RENKLERI[satir]
        for sutun in range(TUGLA_SUTUN_SAYISI):
            x = TUGLA_BASLANGIC_X + sutun * (TUGLA_GENISLIK + TUGLA_SUTUN_BOSLUK)
            y = TUGLA_BASLANGIC_Y + satir * TUGLA_SATIR_YUKSEKLIK
            tugla = Tugla(x, y, renk)
            tuglalar.add(tugla)
    return tuglalar


def main():
    """Ana oyun dongusu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Tugla Kirma - Adim 6: Guclendirmeler")
    saat = pygame.time.Clock()
    yazi_tipi = pygame.font.SysFont("Arial", 24)
    buyuk_yazi = pygame.font.SysFont("Arial", 48, bold=True)
    kucuk_yazi = pygame.font.SysFont("Arial", 20)

    def oyunu_sifirla():
        """Oyunu bastan baslatir."""
        nonlocal raket, top, tuglalar, guclendirmeler
        nonlocal skor, can, oyun_bitti, kazandi
        nonlocal genis_zamanlayici, hizli_zamanlayici

        raket = Raket()
        top = Top()
        tuglalar = tugla_olustur()
        guclendirmeler = pygame.sprite.Group()
        skor = 0
        can = 3
        oyun_bitti = False
        kazandi = False
        genis_zamanlayici = 0
        hizli_zamanlayici = 0
        top.sifirla(raket)

    raket = None
    top = None
    tuglalar = None
    guclendirmeler = None
    skor = 0
    can = 3
    oyun_bitti = False
    kazandi = False
    genis_zamanlayici = 0
    hizli_zamanlayici = 0
    oyunu_sifirla()

    overlay = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    calistir = True
    while calistir:
        dt = saat.tick(FPS) / 1000.0  # Saniye cinsinden delta zaman

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_SPACE:
                    if not oyun_bitti and not kazandi:
                        top.firlat()
                elif olay.key == pygame.K_r:
                    oyunu_sifirla()

        if not oyun_bitti and not kazandi:
            # Zamanlayicilari guncelle
            if genis_zamanlayici > 0:
                genis_zamanlayici -= dt
                if genis_zamanlayici <= 0:
                    genis_zamanlayici = 0
                    raket.normal_boyut()

            if hizli_zamanlayici > 0:
                hizli_zamanlayici -= dt
                if hizli_zamanlayici <= 0:
                    hizli_zamanlayici = 0
                    top.hiz_carpani = 1.0

            # Guncelle
            raket.update()
            top.update(raket)
            top.raket_sekmesi(raket)
            guclendirmeler.update()

            # Tugla carpisma
            if top.aktif:
                kirilan = pygame.sprite.spritecollide(top, tuglalar, True)
                if kirilan:
                    top.hiz_y = -top.hiz_y
                    skor += len(kirilan) * 10

                    # Guclendirme uretme sansi
                    for tugla in kirilan:
                        if random.random() < GUCLENDIRME_SANS:
                            guc = Guclendirme(
                                tugla.rect.centerx, tugla.rect.centery
                            )
                            guclendirmeler.add(guc)

            # Guclendirme toplama
            toplanan = pygame.sprite.spritecollide(raket, guclendirmeler, True)
            for guc in toplanan:
                if guc.tip == "genis":
                    raket.genislet()
                    genis_zamanlayici = 5.0  # 5 saniye
                elif guc.tip == "ekstra_can":
                    can += 1
                elif guc.tip == "hizli_top":
                    top.hiz_carpani = 1.5
                    hizli_zamanlayici = 5.0  # 5 saniye

            # Top duserse
            if top.aktif and top.rect.top > YUKSEKLIK:
                can -= 1
                if can <= 0:
                    oyun_bitti = True
                else:
                    top.sifirla(raket)

            # Kazanma
            if len(tuglalar) == 0:
                kazandi = True

        # --- Cizim ---
        ekran.fill(SIYAH)
        tuglalar.draw(ekran)
        guclendirmeler.draw(ekran)
        ekran.blit(raket.image, raket.rect)
        ekran.blit(top.image, top.rect)

        # Skor ve can
        skor_yazi = yazi_tipi.render(f"Skor: {skor}", True, BEYAZ)
        can_yazi = yazi_tipi.render(f"Can: {can}", True, BEYAZ)
        ekran.blit(skor_yazi, (10, 10))
        ekran.blit(can_yazi, (GENISLIK - 80, 10))

        # Aktif guclendirme zamanlayicilari goster
        bilgi_y = 40
        if genis_zamanlayici > 0:
            gz = kucuk_yazi.render(
                f"[G] Genis raket: {genis_zamanlayici:.1f}s", True, YESIL
            )
            ekran.blit(gz, (10, bilgi_y))
            bilgi_y += 22
        if hizli_zamanlayici > 0:
            hz = kucuk_yazi.render(
                f"[H] Hizli top: {hizli_zamanlayici:.1f}s", True, KIRMIZI
            )
            ekran.blit(hz, (10, bilgi_y))
            bilgi_y += 22

        # Bilgi mesaji
        if not top.aktif and not oyun_bitti and not kazandi:
            bilgi = kucuk_yazi.render("BOSLUK tusu ile topu firlat", True, SARI)
            bilgi_rect = bilgi.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 60))
            ekran.blit(bilgi, bilgi_rect)

        # Game Over
        if oyun_bitti:
            ekran.blit(overlay, (0, 0))
            go_yazi = buyuk_yazi.render("GAME OVER", True, KIRMIZI)
            go_rect = go_yazi.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 - 20))
            ekran.blit(go_yazi, go_rect)

            skor_son = yazi_tipi.render(f"Son Skor: {skor}", True, BEYAZ)
            skor_rect = skor_son.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 30))
            ekran.blit(skor_son, skor_rect)

            tekrar = kucuk_yazi.render("Tekrar baslatmak icin R tusuna basin", True, SARI)
            tekrar_rect = tekrar.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 60))
            ekran.blit(tekrar, tekrar_rect)

        # Kazanma
        if kazandi:
            ekran.blit(overlay, (0, 0))
            kazan_yazi = buyuk_yazi.render("KAZANDINIZ!", True, YESIL)
            kazan_rect = kazan_yazi.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 - 20))
            ekran.blit(kazan_yazi, kazan_rect)

            skor_son = yazi_tipi.render(f"Toplam Skor: {skor}", True, BEYAZ)
            skor_rect = skor_son.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 30))
            ekran.blit(skor_son, skor_rect)

            tekrar = kucuk_yazi.render("Tekrar baslatmak icin R tusuna basin", True, SARI)
            tekrar_rect = tekrar.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 60))
            ekran.blit(tekrar, tekrar_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# --- BEKLENEN CIKTI ---
# [OK] Tuglalar kirildikca %20 olasilikla guclendirme duser
# [OK] Yesil [G] guclendirme: raket 2 kat genisler, 5 saniye surer
# [OK] Mavi [+] guclendirme: +1 can ekler
# [OK] Kirmizi [H] guclendirme: top 1.5 kat hizlanir, 5 saniye surer
# [OK] Guclendirme raket ile yakalanir, yere duserse kaybolur
# [OK] Aktif guclendirme zamanlayicisi sol ustte gorulur
# [OK] Zamanlayici bitince efekt kalkar (raket kuculur, top normallesir)
# [OK] Can, skor, game over ve kazanma sistemi onceki adimlarla ayni
# [OK] ESC ile cikis, R ile yeniden baslama
