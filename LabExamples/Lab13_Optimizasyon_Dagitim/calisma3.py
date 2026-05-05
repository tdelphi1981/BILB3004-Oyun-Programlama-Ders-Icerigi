"""
Lab 13 - Çalışma 3 Başlangıç Kodu
FSM ile Akıllı Düşman

Bu dosya Lab 13 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- Finite State Machine (FSM) tasarımı
- Durum geçiş koşulları
- Mesafe ve zaman tabanlı tetikleyiciler
- 5 durumlu davranış: idle / patrol / chase / attack / cooldown

Lab: 13 - Optimizasyon ve Dağıtım
Çalışma: 3 - FSM ile Akıllı Düşman

Çalıştırma: uv run python calisma3.py
Tuşlar: OK -> Oyuncuyu hareket ettir
        ESC -> Çıkış
"""

import math

import pygame

GENISLIK, YUKSEKLIK = 800, 600

# Hızlar
OYUNCU_HIZ = 200      # px / sn
PATROL_HIZ = 60       # px / sn
CHASE_HIZ = 120       # px / sn

# Mesafeler
ALGI_MESAFESI = 200   # patrol -> chase
SALDIRI_MESAFESI = 50  # chase -> attack
KACIS_MESAFESI = 300  # chase -> patrol (oyuncu kaçtı)

# Zamanlar (saniye)
IDLE_SURESI = 2.0
ATTACK_SURESI = 0.5
COOLDOWN_SURESI = 1.0

# Durum renkleri (HUD için)
DURUM_RENKLERI = {
    "idle":     (180, 180, 180),
    "patrol":   (100, 200, 255),
    "chase":    (255, 200, 80),
    "attack":   (255, 80, 80),
    "cooldown": (160, 100, 200),
}


class Oyuncu:
    """Klavye ile kontrol edilen mavi top."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 14

    def guncelle(self, dt, tuslar):
        if tuslar[pygame.K_LEFT]:  self.x -= OYUNCU_HIZ * dt
        if tuslar[pygame.K_RIGHT]: self.x += OYUNCU_HIZ * dt
        if tuslar[pygame.K_UP]:    self.y -= OYUNCU_HIZ * dt
        if tuslar[pygame.K_DOWN]:  self.y += OYUNCU_HIZ * dt
        # Sınırlar
        self.x = max(self.r, min(GENISLIK - self.r, self.x))
        self.y = max(self.r, min(YUKSEKLIK - self.r, self.y))

    def ciz(self, ekran):
        pygame.draw.circle(ekran, (100, 180, 255), (int(self.x), int(self.y)), self.r)


class Dusman:
    """5 durumlu FSM ile çalışan düşman."""

    def __init__(self, x, y, devriye_noktalari):
        self.x = x
        self.y = y
        self.r = 16
        self.durum = "idle"
        self.zamanlayici = 0.0
        self.devriye = devriye_noktalari
        self.hedef_idx = 0

    # ----- Yardımcılar -----

    def _gecis(self, yeni_durum):
        """Durumu değiştirip zamanlayıcıyı sıfırlar."""
        self.durum = yeni_durum
        self.zamanlayici = 0.0

    def mesafe(self, oyuncu):
        return math.hypot(self.x - oyuncu.x, self.y - oyuncu.y)

    def _hedefe_yurut(self, hx, hy, hiz, dt):
        """(hx, hy) noktasına doğru hiz*dt kadar yaklaş."""
        dx, dy = hx - self.x, hy - self.y
        uzaklik = math.hypot(dx, dy)
        if uzaklik < 1e-3:
            return
        self.x += (dx / uzaklik) * hiz * dt
        self.y += (dy / uzaklik) * hiz * dt

    # ----- FSM Çekirdeği -----

    def guncelle(self, dt, oyuncu):
        self.zamanlayici += dt
        d = self.mesafe(oyuncu)

        if self.durum == "idle":
            # === GOREV 3.1 - idle -> patrol ===
            # 2 saniye bekle, sonra patrol durumuna geç.
            # TODO: a) if self.zamanlayici >= IDLE_SURESI:
            # TODO: b)     self._gecis("patrol")
            pass

        elif self.durum == "patrol":
            # === GOREV 3.2 - patrol -> chase ===
            # a) Hedef noktaya doğru PATROL_HIZ ile yürü.
            # b) Hedefe 5 piksel yaklaşırsan hedef_idx'i bir ilerlet.
            # c) Oyuncuya mesafe < ALGI_MESAFESI ise chase'e geç.
            # TODO: a) hx, hy = self.devriye[self.hedef_idx]
            # TODO: b) self._hedefe_yurut(hx, hy, PATROL_HIZ, dt)
            # TODO: c) if math.hypot(hx - self.x, hy - self.y) < 5:
            # TODO:        self.hedef_idx = (self.hedef_idx + 1) % len(self.devriye)
            # TODO: d) if d < ALGI_MESAFESI:
            # TODO:        self._gecis("chase")
            pass

        elif self.durum == "chase":
            # === GOREV 3.3 - chase -> attack / patrol ===
            # a) Oyuncuya doğru CHASE_HIZ ile git.
            # b) d < SALDIRI_MESAFESI ise attack'a geç.
            # c) d > KACIS_MESAFESI ise oyuncu kaçtı --> patrol'e dön.
            # TODO: a) self._hedefe_yurut(oyuncu.x, oyuncu.y, CHASE_HIZ, dt)
            # TODO: b) if d < SALDIRI_MESAFESI:
            # TODO:        self._gecis("attack")
            # TODO: c) elif d > KACIS_MESAFESI:
            # TODO:        self._gecis("patrol")
            pass

        elif self.durum == "attack":
            # === GOREV 3.4a - attack -> cooldown ===
            # 0.5 saniye saldırı animasyonu (yerinde dur), sonra cooldown.
            # TODO: a) if self.zamanlayici >= ATTACK_SURESI:
            # TODO: b)     self._gecis("cooldown")
            pass

        elif self.durum == "cooldown":
            # === GOREV 3.4b - cooldown -> chase ===
            # 1.0 saniye bekle, sonra tekrar chase'e dön.
            # TODO: a) if self.zamanlayici >= COOLDOWN_SURESI:
            # TODO: b)     self._gecis("chase")
            pass

    def ciz(self, ekran, font):
        # Düşman gövdesi
        pygame.draw.circle(ekran, DURUM_RENKLERI[self.durum],
                           (int(self.x), int(self.y)), self.r)
        # Saldırı halkası
        if self.durum == "attack":
            pygame.draw.circle(ekran, (255, 80, 80),
                               (int(self.x), int(self.y)),
                               SALDIRI_MESAFESI, 2)
        # Algı çemberi (patrol durumunda görünür)
        if self.durum == "patrol":
            pygame.draw.circle(ekran, (100, 100, 100),
                               (int(self.x), int(self.y)),
                               ALGI_MESAFESI, 1)
        # Durum etiketi
        etiket = font.render(self.durum.upper(), True, (255, 255, 255))
        ekran.blit(etiket, etiket.get_rect(
            center=(int(self.x), int(self.y) - self.r - 14)))


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 13 - Calisma 3: FSM Dusman")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 22)
    font_b = pygame.font.Font(None, 28)

    oyuncu = Oyuncu(120, YUKSEKLIK // 2)
    devriye = [(550, 150), (700, 300), (550, 450), (400, 300)]
    dusman = Dusman(550, 300, devriye)

    calistir = True
    while calistir:
        dt = saat.tick(60) / 1000.0

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN and olay.key == pygame.K_ESCAPE:
                calistir = False

        tuslar = pygame.key.get_pressed()
        oyuncu.guncelle(dt, tuslar)
        dusman.guncelle(dt, oyuncu)

        # Çizim
        ekran.fill((20, 25, 35))
        # Devriye noktaları
        for (px, py) in devriye:
            pygame.draw.circle(ekran, (60, 80, 100), (px, py), 4)
        oyuncu.ciz(ekran)
        dusman.ciz(ekran, font)

        # HUD
        bilgi = font_b.render(
            f"Durum: {dusman.durum.upper()}   "
            f"Mesafe: {dusman.mesafe(oyuncu):.0f}   "
            f"FPS: {saat.get_fps():.0f}",
            True, (255, 255, 255))
        ekran.blit(bilgi, (10, 10))
        ipucu = font.render(
            "OK: Hareket   ESC: Cikis",
            True, (180, 180, 200))
        ekran.blit(ipucu, ipucu.get_rect(
            center=(GENISLIK // 2, YUKSEKLIK - 20)))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI (GÖREV'ler tamamlanınca):
----------------------------------------
800x600 pencerede:
- Mavi top (oyuncu) ok tuşları ile hareket eder.
- Düşman 2 sn bekler, sonra devriye noktaları arasında dolaşır.
- Oyuncu 200 piksele yaklaşırsa düşman onu kovalar (turuncu).
- 50 piksel mesafede saldırır (kırmızı halka).
- Saldırı sonrası 1 sn cooldown (mor), tekrar kovalar.
- Oyuncu 300 piksel uzaklaşırsa düşman patrol'e döner (mavi).
"""
