"""
Yok Etme ve Skor Demo - Patlama Efekti ve Combo Mekanigi

Fare ile tiklayarak dusmanlari yok eden bir oyun demosu.
Yok edilen dusmanlar patlama efekti gosterir, skor artar.
Hizli ardisik yok etmelerde combo bonusu kazanilir.

Ogrenilecek kavramlar:
- Fare tiklama ile hedef secimi
- Sprite yok etme (kill)
- Patlama efekti (buyuyup solan daire)
- Skor sistemi
- Combo mekanigi (zamana dayali bonus puan)

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 4 - Carpisma Tepkileri

Calistirma: python 03_yok_etme_skor.py
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
MOR = (155, 89, 182)
KOYU_MAVI = (44, 62, 80)
GRI = (149, 165, 166)
ACIK_GRI = (189, 195, 199)

# Dusman ayarlari
DUSMAN_MIN_BOYUT = 20
DUSMAN_MAX_BOYUT = 40
DUSMAN_HIZ_MIN = 1
DUSMAN_HIZ_MAX = 3
DUSMAN_BASLANGIC_SAYISI = 6
DUSMAN_YENILEME_SURESI = 2000  # ms

# Puan ayarlari
TEMEL_PUAN = 50
COMBO_SURESI = 1500  # ms - bu sure icinde combo devam eder
COMBO_CARPAN_ARTIS = 0.5  # Her combo kademesinde eklenen carpan

# Patlama ayarlari
PATLAMA_SURESI = 500  # ms
PATLAMA_MAX_YARICAP = 50

# Dusman renkleri
DUSMAN_RENKLERI = [KIRMIZI, TURUNCU, MOR, YESIL, MAVI]


# --- SINIFLAR ---

class Dusman(pygame.sprite.Sprite):
    """Ekranda dolasan ve tiklanarak yok edilebilen dusman."""

    def __init__(self):
        super().__init__()
        self.yaricap = random.randint(DUSMAN_MIN_BOYUT, DUSMAN_MAX_BOYUT)
        self.renk = random.choice(DUSMAN_RENKLERI)

        self.image = pygame.Surface(
            (self.yaricap * 2, self.yaricap * 2), pygame.SRCALPHA
        )
        self._gorsel_ciz()

        # Rastgele baslangic konumu (ekran icinde)
        x = random.randint(
            self.yaricap, GENISLIK - self.yaricap
        )
        y = random.randint(
            self.yaricap + 60, YUKSEKLIK - self.yaricap
        )
        self.rect = self.image.get_rect(center=(x, y))

        # Hareket
        aci = random.uniform(0, 2 * math.pi)
        hiz = random.uniform(DUSMAN_HIZ_MIN, DUSMAN_HIZ_MAX)
        self.hiz_x = math.cos(aci) * hiz
        self.hiz_y = math.sin(aci) * hiz

        # Puan degeri: kucuk dusmanlar daha cok puan verir
        boyut_orani = 1 - (
            (self.yaricap - DUSMAN_MIN_BOYUT)
            / (DUSMAN_MAX_BOYUT - DUSMAN_MIN_BOYUT)
        )
        self.puan = int(TEMEL_PUAN * (1 + boyut_orani))

    def _gorsel_ciz(self):
        """Dusman gorselini cizer."""
        self.image.fill((0, 0, 0, 0))
        # Ana govde
        pygame.draw.circle(
            self.image, self.renk,
            (self.yaricap, self.yaricap), self.yaricap
        )
        # Ic halka
        if self.yaricap > 15:
            pygame.draw.circle(
                self.image, BEYAZ,
                (self.yaricap, self.yaricap),
                self.yaricap - 5, 2
            )
        # Gozler
        goz_y = self.yaricap - 3
        pygame.draw.circle(
            self.image, BEYAZ,
            (self.yaricap - 6, goz_y), 4
        )
        pygame.draw.circle(
            self.image, BEYAZ,
            (self.yaricap + 6, goz_y), 4
        )
        pygame.draw.circle(
            self.image, SIYAH,
            (self.yaricap - 5, goz_y), 2
        )
        pygame.draw.circle(
            self.image, SIYAH,
            (self.yaricap + 7, goz_y), 2
        )

    def update(self):
        """Dusmanin hareketini gunceller."""
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Duvarlardan sek
        if self.rect.left < 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x)
        if self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x)
        if self.rect.top < 60:
            self.rect.top = 60
            self.hiz_y = abs(self.hiz_y)
        if self.rect.bottom > YUKSEKLIK:
            self.rect.bottom = YUKSEKLIK
            self.hiz_y = -abs(self.hiz_y)

    def tiklanma_kontrolu(self, fare_konumu):
        """Fare tiklamasinin dusmanin uzerine gelip gelmedigini kontrol eder.

        Args:
            fare_konumu: (x, y) tuple fare koordinatlari.

        Returns:
            True eger tiklanma daire icindeyse.
        """
        # Daire icinde mi? (piksel seviyesinde dogruluk)
        dx = fare_konumu[0] - self.rect.centerx
        dy = fare_konumu[1] - self.rect.centery
        mesafe = math.sqrt(dx * dx + dy * dy)
        return mesafe <= self.yaricap


class Patlama(pygame.sprite.Sprite):
    """Dusman yok edildiginde gosterilen patlama efekti."""

    def __init__(self, merkez, renk):
        super().__init__()
        self.merkez = merkez
        self.renk = renk
        self.baslangic = pygame.time.get_ticks()
        self.sure = PATLAMA_SURESI
        self.max_yaricap = PATLAMA_MAX_YARICAP

        boyut = self.max_yaricap * 2
        self.image = pygame.Surface((boyut, boyut), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=merkez)

    def update(self):
        """Patlamayi gunceller: buyuyen ve solan daire efekti."""
        gecen = pygame.time.get_ticks() - self.baslangic
        oran = gecen / self.sure

        if oran >= 1.0:
            self.kill()
            return

        # Yaricap buyur
        yaricap = int(self.max_yaricap * oran)
        # Opakligi azalt
        alfa = int(255 * (1 - oran))

        # Gorseli yeniden ciz
        self.image.fill((0, 0, 0, 0))

        if yaricap > 0:
            # Dis halka
            renk_alfa = (*self.renk, alfa)
            pygame.draw.circle(
                self.image, renk_alfa,
                (self.max_yaricap, self.max_yaricap),
                yaricap, max(1, 3 - int(oran * 3))
            )
            # Ic parildama
            ic_alfa = int(alfa * 0.5)
            ic_yaricap = max(1, yaricap // 2)
            pygame.draw.circle(
                self.image, (255, 255, 200, ic_alfa),
                (self.max_yaricap, self.max_yaricap),
                ic_yaricap
            )


class SkorYoneticisi:
    """Skor ve combo sistemini yonetir."""

    def __init__(self):
        self.skor = 0
        self.en_yuksek_skor = 0
        self.combo_sayaci = 0
        self.son_yok_etme_zamani = 0
        self.en_yuksek_combo = 0

        # Kayan puan yazilari
        self.puan_yazilari = []  # (metin, konum, zaman, renk)

    def puan_ekle(self, temel_puan, konum):
        """Puan ekler ve combo hesaplar.

        Args:
            temel_puan: Yok edilen dusmanin temel puani.
            konum: Puanin gosterilecegi (x, y) koordinati.

        Returns:
            (kazanilan_puan, combo_kademesi) tuple.
        """
        simdi = pygame.time.get_ticks()

        # Combo kontrolu
        if simdi - self.son_yok_etme_zamani < COMBO_SURESI:
            self.combo_sayaci += 1
        else:
            self.combo_sayaci = 1

        self.son_yok_etme_zamani = simdi

        # Combo carpani
        carpan = 1 + (self.combo_sayaci - 1) * COMBO_CARPAN_ARTIS
        kazanilan = int(temel_puan * carpan)
        self.skor += kazanilan

        # En yuksek combo takibi
        if self.combo_sayaci > self.en_yuksek_combo:
            self.en_yuksek_combo = self.combo_sayaci

        # En yuksek skor takibi
        if self.skor > self.en_yuksek_skor:
            self.en_yuksek_skor = self.skor

        # Kayan puan yazisi olustur
        if self.combo_sayaci > 1:
            metin = f"+{kazanilan} (x{self.combo_sayaci} COMBO!)"
            renk = SARI
        else:
            metin = f"+{kazanilan}"
            renk = BEYAZ

        self.puan_yazilari.append(
            (metin, list(konum), simdi, renk)
        )

        return kazanilan, self.combo_sayaci

    def combo_aktif_mi(self):
        """Combo suresinin devam edip etmedigini kontrol eder."""
        return (
            pygame.time.get_ticks() - self.son_yok_etme_zamani
            < COMBO_SURESI
        )

    def combo_kalan_sure(self):
        """Combodan kalan sureyi saniye olarak dondurur."""
        kalan = COMBO_SURESI - (
            pygame.time.get_ticks() - self.son_yok_etme_zamani
        )
        return max(0, kalan / 1000)

    def puan_yazilari_guncelle(self):
        """Kayan puan yazilarini gunceller (eski olanlari siler)."""
        simdi = pygame.time.get_ticks()
        guncellenmis = []
        for metin, konum, zaman, renk in self.puan_yazilari:
            if simdi - zaman < 1200:
                konum[1] -= 1.5  # Yukari kaydir
                guncellenmis.append((metin, konum, zaman, renk))
        self.puan_yazilari = guncellenmis

    def sifirla(self):
        """Skoru sifirlar (en yuksek skor korunur)."""
        self.skor = 0
        self.combo_sayaci = 0
        self.en_yuksek_combo = 0
        self.puan_yazilari.clear()


# --- YARDIMCI FONKSIYONLAR ---

def hud_ciz(ekran, font, kucuk_font, skor_yon, dusman_sayisi):
    """Ekranin ustune skor ve bilgileri cizer."""
    # Ust bar arka plani
    bar_yuzey = pygame.Surface((GENISLIK, 50), pygame.SRCALPHA)
    bar_yuzey.fill((0, 0, 0, 160))
    ekran.blit(bar_yuzey, (0, 0))

    # Skor
    skor_yazi = font.render(f"SKOR: {skor_yon.skor}", True, BEYAZ)
    ekran.blit(skor_yazi, (15, 12))

    # En yuksek skor
    ey_yazi = kucuk_font.render(
        f"En Yuksek: {skor_yon.en_yuksek_skor}", True, GRI
    )
    ekran.blit(ey_yazi, (15, 34))

    # Combo gostergesi
    if skor_yon.combo_aktif_mi() and skor_yon.combo_sayaci > 1:
        combo_metin = f"COMBO x{skor_yon.combo_sayaci}"
        combo_yazi = font.render(combo_metin, True, SARI)
        combo_rect = combo_yazi.get_rect(center=(GENISLIK // 2, 18))
        ekran.blit(combo_yazi, combo_rect)

        # Combo zamanlayici cubugu
        kalan_oran = skor_yon.combo_kalan_sure() / (COMBO_SURESI / 1000)
        cubuk_gen = int(150 * kalan_oran)
        cubuk_x = GENISLIK // 2 - 75
        cubuk_y = 36
        pygame.draw.rect(
            ekran, GRI, (cubuk_x, cubuk_y, 150, 6)
        )
        if cubuk_gen > 0:
            pygame.draw.rect(
                ekran, SARI, (cubuk_x, cubuk_y, cubuk_gen, 6)
            )

    # Dusman sayisi
    dusman_yazi = font.render(
        f"Dusman: {dusman_sayisi}", True, KIRMIZI
    )
    dusman_rect = dusman_yazi.get_rect(topright=(GENISLIK - 15, 12))
    ekran.blit(dusman_yazi, dusman_rect)


def puan_yazilari_ciz(ekran, font, skor_yon):
    """Kayan puan yazilarini ekrana cizer."""
    simdi = pygame.time.get_ticks()
    for metin, konum, zaman, renk in skor_yon.puan_yazilari:
        gecen = simdi - zaman
        alfa = max(0, 255 - int(gecen * 255 / 1200))
        yazi = font.render(metin, True, renk)
        yazi.set_alpha(alfa)
        ekran.blit(yazi, konum)


def nisangah_ciz(ekran, fare_konumu):
    """Fare konumunda basit bir nisangah cizer."""
    x, y = fare_konumu
    boyut = 12
    kalinlik = 2
    renk = BEYAZ

    # Capraz cizgiler
    pygame.draw.line(
        ekran, renk,
        (x - boyut, y), (x - 4, y), kalinlik
    )
    pygame.draw.line(
        ekran, renk,
        (x + 4, y), (x + boyut, y), kalinlik
    )
    pygame.draw.line(
        ekran, renk,
        (x, y - boyut), (x, y - 4), kalinlik
    )
    pygame.draw.line(
        ekran, renk,
        (x, y + 4), (x, y + boyut), kalinlik
    )

    # Merkez noktasi
    pygame.draw.circle(ekran, renk, (x, y), 2)


# --- ANA OYUN ---

def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Yok Etme ve Skor Demo")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    kucuk_font = pygame.font.Font(None, 22)
    buyuk_font = pygame.font.Font(None, 48)

    # Fare imlecini gizle (nisangah kullanacagiz)
    pygame.mouse.set_visible(False)

    # Sprite gruplari
    dusman_grubu = pygame.sprite.Group()
    patlama_grubu = pygame.sprite.Group()

    # Baslangic dusmanlari
    for _ in range(DUSMAN_BASLANGIC_SAYISI):
        dusman_grubu.add(Dusman())

    # Skor yoneticisi
    skor_yon = SkorYoneticisi()

    # Dusman yenileme zamanlayicisi
    son_yenileme = pygame.time.get_ticks()

    calistir = True

    while calistir:
        saat.tick(FPS)
        simdi = pygame.time.get_ticks()

        # --- OLAYLAR ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_r:
                    # Sifirla
                    dusman_grubu.empty()
                    patlama_grubu.empty()
                    skor_yon.sifirla()
                    for _ in range(DUSMAN_BASLANGIC_SAYISI):
                        dusman_grubu.add(Dusman())
                    son_yenileme = simdi

            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if olay.button == 1:  # Sol tik
                    fare_konumu = olay.pos
                    # Tiklanan dusmani bul
                    vurulan = False
                    for dusman in list(dusman_grubu):
                        if dusman.tiklanma_kontrolu(fare_konumu):
                            # Patlama efekti olustur
                            patlama = Patlama(
                                dusman.rect.center, dusman.renk
                            )
                            patlama_grubu.add(patlama)

                            # Puan ekle
                            skor_yon.puan_ekle(
                                dusman.puan, list(dusman.rect.midtop)
                            )

                            # Dusmani yok et
                            dusman.kill()
                            vurulan = True
                            break  # Tek tikla tek dusman

                    if not vurulan:
                        # Bos tiklamada combo sifirlanir
                        # (sadece combo suresi dolunca sifirlansin,
                        # bos tiklamada bir sey yapma)
                        pass

        # --- GUNCELLEME ---
        dusman_grubu.update()
        patlama_grubu.update()
        skor_yon.puan_yazilari_guncelle()

        # Belirli araliklarla yeni dusman ekle
        if simdi - son_yenileme > DUSMAN_YENILEME_SURESI:
            if len(dusman_grubu) < 12:  # Maksimum dusman siniri
                dusman_grubu.add(Dusman())
            son_yenileme = simdi

        # --- CIZIM ---
        ekran.fill(KOYU_MAVI)

        # Dusmanlar
        dusman_grubu.draw(ekran)

        # Patlama efektleri
        patlama_grubu.draw(ekran)

        # Kayan puan yazilari
        puan_yazilari_ciz(ekran, font, skor_yon)

        # HUD
        hud_ciz(ekran, font, kucuk_font, skor_yon, len(dusman_grubu))

        # Nisangah
        nisangah_ciz(ekran, pygame.mouse.get_pos())

        # Alt bilgi
        bilgi_yazi = kucuk_font.render(
            "Sol Tik: Yok et  |  R: Sifirla  |  ESC: Cikis",
            True, ACIK_GRI
        )
        ekran.blit(
            bilgi_yazi,
            bilgi_yazi.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK - 15)
            )
        )

        pygame.display.flip()

    # Fare imlecini geri getir
    pygame.mouse.set_visible(True)
    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu mavi arka planli bir pencere acilir.
Fare imleci yerine beyaz bir nisangah gosterilir.
Ekranda renkli, farkli boyutlarda dairevi dusmanlar hareket eder.

Tiklama mekanigi:
- Sol tiklama ile nisangahin altindaki dusman yok edilir
- Yok edilen dusman buyuyup solan bir daire (patlama) efekti gosterir
- Kazanilan puan yukari kayarak solar (+50, +75 gibi)
- Kucuk dusmanlar daha cok puan verir

Combo sistemi:
- 1.5 saniye icinde ardisik yok etmelerde combo artar
- Combo aktifken "COMBO x2", "COMBO x3" gibi gosterilir
- Her combo kademesi puan carpanini 0.5 arttirir (x2: 1.5 carpan)
- Combo zamanlayicisi sari cubukla gosterilir
- Sure dolunca combo sifirlanir

HUD bilgileri:
- Sol ust: Mevcut skor ve en yuksek skor
- Orta ust: Combo gostergesi ve zamanlayici
- Sag ust: Mevcut dusman sayisi

Her 2 saniyede yeni bir dusman eklenir (maksimum 12 adet).
R tusu ile oyun sifirlanabilir.
"""
