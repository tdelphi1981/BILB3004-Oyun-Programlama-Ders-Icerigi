"""
Hasar Sistemi Demo - Can, Hasar ve Dokunulmazlik

Oyuncu klavye ile hareket eder, dusmanlar rastgele dolasir.
Dusmanlarla carpistiginda hasar alir ve cani azalir.
Hasar aldiktan sonra kisa sureli dokunulmazlik (invincibility)
aktif olur ve karakter yanip soner.

Ogrenilecek kavramlar:
- Sprite tabanli carpisma algilama
- Hasar ve can sistemi
- Invincibility frames (dokunulmazlik suresi)
- Yanip sonme efekti
- Can bari cizimi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 4 - Carpisma Tepkileri

Calistirma: python 02_hasar_sistemi.py
Gereksinimler: pygame
"""

import pygame
import random
import math

# --- SABITLER ---

GENISLIK = 800
YUKSEKLIK = 600
FPS = 60

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (231, 76, 60)
YESIL = (46, 204, 113)
MAVI = (52, 152, 219)
SARI = (241, 196, 15)
TURUNCU = (243, 156, 18)
KOYU_MAVI = (44, 62, 80)
GRI = (149, 165, 166)
KOYU_KIRMIZI = (192, 57, 43)
KOYU_YESIL = (39, 174, 96)

# Oyuncu ayarlari
OYUNCU_BOYUT = 36
OYUNCU_HIZ = 5
OYUNCU_MAX_CAN = 100
OYUNCU_RENK = MAVI

# Dusman ayarlari
DUSMAN_BOYUT = 28
DUSMAN_HIZ = 2
DUSMAN_SAYISI = 8
DUSMAN_RENK = KIRMIZI
DUSMAN_HASAR = 15

# Dokunulmazlik ayarlari
DOKUNULMAZLIK_SURESI = 1500  # milisaniye
YANIP_SONME_HIZI = 100  # milisaniye


# --- SINIFLAR ---

class Oyuncu(pygame.sprite.Sprite):
    """Klavye ile kontrol edilen oyuncu sprite'i."""

    def __init__(self):
        super().__init__()
        self.boyut = OYUNCU_BOYUT
        self.image = pygame.Surface(
            (self.boyut, self.boyut), pygame.SRCALPHA
        )
        self._gorsel_ciz(OYUNCU_RENK)
        self.rect = self.image.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK // 2)
        )

        # Can sistemi
        self.can = OYUNCU_MAX_CAN
        self.max_can = OYUNCU_MAX_CAN

        # Dokunulmazlik
        self.dokunulmaz = False
        self.dokunulmazlik_basi = 0
        self.gorunur = True

    def _gorsel_ciz(self, renk):
        """Oyuncu gorselini cizer (basit karakter)."""
        self.image.fill((0, 0, 0, 0))
        # Govde (kare)
        pygame.draw.rect(
            self.image, renk,
            (4, 8, self.boyut - 8, self.boyut - 8)
        )
        # Bas (daire)
        pygame.draw.circle(
            self.image, renk,
            (self.boyut // 2, 10), 10
        )
        # Gozler
        pygame.draw.circle(
            self.image, BEYAZ,
            (self.boyut // 2 - 4, 8), 3
        )
        pygame.draw.circle(
            self.image, BEYAZ,
            (self.boyut // 2 + 4, 8), 3
        )

    def update(self):
        """Klavye girdisi ve dokunulmazlik durumunu gunceller."""
        # Klavye hareketi
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= OYUNCU_HIZ
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += OYUNCU_HIZ
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            self.rect.y -= OYUNCU_HIZ
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            self.rect.y += OYUNCU_HIZ

        # Ekran sinirlari
        self.rect.clamp_ip(
            pygame.Rect(0, 0, GENISLIK, YUKSEKLIK)
        )

        # Dokunulmazlik zamanlayicisi
        if self.dokunulmaz:
            gecen_sure = (
                pygame.time.get_ticks() - self.dokunulmazlik_basi
            )
            if gecen_sure >= DOKUNULMAZLIK_SURESI:
                self.dokunulmaz = False
                self.gorunur = True
                self._gorsel_ciz(OYUNCU_RENK)
            else:
                # Yanip sonme efekti
                self.gorunur = (
                    (gecen_sure // YANIP_SONME_HIZI) % 2 == 0
                )
                if self.gorunur:
                    self._gorsel_ciz(OYUNCU_RENK)
                else:
                    self.image.fill((0, 0, 0, 0))

    def hasar_al(self, miktar):
        """Oyuncuya hasar verir ve dokunulmazlik baslatir.

        Args:
            miktar: Alinacak hasar miktari.

        Returns:
            True eger hasar alindiysa, False eger dokunulmazsa.
        """
        if self.dokunulmaz:
            return False

        self.can -= miktar
        if self.can < 0:
            self.can = 0

        # Dokunulmazlik basla
        self.dokunulmaz = True
        self.dokunulmazlik_basi = pygame.time.get_ticks()

        return True

    def hayatta_mi(self):
        """Oyuncunun hayatta olup olmadigini dondurur."""
        return self.can > 0


class Dusman(pygame.sprite.Sprite):
    """Rastgele hareket eden dusman sprite'i."""

    def __init__(self):
        super().__init__()
        self.boyut = DUSMAN_BOYUT
        self.image = pygame.Surface(
            (self.boyut, self.boyut), pygame.SRCALPHA
        )
        self._gorsel_ciz()

        # Rastgele konum (kenarlarda)
        kenar = random.choice(["sol", "sag", "ust", "alt"])
        if kenar == "sol":
            x, y = -self.boyut, random.randint(0, YUKSEKLIK)
        elif kenar == "sag":
            x, y = GENISLIK + self.boyut, random.randint(0, YUKSEKLIK)
        elif kenar == "ust":
            x, y = random.randint(0, GENISLIK), -self.boyut
        else:
            x, y = random.randint(0, GENISLIK), YUKSEKLIK + self.boyut

        self.rect = self.image.get_rect(center=(x, y))

        # Rastgele hareket yonu
        aci = random.uniform(0, 2 * math.pi)
        self.hiz_x = math.cos(aci) * DUSMAN_HIZ
        self.hiz_y = math.sin(aci) * DUSMAN_HIZ

        # Yon degistirme zamanlayicisi
        self.yon_zamani = pygame.time.get_ticks()
        self.yon_suresi = random.randint(1000, 3000)

    def _gorsel_ciz(self):
        """Dusman gorselini cizer (sivri sekil)."""
        self.image.fill((0, 0, 0, 0))
        # Bes koseli yildiz seklinde dusman
        merkez = self.boyut // 2
        noktalar = []
        for i in range(10):
            aci = math.radians(i * 36 - 90)
            if i % 2 == 0:
                r = merkez - 2
            else:
                r = merkez // 2
            x = merkez + math.cos(aci) * r
            y = merkez + math.sin(aci) * r
            noktalar.append((x, y))
        pygame.draw.polygon(self.image, DUSMAN_RENK, noktalar)

    def update(self):
        """Dusmanin rastgele hareketini gunceller."""
        simdi = pygame.time.get_ticks()

        # Belirli araliklarla yon degistir
        if simdi - self.yon_zamani > self.yon_suresi:
            aci = random.uniform(0, 2 * math.pi)
            self.hiz_x = math.cos(aci) * DUSMAN_HIZ
            self.hiz_y = math.sin(aci) * DUSMAN_HIZ
            self.yon_zamani = simdi
            self.yon_suresi = random.randint(1000, 3000)

        # Hareket
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Ekran sinirlarindan sekme
        if self.rect.left < 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x)
        if self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x)
        if self.rect.top < 0:
            self.rect.top = 0
            self.hiz_y = abs(self.hiz_y)
        if self.rect.bottom > YUKSEKLIK:
            self.rect.bottom = YUKSEKLIK
            self.hiz_y = -abs(self.hiz_y)


# --- YARDIMCI FONKSIYONLAR ---

def can_bari_ciz(ekran, x, y, genislik, yukseklik, can, max_can):
    """Ekranda can bari cizer.

    Args:
        ekran: Pygame ekran yuzeyi.
        x: Barin sol kenar x koordinati.
        y: Barin ust kenar y koordinati.
        genislik: Barin toplam genisligi.
        yukseklik: Barin yuksekligi.
        can: Mevcut can degeri.
        max_can: Maksimum can degeri.
    """
    # Can orani
    oran = max(0, can / max_can)

    # Renk gecisi: yesil -> sari -> kirmizi
    if oran > 0.5:
        # Yesil -> Sari
        gecis = (1 - (oran - 0.5) * 2)
        renk = (int(255 * gecis), 255, 0)
    else:
        # Sari -> Kirmizi
        gecis = oran * 2
        renk = (255, int(255 * gecis), 0)

    # Arka plan (koyu kirmizi)
    pygame.draw.rect(
        ekran, KOYU_KIRMIZI,
        (x, y, genislik, yukseklik)
    )
    # Dolu kisim
    dolu_genislik = int(genislik * oran)
    if dolu_genislik > 0:
        pygame.draw.rect(
            ekran, renk,
            (x, y, dolu_genislik, yukseklik)
        )
    # Cerceve
    pygame.draw.rect(
        ekran, BEYAZ,
        (x, y, genislik, yukseklik), 2
    )


def hud_ciz(ekran, font, oyuncu):
    """Ekranin ustune oyuncu bilgilerini cizer."""
    # Can bari
    bar_x = 10
    bar_y = 10
    bar_genislik = 200
    bar_yukseklik = 20

    can_yazi = font.render("CAN:", True, BEYAZ)
    ekran.blit(can_yazi, (bar_x, bar_y - 2))

    can_bari_ciz(
        ekran,
        bar_x + 50, bar_y,
        bar_genislik, bar_yukseklik,
        oyuncu.can, oyuncu.max_can
    )

    # Can degeri (sayi olarak)
    can_sayi = font.render(
        f"{oyuncu.can}/{oyuncu.max_can}", True, BEYAZ
    )
    ekran.blit(
        can_sayi,
        (bar_x + 55 + bar_genislik, bar_y - 2)
    )

    # Dokunulmazlik durumu
    if oyuncu.dokunulmaz:
        gecen = pygame.time.get_ticks() - oyuncu.dokunulmazlik_basi
        kalan_ms = max(0, DOKUNULMAZLIK_SURESI - gecen)
        kalan_sn = kalan_ms / 1000
        durum_yazi = font.render(
            f"DOKUNULMAZ: {kalan_sn:.1f}s", True, SARI
        )
        ekran.blit(durum_yazi, (bar_x, bar_y + 25))


# --- ANA OYUN ---

def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Hasar Sistemi Demo")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    buyuk_font = pygame.font.Font(None, 48)
    kucuk_font = pygame.font.Font(None, 24)

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    dusman_grubu = pygame.sprite.Group()

    # Oyuncu
    oyuncu = Oyuncu()
    tum_spritelar.add(oyuncu)

    # Dusmanlari olustur
    for _ in range(DUSMAN_SAYISI):
        dusman = Dusman()
        dusman_grubu.add(dusman)
        tum_spritelar.add(dusman)

    # Oyun durumu
    calistir = True
    oyun_bitti = False
    hasar_mesajlari = []  # (mesaj, zaman, konum) listesi

    while calistir:
        saat.tick(FPS)

        # --- OLAYLAR ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_r and oyun_bitti:
                    # Oyunu yeniden baslat
                    tum_spritelar.empty()
                    dusman_grubu.empty()
                    oyuncu = Oyuncu()
                    tum_spritelar.add(oyuncu)
                    for _ in range(DUSMAN_SAYISI):
                        dusman = Dusman()
                        dusman_grubu.add(dusman)
                        tum_spritelar.add(dusman)
                    oyun_bitti = False
                    hasar_mesajlari.clear()

        if oyun_bitti:
            # Oyun bitti ekrani
            ekran.fill(KOYU_MAVI)
            bitti_yazi = buyuk_font.render(
                "OYUN BITTI!", True, KIRMIZI
            )
            devam_yazi = font.render(
                "R ile yeniden basla  |  ESC ile cikis", True, GRI
            )
            ekran.blit(
                bitti_yazi,
                bitti_yazi.get_rect(
                    center=(GENISLIK // 2, YUKSEKLIK // 2 - 20)
                )
            )
            ekran.blit(
                devam_yazi,
                devam_yazi.get_rect(
                    center=(GENISLIK // 2, YUKSEKLIK // 2 + 30)
                )
            )
            pygame.display.flip()
            continue

        # --- GUNCELLEME ---
        tum_spritelar.update()

        # Carpisma kontrolu: oyuncu - dusman
        carpisan_dusmanlar = pygame.sprite.spritecollide(
            oyuncu, dusman_grubu, False
        )
        for dusman in carpisan_dusmanlar:
            hasar_alindi = oyuncu.hasar_al(DUSMAN_HASAR)
            if hasar_alindi:
                # Hasar mesaji ekle
                mesaj = f"-{DUSMAN_HASAR}"
                hasar_mesajlari.append(
                    (mesaj, pygame.time.get_ticks(), list(oyuncu.rect.midtop))
                )

        # Oyuncu oldu mu?
        if not oyuncu.hayatta_mi():
            oyun_bitti = True

        # Hasar mesajlarini guncelle (yukari kaydir, sure dolunca sil)
        simdi = pygame.time.get_ticks()
        guncellenmis = []
        for mesaj, zaman, konum in hasar_mesajlari:
            if simdi - zaman < 1000:  # 1 saniye gorunur
                konum[1] -= 1  # Yukari kaydir
                guncellenmis.append((mesaj, zaman, konum))
        hasar_mesajlari = guncellenmis

        # --- CIZIM ---
        ekran.fill(KOYU_MAVI)

        # Sprite'lari ciz
        for sprite in tum_spritelar:
            if sprite == oyuncu and not oyuncu.gorunur:
                continue  # Yanip sonme: gorunmez karede cizme
            ekran.blit(sprite.image, sprite.rect)

        # Hasar mesajlarini ciz
        for mesaj, zaman, konum in hasar_mesajlari:
            gecen = simdi - zaman
            alfa = max(0, 255 - int(gecen * 255 / 1000))
            hasar_yuzey = font.render(mesaj, True, KIRMIZI)
            hasar_yuzey.set_alpha(alfa)
            ekran.blit(hasar_yuzey, konum)

        # HUD
        hud_ciz(ekran, font, oyuncu)

        # Kontrol bilgisi
        kontrol_yazi = kucuk_font.render(
            "WASD/Ok tuslari: Hareket  |  R: Yeniden basla  |  ESC: Cikis",
            True, GRI
        )
        ekran.blit(
            kontrol_yazi,
            kontrol_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK - 20)
            )
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu mavi arka planli bir pencere acilir.
Ortada mavi bir oyuncu karakteri ve etrafta kirmizi yildiz seklinde
8 dusman bulunur.

Oyuncu hareketi:
- WASD veya ok tuslari ile dort yone hareket edebilir

Hasar mekanigi:
- Bir dusmana dokunuldugunda -15 hasar alinir
- Hasar aldiginda kirmizi "-15" yazisi yukari kayarak solar
- Sol ustteki can bari azalir (yesil -> sari -> kirmizi gecisi)
- Can barinin yaninda sayi olarak can degeri gosterilir

Dokunulmazlik:
- Hasar aldiktan sonra 1.5 saniye dokunulmazlik baslar
- Bu surede karakter yanip soner (gorunur/gorunmez)
- "DOKUNULMAZ: X.Xs" yazisi gosterilir
- Dokunulmazlik bitene kadar yeni hasar alinamaz

Can sifirlandiginda "OYUN BITTI!" ekrani gosterilir.
R tusu ile oyun yeniden baslatilabilir.
"""
