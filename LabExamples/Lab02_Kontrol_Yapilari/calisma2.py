"""
Lab 02 - Calisma 2 Baslangic Kodu
FizzBuzz

Bu dosya Lab 02 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- if/elif/else kosul yapilari
- Mod operatoru (%)
- for dongusu
- Fonksiyon tanimlama (def)

Lab: 02 - Kontrol Yapilari ve Fonksiyonlar
Calisma: 2 - FizzBuzz

Calistirma: python calisma2.py
"""

# --- Lab foyundeki ornek kod ---

# 1'den 20'ye kadar cift/tek kontrolu
for i in range(1, 21):
    if i % 2 == 0:
        print(f"{i} -> Cift")
    else:
        print(f"{i} -> Tek")


# === GOREV 2.1 - Fizz ===
# TODO: a) Programi degistirerek 1'den 30'a kadar olan
#          sayilari yazdirin
# TODO: b) 3'e bolunen sayilar icin sayi yerine "Fizz"
#          yazdirin, digerleri icin sayinin kendisini yazdirin
# ============================================


# === GOREV 2.2 - Fizz + Buzz ===
# TODO: a) Programa 5'e bolunen sayilar icin "Buzz"
#          yazdirma ozelligini de ekleyin
# ============================================


# === GOREV 2.3 - FizzBuzz ===
# TODO: a) Hem 3'e hem 5'e bolunen sayilar (15'in katlari)
#          icin "FizzBuzz" yazdirin
# TODO: b) Dikkat: Kosullarin sirasina dikkat edin!
#          FizzBuzz kontrolu en once yapilmalidir.
# Ornek cikti:
#   1
#   2
#   Fizz
#   4
#   Buzz
#   Fizz
#   7
#   8
#   Fizz
#   Buzz
#   11
#   Fizz
#   13
#   14
#   FizzBuzz
# ============================================


# === GOREV 2.4 - Fonksiyon Haline Getirin ===
# TODO: a) FizzBuzz mantigini def fizzbuzz(n): fonksiyonu
#          haline getirin
# TODO: b) Fonksiyon 1'den n'e kadar olan sayilari
#          kontrol etsin
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
1 -> Tek
2 -> Cift
3 -> Tek
4 -> Cift
...
19 -> Tek
20 -> Cift
"""
