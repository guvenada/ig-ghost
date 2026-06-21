<div align="center">
  <img src="src/assets/logo.png" alt="IG GHOST Logo" width="200"/>
  <h1>IG GHOST // Session Engine</h1>
  <p><strong>Advanced, Undetectable Instagram Follow Request Manager</strong></p>

  <p>
    <a href="README_TR.md">🇹🇷 Türkçe Dokümantasyon</a>
  </p>
</div>

---

## ⚡ Overview

**IG GHOST** is a high-performance, stealth-focused automation engine designed to rapidly manage pending outgoing follow requests on Instagram. 

Unlike traditional Selenium-based bots that rely on slow, brittle DOM interactions, IG GHOST utilizes **Dark Routing** and **Raw API Spoofing**. It hijacks internal GraphQL endpoints (`web_profile_info`) and directly forges authenticated `friendships/destroy/` POST requests. This completely bypasses frontend image/asset loading, resulting in near-instantaneous execution times while remaining completely undetected by Akamai and Cloudflare anti-bot systems.

<div align="center">
  <!-- TODO: Replace the src below with your actual demo GIF once you record it -->
  <img src="src/assets/demo.png" alt="IG GHOST Demo" width="700"/>
  <p><i>*Demo showcasing the Dark Routing speed and API Spoofing UI*</i></p>
</div>

## 🚀 Features

- **Dark Routing Engine**: Aborts all non-essential network traffic (Images, Media, Fonts, CSS) via Playwright lifecycle hooks. DOM parses instantly.
- **API Spoofing**: Bypasses UI buttons. Extracts internal `user_id` and `csrftoken` to fire raw, authenticated HTTP requests directly to Instagram's backend.
- **Bump Mode (Cancel & Refollow)**: Cancel stale follow requests and immediately refollow, bumping you to the top of the target's notification feed.
- **Local Browser Hijacking**: No need to provide your password. IG GHOST securely hooks into your existing Chrome, Edge, or Brave sessions via `LOCALAPPDATA`.
- **Titanium UI**: A sleek, borderless, hardware-accelerated dashboard built with CustomTkinter. 

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/guvenada/ig-ghost.git
cd ig-ghost

# Install dependencies
pip install -r requirements.txt

# Run the engine
python src/main.py
```

## ⚠️ Legal Disclaimer (Educational Use Only)

> [!WARNING]
> This software is provided for **educational and research purposes only**. 
> 
> The developers ("guvenada") assume no liability and are not responsible for any misuse, damage, or account bans caused by this program. By using this software, you agree to take full responsibility for your actions. 
> 
> This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Meta Platforms, Inc. or Instagram. The name Instagram, as well as related names, marks, emblems, and images are registered trademarks of their respective owners.

**For commercial use inquiries:** `adaguven@protonmail.com`

---
<div align="center">
  Developed by <a href="https://github.com/guvenada">guvenada</a>
</div>
