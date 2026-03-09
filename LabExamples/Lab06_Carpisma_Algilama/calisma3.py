"""
Lab 06 - Calisma 3 Baslangic Kodu
Yercekimi ve Fizik Simulasyonu

Bu dosya Lab 06 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Yercekimi simulasyonu (hiz_y += YERCEKIMI)
- Enerji kaybı ile geri sekme
- Surukle-birak ile firlatma mekanigi
- Sprite tabanli fizik nesneleri

Lab: 06 - Carpisma Algilama ve Fizik Temelleri
Calisma: 3 - Yercekimi ve Fizik Simulasyonu

Calistirma: uv run python calisma3.py
"""

# --- Lab foyundeki ornek kod ---

import pygame

pygame.init()
GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yercekimi Simulasyonu")
saat = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

# Fizik sabitleri
YERCEKIMI = 0.5
SURTUNME = 0.98
ZEMIN_Y = 550


class Top(pygame.sprite.Sprite):
    def __init__(self, x, y, renk=(52, 152, 219)):
        super().__init__()
        self.yaricap = 15
        self.image = pygame.Surface(
            (self.yaricap * 2, self.yaricap * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, renk,
                          (self.yaricap, self.yaricap), self.yaricap)
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz_x = 0.0
        self.hiz_y = 0.0

    def update(self):
        # Yercekimi uygula
        self.hiz_y += YERCEKIMI

        # Surtunme (yatay)
        self.hiz_x *= SURTUNME

        # Konumu guncelle
        self.rect.x += self.hiz_x
        self.rect.y += self.hiz_y

        # Zemin carpisma ve geri sekme
        if self.rect.bottom >= ZEMIN_Y:
            self.rect.bottom = ZEMIN_Y
            self.hiz_y *= -0.7  # Enerji kaybi ile sekme

        # Duvar carpisma
        if self.rect.left < 0:
            self.rect.left = 0
            self.hiz_x *= -0.8
        elif self.rect.right > GENISLIK:
            self.rect.right = GENISLIK
            self.hiz_x *= -0.8


# Gruplar
tum_spritelar = pygame.sprite.Group()

# Baslangic topu
top = Top(GENISLIK // 2, 100)
tum_spritelar.add(top)

surukleniyor = False
baslangic_pos = (0, 0)

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        elif olay.type == pygame.MOUSEBUTTONDOWN:
            if olay.button == 1:
                surukleniyor = True
                baslangic_pos = olay.pos
        elif olay.type == pygame.MOUSEBUTTONUP:
            if olay.button == 1 and surukleniyor:
                surukleniyor = False
                bx, by = baslangic_pos
                ex, ey = olay.pos
                yeni_top = Top(bx, by, (231, 76, 60))
                yeni_top.hiz_x = (bx - ex) * 0.15
                yeni_top.hiz_y = (by - ey) * 0.15
                tum_spritelar.add(yeni_top)

    tum_spritelar.update()

    ekran.fill((20, 20, 40))

    # Zemin cizgisi
    pygame.draw.line(ekran, (100, 100, 100),
                     (0, ZEMIN_Y), (GENISLIK, ZEMIN_Y), 2)

    # Firlatma oku
    if surukleniyor:
        fare = pygame.mouse.get_pos()
        pygame.draw.line(ekran, (241, 196, 15),
                         baslangic_pos, fare, 2)

    tum_spritelar.draw(ekran)

    bilgi = font.render(
        f"Top sayisi: {len(tum_spritelar)}  |  "
        f"Tiklayip surukle: firlatma",
        True, (200, 200, 200))
    ekran.blit(bilgi, (10, 10))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


# === GOREV 3.1 - Yercekimi Degistirme ===
# TODO: a) Yukari/asagi ok tuslariyla YERCEKIMI degerini
#          0.1 ile 2.0 arasinda artirip azaltin
# TODO: b) Mevcut yercekimi degerini ekranda gosterin
# TODO: c) Ay yercekimi (0.08) ve Jupiter yercekimi (1.3)
#          ile deneyip farkliliklari gozlemleyin
# Ipucu:
#   # YERCEKIMI'yi global degil, degisken olarak kullanin:
#   yercekimi = 0.5
#   # Tus kontrolunde:
#   if tuslar[pygame.K_UP]:
#       yercekimi = min(2.0, yercekimi + 0.01)
#   if tuslar[pygame.K_DOWN]:
#       yercekimi = max(0.1, yercekimi - 0.01)
#   # Top.update icinde self.hiz_y += yercekimi kullanin
# ============================================


# === GOREV 3.2 - Zemin Surtunmesi ===
# TODO: a) Zemine temas eden toplar icin ek surtunme uygulayin:
#          zemine degdiginde hiz_x *= 0.92
# TODO: b) Hiz cok kuculdugunude topu tamamen durdurun
#          (abs(hiz_x) < 0.1 ve abs(hiz_y) < 0.5)
# Ipucu:
#   # Top.update icinde, zemin carpisma blogundan sonra:
#   if self.rect.bottom >= ZEMIN_Y:
#       self.hiz_x *= 0.92  # Zemin surtunmesi
#       if abs(self.hiz_x) < 0.1 and abs(self.hiz_y) < 0.5:
#           self.hiz_x = 0
#           self.hiz_y = 0
# ============================================


# === GOREV 3.3 - Toplar Arasi Carpisma ===
# TODO: a) spritecollide() kullanarak toplarin birbirine
#          carpismasini algilayin
# TODO: b) Carpisan iki top birbirinden uzaklasin:
#          hiz vektorlerini ters cevirin
# Ipucu:
#   for top in tum_spritelar:
#       carpisan = pygame.sprite.spritecollide(
#           top, tum_spritelar, False)
#       for diger in carpisan:
#           if diger != top:
#               top.hiz_x, diger.hiz_x = diger.hiz_x, top.hiz_x
#               top.hiz_y, diger.hiz_y = diger.hiz_y, top.hiz_y
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
800x600 piksel boyutunda koyu mavi bir pencere acilir.
Ortada mavi bir top yercekimi ile asagi duser ve zeminden
enerji kaybederek sekerken yavaslar.

Fare ile tiklayip surukleyerek yeni toplar firlatilabilir.
Firlatma yonu ve hizi sari okla gosterilir.
Yeni toplar kirmizi renktedir.

Sol ustte top sayisi ve kullanim bilgisi gosterilir.
"""
