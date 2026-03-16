# Uzay Kacisi - Asamali Oyun Projesi

PyGame ile adim adim gelistirilen bir uzay savas oyunu.
Her versiyon bir oncekinin uzerine yeni ozellikler ekler.

## Asamalar

| Dosya | Bolum | Eklenen Ozellikler |
|-------|-------|--------------------|
| `v1_sprite_temelleri.py` | Bolum 5 - Gorseller ve Sprite Temelleri | Oyuncu gemisi, kayan yildiz arka plani, hayatta kalma skoru, `clamp_ip` sinir kontrolu |
| `v2_carpisma_mermi.py` | Bolum 6 - Carpisma Algilama ve Fizik | Dusman gemileri, mermi sistemi, `spritecollide`/`groupcollide`, can cubugu, puan, game over ekrani |
| `v3_ses_entegrasyon.py` | Bolum 7 - Ses ve Muzik | SoundManager sinifi, SFX (ates, patlama, hasar, bonus), arka plan muzigi, sessiz modu, bonus nesneleri |

## Kurulum ve Calistirma

```bash
# Bagimlilik yukle ve calistir
uv sync
uv run v1_sprite_temelleri.py
uv run v2_carpisma_mermi.py
uv run v3_ses_entegrasyon.py
```

Veya dogrudan:

```bash
pip install pygame-ce
python v1_sprite_temelleri.py
```

## Kontroller

| Tus | Islem |
|-----|-------|
| WASD / Ok Tuslari | Hareket (v1: dort yon, v2-v3: dort yon) |
| Space | Mermi ates (v2, v3) |
| M | Sessiz modu toggle (v3) |
| R | Tekrar oyna (v2, v3 - game over sonrasi) |
| ESC | Cikis |

## NOT

Gercek projede `assets/` dizinine ses ve gorsel dosyalari eklenir.
Dosyalar olmadan oyun geometrik sekiller ve programatik sesler ile calisir.
