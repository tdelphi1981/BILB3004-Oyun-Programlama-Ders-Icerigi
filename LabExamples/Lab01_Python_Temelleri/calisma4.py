"""
Lab 01 - Calisma 4 Baslangic Kodu
Sayi Tahmin Oyunu

Bu dosya Lab 01 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- random modulu
- if/elif/else kosul yapilari
- input() ile kullanicidan girdi alma
- int() tip donusumu
- while dongusu

Lab: 01 - Python Temelleri
Calisma: 4 - Sayi Tahmin Oyunu

Calistirma: python calisma4.py
"""

# --- Lab foyundeki ornek kod ---

import random

# Bilgisayar 1-100 arasi rastgele sayi secer
gizli_sayi = random.randint(1, 100)

# Oyuncudan tahmin al
tahmin = int(input("1-100 arasi bir sayi tahmin edin: "))

# Kontrol
if tahmin == gizli_sayi:
    print("Tebrikler! Dogru tahmin!")
elif tahmin < gizli_sayi:
    print(f"Daha buyuk! Gizli sayi: {gizli_sayi}")
else:
    print(f"Daha kucuk! Gizli sayi: {gizli_sayi}")


# === GOREV 4.1 - Calistir ve Gozlemle ===
# TODO: a) Programi 3-5 kez calistirin
# TODO: b) Her seferinde farkli gizli sayilar uretildigini
#          gozlemleyin
# TODO: c) Sonuclari lab foyundeki tabloya yazin
# ============================================


# === GOREV 4.2 - Deneme Siniri ===
# TODO: a) Programi bir while dongusu icine alin
# TODO: b) Oyuncuya 3 hak verin
# TODO: c) Dogru tahmin ederse tebrik edin
# TODO: d) Haklar biterse gizli sayiyi gosterin
# Ipucu: kalan_hak degiskeni kullanin ve her yanlis
#         tahminde 1 azaltin
# ============================================


# === GOREV 4.3 - Kalan Hak Gosterimi ===
# TODO: a) Her tahmin sonrasi kalan hak sayisini gosterin
# TODO: b) "Daha buyuk" / "Daha kucuk" ipucunu ekleyin
# Ornek cikti:
#   Tahmininiz: 50
#   Daha buyuk! (Kalan hak: 2)
#   Tahmininiz: 75
#   Daha kucuk! (Kalan hak: 1)
#   Tahmininiz: 63
#   Tebrikler! 3 denemede bildiniz!
# ============================================


# BONUS: Puan Sistemi
# TODO: a) Az denemede bilen oyuncuya yuksek puan verin:
#          - 1. denemede bilme: 100 puan
#          - 2. denemede bilme: 75 puan
#          - 3. denemede bilme: 50 puan
#          - Bilememe: 0 puan
# TODO: b) Oyun sonunda puani ekrana yazdirin
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
1-100 arasi bir sayi tahmin edin: 50
Daha buyuk! Gizli sayi: 73
(Not: Gizli sayi her calistirmada degisir)
"""
