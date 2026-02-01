import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading, time, os, json, logging
import yt_dlp
import queue

# --- LOGGING AYARLARI ---
logging.basicConfig(filename='byte_tube.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ByteTubeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ByteTube - YouTube Dönüştürücü")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Ana frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Başlık
        self.baslik = ctk.CTkLabel(self.main_frame, text="🎵 ByteTube YouTube Dönüştürücü",
                                  font=("Roboto", 24, "bold"))
        self.baslik.pack(pady=(20, 10))

        # Tabview oluştur
        self.tabview = ctk.CTkTabview(self.main_frame, width=900, height=600)
        self.tabview.pack(pady=10)

        # Sadece YouTube İndirme sekmesi
        self.tabview.add("YouTube İndirme")
        self.youtube_sayfasi_olustur()

        # Durum çubuğu
        self.status_label = ctk.CTkLabel(self.main_frame, text="Hazır",
                                        font=("Roboto", 12))
        self.status_label.pack(pady=(10, 0))

        # İlerleme çubuğu
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=400)
        self.progress_bar.pack(pady=(5, 20))
        self.progress_bar.set(0)

        # Kuyruk ve thread yönetimi
        self.queue = queue.Queue()
        self.check_queue()

        # Ayarlar dosyasını yükle
        self.ayarlar_yukle()

    def ayarlar_yukle(self):
        try:
            with open('ayarlar.json', 'r', encoding='utf-8') as f:
                self.ayarlar = json.load(f)
        except FileNotFoundError:
            self.ayarlar = {
                'indirme_klasoru': os.path.join(os.path.expanduser('~'), 'Downloads'),
                'varsayilan_format': 'mp4',
                'varsayilan_kalite': 'best'
            }
            self.ayarlar_kaydet()

    def ayarlar_kaydet(self):
        with open('ayarlar.json', 'w', encoding='utf-8') as f:
            json.dump(self.ayarlar, f, ensure_ascii=False, indent=4)

    def check_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg['type'] == 'status':
                    self.status_label.configure(text=msg['text'])
                elif msg['type'] == 'progress':
                    self.progress_bar.set(msg['value'])
                elif msg['type'] == 'error':
                    messagebox.showerror("Hata", msg['text'])
                elif msg['type'] == 'info':
                    messagebox.showinfo("Bilgi", msg['text'])
        except queue.Empty:
            pass
        self.after(100, self.check_queue)

    def youtube_sayfasi_olustur(self):
        tab = self.tabview.tab("YouTube İndirme")
        
        # URL girişi
        url_frame = ctk.CTkFrame(tab, fg_color="transparent")
        url_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(url_frame, text="YouTube URL:", font=("Roboto", 16, "bold")).pack(side="left")
        self.url_entry = ctk.CTkEntry(url_frame, placeholder_text="https://www.youtube.com/watch?v=...", width=500, height=40)
        self.url_entry.pack(side="right", padx=(10, 0), fill="x", expand=True)
        self.url_entry.bind("<KeyRelease>", self.url_degisti)
        
        # Format seçimi
        format_frame = ctk.CTkFrame(tab, fg_color="transparent")
        format_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(format_frame, text="Format:", font=("Roboto", 14, "bold")).pack(side="left")
        self.format_var = ctk.StringVar(value="mp3")
        mp3_radio = ctk.CTkRadioButton(format_frame, text="🎵 MP3 (Ses)", variable=self.format_var, value="mp3", font=("Roboto", 12))
        mp3_radio.pack(side="left", padx=(20, 10))
        mp4_radio = ctk.CTkRadioButton(format_frame, text="🎬 MP4 (Video)", variable=self.format_var, value="mp4", font=("Roboto", 12))
        mp4_radio.pack(side="left", padx=(10, 20))
        
        # Kalite seçimi (MP4 için)
        quality_frame = ctk.CTkFrame(tab, fg_color="transparent")
        quality_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(quality_frame, text="Kalite:", font=("Roboto", 14, "bold")).pack(side="left")
        self.quality_var = ctk.StringVar(value="best")
        quality_combo = ctk.CTkComboBox(quality_frame, values=["En İyi", "720p", "480p", "360p"], 
                                        variable=self.quality_var, width=150, height=35)
        quality_combo.pack(side="right")
        
        # İndirme butonu
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.download_btn = ctk.CTkButton(btn_frame, text="⬇️ İNDİR", height=50, 
                                          fg_color="#ff6b35", font=("Roboto", 16, "bold"),
                                          command=self.indir)
        self.download_btn.pack(expand=True)
        
        # İlerleme göstergesi
        progress_frame = ctk.CTkFrame(tab, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=5)
        
        self.yt_progress_label = ctk.CTkLabel(progress_frame, text="URL'yi yapıştırın ve MP3'ü indirin", font=("Roboto", 12))
        self.yt_progress_label.pack(side="left")
        
        self.yt_progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
        self.yt_progress_bar.pack(side="right")
        self.yt_progress_bar.set(0)
        
        # Video bilgileri
        info_frame = ctk.CTkFrame(tab)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(info_frame, text="📹 Video Bilgileri", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        
        self.video_info_text = ctk.CTkTextbox(info_frame, fg_color="#08080a", text_color="#00ff88", 
                                             font=("Consolas", 11), height=200)
        self.video_info_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.video_info_text.insert("0.0", "YouTube URL'sini yapıştırın...\n\n")
        self.video_info_text.configure(state="disabled")

    def log_ekle(self, mesaj, seviye="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {mesaj}"
        
        # Terminal'e yaz (eğer varsa)
        try:
            print(log_msg)
        except:
            pass
        
        # Dosyaya log
        if seviye == "ERROR":
            logging.error(mesaj)
        else:
            logging.info(mesaj)

    def url_degisti(self, event=None):
        url = self.url_entry.get().strip()
        if url and ("youtube.com" in url or "youtu.be" in url):
            # Kısa bir gecikme ile otomatik bilgi al
            if hasattr(self, '_url_timer'):
                self.after_cancel(self._url_timer)
            self._url_timer = self.after(1000, self.youtube_bilgi_al_otomatik)

    def youtube_bilgi_al_otomatik(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        
        self.video_info_text.configure(state="normal")
        self.video_info_text.delete("0.0", "end")
        self.video_info_text.insert("0.0", "Video bilgileri alınıyor...\n\n")
        self.video_info_text.configure(state="disabled")
        
        threading.Thread(target=self._youtube_bilgi_al_thread, args=(url,), daemon=True).start()

    def _youtube_bilgi_al_thread(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Bilgileri göster
                info_text = f"📹 Başlık: {info.get('title', 'Bilinmiyor')}\n"
                info_text += f"👤 Yükleyen: {info.get('uploader', 'Bilinmiyor')}\n"
                info_text += f"⏱️ Süre: {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}\n"
                info_text += f"👁️ İzlenme: {info.get('view_count', 0):,}\n"
                info_text += f"👍 Beğeni: {info.get('like_count', 0):,}\n"
                info_text += f"📅 Yüklenme: {info.get('upload_date', 'Bilinmiyor')}\n\n"
                
                # Format bilgileri
                info_text += "🎵 Kullanılabilir Formatlar:\n"
                formats = info.get('formats', [])
                video_formats = [f for f in formats if f.get('vcodec') != 'none']
                audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                
                if video_formats:
                    info_text += f"🎬 Video: {len(video_formats)} format\n"
                    best_video = max(video_formats, key=lambda x: x.get('height', 0))
                    info_text += f"  └ En iyi: {best_video.get('height', 'Bilinmiyor')}p\n"
                
                if audio_formats:
                    info_text += f"🎵 Ses: {len(audio_formats)} format\n"
                    best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
                    info_text += f"  └ En iyi: {best_audio.get('abr', 'Bilinmiyor')}kbps\n"
                
                self.video_info_text.configure(state="normal")
                self.video_info_text.delete("0.0", "end")
                self.video_info_text.insert("0.0", info_text)
                self.video_info_text.configure(state="disabled")
                
        except Exception as e:
            error_msg = f"❌ Hata: {str(e)}\n\nURL'nin doğru olduğundan emin olun."
            self.video_info_text.configure(state="normal")
            self.video_info_text.delete("0.0", "end")
            self.video_info_text.insert("0.0", error_msg)
            self.video_info_text.configure(state="disabled")
            logging.error(f"YouTube bilgi alma hatası: {e}")

    def indir(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Uyarı", "Lütfen YouTube URL'sini girin!")
            self.log_ekle("HATA: URL girilmedi", "ERROR")
            return
        
        if not ("youtube.com" in url or "youtu.be" in url):
            messagebox.showwarning("Uyarı", "Geçerli bir YouTube URL'si girin!")
            self.log_ekle("HATA: Geçersiz YouTube URL'si", "ERROR")
            return
        
        # İndirme klasörü seçimi
        download_dir = filedialog.askdirectory(title="İndirme Klasörünü Seçin")
        if not download_dir:
            self.log_ekle("İptal: Klasör seçilmedi")
            return
        
        format_type = self.format_var.get()
        quality = self.quality_var.get()
        
        self.download_btn.configure(state="disabled", text="⏳ İNDİRİLİYOR...")
        self.yt_progress_bar.set(0)
        self.yt_progress_label.configure(text=f"{format_type.upper()} indirme hazırlanıyor...")
        self.log_ekle(f"İndirme başlatıldı: {format_type.upper()} - {url}")
        
        threading.Thread(target=self._indir_thread, 
                        args=(url, download_dir, format_type, quality), daemon=True).start()

    def _indir_thread(self, url, download_dir, format_type, quality):
        try:
            # Kalite ayarları
            quality_map = {
                "En İyi": "best",
                "720p": "best[height<=720]",
                "480p": "best[height<=480]", 
                "360p": "best[height<=360]"
            }
            
            if format_type == "mp4":
                ydl_opts = {
                    'format': f"{quality_map.get(quality, 'best')}[ext=mp4]/best[ext=mp4]",
                    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [self._youtube_progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                }
                format_name = "MP4 Video"
            else:  # mp3
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'progress_hooks': [self._youtube_progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                }
                format_name = "MP3 Ses"
            
            self.log_ekle(f"yt-dlp seçenekleri hazır: {format_name}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.log_ekle("yt-dlp indirici başlatıldı")
                ydl.download([url])
            
            self.yt_progress_label.configure(text=f"✅ {format_name} başarıyla indirildi!")
            self.yt_progress_bar.set(1.0)
            messagebox.showinfo("Başarılı", f"{format_name} başarıyla indirildi!\nKlasör: {download_dir}")
            self.log_ekle(f"İndirme başarılı: {format_name} - {url}")
            
        except Exception as e:
            error_msg = f"❌ {format_type.upper()} indirme hatası!"
            self.yt_progress_label.configure(text=error_msg)
            messagebox.showerror("Hata", f"İndirme sırasında hata oluştu:\n{str(e)}")
            self.log_ekle(f"İndirme hatası: {e}", "ERROR")
        
        finally:
            self.download_btn.configure(state="normal", text="⬇️ İNDİR")

    def _youtube_progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = float(d.get('_percent_str', '0%').replace('%', ''))
                self.yt_progress_bar.set(percent / 100)
                speed = d.get('_speed_str', 'Bilinmiyor')
                eta = d.get('_eta_str', 'Bilinmiyor')
                self.yt_progress_label.configure(text=f"İndiriliyor... %{percent:.1f} - Hız: {speed} - Kalan: {eta}")
            except:
                self.yt_progress_label.configure(text="İndiriliyor...")
        elif d['status'] == 'finished':
            self.yt_progress_label.configure(text="Dönüştürülüyor...")

    def youtube_temizle(self):
        self.url_entry.delete(0, "end")
        self.video_info_text.configure(state="normal")
        self.video_info_text.delete("0.0", "end")
        self.video_info_text.insert("0.0", "YouTube URL'sini yapıştırın...\n\n")
        self.video_info_text.configure(state="disabled")
        self.yt_progress_bar.set(0)
        self.yt_progress_label.configure(text="URL'yi yapıştırın ve MP3'ü indirin")

    def on_closing(self):
        self.ayarlar_kaydet()
        self.destroy()

if __name__ == "__main__":
    app = ByteTubeApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()