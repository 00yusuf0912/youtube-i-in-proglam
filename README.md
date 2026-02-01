# ByteTube - YouTube Dönüştürücü v2.2.6

YouTube videolarını MP3/MP4 formatına dönüştüren gelişmiş indirme uygulaması. yt-dlp teknolojisi ile yüksek kaliteli indirme sağlar.

## ✨ Özellikler
- **YouTube Video/MP3 İndirme**: yt-dlp ile yüksek kaliteli indirme
- **Çoklu Format Desteği**: MP4 video ve MP3 ses formatları
- **Kalite Seçenekleri**: En İyi, 4K, 1440p, 1080p, 720p, 480p, 360p
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
   pip install --upgrade yt-dlp  # En son sürümü için
   ```

3. Uygulamayı çalıştırın:
   ```bash
   python byte_tube.py
   ```

## 🎮 Kullanım
1. Uygulamayı başlatın
2. YouTube URL'sini yapıştırın (otomatik olarak video bilgileri alınır)
3. Format seçin: MP3 (Ses) veya MP4 (Video)
4. MP4 için kalite seçin (En İyi, 4K, 1440p, 1080p, 720p, 480p, 360p)
5. "⬇️ İNDİR" butonuna tıklayın
6. İndirme klasörünü seçin
7. İndirme işlemini takip edin

**İpucu:** Uygulama içinde "🔄 yt-dlp Güncelle" butonuna tıklayarak yt-dlp'yi otomatik güncelleyebilirsiniz.

## 📝 Notlar
- YouTube'un kullanım şartlarına uygun şekilde kullanın
- FFmpeg MP3 dönüştürme için gereklidir
- Uygulama Windows ve Linux'ta çalışır

## 🔧 Sorun Giderme
- **HTTP 403 Forbidden hatası**: yt-dlp'yi güncelleyin: `pip install --upgrade yt-dlp`
- **ffmpeg bulunamadı hatası**: FFmpeg'i yükleyin ve PATH'e ekleyin
- **İndirme başlamıyor**: URL'nin doğru olduğundan emin olun
- **Video bilgileri gelmiyor**: İnternet bağlantınızı kontrol edin

## 📋 Sürüm Geçmişi

### v2.2.6 - Yüksek Çözünürlükler ve İndirme Kilidi (2026-02-01)
- 4K, 1440p, 1080p çözünürlük seçenekleri eklendi
- Aynı anda sadece bir indirme işlemi yapılabilir (çift indirme önlendi)
- Daha fazla hata ayıklama mesajı eklendi
- Kullanıcı deneyimi iyileştirildi

### v2.2.5 - İndirme Tamamlanma Gösterimi Düzeltmesi (2026-02-01)
- İndirme tamamlandığında "✅ İndirme Tamamlandı!" mesajı gösteriliyor
- İlerleme çubuğu %100'e ulaştığında doğru güncelleniyor
- Kullanıcı deneyimi iyileştirildi

### v2.2.4 - yt-dlp Otomatik Güncelleme Özelliği (2026-02-01)
- Uygulama içine yt-dlp güncelleme butonu eklendi
- Arka planda pip upgrade işlemi
- Kullanıcı dostu güncelleme arayüzü
- Güncelleme sonrası yeniden başlatma hatırlatması

### v2.2.3 - HTTP 403 ve FFmpeg Hata Düzeltmeleri (2026-02-01)
- yt-dlp seçeneklerine User-Agent header eklendi (403 Forbidden hatası için)
- README'ye yt-dlp güncelleme talimatı eklendi
- Sorun giderme bölümü eklendi
- FFmpeg yükleme hatırlatması iyileştirildi

### v2.2.2 - NoneType Karşılaştırma Hatası Düzeltmesi (2026-02-01)
- Video/audio format seçimi sırasında NoneType karşılaştırma hatası giderildi
- height ve abr değerlerinin None olması durumunda varsayılan değer kullanımı
- Format bilgisi alma işlemi stabil hale getirildi

### v2.2 - Hata Ayıklama Eklentileri (2026-02-01)
- Anahtar noktalara debug print ifadeleri eklendi
- İndirme işlemi sırasında URL, format ve kalite bilgilerini loglama
- Video bilgi alma işlemi için detaylı hata ayıklama
- Terminal çıktısında işlem takibi iyileştirildi

### v2.1 - Hata Düzeltmeleri (2026-01-XX)
- Runtime hataları düzeltildi (AttributeError, NameError)
- Eksik import'lar eklendi (time modülü)
- Kullanılmayan UI element referansları temizlendi
- Kod tekrarları giderildi ve performans iyileştirildi

### v2.0 - MP3/MP4 İndirme Desteği (2026-01-XX)
- MP3 ve MP4 format desteği eklendi
- Kalite seçenekleri: En İyi, 720p, 480p, 360p
- İndirme klasörü seçimi özelliği
- İlerleme çubuğu ve durum göstergeleri iyileştirildi

### v1.0 - İlk Sürüm (2026-01-XX)
- YouTube video indirme özelliği
- Temel UI tasarımı
- Video bilgi görüntüleme
- Loglama sistemi