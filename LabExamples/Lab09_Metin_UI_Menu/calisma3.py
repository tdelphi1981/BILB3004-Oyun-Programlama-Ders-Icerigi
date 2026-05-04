"""
Lab 09 - Çalışma 3 Başlangıç Kodu
Buton ve Menü

Bu dosya Lab 09 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- Buton sınıfı (rect, hover, tıklama)
- Callback ile olay-işlem ayrımı
- Sonlu durum makinesi (state) ile menü/oyun/pause yönetimi

Lab: 09 - Metin, UI ve Menü Sistemleri
Çalışma: 3 - Buton ve Menü

Çalıştırma: uv run python calisma3.py
"""

import pygame

pygame.init()
ekran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 09 - Çalışma 3: Menü")
saat = pygame.time.Clock()


class Buton:
    def __init__(self, x, y, gen, yuk, metin, renk=(70, 130, 180), callback=None):
        self.rect = pygame.Rect(x, y, gen, yuk)
        self.metin = metin
        self.renk = renk
        self.hover_renk = tuple(min(255, c + 30) for c in renk)
        self.font = pygame.font.Font(None, 28)
        self.uzerinde = False
        # === GOREV 3.5 - Callback ===
        # TODO: a) self.callback = callback   (parametre olarak gelen fonksiyonu sakla)
        # ============================================

    def guncelle(self):
        self.uzerinde = self.rect.collidepoint(pygame.mouse.get_pos())

    def tikla(self, olay):
        if olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
            if self.rect.collidepoint(olay.pos):
                # === GOREV 3.5 - Callback çağrısı ===
                # TODO: b) if self.callback is not None:
                #              self.callback()
                # ====================================
                return True
        return False

    def ciz(self, yuzey):
        r = self.hover_renk if self.uzerinde else self.renk
        pygame.draw.rect(yuzey, r, self.rect, border_radius=5)
        pygame.draw.rect(yuzey, (255, 255, 255), self.rect, 2, border_radius=5)
        m = self.font.render(self.metin, True, (255, 255, 255))
        yuzey.blit(m, m.get_rect(center=self.rect.center))


# === GOREV 3.5 - ButonYoneticisi sınıfı ===
# Birden fazla butonu yönetmek için yardımcı sınıf.
#
# TODO: a) class ButonYoneticisi:
# TODO: b)     def __init__(self):
#                  self.butonlar = []
# TODO: c)     def ekle(self, buton):
#                  self.butonlar.append(buton)
# TODO: d)     def temizle(self):
#                  self.butonlar.clear()
# TODO: e)     def olay_isle(self, olay):
#                  for b in self.butonlar:
#                      b.tikla(olay)
# TODO: f)     def guncelle_ve_ciz(self, yuzey):
#                  for b in self.butonlar:
#                      b.guncelle()
#                      b.ciz(yuzey)
# ===========================================


# Mevcut basit buton listesi (GOREV 3.5/3.6 sonrası ButonYoneticisi'ne taşınacak)
butonlar = [
    Buton(300, 200, 200, 50, "Buton 1"),
    Buton(300, 270, 200, 50, "Buton 2", renk=(50, 150, 50)),
    Buton(300, 340, 200, 50, "Cikis", renk=(180, 50, 50)),
]


# === GOREV 3.6 - Tam Menü Sistemi (state machine) ===
# Üç durum: "menu", "oyun", "pause"
#
# TODO: a) durum = "menu"
# TODO: b) Yardımcı fonksiyonlar:
#              def baslat():
#                  global durum
#                  durum = "oyun"
#              def cikis():
#                  global calistir
#                  calistir = False
#              def devam():
#                  global durum
#                  durum = "oyun"
#              def ana_menuye_don():
#                  global durum
#                  durum = "menu"
#
# TODO: c) Üç ayrı buton listesi (ana_menu_btn, pause_btn) hazırla.
#             ana_menu_btn = [
#                 Buton(300, 250, 200, 50, "Basla", callback=baslat),
#                 Buton(300, 320, 200, 50, "Cikis", renk=(180,50,50), callback=cikis),
#             ]
#             pause_btn = [
#                 Buton(300, 250, 200, 50, "Devam", callback=devam),
#                 Buton(300, 320, 200, 50, "Ana Menu", callback=ana_menuye_don),
#             ]
#
# TODO: d) Oyun döngüsünde:
#              if durum == "menu":      aktif_btn = ana_menu_btn
#              elif durum == "pause":   aktif_btn = pause_btn
#              else:                    aktif_btn = []   # oyun
#
# TODO: e) ESC olayını yakala:
#              if olay.type == pygame.KEYDOWN and olay.key == pygame.K_ESCAPE:
#                  if durum == "oyun":  durum = "pause"
#                  elif durum == "pause": durum = "oyun"
# =====================================================


calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False
        for i, b in enumerate(butonlar):
            if b.tikla(olay):
                if i == 2:
                    calistir = False
                else:
                    print(f"Buton {i + 1} tiklandi")

    for b in butonlar:
        b.guncelle()

    ekran.fill((20, 20, 40))
    for b in butonlar:
        b.ciz(ekran)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 piksel pencere açılır. Ortada üç buton dikey sıralı:
"Buton 1" (mavi), "Buton 2" (yeşil), "Cikis" (kırmızı).
Fareyle üzerine gelinen buton biraz açılır (hover).
Tıklamada konsola "Buton N tiklandi" yazılır, "Cikis" tıklanınca pencere kapanır.

GOREV 3.5 tamamlanınca:
Buton sınıfı callback fonksiyonu kabul eder ve tıklamada otomatik çağırır.
ButonYoneticisi sınıfı buton listesini tek noktadan yönetir.

GOREV 3.6 tamamlanınca:
- Açılışta ana menü görünür (Basla / Cikis butonları).
- Basla'ya basınca "oyun" durumuna geçilir, ekran sade renkli alan olur.
- ESC: oyun <-> pause arasında geçiş yapar (Devam / Ana Menu butonları).
- Cikis veya pencereyi kapatma: programı sonlandırır.
"""
