"""
Lab 02 - Bonus: Karakter Siniflari
Metin Tabanli Macera Oyunu (Sinif Secimli)

Lab 02 Calisma 4'un bonus gorevinin cozumu.
Oyun basinda karakter sinifi sectirip oyuncu ozelliklerini
buna gore ayarlar.

Karakter siniflari:
- Savasci: guc=20, can=100, silah=kilic
- Buyucu: guc=10, can=70, buyu gucu=30, silah=asa

Lab: 02 - Kontrol Yapilari ve Fonksiyonlar
Bonus: Karakter Siniflari

Calistirma: python bonus_karakter_siniflari.py
"""

import random

# --- Karakter sinifi secimi ---
print("=== Zindan Macerasi ===")
print("\nKarakter sinifinizi secin:")
print("1. Savasci (Guc: 20, Can: 100, Silah: Kilic)")
print("2. Buyucu  (Guc: 10, Can: 70, Buyu: 30, Silah: Asa)")

sinif_secim = input("\nSeciminiz (1/2): ")

if sinif_secim == "1":
    oyuncu = {
        "sinif": "Savasci",
        "can": 100,
        "guc": 20,
        "altin": 50,
        "envanter": ["kilic"]
    }
    print("\n[Savasci secildi] Guclu kollarinla dusmanlari ez!")
elif sinif_secim == "2":
    oyuncu = {
        "sinif": "Buyucu",
        "can": 70,
        "guc": 10,
        "buyu_gucu": 30,
        "altin": 50,
        "envanter": ["asa"]
    }
    print("\n[Buyucu secildi] Buyulerin seni koruyacak!")
else:
    print("Gecersiz secim! Varsayilan: Savasci")
    oyuncu = {
        "sinif": "Savasci",
        "can": 100,
        "guc": 20,
        "altin": 50,
        "envanter": ["kilic"]
    }

# --- Oyuncu bilgilerini goster ---
print(f"\nSinif: {oyuncu['sinif']}")
print(f"Can: {oyuncu['can']}, Guc: {oyuncu['guc']}")
if "buyu_gucu" in oyuncu:
    print(f"Buyu Gucu: {oyuncu['buyu_gucu']}")
print(f"Altin: {oyuncu['altin']}")
print(f"Envanter: {oyuncu['envanter']}")

# --- Basit oda secimi ---
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


"""
BEKLENEN CIKTI (ornek):
----------------------------
=== Zindan Macerasi ===

Karakter sinifinizi secin:
1. Savasci (Guc: 20, Can: 100, Silah: Kilic)
2. Buyucu  (Guc: 10, Can: 70, Buyu: 30, Silah: Asa)

Seciminiz (1/2): 2

[Buyucu secildi] Buyulerin seni koruyacak!

Sinif: Buyucu
Can: 70, Guc: 10
Buyu Gucu: 30
Altin: 50
Envanter: ['asa']

Iki yol var:
1. Sol koridor (karanlik)
2. Sag koridor (isikli)
Seciminiz (1/2): 1
Tuzaga dustunuz! -12 can
Kalan can: 58
"""
