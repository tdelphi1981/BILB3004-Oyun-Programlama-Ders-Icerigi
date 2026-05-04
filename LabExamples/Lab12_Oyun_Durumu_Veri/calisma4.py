"""
Lab 12 - Çalışma 4 Başlangıç Kodu
Settings Sınıfı + Ayar Menüsü

Bu dosya Lab 12 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- Settings sınıfı (3 erişim stili)
- Slider, toggle, seçim, tuş atama widget'ları
- Tuş çakışma kontrolü
- Anında uygulama (pygame_uygula)
- Sıfırlama (reset to defaults)

Lab: 12 - Oyun Durumu ve Veri Yönetimi
Çalışma: 4 - Settings + Ayar Menüsü

Çalıştırma: uv run python calisma4.py
"""

import pygame
import json
import tempfile
from pathlib import Path

GENISLIK, YUKSEKLIK = 800, 600

pygame.init()

DEFAULTS = {
    "version": 1,
    "ses_genel": 1.0,
    "ses_muzik": 0.7,
    "ses_efekt": 1.0,
    "sessiz": False,
    "tam_ekran": False,
    "tus_sol": pygame.K_LEFT,
    "tus_sag": pygame.K_RIGHT,
    "tus_zipla": pygame.K_SPACE,
    "zorluk": "orta",
    "dil": "tr",
}


class Settings:
    def __init__(self, yol):
        self.yol = Path(yol)
        self.yol.parent.mkdir(parents=True, exist_ok=True)
        self._veri = dict(DEFAULTS)
        self.yukle()

    def yukle(self):
        if not self.yol.exists():
            return
        try:
            with open(self.yol, "r", encoding="utf-8") as f:
                kullanici = json.load(f)
        except json.JSONDecodeError:
            return
        for k, v in kullanici.items():
            if k in DEFAULTS:
                self._veri[k] = v

    def kaydet(self):
        with open(self.yol, "w", encoding="utf-8") as f:
            json.dump(self._veri, f, indent=2,
                      ensure_ascii=False, sort_keys=True)

    def __getitem__(self, k): return self._veri[k]
    def __setitem__(self, k, v):
        self._veri[k] = v
        self.kaydet()

    # === GOREV 4.3 - Sıfırlama ===
    # Aşağıdaki sifirla metodunu tamamlayın:
    # TODO: def sifirla(self):
    # TODO:     self._veri = dict(DEFAULTS)
    # TODO:     self.kaydet()


AYAR_SATIRLARI = [
    {"tip": "slider", "ad": "ses_genel",  "etiket": "Genel Ses",
     "min": 0.0, "max": 1.0, "step": 0.05},
    {"tip": "slider", "ad": "ses_muzik",  "etiket": "Muzik Sesi",
     "min": 0.0, "max": 1.0, "step": 0.05},
    {"tip": "slider", "ad": "ses_efekt",  "etiket": "Efekt Sesi",
     "min": 0.0, "max": 1.0, "step": 0.05},
    {"tip": "toggle", "ad": "sessiz",     "etiket": "Sessiz Mod"},
    {"tip": "toggle", "ad": "tam_ekran",  "etiket": "Tam Ekran"},
    {"tip": "secim",  "ad": "zorluk",     "etiket": "Zorluk",
     "secenekler": ["kolay", "orta", "zor"]},
    {"tip": "tus",    "ad": "tus_sol",    "etiket": "Sol"},
    {"tip": "tus",    "ad": "tus_sag",    "etiket": "Sag"},
    {"tip": "tus",    "ad": "tus_zipla",  "etiket": "Zipla"},
    # === GOREV 4.3 - Sıfırlama Satırı ===
    # En altta "Sifirla" satırı eklenir (özel tip):
    # TODO: {"tip": "aksiyon", "ad": "sifirla", "etiket": "TUMUNU SIFIRLA"},
]


class SettingsState:
    def __init__(self, settings):
        self.settings = settings
        self.satirlar = AYAR_SATIRLARI
        self.secili = 0
        self.tus_atama_modu = False
        self.font_b = pygame.font.Font(None, 40)
        self.font_o = pygame.font.Font(None, 24)
        self.font_k = pygame.font.Font(None, 18)
        self.uyari = ""
        self.uyari_zaman = 0

    def _uyari(self, m):
        self.uyari = m
        self.uyari_zaman = pygame.time.get_ticks()

    def olaylari_isle(self, olaylar):
        for olay in olaylar:
            if olay.type != pygame.KEYDOWN:
                continue
            if self.tus_atama_modu:
                self._tus_atandi(olay.key)
            else:
                self._normal_olay(olay.key)

    def _normal_olay(self, tus):
        satir = self.satirlar[self.secili]
        if tus == pygame.K_DOWN:
            self.secili = (self.secili + 1) % len(self.satirlar)
        elif tus == pygame.K_UP:
            self.secili = (self.secili - 1) % len(self.satirlar)
        elif tus == pygame.K_RIGHT:
            self._deger_degistir(satir, +1)
        elif tus == pygame.K_LEFT:
            self._deger_degistir(satir, -1)
        elif tus == pygame.K_RETURN:
            if satir["tip"] == "tus":
                self.tus_atama_modu = True
            elif satir["tip"] == "toggle":
                self.settings[satir["ad"]] = not self.settings[satir["ad"]]
                # === GOREV 4.2 - Anında Uygulama ===
                # if satir["ad"] in ("sessiz", "tam_ekran"):
                #     self._pygame_uygula()
            elif satir["tip"] == "aksiyon":
                # === GOREV 4.3 ===
                # if satir["ad"] == "sifirla":
                #     self.settings.sifirla()
                pass

    def _deger_degistir(self, satir, yon):
        ad = satir["ad"]
        tip = satir["tip"]
        if tip == "slider":
            mevcut = self.settings[ad]
            yeni = max(satir["min"], min(satir["max"],
                                          mevcut + satir["step"] * yon))
            self.settings[ad] = round(yeni, 2)
            # === GOREV 4.2 - Anında Uygulama ===
            # if ad in ("ses_genel", "ses_muzik", "ses_efekt"):
            #     self._pygame_uygula()
        elif tip == "secim":
            secenekler = satir["secenekler"]
            mevcut = self.settings[ad]
            try:
                idx = secenekler.index(mevcut)
            except ValueError:
                idx = 0
            self.settings[ad] = secenekler[(idx + yon) % len(secenekler)]

    def _tus_atandi(self, tus):
        if tus == pygame.K_ESCAPE:
            self.tus_atama_modu = False
            return

        # === GOREV 4.1 - Çakışma Kontrolü ===
        # Aşağıdaki kodu açın ve doldurun:
        # TODO: a) for satir in self.satirlar:
        # TODO:        if satir["tip"] != "tus":
        # TODO:            continue
        # TODO:        if (satir["ad"] != self.satirlar[self.secili]["ad"]
        # TODO:                and self.settings[satir["ad"]] == tus):
        # TODO:            self._uyari(f"Bu tus zaten atanmis: {satir['etiket']}")
        # TODO:            self.tus_atama_modu = False
        # TODO:            return

        self.settings[self.satirlar[self.secili]["ad"]] = tus
        self.tus_atama_modu = False

    def _pygame_uygula(self):
        """Ayarları pygame'e uygula --- GOREV 4.2 için yardımcı."""
        if self.settings["sessiz"]:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(
                self.settings["ses_muzik"] * self.settings["ses_genel"])
        # Tam ekran toggle (basit demo --- gerçekte ayrı kullanılmalı)

    def ciz(self, ekran):
        ekran.fill((25, 25, 50))
        baslik = self.font_b.render("AYARLAR", True, (255, 215, 0))
        ekran.blit(baslik, baslik.get_rect(center=(GENISLIK // 2, 40)))

        for i, satir in enumerate(self.satirlar):
            y = 100 + i * 40
            renk = (255, 255, 255) if i == self.secili else (160, 160, 180)
            if satir["tip"] == "aksiyon":
                renk = (255, 100, 100) if i == self.secili else (200, 80, 80)
            self._satir_ciz(ekran, satir, y, renk)

        if self.tus_atama_modu:
            self._tus_atama_overlay(ekran)

        if self.uyari and pygame.time.get_ticks() - self.uyari_zaman < 3000:
            u = self.font_o.render(self.uyari, True, (255, 100, 100))
            ekran.blit(u, u.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 50)))

        ipucu = self.font_k.render(
            "OK: Sec  YON: Degistir  ENTER: Toggle/Tus",
            True, (180, 180, 200))
        ekran.blit(ipucu, ipucu.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 20)))

    def _satir_ciz(self, ekran, satir, y, renk):
        etiket = self.font_o.render(satir["etiket"], True, renk)
        ekran.blit(etiket, (100, y))

        ad = satir["ad"]
        tip = satir["tip"]

        if tip == "aksiyon":
            return   # Sadece etiket --- değer yok

        deger = self.settings[ad]
        if tip == "slider":
            bar = pygame.Rect(380, y + 8, 250, 8)
            pygame.draw.rect(ekran, (60, 60, 80), bar)
            doluluk = int(250 * (deger - satir["min"]) /
                          (satir["max"] - satir["min"]))
            dolu = pygame.Rect(380, y + 8, doluluk, 8)
            pygame.draw.rect(ekran, renk, dolu)
            yuzde = self.font_o.render(f"{int(deger * 100)}%", True, renk)
            ekran.blit(yuzde, (650, y))
        elif tip == "toggle":
            metin = "ACIK" if deger else "KAPALI"
            ekran.blit(self.font_o.render(metin, True, renk), (380, y))
        elif tip == "secim":
            ekran.blit(self.font_o.render(f"< {deger} >", True, renk), (380, y))
        elif tip == "tus":
            isim = pygame.key.name(deger).upper()
            ekran.blit(self.font_o.render(isim, True, renk), (380, y))

    def _tus_atama_overlay(self, ekran):
        kararti = pygame.Surface(ekran.get_size())
        kararti.set_alpha(180)
        kararti.fill((0, 0, 0))
        ekran.blit(kararti, (0, 0))
        yazi = self.font_b.render("TUSA BASIN...", True, (255, 215, 0))
        ekran.blit(yazi, yazi.get_rect(center=(GENISLIK // 2, 280)))
        ipucu = self.font_o.render(
            "ESC: Iptal", True, (200, 200, 200))
        ekran.blit(ipucu, ipucu.get_rect(center=(GENISLIK // 2, 320)))


def main():
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 12 - Calisma 4: Settings")
    saat = pygame.time.Clock()

    with tempfile.TemporaryDirectory() as tmp:
        s = Settings(yol=Path(tmp) / "settings.json")
        ss = SettingsState(s)

        calistir = True
        while calistir:
            saat.tick(60)
            olaylar = pygame.event.get()
            for olay in olaylar:
                if olay.type == pygame.QUIT:
                    calistir = False
            ss.olaylari_isle(olaylar)
            ss.ciz(ekran)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 pencerede ayar menüsü.
- 9 ayar satırı (3 slider + 2 toggle + 1 seçim + 3 tuş).
- OK ile seç, YON ile değiştir, ENTER toggle veya tuş atama.
- Tuş atama modunda: "TUSA BASIN..." overlay.
- Değişiklikler anında settings.json'a yazılır.

GOREV 4.1 tamamlanınca:
- Çakışan tuş atanmaya çalışıldığında 3 saniye süreyle kırmızı uyarı.

GOREV 4.2 tamamlanınca:
- Slider değişimleri anında ses sistemine uygulanır.

GOREV 4.3 tamamlanınca:
- En altta "TUMUNU SIFIRLA" kırmızı satırı.
- ENTER ile tüm ayarlar varsayılana döner.
"""
