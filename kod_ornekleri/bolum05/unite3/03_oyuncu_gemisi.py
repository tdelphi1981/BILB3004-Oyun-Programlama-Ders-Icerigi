"""
Oyuncu Gemisi - Klavye ile kontrol edilen Sprite

Bu program pygame.sprite.Sprite sinifini kullanarak
klavye ile kontrol edilen bir oyuncu gemisi olusturur.
Ok tuslari veya WASD ile hareket, clamp_ip() ile ekran
siniri kontrolu saglanir.

Ogrenilecek kavramlar:
- Oyuncu sinifi (pygame.sprite.Sprite)
- key.get_pressed() ile surekli girdi okuma
- clamp_ip() ile ekran siniri kontrolu
- Hiz sabiti ile smooth hareket
- gorsel_yukle() fallback mekanizmasi

Bolum: 05 - Gorseller ve Sprite Temelleri
Unite: 3 - Sprite Sinifi

Calistirma: python 03_oyuncu_gemisi.py
Gereksinimler: pygame
"""

import os
import random
import pygame

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
BASLIK = "Oyuncu Gemisi -- Sprite Ornegi"
ARKA_PLAN = (8, 8, 25)
OYUNCU_HIZ = 5
DUSMAN_SAYISI = 6


def gorsel_yukle(dosya_yolu, boyut=None):
    """Gorsel dosyasini yukler, bulunamazsa renkli yuzey dondurur.

    Args:
        dosya_yolu: Gorsel dosyasinin yolu
        boyut: (genislik, yukseklik) demeti, None ise orijinal boyut

    Returns:
        pygame.Surface nesnesi
    """
    try:
        gorsel = pygame.image.load(dosya_yolu).convert_alpha()
        if boyut:
            gorsel = pygame.transform.scale(gorsel, boyut)
        return gorsel
    except (pygame.error, FileNotFoundError):
        if boyut is None:
            boyut = (50, 40)
        yuzey = pygame.Surface(boyut, pygame.SRCALPHA)
        # Fallback: basit gemi sekli ciz
        pygame.draw.polygon(yuzey, (60, 140, 255), [
            (boyut[0] // 2, 0),          # Burun (ust orta)
            (0, boyut[1]),               # Sol alt
            (boyut[0], boyut[1]),        # Sag alt
        ])
        # Kabin detayi
        pygame.draw.circle(yuzey, (120, 200, 255),
                           (boyut[0] // 2, boyut[1] // 2), 6)
        return yuzey


# ---------------------------------------------------------------------------
# Sprite Siniflari
# ---------------------------------------------------------------------------

class Oyuncu(pygame.sprite.Sprite):
    """Klavye ile kontrol edilen oyuncu gemisi Sprite'i.

    Ok tuslari veya WASD ile dort yonlu hareket saglar.
    clamp_ip() ile ekran sinirlarinda kalir.
    """

    def __init__(self, x, y):
        """Oyuncu Sprite'ini olusturur.

        Args:
            x: Baslangic merkez x koordinati
            y: Baslangic merkez y koordinati
        """
        super().__init__()
        # Gorseli yukle (bulunamazsa fallback)
        self.image = gorsel_yukle(
            "assets/images/playerShip1_blue.png", (50, 40)
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz = OYUNCU_HIZ

    def update(self):
        """Klavye girdisine gore hareket et ve ekran sinirinda kal."""
        tuslar = pygame.key.get_pressed()

        # Yatay hareket (ok tuslari + WASD)
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]:
            self.rect.x -= self.hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]:
            self.rect.x += self.hiz

        # Dikey hareket (ok tuslari + WASD)
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]:
            self.rect.y -= self.hiz
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]:
            self.rect.y += self.hiz

        # Ekran sinirlarini asma
        ekran_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(ekran_rect)


class Dusman(pygame.sprite.Sprite):
    """Otomatik hareket eden dusman Sprite'i.

    Ekranin ustunden rastgele konumda belirir ve
    asagiya dogru hareket eder. Ekrandan cikinca yok olur.
    """

    def __init__(self):
        """Dusman Sprite'ini rastgele konum ve hizla olusturur."""
        super().__init__()
        boyut = random.randint(25, 40)
        self.image = pygame.Surface((boyut, boyut), pygame.SRCALPHA)

        # Rastgele kirmizi tonu
        kirmizi = random.randint(160, 230)
        renk = (kirmizi, random.randint(30, 70), random.randint(20, 50))
        pygame.draw.polygon(self.image, renk, [
            (boyut // 2, boyut),         # Alt orta (burun asagi)
            (0, 0),                      # Sol ust
            (boyut, 0),                  # Sag ust
        ])

        self.rect = self.image.get_rect(
            center=(random.randint(30, GENISLIK - 30),
                    random.randint(-100, -20))
        )
        self.hiz = random.uniform(1.5, 4.0)

    def update(self):
        """Her karede asagiya dogru hareket et."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.kill()


class YildizSprite(pygame.sprite.Sprite):
    """Arka plan yildiz efekti."""

    def __init__(self):
        """Yildiz Sprite'i olusturur."""
        super().__init__()
        boyut = random.randint(1, 3)
        self.image = pygame.Surface((boyut, boyut))
        parlaklik = random.randint(80, 200)
        self.image.fill((parlaklik, parlaklik, min(parlaklik + 40, 255)))
        self.rect = self.image.get_rect(
            center=(random.randint(0, GENISLIK),
                    random.randint(0, YUKSEKLIK))
        )
        self.hiz = random.uniform(0.2, 1.0)

    def update(self):
        """Yavasca asagi kay."""
        self.rect.y += self.hiz
        if self.rect.top > YUKSEKLIK:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, GENISLIK)


def main():
    """Ana program fonksiyonu."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # --- Sprite'lari olustur ---
    oyuncu = Oyuncu(GENISLIK // 2, YUKSEKLIK - 80)
    yildizlar = [YildizSprite() for _ in range(50)]
    dusmanlar = [Dusman() for _ in range(DUSMAN_SAYISI)]

    # Bilgi fontu
    font = pygame.font.Font(None, 24)

    print("=" * 55)
    print("  Oyuncu Gemisi -- Sprite Ornegi")
    print("  Ok tuslari veya WASD ile gemiyi kontrol et.")
    print("  Dusmanlar otomatik olarak yukaridan iner.")
    print("  ESC ile cikis.")
    print("=" * 55)

    calistir = True
    while calistir:
        # --- Olay isleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        # --- Guncelleme ---
        oyuncu.update()

        for yildiz in yildizlar:
            yildiz.update()

        for dusman in dusmanlar:
            dusman.update()

        # Yok edilen dusmanlari cikar ve yenile
        dusmanlar = [d for d in dusmanlar if d.alive()]
        while len(dusmanlar) < DUSMAN_SAYISI:
            dusmanlar.append(Dusman())

        # --- Cizim ---
        ekran.fill(ARKA_PLAN)

        # Yildizlari ciz (arka plan)
        for yildiz in yildizlar:
            ekran.blit(yildiz.image, yildiz.rect)

        # Dusmanlari ciz
        for dusman in dusmanlar:
            ekran.blit(dusman.image, dusman.rect)

        # Oyuncuyu ciz (en onde)
        ekran.blit(oyuncu.image, oyuncu.rect)

        # Bilgi metni
        bilgi_metin = (
            f"Konum: ({oyuncu.rect.centerx}, {oyuncu.rect.centery})  |  "
            f"Hiz: {oyuncu.hiz}px/kare  |  "
            f"WASD/Ok tuslari  |  ESC: Cikis"
        )
        bilgi = font.render(bilgi_metin, True, (160, 160, 180))
        ekran.blit(bilgi, (10, 10))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()
    print("\nProgram sonlandi.")


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
=======================================================
  Oyuncu Gemisi -- Sprite Ornegi
  Ok tuslari veya WASD ile gemiyi kontrol et.
  Dusmanlar otomatik olarak yukaridan iner.
  ESC ile cikis.
=======================================================

Ekranda 800x600 koyu pencere acilir.
- Arka planda yavas kayan yildizlar gorulur.
- Alt ortada mavi ucgen seklinde oyuncu gemisi yer alir.
- Ok tuslari veya WASD ile dort yone hareket edebilirsin.
- Gemi ekran sinirlarini asamaz (clamp_ip kontrolu).
- Kirmizi ucgen dusmanlar yukaridan asagiya hareket eder.
- Sol ustte konum ve hiz bilgisi gorulur.
ESC ile cikis yapilir.

Program sonlandi.
"""
