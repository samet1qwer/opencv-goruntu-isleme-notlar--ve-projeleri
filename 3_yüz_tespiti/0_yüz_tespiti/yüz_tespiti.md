# 😶 Gerçek Zamanlı Yüz Ağı Tespiti + Bounding Box (Face Mesh)

MediaPipe ve OpenCV kullanarak kameradan canlı yüz tespiti, 468 yüz noktası işaretleme ve yüzün etrafına otomatik dikdörtgen çizme uygulaması.

---

## 📸 Ne Yapar?

Bu program bilgisayarın kamerasını açar, görüntüyü 400×400 piksel boyutuna getirir ve kare kare analiz eder. Ekranda gördüğü yüzün üzerine:

- 🔵 **468 adet mavi nokta** — her yüz eklem noktasına küçük daire
- 🕸️ **Yüz kontür çizgileri** — göz, kaş, dudak, burun ve yüz hatları
- 🟩 **Yeşil bounding box** — yüzün tamamını çevreleyen dikdörtgen

çizer. Program `q` tuşuna basılana kadar çalışır.

---

## 🧰 Kullanılan Kütüphaneler

| Kütüphane      | Ne İçin Kullanılıyor?                                                     |
| -------------- | ------------------------------------------------------------------------- |
| `cv2` (OpenCV) | Kamera açma, aynalama, boyutlandırma, daire ve dikdörtgen çizme, gösterme |
| `mediapipe`    | 468 noktalı yüz ağı tespiti (AI modeli)                                   |

### Kurulum

```bash
pip install opencv-python
pip install mediapipe
```

---

## 📄 Kodun Tamamı

```python
import cv2
import mediapipe as mp

width = 400
height = 400

vide_cam = cv2.VideoCapture(0)

mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh()
mp_draw = mp.solutions.drawing_utils

while True:
    ret, frame = vide_cam.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (width, height))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face.process(frame_rgb)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:

            mp_draw.draw_landmarks(
                frame,
                face_landmarks,
                mp_face.FACEMESH_CONTOURS
            )

            h, w, c = frame.shape

            x_list = []
            y_list = []

            for id, detection in enumerate(face_landmarks.landmark):
                cx, cy = int(detection.x * w), int(detection.y * h)

                x_list.append(cx)
                y_list.append(cy)

                cv2.circle(frame, (cx, cy), 2, (255, 0, 0), cv2.FILLED)

            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    cv2.imshow("Yuz Tanima", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

vide_cam.release()
cv2.destroyAllWindows()
```

---

## 🔍 Satır Satır Açıklama

### 1. Kütüphane İmportları

```python
import cv2
```

OpenCV kütüphanesini projeye dahil eder. Kamera açma, görüntüyü çevirme, boyutlandırma, renk dönüşümü, daire ve dikdörtgen çizme, ekranda pencere açma işlemlerinin tümü bu kütüphane üzerinden yapılır.

```python
import mediapipe as mp
```

Google'ın geliştirdiği MediaPipe kütüphanesini `mp` kısaltmasıyla dahil eder. Bu kodda MediaPipe'ın **FaceMesh** modeli kullanılacak — bir yüzdeki 468 anatomik noktayı tespit eder.

---

### 2. Boyut Değişkenleri

```python
width = 400
height = 400
```

Görüntünün hem işleneceği hem de gösterileceği boyutu piksel olarak tanımlar. Birkaç satır sonra `cv2.resize()` ile görüntü bu boyuta getirilecek. Değiştirmek istersen bu iki satırı düzenlemek yeterlidir — kodun geri kalanı otomatik uyum sağlar.

---

### 3. Kamera Bağlantısı

```python
vide_cam = cv2.VideoCapture(0)
```

Bilgisayardaki **0 numaralı kamerayı** (varsayılan/dahili webcam) açar. `0` yerine `1` veya `2` yazılarak harici kameralar da seçilebilir. Bu noktada kamera fiziksel olarak aktive olur.

---

### 4. MediaPipe Yüz Ağı Modülünü Hazırlama

```python
mp_face = mp.solutions.face_mesh
```

MediaPipe'ın içindeki `face_mesh` (yüz ağı) çözümüne erişir. Bu satır modeli çalıştırmaz, sadece araçlara erişim kapısı açar.

```python
face = mp_face.FaceMesh()
```

Yüz ağı tespit modelini oluşturur ve çalışmaya hazır hale getirir. Varsayılan parametreler:

| Parametre                  | Varsayılan | Açıklama                                                  |
| -------------------------- | ---------- | --------------------------------------------------------- |
| `static_image_mode`        | `False`    | Video akışı için optimize — her karede sıfırdan aramaz    |
| `max_num_faces`            | `1`        | Aynı anda en fazla kaç yüz tespit edilsin                 |
| `refine_landmarks`         | `False`    | `True` ile göz ve dudak noktaları daha hassas (478 nokta) |
| `min_detection_confidence` | `0.5`      | %50 güven altında yüz olarak saymaz                       |
| `min_tracking_confidence`  | `0.5`      | %50 altında yeniden tam tespit başlatır                   |

```python
mp_draw = mp.solutions.drawing_utils
```

MediaPipe'ın çizim yardımcılarına erişir. İskelet noktalarını ve bağlantı çizgilerini görüntü üzerine çizmek için kullanılır.

---

### 5. Ana Döngü

```python
while True:
```

Program `q` tuşuna basılana kadar sonsuza kadar çalışır. Her döngü = bir kare okunması + işlenmesi + ekranda gösterilmesi.

---

### 6. Kare Okuma

```python
ret, frame = vide_cam.read()
```

Kameradan **bir sonraki kareyi** okur:

- **`ret`** `(bool)` → Okuma başarılı mıydı? Bu kodda kontrol edilmemiş. Güvenli kullanım için `if not ret: break` satırı eklenebilir.
- **`frame`** `(ndarray)` → Kameradan gelen görüntü, BGR formatında NumPy dizisi.

---

### 7. Görüntüyü Aynalama

```python
frame = cv2.flip(frame, 1)
```

Görüntüyü **yatay olarak aynalar** (sol-sağ ters). Sonuç `frame` üzerine yazılır.

- `0` → Dikey çevirme
- `1` → Yatay çevirme ← bu kullanılan
- `-1` → Her iki yönde

**Neden?** Kamera normalde ayna etkisi olmadan çeker. `flip(frame, 1)` ile görüntü ayna gibi davranır — sağa eğilince ekranda da sağa eğilmiş görünürsün.

---

### 8. Görüntüyü Yeniden Boyutlandırma

```python
frame = cv2.resize(frame, (width, height))
```

Görüntüyü `(400, 400)` boyutuna getirir. Sonuç `frame` üzerine yazılır.

> ⚠️ `resize`'da parametre sırası `(genişlik, yükseklik)`, ama `frame.shape`'de sıra `(yükseklik, genişlik, kanal)` — tam tersidir, karıştırmayın!

---

### 9. Renk Uzayı Dönüşümü

```python
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

Görüntüyü **BGR'den RGB'ye** dönüştürür ve `frame_rgb` adında yeni bir değişkene atar. Orijinal `frame` (BGR) bozulmaz çünkü üzerine çizim yapmaya devam edeceğiz.

**Neden?** OpenCV `BGR` okur, MediaPipe `RGB` bekler. Dönüşüm yapılmadan renkler yanlış yorumlanır ve tespit bozulur.

| Değişken    | Format | Kullanım amacı                        |
| ----------- | ------ | ------------------------------------- |
| `frame`     | BGR    | Çizim ve ekranda gösterme             |
| `frame_rgb` | RGB    | Sadece MediaPipe modeline vermek için |

---

### 10. Yüz Ağı Tespiti

```python
result = face.process(frame_rgb)
```

RGB görüntüyü MediaPipe modeline verir, model yüzü bulur ve 468 noktanın koordinatlarını hesaplar. Tüm sonuçlar `result` nesnesine yazılır.

`result.multi_face_landmarks` → tespit edilen her yüzün 468 nokta listesi. Yüz yoksa `None` döner.

---

### 11. Yüz Tespitini Kontrol Et

```python
if result.multi_face_landmarks:
```

Yüz tespit edildi mi diye kontrol eder. Yüz yoksa `None` gelir, `None` üzerinde döngü açmak hata verir. Bu `if` o hatayı önler.

```python
    for face_landmarks in result.multi_face_landmarks:
```

Tespit edilen **her yüz için** döngü açar. Varsayılan `max_num_faces=1` olduğundan genelde 1 kez çalışır.

---

### 12. Kontür Çizgilerini Çiz

```python
        mp_draw.draw_landmarks(
            frame,
            face_landmarks,
            mp_face.FACEMESH_CONTOURS
        )
```

468 yüz noktasının bağlantı çizgilerini `frame` üzerine çizer:

- `frame` → çizimin yapılacağı görüntü (BGR)
- `face_landmarks` → 468 noktanın koordinatları
- `mp_face.FACEMESH_CONTOURS` → göz, kaş, dudak, burun ve yüz oval hatlarını çizen bağlantı şeması

---

### 13. Görüntü Boyutunu Al

```python
        h, w, c = frame.shape
```

Görüntünün boyutlarını alır:

- `h` → yükseklik (height) — piksel cinsinden, örn: `400`
- `w` → genişlik (width) — piksel cinsinden, örn: `400`
- `c` → kanal sayısı (channel) — renkli görüntüde her zaman `3` (B, G, R)

Bu değerler bir sonraki adımda normalize koordinatları gerçek piksel koordinatlarına çevirmek için kullanılacak.

> 💡 Bu satır döngünün içinde her yüz için tekrar çalışıyor. Görüntü boyutu değişmediğinden bunu döngünün dışına, `while True:` bloğunun hemen altına taşımak daha verimli olurdu.

---

### 14. Koordinat Listeleri Oluştur

```python
        x_list = []
        y_list = []
```

Her yüz için **sıfırdan** iki boş liste oluşturur:

- `x_list` → tüm 468 noktanın x koordinatları (piksel)
- `y_list` → tüm 468 noktanın y koordinatları (piksel)

Bu listeler döngü sonunda `min()` ve `max()` ile bounding box koordinatlarını hesaplamak için kullanılacak.

**Neden `for` döngüsünden önce oluşturuluyor?** Eğer döngü içinde oluşturulsaydı her noktada sıfırlanırdı. Döngüden önce oluşturularak her noktanın koordinatı birikimli olarak ekleniyor.

---

### 15. Her Nokta İçin Döngü — Koordinat Hesaplama ve Daire Çizme

```python
        for id, detection in enumerate(face_landmarks.landmark):
```

Tespit edilen **468 yüz noktasının her biri için** döngü başlatır:

- `enumerate()` → her elemana hem sıra numarası hem değer verir
- `id` → noktanın numarası (0'dan 467'ye kadar)
- `detection` → o noktanın `x`, `y`, `z`, `visibility` bilgilerini içeren nesne
- `detection.x` ve `detection.y` → **normalize koordinatlar** (0.0–1.0 arası, görüntü boyutundan bağımsız)

```python
            cx, cy = int(detection.x * w), int(detection.y * h)
```

Normalize koordinatları **gerçek piksel koordinatlarına** çevirir:

- `detection.x` → 0.0–1.0 arası, görüntü genişliğinin yüzde kaçında olduğunu söyler
- `detection.x * w` → gerçek piksel konumu (örn: `0.45 × 400 = 180`)
- `int(...)` → piksel koordinatı tam sayı olmak zorunda, float kabul edilmez
- Aynı mantık `detection.y * h` için de geçerli

Örnek:

```
detection.x = 0.45  →  cx = int(0.45 × 400) = 180
detection.y = 0.30  →  cy = int(0.30 × 400) = 120
```

```python
            x_list.append(cx)
            y_list.append(cy)
```

Hesaplanan piksel koordinatlarını listelerine ekler. 468 nokta döngüsü tamamlandığında `x_list` 468 adet x, `y_list` 468 adet y değeri içerecek.

```python
            cv2.circle(frame, (cx, cy), 2, (255, 0, 0), cv2.FILLED)
```

Her yüz noktasına küçük **mavi dolu daire** çizer:

- `frame` → çizileceği görüntü
- `(cx, cy)` → dairenin merkezi (noktanın piksel koordinatları)
- `2` → yarıçap 2 piksel — küçük tutulmuş ki 468 nokta birbirine karışmasın
- `(255, 0, 0)` → BGR formatında mavi renk (255 mavi, 0 yeşil, 0 kırmızı)
- `cv2.FILLED` → dairenin içini doldur (`-1` ile aynı anlam)

---

### 16. Bounding Box Koordinatlarını Hesapla

```python
        xmin, xmax = min(x_list), max(x_list)
        ymin, ymax = min(y_list), max(y_list)
```

468 noktanın koordinat listelerinden **bounding box (sınırlayıcı kutu)** köşelerini hesaplar.

**Nasıl çalışır?**

- `min(x_list)` → tüm noktalar arasında en soldaki x koordinatı → sol kenar
- `max(x_list)` → tüm noktalar arasında en sağdaki x koordinatı → sağ kenar
- `min(y_list)` → tüm noktalar arasında en üstteki y koordinatı → üst kenar
- `max(y_list)` → tüm noktalar arasında en alttaki y koordinatı → alt kenar

Bu dört değer birleşince yüzün tamamını içine alan minimum dikdörtgeni tanımlar:

```
(xmin, ymin) ──────────── (xmax, ymin)
      │                          │
      │     Yüzün tamamı         │
      │                          │
(xmin, ymax) ──────────── (xmax, ymax)
```

---

### 17. Bounding Box Çiz

```python
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
```

Hesaplanan köşe koordinatlarına **yeşil dikdörtgen** çizer:

- `frame` → çizileceği görüntü
- `(xmin, ymin)` → sol üst köşe
- `(xmax, ymax)` → sağ alt köşe
- `(0, 255, 0)` → BGR formatında yeşil renk (0 mavi, 255 yeşil, 0 kırmızı)
- `2` → çizgi kalınlığı 2 piksel (doldurmak için `-1` yazılırdı)

**Neden yeşil?** Yüz üzerindeki mavi nokta ve beyaz kontür çizgilerinden görsel olarak ayrışsın diye farklı renk seçilmiş.

---

### 18. Görüntüyü Göster

```python
    cv2.imshow("Yuz Tanima", frame)
```

İşlenmiş kareyi ekranda gösterir. `frame` artık üzerinde mavi noktalar, kontür çizgileri ve yeşil bounding box olan görüntüdür.

---

### 19. Çıkış Kontrolü

```python
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

Her karede klavye girdisini dinler:

- `cv2.waitKey(1)` → 1 ms bekle, bu sürede basılan tuşun kodunu döndür. `imshow`'un render edebilmesi için zorunludur.
- `& 0xFF` → Bit maskeleme ile platform bağımsız güvenilir tuş kodu alımı.
- `ord("q")` → `"q"` harfinin ASCII kodu → `113`
- `q` tuşuna basılırsa `break` ile döngü kırılır.

---

### 20. Kaynakları Serbest Bırak

```python
vide_cam.release()
```

Kamerayı kapatır, işletim sistemine geri verir. Kamera LED'i söner.

```python
cv2.destroyAllWindows()
```

Tüm OpenCV pencerelerini kapatır ve ekran belleğini temizler.

---

## 🔄 Programın Genel Akışı

```
Başla
  │
  ├─► Kamerayı aç
  ├─► MediaPipe FaceMesh modelini hazırla
  │
  └─► DÖNGÜ (sonsuz)
        │
        ├─► Kameradan kare oku            (vide_cam.read)
        ├─► Kareyi yatay aynala           (cv2.flip)
        ├─► Kareyi 400×400'e getir        (cv2.resize)
        ├─► BGR → RGB dönüştür            (cv2.cvtColor)
        ├─► Yüz ağı tespiti yap           (face.process)
        │
        ├─► Yüz tespit edildi mi?
        │     └─ EVET → Her yüz için:
        │           │
        │           ├─► Kontür çizgilerini çiz   (draw_landmarks + FACEMESH_CONTOURS)
        │           ├─► Görüntü boyutunu al       (frame.shape)
        │           ├─► Boş koordinat listeleri oluştur  (x_list, y_list)
        │           │
        │           └─► Her nokta için (468 kez):
        │                 ├─► Normalize → piksel koordinatına çevir  (cx, cy)
        │                 ├─► cx'i x_list'e, cy'yi y_list'e ekle
        │                 └─► Mavi dolu daire çiz  (cv2.circle)
        │
        ├─► min/max ile bounding box köşelerini hesapla
        └─► Yeşil dikdörtgen çiz          (cv2.rectangle)
        │
        ├─► Kareyi ekranda göster         (cv2.imshow)
        │
        └─► Q tuşuna basıldı mı?
              ├─ EVET → Döngüden çık
              └─ HAYIR → Döngünün başına dön

Kamerayı serbest bırak    (vide_cam.release)
Pencereleri kapat         (cv2.destroyAllWindows)
Bitir
```

---

## ✨ Önceki Versiyona Göre Eklenenler

Bu kod, önceki yüz ağı koduna göre şu üç yeni özelliği içeriyor:

| Yenilik                                    | Açıklama                                                        | İlgili Satırlar                                        |
| ------------------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------ |
| **Noktaların piksel koordinatı hesaplama** | Her noktanın normalize değeri gerçek piksel konumuna çevriliyor | `cx, cy = int(detection.x * w), int(detection.y * h)`  |
| **Mavi daireler**                          | Her 468 noktaya görsel daire çiziliyor                          | `cv2.circle(frame, (cx,cy), 2, (255,0,0), cv2.FILLED)` |
| **Yeşil bounding box**                     | Tüm noktaların min/max koordinatından yüz kutusu oluşturuluyor  | `cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), ...)`  |

---

## 🚀 Geliştirme Fikirleri

- **Belirli noktalara erişim:** `if id == 1:` (burun ucu), `if id == 33:` (sol göz köşesi) gibi koşullarla özel noktalar işlenebilir.
- **Bounding box etrafına padding ekle:** `xmin - 10`, `ymin - 10` gibi değerlerle kutu biraz genişletilebilir.
- **Yüzü kırpma:** `frame[ymin:ymax, xmin:xmax]` ile bounding box içindeki bölge ayrı bir görüntü olarak alınabilir.
- **Yüz sayısı gösterge:** `cv2.putText()` ile kaç yüz tespit edildiği ekrana yazdırılabilir.
- **FPS göstergesi:** `time` modülü ile her kare arasındaki süre ölçülerek FPS hesaplanabilir.
- **Göz kırpma tespiti:** Üst/alt göz kapağı noktaları arasındaki `cy` farkı ölçülerek göz açık/kapalı durumu tespit edilebilir.

---

## ⚠️ Sık Karşılaşılan Sorunlar

| Sorun                       | Olası Neden                                      | Çözüm                                                             |
| --------------------------- | ------------------------------------------------ | ----------------------------------------------------------------- |
| Kamera açılmıyor            | Başka uygulama kamerayı kullanıyor               | Diğer uygulamaları kapat                                          |
| Yüz tespit edilmiyor        | Karanlık ortam veya çok yakın mesafe             | İyi aydınlatma, 40–80 cm mesafe                                   |
| Bounding box yanlış konumda | `cx, cy` hesabında `w` ve `h` yer değiştirmiş    | `cx = detection.x * w`, `cy = detection.y * h` olduğundan emin ol |
| Daireler görünmüyor         | Yarıçap çok küçük veya renk çizgilerle karışıyor | Yarıçapı `2`'den `5`'e çıkar                                      |
| `mediapipe` bulunamadı      | Kütüphane kurulu değil                           | `pip install mediapipe` çalıştır                                  |
| Program kapanmıyor          | `release()` çağrılmadı                           | `q` ile düzgün çıkıldığından emin ol                              |
