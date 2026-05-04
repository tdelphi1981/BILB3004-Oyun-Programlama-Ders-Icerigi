"""
Lab 09 - Çalışma 2 Başlangıç Kodu
Sağlık Barı ve HUD

Bu dosya Lab 09 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- pygame.draw.rect ile sağlık barı çizimi
- Oran tabanlı renk değişimi (yeşil/sarı/kırmızı)
- Sınıf yapısı (encapsulation)
- Surface.set_alpha ile yarı şeffaf yüzey

Lab: 09 - Metin, UI ve Menü Sistemleri
Çalışma: 2 - Sağlık Barı ve HUD

Çalıştırma: uv run python calisma2.py
"""

import pygame

pygame.init()
ekran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 09 - Çalışma 2: HUD")
saat = pygame.time.Clock()
font = pygame.font.Font(None, 28)


# === GOREV 2.3 - SaglikBari Sınıfı ===
# Aşağıdaki sınıfı doldurun. Mevcut prosedürel kodu (aşağıda)
# bu sınıfa taşıyın ve oyun döngüsünden sınıfı kullanın.
#
# TODO: a) __init__(self, x, y, gen, yuk, max_can):
#           self.x, self.y, self.gen, self.yuk = x, y, gen, yuk
#           self.max_can = max_can
#           self.can = max_can
# TODO: b) hasar_al(self, miktar):
#           self.can = max(0, self.can - miktar)
# TODO: c) iyiles(self, miktar):
#           self.can = min(self.max_can, self.can + miktar)
# TODO: d) ciz(self, yuzey):
#           oran = self.can / self.max_can
#           doluluk = int(self.gen * oran)
#           if oran > 0.6:   renk = (0, 200, 0)
#           elif oran > 0.3: renk = (255, 200, 0)
#           else:            renk = (200, 0, 0)
#           pygame.draw.rect(yuzey, (60,60,60), (self.x, self.y, self.gen, self.yuk))
#           if doluluk > 0:
#               pygame.draw.rect(yuzey, renk, (self.x, self.y, doluluk, self.yuk))
#           pygame.draw.rect(yuzey, (200,200,200), (self.x, self.y, self.gen, self.yuk), 2)
# ============================================

class SaglikBari:
    pass  # GOREV 2.3 ile değiştir


# Mevcut prosedürel değişkenler (GOREV 2.3 sonrası kaldırılabilir)
can = 100
max_can = 100
skor = 0

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_d:
                can = max(0, can - 15)
            elif olay.key == pygame.K_h:
                can = min(max_can, can + 10)
            elif olay.key == pygame.K_SPACE:
                skor += 25

    ekran.fill((30, 30, 50))

    # === GOREV 2.4 - Yarı Şeffaf HUD Paneli ===
    # HUD elemanlarının arkasına 800x42 boyutunda yarı şeffaf
    # siyah bir panel ekleyin. Surface.set_alpha(150) kullanın.
    #
    # TODO: a) panel = pygame.Surface((800, 42))
    # TODO: b) panel.fill((0, 0, 0))
    # TODO: c) panel.set_alpha(150)
    # TODO: d) ekran.blit(panel, (0, 0))
    # ============================================

    # --- Sağlık barı (prosedürel - GOREV 2.3 ile sınıfa taşınacak) ---
    oran = can / max_can
    doluluk = int(200 * oran)
    if oran > 0.6:
        renk = (0, 200, 0)
    elif oran > 0.3:
        renk = (255, 200, 0)
    else:
        renk = (200, 0, 0)

    pygame.draw.rect(ekran, (60, 60, 60), (10, 10, 200, 20))
    if doluluk > 0:
        pygame.draw.rect(ekran, renk, (10, 10, doluluk, 20))
    pygame.draw.rect(ekran, (200, 200, 200), (10, 10, 200, 20), 2)

    # Can metni
    can_metin = font.render(f"Can: {can}/{max_can}", True, (255, 255, 255))
    ekran.blit(can_metin, (220, 8))

    # Skor (sağ üst)
    skor_metin = font.render(f"Skor: {skor:06d}", True, (255, 215, 0))
    skor_rect = skor_metin.get_rect(topright=(790, 10))
    ekran.blit(skor_metin, skor_rect)

    yardim = font.render(
        "D: Hasar | H: Iyiles | SPACE: +25 puan",
        True, (150, 150, 150)
    )
    yardim_rect = yardim.get_rect(center=(400, 580))
    ekran.blit(yardim, yardim_rect)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 piksel pencere açılır. Sol üstte sağlık barı,
yanında "Can: 100/100" metni, sağ üstte sıfırlanmış skor görünür.
- D tuşu: 15 hasar (sağlık barı kısalır, renk yeşil->sarı->kırmızı)
- H tuşu: 10 iyileşme
- SPACE: skor +25

GOREV 2.3 tamamlanınca:
Aynı görsel davranış SaglikBari sınıfı üzerinden çalışır.
Oyun döngüsü içinde:
    bar = SaglikBari(10, 10, 200, 20, 100)
    ...
    bar.hasar_al(15)
    bar.ciz(ekran)

GOREV 2.4 tamamlanınca:
Üst HUD elemanlarının arkasında yarı şeffaf siyah bir bant belirir.
"""
