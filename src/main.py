import os
import sys
import time
import customtkinter as ctk
from PIL import Image

from core.scanner import Scanner
from core.bot import BotEngine
from ui.gui import GhostBotUI

class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IG Ghost Init")
        self.geometry("500x300")
        self.overrideredirect(True) # Borderless
        
        # Center the splash screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)
        y = (screen_height / 2) - (300 / 2)
        self.geometry(f'+{int(x)}+{int(y)}')
        
        self.configure(fg_color="#0a0a0a") # Deep titanium background
        
        # Main Frame
        self.frame = ctk.CTkFrame(self, fg_color="#121212", corner_radius=15, border_width=1, border_color="#333")
        self.frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Load Custom Logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
            self.logo_img = ctk.CTkImage(light_image=Image.open(logo_path), 
                                         dark_image=Image.open(logo_path), 
                                         size=(80, 80))
            self.lbl_logo = ctk.CTkLabel(self.frame, image=self.logo_img, text="")
            self.lbl_logo.pack(pady=(40, 5))
        except Exception as e:
            self.lbl_title = ctk.CTkLabel(self.frame, text="IG GHOST", font=ctk.CTkFont(family="Courier", size=36, weight="bold"), text_color="#ffffff")
            self.lbl_title.pack(pady=(70, 5))
            
        self.lbl_sub = ctk.CTkLabel(self.frame, text="AUTOMATED SESSION ENGINE", font=ctk.CTkFont(size=12), text_color="#00E5FF")
        self.lbl_sub.pack(pady=0)
        
        # Loading Bar
        self.progress = ctk.CTkProgressBar(self.frame, width=300, height=4, fg_color="#222", progress_color="#00E5FF")
        self.progress.pack(pady=(50, 10))
        self.progress.set(0)
        
        self.lbl_status = ctk.CTkLabel(self.frame, text="Initializing drivers...", font=ctk.CTkFont(size=10), text_color="#666")
        self.lbl_status.pack()
        
    def simulate_loading(self):
        steps = [
            ("Mounting payload...", 0.2, 0.3),
            ("Bypassing user-mode APIs...", 0.5, 0.4),
            ("Injecting stealth modules...", 0.8, 0.5),
            ("Ready.", 1.0, 0.4)
        ]
        
        for text, prog, delay in steps:
            self.lbl_status.configure(text=text)
            self.progress.set(prog)
            self.update()
            time.sleep(delay)
            
        self.destroy()

def main():
    # Make sure we're in the right directory so relative paths work
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    sys.path.append(script_dir)
    
    ctk.set_appearance_mode("dark")
    
    splash = SplashScreen()
    splash.update()
    splash.simulate_loading()
    
    scanner = Scanner()
    engine = BotEngine(None, None)
    app = GhostBotUI(scanner, engine)
    
    engine.log = app.log
    engine.update_progress = app.update_progress
    
    app.mainloop()

if __name__ == "__main__":
    main()
