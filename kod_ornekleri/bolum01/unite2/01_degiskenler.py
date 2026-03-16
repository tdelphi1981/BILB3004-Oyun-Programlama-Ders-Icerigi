"""
Değişkenler - Veri Saklama

Bu program, değişken oluşturma ve kullanmayı gösterir.
Değişkenler, oyun verilerini saklamak için kullanılır.

Öğrenilecek kavramlar:
- Değişken tanımlama
- Değişken isimlendirme kuralları
- Değişken değerini değiştirme

Bölüm: 01 - Python'a Giriş
Ünite: 2 - Değişkenler ve Veri Tipleri

Çalıştırma: python 01_degiskenler.py
"""

# Değişken oluşturma
oyuncu_adi = "KahramanAli"
puan = 0
can = 100
seviye = 1

# Değişkenleri kullanma
print("=== OYUNCU BİLGİLERİ ===")
print("Oyuncu:", oyuncu_adi)
print("Puan:", puan)
print("Can:", can)
print("Seviye:", seviye)

# Değişken değerini değiştirme
print("\n=== OYUN BAŞLADI ===")

# Puan kazandık
puan = puan + 100
print("Puan kazanıldı! Yeni puan:", puan)

# Hasar aldık
can = can - 25
print("Hasar alındı! Kalan can:", can)

# Seviye atladık
seviye += 1  # seviye = seviye + 1 ile aynı
print("Seviye atlandı! Yeni seviye:", seviye)

# Final durumu
print("\n=== FİNAL DURUMU ===")
print(f"Oyuncu: {oyuncu_adi}")
print(f"Puan: {puan} | Can: {can} | Seviye: {seviye}")

"""
BEKLENEN ÇIKTI:
---------------
=== OYUNCU BİLGİLERİ ===
Oyuncu: KahramanAli
Puan: 0
Can: 100
Seviye: 1

=== OYUN BAŞLADI ===
Puan kazanıldı! Yeni puan: 100
Hasar alındı! Kalan can: 75
Seviye atlandı! Yeni seviye: 2

=== FİNAL DURUMU ===
Oyuncu: KahramanAli
Puan: 100 | Can: 75 | Seviye: 2
"""
