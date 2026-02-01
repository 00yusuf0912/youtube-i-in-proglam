# ByteTube v16.0 - Video Dönüştürücü

Gelişmiş altyazı tanıma ve çeviri uygulaması. OCR teknolojisi ile ekran üzerindeki metinleri tespit edip istediğiniz dile çevirir.

## ✨ Yeni Özellikler
- **Sekmeli Arayüz**: Ana Sayfa, Ayarlar, Geçmiş sekmeleri
- **Gelişmiş Ayarlar**: Bekleme süresi ve OCR hassasiyeti ayarları
- **Geçmiş Yönetimi**: Dönüştürme geçmişini görüntüleme ve dışa aktarma
- **Otomatik Kaydetme**: Dönüştürmeleri otomatik olarak dosyaya kaydetme
- **Tema Değiştirici**: Koyu/açık tema seçimi
- **Klavye Kısayolları**: F5 (Başlat/Durdur), Ctrl+S (Kaydet), Esc (Çıkış)
- **İlerleme Göstergeleri**: Gerçek zamanlı durum takibi
- **Detaylı Loglama**: Sistem logları ve hata raporlama

## 🚀 Özellikler
- Gerçek zamanlı OCR ile altyazı tespiti
- Google Translate entegrasyonu
- Cümle bitiş algılama
- Sürüklebilir overlay penceresi
- Çoklu dil desteği (Türkçe, İngilizce, Almanca, Fransızca, İspanyolca)
- Optimizasyon ayarları

## 🎮 Kullanım
1. **Dil Seçimi**: Hedef dili combo box'tan seçin
2. **Bölge Seçimi**: "ALTYAZI ALANINI BELİRLE" butonuna tıklayın ve altyazı bölgesini seçin
3. **Başlatma**: "AKILLI DÖNÜŞTÜRÜCÜYÜ BAŞLAT" butonuna tıklayın veya F5'e basın
4. **İzleme**: Overlay penceresinde çeviriler görünecektir
5. **Ayarlar**: Ayarlar sekmesinden parametreleri özelleştirin
6. **Geçmiş**: Geçmiş sekmesinden önceki dönüştürmeleri görüntüleyin

## ⚙️ Ayarlar
- **Bekleme Süresi**: Cümle bitişini algılamak için bekleme süresi (0.5-3.0 sn)
- **OCR Hassasiyeti**: Metin tanıma duyarlılığı (1.0-5.0)
- **Otomatik Kaydetme**: Dönüştürmeleri otomatik olarak dosyaya kaydetme
- **Tema**: Koyu/açık tema seçimi

## ⌨️ Klavye Kısayolları
- **F5**: Dönüştürücüyü başlat/durdur
- **Ctrl+S**: Geçerli dönüştürmeleri kaydet
- **Ctrl+R**: Geçmişi temizle
- **Esc**: Uygulamadan çık

## Gereksinimler
- Python 3.8+
- Tesseract OCR
- Gerekli Python paketleri: customtkinter, pyautogui, pillow, pytesseract, deep-translator

## Kurulum
1. Tesseract OCR'yi yükleyin:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr`

2. Python paketlerini yükleyin:
   ```bash
   pip install customtkinter pyautogui pillow pytesseract deep-translator
   ```

3. Uygulamayı çalıştırın:
   ```bash
   python byte_tube.py
   ```

## Kullanım
1. Hedef dili seçin (varsayılan Türkçe)
2. "ALTYAZI ALANINI BELİRLE" butonuna tıklayın
3. Altyazı bölgesini fare ile seçin
4. "AKILLI ÇEVİRİYİ BAŞLAT" butonuna tıklayın
5. Overlay penceresinde dönüştürmeler görünecektir

## Hata Ayıklama
- Terminal alanında debug mesajları görünür
- OCR sonuçları ve dönüştürme hataları loglanır

## Notlar
- Uygulama Windows için optimize edilmiştir, Linux'ta GUI kısıtlamaları olabilir
- İnternet bağlantısı dönüştürme için gereklidir