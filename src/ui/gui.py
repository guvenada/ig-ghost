import customtkinter as ctk
from tkinter import filedialog
from bs4 import BeautifulSoup
import os
import threading
import requests
from PIL import Image
from io import BytesIO

class GhostBotUI(ctk.CTk):
    def __init__(self, scanner, bot_engine):
        super().__init__()
        self.scanner = scanner
        self.bot_engine = bot_engine
        
        self.title("IG GHOST // Session Engine")
        
        # Start completely transparent/hidden for the smooth boot effect
        self.attributes('-alpha', 0.0)
        self.geometry("800x600") # Start slightly smaller for expansion effect
        
        # Titanium color palette
        self.bg_color = "#0a0a0a"
        self.frame_color = "#121212"
        self.accent_color = "#00E5FF" # Neon Cyan
        self.accent_hover = "#008B99" # Softer hover jump
        self.text_primary = "#ffffff"
        self.text_secondary = "#a0a0a0"
        
        self.configure(fg_color=self.bg_color)
        
        # Set Window Icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo.ico")
            self.iconbitmap(icon_path)
        except:
            pass
        
        self.filepath = None
        self.usernames = []
        self.accounts_data = []

        # Stats
        self.stat_success = 0
        self.stat_already = 0
        self.stat_error = 0
        self.stat_total = 0

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Pre-calculate estimated time components
        self.avg_delay = 5.0 # baseline
        self.start_time = 0

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.frame_color)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        try:
            from PIL import Image, ImageDraw
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo.png")
            raw_img = Image.open(logo_path).convert("RGBA")
            
            # Crop logo to circle for a modern look
            mask = Image.new("L", raw_img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, raw_img.size[0], raw_img.size[1]), fill=255)
            circular_img = Image.new("RGBA", raw_img.size, (0, 0, 0, 0))
            circular_img.paste(raw_img, (0, 0), mask=mask)
            
            self.sidebar_logo_img = ctk.CTkImage(light_image=circular_img, 
                                                 dark_image=circular_img, 
                                                 size=(70, 70))
            self.lbl_sidebar_logo = ctk.CTkLabel(self.sidebar, image=self.sidebar_logo_img, text="")
            self.lbl_sidebar_logo.grid(row=0, column=0, padx=20, pady=(30, 0))
        except Exception as e:
            logo_label = ctk.CTkLabel(self.sidebar, text="IG GHOST", font=ctk.CTkFont(family="Courier", size=24, weight="bold"), text_color=self.accent_color)
            logo_label.grid(row=0, column=0, padx=20, pady=(30, 0))
        
        author_label = ctk.CTkLabel(self.sidebar, text="guvenada.codes", font=ctk.CTkFont(size=12), text_color=self.text_secondary)
        author_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        # File Selection
        self.btn_select = ctk.CTkButton(self.sidebar, text="[1] HTML Seç", command=self.select_file, fg_color=self.accent_color, hover_color=self.accent_hover, text_color="#000")
        self.btn_select.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_file = ctk.CTkLabel(self.sidebar, text="Dosya seçilmedi", text_color=self.text_secondary, font=ctk.CTkFont(size=11))
        self.lbl_file.grid(row=3, column=0, padx=20, pady=(0, 20))

        # Account Scanner
        self.btn_scan = ctk.CTkButton(self.sidebar, text="[2] Sistem Taraması", command=self.scan_accounts, fg_color=self.accent_color, hover_color=self.accent_hover, text_color="#000")
        self.btn_scan.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.scan_loader = ctk.CTkProgressBar(self.sidebar, mode="indeterminate", progress_color=self.accent_color, fg_color="#333333", height=4)
        self.scan_loader.grid(row=4, column=0, padx=20, pady=(45, 0), sticky="nwe")
        self.scan_loader.grid_remove() 

        # Account Dropdown
        self.lbl_acc = ctk.CTkLabel(self.sidebar, text="Kullanılacak Hesap:", text_color=self.text_secondary)
        self.lbl_acc.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.acc_var = ctk.StringVar(value="Manual Login")
        self.dropdown_acc = ctk.CTkOptionMenu(self.sidebar, variable=self.acc_var, values=["Manual Login"], fg_color="#333333", button_color=self.accent_color)
        self.dropdown_acc.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="nwe")

        # Links at bottom
        link_font = ctk.CTkFont(size=11, underline=True)
        lbl_git = ctk.CTkLabel(self.sidebar, text="github.com/guvenada", font=link_font, text_color="#58A6FF", cursor="hand2")
        lbl_git.grid(row=7, column=0, padx=20, pady=5)
        lbl_lin = ctk.CTkLabel(self.sidebar, text="linkedin.com/in/guvenada", font=link_font, text_color="#58A6FF", cursor="hand2")
        lbl_lin.grid(row=8, column=0, padx=20, pady=(0, 10))
        
        lbl_commercial = ctk.CTkLabel(self.sidebar, text="Commercial use inquiries:\nadaguven@protonmail.com", font=ctk.CTkFont(size=10), text_color="#666666")
        lbl_commercial.grid(row=9, column=0, padx=20, pady=(0, 20))

        # --- MAIN AREA ---
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(2, weight=1)

        # 1) Top Controls
        self.top_controls = ctk.CTkFrame(self.main_area, fg_color=self.frame_color, corner_radius=10)
        self.top_controls.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        ctk.CTkLabel(self.top_controls, text="Stealth Delay (Sn):", text_color=self.text_secondary).grid(row=0, column=0, padx=(15, 5), pady=10)
        self.entry_min = ctk.CTkEntry(self.top_controls, width=40, fg_color="#333")
        self.entry_min.insert(0, "4")
        self.entry_min.grid(row=0, column=1, padx=2, pady=10)
        ctk.CTkLabel(self.top_controls, text="-").grid(row=0, column=2)
        self.entry_max = ctk.CTkEntry(self.top_controls, width=40, fg_color="#333")
        self.entry_max.insert(0, "8")
        self.entry_max.grid(row=0, column=3, padx=2, pady=10)

        # Mode Selector
        self.mode_var = ctk.StringVar(value="İptal Et")
        self.dropdown_mode = ctk.CTkSegmentedButton(self.top_controls, variable=self.mode_var, 
                                                    values=["İptal Et", "İptal + Yeniden Takip"], 
                                                    selected_color=self.accent_color, selected_hover_color=self.accent_hover,
                                                    unselected_color="#222", unselected_hover_color="#333", text_color="#fff")
        self.dropdown_mode.grid(row=0, column=4, padx=(15, 10), pady=10)

        self.btn_start = ctk.CTkButton(self.top_controls, text="BAŞLAT", font=ctk.CTkFont(weight="bold"), 
                                       command=self.start_bot, fg_color=self.accent_color, hover_color=self.accent_hover, text_color="#000", width=100)
        self.btn_start.grid(row=0, column=5, padx=(10, 5), pady=10, sticky="e")
        self.btn_stop = ctk.CTkButton(self.top_controls, text="DURDUR", font=ctk.CTkFont(weight="bold"), 
                                       command=self.stop_bot, fg_color="#ff4444", hover_color="#CC0000", text_color="#fff", state="disabled", width=100)
        self.btn_stop.grid(row=0, column=6, padx=(0, 15), pady=10, sticky="e")

        # 2) Live Dashboard
        self.dash_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.dash_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.dash_frame.grid_columnconfigure(0, weight=1)
        self.dash_frame.grid_columnconfigure(1, weight=2)

        self.target_card = ctk.CTkFrame(self.dash_frame, fg_color=self.frame_color, corner_radius=10)
        self.target_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.lbl_pfp = ctk.CTkLabel(self.target_card, text="", width=80, height=80, corner_radius=40, fg_color="#333")
        self.lbl_pfp.pack(pady=(15, 5))
        self.lbl_target_user = ctk.CTkLabel(self.target_card, text="@bekleniyor...", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_target_user.pack()
        self.lbl_target_status = ctk.CTkLabel(self.target_card, text="Sistem Hazır", text_color=self.text_secondary)
        self.lbl_target_status.pack(pady=(0, 15))

        self.stats_card = ctk.CTkFrame(self.dash_frame, fg_color=self.frame_color, corner_radius=10)
        self.stats_card.grid(row=0, column=1, sticky="nsew")
        self.stats_card.grid_columnconfigure((0,1), weight=1)
        self.stats_card.grid_rowconfigure((0,1), weight=1)
        
        stat_font = ctk.CTkFont(size=18, weight="bold")
        
        self.lbl_stat_success = ctk.CTkLabel(self.stats_card, text="[+] Başarılı: 0", font=stat_font, text_color="#00C851")
        self.lbl_stat_success.grid(row=0, column=0, pady=10)
        self.lbl_stat_already = ctk.CTkLabel(self.stats_card, text="[!] Zaten İptal: 0", font=stat_font, text_color="#FFBB33")
        self.lbl_stat_already.grid(row=0, column=1, pady=10)
        self.lbl_stat_error = ctk.CTkLabel(self.stats_card, text="[-] Hata/Silinmiş: 0", font=stat_font, text_color="#ff4444")
        self.lbl_stat_error.grid(row=1, column=0, pady=10)
        
        self.lbl_stat_left = ctk.CTkLabel(self.stats_card, text="[~] Kalan: 0", font=stat_font, text_color=self.accent_color)
        self.lbl_stat_left.grid(row=1, column=1, pady=(10, 0))
        self.lbl_stat_time = ctk.CTkLabel(self.stats_card, text="Tahmini Süre: --:--", font=ctk.CTkFont(size=12), text_color=self.text_secondary)
        self.lbl_stat_time.grid(row=2, column=1, pady=(0, 10))

        # 3) Terminal
        self.terminal = ctk.CTkTextbox(self.main_area, fg_color="#000000", text_color="#00FF00", font=ctk.CTkFont(family="Consolas", size=13))
        self.terminal.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        self.log("[SİSTEM] IG GHOST Session Engine başlatıldı. Sistem hazır.\n")

        # 4) Progress Bar
        self.progress_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.progress_frame.grid(row=3, column=0, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=self.accent_color, fg_color="#222", height=8)
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=5)
        self.progress_bar.set(0)
        
        # Initiate the smooth expansion animation
        self.after(50, self._animate_boot)
        
    def _animate_boot(self, step=0):
        max_steps = 40.0
        if step <= max_steps:
            # Ease-out cubic calculation for ultra-smooth transition
            t = step / max_steps
            ease_out = 1 - pow(1 - t, 3)
            
            alpha = ease_out
            width = int(700 + (200 * ease_out))
            height = int(550 + (150 * ease_out))
            
            # Center the expanding window
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            
            self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
            self.attributes('-alpha', alpha)
            
            self.after(10, self._animate_boot, step + 1)

    def log(self, msg):
        self.terminal.insert("end", f"> {msg}\n")
        self.terminal.see("end")

    def _download_pfp(self, url):
        try:
            response = requests.get(url, timeout=5)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((80, 80))
            
            def update_ui():
                try:
                    self._current_pfp = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
                    self.lbl_pfp.configure(image=self._current_pfp, text="")
                except:
                    pass
                    
            self.after(0, update_ui)
        except Exception as e:
            def set_fail():
                try:
                    self.lbl_pfp.configure(text="Resim\nYok")
                except:
                    pass
            self.after(0, set_fail)

    def update_progress(self, data):
        def _sync_update():
            if isinstance(data, dict):
                msg_type = data.get("type")
                
                if msg_type == "start":
                    user = data.get("username")
                    total = data.get("total")
                    current = data.get("current")
                    
                    self.lbl_target_user.configure(text=f"@{user}")
                    self.lbl_target_status.configure(text="Ziyaret ediliyor...", text_color=self.text_primary)
                    try:
                        self.lbl_pfp.configure(image="", text="Yükleniyor...")
                    except:
                        pass
                    
                    # Update counters (we don't have progress_bar in titanium yet, but stat_left might exist)
                    try:
                        if hasattr(self, 'lbl_stat_left'):
                            left = total - current
                            self.lbl_stat_left.configure(text=f"[~] Kalan: {left}")
                            
                            # Calculate estimated time (Average 6s per loop based on typical stealth delays)
                            # Update avg_delay dynamically if we want, but static 6s is safe for IG
                            est_seconds = left * 6.0 
                            mins = int(est_seconds // 60)
                            secs = int(est_seconds % 60)
                            self.lbl_stat_time.configure(text=f"Tahmini Süre: {mins:02d}:{secs:02d}")
                    except:
                        pass
                        
                elif msg_type == "pfp":
                    pfp_url = data.get("pfp_url")
                    if pfp_url:
                        threading.Thread(target=self._download_pfp, args=(pfp_url,), daemon=True).start()
                    else:
                        try:
                            self.lbl_pfp.configure(image="", text="Resim Yok")
                        except:
                            pass
                        
                elif msg_type == "result":
                    status = data.get("status")
                    if status == "SUCCESS":
                        self.stat_success += 1
                        self.lbl_stat_success.configure(text=f"[+] Başarılı: {self.stat_success}")
                        self.lbl_target_status.configure(text="İstek İptal Edildi", text_color="#00E5FF")
                    elif status == "BUMPED":
                        self.stat_success += 1
                        self.lbl_stat_success.configure(text=f"[+] Başarılı: {self.stat_success}")
                        self.lbl_target_status.configure(text="İptal + Yeniden İstek!", text_color="#00E5FF")
                    elif status == "ALREADY_DONE":
                        self.stat_already += 1
                        self.lbl_stat_already.configure(text=f"[!] Zaten İptal: {self.stat_already}")
                        self.lbl_target_status.configure(text="Zaten İptal", text_color="#ffbb33")
                    elif status == "DELETED":
                        self.stat_error += 1
                        self.lbl_stat_error.configure(text=f"[-] Hata/Silinmiş: {self.stat_error}")
                        self.lbl_target_status.configure(text="Hesap Bulunamadı", text_color="#ff4444")
                        
        self.after(0, _sync_update)

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if self.filepath:
            name = os.path.basename(self.filepath)
            self.lbl_file.configure(text=name[:20] + "..." if len(name) > 20 else name)
            self.usernames = self.extract_usernames(self.filepath)
            self.stat_total = len(self.usernames)
            self.log(f"[DOSYA] {self.stat_total} adet bekleyen istek bulundu.")
            self.lbl_stat_left.configure(text=f"[~] Kalan: {self.stat_total}")
            self.progress_bar.set(0)

    def extract_usernames(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            usernames = []
            for td in soup.find_all('td'):
                if td.text.strip() == "Kullanıcı adı":
                    next_td = td.find_next_sibling('td')
                    if next_td:
                        usernames.append(next_td.text.strip())
            return usernames
        except Exception as e:
            self.log(f"Dosya okuma hatası: {e}")
            return []

    def scan_accounts(self):
        self.log("[TARAMA] Bilgisayardaki tarayıcılar (Chrome, Brave, Edge) taranıyor...")
        self.log("[TARAMA] Bu işlem arkaplanda tarayıcıları çalıştırdığı için 5-15 saniye sürebilir. Lütfen bekleyin...")
        self.btn_scan.configure(state="disabled", text="[+] Taranıyor...")
        self.scan_loader.grid()
        self.scan_loader.start()
        
        def run_scan():
            self.accounts_data = self.scanner.scan_all_profiles()
            
            options = ["Manual Login"]
            for acc in self.accounts_data:
                options.append(acc["display"])
                
            self.after(0, self._update_dropdown, options)
            
        threading.Thread(target=run_scan, daemon=True).start()

    def _update_dropdown(self, options):
        self.scan_loader.stop()
        self.scan_loader.grid_remove()
        self.dropdown_acc.configure(values=options)
        if len(options) > 1:
            self.acc_var.set(options[1])
        self.btn_scan.configure(state="normal", text="[2] Sistem Taraması")
        self.log(f"[TARAMA] Tamamlandı. {len(options)-1} adet profil bulundu.")

    def start_bot(self):
        if not self.usernames:
            self.log("[HATA] Lütfen önce HTML dosyasını seçin.")
            return
            
        try:
            min_d = int(self.entry_min.get())
            max_d = int(self.entry_max.get())
        except ValueError:
            self.log("[HATA] Delay değerleri sayı olmalıdır.")
            return

        selected_display = self.acc_var.get()
        browser_name = "Manual Login"
        profile_dir = "Default"

        if selected_display != "Manual Login":
            for acc in self.accounts_data:
                if acc["display"] == selected_display:
                    browser_name = acc["browser"]
                    profile_dir = acc["profile_dir"]
                    break

        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.btn_select.configure(state="disabled")
        self.btn_scan.configure(state="disabled")
        self.dropdown_acc.configure(state="disabled")
        
        # Reset Stats
        self.stat_success = 0
        self.stat_already = 0
        self.stat_error = 0
        self.lbl_stat_success.configure(text=f"✅ Başarılı: 0")
        self.lbl_stat_already.configure(text=f"⚠️ Zaten İptal: 0")
        self.lbl_stat_error.configure(text=f"❌ Hata/Silinmiş: 0")

        # Grab Mode
        operation_mode = self.mode_var.get()

        def bot_thread():
            self.bot_engine.run(self.usernames, min_d, max_d, browser_name, profile_dir, operation_mode)
            self.after(0, self.on_bot_finish)

        threading.Thread(target=bot_thread, daemon=True).start()

    def stop_bot(self):
        self.log("[SİSTEM] Durdurma komutu gönderildi, mevcut işlemden sonra duracak...")
        self.bot_engine.stop()

    def on_bot_finish(self):
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.btn_select.configure(state="normal")
        self.btn_scan.configure(state="normal")
        self.dropdown_acc.configure(state="normal")
        self.lbl_target_status.configure(text="Sistem Durdu", text_color=self.text_secondary)

