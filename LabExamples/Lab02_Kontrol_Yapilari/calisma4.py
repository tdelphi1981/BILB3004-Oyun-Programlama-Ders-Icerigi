"""
Lab 02 - Calisma 4 Baslangic Kodu
Metin Tabanli Macera Oyunu

Bu dosya Lab 02 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Sozluk (dictionary) kullanimi
- Liste kullanimi (envanter)
- random modulu
- if/elif/else kosul yapilari
- while dongusu
- input() ile kullanici etkilesimi

Lab: 02 - Kontrol Yapilari ve Fonksiyonlar
Calisma: 4 - Metin Tabanli Macera Oyunu

Calistirma: python calisma4.py
"""

# --- Lab foyundeki ornek kod ---

import random

# Oyuncu bilgileri
oyuncu = {
    "can": 100,
    "guc": 15,
    "altin": 50,
    "envanter": ["kilic"]
}

print("=== Zindan Macerasi ===")
print(f"Can: {oyuncu['can']}, Guc: {oyuncu['guc']}")
print(f"Altin: {oyuncu['altin']}")

# Basit oda secimi
print("\nIki yol var:")
print("1. Sol koridor (karanlik)")
print("2. Sag koridor (isikli)")

secim = input("Seciminiz (1/2): ")

if secim == "1":
    hasar = random.randint(5, 20)
    oyuncu["can"] -= hasar
    print(f"Tuzaga dustunuz! -{hasar} can")
    print(f"Kalan can: {oyuncu['can']}")
elif secim == "2":
    altin = random.randint(10, 30)
    oyuncu["altin"] += altin
    print(f"Hazine buldunuz! +{altin} altin")
    print(f"Toplam altin: {oyuncu['altin']}")
else:
    print("Gecersiz secim!")


# === GOREV 4.1 - Calistir ve Oyna ===
# TODO: a) Programi birkac kez calistirin
# TODO: b) Her iki yolu da deneyin
# TODO: c) Sonuclari gozlemleyin
# ============================================


# === GOREV 4.2 - Dukkan Sistemi ===
# TODO: a) Oyuna bir dukkan ekleyin
# TODO: b) Oyuncu altinlariyla esya satin alabilsin:
#          - Iksir (20 altin): +30 can
#          - Kalkan (35 altin): Envantere eklenir
#          - Buyu kitabi (50 altin): Envantere eklenir
# TODO: c) Dukkani bir while dongusu icinde gosterin,
#          "cikis" secenegi ekleyin
# ============================================


# === GOREV 4.3 - Farkli Silah Turleri ===
# TODO: a) Oyuna farkli silahlar ekleyin:
#          - Kilic: 15 hasar (baslangic silahi)
#          - Balta: 25 hasar
#          - Yay: 20 hasar (uzak mesafe)
# TODO: b) Savas sirasinda oyuncunun elindeki silaha gore
#          hasar hesaplayin
# ============================================


# BONUS: Karakter Siniflari
# TODO: a) Oyuna karakter siniflari ekleyin:
#          - Savasci: Yuksek guc (20), orta can (100),
#            baslangic silahi: kilic
#          - Buyucu: Dusuk guc (10), dusuk can (70),
#            buyu gucu: 30, baslangic silahi: asa
# TODO: b) Oyun basinda kullaniciya sinif sectirin
# TODO: c) Oyuncu ozelliklerini buna gore ayarlayin
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
=== Zindan Macerasi ===
Can: 100, Guc: 15
Altin: 50

Iki yol var:
1. Sol koridor (karanlik)
2. Sag koridor (isikli)
Seciminiz (1/2): 1
Tuzaga dustunuz! -12 can
Kalan can: 88
(Not: Hasar degeri her calistirmada degisir)
"""
