"""
Lab 09 - Çalışma 4 (Bonus) Başlangıç Kodu
Game Over Ekranı ve Yüksek Skor

Bu dosya Lab 09 föyünün bonus görevini içerir.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- Oyun durumu yönetimi (oynaniyor / game_over)
- Dosyaya yazma/okuma (yüksek skor kaydı)
- Tekrar oynat akışı (state reset)

Lab: 09 - Metin, UI ve Menü Sistemleri
Çalışma: 4 - Game Over ve Yüksek Skor (Bonus)

Çalıştırma: uv run python calisma4.py
"""

import pygame
from pathlib import Path

pygame.init()
ekran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 09 - Bonus: Game Over")
saat = pygame.time.Clock()
buyuk_font = pygame.font.Font(None, 64)
font = pygame.font.Font(None, 32)

YUKSEK_SKOR_DOSYASI = Path("yuksek_skor.txt")


# === GOREV BONUS.1 - Yüksek skoru oku ===
# Açılışta dosyayı oku, yoksa 0 kabul et.
#
# TODO: a) def yuksek_skor_oku() -> int:
#              if YUKSEK_SKOR_DOSYASI.exists():
#                  try:
#                      return int(YUKSEK_SKOR_DOSYASI.read_text().strip())
#                  except ValueError:
#                      return 0
#              return 0
# ============================================


# === GOREV BONUS.2 - Yüksek skoru yaz ===
# Mevcut yüksek skoru aşan değer geldiğinde dosyaya yaz.
#
# TODO: b) def yuksek_skor_yaz(skor: int) -> None:
#              YUKSEK_SKOR_DOSYASI.write_text(str(skor))
# ============================================


class Buton:
    def __init__(self, x, y, gen, yuk, metin, renk=(70, 130, 180)):
        self.rect = pygame.Rect(x, y, gen, yuk)
        self.metin = metin
        self.renk = renk
        self.hover_renk = tuple(min(255, c + 30) for c in renk)
        self.f = pygame.font.Font(None, 28)

    def ciz(self, yuzey):
        uzerinde = self.rect.collidepoint(pygame.mouse.get_pos())
        r = self.hover_renk if uzerinde else self.renk
        pygame.draw.rect(yuzey, r, self.rect, border_radius=5)
        pygame.draw.rect(yuzey, (255, 255, 255), self.rect, 2, border_radius=5)
        m = self.f.render(self.metin, True, (255, 255, 255))
        yuzey.blit(m, m.get_rect(center=self.rect.center))

    def tikla(self, olay):
        return (
            olay.type == pygame.MOUSEBUTTONDOWN
            and olay.button == 1
            and self.rect.collidepoint(olay.pos)
        )


def yeni_oyun():
    return {"can": 100, "skor": 0, "durum": "oynaniyor"}


durum_obj = yeni_oyun()
yuksek_skor = 0  # GOREV BONUS.1 ile yuksek_skor_oku() çağrılacak

tekrar_btn = Buton(300, 380, 200, 50, "Tekrar Oyna", renk=(50, 150, 50))

calistir = True
while calistir:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calistir = False

        if durum_obj["durum"] == "oynaniyor":
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_d:
                    durum_obj["can"] = max(0, durum_obj["can"] - 25)
                elif olay.key == pygame.K_SPACE:
                    durum_obj["skor"] += 10
            if durum_obj["can"] <= 0:
                durum_obj["durum"] = "game_over"
                # === GOREV BONUS.3 - Yüksek skor güncelleme ===
                # Game Over anında oyuncu skoru yüksek skoru aştıysa
                # dosyaya yaz ve hafızadaki yuksek_skor değişkenini güncelle.
                #
                # TODO: c) if durum_obj["skor"] > yuksek_skor:
                #              yuksek_skor = durum_obj["skor"]
                #              yuksek_skor_yaz(yuksek_skor)
                # =============================================

        elif durum_obj["durum"] == "game_over":
            if tekrar_btn.tikla(olay):
                durum_obj = yeni_oyun()

    ekran.fill((25, 25, 45))

    if durum_obj["durum"] == "oynaniyor":
        can_metin = font.render(
            f"Can: {durum_obj['can']}", True, (255, 255, 255)
        )
        skor_metin = font.render(
            f"Skor: {durum_obj['skor']}", True, (255, 215, 0)
        )
        yuksek_metin = font.render(
            f"Yuksek: {yuksek_skor}", True, (200, 200, 200)
        )
        ekran.blit(can_metin, (20, 20))
        ekran.blit(skor_metin, (20, 60))
        ekran.blit(yuksek_metin, (20, 100))

        yardim = font.render(
            "D: Hasar al  |  SPACE: +10 puan", True, (150, 150, 150)
        )
        ekran.blit(yardim, yardim.get_rect(center=(400, 560)))

    else:  # game_over
        baslik = buyuk_font.render("GAME OVER", True, (255, 80, 80))
        ekran.blit(baslik, baslik.get_rect(center=(400, 200)))

        skor_metin = font.render(
            f"Skorunuz: {durum_obj['skor']}", True, (255, 255, 255)
        )
        yuksek_metin = font.render(
            f"Yuksek Skor: {yuksek_skor}", True, (255, 215, 0)
        )
        ekran.blit(skor_metin, skor_metin.get_rect(center=(400, 290)))
        ekran.blit(yuksek_metin, yuksek_metin.get_rect(center=(400, 330)))

        tekrar_btn.ciz(ekran)

    pygame.display.flip()
    saat.tick(60)

pygame.quit()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 piksel pencere açılır.
- Sol üstte Can / Skor / Yuksek değerleri görünür (Yuksek başta 0).
- D tuşu canı 25 azaltır, SPACE skoru 10 artırır.
- Can 0'a düştüğünde GAME OVER ekranı açılır:
    * Skor ve yüksek skor gösterilir.
    * "Tekrar Oyna" butonu oyunu sıfırlar.

GOREV BONUS tamamlanınca:
- Açılışta yuksek_skor.txt dosyasından yüksek skor okunur.
- Game Over anında skor önceki yüksek skoru aşıyorsa dosyaya yazılır.
- Program kapatılıp yeniden açıldığında yüksek skor korunur.
"""
