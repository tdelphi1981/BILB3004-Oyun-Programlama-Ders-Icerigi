"""
Geri Sekme Demo - Elastik Carpisma Gosterimi

Bir top ekranda hareket eder ve duvarlara carptigi anda
hiz vektoru tersine doner. Basit elastik carpisma
mekaniginin temel calisma prensibini gosterir.

Ogrenilecek kavramlar:
- Hiz vektoru ile hareket
- Duvar carpismasi algilama
- Elastik geri sekme (hiz tersine cevirme)
- Carpisma yonu belirleme (x / y ekseni)

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 4 - Carpisma Tepkileri

Calistirma: python 01_geri_sekme.py
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
KOYU_MAVI = (44, 62, 80)
GRI = (149, 165, 166)
ACIK_GRI = (189, 195, 199)

# Top ayarlari
TOP_YARICAP = 15
TOP_HIZ_MIN = 3
TOP_HIZ_MAX = 7
TOP_RENK = SARI


# --- SINIFLAR ---

class Top(pygame.sprite.Sprite):
    """Ekranda hareket eden ve duvarlardan seken top."""

    def __init__(self, x, y, renk=TOP_RENK):
        super().__init__()
        self.yaricap = TOP_YARICAP
        self.image = pygame.Surface(
            (self.yaricap * 2, self.yaricap * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, renk,
            (self.yaricap, self.yaricap), self.yaricap
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.renk = renk

        # Rastgele hiz vektoru
        aci = random.uniform(0, 2 * math.pi)
        hiz_buyuklugu = random.uniform(TOP_HIZ_MIN, TOP_HIZ_MAX)
        self.hiz_x = math.cos(aci) * hiz_buyuklugu
        self.hiz_y = math.sin(aci) * hiz_buyuklugu

        # Iz efekti icin onceki konumlar
        self.iz_listesi = []
        self.iz_uzunlugu = 10

        # Carpisma gosterge zamanlayici
        self.carpisma_zamani = 0

    def update(self):
        """Topu hareket ettirir ve duvar carpismasini kontrol eder."""
        # Iz kaydini guncelle
        self.iz_listesi.append(self.rect.center)
        if len(self.iz_listesi) > self.iz_uzunlugu:
            self.iz_listesi.pop(0)

        # Hareketi uygula
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Sol duvar carpismasi
        if self.rect.left <= 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x)  # Saga yonlendir
            self.carpisma_zamani = pygame.time.get_ticks()

        # Sag duvar carpismasi
        if self.rect.right >= GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x)  # Sola yonlendir
            self.carpisma_zamani = pygame.time.get_ticks()

        # Ust duvar carpismasi
        if self.rect.top <= 0:
            self.rect.top = 0
            self.hiz_y = abs(self.hiz_y)  # Asagi yonlendir
            self.carpisma_zamani = pygame.time.get_ticks()

        # Alt duvar carpismasi
        if self.rect.bottom >= YUKSEKLIK:
            self.rect.bottom = YUKSEKLIK
            self.hiz_y = -abs(self.hiz_y)  # Yukari yonlendir
            self.carpisma_zamani = pygame.time.get_ticks()

    def iz_ciz(self, ekran):
        """Topun hareket izini cizer."""
        for i, konum in enumerate(self.iz_listesi):
            # Iz giderek soluklasiyor
            alfa = int(255 * (i + 1) / self.iz_uzunlugu * 0.4)
            yaricap = max(2, int(self.yaricap * (i + 1) / self.iz_uzunlugu))
            iz_yuzey = pygame.Surface(
                (yaricap * 2, yaricap * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                iz_yuzey, (*self.renk, alfa),
                (yaricap, yaricap), yaricap
            )
            ekran.blit(
                iz_yuzey,
                iz_yuzey.get_rect(center=konum)
            )

    def hiz_vektoru_ciz(self, ekran):
        """Topun hiz vektorunu ok olarak cizer."""
        merkez = self.rect.center
        # Hiz vektorunu buyuterek goster
        olcek = 8
        hedef_x = merkez[0] + self.hiz_x * olcek
        hedef_y = merkez[1] + self.hiz_y * olcek
        pygame.draw.line(ekran, KIRMIZI, merkez, (hedef_x, hedef_y), 2)

        # Ok ucu
        aci = math.atan2(self.hiz_y, self.hiz_x)
        ok_uzunluk = 8
        sol_aci = aci + math.radians(150)
        sag_aci = aci - math.radians(150)
        sol_x = hedef_x + math.cos(sol_aci) * ok_uzunluk
        sol_y = hedef_y + math.sin(sol_aci) * ok_uzunluk
        sag_x = hedef_x + math.cos(sag_aci) * ok_uzunluk
        sag_y = hedef_y + math.sin(sag_aci) * ok_uzunluk
        pygame.draw.polygon(
            ekran, KIRMIZI,
            [(hedef_x, hedef_y), (sol_x, sol_y), (sag_x, sag_y)]
        )

    def carpisma_aktif_mi(self):
        """Son 200ms icinde carpisma oldu mu kontrol eder."""
        return pygame.time.get_ticks() - self.carpisma_zamani < 200


# --- YARDIMCI FONKSIYONLAR ---

def duvar_kenarliklari_ciz(ekran):
    """Ekranin kenarlarini belirgin cizgilerle gosterir."""
    kalinlik = 3
    pygame.draw.rect(
        ekran, GRI,
        (0, 0, GENISLIK, YUKSEKLIK), kalinlik
    )


def bilgi_paneli_ciz(ekran, font, top):
    """Hiz bilgilerini ekranda gosterir."""
    hiz_buyuklugu = math.sqrt(top.hiz_x ** 2 + top.hiz_y ** 2)
    bilgiler = [
        f"Hiz X: {top.hiz_x:+.2f}",
        f"Hiz Y: {top.hiz_y:+.2f}",
        f"Hiz: {hiz_buyuklugu:.2f}",
        f"Konum: ({top.rect.centerx}, {top.rect.centery})",
    ]

    # Arka plan paneli
    panel_genislik = 220
    panel_yukseklik = len(bilgiler) * 25 + 15
    panel = pygame.Surface(
        (panel_genislik, panel_yukseklik), pygame.SRCALPHA
    )
    panel.fill((0, 0, 0, 128))
    ekran.blit(panel, (10, 10))

    for i, bilgi in enumerate(bilgiler):
        yazi = font.render(bilgi, True, BEYAZ)
        ekran.blit(yazi, (15, 15 + i * 25))

    # Carpisma gostergesi
    if top.carpisma_aktif_mi():
        uyari = font.render("[!] CARPISMA!", True, KIRMIZI)
        ekran.blit(uyari, (15, 15 + len(bilgiler) * 25 + 5))


# --- ANA OYUN ---

def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Geri Sekme Demo - Elastik Carpisma")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    baslik_font = pygame.font.Font(None, 32)

    # Top olustur
    top = Top(GENISLIK // 2, YUKSEKLIK // 2)

    # Yardim metni
    yardim_metni = baslik_font.render(
        "R: Sifirla  |  Space: Yeni top  |  ESC: Cikis", True, ACIK_GRI
    )

    calistir = True
    while calistir:
        saat.tick(FPS)

        # --- OLAYLAR ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_r:
                    # Topu sifirla
                    top = Top(GENISLIK // 2, YUKSEKLIK // 2)
                elif olay.key == pygame.K_SPACE:
                    # Rastgele konumda yeni top
                    x = random.randint(
                        TOP_YARICAP, GENISLIK - TOP_YARICAP
                    )
                    y = random.randint(
                        TOP_YARICAP, YUKSEKLIK - TOP_YARICAP
                    )
                    renkler = [SARI, KIRMIZI, YESIL, MAVI, BEYAZ]
                    top = Top(x, y, random.choice(renkler))

        # --- GUNCELLEME ---
        top.update()

        # --- CIZIM ---
        ekran.fill(KOYU_MAVI)

        # Duvar kenarliklari
        duvar_kenarliklari_ciz(ekran)

        # Topun izi
        top.iz_ciz(ekran)

        # Top
        ekran.blit(top.image, top.rect)

        # Hiz vektoru oku
        top.hiz_vektoru_ciz(ekran)

        # Bilgi paneli
        bilgi_paneli_ciz(ekran, font, top)

        # Yardim metni
        ekran.blit(
            yardim_metni,
            yardim_metni.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK - 25)
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
Ortada sari bir top belirir ve rastgele bir yone dogru hareket eder.

Top duvarlara carptiginda:
- Yatay duvara (ust/alt) carptiginda Y hiz bileseni tersine doner
- Dikey duvara (sol/sag) carptiginda X hiz bileseni tersine doner
- Carpisma aninda "[!] CARPISMA!" uyarisi gosterilir

Topun arkasinda solukla kaybolan bir iz efekti gorunur.
Kirmizi bir ok topun mevcut hiz vektorunu gosterir.
Sol ust kosede hiz ve konum bilgileri gosterilir.

Kontroller:
- R: Topu merkeze sifirla
- Space: Rastgele konumda ve renkte yeni top
- ESC: Cikis
"""
