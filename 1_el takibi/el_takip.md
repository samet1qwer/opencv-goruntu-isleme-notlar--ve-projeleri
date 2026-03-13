# 🖐️ Gerçek Zamanlı El Takibi

MediaPipe ve OpenCV kullanarak kameradan canlı el tespiti ve eklem noktalarını işaretleme uygulaması.

---

## 📸 Ne Yapar?

Bu program bilgisayarın kamerasını açar, görüntüyü kare kare analiz eder ve ekranda gördüğü ellerin üzerine otomatik olarak iskelet çizer. Parmak eklemleri nokta, eklemler arası bağlantılar ise çizgi olarak gösterilir. Program gerçek zamanlı çalışır, `q` tuşuna basılınca kapanır.

---

## 🧰 Kullanılan Kütüphaneler

| Kütüphane      | Ne İçin Kullanılıyor?                             |
| -------------- | ------------------------------------------------- |
| `cv2` (OpenCV) | Kamera açma, görüntü işleme, ekranda gösterme     |
| `mediapipe`    | El tespiti ve eklem noktalarını bulma (AI modeli) |
| `time`         | İmport edilmiş ama bu kodda aktif kullanım yok    |

### Kurulum

```bash
pip install opencv-python
pip install mediapipe
```

---

## 📄 Kodun Tamamı

```python
import cv2
import time
import mediapipe as mp

vide_cam = cv2.VideoCapture(0)

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_draw = mp.solutions.drawing_utils

while True:
    _, frame = vide_cam.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hand.HAND_CONNECTIONS)
    cv2.imshow("El Takibi", frame)
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

OpenCV kütüphanesini projeye dahil eder. Kamera açma, görüntüyü çevirme, renk dönüşümü ve ekranda pencere açma işlemlerinin tümü bu kütüphane üzerinden yapılır.

```python
import time
```

Python'ın yerleşik zaman modülüdür. Bu kodda aktif olarak kullanılmıyor ancak ileride `time.sleep()` ile FPS sınırlama veya işlem süresi ölçmek gibi geliştirmeler için hazır bırakılmış.

```python
import mediapipe as mp
```

Google tarafından geliştirilen MediaPipe kütüphanesini `mp` kısaltmasıyla dahil eder. MediaPipe içinde el tespiti, yüz tespiti, poz tespiti gibi hazır yapay zeka modelleri bulunur. Bu kodda el tespiti modeli kullanılacak.

---

### 2. Kamera Bağlantısı

```python
vide_cam = cv2.VideoCapture(0)
```

Bilgisayardaki **0 numaralı kamerayı** (varsayılan/dahili kamera) açar ve `vide_cam` değişkenine atar. Bu noktada kamera fiziksel olarak aktive olur (kamera LED'i yanar). Birden fazla kamera varsa `1`, `2` yazılarak diğerleri seçilebilir. Kamera yerine video dosyası da verilebilir: `cv2.VideoCapture("video.mp4")`

---

### 3. MediaPipe El Modülünü Hazırlama

```python
mp_hand = mp.solutions.hands
```

MediaPipe'ın içindeki `hands` (eller) çözümüne erişir ve `mp_hand` değişkenine atar. Bu satır henüz modeli çalıştırmaz, sadece el tespiti araçlarına erişim sağlar. `mp.solutions` altında `pose`, `face_mesh`, `holistic` gibi başka modeller de vardır.

```python
hands = mp_hand.Hands()
```

El tespit modelini oluşturur ve çalıştırılmaya hazır hale getirir. `Hands()` sınıfı varsayılan parametrelerle başlar:

| Parametre                  | Varsayılan | Açıklama                           |
| -------------------------- | ---------- | ---------------------------------- |
| `static_image_mode`        | `False`    | Video akışı için optimize çalışır  |
| `max_num_hands`            | `2`        | Aynı anda en fazla 2 el takip eder |
| `min_detection_confidence` | `0.5`      | %50 güven altında el saymaz        |
| `min_tracking_confidence`  | `0.5`      | %50 altında yeniden tespit yapar   |

İstersen özelleştirebilirsin:

```python
hands = mp_hand.Hands(max_num_hands=1, min_detection_confidence=0.7)
```

```python
mp_draw = mp.solutions.drawing_utils
```

MediaPipe'ın çizim yardımcı araçlarına erişir. Bu nesne, tespit edilen eklem noktalarını ve bağlantı çizgilerini görüntü üzerine çizmek için kullanılır. Bunu kullanmasan da el tespiti çalışır ama ekranda hiçbir şey görünmez.

---

### 4. Ana Döngü

```python
while True:
```

Program `q` tuşuna basılana kadar sonsuza kadar çalışır. Her bir döngü adımı = kameradan bir kare okunması + işlenmesi + ekranda gösterilmesi anlamına gelir. Bu yapıya **video processing loop** (video işleme döngüsü) denir.

---

### 5. Kare Okuma

```python
_, frame = vide_cam.read()
```

Kameradan **bir sonraki kareyi** okur. `read()` iki değer döndürür:

- **1. değer** `(bool)`: Okuma başarılı mıydı? `True` veya `False`. Burada `_` ile görmezden geliyoruz çünkü kullanmıyoruz.
- **2. değer** `(ndarray)`: Kameradan gelen görüntü, NumPy dizisi olarak, BGR formatında.

`_` (alt tire): Python'da "bu değeri kullanmayacağım" anlamına gelen konvansiyonel bir değişken adıdır.

---

### 6. Görüntüyü Aynalama

```python
frame = cv2.flip(frame, 1)
```

Görüntüyü **yatay eksende aynalar** (sol-sağ ters çevirir). `flip()` ikinci parametresi:

- `0` → Dikey çevirme (yukarı-aşağı ters)
- `1` → Yatay çevirme (sol-sağ ters) ← bu kullanılan
- `-1` → Her iki yönde çevirme

**Neden gerekli?** Kameralar ayna etkisi olmadan çeker — yani sağ elin sola, sol elin sağa göründüğü "selfie kamera" tersi bir görüntü üretir. `flip(frame, 1)` ile ayna etkisi eklenir, böylece sağ elin sağda, sol elin solda göründüğü, kullanıcıya doğal gelen bir görüntü elde edilir.

---

### 7. Renk Uzayı Dönüşümü

```python
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

Görüntüyü **BGR formatından RGB formatına** dönüştürür ve yeni değişkene atar (orijinal `frame` değişmez).

**Neden gerekli?** OpenCV görüntüleri `BGR` (Mavi-Yeşil-Kırmızı) sıralamasıyla okur. Ancak MediaPipe modeli `RGB` (Kırmızı-Yeşil-Mavi) formatında görüntü bekler. Bu dönüşüm yapılmadan modele verilseydi renkler yanlış yorumlanır ve tespit başarısız olurdu.

> 🔴 **Özet:** `frame` → OpenCV için BGR | `frame_rgb` → MediaPipe için RGB

---

### 8. El Tespiti

```python
result = hands.process(frame_rgb)
```

RGB görüntüyü MediaPipe el tespit modeline verir ve analiz etmesini sağlar. Model görüntüdeki elleri arar ve tüm sonuçları `result` nesnesine yazar. Bu işlem her karede yapay zeka çıkarımı (inference) gerçekleştirir.

`result` nesnesi içinde:

- `result.multi_hand_landmarks` → Tespit edilen her elin 21 eklem noktası
- `result.multi_handedness` → Sağ mı sol el mi bilgisi

MediaPipe bir elde **21 adet landmark (eklem noktası)** tespit eder:

```
0: Bilek
1-4:   Başparmak (4 eklem)
5-8:   İşaret parmağı (4 eklem)
9-12:  Orta parmak (4 eklem)
13-16: Yüzük parmağı (4 eklem)
17-20: Serçe parmak (4 eklem)
```

---

### 9. El Landmark'larını Kontrol Et ve Çiz

```python
if result.multi_hand_landmarks:
```

El tespit edildi mi diye kontrol eder. Eğer hiç el görünmüyorsa `result.multi_hand_landmarks` değeri `None` olur. `None` üzerinde döngü açmaya çalışmak hata verir. Bu `if` bloğu o hatadan korur — el yoksa içeri girmez.

```python
    for hand_landmarks in result.multi_hand_landmarks:
```

Tespit edilen **her el için** döngü başlatır. `max_num_hands=2` olduğundan bu döngü en fazla 2 kez çalışır. Ekranda 1 el varsa 1 kez, 2 el varsa 2 kez çalışır. `hand_landmarks`: o elin 21 eklem noktasını içeren nesne.

```python
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hand.HAND_CONNECTIONS)
```

Eklem noktalarını ve bağlantı çizgilerini **doğrudan `frame` üzerine** çizer. Üç parametre:

- `frame` → Çizimin yapılacağı görüntü (BGR, orijinal kamera görüntüsü)
- `hand_landmarks` → Çizilecek 21 eklem noktasının koordinatları
- `mp_hand.HAND_CONNECTIONS` → Hangi noktaların birbirine çizgi ile bağlanacağını tanımlar (örn: bilek→başparmak tabanı, eklem1→eklem2 vb.)

Sonuç: Her eklem noktasına renkli bir daire, aralarına bağlantı çizgisi çizilir.

---

### 10. Görüntüyü Ekranda Göster

```python
    cv2.imshow("El Takibi", frame)
```

İşlenmiş kareyi **"El Takibi"** başlıklı bir pencerede gösterir. `frame` artık üzerine el iskeletleri çizilmiş halde. Her döngüde bu satır çalıştığı için pencere sürekli yenilenir ve akıcı video izlenimi oluşur. Pencere adı değiştirilmek istenirse tırnak içindeki yazı değiştirilir.

---

### 11. Çıkış Kontrolü

```python
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

Her karede klavye girdisini dinler:

- `cv2.waitKey(1)` → 1 milisaniye bekle ve bu sürede basılan tuşun kodunu döndür. Bu satır aynı zamanda OpenCV'nin görüntüyü ekrana render etmesi için gereklidir — olmadan `imshow` çalışmaz.
- `& 0xFF` → Bit maskeleme. Bazı sistemlerde `waitKey` 32-bit değer döndürür, `0xFF` ile AND işlemi yapılarak sadece son 8 bit (gerçek tuş kodu) alınır. Platforma bağımsız güvenilir çalışma sağlar.
- `ord("q")` → `"q"` harfinin ASCII karşılığını döndürür → `113`
- Kullanıcı `q` tuşuna basarsa koşul `True` olur → `break` ile döngü kırılır

---

### 12. Kaynakları Serbest Bırak

```python
vide_cam.release()
```

Kamerayı kapatır ve işletim sistemine geri verir. Bu satır çalışmadan program sonlanırsa kamera kilitli kalabilir — bir sonraki açılışta "kamera kullanımda" hatası alınabilir. `release()` kamera LED'ini de söndürür.

```python
cv2.destroyAllWindows()
```

Açık olan tüm OpenCV pencerelerini kapatır ve belleği temizler. Sadece `vide_cam.release()` çağırılıp bu satır atlanırsa pencere ekranda donuk halde kalabilir.

---

## 🔄 Programın Genel Akışı

```
Başla
  │
  ├─► Kamerayı aç
  ├─► MediaPipe modelini hazırla
  │
  └─► DÖNGÜ (sonsuz)
        │
        ├─► Kameradan kare oku
        ├─► Kareyi yatay aynala
        ├─► BGR → RGB dönüştür
        ├─► MediaPipe ile el tespiti yap
        │
        ├─► El tespit edildi mi?
        │     ├─ EVET → Her el için iskelet çiz
        │     └─ HAYIR → Atla
        │
        ├─► Kareyi ekranda göster
        │
        └─► Q tuşuna basıldı mı?
              ├─ EVET → Döngüden çık
              └─ HAYIR → Döngünün başına dön

Kamerayı serbest bırak
Pencereleri kapat
Bitir
```

---

## 🚀 Geliştirme Fikirleri

Temel kodu anladıktan sonra şu özellikler eklenebilir:

- **Parmak sayma:** Her parmağın landmark koordinatlarına bakılarak kaç parmağın açık olduğu hesaplanabilir.
- **Jest tanıma:** Belirli eklem pozisyonları kombinasyonlarını (örn. yumruk, açık el) tanımlayıp jest sınıflandırması yapılabilir.
- **FPS göstergesi:** `time` modülü ile her kare arasındaki süre ölçülerek FPS hesaplanıp ekranda gösterilebilir.
- **Koordinat okuma:** `hand_landmarks.landmark[8]` ile işaret parmağı ucunun (x, y, z) koordinatları okunabilir.

---

## ⚠️ Sık Karşılaşılan Sorunlar

| Sorun                   | Olası Neden                        | Çözüm                                    |
| ----------------------- | ---------------------------------- | ---------------------------------------- |
| Kamera açılmıyor        | Başka uygulama kamerayı kullanıyor | Diğer uygulamaları kapat                 |
| El tespit edilmiyor     | Işık yetersiz veya el çok yakın    | Aydınlık ortamda, 30–60 cm mesafede dene |
| `mediapipe` bulunamadı  | Kütüphane kurulu değil             | `pip install mediapipe` çalıştır         |
| Görüntü ayna gibi değil | `flip` satırı kaldırıldı           | `cv2.flip(frame, 1)` satırını geri ekle  |
| Program kapanmıyor      | `release()` çağrılmadı             | `q` ile çıkıldığından emin ol            |
