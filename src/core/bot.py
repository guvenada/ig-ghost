from playwright.sync_api import sync_playwright
import random
import time
import os

class BotEngine:
    def __init__(self, logger_callback, progress_callback):
        self.log = logger_callback
        self.update_progress = progress_callback
        self.is_running = False
        
        # Advanced Stealth Configurations
        self.stealth_args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
            "--disable-site-isolation-trials",
            "--no-sandbox",
            "--disable-web-security",
            "--disable-xss-auditor"
        ]

    def _inject_stealth_scripts(self, page):
        # Cloudflare ve Instagram'ın anti-bot (Akamai vb.) sistemlerini atlatmak için gerekli JS hook'ları.
        # WebDriver bayraklarını gizler ve donanım parmak izlerini manipüle eder.
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {}, app: {}, csi: () => {} };
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['tr-TR', 'tr', 'en-US', 'en']});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 12});
            
            // Canvas/WebGL Fingerprint Spoofing
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                return getParameter(parameter);
            };
        """)

    def stop(self):
        self.is_running = False

    def run(self, usernames, min_delay, max_delay, browser_name, profile_dir, mode="Sadece İptal Et"):
        self.is_running = True
        try:
            with sync_playwright() as p:
                context = None
                browser = None
                
                # Setup Context based on selection
                if browser_name == "Manual Login":
                    self.log("Manuel giriş modu başlatılıyor...")
                    browser = p.chromium.launch(headless=False, args=self.stealth_args)
                    context = browser.new_context(
                        viewport={'width': 1280, 'height': 720},
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                    )
                    page = context.new_page()
                else:
                    self.log(f"[{browser_name}] profili kullanılıyor... Lütfen tarayıcının tamamen kapalı olduğundan emin olun.")
                    local_appdata = os.environ['LOCALAPPDATA']
                    
                    if browser_name == "Brave":
                        executable_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
                        if not os.path.exists(executable_path):
                            executable_path = os.path.join(local_appdata, 'BraveSoftware', 'Brave-Browser', 'Application', 'brave.exe')
                        user_data_dir = os.path.join(local_appdata, 'BraveSoftware', 'Brave-Browser', 'User Data')
                        # Forcibly kill brave to release the SingletonLock
                        os.system("taskkill /F /IM brave.exe /T >nul 2>&1")
                    elif browser_name == "Chrome":
                        executable_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                        if not os.path.exists(executable_path):
                            executable_path = os.path.join(local_appdata, 'Google', 'Chrome', 'Application', 'chrome.exe')
                        user_data_dir = os.path.join(local_appdata, 'Google', 'Chrome', 'User Data')
                        os.system("taskkill /F /IM chrome.exe /T >nul 2>&1")
                    elif browser_name == "Edge":
                        executable_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                        user_data_dir = os.path.join(local_appdata, 'Microsoft', 'Edge', 'User Data')
                        os.system("taskkill /F /IM msedge.exe /T >nul 2>&1")
                    else:
                        raise ValueError("Bilinmeyen tarayıcı!")

                    # Ensure any lingering processes are completely dead before accessing the lockfile
                    time.sleep(1)

                    try:
                        context = p.chromium.launch_persistent_context(
                            user_data_dir=user_data_dir,
                            executable_path=executable_path,
                            headless=False,
                            viewport={'width': 1280, 'height': 720},
                            args=self.stealth_args + [
                                f"--profile-directory={profile_dir}",
                                "--window-position=-2000,-2000"
                            ]
                        )
                        page = context.pages[0] if context.pages else context.new_page()
                    except Exception as e:
                        self.log("[HATA] Tarayıcı profiline erişilemedi. İşlem kilitli olabilir.")
                        self.log("[ÇÖZÜM] Tarayıcının tamamen kapalı olduğundan emin olun.")
                        self.is_running = False
                        return

                self._inject_stealth_scripts(page)
                self.log("[SİSTEM] Ağa müdahale ediliyor... Gereksiz kaynaklar bloklandı.")
                
                # Dark Web Routing: Intercept and drop all non-essential traffic
                def block_aggressively(route):
                    if route.request.resource_type in ["image", "media", "font", "stylesheet", "other"]:
                        route.abort()
                    else:
                        route.continue_()
                
                page.route("**/*", block_aggressively)
                
                self.log("[SİSTEM] Instagram bağlantısı kuruluyor... (Dark Routing Aktif)")
                page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
                # Wait for the main body rather than hard sleeping
                page.wait_for_selector("body", timeout=10000)
                
                # Oturum durumunu kontrol et
                html = page.content()
                if "Giriş Yap" in html or "Log In" in html:
                    self.log("[UYARI] Oturum kapalı. Lütfen tarayıcı profilinizden giriş yapın.")
                    return
                else:
                    self.log("[BİLGİ] Oturum doğrulandı. İşlem kuyruğu başlatılıyor.")

                total = len(usernames)
                for i, username in enumerate(usernames):
                    if not self.is_running:
                        self.log("[DURUM] Bot durduruldu.")
                        break
                        
                    self.log(f"[DURUM] {i+1}/{total} - {username} ziyaret ediliyor.")
                    
                    self.update_progress({
                        "type": "start",
                        "current": i,
                        "total": total,
                        "username": username
                    })
                    
                    try:
                        # Undetected fast routing - wait only for DOM, not heavy images/scripts
                        page.goto(f"https://www.instagram.com/{username}/", wait_until="domcontentloaded")
                        
                        # Wait dynamically for the profile header or error text rather than blind sleeping
                        try:
                            page.wait_for_selector("header, h2, div[dir='auto']", timeout=5000)
                        except:
                            pass
                        
                        # Apply stealth delay *after* page load so it looks like human reading time
                        stealth_time = random.uniform(min_delay, max_delay)
                        self.log(f"[GİZLİLİK] İnsan davranışı simüle ediliyor... ({stealth_time:.1f} sn)")
                        time.sleep(stealth_time)
                        
                        html = page.content()
                        if "Üzgünüz, bu sayfaya ulaşılamıyor" in html or "Sorry, this page isn't available" in html or "Sayfa Bulunamadı" in html:
                            self.log(f"[HATA] {username} hesabı bulunamadı.")
                            self.update_progress({
                                "type": "result",
                                "username": username,
                                "status": "DELETED",
                                "pfp_url": None
                            })
                            continue
                            
                        # Undetected API Spoofing payload
                        payload = page.evaluate(f"""async () => {{
                            try {{
                                // 1. Fetch internal metadata
                                let res = await fetch('/api/v1/users/web_profile_info/?username={username}', {{
                                    headers: {{'x-ig-app-id': '936619743392459'}}
                                }});
                                let json = await res.json();
                                let user_id = json.data.user.id;
                                let pfp = json.data.user.profile_pic_url_hd || json.data.user.profile_pic_url;
                                
                                // 2. Extract CSRF Token
                                let csrf_match = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
                                let csrf = csrf_match ? csrf_match.split('=')[1] : '';
                                
                                // 3. Forge the Unfollow / Cancel Request POST
                                let destroy_res = await fetch(`/api/v1/friendships/destroy/${{user_id}}/`, {{
                                    method: 'POST',
                                    headers: {{
                                        'x-ig-app-id': '936619743392459',
                                        'X-CSRFToken': csrf,
                                        'Content-Type': 'application/x-www-form-urlencoded'
                                    }}
                                }});
                                let destroy_json = await destroy_res.json();
                                
                                let bumped = false;
                                // 4. If Bump Mode is active, send a follow request back immediately
                                if ("{mode}" === "İptal + Yeniden Takip" && destroy_json.status === 'ok') {{
                                    // Wait a tiny bit inside JS to simulate click delay
                                    await new Promise(r => setTimeout(r, 1500));
                                    
                                    let create_res = await fetch(`/api/v1/friendships/create/${{user_id}}/`, {{
                                        method: 'POST',
                                        headers: {{
                                            'x-ig-app-id': '936619743392459',
                                            'X-CSRFToken': csrf,
                                            'Content-Type': 'application/x-www-form-urlencoded'
                                        }}
                                    }});
                                    let create_json = await create_res.json();
                                    bumped = create_json.status === 'ok';
                                }}
                                
                                return {{
                                    'pfp': pfp,
                                    'api_success': destroy_json.status === 'ok',
                                    'bumped': bumped
                                }};
                            }} catch(e) {{
                                return {{'error': e.toString()}};
                            }}
                        }}""")
                        
                        if payload and "error" not in payload:
                            pfp_url = payload.get("pfp")
                            self.update_progress({"type": "pfp", "username": username, "pfp_url": pfp_url})
                            
                            if payload.get("api_success"):
                                if payload.get("bumped"):
                                    self.log(f"[GHOST API] {username} -> İstek iptal edildi ve yeniden gönderildi (BUMP).")
                                    self.update_progress({"type": "result", "username": username, "status": "BUMPED"})
                                else:
                                    self.log(f"[GHOST API] {username} -> İstek başarıyla iptal edildi.")
                                    self.update_progress({"type": "result", "username": username, "status": "SUCCESS"})
                            else:
                                self.log(f"[GHOST API] {username} için iptal API'si reddedildi (Zaten silinmiş olabilir).")
                                self.update_progress({"type": "result", "username": username, "status": "ALREADY_DONE"})
                        else:
                            self.log(f"[HATA] API Spoofing başarısız: {payload.get('error') if payload else 'Bilinmiyor'}")
                            self.update_progress({"type": "result", "username": username, "status": "ALREADY_DONE"})
                            
                    except Exception as e:
                        self.log(f"[HATA] {username} profilinde işlem sırasında hata oluştu: {str(e)[:50]}")
                        self.update_progress({"type": "result", "username": username, "status": "ERROR"})
                    
                    if i < total - 1 and self.is_running:
                        delay = random.uniform(min_delay, max_delay)
                        self.log(f"[DURUM] İstek oranı sınırlayıcısı devrede... {delay:.1f} saniye bekleniyor...")
                        time.sleep(delay)
                        
                if browser_name == "Manual Login" and browser:
                    browser.close()
                elif context:
                    context.close()
                self.log("🎉 İşlemler tamamlandı!")

        except Exception as e:
            self.log(f"Kritik Hata: {str(e)}")
        finally:
            self.is_running = False
