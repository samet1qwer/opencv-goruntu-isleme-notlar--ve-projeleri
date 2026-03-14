# 👁️ OpenCV Görüntü İşleme — Notlar & Projeler

> OpenCV kullanarak görüntü işleme öğrenirken çıkardığım notlar ve geliştirdiğim örnek projeler.

---

## 📖 Repo Hakkında

Bu repo, Python ile görüntü işleme öğrenme sürecimde tuttuğum detaylı notları ve bu notları pekiştirmek için geliştirdiğim küçük projeleri içeriyor. Her konu kendi klasöründe, her satır açıklamalı README dosyasıyla belgelenmiş.

> 🤖 Bu repodaki notlar ve README dosyaları [Claude](https://claude.ai) (Anthropic) yapay zekası yardımıyla düzenlenmiş ve belgelenmiştir. Kodlar tarafımdan yazılmış, açıklamalar ve dokümantasyon Claude ile birlikte hazırlanmıştır.

---

## 🗂️ İçerik

### 📚 Notlar

| Konu | Açıklama |
|---|---|
| [NumPy](0_genel_notlar/ders_notlari.md#1-numpy--temel-dizi-i̇şlemleri) | Array oluşturma, reshape, matematiksel işlemler |
| [Pandas](0_genel_notlar/ders_notlari.md#2-pandas--veri-analizi) | DataFrame, filtreleme, gruplama, CSV |
| [Matplotlib](0_genel_notlar/ders_notlari.md#3-matplotlib--grafik-ve-görselleştirme) | Grafik çizimi, görüntü gösterme |
| [OpenCV — Temel İşlemler](0_genel_notlar/ders_notlari.md#4-opencv--resim-okuma-ve-kaydetme) | Resim okuma, kaydetme, boyutlandırma |
| [OpenCV — Çizim](0_genel_notlar/ders_notlari.md#6-opencv--şekil-ve-metin-çizme) | Çizgi, dikdörtgen, çember, metin |
| [OpenCV — Video](0_genel_notlar/ders_notlari.md#9-opencv--video-okuma-ve-oynatma) | Video okuma, kamera, kayıt |
| [OpenCV — Blur](0_genel_notlar/ders_notlari.md#11-opencv--görüntü-bulanıklaştırma-blur) | Ortalama, Gaussian, Medyan blur |
| [OpenCV — Threshold](0_genel_notlar/ders_notlari.md#12-opencv--görüntü-eşikleme-thresholding) | Basit ve adaptif eşikleme |
| [OpenCV — Kenar Tespiti](0_genel_notlar/ders_notlari.md#13-opencv--kenar-bulma-edge-detection) | Sobel, Laplacian |
| [OpenCV — Morfoloji](0_genel_notlar/ders_notlari.md#14-opencv--morfolojik-i̇şlemler) | Erosion, Dilation, Opening, Closing |
| [OpenCV — Histogram](0_genel_notlar/ders_notlari.md#15-opencv--histogram-i̇şlemleri) | Histogram hesaplama, equalization |
| [OpenCV — Perspektif](0_genel_notlar/ders_notlari.md#16-opencv--perspektif-düzeltme) | Belge/kart düzeltme |
| [OS Modülü](0_genel_notlar/ders_notlari.md#17-os-modülü--dosya-ve-klasör-i̇şlemleri) | Dosya ve klasör işlemleri |

### 🚀 Projeler

| Proje | Klasör | Açıklama | README |
|---|---|---|---|
| 🖐️ El Takibi | `1_el_takibi` | MediaPipe ile gerçek zamanlı el iskelet tespiti | [README](1_el_takibi/el_takip.md) |
| 🧍 Poz Kestirimi | `2_poz_kestirimi/0_poz_kestirimi` | MediaPipe Pose ile 33 vücut noktası tespiti | [README](2_poz_kestirimi/0_poz_kestirimi/poz_kestirimi.md) |
| 🧍‍♂️ Poz Kestirimi Uygulama | `2_poz_kestirimi/1_poz_kestirimi_uygulama` | Video üzerinde poz kestirimi uygulaması | [README](2_poz_kestirimi/1_poz_kestirimi_uygulama/poz_kestirimi_uygulama.md) |
| 😶 Yüz Tespiti | `3_yuz_tespiti/0_yuz_tespiti` | MediaPipe FaceMesh ile 468 yüz noktası | [README](3_yuz_tespiti/0_yuz_tespiti/yuz_tespiti.md) |
| 😶‍🌫️ Yüz Tespiti Uygulama | `3_yuz_tespiti/1_yuz_tespiti_uygulama` | Yüz ağı + bounding box + göz kırpma sayacı | [README](3_yuz_tespiti/1_yuz_tespiti_uygulama/yuz_tespiti_uygulama.md) |

---

## 📁 Klasör Yapısı

```
opencv-goruntu-isleme-notlar--ve-projeleri/
│
├── 0_genel_notlar/
│   └── ders_notlari.md                      # NumPy, Pandas, Matplotlib ve OpenCV temel notları
│
├── 1_el_takibi/
│   ├── el_takip.py                          # El takibi kaynak kodu
│   └── el_takip.md                          # Satır satır açıklamalı README
│
├── 2_poz_kestirimi/
│   ├── 0_poz_kestirimi/
│   │   ├── poz_kestirimi.py                 # Temel poz kestirimi (kamera)
│   │   └── poz_kestirimi.md                 # Satır satır açıklamalı README
│   │
│   └── 1_poz_kestirimi_uygulama/
│       ├── poz_kestirimi_uygulama.py        # Video üzerinde poz kestirimi
│       ├── poz_kestirimi_uygulama.md        # Satır satır açıklamalı README
│       └── video.mp4                        # Test videosu
│
├── 3_yuz_tespiti/
│   ├── 0_yuz_tespiti/
│   │   ├── yuz_tespiti.py                   # Temel yüz ağı tespiti
│   │   └── yuz_tespiti.md                   # Satır satır açıklamalı README
│   │
│   └── 1_yuz_tespiti_uygulama/
│       ├── yuz_tespiti_uygulama.py          # Bounding box + göz kırpma sayacı
│       └── yuz_tespiti_uygulama.md          # Satır satır açıklamalı README
│
└── README.md                                ← şu an buradasın
```

---

## 🛠️ Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip

### Kütüphaneleri Yükle

```bash
pip install opencv-python mediapipe numpy pandas matplotlib
```

### Repoyu Klonla

```bash
git clone https://github.com/samet1qwer/opencv-goruntu-isleme-notlar--ve-projeleri.git
cd opencv-goruntu-isleme-notlar--ve-projeleri
```

---

## 💻 VSCode ile Kullanım

Bu repodaki tüm notlar **Markdown** (`.md`) formatında yazılmıştır. VSCode, Markdown dosyalarını hem düz metin hem de güzel biçimlendirilmiş önizleme olarak gösterebilir.

### Markdown Önizlemeyi Açma

**Yöntem 1 — Sağ Tık Menüsü:**
1. Sol panelde istediğin `.md` dosyasına **sağ tık** yap
2. `Open Preview` seçeneğine tıkla

**Yöntem 2 — Klavye Kısayolu:**
1. `.md` dosyasını aç
2. `Ctrl + Shift + V` (Windows/Linux) veya `Cmd + Shift + V` (Mac) kısayoluna bas

**Yöntem 3 — Yan Yana Görünüm (Tavsiye Edilen):**
1. `.md` dosyasını aç
2. Editörün **sağ üst köşesindeki** kitap ikonu olan **"Open Preview to the Side"** butonuna tıkla
3. Sol tarafta Markdown kodu, sağ tarafta canlı önizleme yan yana açılır

> 💡 Yan yana görünüm en kullanışlı olandır — kodu düzenlerken önizleme anlık güncellenir.

---

### Önerilen VSCode Eklentileri

Daha iyi bir deneyim için şu eklentileri yüklemenizi öneririm:

**1. Markdown All in One** — `yzhang.markdown-all-in-one`
- Markdown yazımını kolaylaştırır, içindekiler tablosunu otomatik oluşturur

**2. Markdown Preview Enhanced** — `shd101wyy.markdown-preview-enhanced`
- Daha gelişmiş ve özelleştirilebilir önizleme sunar

**3. Python** — `ms-python.python`
- Python söz dizimi renklendirme ve IntelliSense (otomatik tamamlama)

**4. Pylance** — `ms-python.vscode-pylance`
- Gelişmiş Python dil desteği ve tip kontrolü

Eklenti yüklemek için:
1. `Ctrl + Shift + X` ile **Extensions** panelini aç
2. Arama kutusuna eklenti adını yaz
3. `Install` butonuna bas

---

### Python Kodlarını Çalıştırma

**Yöntem 1 — Terminal ile:**
```bash
# VSCode terminalini aç: Ctrl + ` (backtick tuşu)

# El takibini çalıştır
cd 1_el_takibi
python el_takip.py

# Poz kestirimi çalıştır
cd 2_poz_kestirimi/0_poz_kestirimi
python poz_kestirimi.py

# Poz kestirimi uygulama çalıştır
cd 2_poz_kestirimi/1_poz_kestirimi_uygulama
python poz_kestirimi_uygulama.py

# Yüz tespiti çalıştır
cd 3_yuz_tespiti/0_yuz_tespiti
python yuz_tespiti.py

# Yüz tespiti uygulama çalıştır
cd 3_yuz_tespiti/1_yuz_tespiti_uygulama
python yuz_tespiti_uygulama.py
```

**Yöntem 2 — Run butonu ile:**
1. `.py` dosyasını aç
2. Sağ üst köşedeki ▶ **Run Python File** butonuna tıkla

**Yöntem 3 — Sağ Tık ile:**
1. Editörde herhangi bir yere sağ tık yap
2. `Run Python File in Terminal` seçeneğine tıkla

> ⚠️ Kamera kullanan projelerde kameranın başka bir uygulama tarafından kullanılmıyor olması gerekir. Çalışan programdan çıkmak için `q` tuşuna bas.

---

## 🧪 Projeler Hakkında Hızlı Bilgi

### 🖐️ El Takibi — `1_el_takibi`
MediaPipe'ın `Hands` modeli ile elde **21 eklem noktası** tespit ederek iskelet çizer. Gerçek zamanlı çalışır, birden fazla eli aynı anda takip edebilir.

### 🧍 Poz Kestirimi — `2_poz_kestirimi/0_poz_kestirimi`
MediaPipe'ın `Pose` modeli ile tüm vücutta **33 nokta** tespit eder. Omuz, dirsek, kalça, diz gibi anatomik noktaları işaretler. Baş noktası (ID: 0) mavi daire ile ayrıca vurgulanır.

### 🧍‍♂️ Poz Kestirimi Uygulama — `2_poz_kestirimi/1_poz_kestirimi_uygulama`
Poz kestirimi modelinin canlı kamera yerine bir **video dosyası** (`video.mp4`) üzerinde çalıştırıldığı uygulama versiyonu.

### 😶 Yüz Tespiti — `3_yuz_tespiti/0_yuz_tespiti`
MediaPipe'ın `FaceMesh` modeli ile yüzde **468 nokta** tespit eder. Göz, kaş, dudak, burun ve yüz oval kontür çizgileri çizilir.

### 😶‍🌫️ Yüz Tespiti Uygulama — `3_yuz_tespiti/1_yuz_tespiti_uygulama`
Yüz tespiti projesinin geliştirilmiş versiyonu. Her noktaya **mavi daire** çizilir, 468 noktanın `min/max` koordinatlarından yüzün etrafına **yeşil bounding box** eklenir ve **EAR (Eye Aspect Ratio)** algoritmasıyla göz kırpma sayılır.

---

## 📌 Notlar Nasıl Okunmalı?

`0_genel_notlar/ders_notlari.md` dosyası kendi içinde ayrıntılı bir içindekiler tablosu içeriyor. Sırasıyla baştan sona okuyabilir ya da VSCode'da `Ctrl + F` ile anahtar kelime arayabilirsin.

Her kod bloğu şu yapıda yazılmıştır:

```python
sonuc = cv2.birFonksiyon(parametre1, parametre2)
# parametre1 → ne işe yarıyor
# parametre2 → ne işe yarıyor
# neden bu fonksiyon kullanıldı
# dikkat edilmesi gereken nokta
```

---

## 🤝 Katkı

Bu repo kişisel öğrenme notlarından oluşuyor. Hata fark edersen veya eklemek istediğin bir şey varsa **issue** açabilir ya da **pull request** gönderebilirsin.

---

<div align="center">

**⭐ Faydalı bulduysan repoyu yıldızlamayı unutma!**

</div>
