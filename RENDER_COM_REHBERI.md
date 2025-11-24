# 🚀 Render.com - Adım Adım Deployment Rehberi

Render.com, PythonAnywhere'den çok daha kolay! GitHub'a yükleyip otomatik deploy ediyor.

---

## 📋 ÖN HAZIRLIK

### 1. GitHub Hesabı Oluşturma (Yoksa)

1. **https://github.com** adresine gidin
2. **"Sign up"** butonuna tıklayın
3. Email ve şifre ile kayıt olun
4. Email doğrulamasını yapın

---

## 📤 ADIM 1: Projeyi GitHub'a Yükleme

### 1.1. Git Kurulumu (Eğer yoksa)

Windows'ta Git genellikle yüklüdür. Kontrol edin:

```bash
git --version
```

Eğer hata verirse: **https://git-scm.com/download/win** adresinden indirin.

### 1.2. GitHub'da Repository Oluştur

1. **https://github.com** adresine gidin
2. Sağ üstte **"+"** → **"New repository"** tıklayın
3. Repository adı: **`heictojpg`** (veya istediğiniz isim)
4. **"Public"** seçin (ücretsiz için)
5. **"Create repository"** tıklayın

### 1.3. Local Projeyi GitHub'a Yükle

**PowerShell veya Command Prompt'u açın** ve şu komutları çalıştırın:

```bash
cd C:\Users\90536\Desktop\heictojpg
```

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Initial commit"
```

```bash
git branch -M main
```

```bash
git remote add origin https://github.com/KULLANICIADI/heictojpg.git
```

**ÖNEMLİ:** `KULLANICIADI` yerine GitHub kullanıcı adınızı yazın!

```bash
git push -u origin main
```

GitHub kullanıcı adı ve şifrenizi isteyecek (veya token).

**✅ Proje GitHub'a yüklendi!**

---

## 🌐 ADIM 2: Render.com'da Hesap Oluşturma

### 2.1. Render.com'a Kayıt Ol

1. **https://render.com** adresine gidin
2. **"Get Started for Free"** butonuna tıklayın
3. **"Sign up with GitHub"** seçeneğini seçin
4. GitHub hesabınızla giriş yapın
5. Render.com'a erişim izni verin

**✅ Render.com hesabınız hazır!**

---

## 🚀 ADIM 3: Web Servisi Oluşturma

### 3.1. Yeni Web Servisi

1. Render.com dashboard'da **"New +"** butonuna tıklayın
2. **"Web Service"** seçeneğini seçin

### 3.2. GitHub Repository'yi Bağla

1. **"Connect account"** veya **"Connect GitHub"** tıklayın
2. GitHub hesabınızı bağlayın
3. Repository listesinden **`heictojpg`** repository'sini seçin
4. **"Connect"** tıklayın

### 3.3. Ayarları Yapılandır

**Temel Ayarlar:**

- **Name:** `heic-to-jpg` (veya istediğiniz isim)
- **Region:** `Frankfurt` (veya size yakın)
- **Branch:** `main` (otomatik gelecek)
- **Root Directory:** (boş bırakın)

**Build & Deploy Ayarları:**

- **Runtime:** `Python 3`
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  gunicorn app:app --bind 0.0.0.0:$PORT
  ```

**Plan:**

- **Free** planını seçin (ücretsiz)

### 3.4. Environment Variables (Gerekirse)

Şu an için gerekmez, boş bırakabilirsiniz.

### 3.5. Oluştur

1. **"Create Web Service"** butonuna tıklayın
2. Deployment otomatik başlayacak! 🎉

---

## ⏳ ADIM 4: Deployment Bekleme

1. Render.com deployment sayfasında bekleyin
2. **"Building"** aşaması 2-5 dakika sürebilir
3. **"Live"** yazısı göründüğünde hazır!

**✅ Uygulamanız canlıda!**

---

## 🌍 ADIM 5: Uygulamanızı Kullanma

1. Render.com dashboard'da web servisinize tıklayın
2. Üstte **URL** göreceksiniz: `https://heic-to-jpg.onrender.com` gibi
3. Bu URL'ye tıklayın veya tarayıcıda açın
4. **HEIC to JPG uygulamanız çalışıyor!** 🎊

---

## 🔄 Güncelleme

Kodunuzu güncellediğinizde:

```bash
cd C:\Users\90536\Desktop\heictojpg
git add .
git commit -m "Update"
git push
```

Render.com otomatik olarak yeniden deploy edecek!

---

## ⚠️ Önemli Notlar

1. **Ücretsiz Plan:**
   - 15 dakika kullanılmazsa uyku moduna geçer
   - İlk açılış 30-60 saniye sürebilir
   - Aylık 750 saat ücretsiz

2. **Dosya Boyutu:**
   - 100MB limit (uygulama ayarında)

3. **SSL:**
   - Otomatik HTTPS (güvenli bağlantı)

---

## 🐛 Sorun Giderme

### "Build failed" Hatası

1. **"Logs"** sekmesine bakın
2. Hata mesajını okuyun
3. Genellikle `requirements.txt` eksik veya yanlış

### "Application error" Hatası

1. **"Logs"** sekmesine bakın
2. Hata mesajını kontrol edin
3. Genellikle `app.py` veya import hatası

### Uygulama Açılmıyor

1. Birkaç dakika bekleyin (ilk deployment biraz zaman alabilir)
2. **"Logs"** sekmesinde hata var mı kontrol edin

---

## ✅ Avantajlar

- ✅ PythonAnywhere'den çok daha kolay
- ✅ Otomatik deployment
- ✅ GitHub entegrasyonu
- ✅ Ücretsiz SSL
- ✅ Modern arayüz
- ✅ Kolay güncelleme

**Başarılar!** 🚀

