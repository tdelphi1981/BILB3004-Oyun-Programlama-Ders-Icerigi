"""
Breakout (Tugla Kirma) - Yan Proje

Klasik Breakout oyununun PyGame ile uygulamasi.
Raket, top ve tuglalardan olusan bu oyun,
Bolum 6'daki tum kavramlari birlestiren bir projedir.

Ogrenilecek kavramlar:
- Rect tabanli carpisma algilama
- Geri sekme mekanigi ve hiz vektorleri
- Hasar ve can sistemi
- Sprite yok etme ve patlama efekti
- Skor sistemi ve combo mekanigi

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 4 - Carpisma Tepkileri

Calistirma: python 04_breakout.py
Gereksinimler: pygame
"""

import pygame
import random
import math

# --- SABITLER ---

# Ekran
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (231, 76, 60)
TURUNCU = (243, 156, 18)
SARI = (241, 196, 15)
YESIL = (46, 204, 113)
MAVI = (52, 152, 219)
MOR = (155, 89, 182)
GRI = (149, 165, 166)
KOYU_MAVI = (44, 62, 80)

# Raket
RAKET_GENISLIK = 100
RAKET_YUKSEKLIK = 12
RAKET_HIZ = 8
RAKET_RENK = MAVI

# Top
TOP_YARICAP = 8
TOP_HIZ = 5
TOP_RENK = BEYAZ

# Tugla
TUGLA_GENISLIK = 70
TUGLA_YUKSEKLIK = 25
TUGLA_BOSLUK = 4
TUGLA_SATIR = 6
TUGLA_SUTUN = 10
TUGLA_UST_BOSLUK = 60

# Tugla turleri: (renk, can)
TUGLA_TURLERI = {
    1: (SARI, 1),       # Sari: 1 vurus
    2: (TURUNCU, 1),     # Turuncu: 1 vurus
    3: (KIRMIZI, 2),     # Kirmizi: 2 vurus
    4: (MOR, 2),         # Mor: 2 vurus
    5: (MAVI, 3),        # Mavi: 3 vurus
    6: (GRI, -1),        # Gri: kirilamaz
}


# --- SINIFLAR ---

class Raket(pygame.sprite.Sprite):
    """Oyuncu tarafindan kontrol edilen raket."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((RAKET_GENISLIK, RAKET_YUKSEKLIK))
        self.image.fill(RAKET_RENK)
        # Raketin ust kenarinda acik mavi bir cizgi
        pygame.draw.rect(self.image, BEYAZ,
                        (0, 0, RAKET_GENISLIK, 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 30
        self.hiz = RAKET_HIZ

    def update(self):
        """Klavye girdisiyle raketi hareket ettirir."""
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += self.hiz

        # Ekran sinirlari
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > GENISLIK:
            self.rect.right = GENISLIK


class Top(pygame.sprite.Sprite):
    """Ekranda hareket eden ve yuzeylerden seken top."""

    def __init__(self, raket):
        super().__init__()
        self.image = pygame.Surface(
            (TOP_YARICAP * 2, TOP_YARICAP * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, TOP_RENK,
            (TOP_YARICAP, TOP_YARICAP), TOP_YARICAP
        )
        self.rect = self.image.get_rect()
        self.raket = raket

        # Baslangic: raket ustunde, hareketsiz
        self.rect.midbottom = self.raket.rect.midtop
        self.hiz_x = 0
        self.hiz_y = 0
        self.aktif = False  # Space ile firlatilacak
        self.dustu = False  # Can kaybi kontrolu

    def firlat(self):
        """Topu rastgele bir acida yukari firlatir."""
        if not self.aktif:
            self.aktif = True
            self.dustu = False
            # 220-320 derece arasi (yukari dogru)
            aci = random.uniform(math.radians(220), math.radians(320))
            self.hiz_x = TOP_HIZ * math.cos(aci)
            self.hiz_y = TOP_HIZ * math.sin(aci)

    def update(self):
        """Topun hareketini ve duvar carpismasini isler."""
        if not self.aktif:
            # Raket ustunde bekle
            self.rect.midbottom = self.raket.rect.midtop
            return

        # Hareketi uygula
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Sol duvar
        if self.rect.left <= 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x)

        # Sag duvar
        elif self.rect.right >= GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x)

        # Ust duvar
        if self.rect.top <= 0:
            self.rect.top = 0
            self.hiz_y = abs(self.hiz_y)

        # Alt kenar: top dustu (can kaybi)
        if self.rect.top > YUKSEKLIK:
            self.aktif = False
            self.dustu = True
            self.rect.midbottom = self.raket.rect.midtop
            self.hiz_x = 0
            self.hiz_y = 0


class Tugla(pygame.sprite.Sprite):
    """Topun kirabilecegi tugla."""

    def __init__(self, x, y, tur=1):
        super().__init__()
        renk, self.can = TUGLA_TURLERI.get(tur, (BEYAZ, 1))
        self.max_can = self.can
        self.renk = renk
        self.puan = tur * 10

        self.image = pygame.Surface((TUGLA_GENISLIK, TUGLA_YUKSEKLIK))
        self._gorsel_guncelle()
        self.rect = self.image.get_rect(topleft=(x, y))

    def _gorsel_guncelle(self):
        """Can durumuna gore gorseli gunceller."""
        self.image.fill(self.renk)
        # Kenarlik
        pygame.draw.rect(
            self.image, BEYAZ,
            (0, 0, TUGLA_GENISLIK, TUGLA_YUKSEKLIK), 1
        )
        # Hasar almissa catlak efekti
        if self.max_can > 1 and self.can < self.max_can:
            oran = self.can / self.max_can
            if oran <= 0.5:
                # Agir hasar: capraz cizgi
                pygame.draw.line(self.image, SIYAH,
                               (5, 5),
                               (TUGLA_GENISLIK - 5,
                                TUGLA_YUKSEKLIK - 5), 2)
            # Hafif hasar: kucuk cizgi
            pygame.draw.line(self.image, SIYAH,
                           (TUGLA_GENISLIK // 3, 3),
                           (TUGLA_GENISLIK // 2,
                            TUGLA_YUKSEKLIK - 3), 1)

    def hasar_al(self):
        """Tuglaya hasar verir. Kirilip kirilmadigini dondurur."""
        if self.can == -1:
            return False  # Kirilamaz tugla

        self.can -= 1
        if self.can <= 0:
            self.kill()
            return True  # Kirildi

        self._gorsel_guncelle()
        return False  # Hala saglam


class Parcacik(pygame.sprite.Sprite):
    """Patlama efekti icin kucuk parcacik."""

    def __init__(self, merkez, renk=TURUNCU):
        super().__init__()
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self.image, renk, (2, 2), 2)
        self.rect = self.image.get_rect(center=merkez)

        # Rastgele yon ve hiz
        aci = random.uniform(0, 2 * math.pi)
        hiz = random.uniform(2, 6)
        self.hiz_x = math.cos(aci) * hiz
        self.hiz_y = math.sin(aci) * hiz

        self.omur = random.randint(15, 30)  # Kare sayisi

    def update(self):
        """Parcacigi hareket ettirir ve omrunu azaltir."""
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y
        self.hiz_y += 0.1  # Hafif yercekimi
        self.omur -= 1
        if self.omur <= 0:
            self.kill()


class SkorYoneticisi:
    """Skor ve combo sistemini yonetir."""

    def __init__(self):
        self.skor = 0
        self.en_yuksek = 0
        self.combo = 0
        self.combo_zamani = 0
        self.combo_suresi = 2000  # ms

    def puan_ekle(self, puan):
        """Puan ekler ve combo kontrolu yapar."""
        simdi = pygame.time.get_ticks()

        # Combo kontrolu
        if simdi - self.combo_zamani < self.combo_suresi:
            self.combo += 1
        else:
            self.combo = 0

        self.combo_zamani = simdi

        # Combo carpani
        carpan = 1 + self.combo * 0.5
        kazanilan = int(puan * carpan)
        self.skor += kazanilan

        if self.skor > self.en_yuksek:
            self.en_yuksek = self.skor

        return kazanilan, self.combo + 1

    def sifirla(self):
        """Yeni oyun icin skoru sifirlar."""
        self.skor = 0
        self.combo = 0


# --- YARDIMCI FONKSIYONLAR ---

def patlama_olustur(merkez, patlama_grubu, parcacik_sayisi=12):
    """Belirtilen konumda parcacik patlamasi olusturur."""
    renkler = [BEYAZ, SARI, TURUNCU, KIRMIZI]
    for _ in range(parcacik_sayisi):
        renk = random.choice(renkler)
        parcacik = Parcacik(merkez, renk)
        patlama_grubu.add(parcacik)


def tuglalari_olustur(tugla_grubu, tum_spritelar):
    """Tugla gridini olusturur."""
    toplam_genislik = (
        TUGLA_SUTUN * (TUGLA_GENISLIK + TUGLA_BOSLUK) - TUGLA_BOSLUK
    )
    baslangic_x = (GENISLIK - toplam_genislik) // 2

    for satir in range(TUGLA_SATIR):
        for sutun in range(TUGLA_SUTUN):
            x = baslangic_x + sutun * (TUGLA_GENISLIK + TUGLA_BOSLUK)
            y = TUGLA_UST_BOSLUK + satir * (
                TUGLA_YUKSEKLIK + TUGLA_BOSLUK
            )

            # Ust satirlar daha guclu
            tur = TUGLA_SATIR - satir
            tugla = Tugla(x, y, tur)
            tugla_grubu.add(tugla)
            tum_spritelar.add(tugla)


def raket_top_carpismasi(top, raket):
    """Topun raketten sekme acisini hesaplar."""
    if not top.aktif:
        return

    if top.rect.colliderect(raket.rect) and top.hiz_y > 0:
        # Carpisma noktasinin raket uzerindeki orani
        carpisma_noktasi = (
            (top.rect.centerx - raket.rect.left) / raket.rect.width
        )
        # -1.0 ile 1.0 arasina cevir
        oran = carpisma_noktasi * 2 - 1

        # Sekme acisi: 150 derece (sol) ile 30 derece (sag)
        aci = math.radians(150 - oran * 60)

        # Mevcut hizi koru, yonu degistir
        hiz = math.sqrt(top.hiz_x**2 + top.hiz_y**2)
        top.hiz_x = hiz * math.cos(aci)
        top.hiz_y = -abs(hiz * math.sin(aci))

        # Topu raketin ustune yerlestir
        top.rect.bottom = raket.rect.top


def top_tugla_carpismasi(top, tugla_grubu, patlama_grubu, skor_yon):
    """Top-tugla carpismasini isler."""
    if not top.aktif:
        return

    carpisan = pygame.sprite.spritecollide(top, tugla_grubu, False)

    for tugla in carpisan:
        # Carpisma yonunu belirle
        dx = top.rect.centerx - tugla.rect.centerx
        dy = top.rect.centery - tugla.rect.centery

        # Yatay mi dikey mi carpisma?
        if abs(dx) / tugla.rect.width > abs(dy) / tugla.rect.height:
            top.hiz_x = -top.hiz_x
        else:
            top.hiz_y = -top.hiz_y

        # Tuglaya hasar ver
        kirildi = tugla.hasar_al()
        if kirildi:
            patlama_olustur(tugla.rect.center, patlama_grubu, 8)
            skor_yon.puan_ekle(tugla.puan)

        break  # Bir karede tek tugla carpismasi isle


# --- ANA OYUN ---

def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Breakout - Tugla Kirma")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    kucuk_font = pygame.font.Font(None, 28)

    # Sprite gruplari
    tum_spritelar = pygame.sprite.Group()
    tugla_grubu = pygame.sprite.Group()
    patlama_grubu = pygame.sprite.Group()

    # Nesneler
    raket = Raket()
    top = Top(raket)
    tum_spritelar.add(raket, top)

    # Tuglalari olustur
    tuglalari_olustur(tugla_grubu, tum_spritelar)

    # Oyun durum degiskenleri
    skor_yon = SkorYoneticisi()
    canlar = 3
    calistir = True
    oyun_bitti = False
    kazandi = False

    while calistir:
        saat.tick(FPS)

        # --- OLAYLAR ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_SPACE:
                    if oyun_bitti:
                        # Yeni oyun baslat
                        tum_spritelar.empty()
                        tugla_grubu.empty()
                        patlama_grubu.empty()
                        raket = Raket()
                        top = Top(raket)
                        tum_spritelar.add(raket, top)
                        tuglalari_olustur(tugla_grubu, tum_spritelar)
                        skor_yon.sifirla()
                        canlar = 3
                        oyun_bitti = False
                        kazandi = False
                    else:
                        top.firlat()
                elif olay.key == pygame.K_ESCAPE:
                    calistir = False

        if oyun_bitti:
            # Oyun bitti ekrani
            ekran.fill(KOYU_MAVI)
            if kazandi:
                mesaj = font.render("TEBRIKLER! Tum tuglalar kirildi!",
                                   True, YESIL)
            else:
                mesaj = font.render("OYUN BITTI!", True, KIRMIZI)
            skor_mesaj = font.render(
                f"Skor: {skor_yon.skor}", True, BEYAZ
            )
            devam_mesaj = kucuk_font.render(
                "Space ile yeni oyun / ESC ile cikis", True, GRI
            )
            ekran.blit(mesaj,
                      mesaj.get_rect(center=(GENISLIK // 2,
                                            YUKSEKLIK // 2 - 40)))
            ekran.blit(skor_mesaj,
                      skor_mesaj.get_rect(center=(GENISLIK // 2,
                                                  YUKSEKLIK // 2 + 10)))
            ekran.blit(devam_mesaj,
                      devam_mesaj.get_rect(center=(GENISLIK // 2,
                                                  YUKSEKLIK // 2 + 50)))
            pygame.display.flip()
            continue

        # --- GUNCELLEME ---
        tum_spritelar.update()
        patlama_grubu.update()

        # Raket-top carpismasi
        raket_top_carpismasi(top, raket)

        # Top-tugla carpismasi
        top_tugla_carpismasi(top, tugla_grubu, patlama_grubu, skor_yon)

        # Top dustu mu?
        if top.dustu:
            top.dustu = False
            canlar -= 1
            if canlar <= 0:
                oyun_bitti = True
                kazandi = False

        # Tum tuglalar kirildi mi?
        kirilamaz = [t for t in tugla_grubu if t.can == -1]
        if len(tugla_grubu) <= len(kirilamaz):
            oyun_bitti = True
            kazandi = True

        # --- CIZIM ---
        ekran.fill(KOYU_MAVI)

        # Sprite'lari ciz
        tum_spritelar.draw(ekran)
        patlama_grubu.draw(ekran)

        # HUD: Skor
        skor_yazi = font.render(
            f"Skor: {skor_yon.skor}", True, BEYAZ
        )
        ekran.blit(skor_yazi, (10, 10))

        # HUD: Can gosterimi (kalpler yerine metin)
        can_yazi = font.render(f"Can: {canlar}", True, BEYAZ)
        ekran.blit(can_yazi, (GENISLIK - 120, 10))

        # Combo gosterimi
        if skor_yon.combo > 0:
            combo_yazi = kucuk_font.render(
                f"Combo x{skor_yon.combo + 1}!", True, SARI
            )
            ekran.blit(combo_yazi, (GENISLIK // 2 - 40, 10))

        # Baslangic mesaji
        if not top.aktif and not oyun_bitti:
            mesaj = kucuk_font.render(
                "Space ile topu firlat!", True, GRI
            )
            ekran.blit(mesaj,
                      mesaj.get_rect(center=(GENISLIK // 2,
                                            YUKSEKLIK - 60)))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu mavi arka planli bir pencere acilir.
Ekranin ustunde 6 satir, 10 sutunluk renkli tuglalar dizilir.
Altta mavi bir raket ve ustunde beyaz bir top bulunur.

Kontroller:
- Space: Topu firlat
- Sol/Sag ok tuslari veya A/D: Raketi hareket ettir
- ESC: Cikis

Oyun mekanigi:
- Top raket, duvarlar ve tuglalardan sekip tuglalari kirar
- Sari/turuncu tuglalar 1, kirmizi/mor 2, mavi 3 vurusla kirilir
- Gri tuglalar kirilamaz
- Top alttan duserse 1 can kaybolur (toplam 3 can)
- Art arda hizli vuruslar combo puani kazandirir
- Tum kirilebilir tuglalar kirildiginda oyun kazanilir
"""
