import os
import json

class Scanner:
    def __init__(self):
        self.accounts = []

    def scan_all_profiles(self):
        """Instantly scans local appdata to find all available browser profiles."""
        self.accounts = []
        local_appdata = os.environ.get('LOCALAPPDATA', '')
        if not local_appdata:
            return self.accounts

        browsers = {
            "Chrome": os.path.join(local_appdata, 'Google', 'Chrome', 'User Data'),
            "Brave": os.path.join(local_appdata, 'BraveSoftware', 'Brave-Browser', 'User Data'),
            "Edge": os.path.join(local_appdata, 'Microsoft', 'Edge', 'User Data')
        }

        for browser_name, user_data_path in browsers.items():
            if not os.path.exists(user_data_path):
                continue
                
            for p in os.listdir(user_data_path):
                p_path = os.path.join(user_data_path, p)
                if os.path.isdir(p_path) and (p == 'Default' or p.startswith('Profile')):
                    display_name = p
                    pref_path = os.path.join(p_path, 'Preferences')
                    if os.path.exists(pref_path):
                        try:
                            with open(pref_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                name = data.get('profile', {}).get('name', '')
                                if name and name != "Person 1" and name != "Person 2":
                                    display_name = f"{p} ({name})"
                        except:
                            pass
                            
                    self.accounts.append({
                        "browser": browser_name,
                        "profile_dir": p,
                        "user_data_dir": user_data_path,
                        "display": f"[{browser_name}] {display_name}"
                    })

        return self.accounts
