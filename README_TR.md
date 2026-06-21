<div align="center">
  <img src="src/assets/logo.png" alt="IG GHOST Logo" width="200"/>
  <h1>IG GHOST // Session Engine</h1>
  <p><strong>Gelişmiş, Tespit Edilemeyen Instagram Takip İstek Yöneticisi</strong></p>

  <p>
    <a href="README.md">🇬🇧 English Documentation</a>
  </p>
</div>

---

## ⚡ Genel Bakış

**IG GHOST**, Instagram'da bekleyen giden takip isteklerini hızlı bir şekilde yönetmek için tasarlanmış yüksek performanslı, gizlilik odaklı bir otomasyon motorudur.

Yavaş ve kırılgan DOM etkileşimlerine dayanan geleneksel Selenium tabanlı botların aksine, IG GHOST **Karanlık Yönlendirme (Dark Routing)** ve **Ham API Kimlik Sahtekarlığı (Raw API Spoofing)** kullanır. Dahili GraphQL uç noktalarını (`web_profile_info`) ele geçirir ve doğrudan kimliği doğrulanmış `friendships/destroy/` POST istekleri oluşturur. Bu, ön uç görüntü/varlık yüklemesini tamamen atlayarak, Akamai ve Cloudflare anti-bot sistemleri tarafından tamamen tespit edilemeden neredeyse anında yürütme süreleri sağlar.

<div align="center">
  <!-- TODO: Uygulama içinden alınacak bir GIF buraya eklenebilir -->
  <img src="src/assets/demo_v2.png" alt="IG GHOST Demo" width="700"/>
  <p><i>*Dark Routing hızını ve API Spoofing arayüzünü gösteren demo*</i></p>
</div>

## 🚀 Özellikler

- **Karanlık Yönlendirme Motoru**: Playwright yaşam döngüsü kancaları aracılığıyla gereksiz tüm ağ trafiğini (Görüntüler, Medya, Yazı Tipleri, CSS) iptal eder. DOM anında ayrıştırılır.
- **API Kimlik Sahtekarlığı (Spoofing)**: UI düğmelerini atlar. Doğrudan Instagram'ın arka ucuna ham, kimliği doğrulanmış HTTP istekleri göndermek için dahili `user_id` ve `csrftoken` bilgilerini çıkarır.
- **Çarpışma Modu (İptal Et & Yeniden Takip Et)**: Eskiyen takip isteklerini iptal edip hemen yeniden takip ederek hedefin bildirim akışının en üstüne çıkmanızı sağlar (Bump).
- **Yerel Tarayıcı Korsanlığı**: Şifrenizi vermenize gerek yoktur. IG GHOST, `LOCALAPPDATA` üzerinden mevcut Chrome, Edge veya Brave oturumlarınıza güvenli bir şekilde bağlanır.
- **Titanyum Arayüz**: CustomTkinter ile oluşturulmuş şık, çerçevesiz, donanım hızlandırmalı bir kontrol paneli.

## 🛠️ Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/guvenada/ig-ghost.git
cd ig-ghost

# Gereksinimleri yükleyin
pip install -r requirements.txt

# Motoru çalıştırın
python src/main.py
```

## ⚠️ Yasal Uyarı (Sadece Eğitim Amaçlıdır)

> [!WARNING]
> Bu yazılım **yalnızca eğitim ve araştırma amaçlı** sağlanmaktadır.
> 
> Geliştiriciler ("guvenada"), bu programın neden olduğu herhangi bir kötüye kullanım, hasar veya hesap yasaklarından sorumlu değildir ve hiçbir sorumluluk kabul etmez. Bu yazılımı kullanarak eylemlerinizin tüm sorumluluğunu almayı kabul edersiniz.
> 
> Bu projenin Meta Platforms, Inc. veya Instagram ile hiçbir bağlantısı, ilişkisi, yetkilendirmesi, onayı veya resmi bir bağı yoktur. Instagram adı ile ilgili adlar, markalar, amblemler ve görseller ilgili sahiplerinin tescilli ticari markalarıdır.

**Ticari kullanım talepleri için:** `adaguven@protonmail.com`

---
<div align="center">
  <a href="https://github.com/guvenada">guvenada</a> tarafından geliştirilmiştir.
</div>
