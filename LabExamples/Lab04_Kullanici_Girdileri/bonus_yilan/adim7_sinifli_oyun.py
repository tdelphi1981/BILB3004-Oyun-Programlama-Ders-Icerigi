"""
Yilan Oyunu (Snake) - Gelismis Sinifli Versiyon

Klasik Snake oyununun sinif tabanli mimarisi ile gelismis
versiyonu. Kalitim (inheritance) ile farkli yem turleri,
birden fazla harita secenegi, dinamik hiz sistemi ve yuksek
skor kaydi icerir.

Ogrenilecek kavramlar:
- Sinif tabanli oyun mimarisi (OOP)
- Kalitim (inheritance) ile yem turleri
- Durum makinesi (State Machine) ile oyun akisi
- JSON dosya islemleri (yuksek skor kaydi)
- Fabrika fonksiyonu ile nesne olusturma
- Property dekoratoru
- Dinamik hiz (FPS) kontrolu

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 4 - Hareket Mekanigi

Calistirma: python adim7_sinifli_oyun.py
Gereksinimler: pygame

Kontroller:
- Menu: 1/2/3 ile harita sec, ESC ile cikis
- Oyun: Ok tuslari ile yon degistir, M ile menu, ESC ile cikis
- Game Over: R ile tekrar, M ile menu, ESC ile cikis
"""

import pygame
import random
import json
import os

# --- Ekran Sabitleri ---
HUCRE_BOYUTU = 30
IZGARA_GENISLIK = 30    # 30 hucre yatay
IZGARA_YUKSEKLIK = 20   # 20 hucre dikey
OYUN_GENISLIK = IZGARA_GENISLIK * HUCRE_BOYUTU    # 900 piksel
OYUN_YUKSEKLIK = IZGARA_YUKSEKLIK * HUCRE_BOYUTU  # 600 piksel
PANEL_GENISLIK = 200    # Skor panosu genisligi
TOPLAM_GENISLIK = OYUN_GENISLIK + PANEL_GENISLIK   # 1100 piksel
TOPLAM_YUKSEKLIK = OYUN_YUKSEKLIK                  # 600 piksel

# --- Renkler ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
YESIL = (0, 200, 0)
KOYU_YESIL = (0, 140, 0)
KIRMIZI = (220, 50, 50)
ACIK_KIRMIZI = (255, 100, 100)
GRI = (40, 40, 40)
KOYU_GRI = (25, 25, 25)
MAVI = (50, 120, 220)
ACIK_MAVI = (100, 170, 255)
MOR = (160, 50, 220)
ACIK_MOR = (200, 120, 255)
ALTIN = (220, 180, 30)
ACIK_ALTIN = (255, 215, 80)
PANEL_ARKA = (20, 20, 30)
PANEL_SINIR = (60, 60, 80)
TURUNCU = (220, 150, 30)
SINIR_RENK = (80, 80, 100)
ENGEL_RENK = (100, 60, 60)
ENGEL_IC_RENK = (140, 80, 80)

# --- Yon Sabitleri ---
YUKARI = (0, -1)
ASAGI = (0, 1)
SOL = (-1, 0)
SAG = (1, 0)

# Ters yonler tablosu
TERS_YONLER = {
    YUKARI: ASAGI,
    ASAGI: YUKARI,
    SOL: SAG,
    SAG: SOL,
}

# --- Hiz Sabitleri ---
BASLANGIC_FPS = 8
MAKS_FPS = 22
SKOR_BASINA_HIZ = 5     # Her 5 skorda +1 FPS
HIZ_YEMI_ETKISI = -2    # -2 FPS
HIZ_YEMI_SURESI = 30    # kare
MIN_FPS = 4

# --- Yem Sabitleri ---
OZEL_YEM_OLASILIK = 0.25
ALTIN_AGIRLIK = 50
HIZ_AGIRLIK = 35
SUPER_AGIRLIK = 15

# --- Dosya ---
SKOR_DOSYASI = "yuksek_skorlar.json"
MAKS_SKOR_SAYISI = 5


# ============================================================
# Yardimci Fonksiyonlar
# ============================================================

def hucre_ciz(ekran, konum, renk, ic_renk=None):
    """Izgara konumundaki bir hucreyi ciz."""
    x = konum[0] * HUCRE_BOYUTU
    y = konum[1] * HUCRE_BOYUTU
    pygame.draw.rect(ekran, renk, (x, y, HUCRE_BOYUTU, HUCRE_BOYUTU))
    if ic_renk:
        pygame.draw.rect(
            ekran, ic_renk,
            (x + 2, y + 2, HUCRE_BOYUTU - 4, HUCRE_BOYUTU - 4)
        )


def izgara_ciz(ekran):
    """Arka plana hafif izgara cizgileri ciz."""
    for x in range(0, OYUN_GENISLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, KOYU_GRI, (x, 0), (x, OYUN_YUKSEKLIK))
    for y in range(0, OYUN_YUKSEKLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, KOYU_GRI, (0, y), (OYUN_GENISLIK, y))


# ============================================================
# Harita Sinifi
# ============================================================

class Harita:
    """Oyun haritasi - sinirlar ve engeller."""

    def __init__(self, ad, engeller, aciklama, baslangic_konum, baslangic_yon):
        self.ad = ad
        self.engeller = set(engeller)
        self.aciklama = aciklama
        self.baslangic_konum = baslangic_konum
        self.baslangic_yon = baslangic_yon

    def engel_mi(self, konum):
        """Konum sinir disi veya engel mi?"""
        x, y = konum
        if x < 0 or x >= IZGARA_GENISLIK:
            return True
        if y < 0 or y >= IZGARA_YUKSEKLIK:
            return True
        if konum in self.engeller:
            return True
        return False

    def bos_konum_mu(self, konum, yilan_govde, yemler):
        """Konum tamamen bos mu? (sinir, engel, yilan, yem yok)"""
        if self.engel_mi(konum):
            return False
        if konum in yilan_govde:
            return False
        for yem in yemler:
            if yem.konum == konum:
                return False
        return True

    def ciz(self, ekran):
        """Sinir cizgileri ve engel hucrelerini ciz."""
        # Sinir cizgileri
        pygame.draw.rect(
            ekran, SINIR_RENK,
            (0, 0, OYUN_GENISLIK, OYUN_YUKSEKLIK), 2
        )
        # Engelleri ciz
        for engel in self.engeller:
            hucre_ciz(ekran, engel, ENGEL_RENK, ENGEL_IC_RENK)


def haritalari_olustur():
    """Fabrika fonksiyonu: Tum haritalari olustur ve dondur."""
    # Harita 1: Klasik - engel yok
    klasik = Harita(
        ad="Klasik",
        engeller=[],
        aciklama="Engelsiz klasik alan",
        baslangic_konum=(15, 10),
        baslangic_yon=SAG,
    )

    # Harita 2: Adalar - 3 ada
    ada_engeller = [
        # Sol ust ada (L sekli)
        (6, 4), (7, 4), (7, 5), (7, 6),
        # Orta ada (T sekli)
        (14, 9), (15, 9), (16, 9), (15, 10), (15, 11), (15, 12),
        # Sag alt ada (kare)
        (22, 14), (23, 14), (22, 15), (23, 15),
    ]
    adalar = Harita(
        ad="Adalar",
        engeller=ada_engeller,
        aciklama="Uc ada ile zorlu alan",
        baslangic_konum=(3, 10),
        baslangic_yon=SAG,
    )

    # Harita 3: Labirent
    labirent_engeller = []
    # Yatay duvar 1: (3-8, 7)
    for x in range(3, 9):
        labirent_engeller.append((x, 7))
    # Yatay duvar 2: (21-26, 12)
    for x in range(21, 27):
        labirent_engeller.append((x, 12))
    # Dikey duvar 1: (10, 2-5)
    for y in range(2, 6):
        labirent_engeller.append((10, y))
    # Dikey duvar 2: (19, 14-17)
    for y in range(14, 18):
        labirent_engeller.append((19, y))
    # Merkez engel
    labirent_engeller.extend([(14, 10), (15, 10), (14, 11)])

    labirent = Harita(
        ad="Labirent",
        engeller=labirent_engeller,
        aciklama="Duvarlar ve gecitler",
        baslangic_konum=(2, 2),
        baslangic_yon=SAG,
    )

    return [klasik, adalar, labirent]


# ============================================================
# Yilan Sinifi
# ============================================================

class Yilan:
    """Yilan govdesi ve hareket yonetimi."""

    def __init__(self, baslangic_konum, baslangic_yon):
        bx, by = baslangic_konum
        # Bas + 2 govde parcasi (basa gore sola dogru)
        self.govde = [
            (bx, by),
            (bx - baslangic_yon[0], by - baslangic_yon[1]),
            (bx - 2 * baslangic_yon[0], by - 2 * baslangic_yon[1]),
        ]
        self.yon = baslangic_yon
        self.buyume_bekleyen = 0
        self.yon_kilitli = False  # Kare basina tek yon degisikligi

    @property
    def bas(self):
        """Yilanin bas konumu."""
        return self.govde[0]

    @property
    def uzunluk(self):
        """Yilanin toplam uzunlugu."""
        return len(self.govde)

    def yon_degistir(self, yeni_yon):
        """Yon degistir. Kare basina tek degisiklik, ters yon engelli."""
        if self.yon_kilitli:
            return
        if yeni_yon != TERS_YONLER.get(self.yon):
            self.yon = yeni_yon
            self.yon_kilitli = True

    def hareket_et(self):
        """Basi bir adim ilerlet, buyume durumuna gore kuyruk sil."""
        self.yon_kilitli = False  # Yeni kare, yon kilidi ac
        bas_x, bas_y = self.bas
        yeni_bas = (bas_x + self.yon[0], bas_y + self.yon[1])
        self.govde.insert(0, yeni_bas)

        if self.buyume_bekleyen > 0:
            self.buyume_bekleyen -= 1
        else:
            self.govde.pop()

    def buyu(self, miktar):
        """Buyume bekleme sayacini artir."""
        self.buyume_bekleyen += miktar

    def kendine_carpti_mi(self):
        """Bas govdedeki diger parcalara carpti mi?"""
        return self.bas in self.govde[1:]

    def ciz(self, ekran, olum_animasyonu=False, kare_sayaci=0):
        """Yilani ciz. Bas rounded rect, kuyruk trapezoid."""
        B = HUCRE_BOYUTU
        R = B // 3          # Kose yaricapi (rounded corners)
        DARALTMA = B // 4   # Kuyruk daralma miktari (her taraftan)
        M = 3               # Ic katman kenarligi

        for i, parca in enumerate(self.govde):
            x = parca[0] * B
            y = parca[1] * B

            if olum_animasyonu and kare_sayaci % 2 == 0:
                hucre_ciz(ekran, parca, KIRMIZI, ACIK_KIRMIZI)

            elif i == 0:
                # --- BAS: Rounded rect (on kose yuvarlatilmis) ---
                # Yone gore hangi koseler yuvarlanacak
                rtl = rtr = rbl = rbr = 0
                if self.yon == SAG:
                    rtr = rbr = R
                elif self.yon == SOL:
                    rtl = rbl = R
                elif self.yon == YUKARI:
                    rtl = rtr = R
                elif self.yon == ASAGI:
                    rbl = rbr = R

                # Dis katman (koyu yesil)
                pygame.draw.rect(
                    ekran, KOYU_YESIL, (x, y, B, B),
                    border_top_left_radius=rtl,
                    border_top_right_radius=rtr,
                    border_bottom_left_radius=rbl,
                    border_bottom_right_radius=rbr,
                )
                # Ic katman (acik yesil) - ayni koseler, kucuk radius
                ir = max(1, R - M)
                pygame.draw.rect(
                    ekran, YESIL,
                    (x + M, y + M, B - 2 * M, B - 2 * M),
                    border_top_left_radius=(ir if rtl else 0),
                    border_top_right_radius=(ir if rtr else 0),
                    border_bottom_left_radius=(ir if rbl else 0),
                    border_bottom_right_radius=(ir if rbr else 0),
                )

            elif i == len(self.govde) - 1:
                # --- KUYRUK: Trapezoid (hareket vektorune gore) ---
                # Onceki parcadan kuyruga giden yon
                prev = self.govde[i - 1]
                dx = parca[0] - prev[0]
                dy = parca[1] - prev[1]

                d = DARALTMA  # kisaltma
                # Genis taraf govdeye yakin, dar taraf uca yakin
                if dx == 1:     # Kuyruk saga uzaniyor
                    dis = [(x, y), (x + B, y + d),
                           (x + B, y + B - d), (x, y + B)]
                    ic = [(x + M, y + M), (x + B - M, y + d + M),
                          (x + B - M, y + B - d - M), (x + M, y + B - M)]
                elif dx == -1:  # Kuyruk sola uzaniyor
                    dis = [(x, y + d), (x + B, y),
                           (x + B, y + B), (x, y + B - d)]
                    ic = [(x + M, y + d + M), (x + B - M, y + M),
                          (x + B - M, y + B - M), (x + M, y + B - d - M)]
                elif dy == 1:   # Kuyruk asagi uzaniyor
                    dis = [(x, y), (x + B, y),
                           (x + B - d, y + B), (x + d, y + B)]
                    ic = [(x + M, y + M), (x + B - M, y + M),
                          (x + B - d - M, y + B - M), (x + d + M, y + B - M)]
                else:           # Kuyruk yukari uzaniyor (dy == -1)
                    dis = [(x + d, y), (x + B - d, y),
                           (x + B, y + B), (x, y + B)]
                    ic = [(x + d + M, y + M), (x + B - d - M, y + M),
                          (x + B - M, y + B - M), (x + M, y + B - M)]

                pygame.draw.polygon(ekran, YESIL, dis)
                pygame.draw.polygon(ekran, KOYU_YESIL, ic)

            else:
                # --- GOVDE: Normal dikdortgen ---
                hucre_ciz(ekran, parca, YESIL, KOYU_YESIL)


# ============================================================
# Yem Siniflari (Kalitim)
# ============================================================

class Yem:
    """Temel yem sinifi (base class)."""

    def __init__(self, konum, renk, ic_renk, puan, buyume, gecici=False, sure=0):
        self.konum = konum
        self.renk = renk
        self.ic_renk = ic_renk
        self.puan = puan
        self.buyume = buyume
        self.gecici = gecici
        self.sure = sure          # Kalan sure (kare)
        self.toplam_sure = sure   # Baslangic suresi

    def guncelle(self):
        """Gecici yem ise sureyi azalt. True: hala aktif, False: suresi doldu."""
        if not self.gecici:
            return True
        self.sure -= 1
        return self.sure > 0

    def gorunur_mu(self, kare):
        """Yanip sonme efekti: son 15 karede her 3 karede bir gorunmez."""
        if not self.gecici:
            return True
        if self.sure > 15:
            return True
        # Son 15 karede yanip son
        return kare % 3 != 0

    def ciz(self, ekran, kare):
        """Yemi ekrana ciz (yanip sonme dahil)."""
        if self.gorunur_mu(kare):
            hucre_ciz(ekran, self.konum, self.renk, self.ic_renk)


class NormalYem(Yem):
    """Normal yem: 1 puan, 1 buyume."""

    def __init__(self, konum):
        super().__init__(
            konum=konum,
            renk=KIRMIZI,
            ic_renk=ACIK_KIRMIZI,
            puan=1,
            buyume=1,
            gecici=False,
        )


class AltinYem(Yem):
    """Altin yem: 3 puan, 2 buyume, gecici (50 kare)."""

    def __init__(self, konum):
        super().__init__(
            konum=konum,
            renk=ALTIN,
            ic_renk=ACIK_ALTIN,
            puan=3,
            buyume=2,
            gecici=True,
            sure=50,
        )


class HizYemi(Yem):
    """Hiz yemi: 2 puan, 1 buyume, gecici (50 kare), hiz yavaslatir."""

    def __init__(self, konum):
        super().__init__(
            konum=konum,
            renk=MAVI,
            ic_renk=ACIK_MAVI,
            puan=2,
            buyume=1,
            gecici=True,
            sure=50,
        )


class SuperYem(Yem):
    """Super yem: 5 puan, 3 buyume, gecici (33 kare)."""

    def __init__(self, konum):
        super().__init__(
            konum=konum,
            renk=MOR,
            ic_renk=ACIK_MOR,
            puan=5,
            buyume=3,
            gecici=True,
            sure=33,
        )


# ============================================================
# YemYoneticisi Sinifi
# ============================================================

class YemYoneticisi:
    """Yem olusturma ve yasam dongusu yonetimi."""

    def __init__(self, harita):
        self.harita = harita
        self.yemler = []

    def rastgele_konum(self, yilan_govde):
        """Bos bir rastgele konum bul."""
        for _ in range(200):
            konum = (
                random.randint(0, IZGARA_GENISLIK - 1),
                random.randint(0, IZGARA_YUKSEKLIK - 1),
            )
            if self.harita.bos_konum_mu(konum, yilan_govde, self.yemler):
                return konum
        return None

    def normal_yem_var_mi(self):
        """Aktif yemler arasinda normal yem var mi?"""
        for yem in self.yemler:
            if isinstance(yem, NormalYem):
                return True
        return False

    def ozel_yem_var_mi(self):
        """Aktif yemler arasinda ozel yem var mi?"""
        for yem in self.yemler:
            if not isinstance(yem, NormalYem):
                return True
        return False

    def ozel_yem_olustur(self, yilan_govde):
        """Agirlikli rastgele ozel yem olustur."""
        konum = self.rastgele_konum(yilan_govde)
        if konum is None:
            return
        # Agirlikli secim
        agirliklar = [
            (AltinYem, ALTIN_AGIRLIK),
            (HizYemi, HIZ_AGIRLIK),
            (SuperYem, SUPER_AGIRLIK),
        ]
        toplam = sum(a for _, a in agirliklar)
        r = random.randint(1, toplam)
        birikim = 0
        for sinif, agirlik in agirliklar:
            birikim += agirlik
            if r <= birikim:
                self.yemler.append(sinif(konum))
                return

    def guncelle(self, yilan_govde):
        """Her karede cagirilir: suresi dolanlari temizle, gerekirse yeni yem ekle."""
        # Suresi dolanlari temizle
        self.yemler = [y for y in self.yemler if y.guncelle()]

        # Her zaman en az 1 normal yem olmali
        if not self.normal_yem_var_mi():
            konum = self.rastgele_konum(yilan_govde)
            if konum:
                self.yemler.append(NormalYem(konum))

        # Ozel yem yoksa %25 olasilikla ozel yem olustur
        if not self.ozel_yem_var_mi():
            if random.random() < OZEL_YEM_OLASILIK:
                self.ozel_yem_olustur(yilan_govde)

    def yem_kontrol(self, konum):
        """Verilen konumda yem var mi? Varsa yemi dondur ve listeden cikar."""
        for yem in self.yemler:
            if yem.konum == konum:
                self.yemler.remove(yem)
                return yem
        return None

    def ciz(self, ekran, kare):
        """Tum yemleri ciz."""
        for yem in self.yemler:
            yem.ciz(ekran, kare)

    def aktif_ozel_yem_bilgisi(self):
        """Aktif ozel yemin adi ve kalan suresini dondur."""
        for yem in self.yemler:
            if isinstance(yem, AltinYem):
                return f"Altin Yem (x{yem.puan})", yem.sure
            elif isinstance(yem, HizYemi):
                return "Hiz Yemi (-2 FPS)", yem.sure
            elif isinstance(yem, SuperYem):
                return f"Super Yem (x{yem.puan})", yem.sure
        return None, 0

    def sifirla(self):
        """Tum yemleri temizle."""
        self.yemler.clear()


# ============================================================
# SkorTablosu Sinifi
# ============================================================

class SkorTablosu:
    """Yan panel skor panosu cizimi (200x400 px)."""

    def __init__(self):
        self.kucuk_font = pygame.font.Font(None, 22)
        self.orta_font = pygame.font.Font(None, 28)
        self.buyuk_font = pygame.font.Font(None, 36)

    def hiz_rengi(self, fps):
        """FPS degerine gore renk: yesil(yavas) -> sari(orta) -> kirmizi(hizli)."""
        oran = (fps - BASLANGIC_FPS) / max(1, MAKS_FPS - BASLANGIC_FPS)
        oran = max(0.0, min(1.0, oran))
        if oran < 0.5:
            # Yesil -> Sari
            r = int(200 * (oran * 2))
            g = 200
        else:
            # Sari -> Kirmizi
            r = 200
            g = int(200 * (1 - (oran - 0.5) * 2))
        return (r, g, 0)

    def ciz(self, ekran, skor, yilan_uzunluk, fps, harita_adi,
            yuksek_skorlar, ozel_yem_bilgi, ozel_yem_sure):
        """Skor panosunu ciz."""
        # Panel arka plani
        panel_x = OYUN_GENISLIK
        panel_rect = pygame.Rect(panel_x, 0, PANEL_GENISLIK, TOPLAM_YUKSEKLIK)
        pygame.draw.rect(ekran, PANEL_ARKA, panel_rect)
        pygame.draw.line(
            ekran, PANEL_SINIR,
            (panel_x, 0), (panel_x, TOPLAM_YUKSEKLIK), 2
        )

        x = panel_x + 15
        y = 15

        # Baslik
        baslik = self.orta_font.render("SKOR PANOSU", True, BEYAZ)
        ekran.blit(baslik, (x, y))
        y += 35

        # Ayirici cizgi
        pygame.draw.line(ekran, PANEL_SINIR, (x, y), (panel_x + PANEL_GENISLIK - 15, y))
        y += 12

        # Skor
        skor_yazi = self.buyuk_font.render(f"Skor: {skor}", True, BEYAZ)
        ekran.blit(skor_yazi, (x, y))
        y += 35

        # Uzunluk
        uz_yazi = self.kucuk_font.render(f"Uzunluk: {yilan_uzunluk}", True, GRI)
        ekran.blit(uz_yazi, (x, y))
        y += 22

        # Hiz
        hiz_r = self.hiz_rengi(fps)
        hiz_yazi = self.kucuk_font.render(f"Hiz: {fps} FPS", True, hiz_r)
        ekran.blit(hiz_yazi, (x, y))
        y += 22

        # Harita adi
        harita_yazi = self.kucuk_font.render(f"Harita: {harita_adi}", True, GRI)
        ekran.blit(harita_yazi, (x, y))
        y += 30

        # Ayirici
        pygame.draw.line(ekran, PANEL_SINIR, (x, y), (panel_x + PANEL_GENISLIK - 15, y))
        y += 10

        # En iyi skorlar
        en_iyi = self.kucuk_font.render("--- En Iyi ---", True, ALTIN)
        ekran.blit(en_iyi, (x, y))
        y += 22

        if yuksek_skorlar:
            for i, s in enumerate(yuksek_skorlar[:MAKS_SKOR_SAYISI]):
                renk = ALTIN if i == 0 else BEYAZ
                satir = self.kucuk_font.render(f"{i + 1}. {s}", True, renk)
                ekran.blit(satir, (x + 5, y))
                y += 19
        else:
            bos = self.kucuk_font.render("Henuz yok", True, GRI)
            ekran.blit(bos, (x + 5, y))
            y += 19

        y += 10
        # Ayirici
        pygame.draw.line(ekran, PANEL_SINIR, (x, y), (panel_x + PANEL_GENISLIK - 15, y))
        y += 10

        # Aktif ozel yem
        if ozel_yem_bilgi:
            aktif_baslik = self.kucuk_font.render("[Aktif Yem]", True, ACIK_ALTIN)
            ekran.blit(aktif_baslik, (x, y))
            y += 20
            yem_detay = self.kucuk_font.render(ozel_yem_bilgi, True, BEYAZ)
            ekran.blit(yem_detay, (x, y))
            y += 18
            sure_yazi = self.kucuk_font.render(f"Sure: {ozel_yem_sure}", True, GRI)
            ekran.blit(sure_yazi, (x, y))
            y += 25
        else:
            y += 20

        # Kontrol bilgisi (alt kisim)
        kontrol_y = TOPLAM_YUKSEKLIK - 55
        pygame.draw.line(
            ekran, PANEL_SINIR,
            (x, kontrol_y - 5), (panel_x + PANEL_GENISLIK - 15, kontrol_y - 5)
        )
        kontrol1 = self.kucuk_font.render("Ok tuslari: Yon", True, GRI)
        ekran.blit(kontrol1, (x, kontrol_y))
        kontrol2 = self.kucuk_font.render("R:Tekrar M:Menu", True, GRI)
        ekran.blit(kontrol2, (x, kontrol_y + 17))
        kontrol3 = self.kucuk_font.render("ESC: Cikis", True, GRI)
        ekran.blit(kontrol3, (x, kontrol_y + 34))


# ============================================================
# YuksekSkorYoneticisi Sinifi
# ============================================================

class YuksekSkorYoneticisi:
    """JSON dosya ile yuksek skor kaydi."""

    def __init__(self):
        self.dosya_yolu = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            SKOR_DOSYASI,
        )
        self.skorlar = self.yukle()

    def yukle(self):
        """Dosyadan skorlari oku. Dosya yoksa veya bozuksa bos liste dondur."""
        try:
            with open(self.dosya_yolu, "r") as f:
                veri = json.load(f)
                if isinstance(veri, list):
                    return sorted(veri, reverse=True)[:MAKS_SKOR_SAYISI]
        except (FileNotFoundError, json.JSONDecodeError, TypeError):
            pass
        return []

    def kaydet(self):
        """Skorlari dosyaya yaz."""
        try:
            with open(self.dosya_yolu, "w") as f:
                json.dump(self.skorlar, f)
        except OSError:
            pass

    def ekle(self, skor):
        """Yeni skor ekle. Rekor ise True dondur."""
        yeni_rekor = len(self.skorlar) == 0 or skor > self.skorlar[0]
        self.skorlar.append(skor)
        self.skorlar.sort(reverse=True)
        self.skorlar = self.skorlar[:MAKS_SKOR_SAYISI]
        self.kaydet()
        return yeni_rekor

    @property
    def en_yuksek(self):
        """En yuksek skoru dondur."""
        if self.skorlar:
            return self.skorlar[0]
        return 0


# ============================================================
# HizYoneticisi Sinifi
# ============================================================

class HizYoneticisi:
    """Dinamik FPS kontrolu."""

    def __init__(self):
        self.hiz_etkisi = 0        # Gecici hiz degisimi
        self.etki_suresi = 0       # Kalan etki suresi (kare)

    def fps_hesapla(self, skor):
        """Skora ve gecici etkilere gore FPS hesapla."""
        temel_fps = BASLANGIC_FPS + (skor // SKOR_BASINA_HIZ)
        temel_fps = min(temel_fps, MAKS_FPS)
        sonuc = temel_fps + self.hiz_etkisi
        return max(MIN_FPS, min(sonuc, MAKS_FPS))

    def hiz_etkisi_uygula(self):
        """Hiz yemi etkisini baslat."""
        self.hiz_etkisi = HIZ_YEMI_ETKISI
        self.etki_suresi = HIZ_YEMI_SURESI

    def guncelle(self):
        """Her karede cagirilir: gecici etkinin suresini azalt."""
        if self.etki_suresi > 0:
            self.etki_suresi -= 1
            if self.etki_suresi <= 0:
                self.hiz_etkisi = 0

    def sifirla(self):
        """Etkileri temizle."""
        self.hiz_etkisi = 0
        self.etki_suresi = 0


# ============================================================
# Oyun Sinifi
# ============================================================

class Oyun:
    """Ana oyun sinifi - durum makinesi ile oyun akisi."""

    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((TOPLAM_GENISLIK, TOPLAM_YUKSEKLIK))
        pygame.display.set_caption("Yilan Oyunu - Sinifli Versiyon")
        self.saat = pygame.time.Clock()

        # Font nesneleri
        self.kucuk_font = pygame.font.Font(None, 24)
        self.orta_font = pygame.font.Font(None, 32)
        self.buyuk_font = pygame.font.Font(None, 52)
        self.dev_font = pygame.font.Font(None, 64)

        # Haritalar
        self.haritalar = haritalari_olustur()
        self.secili_harita = 0

        # Yoneticiler
        self.skor_yoneticisi = YuksekSkorYoneticisi()
        self.hiz_yoneticisi = HizYoneticisi()
        self.skor_tablosu = SkorTablosu()

        # Oyun nesneleri (oyun basladiginda olusturulur)
        self.yilan = None
        self.yem_yoneticisi = None

        # Durum
        self.durum = "menu"   # "menu", "oynuyor", "bitti"
        self.skor = 0
        self.kare_sayaci = 0
        self.yeni_rekor = False

        # Olum animasyonu
        self.olum_animasyonu = False
        self.olum_karesi = 0
        self.olum_toplam = 5  # 5 kare yanip sonme

        self.calistir = True

    def harita(self):
        """Secili haritayi dondur."""
        return self.haritalar[self.secili_harita]

    def oyunu_baslat(self):
        """Secili harita ile yeni oyun baslat."""
        h = self.harita()
        self.yilan = Yilan(h.baslangic_konum, h.baslangic_yon)
        self.yem_yoneticisi = YemYoneticisi(h)
        self.hiz_yoneticisi.sifirla()
        self.skor = 0
        self.kare_sayaci = 0
        self.yeni_rekor = False
        self.olum_animasyonu = False
        self.olum_karesi = 0
        self.durum = "oynuyor"

    # --- Olay Isleme ---

    def olaylari_isle(self):
        """Tum olaylari isle (durum bazli)."""
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                self.calistir = False
                return

            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    self.calistir = False
                    return

                if self.durum == "menu":
                    self.menu_olay(olay.key)
                elif self.durum == "oynuyor":
                    self.oyun_olay(olay.key)
                elif self.durum == "bitti":
                    self.bitti_olay(olay.key)

    def menu_olay(self, tus):
        """Menu ekraninda tus islemleri."""
        if tus == pygame.K_1:
            self.secili_harita = 0
            self.oyunu_baslat()
        elif tus == pygame.K_2:
            self.secili_harita = 1
            self.oyunu_baslat()
        elif tus == pygame.K_3:
            self.secili_harita = 2
            self.oyunu_baslat()

    def oyun_olay(self, tus):
        """Oyun sirasinda tus islemleri."""
        if tus == pygame.K_UP:
            self.yilan.yon_degistir(YUKARI)
        elif tus == pygame.K_DOWN:
            self.yilan.yon_degistir(ASAGI)
        elif tus == pygame.K_LEFT:
            self.yilan.yon_degistir(SOL)
        elif tus == pygame.K_RIGHT:
            self.yilan.yon_degistir(SAG)
        elif tus == pygame.K_m:
            self.durum = "menu"

    def bitti_olay(self, tus):
        """Game Over ekraninda tus islemleri."""
        if tus == pygame.K_r:
            self.oyunu_baslat()
        elif tus == pygame.K_m:
            self.durum = "menu"

    # --- Guncelleme ---

    def guncelle(self):
        """Oyun durumunu guncelle (sadece 'oynuyor' durumunda)."""
        if self.durum != "oynuyor":
            return

        # Olum animasyonu devam ediyorsa
        if self.olum_animasyonu:
            self.olum_karesi += 1
            if self.olum_karesi >= self.olum_toplam:
                self.olum_animasyonu = False
                self.durum = "bitti"
                self.yeni_rekor = self.skor_yoneticisi.ekle(self.skor)
            return

        self.kare_sayaci += 1

        # Yilani hareket ettir
        self.yilan.hareket_et()

        # Carpma kontrolu
        h = self.harita()
        if h.engel_mi(self.yilan.bas) or self.yilan.kendine_carpti_mi():
            self.olum_animasyonu = True
            self.olum_karesi = 0
            return

        # Yem kontrolu
        yenen_yem = self.yem_yoneticisi.yem_kontrol(self.yilan.bas)
        if yenen_yem:
            self.skor += yenen_yem.puan
            self.yilan.buyu(yenen_yem.buyume)
            # Hiz yemi ozel etkisi
            if isinstance(yenen_yem, HizYemi):
                self.hiz_yoneticisi.hiz_etkisi_uygula()

        # Yem yoneticisini guncelle (sureler, yeni yem)
        self.yem_yoneticisi.guncelle(self.yilan.govde)

        # Hiz yoneticisini guncelle
        self.hiz_yoneticisi.guncelle()

    # --- Cizim ---

    def menu_ciz(self):
        """Menu ekranini ciz."""
        self.ekran.fill(SIYAH)

        # Baslik
        baslik = self.dev_font.render("YILAN OYUNU", True, YESIL)
        baslik_rect = baslik.get_rect(center=(TOPLAM_GENISLIK // 2, 60))
        self.ekran.blit(baslik, baslik_rect)

        # Alt baslik
        alt = self.kucuk_font.render("Sinifli Versiyon", True, GRI)
        alt_rect = alt.get_rect(center=(TOPLAM_GENISLIK // 2, 95))
        self.ekran.blit(alt, alt_rect)

        # Harita secenekleri
        y_baslangic = 150
        for i, h in enumerate(self.haritalar):
            renk = BEYAZ
            # Harita numarasi ve adi
            satir = self.orta_font.render(
                f"[{i + 1}] {h.ad}", True, renk
            )
            satir_rect = satir.get_rect(center=(TOPLAM_GENISLIK // 2, y_baslangic))
            self.ekran.blit(satir, satir_rect)

            # Aciklama
            aciklama = self.kucuk_font.render(h.aciklama, True, GRI)
            ac_rect = aciklama.get_rect(center=(TOPLAM_GENISLIK // 2, y_baslangic + 25))
            self.ekran.blit(aciklama, ac_rect)

            y_baslangic += 65

        # Yuksek skor
        if self.skor_yoneticisi.en_yuksek > 0:
            rekor = self.kucuk_font.render(
                f"En Yuksek Skor: {self.skor_yoneticisi.en_yuksek}", True, ALTIN
            )
            rekor_rect = rekor.get_rect(center=(TOPLAM_GENISLIK // 2, 350))
            self.ekran.blit(rekor, rekor_rect)

        # Cikis bilgisi
        cikis = self.kucuk_font.render("ESC: Cikis", True, GRI)
        cikis_rect = cikis.get_rect(center=(TOPLAM_GENISLIK // 2, 380))
        self.ekran.blit(cikis, cikis_rect)

    def oyun_ciz(self):
        """Oyun ekranini ciz."""
        # Oyun alani arka plan
        oyun_alan = pygame.Rect(0, 0, OYUN_GENISLIK, OYUN_YUKSEKLIK)
        pygame.draw.rect(self.ekran, SIYAH, oyun_alan)
        izgara_ciz(self.ekran)

        # Harita (sinirlar + engeller)
        self.harita().ciz(self.ekran)

        # Yemleri ciz
        self.yem_yoneticisi.ciz(self.ekran, self.kare_sayaci)

        # Yilani ciz
        self.yilan.ciz(self.ekran, self.olum_animasyonu, self.olum_karesi)

        # Skor panosunu ciz
        fps = self.hiz_yoneticisi.fps_hesapla(self.skor)
        ozel_bilgi, ozel_sure = self.yem_yoneticisi.aktif_ozel_yem_bilgisi()
        self.skor_tablosu.ciz(
            self.ekran,
            skor=self.skor,
            yilan_uzunluk=self.yilan.uzunluk,
            fps=fps,
            harita_adi=self.harita().ad,
            yuksek_skorlar=self.skor_yoneticisi.skorlar,
            ozel_yem_bilgi=ozel_bilgi,
            ozel_yem_sure=ozel_sure,
        )

    def bitti_ciz(self):
        """Game Over ekranini ciz (oyun alani uzerine)."""
        # Once oyun ekranini ciz (donmus hali)
        self.oyun_ciz()

        # Yari saydam katman (sadece oyun alani)
        katman = pygame.Surface((OYUN_GENISLIK, OYUN_YUKSEKLIK))
        katman.set_alpha(160)
        katman.fill(SIYAH)
        self.ekran.blit(katman, (0, 0))

        merkez_x = OYUN_GENISLIK // 2

        # GAME OVER
        go_yazi = self.buyuk_font.render("GAME OVER", True, KIRMIZI)
        go_rect = go_yazi.get_rect(center=(merkez_x, OYUN_YUKSEKLIK // 2 - 45))
        self.ekran.blit(go_yazi, go_rect)

        # Skor bilgisi
        skor_bilgi = self.orta_font.render(
            f"Skor: {self.skor}  Uzunluk: {self.yilan.uzunluk}",
            True, BEYAZ,
        )
        skor_rect = skor_bilgi.get_rect(center=(merkez_x, OYUN_YUKSEKLIK // 2 - 5))
        self.ekran.blit(skor_bilgi, skor_rect)

        # Yeni rekor bildirimi
        if self.yeni_rekor and self.skor > 0:
            rekor_yazi = self.orta_font.render("YENI REKOR!", True, ALTIN)
            rekor_rect = rekor_yazi.get_rect(center=(merkez_x, OYUN_YUKSEKLIK // 2 + 30))
            self.ekran.blit(rekor_yazi, rekor_rect)
            alt_y = OYUN_YUKSEKLIK // 2 + 65
        else:
            alt_y = OYUN_YUKSEKLIK // 2 + 40

        # Tekrar / Menu bilgisi
        tekrar = self.kucuk_font.render(
            "R: Tekrar  M: Menu  ESC: Cikis", True, GRI
        )
        tekrar_rect = tekrar.get_rect(center=(merkez_x, alt_y))
        self.ekran.blit(tekrar, tekrar_rect)

    def ciz(self):
        """Duruma gore ekrani ciz."""
        if self.durum == "menu":
            self.menu_ciz()
        elif self.durum == "oynuyor":
            self.oyun_ciz()
        elif self.durum == "bitti":
            self.bitti_ciz()

        pygame.display.flip()

    # --- Ana Dongu ---

    def calistir_dongu(self):
        """Ana oyun dongusu."""
        while self.calistir:
            # FPS kontrolu
            if self.durum == "oynuyor":
                fps = self.hiz_yoneticisi.fps_hesapla(self.skor)
            else:
                fps = 30  # Menu ve bitti ekranlarinda sabit FPS

            self.saat.tick(fps)

            self.olaylari_isle()
            self.guncelle()
            self.ciz()

        pygame.quit()


# ============================================================
# Giris Noktasi
# ============================================================

def main():
    """Oyunu baslat."""
    oyun = Oyun()
    oyun.calistir_dongu()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
800x400 piksel boyutunda bir pencere acilir.
Sol taraf (600x400): Oyun alani - izgara, yilan, yemler.
Sag taraf (200x400): Skor panosu - skor, hiz, yuksek skorlar.

Menu Ekrani:
- "YILAN OYUNU" basligi
- 3 harita secenegi (1: Klasik, 2: Adalar, 3: Labirent)
- 1/2/3 tuslari ile harita secilir ve oyun baslar

Oyun Ekrani:
- Yesil yilan harita uzerinde hareket eder
- Kirmizi normal yem her zaman aktiftir
- Altin (sari), Hiz (mavi), Super (mor) ozel yemler belirir
- Ozel yemler suresi dolmadan yanip sonerek kaybolur
- Skor arttikca oyun hizi (FPS) kademeli olarak artar
- Hiz yemi yenildiginde gecici olarak yavaslama olur
- Engellere veya kendine carpinca olum animasyonu oynar

Game Over Ekrani:
- Skor ve uzunluk bilgisi
- Yeni rekor ise "YENI REKOR!" altin yaziyla gosterilir
- R ile tekrar, M ile menu, ESC ile cikis
- Skor yuksek_skorlar.json dosyasina kaydedilir
"""
