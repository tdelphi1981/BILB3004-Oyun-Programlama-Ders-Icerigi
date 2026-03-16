"""
Fonksiyonlar Örnekleri

Bu dosya fonksiyon tanımlama, parametreler, return ve
scope kavramlarını oyun geliştirme bağlamında gösterir.

Bölüm: 02 - Python Kontrol Yapıları ve Fonksiyonlar
Ünite: 3 - Fonksiyonlar

Çalıştırma: python 03_fonksiyonlar.py
"""

import random

# =============================================================================
# Örnek 1: Basit Fonksiyon
# =============================================================================
print("=== Örnek 1: Basit Fonksiyon ===")


def selamla():
    """Oyuncuyu selamla."""
    print("Merhaba, Maceraperest!")
    print("Yeni bir oyuna hoş geldin!")


selamla()

# =============================================================================
# Örnek 2: Parametreli Fonksiyon
# =============================================================================
print("\n=== Örnek 2: Parametreli Fonksiyon ===")


def selamla_isimle(isim):
    """Oyuncuyu ismiyle selamla."""
    print(f"Merhaba, {isim}!")


selamla_isimle("Ahmet")
selamla_isimle("Zeynep")

# =============================================================================
# Örnek 3: Çoklu Parametre
# =============================================================================
print("\n=== Örnek 3: Çoklu Parametre ===")


def hasar_ver(hedef, miktar):
    """Hedefe hasar ver."""
    print(f"{hedef} {miktar} hasar aldı!")


hasar_ver("Goblin", 25)
hasar_ver("Ejderha", 100)

# =============================================================================
# Örnek 4: Varsayılan Parametre
# =============================================================================
print("\n=== Örnek 4: Varsayılan Parametre ===")


def saldir(silah="Yumruk", hasar=5):
    """Saldırı yap."""
    print(f"{silah} ile saldırdın! {hasar} hasar!")


saldir()
saldir("Kılıç")
saldir("Balta", 15)
saldir(hasar=100)

# =============================================================================
# Örnek 5: Return ile Değer Döndürme
# =============================================================================
print("\n=== Örnek 5: Return ===")


def hasar_hesapla(guc, silah_bonusu, zirh):
    """Hasar hesapla ve döndür."""
    ham_hasar = guc + silah_bonusu
    gercek_hasar = ham_hasar - zirh
    return max(0, gercek_hasar)


hasar = hasar_hesapla(20, 10, 15)
print(f"Verilen hasar: {hasar}")

# =============================================================================
# Örnek 6: Boolean Döndürme
# =============================================================================
print("\n=== Örnek 6: Boolean Return ===")


def hayatta_mi(can):
    """Oyuncu hayatta mı kontrol et."""
    return can > 0


def yeterli_mana_var_mi(mana, maliyet):
    """Yeterli mana var mı kontrol et."""
    return mana >= maliyet


print(f"Hayatta mı (can=50): {hayatta_mi(50)}")
print(f"Hayatta mı (can=0): {hayatta_mi(0)}")
print(f"Mana yeterli mi (30 >= 25): {yeterli_mana_var_mi(30, 25)}")

# =============================================================================
# Örnek 7: Çoklu Değer Döndürme
# =============================================================================
print("\n=== Örnek 7: Çoklu Return ===")


def oyuncu_durumu(isim, seviye, deneyim):
    """Oyuncu durumunu hesapla."""
    sonraki_seviye_xp = seviye * 100
    kalan_xp = sonraki_seviye_xp - deneyim
    return seviye, kalan_xp, sonraki_seviye_xp


mevcut, kalan, gereken = oyuncu_durumu("Kahraman", 5, 420)
print(f"Seviye: {mevcut}")
print(f"Sonraki seviye: {gereken} XP")
print(f"Kalan: {kalan} XP")

# =============================================================================
# Örnek 8: Erken Return
# =============================================================================
print("\n=== Örnek 8: Erken Return ===")


def buyu_kullan(mana, maliyet, sessiz=False):
    """Büyü kullan ve sonucu döndür."""
    if mana < maliyet:
        return "Yetersiz mana!"

    if sessiz:
        return "Büyü sessizce kullanıldı..."

    return "Büyü kullanıldı!"


print(buyu_kullan(10, 50))
print(buyu_kullan(100, 50, sessiz=True))
print(buyu_kullan(100, 50))

# =============================================================================
# Örnek 9: Zar Atma Fonksiyonu
# =============================================================================
print("\n=== Örnek 9: Zar Atma ===")


def zar_at(yuz_sayisi=6):
    """Zar at ve sonucu döndür."""
    return random.randint(1, yuz_sayisi)


def coklu_zar_at(zar_adedi, yuz_sayisi=6):
    """Birden fazla zar at."""
    sonuclar = []
    for _ in range(zar_adedi):
        sonuclar.append(zar_at(yuz_sayisi))
    return sonuclar, sum(sonuclar)


print(f"D6 zarı: {zar_at()}")
print(f"D20 zarı: {zar_at(20)}")

zarlar, toplam = coklu_zar_at(3)
print(f"3D6: {zarlar} = {toplam}")

# =============================================================================
# Örnek 10: Karakter Oluşturma Sistemi
# =============================================================================
print("\n=== Örnek 10: Karakter Sistemi ===")


def karakter_olustur(isim, sinif="Savaşçı", can=100, guc=10):
    """Yeni karakter oluştur."""
    karakter = {
        "isim": isim,
        "sinif": sinif,
        "seviye": 1,
        "can": can,
        "guc": guc
    }
    return karakter


def karakter_goster(k):
    """Karakter bilgilerini göster."""
    print(f"  {k['isim']} - {k['sinif']} (Lv.{k['seviye']})")
    print(f"  Can: {k['can']} | Güç: {k['guc']}")


kahraman = karakter_olustur("Thorin")
karakter_goster(kahraman)

buyucu = karakter_olustur("Gandalf", sinif="Büyücü", can=80, guc=25)
karakter_goster(buyucu)

# =============================================================================
# Örnek 11: Savaş Fonksiyonları
# =============================================================================
print("\n=== Örnek 11: Savaş Sistemi ===")


def saldir_hesapla(saldiran_guc, hedef_zirh):
    """Saldırı hasarını hesapla."""
    hasar = saldiran_guc - hedef_zirh
    kritik = random.random() < 0.1  # %10 kritik şansı

    if kritik:
        hasar *= 2

    return max(1, hasar), kritik


def savasi_coz(oyuncu_guc, dusman_can, dusman_zirh):
    """Savaşı simüle et."""
    tur = 0

    while dusman_can > 0:
        tur += 1
        hasar, kritik = saldir_hesapla(oyuncu_guc, dusman_zirh)
        dusman_can -= hasar

        if kritik:
            print(f"Tur {tur}: KRİTİK! {hasar} hasar, kalan: {dusman_can}")
        else:
            print(f"Tur {tur}: {hasar} hasar, kalan: {dusman_can}")

    return tur


toplam_tur = savasi_coz(oyuncu_guc=25, dusman_can=100, dusman_zirh=10)
print(f"Düşman {toplam_tur} turda yenildi!")


"""
BEKLENEN ÇIKTI:
---------------
=== Örnek 1: Basit Fonksiyon ===
Merhaba, Maceraperest!
Yeni bir oyuna hoş geldin!

=== Örnek 2: Parametreli Fonksiyon ===
Merhaba, Ahmet!
Merhaba, Zeynep!

... (diğer örnekler)
"""
