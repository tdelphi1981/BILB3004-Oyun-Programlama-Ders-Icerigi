"""
Lab 12 - Çalışma 1 Başlangıç Kodu
Mini State Machine (Menu - Play - Pause)

Bu dosya Lab 12 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- Soyut State sınıfı + StateManager
- Yığın tabanlı state organizasyonu
- Pause snapshot tekniği

Lab: 12 - Oyun Durumu ve Veri Yönetimi
Çalışma: 1 - Mini State Machine

Çalıştırma: uv run python calisma1.py
"""

import pygame

GENISLIK, YUKSEKLIK = 800, 600

pygame.init()


# === SOYUT STATE ALTYAPISI (verilmiş) ===
class State:
    def __init__(self, manager):
        self.manager = manager

    def gir(self): pass
    def cik(self): pass
    def olaylari_isle(self, olaylar): pass
    def guncelle(self, dt): pass
    def ciz(self, ekran): pass


class StateManager:
    def __init__(self):
        self._yigin = []

    @property
    def aktif(self):
        return self._yigin[-1] if self._yigin else None

    def it(self, state):
        self._yigin.append(state)
        state.gir()

    def pop(self):
        if self._yigin:
            self._yigin.pop().cik()

    def degistir(self, state):
        if self._yigin:
            self.pop()
        self.it(state)


# === MENU STATE (verilmiş) ===
class MenuState(State):
    def gir(self):
        self.font_b = pygame.font.Font(None, 64)
        self.font_o = pygame.font.Font(None, 32)
        self.secili = 0
        self.secenekler = ["Baslat", "Cikis"]

    def olaylari_isle(self, olaylar):
        for olay in olaylar:
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_DOWN:
                    self.secili = (self.secili + 1) % len(self.secenekler)
                elif olay.key == pygame.K_UP:
                    self.secili = (self.secili - 1) % len(self.secenekler)
                elif olay.key == pygame.K_RETURN:
                    if self.secenekler[self.secili] == "Baslat":
                        self.manager.degistir(PlayState(self.manager))
                    else:
                        self.manager.pop()

    def ciz(self, ekran):
        ekran.fill((25, 25, 50))
        baslik = self.font_b.render("STATE DEMO", True, (255, 215, 0))
        ekran.blit(baslik, baslik.get_rect(center=(GENISLIK // 2, 150)))
        for i, s in enumerate(self.secenekler):
            renk = (255, 255, 255) if i == self.secili else (140, 140, 160)
            yuzey = self.font_o.render(s, True, renk)
            ekran.blit(yuzey, yuzey.get_rect(
                center=(GENISLIK // 2, 320 + i * 50)))


# === PLAY STATE (yarısı verilmiş, yarısı GOREV) ===
class PlayState(State):
    def gir(self):
        self.font = pygame.font.Font(None, 24)
        self.x = GENISLIK // 2
        self.y = YUKSEKLIK // 2
        self.can = 3   # === GOREV 1.2 - Hayat Sayacı ===

    def olaylari_isle(self, olaylar):
        for olay in olaylar:
            if olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    self.manager.it(PauseState(self.manager, snapshot=self))

                # === GOREV 1.1 - X Tuşu ile GameOver ===
                # X tuşuna basıldığında GameOverState'e geç
                # TODO: a) elif olay.key == pygame.K_x:
                # TODO: b)     self.manager.degistir(GameOverState(self.manager))

                # === GOREV 1.2 - SPACE ile Can Azalt ===
                # SPACE tuşuna her basışta can 1 azalsın.
                # Can sıfıra ulaşırsa otomatik GameOverState'e geç.
                # TODO: a) elif olay.key == pygame.K_SPACE:
                # TODO: b)     self.can -= 1
                # TODO: c)     if self.can <= 0:
                # TODO: d)         self.manager.degistir(GameOverState(self.manager))

    def guncelle(self, dt):
        tuslar = pygame.key.get_pressed()
        hiz = 240
        if tuslar[pygame.K_LEFT]:  self.x -= hiz * dt
        if tuslar[pygame.K_RIGHT]: self.x += hiz * dt
        if tuslar[pygame.K_UP]:    self.y -= hiz * dt
        if tuslar[pygame.K_DOWN]:  self.y += hiz * dt

    def ciz(self, ekran):
        ekran.fill((20, 30, 40))
        pygame.draw.circle(ekran, (255, 215, 0),
                           (int(self.x), int(self.y)), 25)
        info = self.font.render(
            f"Can: {self.can}  ESC: Pause  X: GameOver  SPACE: -1 can",
            True, (200, 200, 200))
        ekran.blit(info, (10, 10))


# === PAUSE STATE (verilmiş --- snapshot tekniği) ===
class PauseState(State):
    def __init__(self, manager, snapshot=None):
        super().__init__(manager)
        self.snapshot = snapshot

    def gir(self):
        self.font_b = pygame.font.Font(None, 64)
        self.font_o = pygame.font.Font(None, 28)
        self.altyuz = pygame.Surface((GENISLIK, YUKSEKLIK))
        if self.snapshot is not None:
            self.snapshot.ciz(self.altyuz)
        kararti = pygame.Surface((GENISLIK, YUKSEKLIK))
        kararti.set_alpha(160)
        kararti.fill((0, 0, 0))
        self.altyuz.blit(kararti, (0, 0))

    def olaylari_isle(self, olaylar):
        for olay in olaylar:
            if olay.type == pygame.KEYDOWN and olay.key == pygame.K_ESCAPE:
                self.manager.pop()

    def ciz(self, ekran):
        ekran.blit(self.altyuz, (0, 0))
        yazi = self.font_b.render("DURAKLATILDI", True, (255, 255, 255))
        ekran.blit(yazi, yazi.get_rect(center=(GENISLIK // 2, 280)))
        ipucu = self.font_o.render("ESC: Devam", True, (200, 200, 200))
        ekran.blit(ipucu, ipucu.get_rect(center=(GENISLIK // 2, 340)))


# === GOREV 1.1 - GameOverState ===
# Aşağıdaki sınıfı tamamlayın.
# - gir: font hazırla
# - olaylari_isle: ENTER -> degistir(PlayState), ESC -> degistir(MenuState)
# - ciz: kırmızı arkaplan, "OYUN BITTI" başlığı, ipucu metni
#
# TODO: class GameOverState(State):
# TODO:     def gir(self):
# TODO:         self.font_b = pygame.font.Font(None, 80)
# TODO:         self.font_o = pygame.font.Font(None, 32)
# TODO:
# TODO:     def olaylari_isle(self, olaylar):
# TODO:         for olay in olaylar:
# TODO:             if olay.type == pygame.KEYDOWN:
# TODO:                 if olay.key == pygame.K_RETURN:
# TODO:                     self.manager.degistir(PlayState(self.manager))
# TODO:                 elif olay.key == pygame.K_ESCAPE:
# TODO:                     self.manager.degistir(MenuState(self.manager))
# TODO:
# TODO:     def ciz(self, ekran):
# TODO:         ekran.fill((30, 0, 0))
# TODO:         baslik = self.font_b.render("OYUN BITTI", True, (255, 80, 80))
# TODO:         ekran.blit(baslik, baslik.get_rect(center=(GENISLIK // 2, 200)))
# TODO:         ipucu = self.font_o.render(
# TODO:             "ENTER: Tekrar  ESC: Menu", True, (200, 200, 200))
# TODO:         ekran.blit(ipucu, ipucu.get_rect(center=(GENISLIK // 2, 350)))


# === ANA DÖNGÜ ===
def main():
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 12 - Calisma 1: State Machine")
    saat = pygame.time.Clock()

    manager = StateManager()
    manager.it(MenuState(manager))

    calistir = True
    while calistir and manager.aktif:
        dt = saat.tick(60) / 1000.0
        olaylar = pygame.event.get()
        for olay in olaylar:
            if olay.type == pygame.QUIT:
                calistir = False

        manager.aktif.olaylari_isle(olaylar)
        manager.aktif.guncelle(dt)
        manager.aktif.ciz(ekran)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN ÇIKTI (temel kod):
---------------------------
800x600 pencere açılır, ana menü görünür.
- ENTER ile oyuna girilir, sarı top OK tuşları ile kontrol edilir.
- ESC pause açar, ESC tekrar devam ettirir.
- Cikis seçilince pencere kapanır.

GOREV 1.1 tamamlanınca:
- X tuşu Game Over ekranına geçer.
- Game Over'dan ENTER ile yeniden başlar, ESC menüye döner.

GOREV 1.2 tamamlanınca:
- SPACE her basışta canı 1 azaltır.
- Can 0 olunca otomatik Game Over.
"""
