# BILB3004 - Oyun Programlama Ders İçeriği

**PyGame ile Oyun Geliştirme** dersi için materyaller.

Karadeniz Teknik Üniversitesi | Fen Fakültesi, Bilgisayar Bilimleri | Bahar Dönemi

## Ders Bilgileri

| | |
|---|---|
| **Ders Kodu** | BILB3004 |
| **Süre** | 14 hafta |
| **Haftalık** | 2 saat teori + 2 saat uygulama |
| **Ön Koşul** | Yok |

## İçerik

| Klasör | Açıklama |
|--------|----------|
| [`pygame_kitap.pdf`](pygame_kitap.pdf) | Ders kitabı (634 sayfa) |
| [`slides/`](slides/) | Haftalık ders slaytları |
| [`labs/`](labs/) | Lab föyleri (uygulamalı çalışma kağıtları) |
| [`LabExamples/`](LabExamples/) | Lab başlangıç kodları (.py dosyaları) |
| [`kod_ornekleri/`](kod_ornekleri/) | Kitap kod örnekleri (bölüm bazlı) |
| [`quizzes/`](quizzes/) | Haftalık quizler |
| [`worksheets/`](worksheets/) | Bölüm çalışma kağıtları |

## Haftalık Plan

| Hafta | Konu | Slayt | Lab | Quiz | Çalışma Kağıdı |
|-------|------|-------|-----|------|-----------------|
| 1 | Python Temelleri | [Slayt](slides/Hafta01_Python_Temelleri.pdf) | [Lab](labs/Lab01_Python_Temelleri.pdf) | [Quiz](quizzes/Hafta01_Ogrenci.pdf) | [CK](worksheets/Bolum01_Calisma_Kagidi.pdf) |
| 2 | Kontrol Yapıları | [Slayt](slides/Hafta02_Kontrol_Yapilari.pdf) | [Lab](labs/Lab02_Kontrol_Yapilari.pdf) | [Quiz](quizzes/Hafta02_Ogrenci.pdf) | [CK](worksheets/Bolum02_Calisma_Kagidi.pdf) |
| 3 | PyGame Girişi | [Slayt](slides/Hafta03_PyGame_Giris.pdf) | [Lab](labs/Lab03_PyGame_Giris.pdf) | [Quiz](quizzes/Hafta03_Ogrenci.pdf) | [CK](worksheets/Bolum03_Calisma_Kagidi.pdf) |
| 4 | Kullanıcı Girdileri | [Slayt](slides/Hafta04_Kullanici_Girdileri.pdf) | [Lab](labs/Lab04_Kullanici_Girdileri.pdf) | [Quiz](quizzes/Hafta04_Ogrenci.pdf) | [CK](worksheets/Bolum04_Calisma_Kagidi.pdf) |
| 5 | Görseller ve Sprite | [Slayt](slides/Hafta05_Sprite_Temelleri.pdf) | [Lab](labs/Lab05_Gorseller_ve_Sprite.pdf) | [Quiz](quizzes/Hafta05_Ogrenci.pdf) | [CK](worksheets/Bolum05_Calisma_Kagidi.pdf) |
| 6 | Çarpışma Algılama | [Slayt](slides/Hafta06_Carpisma_Algilama.pdf) | [Lab](labs/Lab06_Carpisma_Algilama.pdf) | [Quiz](quizzes/Hafta06_Ogrenci.pdf) | [CK](worksheets/Bolum06_Calisma_Kagidi.pdf) |
| 7 | Ses ve Müzik | [Slayt](slides/Hafta07_Ses_ve_Muzik.pdf) | [Lab](labs/Lab07_Ses_ve_Muzik.pdf) | [Quiz](quizzes/Hafta07_Ogrenci.pdf) | [CK](worksheets/Bolum07_Calisma_Kagidi.pdf) |
| 8 | Animasyon ve Zamanlayıcılar | [Slayt](slides/Hafta08_Animasyon_Zamanlayicilar.pdf) | [Lab](labs/Lab08_Animasyon_Zamanlayicilar.pdf) | [Quiz](quizzes/Hafta08_Ogrenci.pdf) | [CK](worksheets/Bolum08_Calisma_Kagidi.pdf) |
| 9 | Metin, UI ve Menü Sistemleri | [Slayt](slides/Hafta09_Metin_UI_Menu.pdf) | [Lab](labs/Lab09_Metin_UI_Menu.pdf) | [Quiz](quizzes/Hafta09_Ogrenci.pdf) | [CK](worksheets/Bolum09_Calisma_Kagidi.pdf) |
| 10 | Tile-Based Oyun Dünyası | [Slayt](slides/Hafta10_Tile_Harita.pdf) | [Lab](labs/Lab10_Tile_Harita.pdf) | [Quiz](quizzes/Hafta10_Ogrenci.pdf) | [CK](worksheets/Bolum10_Calisma_Kagidi.pdf) |
| 11-14 | *İçerik hazırlanıyor* | | | | |

> Her haftanın cevap anahtarı için: `quizzes/Hafta##_CevapAnahtari.pdf`

## Kod Örnekleri

Kitaptaki kod örnekleri bölüm bazlı olarak [`kod_ornekleri/`](kod_ornekleri/) klasöründe bulunur:

```
kod_ornekleri/bolum##/
├── unite1/       # Ünite 1 kod örnekleri
├── unite2/       # Ünite 2 kod örnekleri
├── unite3/       # Ünite 3 kod örnekleri
├── unite4/       # Ünite 4 kod örnekleri
├── ornekler/     # Birleşik demo örnekleri
└── projeler/     # Proje dosyaları (Uzay Kaçışı, Zıplayan Macera, vb.)
```

## Lab Kodları

Lab başlangıç kodlarını [`LabExamples/`](LabExamples/) klasöründen indirin. Her dosyada `GOREV` işaretli bölgeler bulunur - lab föyündeki talimatlara göre bu görevleri tamamlayın.

```bash
# PyGame gerektiren lablar için (Lab03+)
uv init pygame_lab
cd pygame_lab
uv add pygame-ce
uv run python calisma1.py
```

Detaylar için [`LabExamples/README.txt`](LabExamples/README.txt) dosyasına bakın.

## Lisans

Bu materyaller akademik kullanım için hazırlanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
