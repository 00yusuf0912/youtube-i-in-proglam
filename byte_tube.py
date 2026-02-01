import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading, time, os, pyautogui, json, logging
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pytesseract
from deep_translator import GoogleTranslator
import queue

# --- LOGGING AYARLARI ---
logging.basicConfig(filename='byte_tube.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- TESSERACT KONFIGURASYONU ---
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

class SubtitleOverlay(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.attributes("-topmost", True, "-alpha", 0.9)
        self.config(bg='#000000')
        self.geometry("900x130+400+820")

        # Gamer Teması (Neon Mavi)
        self.border = tk.Frame(self, bg='#00d2ff', padx=2, pady=2)
        self.border.pack(expand=True, fill="both")
        
        self.inner = tk.Frame(self.border, bg='#050505')
        self.inner.pack(expand=True, fill="both")

        self.label = tk.Label(self.inner, text="ByteTube AI: Konuşma Bekleniyor...", 
                               font=("Segoe UI", 20, "bold"), fg="white", 
                               bg="#050505", wraplength=850, justify="center")
        self.label.pack(expand=True, fill="both", padx=15)
        
        self.bind("<Button-1>", self.basla)
        self.bind("<B1-Motion>", self.surukle)

    def basla(self, e): self.x, self.y = e.x, e.y
    def surukle(self, e): self.geometry(f"+{self.winfo_x()+(e.x-self.x)}+{self.winfo_y()+(e.y-self.y)}")
    def guncelle(self, metin): self.label.config(text=metin)

class ByteTubeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ByteTube v16.0 - Video Dönüştürücü")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        
        # Ana değişkenler
        self.calisiyor = False
        self.secili_alan = None
        self.target_lang = 'tr'
        self.translator = GoogleTranslator(source='en', target=self.target_lang)
        
        # Yeni özellikler için değişkenler
        self.bekleme_suresi = 1.0
        self.ocr_hassasiyet = 2.5
        self.gecmis = []
        self.kaydet_dosyasi = "donusturulen_metinler.txt"
        self.log_queue = queue.Queue()
        
        # Ayarlar
        self.ayarlar = {
            'bekleme_suresi': 1.0,
            'ocr_hassasiyet': 2.5,
            'tema': 'dark',
            'kaydet_otomatik': False
        }
        self.ayarlar_yukle()
        
        self.arayuz()

    def ayarlar_yukle(self):
        try:
            if os.path.exists('ayarlar.json'):
                with open('ayarlar.json', 'r') as f:
                    self.ayarlar.update(json.load(f))
                self.bekleme_suresi = self.ayarlar['bekleme_suresi']
                self.ocr_hassasiyet = self.ayarlar['ocr_hassasiyet']
                ctk.set_appearance_mode(self.ayarlar['tema'])
        except Exception as e:
            logging.error(f"Ayarlar yüklenirken hata: {e}")

    def ayarlar_kaydet(self):
        try:
            with open('ayarlar.json', 'w') as f:
                json.dump(self.ayarlar, f, indent=4)
        except Exception as e:
            logging.error(f"Ayarlar kaydedilirken hata: {e}")

    def gecmis_yukle(self):
        try:
            if os.path.exists('gecmis.json'):
                with open('gecmis.json', 'r') as f:
                    self.gecmis = json.load(f)
        except Exception as e:
            logging.error(f"Geçmiş yüklenirken hata: {e}")

    def gecmis_kaydet(self):
        try:
            with open('gecmis.json', 'w') as f:
                json.dump(self.gecmis[-50:], f, indent=4)  # Son 50 kayıt
        except Exception as e:
            logging.error(f"Geçmiş kaydedilirken hata: {e}")

    def arayuz(self):
        self.configure(fg_color="#050505")
        
        # Ana container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Üst panel
        self.ust_panel = ctk.CTkFrame(self.main_container, height=80, fg_color="#0a0a0a")
        self.ust_panel.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.ust_panel, text="ByteTube", font=("Orbitron", 32, "bold"), text_color="#00d2ff").pack(side="left", padx=30, pady=20)
        
        # Tema değiştirici
        self.tema_btn = ctk.CTkButton(self.ust_panel, text="🌙", width=50, height=40, command=self.tema_degistir)
        self.tema_btn.pack(side="right", padx=20, pady=20)
        
        # Sekme sistemi
        self.tabview = ctk.CTkTabview(self.main_container, fg_color="#0a0a0a", segmented_button_fg_color="#00d2ff", 
                                      segmented_button_selected_color="#00d2ff", segmented_button_unselected_color="#1a1a1a")
        self.tabview.pack(fill="both", expand=True)
        
        # Sekmeler
        self.tabview.add("Ana Sayfa")
        self.tabview.add("Ayarlar")
        self.tabview.add("Geçmiş")
        
        self.ana_sayfa_olustur()
        self.ayarlar_sayfasi_olustur()
        self.gecmis_sayfasi_olustur()
        
        self.gecmis_sayfasi_olustur()
        
        # Klavye kısayolları
        self.bind('<Control-s>', lambda e: self.donusturme_kaydet())
        self.bind('<Control-r>', lambda e: self.gecmis_temizle())
        self.bind('<F5>', lambda e: self.motor_tetikle())
        self.bind('<Escape>', lambda e: self.on_closing())

    def ana_sayfa_olustur(self):
        tab = self.tabview.tab("Ana Sayfa")
        
        # Dil Seçimi
        dil_frame = ctk.CTkFrame(tab, fg_color="transparent")
        dil_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(dil_frame, text="Hedef Dil:", font=("Roboto", 16)).pack(side="left")
        self.dil_secici = ctk.CTkComboBox(dil_frame, width=200, height=40, 
                                           values=["Türkçe (tr)", "İngilizce (en)", "Almanca (de)", "Fransızca (fr)", "İspanyolca (es)"],
                                           command=self.dil_degistir)
        self.dil_secici.set("Türkçe (tr)")
        self.dil_secici.pack(side="right")
        
        # Kontrol butonları
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.btn_bolge = ctk.CTkButton(btn_frame, text="📍 ALTYAZI ALANINI BELİRLE", height=50, 
                                        fg_color="#1a1a2e", border_width=1, border_color="#00d2ff", 
                                        command=self.alan_sec)
        self.btn_bolge.pack(side="left", padx=(0, 10), expand=True)

        self.btn_baslat = ctk.CTkButton(btn_frame, text="▶️ AKILLI DÖNÜŞTÜRÜCÜYÜ BAŞLAT", height=50, 
                                         fg_color="#00d2ff", text_color="#000", font=("Roboto", 16, "bold"),
                                         command=self.motor_tetikle)
        self.btn_baslat.pack(side="right", padx=(10, 0), expand=True)
        
        # İlerleme çubuğu
        progress_frame = ctk.CTkFrame(tab, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=5)
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="Durum: Hazır", font=("Roboto", 12))
        self.progress_label.pack(side="left")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=300)
        self.progress_bar.pack(side="right")
        self.progress_bar.set(0)
        
        # Terminal
        terminal_frame = ctk.CTkFrame(tab)
        terminal_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(terminal_frame, text="📋 Sistem Logları", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        
        self.terminal = ctk.CTkTextbox(terminal_frame, fg_color="#08080a", text_color="#00ff88", font=("Consolas", 12))
        self.terminal.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.terminal.insert("0.0", ">>> ByteTube Video Dönüştürücü Aktif\n>>> Klavye kısayolları: F5=Başlat, Ctrl+S=Kaydet, Esc=Çıkış\n>>> Hazır durumda...")

    def ayarlar_sayfasi_olustur(self):
        tab = self.tabview.tab("Ayarlar")
        
        # Bekleme süresi ayarı
        sure_frame = ctk.CTkFrame(tab, fg_color="transparent")
        sure_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(sure_frame, text="⏱️ Cümle Bekleme Süresi (sn):", font=("Roboto", 14)).pack(side="left")
        self.sure_slider = ctk.CTkSlider(sure_frame, from_=0.5, to=3.0, number_of_steps=25, command=self.sure_degistir)
        self.sure_slider.set(self.bekleme_suresi)
        self.sure_slider.pack(side="right", padx=(10, 0), fill="x", expand=True)
        self.sure_label = ctk.CTkLabel(sure_frame, text=f"{self.bekleme_suresi:.1f} sn")
        self.sure_label.pack(side="right")
        
        # OCR hassasiyeti
        ocr_frame = ctk.CTkFrame(tab, fg_color="transparent")
        ocr_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(ocr_frame, text="🔍 OCR Hassasiyeti:", font=("Roboto", 14)).pack(side="left")
        self.ocr_slider = ctk.CTkSlider(ocr_frame, from_=1.0, to=5.0, number_of_steps=40, command=self.ocr_degistir)
        self.ocr_slider.set(self.ocr_hassasiyet)
        self.ocr_slider.pack(side="right", padx=(10, 0), fill="x", expand=True)
        self.ocr_label = ctk.CTkLabel(ocr_frame, text=f"{self.ocr_hassasiyet:.1f}")
        self.ocr_label.pack(side="right")
        
        # Otomatik kaydetme
        auto_frame = ctk.CTkFrame(tab, fg_color="transparent")
        auto_frame.pack(fill="x", padx=20, pady=10)
        
        self.auto_save_var = ctk.BooleanVar(value=self.ayarlar.get('kaydet_otomatik', False))
        self.auto_save_check = ctk.CTkCheckBox(auto_frame, text="💾 Dönüştürmeleri otomatik kaydet", 
                                               variable=self.auto_save_var, command=self.auto_save_degistir)
        self.auto_save_check.pack(side="left")
        
        # Kaydetme butonları
        save_frame = ctk.CTkFrame(tab, fg_color="transparent")
        save_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(save_frame, text="💾 Ayarları Kaydet", command=self.ayarlar_kaydet).pack(side="left", padx=(0, 10))
        ctk.CTkButton(save_frame, text="🔄 Varsayılana Dön", command=self.varsayilan_ayarlar).pack(side="right", padx=(10, 0))

    def gecmis_sayfasi_olustur(self):
        tab = self.tabview.tab("Geçmiş")
        
        # Geçmiş listesi
        self.gecmis_textbox = ctk.CTkTextbox(tab, fg_color="#08080a", text_color="#00ff88", font=("Consolas", 12))
        self.gecmis_textbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Kontrol butonları
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(btn_frame, text="🔄 Yenile", command=self.gecmis_goster).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_frame, text="🗑️ Temizle", command=self.gecmis_temizle).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_frame, text="💾 Dışa Aktar", command=self.gecmis_disa_aktar).pack(side="right", padx=(10, 0))
        
        self.gecmis_goster()

    def tema_degistir(self):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.tema_btn.configure(text="☀️")
            self.ayarlar['tema'] = 'light'
        else:
            ctk.set_appearance_mode("Dark")
            self.tema_btn.configure(text="🌙")
            self.ayarlar['tema'] = 'dark'
        self.ayarlar_kaydet()

    def sure_degistir(self, value):
        self.bekleme_suresi = float(value)
        self.sure_label.configure(text=f"{self.bekleme_suresi:.1f} sn")
        self.ayarlar['bekleme_suresi'] = self.bekleme_suresi
        self.ayarlar_kaydet()

    def ocr_degistir(self, value):
        self.ocr_hassasiyet = float(value)
        self.ocr_label.configure(text=f"{self.ocr_hassasiyet:.1f}")
        self.ayarlar['ocr_hassasiyet'] = self.ocr_hassasiyet
        self.ayarlar_kaydet()

    def auto_save_degistir(self):
        self.ayarlar['kaydet_otomatik'] = self.auto_save_var.get()
        self.ayarlar_kaydet()

    def varsayilan_ayarlar(self):
        self.ayarlar = {
            'bekleme_suresi': 1.0,
            'ocr_hassasiyet': 2.5,
            'tema': 'dark',
            'kaydet_otomatik': False
        }
        self.sure_slider.set(1.0)
        self.ocr_slider.set(2.5)
        self.auto_save_var.set(False)
        ctk.set_appearance_mode("Dark")
        self.tema_btn.configure(text="🌙")
        self.ayarlar_kaydet()
        messagebox.showinfo("Bilgi", "Ayarlar varsayılana döndürüldü!")

    def donusturme_kaydet(self):
        try:
            with open(self.kaydet_dosyasi, 'a', encoding='utf-8') as f:
                f.write(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                for item in self.gecmis[-10:]:  # Son 10 kayıt
                    f.write(f"{item}\n")
            messagebox.showinfo("Başarılı", f"Dönüştürmeler {self.kaydet_dosyasi} dosyasına kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {e}")

    def gecmis_goster(self):
        self.gecmis_textbox.delete("0.0", "end")
        if not self.gecmis:
            self.gecmis_textbox.insert("0.0", "📝 Henüz dönüştürme geçmişi yok.")
        else:
            for i, item in enumerate(reversed(self.gecmis[-20:]), 1):  # Son 20 kayıt
                self.gecmis_textbox.insert("end", f"{i}. {item}\n")

    def gecmis_temizle(self):
        if messagebox.askyesno("Onay", "Geçmişi temizlemek istediğinizden emin misiniz?"):
            self.gecmis.clear()
            self.gecmis_kaydet()
            self.gecmis_goster()
            messagebox.showinfo("Başarılı", "Geçmiş temizlendi!")

    def gecmis_disa_aktar(self):
        try:
            dosya = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if dosya:
                with open(dosya, 'w', encoding='utf-8') as f:
                    f.write("ByteTube Dönüştürme Geçmişi\n")
                    f.write("=" * 50 + "\n\n")
                    for item in self.gecmis:
                        f.write(f"{item}\n\n")
                messagebox.showinfo("Başarılı", f"Geçmiş {dosya} dosyasına aktarıldı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dışa aktarma hatası: {e}")

    def on_closing(self):
        if self.calisiyor:
            if messagebox.askyesno("Çıkış", "Program çalışıyor. Çıkmak istediğinizden emin misiniz?"):
                self.calisiyor = False
                if hasattr(self, 'ekran'):
                    self.ekran.destroy()
                self.ayarlar_kaydet()
                self.destroy()
        else:
            self.ayarlar_kaydet()
            self.destroy()

    def log_ekle(self, mesaj, seviye="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {mesaj}"
        self.terminal.insert("end", f"\n{log_msg}")
        self.terminal.see("end")
        
        # Dosyaya log
        if seviye == "ERROR":
            logging.error(mesaj)
        else:
            logging.info(mesaj)

    def dil_degistir(self, secim):
        lang_map = {"Türkçe (tr)": "tr", "İngilizce (en)": "en", "Almanca (de)": "de", "Fransızca (fr)": "fr", "İspanyolca (es)": "es"}
        self.target_lang = lang_map.get(secim, "tr")
        self.translator = GoogleTranslator(source='en', target=self.target_lang)
        self.log_ekle(f"Hedef dil {secim} olarak ayarlandı.")

    def alan_sec(self):
        self.withdraw()
        time.sleep(0.5)
        top = tk.Toplevel()
        top.attributes("-alpha", 0.4, "-fullscreen", True, "-topmost", True)
        top.config(cursor="cross")
        canvas = tk.Canvas(top, bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def bitti(e):
            self.secili_alan = (min(self.sx, e.x), min(self.sy, e.y), abs(e.x-self.sx), abs(e.y-self.sy))
            top.destroy()
            self.deiconify()
            self.log_ekle("Altyazı bölgesi kilitlendi.")
            self.progress_label.configure(text="Durum: Bölge seçildi")

        canvas.bind("<ButtonPress-1>", lambda e: setattr(self, 'sx', e.x) or setattr(self, 'sy', e.y))
        canvas.bind("<B1-Motion>", lambda e: canvas.delete("r") or canvas.create_rectangle(self.sx, self.sy, e.x, e.y, outline="#00d2ff", width=3, tags="r"))
        canvas.bind("<ButtonRelease-1>", bitti)

    def motor_tetikle(self):
        if not self.secili_alan: 
            messagebox.showwarning("Hata", "Önce bölge seçmelisin!")
            return
        
        if not self.calisiyor:
            self.calisiyor = True
            self.ekran = SubtitleOverlay()
            self.btn_baslat.configure(text="⏹️ DURDUR", fg_color="#ff4b4b", text_color="#fff")
            self.progress_label.configure(text="Durum: Çalışıyor...")
            self.progress_bar.set(0.5)
            threading.Thread(target=self.akilli_isleyici, daemon=True).start()
            self.log_ekle("Dönüştürücü başlatıldı.")
        else:
            self.calisiyor = False
            self.ekran.destroy()
            self.btn_baslat.configure(text="▶️ AKILLI DÖNÜŞTÜRÜCÜYÜ BAŞLAT", fg_color="#00d2ff", text_color="#000")
            self.progress_label.configure(text="Durum: Durduruldu")
            self.progress_bar.set(0)
            self.log_ekle("Dönüştürücü durduruldu.")

    def akilli_isleyici(self):
        biriken_metin = ""
        son_okuma_vakti = time.time()
        donusturme_sayisi = 0
        
        while self.calisiyor:
            try:
                # Optimizasyon: Görüntüyü daha hızlı işle
                ekran_goruntusu = pyautogui.screenshot(region=self.secili_alan)
                
                # Gelişmiş görüntü işleme
                processed_img = ImageOps.grayscale(ekran_goruntusu)
                processed_img = ImageOps.invert(processed_img)
                processed_img = processed_img.filter(ImageFilter.MedianFilter(size=3))  # Gürültü azaltma
                processed_img = ImageEnhance.Contrast(processed_img).enhance(self.ocr_hassasiyet)
                
                su_anki_metin = pytesseract.image_to_string(processed_img, lang='eng', config='--psm 6').strip()
                
                # Debug log
                if su_anki_metin and len(su_anki_metin) > 2:
                    self.log_ekle(f"OCR: '{su_anki_metin[:50]}...'" if len(su_anki_metin) > 50 else f"OCR: '{su_anki_metin}'", "DEBUG")
                
                # Yeni metin kontrolü
                if len(su_anki_metin) > 3:  # Minimum uzunluk
                    if su_anki_metin != biriken_metin:
                        biriken_metin = su_anki_metin
                        son_okuma_vakti = time.time()
                        self.log_ekle(f"Yeni metin: '{biriken_metin[:30]}...'" if len(biriken_metin) > 30 else f"Yeni metin: '{biriken_metin}'", "DEBUG")
                        self.progress_bar.set(0.7)
                
                # Cümle bitiş kontrolü
                if biriken_metin and (time.time() - son_okuma_vakti > self.bekleme_suresi):
                    try:
                        # Dönüştürme
                        cevirilen = self.translator.translate(biriken_metin)
                        self.ekran.guncelle(cevirilen)
                        
                        # Geçmişe ekle
                        timestamp = time.strftime("%H:%M:%S")
                        gecmis_item = f"[{timestamp}] {biriken_metin} → {cevirilen}"
                        self.gecmis.append(gecmis_item)
                        
                        self.log_ekle(f"DÖNÜŞTÜRÜLDÜ: {cevirilen}")
                        donusturme_sayisi += 1
                        self.progress_label.configure(text=f"Durum: {donusturme_sayisi} dönüştürme yapıldı")
                        
                        # Otomatik kaydetme
                        if self.ayarlar.get('kaydet_otomatik', False):
                            self.donusturme_kaydet()
                        
                        self.progress_bar.set(1.0)
                        
                    except Exception as e:
                        self.log_ekle(f"Dönüştürme hatası: {e}", "ERROR")
                    
                    biriken_metin = ""
                    self.progress_bar.set(0.5)
                
                time.sleep(0.2)  # Daha hızlı tarama
                
            except Exception as e:
                self.log_ekle(f"Genel hata: {e}", "ERROR")
                time.sleep(0.5)

if __name__ == "__main__":
    app = ByteTubeApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()