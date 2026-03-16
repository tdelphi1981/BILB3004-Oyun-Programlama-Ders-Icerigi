"""
Event Gozlemcisi - Tum olaylari konsola yazdir

Bu program bir PyGame penceresi acar ve kullanici tarafindan
uretilen tum olaylari detayli formatta konsola yazdirir.
Her olay turu icin farkli bilgiler gosterilir.

Ogrenilecek kavramlar:
- pygame.event.get() ile olay kuyrugunu okuma
- Event nesnesinin type, key, pos, button ozellikleri
- Olay turlerine gore farkli bilgilere erisim
- Olay sayaci ile istatistik tutma

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 1 - Event Sistemi

Calistirma: python 01_event_gozlemci.py
Gereksinimler: pygame
"""

import pygame

# Sabitler
GENISLIK = 640
YUKSEKLIK = 480
BASLIK = "Event Gozlemcisi"
ARKA_PLAN = (20, 20, 40)
FPS = 60


def olay_bilgisi_yazdir(olay, sayac):
    """Olay turune gore detayli bilgi yazdirir."""

    # QUIT olayini isle
    if olay.type == pygame.QUIT:
        print(f"[{sayac}] QUIT - Pencere kapatma istegi")
        return

    # KEYDOWN olayini isle
    if olay.type == pygame.KEYDOWN:
        tus_adi = pygame.key.name(olay.key)
        karakter = olay.unicode if olay.unicode else "(yok)"
        mod_bilgi = ""
        if olay.mod & pygame.KMOD_SHIFT:
            mod_bilgi += " +Shift"
        if olay.mod & pygame.KMOD_CTRL:
            mod_bilgi += " +Ctrl"
        if olay.mod & pygame.KMOD_ALT:
            mod_bilgi += " +Alt"
        print(
            f"[{sayac}] KEYDOWN - Tus: {tus_adi} "
            f"(kod: {olay.key}), Karakter: {karakter}{mod_bilgi}"
        )
        return

    # KEYUP olayini isle
    if olay.type == pygame.KEYUP:
        tus_adi = pygame.key.name(olay.key)
        print(f"[{sayac}] KEYUP   - Tus: {tus_adi} (kod: {olay.key})")
        return

    # MOUSEBUTTONDOWN olayini isle
    if olay.type == pygame.MOUSEBUTTONDOWN:
        dugme_adi = {1: "Sol", 2: "Orta", 3: "Sag",
                     4: "Tekerlek yukari", 5: "Tekerlek asagi"}
        adi = dugme_adi.get(olay.button, f"Dugme {olay.button}")
        print(
            f"[{sayac}] MOUSEBUTTONDOWN - "
            f"Konum: {olay.pos}, Dugme: {adi} ({olay.button})"
        )
        return

    # MOUSEBUTTONUP olayini isle
    if olay.type == pygame.MOUSEBUTTONUP:
        print(
            f"[{sayac}] MOUSEBUTTONUP   - "
            f"Konum: {olay.pos}, Dugme: {olay.button}"
        )
        return

    # MOUSEMOTION olayini isle (cok sik uretilir, kisaca yazdir)
    if olay.type == pygame.MOUSEMOTION:
        basili = []
        if olay.buttons[0]:
            basili.append("Sol")
        if olay.buttons[1]:
            basili.append("Orta")
        if olay.buttons[2]:
            basili.append("Sag")
        basili_str = ", ".join(basili) if basili else "Yok"
        print(
            f"[{sayac}] MOUSEMOTION     - "
            f"Konum: {olay.pos}, Fark: {olay.rel}, "
            f"Basili: {basili_str}"
        )
        return

    # Diger olay turleri
    print(f"[{sayac}] Olay turu: {olay.type} - {olay}")


def main():
    """Ana fonksiyon."""
    pygame.init()

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    olay_sayaci = 0

    print("=" * 60)
    print("Event Gozlemcisi Basladi")
    print("Klavye tuslarini dene, fareyi hareket ettir, tikla.")
    print("Kapatmak icin pencereyi kapat veya ESC tusuna bas.")
    print("=" * 60)

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            olay_sayaci += 1
            olay_bilgisi_yazdir(olay, olay_sayaci)

            if olay.type == pygame.QUIT:
                calistir = False
            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

        ekran.fill(ARKA_PLAN)
        pygame.display.flip()
        saat.tick(FPS)

    print("=" * 60)
    print(f"Toplam {olay_sayaci} olay islendi.")
    print("Program sonlandi.")
    print("=" * 60)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
============================================================
Event Gozlemcisi Basladi
Klavye tuslarini dene, fareyi hareket ettir, tikla.
Kapatmak icin pencereyi kapat veya ESC tusuna bas.
============================================================
[1] MOUSEMOTION     - Konum: (320, 240), Fark: (0, 0), Basili: Yok
[2] KEYDOWN - Tus: a (kod: 97), Karakter: a
[3] KEYUP   - Tus: a (kod: 97)
[4] MOUSEBUTTONDOWN - Konum: (150, 200), Dugme: Sol (1)
[5] MOUSEBUTTONUP   - Konum: (150, 200), Dugme: 1
...
[42] QUIT - Pencere kapatma istegi
============================================================
Toplam 42 olay islendi.
Program sonlandi.
============================================================
"""
