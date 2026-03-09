"""
Lab 02 - Calisma 3 Baslangic Kodu
Asal Sayi Kontrolu

Bu dosya Lab 02 foyu ile birlikte kullanilir.
"GOREV" isaretli bolgeleri tamamlayin.

Ogrenilecek kavramlar:
- Fonksiyon tanimlama ve kullanma
- return ifadesi
- Bolunebilirlik kontrolu
- Dongu ile arama
- math modulu (bonus)

Lab: 02 - Kontrol Yapilari ve Fonksiyonlar
Calisma: 3 - Asal Sayi Kontrolu

Calistirma: python calisma3.py
"""

# --- Lab foyundeki ornek kod ---

def cift_mi(sayi):
    """Sayinin 2'ye bolunup bolunmedigini kontrol eder."""
    if sayi % 2 == 0:
        return True
    else:
        return False

# Test
print(cift_mi(4))   # True
print(cift_mi(7))   # False


# === GOREV 3.1 - Tum Bolenler ===
# TODO: a) Fonksiyonu genisleterek bir sayinin 2'den
#          kendisine kadar olan tum bolenleri kontrol edin
# TODO: b) Herhangi birine bolunuyorsa False, hicbirine
#          bolunmuyorsa True dondurun
# Ipucu: for i in range(2, sayi): dongusunu kullanin
# ============================================


# === GOREV 3.2 - asal_mi(n) Fonksiyonu ===
# TODO: a) asal_mi(n) fonksiyonunu tamamlayin:
#          - 1 ve alti sayilar icin False dondursun
#          - 2 icin True dondursun
#          - Diger sayilar icin bolen kontrolu yapsin
#          - True veya False dondursun
# ============================================


# === GOREV 3.3 - Asal Sayi Listesi ===
# TODO: a) asal_mi() fonksiyonunu kullanarak 2'den 100'e
#          kadar olan tum asal sayilari listeleyin
# TODO: b) Ciktida toplam kac asal sayi bulundugunu
#          yazdirin
# ============================================


# BONUS: Karekok Optimizasyonu
# TODO: a) import math ile math.isqrt(n) fonksiyonunu
#          kullanarak fonksiyonunuzu optimize edin
# TODO: b) Bolenleri sadece karekoke kadar kontrol edin
# Neden? Eger n = a * b ise, a ve b'den en az biri
#         sqrt(n)'den kucuk veya esit olmalidir
# ============================================


"""
BEKLENEN CIKTI (temel kod):
----------------------------
True
False
"""
