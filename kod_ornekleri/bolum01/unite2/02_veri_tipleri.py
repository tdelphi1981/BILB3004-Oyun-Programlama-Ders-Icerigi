"""
Veri Tipleri - int, float, str, bool

Bu program, Python'daki temel veri tiplerini gösterir.
Her veri tipi farklı türde verileri saklamak için kullanılır.

Öğrenilecek kavramlar:
- int: Tam sayılar
- float: Ondalıklı sayılar
- str: Metinler
- bool: Mantıksal değerler
- type() fonksiyonu

Bölüm: 01 - Python'a Giriş
Ünite: 2 - Değişkenler ve Veri Tipleri

Çalıştırma: python 02_veri_tipleri.py
"""

print("=== VERİ TİPLERİ ===\n")

# int - Tam Sayılar
print("--- int (Tam Sayı) ---")
puan = 1500
can = 3
dusmus_dusmanlar = 42

print(f"Puan: {puan} (tip: {type(puan)})")
print(f"Can: {can} (tip: {type(can)})")
print(f"Düşmüş düşmanlar: {dusmus_dusmanlar}")

# float - Ondalıklı Sayılar
print("\n--- float (Ondalıklı Sayı) ---")
hiz = 5.5
x_pozisyon = 320.75
aci = 45.0

print(f"Hız: {hiz} (tip: {type(hiz)})")
print(f"X pozisyon: {x_pozisyon}")
print(f"Açı: {aci}")

# str - Metinler
print("\n--- str (Metin) ---")
oyuncu_adi = "KahramanAli"
silah = 'Lazer Tabancası'
hikaye = """Uzak bir galakside,
cesur bir pilot maceraya atılıyor..."""

print(f"Oyuncu: {oyuncu_adi} (tip: {type(oyuncu_adi)})")
print(f"Silah: {silah}")
print(f"Hikaye:\n{hikaye}")

# bool - Mantıksal Değerler
print("\n--- bool (Mantıksal) ---")
oyun_aktif = True
oyuncu_oldu = False
ses_acik = True

print(f"Oyun aktif mi? {oyun_aktif} (tip: {type(oyun_aktif)})")
print(f"Oyuncu öldü mü? {oyuncu_oldu}")
print(f"Ses açık mı? {ses_acik}")

# Karşılaştırma sonuçları boolean döndürür
print("\n--- Karşılaştırma Sonuçları ---")
puan = 1500
hedef = 1000
yuksek_skor = 2000

print(f"{puan} > {hedef}? {puan > hedef}")
print(f"{puan} > {yuksek_skor}? {puan > yuksek_skor}")
print(f"{puan} == 1500? {puan == 1500}")

"""
BEKLENEN ÇIKTI:
---------------
=== VERİ TİPLERİ ===

--- int (Tam Sayı) ---
Puan: 1500 (tip: <class 'int'>)
Can: 3 (tip: <class 'int'>)
Düşmüş düşmanlar: 42

--- float (Ondalıklı Sayı) ---
Hız: 5.5 (tip: <class 'float'>)
X pozisyon: 320.75
Açı: 45.0

--- str (Metin) ---
Oyuncu: KahramanAli (tip: <class 'str'>)
Silah: Lazer Tabancası
Hikaye:
Uzak bir galakside,
cesur bir pilot maceraya atılıyor...

--- bool (Mantıksal) ---
Oyun aktif mi? True (tip: <class 'bool'>)
Oyuncu öldü mü? False
Ses açık mı? True

--- Karşılaştırma Sonuçları ---
1500 > 1000? True
1500 > 2000? False
1500 == 1500? True
"""
