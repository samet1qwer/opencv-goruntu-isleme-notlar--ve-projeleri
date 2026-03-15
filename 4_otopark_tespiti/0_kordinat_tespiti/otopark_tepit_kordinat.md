# 🖱️ Otopark Koordinat Tespiti Aracı

Fare tıklamalarıyla otopark görselindeki park alanlarının konumlarını işaretleyip kaydeden interaktif araç.

---

## 📸 Ne Yapar?

Bu program bir otopark görselini (`otopark.png`) açar ve üzerine fare ile tıklanmasını bekler. **Sol tık** ile yeni park yeri eklenir, **sağ tık** ile son eklenen park yeri silinir. Her tıklamadan sonra koordinatlar otomatik olarak `cordinates` dosyasına kaydedilir. Program kapatılıp yeniden açıldığında önceki koordinatlar kaldığı yerden devam eder. Bu araçla kaydedilen koordinatlar, otopark doluluk tespiti (`1_doluluk_tespiti`) kodunda kullanılır.

---

## 🗂️ Proje İçindeki Yeri

Bu kod iki aşamalı sistemin **1. aşamasıdır:**

```
proje/
│
├── 0_kordinat_tespiti/        ← ŞU AN BU KOD
│   ├── koordinat_tespiti.py   → fare ile park yerlerini işaretler
│   ├── otopark.png            → üzerine tıklanacak otopark görseli
│   └── cordinates             → kaydedilen koordinatlar (otomatik oluşur)
│
└── 1_doluluk_tespiti/
    ├── main.py                → kaydedilen koordinatları kullanarak doluluk tespiti yapar
    └── video.mp4              → analiz edilecek otopark videosu
```

**Çalışma sırası:**

1. Bu kod çalıştırılır → park yerleri fare ile işaretlenir → `cordinates` dosyası oluşur
2. `1_doluluk_tespiti/main.py` çalıştırılır → bu koordinatlar yüklenerek video analizi yapılır

---

## 🧰 Kullanılan Kütüphaneler

| Kütüphane      | Ne İçin Kullanılıyor?                                                     |
| -------------- | ------------------------------------------------------------------------- |
| `cv2` (OpenCV) | Görseli açma, fare olaylarını dinleme, dikdörtgen çizme, pencere yönetimi |
| `pickle`       | Koordinat listesini dosyaya kaydetme ve dosyadan okuma                    |

### Kurulum

```bash
pip install opencv-python
```

> `pickle` Python'ın standart kütüphanesinde gelir, kurulum gerekmez.

---

## 🖱️ Kullanım

| İşlem               | Tuş / Tıklama | Sonuç                                          |
| ------------------- | ------------- | ---------------------------------------------- |
| Park yeri ekle      | **Sol tık**   | Tıklanan konuma kırmızı dikdörtgen eklenir     |
| Son park yerini sil | **Sağ tık**   | En son eklenen koordinat silinir               |
| Programdan çık      | **q** tuşu    | Pencere kapanır, koordinatlar kaydedilmiş olur |

---

## 📄 Kodun Tamamı

```python
import cv2
import pickle

width = 27
height = 15

try:
    with open("cordinates", "rb") as f:
        cordinates = pickle.load(f)
except:
    cordinates = []

def mause_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        cordinates.append((x, y))
        print(cordinates)
    if event == cv2.EVENT_RBUTTONDOWN:
        cordinates.pop()
        print(cordinates)
    with open("cordinates", "wb") as f:
        pickle.dump(cordinates, f)

while True:
    img = cv2.imread("otopark.png")

    cv2.namedWindow("Otopark Tespiti")
    cv2.setMouseCallback("Otopark Tespiti", mause_click)

    for cord in cordinates:
        cv2.rectangle(img, cord, (cord[0] + width, cord[1] + height), (0, 0, 255), 2)

    cv2.imshow("Otopark Tespiti", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
```

---

## 🔍 Satır Satır Açıklama

### 1. Kütüphane İmportları

```python
import cv2
```

OpenCV kütüphanesini projeye dahil eder. Görseli diskten okuma, fare olaylarını dinleme, dikdörtgen çizme ve pencere açma işlemlerinin tümü bu kütüphane üzerinden yapılır.

```python
import pickle
```

Python nesnelerini (liste, sözlük, sınıf vb.) olduğu gibi dosyaya yazıp geri okumayı sağlayan standart kütüphane. Bu kodda koordinat listesini (`cordinates`) diske kaydetmek ve geri yüklemek için kullanılır.

---

### 2. Park Yeri Boyutları

```python
width = 27
height = 15
```

Her park alanı dikdörtgeninin piksel cinsinden **genişliği** ve **yüksekliği**. Fare ile tıklandığında sadece sol üst köşe kaydedilir; dikdörtgenin sağ alt köşesi bu iki değer kullanılarak hesaplanır:

- Sol üst köşe: `(x, y)` → tıklanan nokta
- Sağ alt köşe: `(x + 27, y + 15)` → hesaplanan nokta

**Bu değerler nereden geliyor?** Otopark görselinde bir park yeri ölçülerek piksel cinsinden belirlenir. Farklı kamera yüksekliği veya açısı için bu değerlerin değiştirilmesi gerekir. Doluluk tespiti kodunda da aynı `width` ve `height` değerleri kullanılmalıdır, aksi halde kesilen alan hatalı olur.

---

### 3. Koordinatları Diskten Yükleme (try-except)

```python
try:
    with open("cordinates", "rb") as f:
        cordinates = pickle.load(f)
except:
    cordinates = []
```

Bu blok programın **önceki çalışmadan kaldığı yerden devam etmesini** sağlar.

```python
try:
```

İçindeki kodu çalıştırmayı dene. Eğer herhangi bir hata oluşursa `except` bloğuna geç.

```python
    with open("cordinates", "rb") as f:
```

- `open("cordinates", "rb")` → `cordinates` adlı dosyayı **ikili okuma** (`rb` = read binary) modunda aç
- `"rb"` kullanılması zorunlu: pickle dosyaları metin değil binary (ikili) formatta saklanır, `"r"` ile açılsaydı hata verilirdi
- `with` bloğu → işlem bitince dosyayı otomatik kapatır, `f.close()` yazmak gerekmez

```python
        cordinates = pickle.load(f)
```

Dosyadaki binary veriyi Python listesine geri dönüştürür. Önceki çalışmada kaydedilen `[(x1,y1), (x2,y2), ...]` listesi aynen geri yüklenir.

```python
except:
    cordinates = []
```

Eğer `try` bloğu hata verirse (örneğin dosya henüz hiç oluşturulmamışsa — ilk çalıştırma) buraya düşer ve boş bir liste oluşturur. Program hata vermeden temiz başlar.

> 💡 **Tasarım kararı:** `except` içinde hata türü belirtilmemiş (örn. `except FileNotFoundError`). Bu pratik ama iyi bir alışkanlık değildir — beklenmedik hataları da susturur. Daha güvenli yazım: `except (FileNotFoundError, EOFError):`

---

### 4. Fare Tıklama Fonksiyonu

```python
def mause_click(event, x, y, flags, params):
```

OpenCV'nin fare olay sistemi için tanımlanan **callback (geri çağırma) fonksiyonu**. Bu fonksiyon doğrudan çağrılmaz — OpenCV, pencereye fare ile dokunulduğunda otomatik olarak çağırır.

Parametreler OpenCV tarafından otomatik gönderilir:

- `event` → ne tür bir fare olayı olduğu (tık, bırak, sürükle vb.)
- `x` → fare imlecinin **yatay** piksel konumu (sol köşe = 0)
- `y` → fare imlecinin **dikey** piksel konumu (üst köşe = 0)
- `flags` → tıklama sırasında basılı olan tuşlar (Shift, Ctrl vb.) — bu kodda kullanılmıyor
- `params` → `setMouseCallback`'e ekstra veri göndermek için — bu kodda kullanılmıyor

---

```python
    if event == cv2.EVENT_LBUTTONDOWN:
        cordinates.append((x, y))
        print(cordinates)
```

Eğer olay **sol fare tuşuna basılması** ise:

- `cv2.EVENT_LBUTTONDOWN` → Left Button Down (sol tuş basıldı)
- `cordinates.append((x, y))` → tıklanan noktanın koordinatını listeye ekle. `(x, y)` → tuple olarak kaydedilir
- `print(cordinates)` → güncel listeyi terminale yazdır (hangi koordinatların eklendiğini takip etmek için)

Diğer fare olayları:

| Sabit               | Açıklama                              |
| ------------------- | ------------------------------------- |
| `EVENT_LBUTTONDOWN` | Sol tuş basıldı ← bu kodda kullanılan |
| `EVENT_RBUTTONDOWN` | Sağ tuş basıldı ← bu kodda kullanılan |
| `EVENT_MOUSEMOVE`   | Fare hareket etti                     |
| `EVENT_LBUTTONUP`   | Sol tuş bırakıldı                     |
| `EVENT_MBUTTONDOWN` | Orta tuş (tekerlek) basıldı           |

---

```python
    if event == cv2.EVENT_RBUTTONDOWN:
        cordinates.pop()
        print(cordinates)
```

Eğer olay **sağ fare tuşuna basılması** ise:

- `cv2.EVENT_RBUTTONDOWN` → Right Button Down (sağ tuş basıldı)
- `cordinates.pop()` → listeden **son eklenen koordinatı** çıkar
  - `pop()` argümansız çağrılırsa listenin son elemanını siler ve döndürür
  - `pop(0)` yazılsaydı ilk eleman silinirdi
- Liste boşsa `pop()` hata verir! (`IndexError`) — bu kodda kontrol yok, dikkatli olunmalı

> ⚠️ **Güvenli yazım:**
>
> ```python
> if cordinates:   # Liste boş değilse
>     cordinates.pop()
> ```

---

```python
    with open("cordinates", "wb") as f:
        pickle.dump(cordinates, f)
```

Her fare tıklamasından (sol veya sağ) **hemen sonra** koordinat listesini diske kaydeder.

- `open("cordinates", "wb")` → dosyayı **ikili yazma** (`wb` = write binary) modunda aç. Dosya yoksa oluşturulur, varsa üzerine yazılır.
- `pickle.dump(cordinates, f)` → `cordinates` listesini binary formata çevirir ve dosyaya yazar.

**Neden her tıklamada kaydediliyor?** Program herhangi bir anda kapanırsa (hata, güç kesintisi) koordinatlar kaybolmaz. `q` tuşuna basmadan pencere kapatılsa bile son durum güvendedir.

**`"wb"` ve `"rb"` farkı:**

| Mod    | Açıklama      | Ne Zaman Kullanılır?     |
| ------ | ------------- | ------------------------ |
| `"rb"` | Read Binary   | Dosyadan okurken         |
| `"wb"` | Write Binary  | Dosyaya yazarken         |
| `"ab"` | Append Binary | Dosyanın sonuna eklerken |

---

### 5. Ana Döngü

```python
while True:
```

Program `q` tuşuna basılana kadar sonsuza döner. Her döngü adımı: görseli yeniden yükle → koordinatları çiz → ekranda göster.

---

```python
    img = cv2.imread("otopark.png")
```

Her döngüde görsel **diskten yeniden yüklenir**. Bu biraz verimsiz görünse de önemli bir nedeni vardır: `cv2.rectangle()` doğrudan `img` üzerine çizim yapar (destructive). Döngünün başında temiz görsel yüklenirse önceki dikdörtgenler silinmiş olur ve koordinat listesine göre tüm dikdörtgenler baştan çizilir. Böylece silme işlemi (sağ tık) anında yansır.

> 💡 Alternatif: `img_copy = img.copy()` ile her döngüde orijinalin kopyasına çizmek daha verimli olurdu — disk erişimi yerine bellekten kopya alınır.

---

```python
    cv2.namedWindow("Otopark Tespiti")
```

**"Otopark Tespiti"** adında bir OpenCV penceresi oluşturur. Bu satır döngü içinde her tekrarda çalışıyor ama OpenCV aynı isimde pencere zaten varsa yeni pencere açmaz, mevcut olanı kullanır. Teknik olarak döngü dışına alınabilirdi.

---

```python
    cv2.setMouseCallback("Otopark Tespiti", mause_click)
```

**"Otopark Tespiti"** penceresine fare olaylarını dinleyecek fonksiyonu bağlar.

- 1. parametre: hangi pencereyi dinleyeceği → `namedWindow`'daki isimle tam eşleşmeli!
- 2. parametre: olay olduğunda çağrılacak fonksiyon → `mause_click`

Bu satırdan sonra pencereye yapılan her fare hareketi/tıklaması otomatik olarak `mause_click` fonksiyonunu tetikler. Bu tasarıma **event-driven programming** (olay güdümlü programlama) denir.

---

```python
    for cord in cordinates:
        cv2.rectangle(img, cord, (cord[0] + width, cord[1] + height), (0, 0, 255), 2)
```

Kayıtlı her koordinat için görsel üzerine kırmızı dikdörtgen çizer.

```python
    for cord in cordinates:
```

`cordinates` listesindeki her `(x, y)` koordinatı sırayla `cord` değişkenine alır.

```python
        cv2.rectangle(img, cord, (cord[0] + width, cord[1] + height), (0, 0, 255), 2)
```

Dikdörtgen çizme parametreleri:

- `img` → üzerine çizilecek görüntü
- `cord` → sol üst köşe `(x, y)` → tıklanan nokta
- `(cord[0] + width, cord[1] + height)` → sağ alt köşe → `(x + 27, y + 15)`
- `(0, 0, 255)` → BGR kırmızı renk
- `2` → çizgi kalınlığı (piksel)

> Doluluk tespiti kodunda `color` değişkeni yeşil veya kırmızı oluyordu. Burada hepsi kırmızı — çünkü bu aşamada doluluk bilgisi yok, sadece konum işaretleniyor.

---

```python
    cv2.imshow("Otopark Tespiti", img)
```

İşlenmiş görüntüyü (üzerine kırmızı dikdörtgenler çizilmiş) "Otopark Tespiti" penceresinde gösterir. Her döngüde görüntü yenilendiği için tıklamalar anlık yansır.

---

```python
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

Her karede klavye girdisini dinler:

- `cv2.waitKey(1)` → 1 milisaniye bekle. OpenCV'nin pencereyi render etmesi ve fare olaylarını işlemesi için zorunludur.
- `& 0xFF` → Bit maskeleme: platformdan bağımsız güvenilir tuş kodu almak için.
- `ord("q")` → `q` harfinin ASCII kodu olan `113`.
- `q` basılırsa `break` → döngü kırılır → program sonlanır.

---

```python
cv2.destroyAllWindows()
```

Tüm OpenCV pencerelerini kapatır ve ekran belleğini temizler. Döngü kırıldıktan sonra çalışır.

---

## 🔄 Programın Genel Akışı

```
Başla
  │
  ├─► width=27, height=15 tanımla
  │
  ├─► cordinates dosyası var mı?
  │     ├─ VAR   → pickle ile yükle → cordinates = [(x1,y1), (x2,y2), ...]
  │     └─ YOK   → boş liste oluştur → cordinates = []
  │
  └─► DÖNGÜ (sonsuz)
        │
        ├─► otopark.png'yi diskten yükle (temiz görüntü)
        ├─► Pencereyi oluştur / fare callback'ini bağla
        │
        ├─► Kayıtlı her koordinat için:
        │     └─ Kırmızı dikdörtgen çiz
        │
        ├─► Görüntüyü ekranda göster
        │
        ├─► Fare tıklaması var mı? (OpenCV otomatik dinler)
        │     ├─ SOL TIK  → koordinat ekle → dosyaya kaydet
        │     └─ SAĞ TIK  → son koordinatı sil → dosyaya kaydet
        │
        └─► Q tuşuna basıldı mı?
              ├─ EVET → Döngüden çık
              └─ HAYIR → Döngünün başına dön

Pencereleri kapat (destroyAllWindows)
Bitir
```

---

## 💾 Koordinat Dosyası Yapısı

`cordinates` dosyası pickle formatında bir Python listesi içerir:

```python
# İçerik örneği (pickle ile okunduğunda)
[
    (45, 120),    # 1. park yeri sol üst köşe (x=45, y=120)
    (73, 120),    # 2. park yeri
    (101, 120),   # 3. park yeri
    (45, 138),    # 4. park yeri (bir alt sıra)
    ...
]
```

Her eleman bir park yerinin **sol üst köşe koordinatıdır**. Sağ alt köşe çizim sırasında `(x + width, y + height)` ile hesaplanır.

---

## 🔀 İki Kod Arasındaki İlişki

| Özellik                 | Bu Kod (Koordinat Tespiti)        | Doluluk Tespiti                    |
| ----------------------- | --------------------------------- | ---------------------------------- |
| Girdi                   | `otopark.png` (tek görsel)        | `video.mp4` (video akışı)          |
| `cordinates` ile ilişki | **Yazar** (`pickle.dump`)         | **Okur** (`pickle.load`)           |
| İşlem                   | Fare tıklaması → koordinat kaydet | Her kare → koordinatları analiz et |
| Çıktı                   | `cordinates` dosyası              | Ekranda boş/dolu gösterimi         |
| Kullanıcı etkileşimi    | Var (fare tıklaması)              | Yok (otomatik)                     |
| `width` / `height`      | Dikdörtgen çizmek için            | Park alanını kırpmak için          |

> ⚠️ **Kritik:** Her iki kodda da `width = 27` ve `height = 15` değerleri **aynı olmalıdır**. Koordinat tespitinde farklı bir boyut kullanılırsa doluluk tespiti yanlış piksel bölgesini analiz eder.

---

## ⚠️ Sık Karşılaşılan Sorunlar

| Sorun                      | Olası Neden                                                        | Çözüm                                                |
| -------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------- |
| `otopark.png` bulunamadı   | Dosya farklı klasörde                                              | Dosyayı aynı dizine taşı veya tam yol yaz            |
| Sağ tıkta `IndexError`     | Liste boşken `pop()` çağrıldı                                      | `if cordinates: cordinates.pop()` ile kontrol ekle   |
| Tıklama çalışmıyor         | `namedWindow` ile `setMouseCallback` isimleri eşleşmiyor           | Her ikisinde de aynı string kullanıldığından emin ol |
| Koordinatlar kaydedilmiyor | `pickle.dump` yazma hatası                                         | Klasör yazma iznini kontrol et                       |
| Dikdörtgenler görünmüyor   | `cordinates` listesi boş                                           | Sol tıkla koordinat eklediğinden emin ol             |
| Program çöküyor            | `ret` kontrolü yok (bu kodda `imread` kullanıldığı için sorun yok) | —                                                    |
