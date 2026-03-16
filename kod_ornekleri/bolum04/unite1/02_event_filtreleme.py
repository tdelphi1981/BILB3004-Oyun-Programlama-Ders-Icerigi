"""
Olay Filtreleme ve Ozel Olaylar

Bu program olay filtreleme (set_blocked/set_allowed),
ozel olay tanimlama (USEREVENT) ve zamanlayici olaylari
(set_timer) bir arada gosterir.

Ogrenilecek kavramlar:
- pygame.event.set_blocked() ile olay engelleme
- pygame.event.set_allowed() ile izin listesi
- USEREVENT ile ozel olay tanimlama
- pygame.event.post() ile olay gonderme
- pygame.time.set_timer() ile zamanlayici olay

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 1 - Event Sistemi

Calistirma: python 02_event_filtreleme.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 640
YUKSEKLIK = 480
BASLIK = "Olay Filtreleme ve Ozel Olaylar"
FPS = 60

# Renkler
ARKA_PLAN = (15, 15, 35)
BEYAZ = (255, 255, 255)
SARI = (255, 220, 50)
YESIL = (50, 220, 100)
KIRMIZI = (220, 50, 50)
MAVI = (50, 150, 255)

# Ozel olay turleri
DUSMAN_OLUSTUR = pygame.USEREVENT + 1
BONUS_ZAMANI = pygame.USEREVENT + 2
SKOR_GUNCELLE = pygame.USEREVENT + 3


def main():
    """Ana fonksiyon."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Font olustur
    font = pygame.font.SysFont("Arial", 18)
    baslik_font = pygame.font.SysFont("Arial", 22, bold=True)

    # --- Olay Filtreleme ---
    # MOUSEMOTION olaylarini engelle (gereksiz, performans icin)
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    print("[FILTRE] MOUSEMOTION olaylari engellendi.")

    # --- Zamanlayici Olaylari ---
    # Her 3 saniyede bir dusman olusturma olayini gonder
    pygame.time.set_timer(DUSMAN_OLUSTUR, 3000)
    print("[TIMER] Dusman olusturma: her 3 saniye")

    # Her 5 saniyede bir bonus zamani olayini gonder
    pygame.time.set_timer(BONUS_ZAMANI, 5000)
    print("[TIMER] Bonus zamani: her 5 saniye")

    # Oyun degiskenleri
    skor = 0
    dusman_sayisi = 0
    bonus_sayisi = 0
    mesajlar = []
    maksimum_mesaj = 12

    def mesaj_ekle(metin, renk=BEYAZ):
        """Ekrana mesaj ekler, eski mesajlari siler."""
        mesajlar.append((metin, renk))
        if len(mesajlar) > maksimum_mesaj:
            mesajlar.pop(0)

    mesaj_ekle("Program basladi. Tus veya fare tiklama dene.", MAVI)
    mesaj_ekle("MOUSEMOTION olaylari engellendi.", SARI)
    mesaj_ekle("Zamanlayicilar aktif: Dusman(3sn), Bonus(5sn)", SARI)
    mesaj_ekle("SPACE: Skor olayini gonder | ESC: Cikis", MAVI)

    print("\n" + "=" * 50)
    print("Olay Filtreleme Ornegi Basladi")
    print("SPACE: Skor olayini gonder | ESC: Cikis")
    print("=" * 50)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            # Pencere kapatma
            if olay.type == pygame.QUIT:
                calistir = False

            # Klavye olaylari
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False
                elif olay.key == pygame.K_SPACE:
                    # Ozel skor olayini olustur ve gonder
                    skor_olayi = pygame.event.Event(
                        SKOR_GUNCELLE, puan=10, kaynak="oyuncu"
                    )
                    pygame.event.post(skor_olayi)
                    print("[POST] Skor guncelleme olayi gonderildi.")
                else:
                    tus_adi = pygame.key.name(olay.key)
                    mesaj_ekle(f"KEYDOWN: {tus_adi}", BEYAZ)

            # Fare tiklama (MOUSEMOTION engellendigini goster)
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                mesaj_ekle(
                    f"MOUSEBUTTONDOWN: konum={olay.pos}, "
                    f"dugme={olay.button}",
                    BEYAZ
                )

            # --- Ozel Olaylari Isle ---

            # Dusman olusturma zamanlayicisi
            elif olay.type == DUSMAN_OLUSTUR:
                dusman_sayisi += 1
                mesaj_ekle(
                    f"[DUSMAN] Yeni dusman! Toplam: {dusman_sayisi}",
                    KIRMIZI
                )
                print(f"[DUSMAN] Olusturuldu. Toplam: {dusman_sayisi}")

            # Bonus zamanlayicisi
            elif olay.type == BONUS_ZAMANI:
                bonus_sayisi += 1
                skor += 25
                mesaj_ekle(
                    f"[BONUS] +25 puan! Toplam bonus: {bonus_sayisi}",
                    YESIL
                )
                print(f"[BONUS] Kazanildi. Skor: {skor}")

            # Skor guncelleme ozel olayi
            elif olay.type == SKOR_GUNCELLE:
                skor += olay.puan
                mesaj_ekle(
                    f"[SKOR] +{olay.puan} puan "
                    f"(kaynak: {olay.kaynak}). "
                    f"Toplam: {skor}",
                    SARI
                )
                print(f"[SKOR] +{olay.puan}. Toplam: {skor}")

        # --- Cizim ---
        ekran.fill(ARKA_PLAN)

        # Baslik
        baslik = baslik_font.render(
            "Olay Filtreleme ve Ozel Olaylar", True, MAVI
        )
        ekran.blit(baslik, (20, 15))

        # Durum bilgileri
        durum_metinleri = [
            f"Skor: {skor}",
            f"Dusmanlar: {dusman_sayisi}",
            f"Bonuslar: {bonus_sayisi}",
        ]
        for i, metin in enumerate(durum_metinleri):
            yazi = font.render(metin, True, SARI)
            ekran.blit(yazi, (20 + i * 200, 50))

        # Ayirici cizgi
        pygame.draw.line(ekran, MAVI, (20, 80), (GENISLIK - 20, 80), 1)

        # Mesaj listesi
        for i, (metin, renk) in enumerate(mesajlar):
            yazi = font.render(metin, True, renk)
            ekran.blit(yazi, (20, 95 + i * 28))

        pygame.display.flip()
        saat.tick(FPS)

    # Zamanlayicilari durdur
    pygame.time.set_timer(DUSMAN_OLUSTUR, 0)
    pygame.time.set_timer(BONUS_ZAMANI, 0)

    print("\n" + "=" * 50)
    print(f"Son skor: {skor}")
    print(f"Toplam dusman: {dusman_sayisi}")
    print(f"Toplam bonus: {bonus_sayisi}")
    print("Program sonlandi.")
    print("=" * 50)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
[FILTRE] MOUSEMOTION olaylari engellendi.
[TIMER] Dusman olusturma: her 3 saniye
[TIMER] Bonus zamani: her 5 saniye

==================================================
Olay Filtreleme Ornegi Basladi
SPACE: Skor olayini gonder | ESC: Cikis
==================================================
[POST] Skor guncelleme olayi gonderildi.
[SKOR] +10. Toplam: 10
[DUSMAN] Olusturuldu. Toplam: 1
[BONUS] Kazanildi. Skor: 35
[DUSMAN] Olusturuldu. Toplam: 2
...
==================================================
Son skor: 85
Toplam dusman: 4
Toplam bonus: 2
Program sonlandi.
==================================================
"""
