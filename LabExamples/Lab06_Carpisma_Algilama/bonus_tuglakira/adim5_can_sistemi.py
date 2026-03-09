"""
Tugla Kirma (Breakout) - Adim 5: Can Sistemi, Game Over, Kazanma

Can sistemi eklenir. Top duserse can azalir, canlar bitince
Game Over olur. Bosluq tusu ile top firlatilir.

Ogrenilecek kavramlar:
- Can sistemi ve oyun durumlari
- Top firlatma mekanigi (bosluk tusu)
- Yari saydam kaplama (overlay) ile mesaj gosterme
- Oyunu yeniden baslatma (R tusu)

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Lab: 06 - Bonus: Tugla Kirma (Adim 5/7)

Calistirma: uv run python adim5_can_sistemi.py
Gereksinimler: pygame
"""

import pygame
import sys
import math

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
TOP_HIZ = 5
RAKET_HIZ = 7

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


class Raket(pygame.sprite.Sprite):
    """Oyuncunun kontrol ettigi raket."""

    def __init__(self):
        super().__init__()
        self.genislik = 120
        self.yukseklik = 15
        self.image = pygame.Surface((self.genislik, self.yukseklik), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image, ACIK_MAVI,
            (0, 0, self.genislik, self.yukseklik),
            border_radius=7
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.y = YUKSEKLIK - 30

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
        self.aktif = False  # False = raketin ustunde bekliyor

    def update(self, raket):
        """Top hareketi. Aktif degilse raketin ustunde durur."""
        if not self.aktif:
            self.rect.centerx = raket.rect.centerx
            self.rect.bottom = raket.rect.top
            return

        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

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
        self.rect.centerx = raket.rect.centerx
        self.rect.bottom = raket.rect.top


class Tugla(pygame.sprite.Sprite):
    """Kirilan tugla nesnesi."""

    def __init__(self, x, y, renk):
        super().__init__()
        self.image = pygame.Surface((TUGLA_GENISLIK, TUGLA_YUKSEKLIK))
        self.image.fill(renk)
        pygame.draw.rect(
            self.image, BEYAZ,
            (0, 0, TUGLA_GENISLIK, TUGLA_YUKSEKLIK), 1
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
    pygame.display.set_caption("Tugla Kirma - Adim 5: Can Sistemi")
    saat = pygame.time.Clock()
    yazi_tipi = pygame.font.SysFont("Arial", 24)
    buyuk_yazi = pygame.font.SysFont("Arial", 48, bold=True)
    kucuk_yazi = pygame.font.SysFont("Arial", 20)

    def oyunu_sifirla():
        """Oyunu bastan baslatir."""
        nonlocal raket, top, tuglalar, tum_spritelar, skor, can, oyun_bitti, kazandi
        raket = Raket()
        top = Top()
        tuglalar = tugla_olustur()
        tum_spritelar = pygame.sprite.Group()
        tum_spritelar.add(raket, top)
        tum_spritelar.add(tuglalar)
        skor = 0
        can = 3
        oyun_bitti = False
        kazandi = False
        top.sifirla(raket)

    raket = None
    top = None
    tuglalar = None
    tum_spritelar = None
    skor = 0
    can = 3
    oyun_bitti = False
    kazandi = False
    oyunu_sifirla()

    # Yari saydam kaplama
    overlay = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    calistir = True
    while calistir:
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
            # Guncelle
            raket.update()
            top.update(raket)
            top.raket_sekmesi(raket)

            # Tugla carpisma
            if top.aktif:
                kirilan = pygame.sprite.spritecollide(top, tuglalar, True)
                if kirilan:
                    top.hiz_y = -top.hiz_y
                    skor += len(kirilan) * 10

            # Top duserse can azalt
            if top.aktif and top.rect.top > YUKSEKLIK:
                can -= 1
                if can <= 0:
                    oyun_bitti = True
                else:
                    top.sifirla(raket)

            # Kazanma kontrolu
            if len(tuglalar) == 0:
                kazandi = True

        # Ciz
        ekran.fill(SIYAH)
        tum_spritelar.draw(ekran)

        # Skor ve can
        skor_yazi = yazi_tipi.render(f"Skor: {skor}", True, BEYAZ)
        can_yazi = yazi_tipi.render(f"Can: {can}", True, BEYAZ)
        ekran.blit(skor_yazi, (10, 10))
        ekran.blit(can_yazi, (GENISLIK - 80, 10))

        # Top aktif degilse bilgi mesaji
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
        saat.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# --- BEKLENEN CIKTI ---
# [OK] Oyun baslarken top raketin ustunde bekler
# [OK] BOSLUK tusu ile top firlatilir
# [OK] Top duserse can 1 azalir ve top raketin ustune doner
# [OK] Can 0 olunca yari saydam ekranda "GAME OVER" gorulur
# [OK] Tum tuglalar kirilinca "KAZANDINIZ!" mesaji gorulur
# [OK] R tusu ile oyun yeniden baslar
# [OK] Sag ustte can sayisi guncellenir
# [OK] ESC ile cikis yapilir
