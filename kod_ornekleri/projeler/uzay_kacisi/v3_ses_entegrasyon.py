"""
Uzay Kacisi v3 - Tam Ses Entegrasyonu

Uzay Kacisi serisinin nihai versiyonu. v2'deki tum ozelliklerin
(dusmanlar, mermiler, carpisma, can, skor) uzerine SoundManager
sinifi ile merkezi ses yonetimi, SFX efektleri, arka plan muzigi,
sessiz modu ve bonus nesneleri eklenmistir.

Ogrenilecek kavramlar:
- SoundManager sinifi tasarimi ve oyuna entegrasyonu
- Programatik ses olusturma (dosya olmadan fallback)
- Oyun olaylarina ses baglama (ates, patlama, hasar, bonus)
- Muzik ve SFX birlestirme
- Sessiz modu (M tusu) ve volume kontrolu
- Kanal bazli ses yonetimi
- Bonus (guc artirici) nesneleri

Bolum: 07 - Ses ve Muzik
Unite: 2-4 - Ses Efektleri ve Ses Tasarimi Prensipleri

Calistirma: python v3_ses_entegrasyon.py
            uv run v3_ses_entegrasyon.py
Gereksinimler: pygame-ce

Not: Ses ve gorsel dosyalari olmadan geometrik sekiller ve
programatik sesler ile calisir.
"""

import pygame
import random
import array
import os
import sys


# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Kacisi v3 - Ses Entegrasyonu"

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
MERMI_BEKLEME = 200  # milisaniye

# Yildiz ayarlari
YILDIZ_SAYISI = 80

# Bonus ayarlari
BONUS_SPAWN_MS = 5000  # milisaniye
BONUS_CAN = 15
BONUS_PUAN = 50


# --- Ses Yardimcilari ---
def ses_dalgasi_olustur(frekans=440, sure_ms=200, ampl=3000):
    """Basit kare dalga ses olustur (dosya olmadan fallback).

    Args:
        frekans: Ses frekansi (Hz).
        sure_ms: Ses suresi (milisaniye).
        ampl: Genlik (ses siddeti).

    Returns:
        pygame.mixer.Sound: Olusturulan ses nesnesi.
    """
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


# =========================================================================
# SoundManager Sinifi
# =========================================================================
class SoundManager:
    """Merkezi ses yonetim sinifi.

    SFX ve muzik islemlerini tek bir noktadan yonetir.
    Ses dosyalari bulunamazsa programatik sesler olusturur.
    """

    def __init__(self, ses_dizini="assets/sounds"):
        self.master_volume = 1.0
        self.sfx_volume = 0.75
        self.bgm_volume = 0.40
        self._onceki_volume = 1.0
        self.sesler = {}
        self.ses_dizini = ses_dizini
        self._sesleri_yukle()

    def _sesleri_yukle(self):
        """SFX seslerini yukle. Dosya yoksa programatik olustur."""
        sfx_dosyalari = {
            "ates": "sfx/ates.ogg",
            "patlama": "sfx/patlama.ogg",
            "hasar": "sfx/hasar.ogg",
            "bonus": "sfx/bonus.ogg",
        }

        # Fallback ses parametreleri
        fallback = {
            "ates": (880, 100, 2000),
            "patlama": (100, 300, 4000),
            "hasar": (200, 250, 3500),
            "bonus": (660, 400, 2500),
        }

        for ad, dosya in sfx_dosyalari.items():
            yol = os.path.join(self.ses_dizini, dosya)
            if os.path.exists(yol):
                self.sesler[ad] = pygame.mixer.Sound(yol)
            else:
                # Dosya yoksa programatik ses olustur
                frek, sure, amp = fallback[ad]
                self.sesler[ad] = ses_dalgasi_olustur(frek, sure, amp)

            self.sesler[ad].set_volume(
                self.sfx_volume * self.master_volume
            )

    def cal(self, ad, dongu=0):
        """SFX sesi cal.

        Args:
            ad: Ses efekti adi ("ates", "patlama", vb.).
            dongu: Tekrar sayisi (0 = bir kez cal).
        """
        ses = self.sesler.get(ad)
        if ses:
            ses.play(loops=dongu)

    def muzik_cal(self, dosya, dongu=-1, fade_ms=1000):
        """Arka plan muzigini cal.

        Args:
            dosya: Muzik dosyasi adi.
            dongu: Tekrar sayisi (-1 = sonsuz).
            fade_ms: Fade in suresi (ms).
        """
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
        """Master volume ayarla (0.0 - 1.0).

        Args:
            deger: Hedef ses seviyesi.
        """
        self.master_volume = max(0.0, min(1.0, deger))
        for ses in self.sesler.values():
            ses.set_volume(self.sfx_volume * self.master_volume)
        pygame.mixer.music.set_volume(
            self.bgm_volume * self.master_volume
        )

    def sessize_al(self):
        """Sessiz modu toggle (ac/kapat)."""
        if self.master_volume > 0:
            self._onceki_volume = self.master_volume
            self.master_ayarla(0.0)
        else:
            self.master_ayarla(self._onceki_volume)

    def tumu_durdur(self):
        """Tum ses efektlerini durdur."""
        for ses in self.sesler.values():
            ses.stop()


# --- Gorsel Yardimcilari ---
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


# =========================================================================
# Sprite Siniflari
# =========================================================================
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
        self.hasar = 25

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


class Bonus(pygame.sprite.Sprite):
    """Can yenileyen bonus nesnesi (guc artirici).

    Dusman yok edildiginde %20 olasilikla veya
    zamanlayici ile olusur. Yesil daire seklinde.
    """

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YESIL, (10, 10), 10)
        pygame.draw.circle(self.image, BEYAZ, (10, 10), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz = 2

    def update(self):
        """Asagi dogru hareket et."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
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


# =========================================================================
# HUD Fonksiyonlari
# =========================================================================
def hud_ciz(ekran, font, skor, can, dusman_sayisi, ses_volume):
    """Skor, can cubugu, ses durumu ve bilgileri ekrana ciz.

    Args:
        ekran: Cizdirme yapilacak yuzey.
        font: Yazi fontu.
        skor: Oyuncu puani.
        can: Oyuncu cani.
        dusman_sayisi: Aktif dusman sayisi.
        ses_volume: Master ses seviyesi (0.0 - 1.0).
    """
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

    # Ses durumu (sag ust, can cubugunun altinda)
    if ses_volume == 0:
        ses_metin = "Ses: SESSIZ (M)"
    else:
        ses_metin = f"Ses: {ses_volume:.0%} (M)"
    ses_yazi = font.render(ses_metin, True, GRI)
    ekran.blit(ses_yazi, (cubuk_x, cubuk_y + 48))

    # Kontrol bilgisi (alt orta)
    kontrol = font.render(
        "WASD: Hareket | Space: Ates | M: Sessiz | ESC: Cikis",
        True, KOYU_GRI
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


# =========================================================================
# Oyun Yonetimi
# =========================================================================
def oyunu_baslat():
    """Oyun durumunu sifirla ve gerekli nesneleri olustur."""
    tum_spritelar = pygame.sprite.Group()
    yildizlar = pygame.sprite.Group()
    dusmanlar = pygame.sprite.Group()
    mermiler = pygame.sprite.Group()
    bonuslar = pygame.sprite.Group()

    # Yildizlari olustur
    for _ in range(YILDIZ_SAYISI):
        yildiz = Yildiz(ustten_baslat=False)
        tum_spritelar.add(yildiz)
        yildizlar.add(yildiz)

    # Oyuncuyu olustur (yildizlarin ustunde cizilsin)
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    return (tum_spritelar, yildizlar, dusmanlar,
            mermiler, bonuslar, oyuncu)


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.mixer.set_num_channels(12)

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    font_buyuk = pygame.font.Font(None, 72)

    # --- Ses yoneticisini olustur ---
    ses = SoundManager("assets/sounds")
    ses.muzik_cal("uzay_temasi.ogg")

    # --- Zamanlayicilar ---
    DUSMAN_OLAY = pygame.USEREVENT + 1
    pygame.time.set_timer(DUSMAN_OLAY, DUSMAN_SPAWN_MS)

    BONUS_OLAY = pygame.USEREVENT + 2
    pygame.time.set_timer(BONUS_OLAY, BONUS_SPAWN_MS)

    # --- Oyunu baslat ---
    (tum_spritelar, yildizlar, dusmanlar,
     mermiler, bonuslar, oyuncu) = oyunu_baslat()
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

                # Sessiz modu toggle (M tusu)
                elif olay.key == pygame.K_m:
                    ses.sessize_al()

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
                        ses.cal("ates")

                # Oyun bittiyse R ile tekrar baslat
                elif (olay.key == pygame.K_r
                      and not oyun_aktif):
                    (tum_spritelar, yildizlar, dusmanlar,
                     mermiler, bonuslar, oyuncu) = oyunu_baslat()
                    skor = 0
                    oyun_aktif = True
                    ses.muzik_cal("uzay_temasi.ogg")

            # Dusman spawn olayi
            elif olay.type == DUSMAN_OLAY and oyun_aktif:
                dusman = Dusman()
                tum_spritelar.add(dusman)
                dusmanlar.add(dusman)

            # Bonus spawn olayi (zamanlayici ile)
            elif olay.type == BONUS_OLAY and oyun_aktif:
                bonus = Bonus(
                    random.randint(20, GENISLIK - 20),
                    -20
                )
                tum_spritelar.add(bonus)
                bonuslar.add(bonus)

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
                    ses.cal("patlama")
                    # %20 olasilikla bonus birak
                    if random.random() < 0.2:
                        bonus = Bonus(
                            dusman.rect.centerx,
                            dusman.rect.centery
                        )
                        tum_spritelar.add(bonus)
                        bonuslar.add(bonus)

            # 2. Oyuncu-dusman carpismalari (spritecollide)
            if oyuncu.alive():
                vurulan_dusmanlar = pygame.sprite.spritecollide(
                    oyuncu, dusmanlar, True
                )
                for dusman in vurulan_dusmanlar:
                    oyuncu.can -= dusman.hasar
                    ses.cal("hasar")
                    if oyuncu.can <= 0:
                        oyuncu.can = 0
                        oyuncu.kill()
                        oyun_aktif = False
                        ses.muzik_durdur(fade_ms=2000)

            # 3. Oyuncu-bonus carpismalari
            if oyuncu.alive():
                alinan_bonuslar = pygame.sprite.spritecollide(
                    oyuncu, bonuslar, True
                )
                for bonus in alinan_bonuslar:
                    oyuncu.can = min(OYUNCU_CAN,
                                     oyuncu.can + BONUS_CAN)
                    skor += BONUS_PUAN
                    ses.cal("bonus")
        else:
            # Oyun bittiyse sadece yildizlari guncelle
            yildizlar.update()

        # --- Cizim ---
        ekran.fill(KOYU_MAVI)
        tum_spritelar.draw(ekran)

        # HUD
        hud_ciz(ekran, font, skor, oyuncu.can,
                len(dusmanlar), ses.master_volume)

        # Oyun bittiyse overlay
        if not oyun_aktif:
            oyun_bitti_ciz(ekran, font_buyuk, font, skor)

        pygame.display.flip()

    # --- Temizlik ---
    ses.tumu_durdur()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel Uzay Kacisi oyunu penceresi acilir.
Koyu mavi arka planda kayan yildizlar gorulur.

Ekranin altinda mavi oyuncu gemisi WASD/ok tuslari ile
dort yonde hareket ettirilir.

Yukaridan kirmizi dusman gemileri gelir (her 800 ms).
Space tusuna basinca sari mermiler yukari firlar ve
ates sesi duyulur.

Carpisma algilama ve ses:
- Mermi dusmana isabet: patlama sesi, +10 puan, %20 bonus
- Dusman oyuncuya carparsa: hasar sesi, -25 can
- Yesil bonus toplanirsa: bonus sesi, +15 can, +50 puan
- Her 5 saniyede zamanlayici ile bonus olusur

Ses kontrolleri:
- M tusu: Sessiz modu toggle
- Ses durumu HUD'da gosterilir

Can sifira dusunce "GAME OVER" ekrani cikar ve
muzik fade out olur. R tusu ile tekrar baslanabilir.

Sag ustte can cubugu (yesil->turuncu->kirmizi),
sol ustte skor ve dusman sayisi gosterilir.
"""
