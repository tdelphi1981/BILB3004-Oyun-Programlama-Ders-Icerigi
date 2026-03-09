"""
Lab 03 - Calisma 1 Baslangic Kodu
PyGame Kurulumu ve Ilk Test

Bu dosya Lab 03 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- PyGame kurulumu (uv add pygame-ce)
- pygame.init() ile baslangic
- Modul ve surum bilgileri
- Ekran bilgisi sorgulama

Lab: 03 - PyGame'e Giris ve Oyun Penceresi
Calisma: 1 - PyGame Kurulumu ve Ilk Test

Calistirma: uv run python calisma1.py
"""

# --- Lab foyundeki ornek kod ---

import pygame

# PyGame'i baslat
pygame.init()

# Modul durumlarini yazdir
print(f"PyGame surumu: {pygame.version.ver}")
print(f"SDL surumu: {pygame.version.SDL}")
print(f"Baslayan modul sayisi: {pygame.get_init()}")

# Ekran bilgilerini al
bilgi = pygame.display.Info()
print(f"Ekran cozunurlugu: {bilgi.current_w}x{bilgi.current_h}")

# PyGame'i kapat
pygame.quit()
print("Kurulum basarili!")


# === GOREV 1.1 - Calistir ve Gozlemle ===
# TODO: a) Programi "uv run python calisma1.py" komutuyla
#          calistirin
# TODO: b) Ekrana yazilan bilgileri lab foyundeki tabloya
#          not edin:
#          - PyGame surumu
#          - SDL surumu
#          - Ekran cozunurlugu
# ============================================


# === GOREV 1.2 - Modul Kontrolu ===
# TODO: a) pygame.font.get_init() fonksiyonunu kullanarak
#          font modulunun baslatilip baslatilmadigini
#          kontrol edin
# TODO: b) pygame.mixer.get_init() ile ses modulunu
#          kontrol edin
# TODO: c) pygame.display.get_init() ile goruntuyu
#          kontrol edin
# TODO: d) Sonuclari ekrana yazdirin
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
PyGame surumu: 2.x.x
SDL surumu: (2, x, x)
Baslayan modul sayisi: True
Ekran cozunurlugu: ????x????
Kurulum basarili!
(Not: Degerler sisteminize gore degisir)
"""
