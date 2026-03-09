"""
Tugla Kirma (Breakout) - Adim 7: Polished Tam Versiyon

Coklu seviye, parcacik efektleri, zorluk artisi, en yuksek skor
takibi ve duraklatma ozellikleri ile tamamlanmis Breakout oyunu.

Ogrenilecek kavramlar:
- Seviye sistemi ve dinamik zorluk artisi
- Parcacik efektleri (Parcacik sinifi)
- Fade-in gecis animasyonu
- Oyun durumu yonetimi (duraklatma, seviye gecisi)
- En yuksek skor takibi (oturum bazli)

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Tugla Kirma (Adim 7/7)

Calistirma: uv run python adim7_tam_oyun.py
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
GUCLENDIRME_SANS = 0.20
MAKS_SATIR = 6

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
GRI = (120, 120, 120)

TUGLA_RENKLERI = [KIRMIZI, TURUNCU, SARI, YESIL, MOR, ACIK_MAVI]

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


class Parcacik(pygame.sprite.Sprite):
    """Tugla kirildikca ucan kucuk parcacik efekti."""

    def __init__(self, x, y, renk):
        super().__init__()
        self.boyut = random.randint(3, 6)
        self.image = pygame.Surface((self.boyut, self.boyut), pygame.SRCALPHA)
        self.image.fill(renk)
        self.rect = self.image.get_rect(center=(x, y))

        # Rastgele yon ve hiz
        aci = random.uniform(0, 2 * math.pi)
        hiz = random.uniform(2, 6)
        self.hiz_x = math.cos(aci) * hiz
        self.hiz_y = math.sin(aci) * hiz
        self.omur = random.uniform(0.3, 0.8)  # Saniye cinsinden
        self.gecen_zaman = 0
        self.alfa = 255

    def update(self, dt):
        """Parcacik hareketi ve solma."""
        self.gecen_zaman += dt
        if self.gecen_zaman >= self.omur:
            self.kill()
            return

        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y
        self.hiz_y += 5 * dt  # Hafif yercekimi

        # Solma efekti
        oran = 1.0 - (self.gecen_zaman / self.omur)
        self.alfa = max(0, int(255 * oran))
        self.image.set_alpha(self.alfa)


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
        """Raket gorselini olusturur."""
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
        self.hiz_carpani = 1.0
        self.temel_hiz = TOP_HIZ

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

            self.hiz_x = math.sin(math.radians(aci)) * self.temel_hiz
            self.hiz_y = -abs(math.cos(math.radians(aci)) * self.temel_hiz)
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


def tugla_olustur(satir_sayisi=4):
    """Belirtilen satir sayisinda tugla izgara duzeni olusturur."""
    tuglalar = pygame.sprite.Group()
    for satir in range(satir_sayisi):
        renk = TUGLA_RENKLERI[satir % len(TUGLA_RENKLERI)]
        for sutun in range(TUGLA_SUTUN_SAYISI):
            x = TUGLA_BASLANGIC_X + sutun * (TUGLA_GENISLIK + TUGLA_SUTUN_BOSLUK)
            y = TUGLA_BASLANGIC_Y + satir * TUGLA_SATIR_YUKSEKLIK
            tugla = Tugla(x, y, renk)
            tuglalar.add(tugla)
    return tuglalar


def parcacik_olustur(x, y, renk, parcaciklar, adet=8):
    """Belirtilen noktada parcacik efekti olusturur."""
    for _ in range(adet):
        p = Parcacik(x, y, renk)
        parcaciklar.add(p)


def main():
    """Ana oyun dongusu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Tugla Kirma - Tam Versiyon")
    saat = pygame.time.Clock()
    yazi_tipi = pygame.font.SysFont("Arial", 24)
    buyuk_yazi = pygame.font.SysFont("Arial", 48, bold=True)
    kucuk_yazi = pygame.font.SysFont("Arial", 20)
    dev_yazi = pygame.font.SysFont("Arial", 64, bold=True)

    en_yuksek_skor = 0

    # Oyun durumlari
    OYNUYOR = "oynuyor"
    DURAKLATILDI = "duraklatildi"
    OYUN_BITTI = "oyun_bitti"
    KAZANDI = "kazandi"
    SEVIYE_GECISI = "seviye_gecisi"

    def yeni_oyun():
        """Oyunu tamamen sifirlar."""
        nonlocal raket, top, tuglalar, guclendirmeler, parcaciklar
        nonlocal skor, can, seviye, durum
        nonlocal genis_zamanlayici, hizli_zamanlayici
        nonlocal gecis_alfa, gecis_zamanlayici

        raket = Raket()
        top = Top()
        seviye = 1
        satir = min(4, MAKS_SATIR)
        tuglalar = tugla_olustur(satir)
        guclendirmeler = pygame.sprite.Group()
        parcaciklar = pygame.sprite.Group()
        skor = 0
        can = 3
        durum = OYNUYOR
        genis_zamanlayici = 0
        hizli_zamanlayici = 0
        gecis_alfa = 0
        gecis_zamanlayici = 0
        top.temel_hiz = TOP_HIZ
        top.sifirla(raket)

    def sonraki_seviye():
        """Sonraki seviyeye gecer."""
        nonlocal seviye, tuglalar, guclendirmeler, durum
        nonlocal gecis_alfa, gecis_zamanlayici
        nonlocal genis_zamanlayici, hizli_zamanlayici

        seviye += 1
        satir = min(4 + (seviye - 1), MAKS_SATIR)
        tuglalar = tugla_olustur(satir)
        guclendirmeler = pygame.sprite.Group()

        # Zorluk artisi: top biraz hizlanir her seviyede
        top.temel_hiz = TOP_HIZ + (seviye - 1) * 0.3
        top.sifirla(raket)
        raket.normal_boyut()
        genis_zamanlayici = 0
        hizli_zamanlayici = 0
        top.hiz_carpani = 1.0

        # Seviye gecis animasyonu basla
        durum = SEVIYE_GECISI
        gecis_alfa = 255
        gecis_zamanlayici = 1.5  # 1.5 saniye fade-in

    # Degiskenleri baslat
    raket = None
    top = None
    tuglalar = None
    guclendirmeler = None
    parcaciklar = None
    skor = 0
    can = 3
    seviye = 1
    durum = OYNUYOR
    genis_zamanlayici = 0
    hizli_zamanlayici = 0
    gecis_alfa = 0
    gecis_zamanlayici = 0
    yeni_oyun()

    overlay = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
    gecis_surface = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)

    calistir = True
    while calistir:
        dt = saat.tick(FPS) / 1000.0

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_SPACE:
                    if durum == OYNUYOR:
                        top.firlat()
                elif olay.key == pygame.K_r:
                    yeni_oyun()
                elif olay.key == pygame.K_p:
                    if durum == OYNUYOR:
                        durum = DURAKLATILDI
                    elif durum == DURAKLATILDI:
                        durum = OYNUYOR

        # --- Guncelleme ---
        if durum == SEVIYE_GECISI:
            gecis_zamanlayici -= dt
            gecis_alfa = max(0, int(255 * (gecis_zamanlayici / 1.5)))
            if gecis_zamanlayici <= 0:
                durum = OYNUYOR
                gecis_alfa = 0

        elif durum == OYNUYOR:
            # Zamanlayicilar
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

            raket.update()
            top.update(raket)
            top.raket_sekmesi(raket)
            guclendirmeler.update()

            # Parcaciklari guncelle (dt parametresi ile)
            for p in parcaciklar:
                p.update(dt)

            # Tugla carpisma
            if top.aktif:
                kirilan = pygame.sprite.spritecollide(top, tuglalar, True)
                if kirilan:
                    top.hiz_y = -top.hiz_y
                    skor += len(kirilan) * 10

                    for tugla in kirilan:
                        # Parcacik efekti
                        parcacik_olustur(
                            tugla.rect.centerx, tugla.rect.centery,
                            tugla.renk, parcaciklar
                        )
                        # Guclendirme sansi
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
                    genis_zamanlayici = 5.0
                elif guc.tip == "ekstra_can":
                    can += 1
                elif guc.tip == "hizli_top":
                    top.hiz_carpani = 1.5
                    hizli_zamanlayici = 5.0

            # Top duserse
            if top.aktif and top.rect.top > YUKSEKLIK:
                can -= 1
                if can <= 0:
                    durum = OYUN_BITTI
                    if skor > en_yuksek_skor:
                        en_yuksek_skor = skor
                else:
                    top.sifirla(raket)

            # Tum tuglalar kirildiysa
            if len(tuglalar) == 0:
                if skor > en_yuksek_skor:
                    en_yuksek_skor = skor
                sonraki_seviye()

        # --- Cizim ---
        ekran.fill(SIYAH)

        # Oyun alani
        tuglalar.draw(ekran)
        guclendirmeler.draw(ekran)
        parcaciklar.draw(ekran)
        ekran.blit(raket.image, raket.rect)
        ekran.blit(top.image, top.rect)

        # Ust bilgi cubugu
        skor_yazi = yazi_tipi.render(f"Skor: {skor}", True, BEYAZ)
        can_yazi = yazi_tipi.render(f"Can: {can}", True, BEYAZ)
        seviye_yazi = yazi_tipi.render(f"Seviye: {seviye}", True, BEYAZ)
        rekor_yazi = kucuk_yazi.render(f"En Yuksek: {en_yuksek_skor}", True, GRI)

        ekran.blit(skor_yazi, (10, 10))
        ekran.blit(seviye_yazi, (GENISLIK // 2 - seviye_yazi.get_width() // 2, 10))
        ekran.blit(can_yazi, (GENISLIK - 80, 10))
        ekran.blit(rekor_yazi, (GENISLIK - rekor_yazi.get_width() - 10, 35))

        # Aktif guclendirme zamanlayicilari
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

        # Bilgi mesaji - top beklerken
        if not top.aktif and durum == OYNUYOR:
            bilgi = kucuk_yazi.render("BOSLUK tusu ile topu firlat", True, SARI)
            bilgi_rect = bilgi.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 60))
            ekran.blit(bilgi, bilgi_rect)

        # Seviye gecis efekti (fade-in)
        if durum == SEVIYE_GECISI:
            gecis_surface.fill((0, 0, 0, gecis_alfa))
            ekran.blit(gecis_surface, (0, 0))
            seviye_mesaj = dev_yazi.render(f"Seviye {seviye}", True, BEYAZ)
            mesaj_rect = seviye_mesaj.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2))
            ekran.blit(seviye_mesaj, mesaj_rect)

        # Duraklatma
        if durum == DURAKLATILDI:
            overlay.fill((0, 0, 0, 150))
            ekran.blit(overlay, (0, 0))
            dur_yazi = buyuk_yazi.render("DURAKLATILDI", True, SARI)
            dur_rect = dur_yazi.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 - 20))
            ekran.blit(dur_yazi, dur_rect)

            devam = kucuk_yazi.render("Devam etmek icin P tusuna basin", True, BEYAZ)
            devam_rect = devam.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 30))
            ekran.blit(devam, devam_rect)

        # Game Over
        if durum == OYUN_BITTI:
            overlay.fill((0, 0, 0, 150))
            ekran.blit(overlay, (0, 0))

            go_yazi = buyuk_yazi.render("GAME OVER", True, KIRMIZI)
            go_rect = go_yazi.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 - 40))
            ekran.blit(go_yazi, go_rect)

            skor_son = yazi_tipi.render(f"Son Skor: {skor}", True, BEYAZ)
            skor_rect = skor_son.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 10))
            ekran.blit(skor_son, skor_rect)

            rekor_son = yazi_tipi.render(
                f"En Yuksek Skor: {en_yuksek_skor}", True, SARI
            )
            rekor_rect = rekor_son.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 40))
            ekran.blit(rekor_son, rekor_rect)

            tekrar = kucuk_yazi.render(
                "Tekrar baslatmak icin R tusuna basin", True, BEYAZ
            )
            tekrar_rect = tekrar.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2 + 75))
            ekran.blit(tekrar, tekrar_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# --- BEKLENEN CIKTI ---
# [OK] Tam ozellikli Tugla Kirma oyunu
# [OK] Tum tuglalar kirilinca sonraki seviyeye gecilir (+1 satir tugla, maks 6)
# [OK] Seviye gecisinde fade-in animasyonu gorulur
# [OK] Her seviyede top hizi biraz artar (zorluk artisi)
# [OK] Tuglalar kirildikca renkli parcacik efektleri olusur
# [OK] Guclendirmeler calismaya devam eder (genis raket, ekstra can, hizli top)
# [OK] P tusu ile oyun duraklatilir/devam eder
# [OK] En yuksek skor (oturum bazli) sag ustte gorulur
# [OK] Seviye bilgisi ortada gorulur
# [OK] R ile yeniden baslama, ESC ile cikis
