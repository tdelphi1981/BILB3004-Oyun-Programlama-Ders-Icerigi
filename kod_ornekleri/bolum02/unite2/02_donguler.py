"""
Döngüler Örnekleri

Bu dosya while, for, range, break ve continue
kullanımını oyun geliştirme bağlamında gösterir.

Bölüm: 02 - Python Kontrol Yapıları ve Fonksiyonlar
Ünite: 2 - Döngüler

Çalıştırma: python 02_donguler.py
"""

# =============================================================================
# Örnek 1: While Döngüsü - Geri Sayım
# =============================================================================
print("=== Örnek 1: Geri Sayım ===")

sayac = 5
while sayac > 0:
    print(f"Kalkışa {sayac}...")
    sayac -= 1
print("Kalkış!")

# =============================================================================
# Örnek 2: While ile Can Azaltma
# =============================================================================
print("\n=== Örnek 2: Can Azaltma ===")

can = 100
darbe_sayisi = 0
hasar = 15

while can > 0:
    can -= hasar
    darbe_sayisi += 1
    print(f"Darbe {darbe_sayisi}: Can = {can}")

print(f"Oyuncu {darbe_sayisi} darbede yenildi!")

# =============================================================================
# Örnek 3: For ile Liste Gezinme
# =============================================================================
print("\n=== Örnek 3: Envanter Listesi ===")

envanter = ["Kılıç", "Kalkan", "Sağlık İksiri", "Anahtar"]

print("Envanterin:")
for esya in envanter:
    print(f"  - {esya}")

# =============================================================================
# Örnek 4: enumerate ile İndeks
# =============================================================================
print("\n=== Örnek 4: Silah Seçimi ===")

silahlar = ["Kılıç", "Balta", "Yay", "Asa"]

print("Silah Seç:")
for indeks, silah in enumerate(silahlar, start=1):
    print(f"  {indeks}. {silah}")

# =============================================================================
# Örnek 5: range() Kullanımı
# =============================================================================
print("\n=== Örnek 5: range() Örnekleri ===")

# 0'dan 4'e
print("range(5):", list(range(5)))

# 1'den 5'e
print("range(1, 6):", list(range(1, 6)))

# 2'şer atlayarak
print("range(0, 10, 2):", list(range(0, 10, 2)))

# Geriye sayma
print("range(5, 0, -1):", list(range(5, 0, -1)))

# =============================================================================
# Örnek 6: 2D Grid Oluşturma
# =============================================================================
print("\n=== Örnek 6: 2D Grid ===")

satir = 3
sutun = 5

for y in range(satir):
    for x in range(sutun):
        print(".", end=" ")
    print()

# =============================================================================
# Örnek 7: Düşman Güncelleme
# =============================================================================
print("\n=== Örnek 7: Düşman Güncelleme ===")

dusmanlar = [
    {"isim": "Goblin 1", "can": 30},
    {"isim": "Goblin 2", "can": 25},
    {"isim": "Ork", "can": 50}
]

alan_hasari = 20

print("Ateş Topu büyüsü!")
for dusman in dusmanlar:
    dusman["can"] -= alan_hasari
    if dusman["can"] <= 0:
        print(f"  [OLUM] {dusman['isim']} yok edildi!")
    else:
        print(f"  {dusman['isim']}: {dusman['can']} HP kaldı")

# =============================================================================
# Örnek 8: break ile Döngüden Çıkış
# =============================================================================
print("\n=== Örnek 8: break ===")

hedefler = ["Goblin", "Ork", "Trol", "Ejderha"]
aranan = "Trol"

for hedef in hedefler:
    print(f"Kontrol: {hedef}")
    if hedef == aranan:
        print(f"  {aranan} bulundu!")
        break

# =============================================================================
# Örnek 9: continue ile İterasyon Atlama
# =============================================================================
print("\n=== Örnek 9: continue ===")

dusmanlar = [
    {"isim": "Goblin", "can": 0},   # Ölü
    {"isim": "Ork", "can": 30},     # Canlı
    {"isim": "Trol", "can": 0},     # Ölü
    {"isim": "Ejderha", "can": 100} # Canlı
]

print("Canlı düşmanlar:")
for dusman in dusmanlar:
    if dusman["can"] <= 0:
        continue
    print(f"  {dusman['isim']}: {dusman['can']} HP")

# =============================================================================
# Örnek 10: for-else Yapısı
# =============================================================================
print("\n=== Örnek 10: for-else ===")

oyuncu_x = 100
engeller = [50, 75, 150, 200]

for engel in engeller:
    if oyuncu_x == engel:
        print(f"Çarpışma! Engel: {engel}")
        break
else:
    print("Çarpışma yok, yol açık!")

# =============================================================================
# Örnek 11: Mermi Spawn
# =============================================================================
print("\n=== Örnek 11: Çoklu Mermi ===")

mermi_sayisi = 5

print(f"{mermi_sayisi} mermi ateşleniyor:")
for i in range(mermi_sayisi):
    aci = i * 30
    print(f"  Mermi {i+1}: {aci}° açısında")


"""
BEKLENEN ÇIKTI:
---------------
=== Örnek 1: Geri Sayım ===
Kalkışa 5...
Kalkışa 4...
Kalkışa 3...
Kalkışa 2...
Kalkışa 1...
Kalkış!

=== Örnek 2: Can Azaltma ===
Darbe 1: Can = 85
Darbe 2: Can = 70
...
Oyuncu 7 darbede yenildi!

=== Örnek 3: Envanter Listesi ===
Envanterin:
  - Kılıç
  - Kalkan
  - Sağlık İksiri
  - Anahtar

... (diğer örnekler)
"""
