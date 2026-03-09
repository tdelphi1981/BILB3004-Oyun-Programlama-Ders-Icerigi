"""
Lab 01 - Bonus: Puan Sistemi
Sayi Tahmin Oyunu (Puanli Versiyon)

Lab 01 Calisma 4'un bonus gorevinin cozumu.
While dongusu + 3 hak + puanlama sistemi.

Puanlama:
- 1. denemede bilme: 100 puan
- 2. denemede bilme: 75 puan
- 3. denemede bilme: 50 puan
- Bilememe: 0 puan

Lab: 01 - Python Temelleri
Bonus: Puan Sistemi

Calistirma: python bonus_puan_sistemi.py
"""

import random

# Bilgisayar 1-100 arasi rastgele sayi secer
gizli_sayi = random.randint(1, 100)

# Puan tablosu: deneme sayisina gore puan
puan_tablosu = {1: 100, 2: 75, 3: 50}

kalan_hak = 3
deneme = 0
bildi = False

print("=== Sayi Tahmin Oyunu (Puanli) ===")
print("1-100 arasi bir sayi tuttum. 3 hakkiniz var!\n")

while kalan_hak > 0:
    tahmin = int(input("Tahmininiz: "))
    deneme += 1
    kalan_hak -= 1

    if tahmin == gizli_sayi:
        bildi = True
        print(f"Tebrikler! {deneme} denemede bildiniz!")
        break
    elif tahmin < gizli_sayi:
        print(f"Daha buyuk! (Kalan hak: {kalan_hak})")
    else:
        print(f"Daha kucuk! (Kalan hak: {kalan_hak})")

# Puan hesapla
if bildi:
    puan = puan_tablosu.get(deneme, 0)
else:
    puan = 0
    print(f"\nHakkiniz bitti! Gizli sayi: {gizli_sayi}")

print(f"\n--- Sonuc ---")
print(f"Puaniniz: {puan}")


"""
BEKLENEN CIKTI (ornek):
----------------------------
=== Sayi Tahmin Oyunu (Puanli) ===
1-100 arasi bir sayi tuttum. 3 hakkiniz var!

Tahmininiz: 50
Daha buyuk! (Kalan hak: 2)
Tahmininiz: 75
Daha kucuk! (Kalan hak: 1)
Tahmininiz: 63
Tebrikler! 3 denemede bildiniz!

--- Sonuc ---
Puaniniz: 50
"""
