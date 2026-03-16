Uzay Kacisi - Assets Dizini
============================

Bu dizine oyun icin gereken ses ve gorsel dosyalari eklenir.
Dosyalar olmadan oyun geometrik sekiller ve programatik sesler
ile calisir (fallback modu).

Beklenen dizin yapisi:

  assets/
  ├── images/
  │   ├── gemi.png          # Oyuncu gemisi gorseli
  │   └── dusman.png        # Dusman gemisi gorseli
  └── sounds/
      ├── sfx/
      │   ├── ates.ogg      # Mermi atesleme sesi
      │   ├── patlama.ogg   # Dusman patlama sesi
      │   ├── hasar.ogg     # Oyuncuya hasar sesi
      │   └── bonus.ogg     # Bonus toplama sesi
      └── muzik/
          └── uzay_temasi.ogg  # Arka plan muzigi

Onerilen format:
  - Gorseller: PNG (seffaf arka plan)
  - Sesler: OGG Vorbis (kucuk dosya boyutu, iyi kalite)
  - Muzik: OGG Vorbis (dongu icin uygun)
