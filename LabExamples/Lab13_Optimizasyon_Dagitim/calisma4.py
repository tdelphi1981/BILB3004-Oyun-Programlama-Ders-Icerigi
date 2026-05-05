"""
Lab 13 - Çalışma 4 Başlangıç Kodu
PyInstaller Uyumlu resource_path

Bu dosya Lab 13 föyü ile birlikte kullanılır.
"GOREV" işaretli bölgeleri tamamlayın.

Öğrenilecek kavramlar:
- sys._MEIPASS özniteliği (PyInstaller --onefile çalışma zamanı kökü)
- Geliştirme ortamı için __file__ tabanlı kök tespiti
- pygame.image.load çağrılarını sarmalama
- pyinstaller --onefile --add-data ... komutu

Lab: 13 - Optimizasyon ve Dağıtım
Çalışma: 4 - PyInstaller Dağıtım

Çalıştırma (geliştirme): uv run python calisma4.py
Çalıştırma (paketlenmiş):
    pyinstaller --onefile --windowed --add-data "assets:assets" calisma4.py
    ./dist/calisma4   (veya Windows: dist\\calisma4.exe)

Tuşlar: ESC -> Çıkış
"""

# === GOREV 4.1 - Modül İçe Aktarımları ===
# Aşağıdaki iki modülü ekle. resource_path için ZORUNLUlar.
# TODO: a) import sys
# TODO: b) import os

from pathlib import Path

import pygame

GENISLIK, YUKSEKLIK = 640, 480
ASSETS_DIZIN = "assets"


# === GOREV 4.2 - resource_path Fonksiyonu ===
# Hem geliştirme hem PyInstaller --onefile altında çalışacak şekilde
# yaz. PyInstaller çalışma zamanında sys._MEIPASS özniteliğini ekler;
# geliştirmede bu öznitelik yoktur, o zaman __file__'in dizini kök olur.
#
# def resource_path(rel_path):
# TODO: a) kok = getattr(sys, "_MEIPASS",
# TODO:                  os.path.dirname(os.path.abspath(__file__)))
# TODO: b) return os.path.join(kok, rel_path)
def resource_path(rel_path):
    """GOREV 4.2 -- aşağıyı doldur ve return ekle."""
    return rel_path   # !!! ŞİMDİLİK SADECE GÖRECELİ DÖNDÜRÜR !!!


def yapay_assets_olustur():
    """assets/oyuncu.png dosyası yoksa basit bir görsel üretir.

    Bu fonksiyon, lab başlangıcında öğrencinin elinde gerçek bir asset
    dosyası olmasa da uygulamanın çalışmasını sağlar. Gerçek projende
    elindeki PNG dosyalarını assets/ altına koyarsın.

    Path(__file__) standart kütüphane kullanır; sys/os import'larından
    bağımsız çalışır (GOREV 4.1'den önce de hata vermez).
    """
    dizin = Path(__file__).resolve().parent / ASSETS_DIZIN
    dizin.mkdir(parents=True, exist_ok=True)
    yol = dizin / "oyuncu.png"
    if yol.exists():
        return
    # 64x64 sarı daire üret
    yuzey = pygame.Surface((64, 64), pygame.SRCALPHA)
    pygame.draw.circle(yuzey, (255, 215, 0, 255), (32, 32), 28)
    pygame.draw.circle(yuzey, (200, 150, 0, 255), (32, 32), 28, 4)
    pygame.image.save(yuzey, str(yol))


def main():
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption("Lab 13 - Calisma 4: PyInstaller")
    saat = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # İlk çalıştırmada assets/ klasörü ve örnek görseli oluştur
    yapay_assets_olustur()

    # === GOREV 4.3 - pygame.image.load çağrısını sarmala ===
    # Aşağıdaki satırı resource_path ile sarmala:
    # ESKI: yuzey = pygame.image.load("assets/oyuncu.png").convert_alpha()
    # YENI: yuzey = pygame.image.load(
    #            resource_path("assets/oyuncu.png")).convert_alpha()
    yol = "assets/oyuncu.png"   # GOREV 4.3: bu satırı resource_path ile sar
    try:
        yuzey = pygame.image.load(yol).convert_alpha()
        hata = None
    except (pygame.error, FileNotFoundError) as e:
        yuzey = None
        hata = str(e)

    x, y = GENISLIK // 2, YUKSEKLIK // 2

    calistir = True
    while calistir:
        dt = saat.tick(60) / 1000.0

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN and olay.key == pygame.K_ESCAPE:
                calistir = False

        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT]:  x -= 200 * dt
        if tuslar[pygame.K_RIGHT]: x += 200 * dt
        if tuslar[pygame.K_UP]:    y -= 200 * dt
        if tuslar[pygame.K_DOWN]:  y += 200 * dt

        ekran.fill((20, 25, 35))

        if yuzey is not None:
            ekran.blit(yuzey, yuzey.get_rect(center=(int(x), int(y))))
            durum = font.render("OK: Asset yuklendi", True, (120, 240, 120))
        else:
            durum = font.render(
                f"HATA: {hata}", True, (255, 100, 100))

        ekran.blit(durum, (10, 10))

        # === GOREV 4.4 - Paketleme ===
        # Bu kod çalıştığını doğruladıktan sonra terminalden:
        # pyinstaller --onefile --windowed --add-data "assets:assets" calisma4.py
        # komutuyla paketle ve dist/ klasöründeki dosyayı çalıştır.
        ipucu = font.render(
            "OK: Hareket  ESC: Cikis  |  Goreceli yol: " + str(yol),
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
- Geliştirme ortamında: 640x480 pencerede sarı daire ok tuşlarıyla hareket eder.
  "OK: Asset yuklendi" yazısı yeşil renkte üstte görünür.
- pyinstaller --onefile --windowed --add-data "assets:assets" calisma4.py
  komutundan sonra dist/ altında üretilen tek dosya çift tıklanır ve
  aynı pencereyi açar. _MEIPASS klasöründen assets/oyuncu.png yüklenir.

GÖREV 4.2 yapılmazsa: paketlenmiş versiyonda "HATA: Couldn't open ..." görünür.
GÖREV 4.3 yapılmazsa: pyinstaller paketinden sonra resim yüklenmez.
"""
