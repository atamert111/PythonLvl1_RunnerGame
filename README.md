# Runner Game  - PGZero ile Hazırlanmış 2D Oyun

Bu proje, Python programlama dili ve PGZero kütüphanesi kullanılarak hazırlanmış bir runner oyunudur. Oyuncu zombilerden SPACE tuşuna basarak zıplar ve hayatta kalmaya çalışır.

##  Oyun Özellikleri
- **Zıplama ve fizik sistemi**
- **Ses efektleri ve arka plan müziği**
- **Zorluk seviyesi seçimi (1-5)**
- **OOP (Nesne Tabanlı Programlama) yapısı**
- **Başlangıç menüsü, ses aç/kapat ve çıkış butonu**
- **Game Over ekranı**

##  Zorluk Seviyeleri
| Seviye | Zombi Sıklığı | Zıplama Gücü |
|--------|----------------|----------------|
| 1      | Düşük          | Yüksek (-20)   |
| 2      | Orta           | -17            |
| 3      | Normal         | -14            |
| 4      | Zor            | -12            |
| 5      | Çok Zor        | Düşük (-10)    |

> Menüden 1-5 arası butonlara tıklayarak zorluk seviyesi seçilebilir.

##  Klasör Yapısı

runner-game/ │ 
    ├── game.py 
    ├── README.md 
    ├── requirements.txt │ 
    ├── images/ │ 
        └── hero/ # Oyuncu sprite'ları │ 
        └── zombi/ # Zombi sprite'ları │ 
    ├── sounds/ # Efekt sesleri (jump, gameover, funny_crash) 
    └── music/ # background.wav (arka plan müziği)

##  Kurulum ve Çalıştırma

```bash
pip install -r requirements.txt
pgzrun game.py

##  Hazırlayan
Ad Soyad: Ata Mert Erdihan
Tarih: 25.04.2025