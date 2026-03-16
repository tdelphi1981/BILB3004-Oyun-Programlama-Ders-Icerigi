"""
Fare Takip ve Iz Efekti

Ekrandaki bir daire, fare imlecini lerp teknigi ile
kademeli olarak takip eder. Farenin arkasinda giderek
kuculen dairelerden olusan bir iz efekti olusur.
Fare imleci gizlenir ve yerine ozel cizim yapilir.

Ogrenilecek kavramlar:
- MOUSEMOTION olayi ve olay.pos
- pygame.mouse.get_pos() ile anlik konum sorgulama
- pygame.mouse.set_visible() ile imleci gizleme
- Lerp (dogrusal enterpolasyon) ile yumusak takip
- Liste ile iz efekti olusturma

Bolum: 04 - Kullanici Girdileri ve Hareket
Unite: 3 - Fare Girdileri

Calistirma: python 02_fare_takip.py
Gereksinimler: pygame
"""

import pygame

# --- Sabitler ---
GENISLIK = 800
YUKSEKLIK = 600
BASLIK = "Fare Takip - Iz Efekti"
FPS = 60

ARKA_PLAN = (15, 15, 30)
TAKIP_RENGI = (100, 200, 255)
IZ_RENGI = (60, 140, 220)
NESNE_YARICAP = 18

# Lerp orani: 0.0 (hareketsiz) - 1.0 (aninda yapisir)
TAKIP_HIZI = 0.06

# Iz efekti icin saklanacak konum sayisi
IZ_UZUNLUGU = 25


def main():
    """Ana oyun fonksiyonu."""
    pygame.init()
    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()

    # Fare imlecini gizle
    pygame.mouse.set_visible(False)

    # Takip eden nesnenin baslangic konumu (ekran ortasi)
    nesne_x = float(GENISLIK // 2)
    nesne_y = float(YUKSEKLIK // 2)

    # Iz konumlarini saklayan liste
    iz = []

    calistir = True
    while calistir:
        # --- Olay isleme ---
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

        # --- Guncelleme ---
        # Farenin o anki konumunu al
        hedef_x, hedef_y = pygame.mouse.get_pos()

        # Lerp ile nesneyi hedefe yaklastir
        nesne_x += (hedef_x - nesne_x) * TAKIP_HIZI
        nesne_y += (hedef_y - nesne_y) * TAKIP_HIZI

        # Mevcut konumu iz listesine ekle
        iz.append((int(nesne_x), int(nesne_y)))

        # Iz listesi maksimum uzunlugu asarsa eski konumlari sil
        if len(iz) > IZ_UZUNLUGU:
            iz.pop(0)

        # --- Cizim ---
        ekran.fill(ARKA_PLAN)

        # Iz efektini ciz (eski konumlar kucuk ve soluk)
        for i, konum in enumerate(iz):
            # Oran: 0.0 (en eski) -> 1.0 (en yeni)
            oran = (i + 1) / len(iz)

            # Yaricap orana gore buyur
            yaricap = max(2, int(NESNE_YARICAP * oran * 0.7))

            # Renk orana gore parlaklik kazanir
            r = int(IZ_RENGI[0] * oran)
            g = int(IZ_RENGI[1] * oran)
            b = int(IZ_RENGI[2] * oran)

            pygame.draw.circle(ekran, (r, g, b), konum, yaricap)

        # Ana takipci nesneyi ciz
        pygame.draw.circle(
            ekran, TAKIP_RENGI,
            (int(nesne_x), int(nesne_y)),
            NESNE_YARICAP,
        )

        # Fare konumunda kucuk bir nokta (hedef gostergesi)
        pygame.draw.circle(ekran, (255, 255, 255), (hedef_x, hedef_y), 3)

        # Bilgi metni
        font = pygame.font.Font(None, 24)
        bilgi = f"Fare: ({hedef_x}, {hedef_y}) | Nesne: ({int(nesne_x)}, {int(nesne_y)})"
        metin = font.render(bilgi, True, (180, 180, 180))
        ekran.blit(metin, (10, 10))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()


"""
BEKLENEN CIKTI:
---------------
800x600 piksel boyutunda koyu bir pencere acilir.
Fare imleci gizlenir, yerine beyaz bir nokta gorunur.
Mavi bir daire fareyi yumusak bir sekilde takip eder.
Dairenin arkasinda giderek kuculen ve solan dairelerden
olusan bir iz efekti gorulur.
Sol ust kosede fare ve nesne koordinatlari gosterilir.
"""
