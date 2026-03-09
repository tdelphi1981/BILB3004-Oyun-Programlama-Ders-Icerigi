"""
Lab 02 - Bonus: Karekok Optimizasyonu
Asal Sayi Kontrolu (Optimize Edilmis)

Lab 02 Calisma 3'un bonus gorevinin cozumu.
math.isqrt(n) ile optimize edilmis asal_mi() fonksiyonu.
2-100 arasi asal sayilari listeler ve toplam sayiyi yazdirir.

Neden karekok yeterli? Eger n = a * b ise, a ve b'den en az
biri sqrt(n)'den kucuk veya esit olmalidir.

Lab: 02 - Kontrol Yapilari ve Fonksiyonlar
Bonus: Karekok Optimizasyonu

Calistirma: python bonus_karekok.py
"""

import math


def asal_mi(n):
    """Sayinin asal olup olmadigini kontrol eder (optimize)."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Bolenleri sadece karekoke kadar kontrol et
    sinir = math.isqrt(n)
    for i in range(3, sinir + 1, 2):
        if n % i == 0:
            return False
    return True


# 2'den 100'e kadar asal sayilari listele
print("2-100 arasi asal sayilar:")
print("-" * 40)

asal_sayilar = []
for sayi in range(2, 101):
    if asal_mi(sayi):
        asal_sayilar.append(sayi)

print(asal_sayilar)
print(f"\nToplam {len(asal_sayilar)} asal sayi bulundu.")


"""
BEKLENEN CIKTI:
----------------------------
2-100 arasi asal sayilar:
----------------------------------------
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

Toplam 25 asal sayi bulundu.
"""
