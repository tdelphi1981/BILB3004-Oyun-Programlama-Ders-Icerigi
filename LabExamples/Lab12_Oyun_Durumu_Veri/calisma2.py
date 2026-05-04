"""
Lab 12 - Çalışma 2 Başlangıç Kodu
JSON ile Save/Load

Bu dosya Lab 12 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- to_dict / from_dict deseni
- json.dump / json.load
- Atomik yazma (.tmp + replace)
- Yedek dosya (.bak)

Lab: 12 - Oyun Durumu ve Veri Yönetimi
Çalışma: 2 - JSON Save/Load

Çalıştırma: uv run python calisma2.py
"""

import pygame
import json
import os
import tempfile
from pathlib import Path

GENISLIK, YUKSEKLIK = 800, 600


class Oyuncu:
    """Save edilebilir basit oyuncu sınıfı."""

    def __init__(self, x, y, can=5, altin=0):
        self.x = x
        self.y = y
        self.can = can
        self.altin = altin

    def to_dict(self):
        return {"x": self.x, "y": self.y,
                "can": self.can, "altin": self.altin}

    @classmethod
    def from_dict(cls, d):
        return cls(
            x=d["x"], y=d["y"],
            can=d.get("can", 5),
            altin=d.get("altin", 0),
        )


# === GOREV 2.1 - Atomik Yazma ===
# Aşağıdaki kaydet fonksiyonunu atomik yazma desenine çevirin.
# Önce .tmp dosyasına yaz, flush + fsync, sonra replace.
#
# Mevcut "basit" sürüm:
def kaydet(yol, oyuncu):
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(
            {"version": 1, "oyuncu": oyuncu.to_dict()},
            f, indent=2, ensure_ascii=False, sort_keys=True,
        )

# TODO: Atomik versiyona çevir:
# TODO: def kaydet(yol, oyuncu):
# TODO:     yol = Path(yol)
# TODO:     # === GOREV 2.2 - Yedek ===
# TODO:     # if yol.exists():
# TODO:     #     yedek = yol.with_suffix(".json.bak")
# TODO:     #     yedek.write_bytes(yol.read_bytes())
# TODO:
# TODO:     tmp = yol.with_suffix(".json.tmp")
# TODO:     with open(tmp, "w", encoding="utf-8") as f:
# TODO:         json.dump({"version": 1, "oyuncu": oyuncu.to_dict()},
# TODO:                   f, indent=2, ensure_ascii=False, sort_keys=True)
# TODO:         f.flush()
# TODO:         os.fsync(f.fileno())
# TODO:     tmp.replace(yol)


def yukle(yol):
    """Slot'tan oyuncu yükle. Yoksa veya bozuksa None."""
    yol = Path(yol)
    if not yol.exists():
        return None
    try:
        with open(yol, "r", encoding="utf-8") as f:
            d = json.load(f)
    except json.JSONDecodeError:
        # === GOREV 2.2 - Yedek Dosya ===
        # Ana dosya bozuksa .bak'tan yüklemeyi dene
        # TODO: a) yedek = yol.with_suffix(".json.bak")
        # TODO: b) if not yedek.exists():
        # TODO:        return None
        # TODO: c) try:
        # TODO:        with open(yedek, "r", encoding="utf-8") as f:
        # TODO:            d = json.load(f)
        # TODO:    except json.JSONDecodeError:
        # TODO:        return None
        return None
    return Oyuncu.from_dict(d["oyuncu"])


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 12 - Calisma 2: Save/Load")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 26)
    font_k = pygame.font.Font(None, 22)

    # Geçici dizin --- gerçek üretimde Path.home() / ".oyun" kullan
    with tempfile.TemporaryDirectory() as tmp:
        yol = Path(tmp) / "save.json"

        oyuncu = Oyuncu(GENISLIK // 2, YUKSEKLIK // 2)
        mesaj = ""
        mesaj_zaman = 0

        def goster(m):
            nonlocal mesaj, mesaj_zaman
            mesaj = m
            mesaj_zaman = pygame.time.get_ticks()

        calistir = True
        while calistir:
            dt = saat.tick(60) / 1000.0

            for olay in pygame.event.get():
                if olay.type == pygame.QUIT:
                    calistir = False
                elif olay.type == pygame.KEYDOWN:
                    if olay.key == pygame.K_F5:
                        kaydet(yol, oyuncu)
                        goster(f"Kaydedildi: {yol.name}")
                    elif olay.key == pygame.K_F9:
                        yuklenen = yukle(yol)
                        if yuklenen is None:
                            goster("Slot bos veya bozuk.")
                        else:
                            oyuncu = yuklenen
                            goster(f"Yuklendi: x={oyuncu.x}, can={oyuncu.can}")
                    elif olay.key == pygame.K_a:
                        oyuncu.altin += 100
                    elif olay.key == pygame.K_h:
                        oyuncu.can = max(0, oyuncu.can - 1)

            # Hareket
            tuslar = pygame.key.get_pressed()
            hiz = 200
            if tuslar[pygame.K_LEFT]:  oyuncu.x -= hiz * dt
            if tuslar[pygame.K_RIGHT]: oyuncu.x += hiz * dt
            if tuslar[pygame.K_UP]:    oyuncu.y -= hiz * dt
            if tuslar[pygame.K_DOWN]:  oyuncu.y += hiz * dt

            # Çizim
            ekran.fill((20, 30, 40))
            pygame.draw.circle(ekran, (255, 215, 0),
                               (int(oyuncu.x), int(oyuncu.y)), 25)

            # HUD
            hud = font.render(
                f"x: {int(oyuncu.x)}  y: {int(oyuncu.y)}  "
                f"can: {oyuncu.can}  altin: {oyuncu.altin}",
                True, (255, 255, 255))
            ekran.blit(hud, (10, 10))

            ipucu = font_k.render(
                "OK: Hareket  A: +100 altin  H: -1 can  F5: Kaydet  F9: Yukle",
                True, (180, 180, 200))
            ekran.blit(ipucu, ipucu.get_rect(
                center=(GENISLIK // 2, YUKSEKLIK - 20)))

            # Mesaj (2 sn)
            if mesaj and pygame.time.get_ticks() - mesaj_zaman < 2000:
                m = font.render(mesaj, True, (255, 215, 0))
                ekran.blit(m, m.get_rect(center=(GENISLIK // 2, 60)))

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 pencerede sarı top.
- A ile altın artırılabilir, H ile can azaltılabilir.
- F5 mevcut konumu/sayıları kaydeder, F9 geri yükler.
- Üstte HUD: x, y, can, altın.
- Mesajlar 2 saniye süreyle ekranın üst orta kısmında belirir.

GOREV 2.1 tamamlanınca:
- Kaydetme sırasında program çökse bile dosya bozulmaz.

GOREV 2.2 tamamlanınca:
- Ana save dosyası bozuksa otomatik .bak dosyasından yükleme yapılır.
"""
