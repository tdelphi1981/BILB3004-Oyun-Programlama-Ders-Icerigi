"""
Sayı Tahmin Oyunu - Mini Proje

Bilgisayar 1-100 arasında rastgele bir sayı seçer.
Oyuncu sayıyı tahmin etmeye çalışır.

Öğrenilecek kavramlar:
- import ve random modülü
- input() ile kullanıcı girişi
- f-string formatlama
- Temel oyun mantığı

Bölüm: 01 - Python'a Giriş
Ünite: 4 - Temel Giriş/Çıkış

Çalıştırma: python 01_sayi_tahmin.py
"""

import random

def oyun_baslat():
    """Ana oyun fonksiyonu"""
    print()
    print("+============================+")
    print("|   SAYI TAHMIN OYUNU        |")
    print("|   1-100 arasi bir sayi     |")
    print("+============================+")
    print()

    # Oyun ayarları
    gizli_sayi = random.randint(1, 100)
    max_deneme = 7
    deneme = 0
    kazandi = False

    print(f"[IPUCU] {max_deneme} deneme hakkın var!")
    print()

    # Oyun döngüsü
    while deneme < max_deneme and not kazandi:
        deneme += 1
        kalan = max_deneme - deneme

        # Tahmin al
        try:
            tahmin = int(input(f"[{deneme}/{max_deneme}] Tahminin: "))
        except ValueError:
            print("[UYARI] Lütfen geçerli bir sayı gir!")
            deneme -= 1  # Hatalı giriş hak götürmesin
            continue

        # 1-100 aralık kontrolü
        if tahmin < 1 or tahmin > 100:
            print("[UYARI] 1-100 arası bir sayı gir!")
            deneme -= 1
            continue

        # Kontrol et
        if tahmin == gizli_sayi:
            kazandi = True
            print()
            print("[BASARI] " + "=" * 26)
            print(f"   TEBRİKLER! {deneme} denemede buldun!")

            # Puan hesapla
            if deneme == 1:
                puan = 1000
            elif deneme <= 3:
                puan = 750
            elif deneme <= 5:
                puan = 500
            else:
                puan = 250

            print(f"   Kazanılan puan: {puan}")
            print("[BASARI] " + "=" * 26)

        elif tahmin < gizli_sayi:
            print(f"   [YUKARI] Daha BÜYÜK! (Kalan hak: {kalan})")
        else:
            print(f"   [ASAGI] Daha KÜÇÜK! (Kalan hak: {kalan})")

    # Kaybettiyse
    if not kazandi:
        print()
        print("[GAME OVER] " + "=" * 24)
        print(f"   Kaybettin! Sayı: {gizli_sayi}")
        print("[GAME OVER] " + "=" * 24)

    # Tekrar oyna
    print()
    tekrar = input("Tekrar oynamak ister misin? (e/h): ")
    if tekrar.lower() == 'e':
        oyun_baslat()
    else:
        print("\nOynadığın için teşekkürler!")


# Oyunu başlat
if __name__ == "__main__":
    oyun_baslat()
