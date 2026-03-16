"""
Aritmetik Operatörler

Bu program, Python'daki matematiksel işlemleri gösterir.
Oyunlarda puan, hasar, hız hesaplamaları için kullanılır.

Öğrenilecek kavramlar:
- Toplama, çıkarma, çarpma, bölme
- Tam bölme (//) ve mod (%)
- Üs alma (**)
- Bileşik atama (+=, -=)

Bölüm: 01 - Python'a Giriş
Ünite: 3 - Operatörler ve İfadeler

Çalıştırma: python 01_aritmetik.py
"""

print("=== ARİTMETİK OPERATÖRLER ===\n")

# Temel işlemler
print("--- Temel İşlemler ---")
a = 10
b = 3

print(f"{a} + {b} = {a + b}")   # Toplama
print(f"{a} - {b} = {a - b}")   # Çıkarma
print(f"{a} * {b} = {a * b}")   # Çarpma
print(f"{a} / {b} = {a / b}")   # Bölme (float sonuç)

# Özel işlemler
print("\n--- Özel İşlemler ---")
print(f"{a} // {b} = {a // b}")  # Tam bölme
print(f"{a} % {b} = {a % b}")    # Mod (kalan)
print(f"2 ** 8 = {2 ** 8}")      # Üs alma

# Oyun örneği: Dakika-saniye dönüşümü
print("\n--- Oyun Örneği: Süre ---")
toplam_saniye = 185

dakika = toplam_saniye // 60
saniye = toplam_saniye % 60

print(f"Toplam: {toplam_saniye} saniye")
print(f"Süre: {dakika} dakika {saniye} saniye")

# Bileşik atama
print("\n--- Bileşik Atama ---")
puan = 100
print(f"Başlangıç puanı: {puan}")

puan += 50  # puan = puan + 50
print(f"Bonus sonrası: {puan}")

puan *= 2   # puan = puan * 2
print(f"Çarpan sonrası: {puan}")

puan -= 75  # puan = puan - 75
print(f"Ceza sonrası: {puan}")

# Oyun örneği: Hasar hesaplama
print("\n--- Oyun Örneği: Hasar Hesaplama ---")
baz_hasar = 50
kritik_carpan = 2.5
zirh = 20

kritik_hasar = baz_hasar * kritik_carpan
gercek_hasar = kritik_hasar - zirh

print(f"Baz hasar: {baz_hasar}")
print(f"Kritik çarpan: x{kritik_carpan}")
print(f"Kritik hasar: {kritik_hasar}")
print(f"Zırh azaltması: -{zirh}")
print(f"Gerçek hasar: {gercek_hasar}")

"""
BEKLENEN ÇIKTI:
---------------
=== ARİTMETİK OPERATÖRLER ===

--- Temel İşlemler ---
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333333333333335

--- Özel İşlemler ---
10 // 3 = 3
10 % 3 = 1
2 ** 8 = 256

--- Oyun Örneği: Süre ---
Toplam: 185 saniye
Süre: 3 dakika 5 saniye

--- Bileşik Atama ---
Başlangıç puanı: 100
Bonus sonrası: 150
Çarpan sonrası: 300
Ceza sonrası: 225

--- Oyun Örneği: Hasar Hesaplama ---
Baz hasar: 50
Kritik çarpan: x2.5
Kritik hasar: 125.0
Zırh azaltması: -20
Gerçek hasar: 105.0
"""
