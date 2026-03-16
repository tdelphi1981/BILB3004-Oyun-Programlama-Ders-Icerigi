"""
Kanal Yonetimi - Channel ile Ses Kontrolu

Bu program pygame.mixer.Channel kullanimini gosterir:
belirli kanalda ses calma, kanal kontrolu ve set_endevent().

Ogrenilecek kavramlar:
- pygame.mixer.Channel olusturma
- Belirli kanalda ses calma
- Kanal pause/unpause
- queue() ile sirali calma
- set_endevent() ile olay tetikleme

Bolum: 07 - Ses ve Muzik
Unite: 2 - Ses Efektleri

Calistirma: python 03_kanal_yonetimi.py
Gereksinimler: pygame
"""

import pygame
import array

# Sabitler
GENISLIK = 700
YUKSEKLIK = 450
BASLIK = "Kanal Yonetimi"
FPS = 60

# Ozel olay: ses bitti
SES_BITTI = pygame.USEREVENT + 1


def ses_olustur(frekans=440, sure_ms=1000):
    """Basit test ses dalgasi olustur."""
    ornekleme = 44100
    ornek_sayisi = int(ornekleme * sure_ms / 1000)

    buf = array.array('h')
    ampl = 3000
    periyot = max(1, int(ornekleme / frekans))

    for i in range(ornek_sayisi):
        if (i % periyot) < (periyot // 2):
            buf.append(ampl)
        else:
            buf.append(-ampl)

    return pygame.mixer.Sound(buffer=buf)


def main():
    """Ana fonksiyon."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

    # Kanal sayisini 4 olarak ayarla
    pygame.mixer.set_num_channels(4)

    ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
    pygame.display.set_caption(BASLIK)
    saat = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    font_buyuk = pygame.font.SysFont("Arial", 20)

    # 4 farkli frekans icin sesler olustur
    sesler = [
        ("Do (262 Hz)", ses_olustur(262, 2000)),
        ("Mi (330 Hz)", ses_olustur(330, 2000)),
        ("Sol (392 Hz)", ses_olustur(392, 2000)),
        ("La (440 Hz)", ses_olustur(440, 2000)),
    ]

    # Kanallar
    kanallar = [pygame.mixer.Channel(i) for i in range(4)]

    # Kanal 0 icin endevent ayarla
    kanallar[0].set_endevent(SES_BITTI)

    durum_mesaji = "Bir tusa basin..."
    olay_sayaci = 0

    # Renk tablosu
    kanal_renkleri = [
        (100, 200, 100),  # Yesil
        (100, 100, 255),  # Mavi
        (255, 200, 50),   # Sari
        (255, 100, 100),  # Kirmizi
    ]

    calistir = True
    while calistir:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                calistir = False

            elif olay.type == SES_BITTI:
                olay_sayaci += 1
                durum_mesaji = f"[OLAY] Kanal 0 sesi bitti! (#{olay_sayaci})"

            elif olay.type == pygame.KEYDOWN:
                if olay.key == pygame.K_ESCAPE:
                    calistir = False

                # 1-4: Ilgili kanalda ses cal
                elif olay.key == pygame.K_1:
                    kanallar[0].play(sesler[0][1], loops=-1)
                    durum_mesaji = "Kanal 0: Do notasi (sonsuz)"

                elif olay.key == pygame.K_2:
                    kanallar[1].play(sesler[1][1], loops=-1)
                    durum_mesaji = "Kanal 1: Mi notasi (sonsuz)"

                elif olay.key == pygame.K_3:
                    kanallar[2].play(sesler[2][1], loops=-1)
                    durum_mesaji = "Kanal 2: Sol notasi (sonsuz)"

                elif olay.key == pygame.K_4:
                    kanallar[3].play(sesler[3][1], loops=-1)
                    durum_mesaji = "Kanal 3: La notasi (sonsuz)"

                # Q-R: Ilgili kanali durdur
                elif olay.key == pygame.K_q:
                    kanallar[0].stop()
                    durum_mesaji = "Kanal 0 durduruldu"

                elif olay.key == pygame.K_w:
                    kanallar[1].stop()
                    durum_mesaji = "Kanal 1 durduruldu"

                elif olay.key == pygame.K_e:
                    kanallar[2].stop()
                    durum_mesaji = "Kanal 2 durduruldu"

                elif olay.key == pygame.K_r:
                    kanallar[3].stop()
                    durum_mesaji = "Kanal 3 durduruldu"

                # P: Tum kanallari duraklat/devam ettir
                elif olay.key == pygame.K_p:
                    herhangi_aktif = any(k.get_busy() for k in kanallar)
                    if herhangi_aktif:
                        pygame.mixer.pause()
                        durum_mesaji = "Tum kanallar duraklatildi"
                    else:
                        pygame.mixer.unpause()
                        durum_mesaji = "Tum kanallar devam ediyor"

                # S: Tum kanallari durdur
                elif olay.key == pygame.K_s:
                    pygame.mixer.stop()
                    durum_mesaji = "Tum kanallar durduruldu"

        # Cizim
        ekran.fill((20, 20, 35))

        # Baslik
        baslik = font_buyuk.render("Kanal Yonetimi", True, (255, 200, 50))
        ekran.blit(baslik, (20, 10))

        # Kontroller
        kontrol_metinleri = [
            "1-4: Kanallarda ses cal | Q,W,E,R: Kanallari durdur",
            "P: Tumu duraklat/devam | S: Tumu durdur | ESC: Cikis",
        ]
        for i, metin in enumerate(kontrol_metinleri):
            render = font.render(metin, True, (160, 160, 160))
            ekran.blit(render, (20, 45 + i * 22))

        # Kanal durum gostergeleri
        y_baslangic = 110
        for i, kanal in enumerate(kanallar):
            aktif = kanal.get_busy()
            renk = kanal_renkleri[i] if aktif else (80, 80, 80)

            # Kanal kutusu
            pygame.draw.rect(ekran, renk, (20, y_baslangic + i * 65, 660, 50),
                             border_radius=5)
            pygame.draw.rect(ekran, (40, 40, 55), (22, y_baslangic + i * 65 + 2, 656, 46),
                             border_radius=4)

            # Kanal bilgisi
            durum_text = "AKTIF" if aktif else "BOS"
            bilgi = f"Kanal {i}: {sesler[i][0]} - [{durum_text}]"
            bilgi_render = font.render(bilgi, True, renk)
            ekran.blit(bilgi_render, (35, y_baslangic + i * 65 + 15))

            # Durum gostergesi (kucuk daire)
            daire_renk = (0, 255, 0) if aktif else (100, 0, 0)
            pygame.draw.circle(ekran, daire_renk,
                               (650, y_baslangic + i * 65 + 25), 8)

        # Olay sayaci
        olay_metin = font.render(f"set_endevent olaylari: {olay_sayaci}", True, (180, 180, 255))
        ekran.blit(olay_metin, (20, 385))

        # Durum mesaji
        durum_render = font.render(durum_mesaji, True, (200, 200, 100))
        ekran.blit(durum_render, (20, YUKSEKLIK - 30))

        pygame.display.flip()
        saat.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

"""
BEKLENEN CIKTI:
---------------
700x450 piksel bir pencere acilir.
4 kanal gorsel olarak gosterilir.
- 1-4 tuslariyla farkli kanallarda ses baslatilir
- Q,W,E,R tuslariyla kanallar durdurulur
- P ile tum kanallar duraklatilir/devam ettirilir
- S ile tum kanallar durdurulur
Kanal 0'daki ses bittiginde olay sayaci artar (set_endevent).
"""
