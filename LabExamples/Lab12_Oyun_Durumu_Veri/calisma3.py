"""
Lab 12 - Çalışma 3 Başlangıç Kodu
Çoklu Slot + LoadState

Bu dosya Lab 12 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- SaveManager sınıfı (3 slot)
- Slot özet listesi
- LoadState UI
- SaveState (üzerine yazma onayı)
- Autosave bildirimi

Lab: 12 - Oyun Durumu ve Veri Yönetimi
Çalışma: 3 - Çoklu Slot Sistemi

Çalıştırma: uv run python calisma3.py
"""

import pygame
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

GENISLIK, YUKSEKLIK = 800, 600

pygame.init()


class SaveManager:
    """Çoklu slot kayıt yöneticisi."""

    AUTOSAVE_SLOT = 0

    def __init__(self, dizin):
        self.dizin = Path(dizin)
        self.dizin.mkdir(parents=True, exist_ok=True)
        self._son_auto = 0.0

    def slot_yolu(self, slot):
        return self.dizin / f"slot{slot}.json"

    def kaydet(self, slot, veri):
        yol = self.slot_yolu(slot)

        # Yedek
        if yol.exists():
            yedek = yol.with_suffix(".json.bak")
            yedek.write_bytes(yol.read_bytes())

        # Atomik
        tmp = yol.with_suffix(".json.tmp")
        veri_full = {
            "version": 1,
            "kayit_zamani": datetime.now().isoformat(timespec="seconds"),
            **veri,
        }
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(veri_full, f, indent=2,
                      ensure_ascii=False, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
        tmp.replace(yol)

    def yukle(self, slot):
        yol = self.slot_yolu(slot)
        if not yol.exists():
            return None
        try:
            with open(yol, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            yedek = yol.with_suffix(".json.bak")
            if not yedek.exists():
                return None
            try:
                with open(yedek, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None

    def slot_ozetleri(self, n=3):
        sonuc = []
        for i in range(1, n + 1):
            yol = self.slot_yolu(i)
            if not yol.exists():
                sonuc.append({"slot": i, "bos": True})
                continue
            try:
                with open(yol, "r", encoding="utf-8") as f:
                    veri = json.load(f)
                sonuc.append({
                    "slot": i, "bos": False,
                    "oyuncu_adi": veri.get("oyuncu_adi", "?"),
                    "altin": veri.get("altin", 0),
                    "sure": veri.get("sure", 0),
                    "zaman": veri.get("kayit_zamani", "?"),
                })
            except json.JSONDecodeError:
                sonuc.append({"slot": i, "bos": False, "bozuk": True})
        return sonuc

    def sil(self, slot):
        yol = self.slot_yolu(slot)
        bak = yol.with_suffix(".json.bak")
        if yol.exists(): yol.unlink()
        if bak.exists(): bak.unlink()

    # === GOREV 3.2 - Autosave ===
    # Aşağıdaki autosave_kontrol metodunu tamamlayın.
    # Eğer son autosave'den itibaren self.aralik saniye geçtiyse
    # AUTOSAVE_SLOT'a yaz ve True döndür.
    aralik = 5.0   # saniye

    def autosave_kontrol(self, oyun_zamani, veri):
        # TODO: a) if oyun_zamani - self._son_auto >= self.aralik:
        # TODO: b)     self.kaydet(self.AUTOSAVE_SLOT, veri)
        # TODO: c)     self._son_auto = oyun_zamani
        # TODO: d)     return True
        # TODO: e) return False
        return False


# Basit state altyapısı
class State:
    def __init__(self, manager): self.manager = manager
    def gir(self): pass
    def cik(self): pass
    def olaylari_isle(self, olaylar): pass
    def guncelle(self, dt): pass
    def ciz(self, ekran): pass


class StateManager:
    def __init__(self): self._yigin = []
    @property
    def aktif(self): return self._yigin[-1] if self._yigin else None
    def it(self, s): self._yigin.append(s); s.gir()
    def pop(self):
        if self._yigin: self._yigin.pop().cik()
    def degistir(self, s):
        if self._yigin: self.pop()
        self.it(s)


class LoadState(State):
    """Yükleme menüsü --- slot listesi, seçim, silme."""

    def __init__(self, manager, save_mgr):
        super().__init__(manager)
        self.save_mgr = save_mgr
        self.secili = 0

    def gir(self):
        self.font_b = pygame.font.Font(None, 48)
        self.font_o = pygame.font.Font(None, 28)
        self.font_k = pygame.font.Font(None, 20)
        self._yenile()

    def _yenile(self):
        self.slotlar = self.save_mgr.slot_ozetleri(n=3)

    def olaylari_isle(self, olaylar):
        for olay in olaylar:
            if olay.type != pygame.KEYDOWN:
                continue
            if olay.key == pygame.K_DOWN:
                self.secili = (self.secili + 1) % len(self.slotlar)
            elif olay.key == pygame.K_UP:
                self.secili = (self.secili - 1) % len(self.slotlar)
            elif olay.key == pygame.K_RETURN:
                slot = self.secili + 1
                veri = self.save_mgr.yukle(slot)
                if veri is not None:
                    self.manager.pop()
                    # Burada PlayState'e geçilebilir; demo için sadece pop
            elif olay.key == pygame.K_DELETE:
                self.save_mgr.sil(self.secili + 1)
                self._yenile()
            elif olay.key == pygame.K_ESCAPE:
                self.manager.pop()

    def ciz(self, ekran):
        ekran.fill((20, 20, 40))
        baslik = self.font_b.render("KAYIT YUKLE", True, (255, 215, 0))
        ekran.blit(baslik, baslik.get_rect(center=(GENISLIK // 2, 60)))

        for i, ozet in enumerate(self.slotlar):
            y = 150 + i * 110
            renk = (255, 255, 255) if i == self.secili else (160, 160, 180)
            self._slot_kutu_ciz(ekran, ozet, y, renk)

        ipucu = self.font_k.render(
            "OK: Sec  ENTER: Yukle  DEL: Sil  ESC: Geri",
            True, (200, 200, 200))
        ekran.blit(ipucu, ipucu.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 30)))

    def _slot_kutu_ciz(self, ekran, ozet, y, renk):
        cerceve = pygame.Rect(120, y, GENISLIK - 240, 90)
        pygame.draw.rect(ekran, renk, cerceve, 2)
        if ozet.get("bos"):
            metin = self.font_o.render(
                f"Slot {ozet['slot']}: -- BOS --", True, renk)
            ekran.blit(metin, metin.get_rect(center=cerceve.center))
            return
        if ozet.get("bozuk"):
            metin = self.font_o.render(
                f"Slot {ozet['slot']}: BOZUK", True, (255, 80, 80))
            ekran.blit(metin, metin.get_rect(center=cerceve.center))
            return
        ust = self.font_o.render(
            f"Slot {ozet['slot']}: {ozet['oyuncu_adi']}", True, renk)
        alt = self.font_k.render(
            f"{int(ozet['sure'])}sn | {ozet['altin']} altin",
            True, renk)
        zaman = self.font_k.render(ozet['zaman'], True, (140, 140, 160))
        ekran.blit(ust, (cerceve.x + 15, cerceve.y + 10))
        ekran.blit(alt, (cerceve.x + 15, cerceve.y + 40))
        ekran.blit(zaman, (cerceve.x + 15, cerceve.y + 62))


# === GOREV 3.1 - SaveState ===
# LoadState'e benzer ama ENTER ile slota YAZAR (yüklemez).
# Dolu slot üzerine yazılırken Y/N onayı sor.
#
# class SaveState(State):
#     def __init__(self, manager, save_mgr, oyun_durumu):
#         super().__init__(manager)
#         self.save_mgr = save_mgr
#         self.oyun_durumu = oyun_durumu
#         self.secili = 0
#         self.onay_modu = False
#
#     def gir(self):
#         # ... LoadState ile benzer ...
#
#     def olaylari_isle(self, olaylar):
#         for olay in olaylar:
#             if olay.type != pygame.KEYDOWN: continue
#             if self.onay_modu:
#                 if olay.key == pygame.K_y:
#                     self._kaydet()
#                     self.onay_modu = False
#                 elif olay.key == pygame.K_n:
#                     self.onay_modu = False
#             else:
#                 # ... yön + ENTER ...
#                 # ENTER: dolu slot ise self.onay_modu = True
#                 # bos slot ise dogrudan _kaydet()


def main():
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 12 - Calisma 3: Coklu Slot")
    saat = pygame.time.Clock()

    with tempfile.TemporaryDirectory() as tmp:
        sm = SaveManager(dizin=tmp)
        # Test verisi: birkaç slot dolu
        sm.kaydet(1, {"oyuncu_adi": "Ayse", "altin": 1250, "sure": 1820.5})
        sm.kaydet(3, {"oyuncu_adi": "Sukru", "altin": 5000, "sure": 5400})

        manager = StateManager()
        manager.it(LoadState(manager, sm))

        calistir = True
        while calistir and manager.aktif:
            saat.tick(60)
            olaylar = pygame.event.get()
            for olay in olaylar:
                if olay.type == pygame.QUIT:
                    calistir = False
            manager.aktif.olaylari_isle(olaylar)
            manager.aktif.ciz(ekran)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 pencerede yükleme menüsü.
- Slot 1: Ayse | 1820sn | 1250 altin
- Slot 2: -- BOS --
- Slot 3: Sukru | 5400sn | 5000 altin
- OK ile seç, ENTER ile yükle (LoadState pop), DEL ile sil.

GOREV 3.1 tamamlanınca:
SaveState oluşturulup test edilebilir; dolu slota yazarken onay sorulur.

GOREV 3.2 tamamlanınca:
SaveManager.autosave_kontrol her 5 saniyede bir slot 0'a yazar.
"""
