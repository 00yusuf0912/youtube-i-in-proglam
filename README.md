# ByteTube - YouTube Dönüştürücü

YouTube videolarını MP3/MP4 formatına dönüştüren gelişmiş indirme uygulaması. yt-dlp teknolojisi ile yüksek kaliteli indirme sağlar.

## ✨ Özellikler
- **YouTube Video/MP3 İndirme**: yt-dlp ile yüksek kaliteli indirme
- **Çoklu Format Desteği**: MP4 video ve MP3 ses formatları
- **Kalite Seçenekleri**: En İyi, 720p, 480p, 360p
- **Video Bilgi Görüntüleme**: Başlık, süre, izlenme, beğeni bilgileri
- **İlerleme Takibi**: Gerçek zamanlı indirme ilerlemesi
- **Kolay Kullanım**: Modern ve kullanıcı dostu arayüz

## 🚀 Özellikler
- **Otomatik Video Bilgi Alma**: URL yapıştırılınca otomatik olarak video bilgileri alınır
- **Çoklu Format Desteği**: MP3 (Ses) ve MP4 (Video) formatları
- **Kalite Seçenekleri**: MP4 için En İyi, 720p, 480p, 360p seçenekleri
- **Kolay Kullanım**: Tek butonla indirme
- **İlerleme Takibi**: Gerçek zamanlı indirme ilerlemesi ve hata ayıklama
- **Detaylı Loglama**: Tüm işlemler loglanır ve takip edilebilir

## 🎮 Kullanım
1. Uygulamayı başlatın
2. YouTube URL'sini yapıştırın (otomatik olarak video bilgileri alınır)
3. Format seçin: MP3 (Ses) veya MP4 (Video)
4. MP4 için kalite seçin (En İyi, 720p, 480p, 360p)
5. "⬇️ İNDİR" butonuna tıklayın
6. İndirme klasörünü seçin
7. İndirme işlemini takip edin

## 📋 Gereksinimler
- Python 3.8+
- FFmpeg (MP3 dönüştürme için)
- Gerekli Python paketleri: customtkinter, yt-dlp

## 🔧 Kurulum
1. FFmpeg'i yükleyin (MP3 dönüştürme için):
   - Windows: https://ffmpeg.org/download.html
   - Linux: `sudo apt install ffmpeg`

2. Python paketlerini yükleyin:
   ```bash
   pip install customtkinter yt-dlp
   ```

3. Uygulamayı çalıştırın:
   ```bash
   python byte_tube.py
   ```

## 📝 Notlar
- YouTube'un kullanım şartlarına uygun şekilde kullanın
- FFmpeg MP3 dönüştürme için gereklidir
- Uygulama Windows ve Linux'ta çalışır