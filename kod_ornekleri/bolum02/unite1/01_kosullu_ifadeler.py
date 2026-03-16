"""
Koşullu İfadeler Örnekleri

Bu dosya if, elif, else ve mantıksal operatörlerin
oyun geliştirme bağlamında kullanımını gösterir.

Bölüm: 02 - Python Kontrol Yapıları ve Fonksiyonlar
Ünite: 1 - Koşullu İfadeler

Çalıştırma: python 01_kosullu_ifadeler.py
"""

# =============================================================================
# Örnek 1: Basit if İfadesi
# =============================================================================
print("=== Örnek 1: Basit if ===")

oyuncu_can = 100

if oyuncu_can > 0:
    print("Oyuncu hayatta!")

# =============================================================================
# Örnek 2: if-else
# =============================================================================
print("\n=== Örnek 2: if-else ===")

oyuncu_can = 0

if oyuncu_can > 0:
    print("Oyuncu hayatta!")
else:
    print("Game Over!")

# =============================================================================
# Örnek 3: if-elif-else (Sağlık Durumu)
# =============================================================================
print("\n=== Örnek 3: Sağlık Durumu ===")

can = 35

if can >= 70:
    durum = "İyi"
    renk = "Yeşil"
elif can >= 30:
    durum = "Orta"
    renk = "Sarı"
else:
    durum = "Kritik"
    renk = "Kırmızı"

print(f"Sağlık: {durum} ({renk})")

# =============================================================================
# Örnek 4: Seviye Sistemi
# =============================================================================
print("\n=== Örnek 4: Seviye Sistemi ===")

puan = 2500

if puan >= 5000:
    seviye = "Efsane"
elif puan >= 2000:
    seviye = "Usta"
elif puan >= 1000:
    seviye = "Deneyimli"
elif puan >= 500:
    seviye = "Acemi"
else:
    seviye = "Çaylak"

print(f"Puan: {puan} -> Seviye: {seviye}")

# =============================================================================
# Örnek 5: Mantıksal Operatörler (and, or, not)
# =============================================================================
print("\n=== Örnek 5: Mantıksal Operatörler ===")

can = 50
mermi = 10
dusman_menzilde = True

# and: Tüm koşullar doğru olmalı
if can > 0 and mermi > 0 and dusman_menzilde:
    print("Ateş edebilirsin!")

# or: En az biri doğru olmalı
anahtar = False
maymuncuk = True
patlayici = False

if anahtar or maymuncuk or patlayici:
    print("Kapıyı açabilirsin!")

# not: Tersine çevirme
oyun_bitti = False

if not oyun_bitti:
    print("Oyun devam ediyor...")

# =============================================================================
# Örnek 6: İç İçe Koşullar
# =============================================================================
print("\n=== Örnek 6: İç İçe Koşullar ===")

oyuncu_can = 80
mermi = 5
dusman_gorunur = True
dusman_mesafe = 15

if oyuncu_can > 0:
    print("Oyuncu hayatta")

    if dusman_gorunur:
        print("  Düşman görünürde")

        if dusman_mesafe <= 20:
            print("    Düşman menzilde")

            if mermi > 0:
                print("      Ateş!")
            else:
                print("      Mermi yok!")
        else:
            print("    Düşman çok uzakta")
    else:
        print("  Hedef yok")
else:
    print("Game Over!")

# =============================================================================
# Örnek 7: Büyü Sistemi
# =============================================================================
print("\n=== Örnek 7: Büyü Sistemi ===")

mana = 30
buyucu_seviyesi = 5
hedef_secili = True
buz_buyusu_maliyeti = 25
gereken_seviye = 3

if mana >= buz_buyusu_maliyeti and buyucu_seviyesi >= gereken_seviye:
    if hedef_secili:
        print("Buz Fırtınası büyüsü kullanıldı!")
        mana -= buz_buyusu_maliyeti
        print(f"Kalan mana: {mana}")
    else:
        print("Önce bir hedef seç!")
elif mana < buz_buyusu_maliyeti:
    print(f"Yetersiz mana! Gereken: {buz_buyusu_maliyeti}, Mevcut: {mana}")
else:
    print(f"Bu büyü için seviye {gereken_seviye} gerekli!")

# =============================================================================
# Örnek 8: in Operatörü ile Kontrol
# =============================================================================
print("\n=== Örnek 8: in Operatörü ===")

dusman_turu = "goblin"

if dusman_turu in ["goblin", "ork", "trol"]:
    print("Bu bir yeşil düşman!")
elif dusman_turu in ["iskelet", "zombi", "hayalet"]:
    print("Bu bir undead düşman!")
else:
    print("Bilinmeyen düşman türü")

# =============================================================================
# Örnek 9: Aralık Kontrolü
# =============================================================================
print("\n=== Örnek 9: Aralık Kontrolü ===")

sicaklik = 25

if 20 <= sicaklik <= 30:
    print("Hava güzel, dışarı çıkabilirsin!")
elif sicaklik < 20:
    print("Hava soğuk, mont al!")
else:
    print("Hava çok sıcak, gölgede kal!")


"""
BEKLENEN ÇIKTI:
---------------
=== Örnek 1: Basit if ===
Oyuncu hayatta!

=== Örnek 2: if-else ===
Game Over!

=== Örnek 3: Sağlık Durumu ===
Sağlık: Orta (Sarı)

=== Örnek 4: Seviye Sistemi ===
Puan: 2500 -> Seviye: Usta

=== Örnek 5: Mantıksal Operatörler ===
Ateş edebilirsin!
Kapıyı açabilirsin!
Oyun devam ediyor...

=== Örnek 6: İç İçe Koşullar ===
Oyuncu hayatta
  Düşman görünürde
    Düşman menzilde
      Ateş!

=== Örnek 7: Büyü Sistemi ===
Buz Fırtınası büyüsü kullanıldı!
Kalan mana: 5

=== Örnek 8: in Operatörü ===
Bu bir yeşil düşman!

=== Örnek 9: Aralık Kontrolü ===
Hava güzel, dışarı çıkabilirsin!
"""
