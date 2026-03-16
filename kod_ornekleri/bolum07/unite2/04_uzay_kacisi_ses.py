"""
Uzay Kacisi - Ses Efektleri Entegrasyonu

Bu program Uzay Kacisi projesine ses efektleri ekler:
mermi atesleme, patlama, guc toplama ve hasar sesleri.

Ogrenilecek kavramlar:
- SesYoneticisi sinifi tasarimi
- Oyun olaylarina ses baglanma
- Ses seviyesi dengeleme (mixing)
- Kanal bazli ses yonetimi

Bolum: 07 - Ses ve Muzik
Unite: 2 - Ses Efektleri

Calistirma: python 04_uzay_kacisi_ses.py
Gereksinimler: pygame
"""

import pygame
import random
import array

# Sabitler
GENISLIK = 600
YUKSEKLIK = 700
BASLIK = "Uzay Kacisi - Ses Efektleri"
FPS = 60
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)


def ses_olustur(frekans=440, sure_ms=200, ampl=3000):
    """Basit test ses dalgasi olustur."""
    ornekleme = 44100
    ornek_sayisi = int(ornekleme * sure_ms / 1000)
    buf = array.array('h')
    periyot = max(1, int(ornekleme / frekans))

    for i in range(ornek_sayisi):
        # Zaman icerisinde azalan genlik (zarf)
        zarf = 1.0 - (i / ornek_sayisi)
        deger = int(ampl * zarf)
        if (i % periyot) < (periyot // 2):
            buf.append(deger)
        else:
            buf.append(-deger)

    return pygame.mixer.Sound(buffer=buf)


# ---------------------------------------------------------------------------
# SES YONETICISI
# ---------------------------------------------------------------------------
class SesYoneticisi:
    """Oyun ses efektlerini yoneten sinif."""

    def __init__(self):
        """Ses efektlerini yukle ve yapilandir."""
        # Programatik sesler olustur (gercek projede dosyadan yuklersin)
        self.sesler = {
            "lazer": ses_olustur(frekans=880, sure_ms=100, ampl=2000),
            "patlama": ses_olustur(frekans=100, sure_ms=300, ampl=4000),
            "powerup": ses_olustur(frekans=660, sure_ms=400, ampl=2500),
            "hasar": ses_olustur(frekans=200, sure_ms=250, ampl=3500),
        }

        # Ses seviyeleri
        self.sesler["lazer"].set_volume(0.3)
        self.sesler["patlama"].set_volume(0.5)
        self.sesler["powerup"].set_volume(0.4)
        self.sesler["hasar"].set_volume(0.6)

    def cal(self, ses_adi):
        """Belirtilen ses efektini cal."""
        if ses_adi in self.sesler:
            self.sesler[ses_adi].play()

    def tumu_durdur(self):
        """Tum ses efektlerini durdur."""
        for ses in self.sesler.values():
            ses.stop()


# ---------------------------------------------------------------------------
# OYUNCU
# ---------------------------------------------------------------------------
class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi."""

    def __init__(self, ses_yon):
        super().__init__()
        # Basit gemi sekli
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (50, 200, 255),
                            [(20, 0), (0, 40), (40, 40)])
        self.rect = self.image.get_rect(centerx=GENISLIK // 2, bottom=YUKSEKLIK - 20)
        self.hiz = 5
        self.can = 100
        self.ses = ses_yon
        self.son_ates = 0
        self.ates_bekleme = 250  # ms

    def update(self):
        """Oyuncu hareketini guncelle."""
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] and self.rect.right < GENISLIK:
            self.rect.x += self.hiz

    def ates_et(self, mermi_grubu):
        """Mermi atesle ve ses cal."""
        simdi = pygame.time.get_ticks()
        if simdi - self.son_ates >= self.ates_bekleme:
            mermi = Mermi(self.rect.centerx, self.rect.top)
            mermi_grubu.add(mermi)
            self.ses.cal("lazer")
            self.son_ates = simdi


# ---------------------------------------------------------------------------
# MERMI
# ---------------------------------------------------------------------------
class Mermi(pygame.sprite.Sprite):
    """Oyuncu mermisi."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 0), (0, 0, 4, 12))
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.hiz = -8

    def update(self):
        """Mermiyi yukari hareket ettir."""
        self.rect.y += self.hiz
        if self.rect.bottom < 0:
            self.kill()


# ---------------------------------------------------------------------------
# DUSMAN
# ---------------------------------------------------------------------------
class Dusman(pygame.sprite.Sprite):
    """Dusman gemisi."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 50, 50),
                            [(15, 30), (0, 0), (30, 0)])
        self.rect = self.image.get_rect(
            x=random.randint(0, GENISLIK - 30),
            y=random.randint(-100, -30)
        )
        self.hiz = random.uniform(1.5, 3.5)
        self.puan = 10
        self.hasar = 20

    def update(self):
        """Dusmani asagi hareket ettir."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


# ---------------------------------------------------------------------------
# GUC ARTIRICI
# ---------------------------------------------------------------------------
class GucArtirici(pygame.sprite.Sprite):
    """Guc artirici (power-up)."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 100), (10, 10), 10)
        pygame.draw.circle(self.image, (200, 255, 200), (10, 10), 5)
        self.rect = self.image.get_rect(
            x=random.randint(0, GENISLIK - 20),
            y=random.randint(-200, -50)
        )
        self.hiz = 2

    def update(self):
        """Guc artiriciyi asagi hareket ettir."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


# ---------------------------------------------------------------------------
# ANA OYUN
# ---------------------------------------------------------------------------
def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    pygame.mixer.set_num_channels(12)

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    # Ses yoneticisi
    ses_yon = SesYoneticisi()

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()
    gucler = pygame.sprite.Group()

    # Oyuncu
    oyuncu = Oyuncu(ses_yon)
    tum_spritelar.add(oyuncu)

    # Dusman olusturma zamanlayicisi
    DUSMAN_OLAY = pygame.USEREVENT + 1
    pygame.time.set_timer(DUSMAN_OLAY, 1000)

    # Guc artirici zamanlayicisi
    GUC_OLAY = pygame.USEREVENT + 2
    pygame.time.set_timer(GUC_OLAY, 5000)

    skor = 0

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
            elif olay.type == DUSMAN_OLAY:
                dusman = Dusman()
                tum_spritelar.add(dusman)
                dusmanlar.add(dusman)
            elif olay.type == GUC_OLAY:
                guc = GucArtirici()
                tum_spritelar.add(guc)
                gucler.add(guc)

        # Ates etme (SPACE basili tutulursa)
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_SPACE]:
            oyuncu.ates_et(mermiler)
            # Mermileri gruplara ekle
            for m in mermiler:
                if m not in tum_spritelar:
                    tum_spritelar.add(m)

        # Guncelleme
        tum_spritelar.update()

        # --- CARPISMA KONTROLLERI ---

        # Mermi-dusman carpismasi
        carpisma_mermi = pygame.sprite.groupcollide(mermiler, dusmanlar, True, True)
        for mermi, vurulanlar in carpisma_mermi.items():
            for dusman in vurulanlar:
                ses_yon.cal("patlama")
                skor += dusman.puan

        # Oyuncu-guc artirici carpismasi
        toplanan = pygame.sprite.spritecollide(oyuncu, gucler, True)
        for guc in toplanan:
            ses_yon.cal("powerup")
            oyuncu.can = min(100, oyuncu.can + 15)

        # Oyuncu-dusman carpismasi
        dusman_carpisma = pygame.sprite.spritecollide(oyuncu, dusmanlar, True)
        for dusman in dusman_carpisma:
            ses_yon.cal("hasar")
            oyuncu.can -= dusman.hasar

        # Can kontrolu
        if oyuncu.can <= 0:
            calistir = False

        # --- CIZIM ---
        ekran.fill((10, 10, 30))

        # Yildizlar (basit)
        for _ in range(2):
            x = random.randint(0, GENISLIK)
            y = random.randint(0, YUKSEKLIK)
            ekran.set_at((x, y), (200, 200, 200))

        tum_spritelar.draw(ekran)

        # HUD
        skor_metin = font.render(f"Skor: {skor}", True, BEYAZ)
        can_metin = font.render(f"Can: {oyuncu.can}", True,
                                (0, 255, 0) if oyuncu.can > 30 else (255, 50, 50))
        ekran.blit(skor_metin, (10, 10))
        ekran.blit(can_metin, (10, 35))

        # Kontrol bilgisi
        bilgi = font.render("OK: Hareket | SPACE: Ates | ESC: Cikis", True, (120, 120, 120))
        ekran.blit(bilgi, (10, YUKSEKLIK - 25))

        pygame.display.flip()
        saat.tick(FPS)

    # Oyun bitti
    ses_yon.tumu_durdur()
    pygame.quit()
    print(f"Oyun bitti! Son skor: {skor}")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
600x700 piksel bir uzay oyunu penceresi acilir.
- Ok tuslari ile gemi saga/sola hareket eder
- SPACE ile mermi atesler (lazer sesi)
- Dusmanlara mermi isabet edince patlama sesi duyulur
- Yesil guc artiricilar toplaninca powerup sesi calar
- Dusman gemiye carpinca hasar sesi calar ve can azalir
- Can 0'a dusunce oyun biter ve skor yazdirilir
"""
