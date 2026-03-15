# 🅿️ Akıllı Otopark Doluluk Tespiti

OpenCV ve görüntü işleme teknikleri kullanarak video üzerinden otopark alanlarının boş mu dolu mu olduğunu gerçek zamanlı tespit eden uygulama.

---

## 📸 Ne Yapar?

Bu program bir otopark videosunu kare kare analiz eder. Daha önceden koordinatları kaydedilmiş her park alanına bakar ve o alanın boş mu dolu mu olduğuna karar verir. Boş alanları **yeşil**, dolu alanları **kırmızı** dikdörtgenle işaretler. Ekranın sol üst köşesinde anlık olarak kaç alanın boş olduğunu gösterir. Video bittiğinde otomatik olarak başa sarar ve döngü halinde oynatmaya devam eder.

---

## 🗂️ Proje Yapısı

Bu kod tek başına çalışmaz. İki aşamalı bir sistemin parçasıdır:

```
proje/
│
├── 0_kordinat_tespiti/       ← 1. AŞAMA (önce bu çalışır)
│   ├── koordinat_tespiti.py  → park alanı köşelerini fare ile seçip kaydeder
│   └── cordinates            → pickle ile kaydedilmiş koordinat listesi
│
└── 1_doluluk_tespiti/        ← 2. AŞAMA (bu kod)
    ├── main.py               → koordinatları okuyup doluluk tespiti yapar
    └── video.mp4             → analiz edilecek otopark videosu
```

**Çalışma sırası:**

1. Önce `0_kordinat_tespiti` klasöründeki kod çalıştırılır → fare ile her park yeri işaretlenir → `cordinates` dosyası oluşturulur.
2. Sonra bu kod (`main.py`) çalıştırılır → kaydedilen koordinatları okur → video üzerinde doluluk tespiti yapar.

---

## 🧰 Kullanılan Kütüphaneler

| Kütüphane      | Ne İçin Kullanılıyor?                                 |
| -------------- | ----------------------------------------------------- |
| `cv2` (OpenCV) | Video okuma, görüntü işleme, dikdörtgen ve yazı çizme |
| `numpy`        | Kernel matrisi oluşturma (morfolojik işlem için)      |
| `pickle`       | Koordinat dosyasını diskten okuma                     |

### Kurulum

```bash
pip install opencv-python
pip install numpy
```

> `pickle` Python'ın standart kütüphanesinde gelir, ayrıca kurulum gerekmez.

---

## 📄 Kodun Tamamı

```python
import cv2
import numpy as np
import pickle

width = 27
height = 15

video = cv2.VideoCapture("video.mp4")

with open("../0_kordinat_tespiti/cordinates", "rb") as f:
    cordinates = pickle.load(f)

def check_park(img, original):
    space_counter = 0
    for pos in cordinates:
        crop_img = img[pos[1]:pos[1] + height, pos[0]:pos[0] + width]
        count = cv2.countNonZero(crop_img)

        if count < 150:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(original, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cv2.putText(original, str(count), (pos[0], pos[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    return space_counter


while True:
    ret, frame = video.read()

    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    img_gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur   = cv2.GaussianBlur(img_gray, (7, 7), 0)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_thresh, 5)
    kernel     = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    free_spaces = check_park(img_dilate, frame)
    total_spaces = len(cordinates)

    cv2.rectangle(frame, (0, 0), (220, 50), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, f"Bos: {free_spaces} / {total_spaces}",
                (1, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.1,
                (0, 255, 0) if free_spaces > 0 else (0, 0, 255), 2)

    cv2.imshow("Otopark", frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
```

---

## 🔍 Satır Satır Açıklama

### 1. Kütüphane İmportları

```python
import cv2
```

OpenCV kütüphanesini projeye dahil eder. Video okuma, gri dönüşüm, bulanıklaştırma, eşikleme, morfolojik işlemler ve ekranda şekil çizme işlemlerinin tümü bu kütüphane üzerinden yapılır.

```python
import numpy as np
```

Sayısal işlemler kütüphanesi. Bu kodda sadece morfolojik genişleme (dilation) için gereken kernel matrisini oluşturmak amacıyla kullanılır.

```python
import pickle
```

Python nesnelerini dosyaya yazmaya ve dosyadan okumaya yarayan standart kütüphane. Önceden fare ile belirlenen park yeri koordinatları `pickle` ile kaydedilmiş, bu kod o dosyayı okuyarak koordinatları geri yükler.

---

### 2. Park Yeri Boyutları

```python
width = 27
height = 15
```

Her bir park alanının piksel cinsinden **genişliği** ve **yüksekliği**. Bu değerler sabittir çünkü tüm park yerleri aynı boyuttadır (yukarıdan sabit açıyla çekilmiş kamera görüntüsü).

**Bu değerler neden önemli?**

- Park koordinatı `pos = (x, y)` → sadece sol üst köşeyi verir
- Sağ alt köşeyi bulmak için: `(pos[0] + width, pos[1] + height)` hesaplanır
- `crop_img` kesmek için: `img[pos[1] : pos[1]+height, pos[0] : pos[0]+width]`

Kamera açısı veya park yeri boyutu değişirse bu değerlerin güncellenmesi gerekir.

---

### 3. Video Yükleme

```python
video = cv2.VideoCapture("video.mp4")
```

`video.mp4` dosyasını açar ve `video` nesnesine atar. Kamera yerine video dosyası kullanıldığı için `0` değil dosya adı verilmiş. Her döngüde `video.read()` ile bir sonraki kare okunacak.

---

### 4. Koordinatları Diskten Yükleme

```python
with open("../0_kordinat_tespiti/cordinates", "rb") as f:
    cordinates = pickle.load(f)
```

Bu bloğu satır satır açıklayalım:

```python
with open("../0_kordinat_tespiti/cordinates", "rb") as f:
```

- `open(dosya_yolu, mod)` → dosyayı açar
- `"../0_kordinat_tespiti/cordinates"` → bir üst klasöre çıkıp (`..`) oradan `0_kordinat_tespiti` klasörüne gir ve `cordinates` dosyasını aç
- `"rb"` → **r**ead **b**inary (ikili okuma modu). `pickle` dosyaları metin değil ikili (binary) formatta saklanır, bu yüzden `"r"` değil `"rb"` kullanılır
- `with` bloğu → dosya işlemi bitince otomatik olarak kapatır, `f.close()` yazmak gerekmez

```python
    cordinates = pickle.load(f)
```

- `pickle.load(f)` → açık dosyadan Python nesnesini okur ve orijinal haline geri döndürür
- `cordinates` → her eleman bir park yerinin `(x, y)` koordinatı olan liste. Örnek: `[(45, 120), (73, 120), (101, 120), ...]`

---

### 5. Park Doluluk Kontrol Fonksiyonu

```python
def check_park(img, original):
```

İki parametre alır:

- `img` → işlenmiş (gri + blur + threshold + dilate uygulanmış) görüntü — **doluluk kararı bu görüntüye bakılarak verilir**
- `original` → orijinal renkli kamera karesi — **dikdörtgenler ve yazılar bu görüntüye çizilir**

---

```python
    space_counter = 0
```

Boş park sayacını sıfırdan başlatır. Fonksiyon her çağrıldığında sıfırlanır ve o karedeki boş alan sayısı taze olarak hesaplanır.

---

```python
    for pos in cordinates:
```

Pickle'dan yüklenen koordinat listesindeki **her park yeri için** döngü başlatır. `pos` → o park yerinin sol üst köşe koordinatı: `(x, y)`.

---

```python
        crop_img = img[pos[1]:pos[1] + height, pos[0]:pos[0] + width]
```

İşlenmiş görüntüden o park yerine ait dikdörtgen bölgeyi keser (crop).

NumPy dilimleme söz dizimi: `img[y_başlangıç : y_bitiş, x_başlangıç : x_bitiş]`

- `pos[1]` → sol üst köşenin **y** koordinatı (satır başlangıcı)
- `pos[1] + height` → y + 15 → alt kenar
- `pos[0]` → sol üst köşenin **x** koordinatı (sütun başlangıcı)
- `pos[0] + width` → x + 27 → sağ kenar

Sonuç: 15×27 piksellik küçük bir görüntü parçası — sadece o park yerine ait alan.

---

```python
        count = cv2.countNonZero(crop_img)
```

Kesilen park alanı görüntüsündeki **sıfır olmayan (beyaz) piksel sayısını** sayar.

**Neden beyaz piksel sayısı karar verir?**

Görüntüye uygulanan işlemler (`THRESH_BINARY_INV` + dilate) sonucunda:

- **Boş park yeri** → düzgün, tek renkli zemin → az beyaz piksel → düşük `count`
- **Dolu park yeri** → araba kenarları, lastikler, gölgeler → çok beyaz piksel → yüksek `count`

Bu yüzden `count` değeri doluluk göstergesidir.

---

```python
        if count < 150:
            color = (0, 255, 0)    # BGR → Yeşil
            thickness = 5
            space_counter += 1
```

Eğer beyaz piksel sayısı **150'den az** ise park yeri **boş** demektir:

- Rengi yeşil yap
- Kalınlığı 5 yap (boş olduğu daha çok dikkat çeksin diye kalın)
- Boş sayacını 1 artır

**150 eşik değeri nereden geliyor?** Deneme-yanılma ile belirlenen pratik bir değer. Çok düşük olursa dolu alanlar da boş sayılır. Çok yüksek olursa boş alanlar dolu sayılır. Farklı kamera açıları veya aydınlatma koşulları için bu değer ayarlanmalıdır.

---

```python
        else:
            color = (0, 0, 255)    # BGR → Kırmızı
            thickness = 2
```

Eğer beyaz piksel sayısı **150 veya daha fazla** ise park yeri **dolu** demektir:

- Rengi kırmızı yap
- Kalınlığı 2 yap (ince çizgi, arka plan dolu arabaların görünmesini engellemesin)

---

```python
        cv2.rectangle(original, pos, (pos[0] + width, pos[1] + height), color, thickness)
```

**Orijinal renkli görüntüye** park yeri dikdörtgeni çizer.

- `original` → orijinal BGR kamera karesi (işlenmemiş, renkli)
- `pos` → sol üst köşe `(x, y)`
- `(pos[0] + width, pos[1] + height)` → sağ alt köşe `(x+27, y+15)`
- `color` → yeşil (boş) veya kırmızı (dolu)
- `thickness` → 5 (boş) veya 2 (dolu)

---

```python
        cv2.putText(original, str(count), (pos[0], pos[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
```

Her park alanının **üzerine beyaz piksel sayısını** küçük yazıyla yazar. Bu sayı debug/ayar amaçlıdır — eşik değerini (150) ayarlamak için hangi alanın kaç sayı verdiğini görmek gerekir.

- `str(count)` → sayıyı stringe çevir (putText metin ister)
- `(pos[0], pos[1] - 5)` → dikdörtgenin 5 piksel **üstüne** yaz (dikdörtgenin içine sığmasın diye)
- `0.4` → küçük font boyutu (alanlar küçük olduğu için)

---

```python
    return space_counter
```

Fonksiyonun sonunda o karedeki toplam boş alan sayısını döndürür. Ana döngüde `free_spaces` değişkenine atanacak.

---

### 6. Ana Video Döngüsü

```python
while True:
```

Video bitene (ve başa sarılana) kadar sonsuza döner. `q` tuşuyla çıkılır.

---

```python
    ret, frame = video.read()
```

Videodan bir sonraki kareyi okur:

- `ret` `(bool)` → okuma başarılı mı?
- `frame` `(ndarray)` → BGR formatında video karesi

---

```python
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
```

Video bittiğinde `ret = False` olur. Bu blok devreye girer:

- `video.set(cv2.CAP_PROP_POS_FRAMES, 0)` → videoyu **0. kareye** geri sarar (başa döner)
  - `cv2.CAP_PROP_POS_FRAMES` → "şu an hangi karedeyiz" özelliği
  - `0` → ilk kareye dön
- `continue` → döngünün geri kalanını atla, baştan başla → video baştan oynamaya devam eder

Böylece video bitmeden sürekli döngü halinde oynar. Park kamerası simülasyonu için idealdir.

---

### 7. Görüntü İşleme Pipeline'ı

Her kareye sırayla 5 işlem uygulanır. Bu işlemlerin amacı: renkli videoyu, arabanın varlığını sayıma dönüştürebilecek siyah-beyaz görüntüye çevirmek.

```python
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

**Adım 1 — Gri Dönüşüm:** Renkli (3 kanal BGR) görüntüyü tek kanallı gri görüntüye çevirir.

- Neden? Threshold ve countNonZero işlemleri tek kanallı görüntüde çalışır.
- Sonuç: `(yükseklik, genişlik)` boyutlu 2D dizi, her piksel 0-255 arası parlaklık değeri.

---

```python
    img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)
```

**Adım 2 — Gaussian Bulanıklaştırma:** Gri görüntüye Gaussian blur uygular.

- `(7, 7)` → 7×7 piksellik kernel (büyük kernel = daha fazla bulanıklık)
- `0` → sigma değeri, 0 yazılırsa kernel boyutundan otomatik hesaplanır
- Neden? Küçük gürültüleri ve ince dokuları yumuşatır. Sonraki eşikleme adımında gereksiz küçük detayların beyaz piksel olarak sayılmasını önler.

---

```python
    img_thresh = cv2.adaptiveThreshold(img_blur, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 25, 16)
```

**Adım 3 — Adaptif Eşikleme:** Bulanık gri görüntüyü siyah-beyaz (binary) görüntüye dönüştürür.

Parametreler:

- `img_blur` → giriş görüntüsü
- `255` → eşiği geçen piksele atanacak maksimum değer (beyaz)
- `cv2.ADAPTIVE_THRESH_GAUSSIAN_C` → her bölge için Gaussian ağırlıklı ortalama eşik hesapla
- `cv2.THRESH_BINARY_INV` → **ters binary**: koyu pikseller beyaz, açık pikseller siyah olur
- `25` → blok boyutu: her piksel için 25×25 komşuluk alanına bakılır (tek sayı olmalı)
- `16` → C sabiti: hesaplanan eşikten çıkarılan ince ayar değeri

**Neden `THRESH_BINARY_INV`?** Arabanın kenarları (lastikler, gövde çizgileri) koyu renktir. `INV` ile koyu → beyaz olur → `countNonZero` bu beyazları sayar → yüksek sayı = araba var.

**Neden adaptif?** Güneş ışığı, gölge, farklı zemin renkleri nedeniyle görüntünün farklı bölgelerinde aydınlatma değişir. Global bir eşik bazı bölgelerde çalışırken diğerlerinde başarısız olur. Adaptif threshold her bölge için ayrı eşik hesaplar.

---

```python
    img_median = cv2.medianBlur(img_thresh, 5)
```

**Adım 4 — Medyan Bulanıklaştırma:** Binary görüntüdeki küçük beyaz gürültü noktalarını temizler.

- `5` → 5×5 kernel (tek sayı olmalı)
- Neden medyan? Tuz-biber gürültüsüne (rastgele tek nokta beyaz/siyah pikseller) karşı çok etkilidir. Threshold sonrası görüntüde bu tür gürültü oluşur, medyan blur onu temizler.

---

```python
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)
```

**Adım 5 — Morfolojik Genişleme (Dilation):** Beyaz bölgeleri biraz büyütür.

- `np.ones((3, 3), np.uint8)` → tüm değerleri 1 olan 3×3 kare kernel
- `iterations=1` → işlemi 1 kez uygula
- Neden? Arabaların kenarları threshold sonrasında kesik kesik çizgiler halinde kalabilir. Dilation bu kesik çizgileri birleştirir, daha bütün ve belirgin bir yapı oluşturur. Bu da `countNonZero` sayısını daha tutarlı yapar.

---

### 8. Doluluk Tespitini Çalıştır

```python
    free_spaces = check_park(img_dilate, frame)
```

İşlenmiş görüntüyü (`img_dilate`) ve orijinal kareyi (`frame`) `check_park` fonksiyonuna gönderir.

- `img_dilate` → doluluk kararı için analiz edilecek
- `frame` → dikdörtgen ve yazılar bu görüntüye çizilecek
- `free_spaces` → fonksiyonun döndürdüğü boş alan sayısı

```python
    total_spaces = len(cordinates)
```

`cordinates` listesinin uzunluğu = toplam park alanı sayısı. Her çağrıda hesaplanıyor ama sabit bir değer — döngü dışına alınabilirdi.

---

### 9. Bilgi Kutusunu Çiz

```python
    cv2.rectangle(frame, (0, 0), (220, 50), (0, 0, 0), cv2.FILLED)
```

Sol üst köşeye **siyah dolgu dikdörtgen** çizer. Yazının arkasına kontrast sağlamak için arka plan oluşturur. Parametreler:

- `(0, 0)` → sol üst köşe (ekranın köşesi)
- `(220, 50)` → sağ alt köşe (220px geniş, 50px yüksek kutu)
- `(0, 0, 0)` → siyah renk
- `cv2.FILLED` → içi dolu (`-1` ile aynı)

---

```python
    cv2.putText(frame, f"Bos: {free_spaces} / {total_spaces}",
                (1, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.1,
                (0, 255, 0) if free_spaces > 0 else (0, 0, 255), 2)
```

Siyah kutunun üzerine boş/toplam park bilgisini yazar. Parametreler:

- `f"Bos: {free_spaces} / {total_spaces}"` → f-string ile dinamik metin. Örnek: `"Bos: 12 / 50"`
- `(1, 35)` → metnin sol-alt başlangıç noktası (kutunun içinde)
- `1.1` → font boyutu (büyük ve okunabilir)
- `(0, 255, 0) if free_spaces > 0 else (0, 0, 255)` → **ternary operatör**:
  - Boş yer **varsa** → yeşil yazı
  - Boş yer **yoksa** → kırmızı yazı (park tamamen doldu uyarısı)
- `2` → yazı kalınlığı

---

### 10. Görüntüyü Göster ve Çıkış Kontrolü

```python
    cv2.imshow("Otopark", frame)
```

İşlenmiş kareyi **"Otopark"** başlıklı pencerede gösterir. `frame` artık üzerinde renkli dikdörtgenler, piksel sayıları ve sol üstte boş/dolu bilgisi olan tam görüntüdür.

```python
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
```

- `cv2.waitKey(30)` → **30 milisaniye** bekle (diğer kodlarda 1 ms'di)
- Neden 30 ms? Video oynatma hızını kontrol eder. 30 ms bekleme → saniyede yaklaşık 33 kare (FPS) → normal video hızına yakın akıcı oynatma. `waitKey(1)` yazılsaydı video çok hızlı oynatılırdı.
- `& 0xFF == ord('q')` → `q` tuşuna basılırsa döngüden çık

---

### 11. Kaynakları Serbest Bırak

```python
video.release()
```

Video dosyasını kapatır ve sistem kaynaklarını serbest bırakır. Video dosyaları da kamera gibi `release()` ile kapatılmalıdır.

```python
cv2.destroyAllWindows()
```

Tüm OpenCV pencerelerini kapatır ve belleği temizler.

---

## 🔄 Programın Genel Akışı

```
Başla
  │
  ├─► Boyut değişkenlerini tanımla (width=27, height=15)
  ├─► video.mp4 dosyasını aç
  ├─► cordinates dosyasını pickle ile yükle
  │
  └─► DÖNGÜ (sonsuz)
        │
        ├─► Videodan kare oku (ret, frame)
        │
        ├─► Video bitti mi? (ret = False)
        │     ├─ EVET → Videoya başa sar → continue
        │     └─ HAYIR → Devam et
        │
        ├─► [İŞLEME PIPELINE'I]
        │     ├─ BGR → Gri
        │     ├─ Gaussian Blur (7×7)
        │     ├─ Adaptif Threshold (BINARY_INV)
        │     ├─ Medyan Blur (gürültü temizle)
        │     └─ Dilation (kenarları birleştir)
        │
        ├─► check_park() fonksiyonunu çalıştır
        │     └─ Her koordinat için:
        │           ├─ O alanı kırp (crop)
        │           ├─ Beyaz piksel say (countNonZero)
        │           ├─ count < 150 → BOŞ (yeşil, kalın)
        │           ├─ count ≥ 150 → DOLU (kırmızı, ince)
        │           └─ Dikdörtgen + sayı yaz
        │
        ├─► Sol üste siyah kutu çiz
        ├─► "Bos: X / Y" yaz (boşsa yeşil, doluysa kırmızı)
        ├─► Kareyi ekranda göster
        │
        └─► Q tuşuna basıldı mı?
              ├─ EVET → Döngüden çık
              └─ HAYIR → Döngünün başına dön

Video dosyasını kapat (release)
Pencereleri kapat (destroyAllWindows)
Bitir
```

---

## 🖼️ Görüntü İşleme Pipeline'ı Görsel

```
Orijinal Renkli Kare (BGR)
         │
         ▼
    cvtColor (BGR → GRAY)
         │  Renk bilgisi atıldı, tek kanal
         ▼
    GaussianBlur (7×7)
         │  Küçük gürültüler yumuşatıldı
         ▼
    adaptiveThreshold (BINARY_INV)
         │  Koyu pikseller beyaz, açık pikseller siyah
         ▼
    medianBlur (5×5)
         │  Tuz-biber gürültüsü temizlendi
         ▼
    dilate (3×3, 1 iter)
         │  Beyaz bölgeler genişletildi
         ▼
    check_park() → countNonZero → karar
```

---

## ⚙️ Ayarlanabilir Parametreler

| Parametre                | Mevcut Değer | Etkisi                                                       |
| ------------------------ | ------------ | ------------------------------------------------------------ |
| `width`                  | `27`         | Park yeri genişliği (piksel)                                 |
| `height`                 | `15`         | Park yeri yüksekliği (piksel)                                |
| `count < 150`            | `150`        | Boş/dolu eşik değeri — düşürülürse daha az yer boş sayılır   |
| `GaussianBlur (7,7)`     | `7×7`        | Büyütülürse daha fazla gürültü temizlenir ama detay kaybolur |
| `adaptiveThreshold` blok | `25`         | Büyütülürse daha geniş bölge ortalaması alınır               |
| `adaptiveThreshold` C    | `16`         | Artırılırsa daha az alan beyaz olur                          |
| `medianBlur`             | `5`          | Büyütülürse daha fazla gürültü temizlenir                    |
| `waitKey(30)`            | `30 ms`      | Azaltılırsa video hızlanır, artırılırsa yavaşlar             |

---

## 🚀 Geliştirme Fikirleri

- **Anlık istatistik kaydı:** Her dakika boş yer sayısını CSV'ye yazarak doluluk geçmişi tutulabilir.
- **Renk özelleştirme:** `draw_landmarks` yerine özel renkler ve stil belirlenerek görsel iyileştirme yapılabilir.
- **Sesli uyarı:** `free_spaces == 0` olduğunda `playsound` ile sesli bildirim verilebilir.
- **Web arayüzü:** Flask ile basit bir web sayfasına aktarılarak uzaktan izleme sağlanabilir.
- **Çoklu kamera:** Birden fazla `VideoCapture` nesnesi ile farklı otopark bölgeleri aynı anda izlenebilir.

---

## ⚠️ Sık Karşılaşılan Sorunlar

| Sorun                           | Olası Neden                                  | Çözüm                                             |
| ------------------------------- | -------------------------------------------- | ------------------------------------------------- |
| `cordinates` dosyası bulunamadı | Koordinat tespiti adımı atlandı              | Önce `0_kordinat_tespiti` kodunu çalıştır         |
| Tüm alanlar kırmızı gösteriyor  | Eşik değeri (150) çok düşük                  | `count < 150` değerini artır (örn: 200, 300)      |
| Tüm alanlar yeşil gösteriyor    | Eşik değeri çok yüksek                       | `count < 150` değerini azalt                      |
| Video çok hızlı/yavaş           | `waitKey` değeri uygun değil                 | `waitKey(30)` değerini ayarla                     |
| `video.mp4` bulunamadı          | Dosya yolu yanlış                            | Video dosyasının aynı klasörde olduğundan emin ol |
| Program çöküyor                 | `ret = False` ama devam edilmeye çalışılıyor | `if not ret` bloğunun doğru yazıldığından emin ol |
