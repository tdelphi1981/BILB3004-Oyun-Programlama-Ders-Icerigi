"""
Uzay Savaşçısı - Adım 7: Sınıflı Gelişmiş Oyun (OOP)

Tam nesne yönelimli tasarım ile gelişmiş uzay savaşı oyunu.
Patlama animasyonu, düşman mermi ateşi, güçlendirmeler
(power-up), dalga sistemi ve JSON skor tablosu içerir.

Öğrenilecek kavramlar:
- Sınıf hiyerarşisi ve OOP tasarım
- Sprite animasyonu (frame dizisi)
- State machine (oyun durumları)
- JSON ile dosyaya veri kaydetme/okuma
- Dalga (wave) sistemi ile zorluk yönetimi
- Birden fazla sprite grubu koordinasyonu

Bölüm: 05 - Görseller ve Sprite Temelleri
Lab: 05 - Bonus: Uzay Savaşçısı (Adım 7/7)

Çalıştırma: uv run python adim7_sinifli_oyun.py
Gereksinimler: pygame

Kontroller:
- WASD / Ok tuşları: Hareket
- SPACE: Ateş
- R: Yeniden başla (Game Over sonrası)
- ESC: Çıkış
"""

import pygame
import random
import os
import sys
import json

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Uzay Savaşçısı - Gelişmiş"

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KOYU_MAVI = (8, 8, 32)
ACIK_MAVI = (100, 180, 255)
SARI = (255, 220, 50)
GRI = (150, 150, 160)
KOYU_GRI = (80, 80, 90)
KIRMIZI = (220, 50, 50)
KOYU_KIRMIZI = (150, 30, 30)
YESIL = (50, 220, 50)
TURUNCU = (255, 140, 0)
MOR = (150, 50, 200)

# Asset dizini
ASSET_DIZIN = os.path.join(
    os.path.dirname(__file__), "..", "assets", "kenney_space-shooter-redux"
)

# Skor dosyası (bu dosyanın yanına kaydedilir)
SKOR_DOSYASI = os.path.join(os.path.dirname(__file__), "yuksek_skorlar.json")


# --- Yardımcı Fonksiyonlar ---

def gorsel_yukle(dosya_adi, boyut=None):
    """Görsel dosyasını yükle, bulunamazsa None döndür."""
    try:
        yol = os.path.join(ASSET_DIZIN, dosya_adi)
        gorsel = pygame.image.load(yol).convert_alpha()
        if boyut:
            gorsel = pygame.transform.smoothscale(gorsel, boyut)
        # Colorkey ile ek şeffaflık garantisi (alpha sorunlu
        # sistemlerde siyah arka plan yerine şeffaflık sağlar)
        gorsel.set_colorkey(SIYAH)
        return gorsel
    except (pygame.error, FileNotFoundError):
        return None


def gorsel_listesi_yukle(dosya_deseni, sayi, boyut=None):
    """Numaralı görsel dizisini yükle (animasyon için).

    Args:
        dosya_deseni: Dosya adı şablonu (orn: "PNG/Effects/fire{:02d}.png")
        sayi: Yüklenecek görsel sayısı.
        boyut: Her görsel için boyut.

    Returns:
        Görsel listesi (başarılı olanlar) veya boş liste.
    """
    gorseller = []
    for i in range(sayi):
        gorsel = gorsel_yukle(dosya_deseni.format(i), boyut)
        if gorsel:
            gorseller.append(gorsel)
    return gorseller


def skorlari_oku():
    """JSON dosyasından skor tablosunu oku.

    Returns:
        En yüksek 5 skoru içeren liste.
    """
    try:
        with open(SKOR_DOSYASI, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def skorlari_kaydet(skorlar):
    """Skor tablosunu JSON dosyasına kaydet.

    Args:
        skorlar: Skor listesi.
    """
    # En yüksek 5 skoru tut
    skorlar = sorted(skorlar, reverse=True)[:5]
    with open(SKOR_DOSYASI, "w") as f:
        json.dump(skorlar, f)


def arkaplan_olustur():
    """Döşemeli arka plan Surface'i oluştur."""
    arkaplan = pygame.Surface((GENISLIK, YUKSEKLIK * 2))
    gorsel = gorsel_yukle("Backgrounds/darkPurple.png")

    if gorsel:
        g_gen = gorsel.get_width()
        g_yuk = gorsel.get_height()
        for x in range(0, GENISLIK, g_gen):
            for y in range(0, YUKSEKLIK * 2, g_yuk):
                arkaplan.blit(gorsel, (x, y))
    else:
        arkaplan.fill(KOYU_MAVI)
        for _ in range(200):
            x = random.randint(0, GENISLIK - 1)
            y = random.randint(0, YUKSEKLIK * 2 - 1)
            boyut = random.randint(1, 3)
            if boyut == 3:
                renk = BEYAZ
            elif boyut == 2:
                renk = GRI
            else:
                renk = KOYU_GRI
            pygame.draw.circle(arkaplan, renk, (x, y), boyut)

    return arkaplan


# --- Sprite Sınıfları ---

class Oyuncu(pygame.sprite.Sprite):
    """Oyuncu uzay gemisi.

    Özellikler:
    - 4 yönlü hareket (WASD + Ok tuşları)
    - Mermi atma (SPACE, cooldown ile)
    - Can sistemi
    - Kalkan güçlendirmesi desteği
    """

    def __init__(self):
        super().__init__()
        gorsel = gorsel_yukle("PNG/playerShip1_blue.png", (50, 40))
        if gorsel:
            self.image = gorsel
        else:
            self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
            govde = [(25, 2), (46, 38), (4, 38)]
            pygame.draw.polygon(self.image, ACIK_MAVI, govde)
            pygame.draw.polygon(self.image, BEYAZ, govde, 2)
            pygame.draw.circle(self.image, SARI, (25, 20), 4)

        self.rect = self.image.get_rect()
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.hiz = 5
        self.sinir = pygame.Rect(0, 0, GENISLIK, YUKSEKLIK)
        self.son_ates = 0
        self.mermi_bekleme = 250
        self.can = 3
        self.max_can = 3
        # Kalkan durumu
        self.kalkan_aktif = False
        self.kalkan_bitis = 0

    def update(self):
        """Klavye girdilerine göre hareket et."""
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

        # Kalkan süresi kontrolü
        if self.kalkan_aktif:
            if pygame.time.get_ticks() > self.kalkan_bitis:
                self.kalkan_aktif = False

    def ates_et(self, mermi_grubu, tum_grup):
        """Cooldown süresi dolduysa mermi oluştur."""
        simdi = pygame.time.get_ticks()
        if simdi - self.son_ates >= self.mermi_bekleme:
            mermi = Mermi(self.rect.centerx, self.rect.top, yukari=True)
            mermi_grubu.add(mermi)
            tum_grup.add(mermi)
            self.son_ates = simdi

    def kalkan_al(self, sure=5000):
        """Kalkanı etkinleştir.

        Args:
            sure: Kalkan süresi (ms). Varsayılan 5 saniye.
        """
        self.kalkan_aktif = True
        self.kalkan_bitis = pygame.time.get_ticks() + sure

    def hasar_al(self):
        """Hasar al. Kalkan aktifse hasar almaz.

        Returns:
            True: Gerçekten hasar aldıysa, False: Kalkan koruduysa.
        """
        if self.kalkan_aktif:
            return False
        self.can -= 1
        return True

    def ciz_ek(self, ekran):
        """Kalkan efektini oyuncunun üstüne çiz."""
        if self.kalkan_aktif:
            # Mavi yarı saydam daire
            kalkan_yuzey = pygame.Surface((60, 50), pygame.SRCALPHA)
            pygame.draw.ellipse(
                kalkan_yuzey, (100, 180, 255, 80),
                (0, 0, 60, 50)
            )
            pygame.draw.ellipse(
                kalkan_yuzey, (100, 180, 255, 160),
                (0, 0, 60, 50), 2
            )
            ekran.blit(
                kalkan_yuzey,
                (self.rect.centerx - 30, self.rect.centery - 25)
            )

    def sifirla(self):
        """Oyuncuyu başlangıç durumuna döndür."""
        self.rect.centerx = GENISLIK // 2
        self.rect.bottom = YUKSEKLIK - 20
        self.can = self.max_can
        self.kalkan_aktif = False
        self.son_ates = 0


class Mermi(pygame.sprite.Sprite):
    """Mermi sprite'ı (oyuncu ve düşman için kullanılır)."""

    def __init__(self, x, y, yukari=True):
        """Mermi oluştur.

        Args:
            x: Başlangıç x konumu (merkez).
            y: Başlangıç y konumu.
            yukari: True ise yukarı, False ise aşağı gider.
        """
        super().__init__()
        if yukari:
            gorsel = gorsel_yukle("PNG/Lasers/laserBlue01.png", (9, 37))
            fallback_renk = SARI
        else:
            gorsel = gorsel_yukle("PNG/Lasers/laserRed01.png", (9, 37))
            fallback_renk = KIRMIZI

        if gorsel:
            self.image = gorsel
        else:
            self.image = pygame.Surface((9, 37), pygame.SRCALPHA)
            pygame.draw.rect(self.image, fallback_renk, (2, 0, 5, 37))
            pygame.draw.rect(self.image, BEYAZ, (3, 0, 3, 10))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if yukari:
            self.rect.bottom = y
            self.hiz = -8
        else:
            self.rect.top = y
            self.hiz = 5

    def update(self):
        """Mermiyi hareket ettir, ekran dışında sil."""
        self.rect.y += self.hiz
        if self.rect.bottom < 0 or self.rect.top > YUKSEKLIK:
            self.kill()


class Dusman(pygame.sprite.Sprite):
    """Düşman uzay gemisi.

    Farklı tiplerde (küçük/orta/büyük) olabilir.
    Bazı düşmanlar mermi atabilir.
    """

    TIPLERI = [
        {"dosya": "PNG/Enemies/enemyRed1.png", "boyut": (40, 30),
         "hiz": (2, 4), "puan": 100, "ates_sans": 0},
        {"dosya": "PNG/Enemies/enemyRed2.png", "boyut": (50, 35),
         "hiz": (1, 3), "puan": 150, "ates_sans": 0.005},
        {"dosya": "PNG/Enemies/enemyRed3.png", "boyut": (60, 40),
         "hiz": (1, 2), "puan": 200, "ates_sans": 0.01},
    ]

    def __init__(self, hiz_carpani=1.0):
        super().__init__()
        self.tip = random.choice(self.TIPLERI)

        gorsel = gorsel_yukle(self.tip["dosya"], self.tip["boyut"])
        if gorsel:
            self.image = gorsel
        else:
            boyut = self.tip["boyut"]
            self.image = pygame.Surface(boyut, pygame.SRCALPHA)
            pygame.draw.rect(
                self.image, KIRMIZI, (0, 0, boyut[0], boyut[1]),
                border_radius=4
            )
            pygame.draw.rect(
                self.image, KOYU_KIRMIZI,
                (3, 3, boyut[0] - 6, boyut[1] - 6),
                border_radius=3
            )

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GENISLIK - self.rect.width)
        self.rect.bottom = 0

        min_hiz, max_hiz = self.tip["hiz"]
        self.hiz = random.uniform(min_hiz, max_hiz) * hiz_carpani
        self.puan = self.tip["puan"]
        self.ates_sans = self.tip["ates_sans"]

    def update(self):
        """Düşmanı aşağı hareket ettir."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()

    def ates_dene(self, dusman_mermi_grubu, tum_grup):
        """Her frame'de düşmanın ateş etme şansını dene.

        Args:
            dusman_mermi_grubu: Düşman mermilerinin grubu.
            tum_grup: Tüm sprite'ların grubu.
        """
        if random.random() < self.ates_sans:
            mermi = Mermi(self.rect.centerx, self.rect.bottom, yukari=False)
            dusman_mermi_grubu.add(mermi)
            tum_grup.add(mermi)


class Patlama(pygame.sprite.Sprite):
    """Patlama animasyonu.

    Görsel dosyaları varsa fire00-fire08 animasyonu,
    yoksa büyüyüp solarak kaybolan turuncu daire.
    """

    def __init__(self, merkez):
        """Patlama oluştur.

        Args:
            merkez: (x, y) patlama merkez konumu.
        """
        super().__init__()
        self.frameler = gorsel_listesi_yukle(
            "PNG/Effects/fire{:02d}.png", 9, (50, 50)
        )

        if self.frameler:
            # Görsel animasyon
            self.frame_no = 0
            self.image = self.frameler[0]
            self.rect = self.image.get_rect(center=merkez)
            self.animasyon_hizi = 3  # Her 3 frame'de bir değiştir
            self.sayac = 0
        else:
            # Fallback: büyüyen turuncu daire
            self.frame_no = 0
            self.max_frame = 15
            self.boyut = 10
            self.merkez = merkez
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(self.image, TURUNCU, (30, 30), self.boyut)
            self.rect = self.image.get_rect(center=merkez)
            self.animasyon_hizi = 0
            self.sayac = 0

    def update(self):
        """Animasyonu ilerlet, bitince sil."""
        self.sayac += 1

        if self.frameler:
            if self.sayac >= self.animasyon_hizi:
                self.sayac = 0
                self.frame_no += 1
                if self.frame_no >= len(self.frameler):
                    self.kill()
                    return
                self.image = self.frameler[self.frame_no]
        else:
            # Fallback animasyon
            self.frame_no += 1
            if self.frame_no >= self.max_frame:
                self.kill()
                return
            # Büyüyüp solan daire
            self.boyut = 10 + self.frame_no * 3
            alfa = max(0, 255 - self.frame_no * 17)
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
            renk = (255, 140, 0, alfa)
            pygame.draw.circle(
                self.image, renk, (30, 30), min(self.boyut, 30)
            )


class GucLendirme(pygame.sprite.Sprite):
    """Güçlendirme (power-up) sprite'ı.

    Düşman yok edildiğinde düşük olasılıkla ortaya çıkar.
    Oyuncu toplarsa kalkan aktif olur.
    """

    def __init__(self, x, y):
        super().__init__()
        gorsel = gorsel_yukle(
            "PNG/Power-ups/powerupBlue_shield.png", (30, 30)
        )
        if gorsel:
            self.image = gorsel
        else:
            # Fallback: mor daire
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.image, MOR, (15, 15), 14)
            pygame.draw.circle(self.image, BEYAZ, (15, 15), 14, 2)
            # K harfi (kalkan)
            font = pygame.font.Font(None, 20)
            harf = font.render("K", True, BEYAZ)
            harf_rect = harf.get_rect(center=(15, 15))
            self.image.blit(harf, harf_rect)

        self.rect = self.image.get_rect(center=(x, y))
        self.hiz = 2

    def update(self):
        """Aşağı hareket et, ekrandan çıkınca sil."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


# --- Oyun Yönetici Sınıfı ---

class Oyun:
    """Ana oyun yönetici sınıfı.

    Tüm oyun durumunu, sprite gruplarını ve oyun
    döngüsünü yönetir.
    """

    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
        pygame.display.set_caption(BASLIK)
        self.saat = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.buyuk_font = pygame.font.Font(None, 64)
        self.kucuk_font = pygame.font.Font(None, 22)

        # Arka plan
        self.arkaplan = arkaplan_olustur()
        self.arkaplan_y = 0

        # Skor tablosu
        self.skor_tablosu = skorlari_oku()

        # Oyunu başlat
        self.sifirla()

    def sifirla(self):
        """Oyun durumunu sıfırla."""
        # Sprite grupları
        self.tum_spritelar = pygame.sprite.Group()
        self.mermiler = pygame.sprite.Group()
        self.dusmanlar = pygame.sprite.Group()
        self.dusman_mermileri = pygame.sprite.Group()
        self.patlamalar = pygame.sprite.Group()
        self.guc_lendirmeler = pygame.sprite.Group()

        # Oyuncu
        self.oyuncu = Oyuncu()
        self.tum_spritelar.add(self.oyuncu)

        # Oyun durumu
        self.skor = 0
        self.dalga = 1
        self.oyun_bitti = False
        self.baslangic_zamani = pygame.time.get_ticks()
        self.son_dusman_zamani = pygame.time.get_ticks()
        self.son_dalga_zamani = pygame.time.get_ticks()

    def olay_isle(self):
        """Kullanıcı olaylarını işle.

        Returns:
            False: Program kapatılacak, True: Devam.
        """
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                return False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    return False

                if self.oyun_bitti:
                    if olay.key == pygame.K_r:
                        self.sifirla()
                    continue

                if olay.key == pygame.K_SPACE:
                    self.oyuncu.ates_et(
                        self.mermiler, self.tum_spritelar
                    )
        return True

    def guncelle(self):
        """Oyun durumunu güncelle."""
        if self.oyun_bitti:
            return

        # Arka plan kaydırma
        self.arkaplan_y += 1
        if self.arkaplan_y >= YUKSEKLIK:
            self.arkaplan_y = 0

        simdi = pygame.time.get_ticks()
        gecen_sure = (simdi - self.baslangic_zamani) / 1000

        # Dalga sistemi: her 30 saniyede yeni dalga
        if simdi - self.son_dalga_zamani >= 30000:
            self.dalga += 1
            self.son_dalga_zamani = simdi

        # Spawn aralığı: dalga arttıkça kısalır
        spawn_arasi = max(300, 1000 - (self.dalga - 1) * 80)
        hiz_carpani = 1.0 + (self.dalga - 1) * 0.15

        # Düşman spawn
        if simdi - self.son_dusman_zamani >= spawn_arasi:
            dusman = Dusman(hiz_carpani)
            self.dusmanlar.add(dusman)
            self.tum_spritelar.add(dusman)
            self.son_dusman_zamani = simdi

        # Düşman ateş denemesi
        for dusman in self.dusmanlar:
            dusman.ates_dene(
                self.dusman_mermileri, self.tum_spritelar
            )

        # Tüm sprite'ları güncelle
        self.tum_spritelar.update()

        # --- Çarpışmalar ---
        self._carpismalari_isle()

    def _carpismalari_isle(self):
        """Tüm çarpışmaları kontrol et ve işle."""
        # Oyuncu mermisi - Düşman
        vurulanlar = pygame.sprite.groupcollide(
            self.mermiler, self.dusmanlar, True, True
        )
        for mermi, dusman_listesi in vurulanlar.items():
            for dusman in dusman_listesi:
                self.skor += dusman.puan
                # Patlama efekti
                patlama = Patlama(dusman.rect.center)
                self.patlamalar.add(patlama)
                self.tum_spritelar.add(patlama)
                # Güçlendirme şansı (%8)
                if random.random() < 0.08:
                    guc = GucLendirme(*dusman.rect.center)
                    self.guc_lendirmeler.add(guc)
                    self.tum_spritelar.add(guc)

        # Düşman - Oyuncu
        carpanlar = pygame.sprite.spritecollide(
            self.oyuncu, self.dusmanlar, True
        )
        for dusman in carpanlar:
            patlama = Patlama(dusman.rect.center)
            self.patlamalar.add(patlama)
            self.tum_spritelar.add(patlama)
            if self.oyuncu.hasar_al():
                if self.oyuncu.can <= 0:
                    self._oyunu_bitir()

        # Düşman mermisi - Oyuncu
        mermi_carpma = pygame.sprite.spritecollide(
            self.oyuncu, self.dusman_mermileri, True
        )
        for mermi in mermi_carpma:
            if self.oyuncu.hasar_al():
                if self.oyuncu.can <= 0:
                    self._oyunu_bitir()

        # Güçlendirme - Oyuncu
        gucler = pygame.sprite.spritecollide(
            self.oyuncu, self.guc_lendirmeler, True
        )
        for guc in gucler:
            self.oyuncu.kalkan_al(5000)

    def _oyunu_bitir(self):
        """Oyunu bitir ve skoru kaydet."""
        self.oyun_bitti = True
        self.oyuncu.can = 0
        # Skor tablosuna ekle
        self.skor_tablosu.append(self.skor)
        self.skor_tablosu = sorted(
            self.skor_tablosu, reverse=True
        )[:5]
        skorlari_kaydet(self.skor_tablosu)

    def ciz(self):
        """Tüm görüntüyü çiz."""
        # Arka plan
        self.ekran.blit(
            self.arkaplan, (0, self.arkaplan_y - YUKSEKLIK)
        )
        self.ekran.blit(self.arkaplan, (0, self.arkaplan_y))

        # Tüm sprite'lar
        self.tum_spritelar.draw(self.ekran)

        # Oyuncu kalkan efekti
        self.oyuncu.ciz_ek(self.ekran)

        # HUD
        self._hud_ciz()

        # Game Over
        if self.oyun_bitti:
            self._game_over_ciz()

        pygame.display.flip()

    def _hud_ciz(self):
        """Başlık ekranı bilgilerini çiz."""
        # Skor (sol üst)
        skor_yazi = self.font.render(
            f"Skor: {self.skor}", True, SARI
        )
        self.ekran.blit(skor_yazi, (15, 15))

        # Dalga (sol üst, ikinci satır)
        dalga_yazi = self.font.render(
            f"Dalga: {self.dalga}", True, GRI
        )
        self.ekran.blit(dalga_yazi, (15, 42))

        # Can (sağ üst)
        can_metin = "Can: " + "| " * self.oyuncu.can
        can_renk = YESIL if self.oyuncu.can > 1 else KIRMIZI
        can_yazi = self.font.render(can_metin, True, can_renk)
        can_rect = can_yazi.get_rect(right=GENISLIK - 15, top=15)
        self.ekran.blit(can_yazi, can_rect)

        # Kalkan durumu (sağ üst, ikinci satır)
        if self.oyuncu.kalkan_aktif:
            kalan = (self.oyuncu.kalkan_bitis
                     - pygame.time.get_ticks()) / 1000
            kalkan_yazi = self.font.render(
                f"Kalkan: {kalan:.1f}s", True, ACIK_MAVI
            )
            kalkan_rect = kalkan_yazi.get_rect(
                right=GENISLIK - 15, top=42
            )
            self.ekran.blit(kalkan_yazi, kalkan_rect)

        # Kontrol bilgisi (alt orta)
        if not self.oyun_bitti:
            kontrol = self.kucuk_font.render(
                "WASD: Hareket | SPACE: Ateş | ESC: Çıkış",
                True, KOYU_GRI
            )
            kontrol_rect = kontrol.get_rect(
                centerx=GENISLIK // 2, bottom=YUKSEKLIK - 8
            )
            self.ekran.blit(kontrol, kontrol_rect)

    def _game_over_ciz(self):
        """Game Over ekranını çiz."""
        # Yarı saydam katman
        katman = pygame.Surface((GENISLIK, YUKSEKLIK))
        katman.set_alpha(150)
        katman.fill(SIYAH)
        self.ekran.blit(katman, (0, 0))

        # OYUN BİTTİ
        go_yazi = self.buyuk_font.render("OYUN BİTTİ", True, KIRMIZI)
        go_rect = go_yazi.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK // 2 - 80)
        )
        self.ekran.blit(go_yazi, go_rect)

        # Final skor
        skor_yazi = self.font.render(
            f"Skor: {self.skor} | Dalga: {self.dalga}",
            True, BEYAZ
        )
        skor_rect = skor_yazi.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK // 2 - 35)
        )
        self.ekran.blit(skor_yazi, skor_rect)

        # Skor tablosu
        tablo_baslik = self.font.render(
            "-- En Yüksek Skorlar --", True, SARI
        )
        tablo_rect = tablo_baslik.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK // 2)
        )
        self.ekran.blit(tablo_baslik, tablo_rect)

        for i, s in enumerate(self.skor_tablosu[:5]):
            renk = SARI if s == self.skor else GRI
            satir = self.font.render(
                f"{i + 1}. {s}", True, renk
            )
            satir_rect = satir.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK // 2 + 28 + i * 24)
            )
            self.ekran.blit(satir, satir_rect)

        # Yeniden başlatma
        tekrar_yazi = self.font.render(
            "R: Tekrar | ESC: Çıkış", True, GRI
        )
        tekrar_rect = tekrar_yazi.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK // 2 + 160)
        )
        self.ekran.blit(tekrar_yazi, tekrar_rect)

    def calistir(self):
        """Ana oyun döngüsünü başlat."""
        while True:
            self.saat.tick(FPS)

            if not self.olay_isle():
                break

            self.guncelle()
            self.ciz()

        pygame.quit()
        sys.exit()


# --- Ana Program ---

def main():
    """Oyunu başlat."""
    oyun = Oyun()
    oyun.calistir()


if __name__ == "__main__":
    main()

"""
BEKLENEN ÇIKTI:
---------------
800x600 piksel boyutunda gelişmiş uzay savaşı oyunu açılır.

Oyun özellikleri:
- WASD/Ok tuşları ile hareket, SPACE ile ateş
- 3 farklı düşman tipi (küçük=100, orta=150, büyük=200 puan)
- Büyük düşmanlar ara sıra kırmızı mermi atar
- Düşmanlar vurulunca patlama animasyonu gösterilir
- %8 olasılıkla güçlendirme (kalkan) düşer
- Kalkanı topla: 5 saniye boyunca hasar almaz (mavi aura)

Dalga sistemi:
- Her 30 saniyede yeni dalga başlar
- Her dalgada düşmanlar daha sık ve hızlı gelir
- Sol üstte dalga numarası görülür

Skor tablosu:
- Game Over ekranında en yüksek 5 skor listelenir
- Skorlar JSON dosyasına kaydedilir (kalıcı)

Kontroller:
- WASD / Ok tuşları: Hareket
- SPACE: Ateş
- R: Yeniden başla (Game Over sonrası)
- ESC: Çıkış
"""
