"""
Metin Tabanlı Macera Oyunu - Zindanın Derinlikleri

Bu mini proje, Bölüm 2'de öğrenilen tüm kavramları bir araya getirir:
- Koşullu ifadeler (if/elif/else)
- Döngüler (while, for)
- Fonksiyonlar (def, return, parametreler)
- Veri yapıları (liste, sözlük)

Bölüm: 02 - Python Kontrol Yapıları ve Fonksiyonlar
Ünite: 4 - Veri Yapıları Temelleri

Çalıştırma: python metin_macera.py
Gereksinimler: Python 3.x (ek kütüphane gerektirmez)
"""

import random

# =============================================================================
# Oyun Verileri
# =============================================================================

# Oyuncu başlangıç değerleri
oyuncu = {
    "isim": "",
    "can": 100,
    "max_can": 100,
    "guc": 15,
    "altin": 0,
    "envanter": []
}

# Düşman türleri ve özellikleri
dusmanlar = {
    "Goblin": {"can": 30, "hasar": 10, "altin": 10},
    "Ork": {"can": 50, "hasar": 15, "altin": 25},
    "İskelet": {"can": 40, "hasar": 12, "altin": 15},
    "Trol": {"can": 80, "hasar": 20, "altin": 50}
}

# =============================================================================
# Yardımcı Fonksiyonlar
# =============================================================================

def temizle_ekran():
    """Ekranı temizlemek için boş satırlar yazdır."""
    print("\n" * 2)


def durum_goster():
    """Oyuncu durumunu göster."""
    print(f"\n{'='*50}")
    print(f"  {oyuncu['isim']} | Can: {oyuncu['can']}/{oyuncu['max_can']}")
    print(f"  Güç: {oyuncu['guc']} | Altın: {oyuncu['altin']}")
    if oyuncu['envanter']:
        print(f"  Envanter: {', '.join(oyuncu['envanter'])}")
    print(f"{'='*50}\n")


def iyiles(miktar):
    """Oyuncuyu belirtilen miktar kadar iyileştir."""
    oyuncu['can'] += miktar
    if oyuncu['can'] > oyuncu['max_can']:
        oyuncu['can'] = oyuncu['max_can']
    print(f"[+] {miktar} can kazandin! Su anki can: {oyuncu['can']}")


def gecerli_secim_al(secenekler):
    """Kullanıcıdan geçerli bir seçim al."""
    while True:
        secim = input("Seçimin: ").strip()
        if secim in secenekler:
            return secim
        print("Geçersiz seçim! Tekrar dene.")


# =============================================================================
# Savaş Sistemi
# =============================================================================

def savas(dusman_adi):
    """
    Düşmanla savaş yap.

    Args:
        dusman_adi: Savaşılacak düşmanın adı

    Returns:
        bool: Oyuncu kazandıysa True, kaybettiyse False
    """
    dusman = dusmanlar[dusman_adi].copy()

    print(f"\n{'-'*40}")
    print(f"[SAVAS] {dusman_adi} ile karsilastin!")
    print(f"Dusman Can: {dusman['can']} | Hasar: {dusman['hasar']}")
    print(f"{'-'*40}")

    while dusman['can'] > 0 and oyuncu['can'] > 0:
        print("\n1. Saldır")
        print("2. İksir Kullan")
        print("3. Kaç")

        secim = gecerli_secim_al(["1", "2", "3"])

        if secim == "1":
            # Oyuncu saldırır
            hasar = random.randint(oyuncu['guc'] - 5, oyuncu['guc'] + 5)
            hasar = max(1, hasar)  # En az 1 hasar
            dusman['can'] -= hasar
            print(f"[SALDIRI] {hasar} hasar verdin!")

            if dusman['can'] > 0:
                # Düşman karşılık verir
                dusman_hasar = random.randint(
                    dusman['hasar'] - 3,
                    dusman['hasar'] + 3
                )
                dusman_hasar = max(1, dusman_hasar)
                oyuncu['can'] -= dusman_hasar
                print(f"[HASAR] {dusman_adi} sana {dusman_hasar} hasar verdi!")
                print(f"   Canın: {oyuncu['can']}")

        elif secim == "2":
            if "Sağlık İksiri" in oyuncu['envanter']:
                oyuncu['envanter'].remove("Sağlık İksiri")
                iyiles(30)
            else:
                print("[X] Iksirin yok!")

        elif secim == "3":
            if random.random() < 0.5:
                print("[KACIS] Kacmayi basardin!")
                return True
            else:
                print("[X] Kacamadin!")
                hasar = dusman['hasar']
                oyuncu['can'] -= hasar
                print(f"[HASAR] Kacarken {hasar} hasar aldin!")

    # Savaş sonucu
    if oyuncu['can'] <= 0:
        print("\n[OLUM] Oldun!")
        return False
    else:
        print(f"\n[ZAFER] {dusman_adi}'i yendin!")
        kazanc = dusmanlar[dusman_adi]['altin']
        oyuncu['altin'] += kazanc
        print(f"[ALTIN] {kazanc} altin kazandin!")
        return True


# =============================================================================
# Oda Olayları
# =============================================================================

def bos_oda():
    """Boş oda - dinlenme fırsatı."""
    print("\n[ODA] Bos bir odaya girdin.")
    print("Biraz dinlenebilirsin.")
    if oyuncu['can'] < oyuncu['max_can']:
        iyiles(10)
    else:
        print("Zaten tam candasın.")


def hazine_odasi():
    """Hazine odası."""
    print("\n[HAZINE] Bir hazine sandigi buldun!")
    altin = random.randint(20, 50)
    oyuncu['altin'] += altin
    print(f"[ALTIN] {altin} altin buldun!")

    if random.random() < 0.3:
        oyuncu['envanter'].append("Sağlık İksiri")
        print("[IKSIR] Bir Saglik Iksiri de buldun!")


def tuzak_odasi():
    """Tuzak odası."""
    print("\n[UYARI] Tuzaga dustun!")
    hasar = random.randint(10, 20)
    oyuncu['can'] -= hasar
    print(f"[HASAR] {hasar} hasar aldin!")
    print(f"Kalan can: {oyuncu['can']}")


def dusman_odasi():
    """Düşman odası - rastgele düşmanla savaş."""
    dusman = random.choice(list(dusmanlar.keys()))
    return savas(dusman)


def dukkan():
    """Ara sıra çıkan gezici tüccar."""
    print("\n[DUKKAN] Gezici bir tuccar ile karsilastin!")
    print("Tuccar: 'Ne almak istersin, yolcu?'")

    while True:
        print(f"\nAltının: {oyuncu['altin']}")
        print("1. Sağlık İksiri (20 altın)")
        print("2. Güç Artışı (50 altın, +5 güç)")
        print("3. Ayrıl")

        secim = gecerli_secim_al(["1", "2", "3"])

        if secim == "1":
            if oyuncu['altin'] >= 20:
                oyuncu['altin'] -= 20
                oyuncu['envanter'].append("Sağlık İksiri")
                print("[IKSIR] Saglik Iksiri aldin!")
            else:
                print("Yeterli altının yok!")

        elif secim == "2":
            if oyuncu['altin'] >= 50:
                oyuncu['altin'] -= 50
                oyuncu['guc'] += 5
                print(f"[GUC] Guc artti! Yeni guc: {oyuncu['guc']}")
            else:
                print("Yeterli altının yok!")

        elif secim == "3":
            print("Tuccar: 'Yine beklerim!'")
            break


# =============================================================================
# Ana Oyun Döngüsü
# =============================================================================

def oyunu_baslat():
    """Ana oyun fonksiyonu."""
    # Başlık ekranı
    print("\n" + "="*50)
    print("        ZINDANIN DERİNLİKLERİ")
    print("        Metin Tabanlı Macera Oyunu")
    print("="*50)
    print("\nBu oyunda bir zindanı keşfedeceksin.")
    print("Düşmanlarla savaş, hazineler bul ve hayatta kal!")

    # Oyuncu ismi al
    oyuncu['isim'] = input("\nAdın ne, cesur kahraman? ").strip()
    if not oyuncu['isim']:
        oyuncu['isim'] = "Adsız Kahraman"

    print(f"\nHoş geldin {oyuncu['isim']}! Zindan seni bekliyor...")
    input("Devam etmek için Enter'a bas...")

    # Oyun değişkenleri
    oda_sayisi = 10
    mevcut_oda = 0

    # Ana oyun döngüsü
    while mevcut_oda < oda_sayisi and oyuncu['can'] > 0:
        mevcut_oda += 1
        temizle_ekran()

        print(f"\n{'='*50}")
        print(f"                ODA {mevcut_oda}/{oda_sayisi}")
        print(f"{'='*50}")

        durum_goster()

        # Rastgele oda olayı
        olay = random.choices(
            ['bos', 'hazine', 'tuzak', 'dusman', 'dukkan'],
            weights=[15, 20, 15, 40, 10]
        )[0]

        if olay == 'bos':
            bos_oda()
        elif olay == 'hazine':
            hazine_odasi()
        elif olay == 'tuzak':
            tuzak_odasi()
        elif olay == 'dusman':
            if not dusman_odasi():
                break
        elif olay == 'dukkan':
            dukkan()

        # Oyuncu hâlâ yaşıyor mu kontrol et
        if oyuncu['can'] <= 0:
            break

        input("\nDevam etmek için Enter'a bas...")

    # Oyun sonu
    temizle_ekran()
    print("\n" + "="*50)

    if oyuncu['can'] > 0 and mevcut_oda >= oda_sayisi:
        print("    [BASARI] TEBRİKLER! ZİNDANI TAMAMLADIN!")
        print(f"\n    {oyuncu['isim']} efsanevi bir kahraman oldu!")
    else:
        print("           [GAME OVER] GAME OVER")
        print(f"\n    {oyuncu['isim']} zindanda yenildi...")

    print(f"\n    Istatistikler:")
    print(f"    -----------------")
    print(f"    Keşfedilen oda: {mevcut_oda}")
    print(f"    Toplanan altın: {oyuncu['altin']}")
    print(f"    Final can: {max(0, oyuncu['can'])}")
    print("="*50)

    # Tekrar oyna?
    print("\nTekrar oynamak ister misin?")
    cevap = input("(E/H): ").strip().upper()
    if cevap == "E":
        # Değerleri sıfırla
        oyuncu['can'] = 100
        oyuncu['guc'] = 15
        oyuncu['altin'] = 0
        oyuncu['envanter'] = []
        oyunu_baslat()


# =============================================================================
# Program Başlangıcı
# =============================================================================

if __name__ == "__main__":
    oyunu_baslat()


"""
BEKLENEN ÇIKTI:
---------------
Oyun başladığında oyuncudan isim alınır ve zindan macerası başlar.
Her odada farklı olaylar yaşanır:
- Boş oda: Dinlenme, can yenileme
- Hazine: Altın ve iksir bulma
- Tuzak: Hasar alma
- Düşman: Savaş mekaniği
- Dükkan: Eşya satın alma

Oyun, 10 oda tamamlanınca veya oyuncu ölünce biter.

ÖRNEK OYUN AKIŞI:
================
> Adın ne, cesur kahraman? Ahmet
> Hoş geldin Ahmet! Zindan seni bekliyor...

ODA 1/10
=== Ahmet | Can: 100/100 ===
Güç: 15 | Altın: 0

[SAVAS] Goblin ile karsilastin!
1. Saldır
2. İksir Kullan
3. Kaç
> 1
[SALDIRI] 17 hasar verdin!
[HASAR] Goblin sana 8 hasar verdi!
...
"""
