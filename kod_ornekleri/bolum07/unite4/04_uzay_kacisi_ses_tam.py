"""
Uzay Kacisi - Tam Ses Entegrasyonu

Bu program Uzay Kacisi projesinin ses entegrasyonlu versiyonunu
gosterir. SoundManager sinifi ile SFX, muzik ve ses ayarlari
merkezi olarak yonetilir.

Ogrenilecek kavramlar:
- SoundManager sinifinin oyuna entegrasyonu
- Oyun olaylarina ses baglama
- Muzik ve SFX birlestirme
- Sessiz modu ve volume kontrolu

Bolum: 07 - Ses ve Muzik
Unite: 4 - Ses Tasarimi Prensipleri

Calistirma: python 04_uzay_kacisi_ses_tam.py
Gereksinimler: pygame

Not: Bu ornek gorsel/ses dosyalari olmadan basitlestirilmis
geometrik sekiller ve konsol ciktisi ile calisir.
"""

import os
import random
import pygame

# -- Sabitler --
GENISLIK = 600
YUKSEKLIK = 700
FPS = 60
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
KIRMIZI = (200, 50, 50)
MAVI = (50, 100, 200)
YESIL = (50, 200, 100)
SARI = (255, 200, 50)


# =============================================================================
# SoundManager Sinifi
# =============================================================================
class SoundManager:
    """Merkezi ses yonetim sinifi."""

    def __init__(self, ses_dizini="assets/sounds"):
        self.master_volume = 1.0
        self.sfx_volume = 0.75
        self.bgm_volume = 0.40
        self._onceki_volume = 1.0
        self.sesler = {}
        self.ses_dizini = ses_dizini
        self._sesleri_yukle()

    def _sesleri_yukle(self):
        """SFX seslerini yukle (dosya varsa)."""
        sfx_dosyalari = {
            "ates": "sfx/ates.ogg",
            "patlama": "sfx/patlama.ogg",
            "hasar": "sfx/hasar.ogg",
            "bonus": "sfx/bonus.ogg",
        }
        for ad, dosya in sfx_dosyalari.items():
            yol = os.path.join(self.ses_dizini, dosya)
            if os.path.exists(yol):
                self.sesler[ad] = pygame.mixer.Sound(yol)
                self.sesler[ad].set_volume(
                    self.sfx_volume * self.master_volume
                )

    def cal(self, ad, dongu=0):
        """SFX sesi cal."""
        ses = self.sesler.get(ad)
        if ses:
            ses.play(loops=dongu)
        # Ses dosyasi yoksa konsola bilgi yaz (demo modu)
        # print(f"  [SES] {ad}")

    def muzik_cal(self, dosya, dongu=-1, fade_ms=1000):
        """Arka plan muzigini cal."""
        yol = os.path.join(self.ses_dizini, "muzik", dosya)
        if os.path.exists(yol):
            pygame.mixer.music.load(yol)
            pygame.mixer.music.set_volume(
                self.bgm_volume * self.master_volume
            )
            pygame.mixer.music.play(loops=dongu, fade_ms=fade_ms)

    def muzik_durdur(self, fade_ms=500):
        """Muzigi fade out ile durdur."""
        pygame.mixer.music.fadeout(fade_ms)

    def master_ayarla(self, deger):
        """Master volume ayarla."""
        self.master_volume = max(0.0, min(1.0, deger))
        for ses in self.sesler.values():
            ses.set_volume(self.sfx_volume * self.master_volume)
        pygame.mixer.music.set_volume(
            self.bgm_volume * self.master_volume
        )

    def sessize_al(self):
        """Sessiz modu toggle."""
        if self.master_volume > 0:
            self._onceki_volume = self.master_volume
            self.master_ayarla(0.0)
        else:
            self.master_ayarla(self._onceki_volume)


# =============================================================================
# Oyun Nesneleri
# =============================================================================
class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Basit gemi sekli (ucgen)
        pygame.draw.polygon(self.image, MAVI,
                            [(20, 0), (0, 40), (40, 40)])
        pygame.draw.polygon(self.image, BEYAZ,
                            [(20, 0), (0, 40), (40, 40)], 2)
        self.rect = self.image.get_rect(
            centerx=GENISLIK // 2, bottom=YUKSEKLIK - 20
        )
        self.hiz = 5
        self.can = 3
        self.son_ates = 0
        self.ates_bekleme = 250  # ms

    def update(self):
        """Oyuncu hareketini guncelle."""
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] and self.rect.right < GENISLIK:
            self.rect.x += self.hiz

    def ates_edebilir(self):
        """Ates bekleme suresi doldu mu?"""
        simdi = pygame.time.get_ticks()
        if simdi - self.son_ates >= self.ates_bekleme:
            self.son_ates = simdi
            return True
        return False


class Mermi(pygame.sprite.Sprite):
    """Oyuncu mermisi."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(SARI)
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.hiz = -8

    def update(self):
        self.rect.y += self.hiz
        if self.rect.bottom < 0:
            self.kill()


class Dusman(pygame.sprite.Sprite):
    """Basit dusman."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, KIRMIZI,
                            [(15, 30), (0, 0), (30, 0)])
        pygame.draw.polygon(self.image, BEYAZ,
                            [(15, 30), (0, 0), (30, 0)], 1)
        self.rect = self.image.get_rect(
            x=random.randint(0, GENISLIK - 30),
            y=random.randint(-100, -30)
        )
        self.hiz = random.uniform(1.5, 3.5)

    def update(self):
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


class Bonus(pygame.sprite.Sprite):
    """Bonus nesne."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YESIL, (8, 8), 8)
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz = 2

    def update(self):
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


# =============================================================================
# Ana Oyun
# =============================================================================
def main():
    """Uzay Kacisi - Ses entegrasyonlu ana oyun dongusu."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Uzay Kacisi - Ses Entegrasyonu")
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    font_buyuk = pygame.font.SysFont("Arial", 28, bold=True)

    # --- Ses yoneticisini olustur ---
    ses = SoundManager("assets/sounds")
    ses.muzik_cal("uzay_temasi.ogg")

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()
    bonuslar = pygame.sprite.Group()

    # Oyuncu
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Oyun degiskenleri
    skor = 0
    oyun_aktif = True
    dusman_zamanlayici = pygame.USEREVENT + 1
    pygame.time.set_timer(dusman_zamanlayici, 800)

    print("[BILGI] Uzay Kacisi - Ses Entegrasyonlu")
    print("[BILGI] SPACE: Ates | M: Sessiz | ESC: Cikis")
    print("[BILGI] Ses dosyalari olmadan demo modunda calisir.\n")

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                # --- Ses: M tusu ile sessiz modu ---
                elif olay.key == pygame.K_m:
                    ses.sessize_al()
                    durum = "SESSIZ" if ses.master_volume == 0 else "ACIK"
                    print(f"[SES] Ses modu: {durum}")

                # --- Ses: Ates etme ---
                elif olay.key == pygame.K_SPACE and oyun_aktif:
                    if oyuncu.ates_edebilir():
                        mermi = Mermi(oyuncu.rect.centerx, oyuncu.rect.top)
                        mermiler.add(mermi)
                        tum_spritelar.add(mermi)
                        ses.cal("ates")  # [SES] Ates sesi

            # Dusman olusturma zamanlayicisi
            elif olay.type == dusman_zamanlayici and oyun_aktif:
                dusman = Dusman()
                dusmanlar.add(dusman)
                tum_spritelar.add(dusman)

        if oyun_aktif:
            # Guncelle
            tum_spritelar.update()

            # --- Carpisma: Mermi <-> Dusman ---
            vurulanlar = pygame.sprite.groupcollide(
                mermiler, dusmanlar, True, True
            )
            for mermi, dusman_listesi in vurulanlar.items():
                for d in dusman_listesi:
                    skor += 100
                    ses.cal("patlama")  # [SES] Patlama sesi
                    # %20 ihtimalle bonus birak
                    if random.random() < 0.2:
                        bonus = Bonus(d.rect.centerx, d.rect.centery)
                        bonuslar.add(bonus)
                        tum_spritelar.add(bonus)

            # --- Carpisma: Oyuncu <-> Dusman ---
            carpisanlar = pygame.sprite.spritecollide(
                oyuncu, dusmanlar, True
            )
            if carpisanlar:
                oyuncu.can -= len(carpisanlar)
                ses.cal("hasar")  # [SES] Hasar sesi
                if oyuncu.can <= 0:
                    oyun_aktif = False
                    ses.muzik_durdur(fade_ms=2000)  # [SES] Muzik fade out
                    ses.cal("oyun_bitti")  # [SES] Oyun bitti sesi
                    print(f"[OYUN BITTI] Skor: {skor}")

            # --- Carpisma: Oyuncu <-> Bonus ---
            alinan_bonuslar = pygame.sprite.spritecollide(
                oyuncu, bonuslar, True
            )
            if alinan_bonuslar:
                skor += 50 * len(alinan_bonuslar)
                ses.cal("bonus")  # [SES] Bonus sesi

        # --- Cizim ---
        ekran.fill((10, 10, 30))

        # Yildizlar (basit arka plan)
        for _ in range(3):
            x = random.randint(0, GENISLIK)
            y = random.randint(0, YUKSEKLIK)
            pygame.draw.circle(ekran, (100, 100, 100), (x, y), 1)

        tum_spritelar.draw(ekran)

        # HUD
        skor_metin = font.render(f"Skor: {skor}", True, BEYAZ)
        ekran.blit(skor_metin, (10, 10))

        can_metin = font.render(f"Can: {'*' * max(0, oyuncu.can)}", True, KIRMIZI)
        ekran.blit(can_metin, (10, 35))

        ses_durum = "SESSIZ" if ses.master_volume == 0 else f"{ses.master_volume:.0%}"
        ses_metin = font.render(f"Ses: {ses_durum} (M)", True, (150, 150, 150))
        ekran.blit(ses_metin, (GENISLIK - 160, 10))

        if not oyun_aktif:
            bitti_metin = font_buyuk.render("OYUN BITTI", True, KIRMIZI)
            ekran.blit(bitti_metin, (
                GENISLIK // 2 - bitti_metin.get_width() // 2,
                YUKSEKLIK // 2 - 20
            ))
            skor_son = font.render(f"Final Skor: {skor}", True, BEYAZ)
            ekran.blit(skor_son, (
                GENISLIK // 2 - skor_son.get_width() // 2,
                YUKSEKLIK // 2 + 20
            ))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
600x700 boyutunda Uzay Kacisi oyunu acilir.
Oyuncu (mavi ucgen) sol/sag ok tuslariyla hareket eder.
SPACE ile ates eder (SFX sesi calinir).
Dusmanlar (kirmizi ucgenler) yukaridan asagi iner.
Mermi dusmana isabet edince patlama sesi calinir.
Dusman oyuncuya carparsa hasar sesi calinir.
M tusu sessiz modu acip kapatir.
Oyun bittiginde muzik fade out olur.
"""
