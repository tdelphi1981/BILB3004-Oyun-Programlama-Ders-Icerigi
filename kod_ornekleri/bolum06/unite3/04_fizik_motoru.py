"""
PhysicsBody Sinifi - Basit Fizik Motoru

Yercekimi, ivme, surtunme ve momentum kavramlarini birlestiren
tekrar kullanilabilir PhysicsBody sinifi. Farkli parametrelerle
farkli fizik davranislari gosteren nesneler olusturulur.

Ogrenilecek kavramlar:
- PhysicsBody sinifi tasarimi
- Kalitim ile farkli fizik davranislari
- Kuvvet uygulama (Newton 2. yasa)
- Tam fizik dongusu

Bolum: 06 - Carpisma Algilama ve Fizik Temelleri
Unite: 3 - Temel Fizik Simulasyonu

Calistirma: python 04_fizik_motoru.py
Gereksinimler: pygame
"""

import pygame
import math

# Sabitler
GENISLIK = 800
YUKSEKLIK = 600
FPS = 60
ZEMIN_Y = 550


class PhysicsBody(pygame.sprite.Sprite):
    """Fizik davranisi gosteren temel sprite sinifi."""

    def __init__(self, x, y, genislik, yukseklik, kutle=1.0):
        super().__init__()
        self.image = pygame.Surface((genislik, yukseklik))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Hareket
        self.hiz_x = 0.0
        self.hiz_y = 0.0

        # Fizik parametreleri
        self.kutle = kutle
        self.yercekimi = 0.5
        self.surtunme = 0.80
        self.hava_direnci = 0.99
        self.max_hiz = 8.0
        self.terminal_hiz = 15.0

        # Durum
        self.yerde_mi = False

    def kuvvet_uygula(self, kuvvet_x, kuvvet_y):
        """Nesneye kuvvet uygular (F = m * a -> a = F / m)."""
        self.hiz_x += kuvvet_x / self.kutle
        self.hiz_y += kuvvet_y / self.kutle

    def fizik_guncelle(self):
        """Her karede cagirilacak fizik hesaplamalari."""
        # 1. Yercekimi
        self.hiz_y += self.yercekimi

        # 2. Surtunme / hava direnci
        if self.yerde_mi:
            self.hiz_x *= self.surtunme
        else:
            self.hiz_x *= self.hava_direnci

        # 3. Cok kucuk hizlari sifirla
        if abs(self.hiz_x) < 0.1:
            self.hiz_x = 0

        # 4. Hiz sinirlamalari
        if self.hiz_x > self.max_hiz:
            self.hiz_x = self.max_hiz
        elif self.hiz_x < -self.max_hiz:
            self.hiz_x = -self.max_hiz

        if self.hiz_y > self.terminal_hiz:
            self.hiz_y = self.terminal_hiz

        # 5. Konum guncelle
        self.rect.x += int(self.hiz_x)
        self.rect.y += int(self.hiz_y)

    def zemin_kontrolu(self, zemin_y):
        """Nesnenin zemin altina dusmesini engeller."""
        if self.rect.bottom >= zemin_y:
            self.rect.bottom = zemin_y
            self.hiz_y = 0
            self.yerde_mi = True
        else:
            self.yerde_mi = False

    def zipla(self, guc=-12):
        """Nesneyi ziplatir (sadece yerdeyken)."""
        if self.yerde_mi:
            self.hiz_y = guc
            self.yerde_mi = False


class Oyuncu(PhysicsBody):
    """Oyuncu karakteri - standart fizik."""

    def __init__(self, x, y):
        super().__init__(x, y, 32, 48, kutle=1.0)
        self.image.fill((100, 200, 100))
        self.ivme_gucu = 0.8

    def update(self):
        tuslar = pygame.key.get_pressed()

        if tuslar[pygame.K_RIGHT]:
            self.kuvvet_uygula(self.ivme_gucu, 0)
        if tuslar[pygame.K_LEFT]:
            self.kuvvet_uygula(-self.ivme_gucu, 0)

        self.fizik_guncelle()
        self.zemin_kontrolu(ZEMIN_Y)

        # Ekran siniri
        if self.rect.left < 0:
            self.rect.left = 0
            self.hiz_x = 0
        elif self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = 0


class AgirKutu(PhysicsBody):
    """Agir, yavas hareket eden kutu."""

    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, kutle=5.0)
        self.image.fill((150, 100, 50))
        self.max_hiz = 3.0
        self.surtunme = 0.70

    def update(self):
        self.fizik_guncelle()
        self.zemin_kontrolu(ZEMIN_Y)


class HafifTop(PhysicsBody):
    """Hafif, zipziplayan top."""

    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, kutle=0.3)
        self.image.fill((255, 200, 50))
        self.yercekimi = 0.3
        self.surtunme = 0.95
        self.sekme_sayaci = 0

    def update(self):
        self.fizik_guncelle()

        # Zemin kontrolu - sekme efekti
        if self.rect.bottom >= ZEMIN_Y:
            self.rect.bottom = ZEMIN_Y
            if abs(self.hiz_y) > 2:
                # Geri sek (enerjinin %60'ini koru)
                self.hiz_y = -self.hiz_y * 0.6
                self.sekme_sayaci += 1
            else:
                self.hiz_y = 0
                self.yerde_mi = True

        # Ekran siniri - yandan sekme
        if self.rect.left <= 0:
            self.rect.left = 0
            self.hiz_x = abs(self.hiz_x) * 0.8
        elif self.rect.right >= GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x = -abs(self.hiz_x) * 0.8


def main():
    """Ana fonksiyon."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("PhysicsBody - Fizik Motoru Demo")
    saat = pygame.time.Clock()

    # Nesneleri olustur
    oyuncu = Oyuncu(100, 400)
    kutu = AgirKutu(400, 300)
    top = HafifTop(600, 200)

    # Topu firlat
    top.kuvvet_uygula(5, -8)

    tum_nesneler = pygame.sprite.Group(oyuncu, kutu, top)

    font = pygame.font.Font(None, 24)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_SPACE:
                    oyuncu.zipla()
                elif olay.key == pygame.K_r:
                    # Topu yeniden firlat
                    top.rect.center = (600, 200)
                    top.hiz_x = 0
                    top.hiz_y = 0
                    top.yerde_mi = False
                    top.kuvvet_uygula(5, -8)

        tum_nesneler.update()

        # Cizim
        ekran.fill((30, 30, 50))

        # Zemin
        pygame.draw.line(ekran, (100, 100, 100),
                         (0, ZEMIN_Y), (GENISLIK, ZEMIN_Y), 2)

        tum_nesneler.draw(ekran)

        # Etiketler
        oyuncu_bilgi = font.render(
            f"Oyuncu (kutle=1.0) hiz: ({oyuncu.hiz_x:.1f}, {oyuncu.hiz_y:.1f})",
            True, (100, 200, 100)
        )
        kutu_bilgi = font.render(
            f"Kutu (kutle=5.0) hiz: ({kutu.hiz_x:.1f}, {kutu.hiz_y:.1f})",
            True, (150, 100, 50)
        )
        top_bilgi = font.render(
            f"Top (kutle=0.3) hiz: ({top.hiz_x:.1f}, {top.hiz_y:.1f})",
            True, (255, 200, 50)
        )
        kontrol = font.render(
            "Ok Tuslari: Hareket | Bosluk: Zipla | R: Topu Yeniden Firlat",
            True, (150, 150, 150)
        )

        ekran.blit(oyuncu_bilgi, (10, 10))
        ekran.blit(kutu_bilgi, (10, 30))
        ekran.blit(top_bilgi, (10, 50))
        ekran.blit(kontrol, (10, 80))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
Uc farkli nesne ekranda:
- Yesil dikdortgen (Oyuncu): Ok tuslariyla hareket, boslukla zipla
- Kahverengi kare (Agir Kutu): Yercekimiyle duser, hizla durur
- Sari kucuk kare (Hafif Top): Firlatilir, duvarlarda ve yerde seker

Her nesne farkli kutle ve surtunme parametreleriyle farkli davranir.
R tusu ile top tekrar firlatilabilir.
"""
