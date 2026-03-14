# 🧍 Gerçek Zamanlı Poz Kestirimi (Pose Estimation)

MediaPipe ve OpenCV kullanarak kameradan canlı insan vücudu tespiti ve iskelet noktalarını işaretleme uygulaması.

---

## 📸 Ne Yapar?

Bu program bilgisayarın kamerasını açar, görüntüyü kare kare analiz eder ve ekranda gördüğü insanın vücudu üzerine otomatik olarak iskelet çizer. Omuz, dirsek, kalça, diz gibi 33 adet vücut noktası tespit edilir, bu noktalar arası bağlantılar çizilir. Ayrıca baş noktası (ID: 0) büyük mavi bir daire ile ayrıca vurgulanır. Tespit edilen her noktanın koordinatları terminale yazdırılır.

---

## 🧰 Kullanılan Kütüphaneler

| Kütüphane      | Ne İçin Kullanılıyor?                                      |
| -------------- | ---------------------------------------------------------- |
| `cv2` (OpenCV) | Kamera açma, görüntü işleme, ekranda gösterme, daire çizme |
| `mediapipe`    | Vücut poz tespiti ve iskelet noktalarını bulma (AI modeli) |

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

mp_pozition = mp.solutions.pose
pose = mp_pozition.Pose()
mp_draw = mp.solutions.drawing_utils

while True:
    ret, frame = vide_cam.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = pose.process(frame_rgb)

    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pozition.POSE_CONNECTIONS)
        for id, lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            print(id, lm)
            if id == 0:
                cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    cv2.imshow("poz kestirimi", frame)

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

OpenCV kütüphanesini projeye dahil eder. Kamera açma, renk dönüşümü, ekranda pencere açma ve görüntü üzerine şekil çizme işlemlerinin tümü bu kütüphane üzerinden yapılır.

```python
import mediapipe as mp
```

Google'ın geliştirdiği MediaPipe kütüphanesini `mp` kısaltmasıyla dahil eder. Bu kodda MediaPipe'ın **Pose** (poz/duruş) modeli kullanılacak. Bu model insan vücudundaki 33 anatomik noktayı tespit edebilir.

---

### 2. Boyut Değişkenleri

```python
width = 400
height = 400
```

`400` değerinde iki değişken tanımlanmış. Ancak bu değişkenler kodun geri kalanında **hiçbir yerde kullanılmıyor**. Muhtemelen ileride kamera çözünürlüğünü ayarlamak ya da görüntüyü yeniden boyutlandırmak için planlanmış ama henüz eklenmemiş. Şu haliyle kod çalışmasını etkilemez.

Kullanmak istenseydi şöyle yazılırdı:

```python
vide_cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vide_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
```

---

### 3. Kamera Bağlantısı

```python
vide_cam = cv2.VideoCapture(0)
```

Bilgisayardaki **0 numaralı kamerayı** (varsayılan/dahili webcam) açar ve `vide_cam` nesnesine atar. Bu noktada kamera fiziksel olarak aktive olur. Birden fazla kamera varsa `1`, `2` yazılarak diğerleri seçilebilir.

---

### 4. MediaPipe Poz Modülünü Hazırlama

```python
mp_pozition = mp.solutions.pose
```

MediaPipe'ın içindeki `pose` (poz/duruş) çözümüne erişir ve `mp_pozition` değişkenine atar. Bu satır henüz modeli çalıştırmaz, sadece poz tespiti araçlarına erişim kapısını açar.

```python
pose = mp_pozition.Pose()
```

Poz tespit modelini oluşturur ve çalışmaya hazır hale getirir. `Pose()` sınıfı varsayılan parametrelerle başlar:

| Parametre                  | Varsayılan | Açıklama                                                                 |
| -------------------------- | ---------- | ------------------------------------------------------------------------ |
| `static_image_mode`        | `False`    | Video akışı için optimize çalışır, her karede sıfırdan aramaz            |
| `model_complexity`         | `1`        | Model karmaşıklığı: 0 (hızlı/düşük doğruluk) → 2 (yavaş/yüksek doğruluk) |
| `smooth_landmarks`         | `True`     | Noktalar arasında yumuşatma yapar, titreme azalır                        |
| `min_detection_confidence` | `0.5`      | %50 güven altında kişi olarak saymaz                                     |
| `min_tracking_confidence`  | `0.5`      | %50 altında yeniden tam tespit yapar                                     |

İstersen özelleştirebilirsin:

```python
pose = mp_pozition.Pose(model_complexity=2, min_detection_confidence=0.7)
```

```python
mp_draw = mp.solutions.drawing_utils
```

MediaPipe'ın çizim yardımcı araçlarına erişir. Tespit edilen iskelet noktalarını ve bağlantı çizgilerini görüntü üzerine otomatik olarak çizer. Bu olmadan poz tespiti hâlâ çalışır ama ekranda hiçbir şey görünmez.

---

### 5. Ana Döngü

```python
while True:
```

Program `q` tuşuna basılana kadar sonsuza kadar çalışır. Her döngü adımı: kameradan bir kare oku → işle → ekranda göster. Bu yapıya **video processing loop** (video işleme döngüsü) denir.

---

### 6. Kare Okuma

```python
ret, frame = vide_cam.read()
```

Kameradan **bir sonraki kareyi** okur. `read()` iki değer döndürür:

- **`ret`** `(bool)` → Okuma başarılı mıydı? `True` veya `False`. Bu kodda `ret` kontrol edilmiyor ama iyi pratik olarak `if not ret: break` şeklinde kullanılmalıdır.
- **`frame`** `(ndarray)` → Kameradan gelen görüntü, BGR formatında NumPy dizisi.

---

### 7. Renk Uzayı Dönüşümü

```python
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

Görüntüyü **BGR formatından RGB formatına** dönüştürür.

**Neden gerekli?** OpenCV kamerayı `BGR` (Mavi-Yeşil-Kırmızı) sırasıyla okur. Ancak MediaPipe modeli `RGB` (Kırmızı-Yeşil-Mavi) formatında görüntü bekler. Bu dönüşüm yapılmadan modele verilseydi renkler yanlış yorumlanır ve poz tespiti başarısız olurdu.

> `frame` → OpenCV için BGR (orijinal, çizimler burada yapılır)
> `frame_rgb` → MediaPipe için RGB (sadece analiz için kullanılır)

---

### 8. Poz Tespiti

```python
result = pose.process(frame_rgb)
```

RGB görüntüyü MediaPipe poz tespit modeline verir ve analiz etmesini sağlar. Model görüntüdeki kişinin vücudunu bulur, 33 anatomik noktanın koordinatlarını hesaplar ve tüm sonuçları `result` nesnesine yazar.

`result` nesnesi içinde:

- `result.pose_landmarks` → 33 iskelet noktasının normalize (0-1 arası) koordinatları
- `result.pose_world_landmarks` → 3 boyutlu gerçek dünya koordinatları (metre cinsinden)

---

### 9. Poz Noktalarını Kontrol Et ve Çiz

```python
if result.pose_landmarks:
```

Vücutta poz tespit edildi mi diye kontrol eder. Görüntüde kimse yoksa `result.pose_landmarks` değeri `None` olur. `None` üzerinde işlem yapmaya çalışmak hata verir. Bu `if` bloğu o hatadan korur.

```python
    mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pozition.POSE_CONNECTIONS)
```

33 iskelet noktasını ve bağlantı çizgilerini **doğrudan `frame` üzerine** çizer. Üç parametre:

- `frame` → Çizimin yapılacağı görüntü (BGR formatında orijinal kamera görüntüsü)
- `result.pose_landmarks` → Çizilecek 33 noktanın koordinatları
- `mp_pozition.POSE_CONNECTIONS` → Hangi noktaların birbirine çizgiyle bağlanacağını tanımlar (omuz↔dirsek, kalça↔diz gibi)

---

### 10. Her Nokta İçin Koordinat Hesaplama

```python
    for id, lm in enumerate(result.pose_landmarks.landmark):
```

Tespit edilen **33 poz noktasının her biri için** döngü başlatır.

- `enumerate()` → her elemana hem sıra numarası (id) hem de değer (lm) verir
- `id` → noktanın numarası (0'dan 32'ye kadar)
- `lm` → o noktanın `x`, `y`, `z`, `visibility` bilgilerini içeren nesne
- `lm.x` ve `lm.y` → **normalize koordinatlar** (0.0 ile 1.0 arasında, görüntü boyutundan bağımsız)
- `lm.visibility` → noktanın ne kadar görünür olduğu (0=görünmez, 1=tam görünür)

```python
        h, w, c = frame.shape
```

Görüntünün boyutlarını alır. `frame.shape` üç değer döndürür:

- `h` → yükseklik (height), piksel cinsinden (örn: 480)
- `w` → genişlik (width), piksel cinsinden (örn: 640)
- `c` → kanal sayısı (channel), renkli görüntüde her zaman 3 (B, G, R)

> ⚠️ **Not:** Bu satır döngünün içinde her tekrarda çalışıyor. Görüntü boyutu döngü boyunca değişmediğinden bunu döngüden önce bir kez yazmak daha verimli olurdu.

```python
        cx, cy = int(lm.x * w), int(lm.y * h)
```

Normalize koordinatları **gerçek piksel koordinatlarına** çevirir:

- `lm.x` → 0.0 ile 1.0 arasında, görüntü genişliğinin yüzde kaçında olduğunu söyler
- `lm.x * w` → gerçek piksel konumunu verir (örn: 0.5 × 640 = 320 → ekranın ortası)
- `int(...)` → piksel koordinatı tam sayı olmak zorunda, float kabul edilmez
- Aynı mantık `lm.y * h` için de geçerli

Örnek: `lm.x=0.3`, `lm.y=0.6`, `w=640`, `h=480` ise → `cx=192`, `cy=288`

```python
        print(id, lm)
```

Her noktanın ID'sini ve tam bilgilerini terminale yazdırır. `lm` içinde şunlar gösterilir:

```
x: 0.512...    # yatay konum (normalize)
y: 0.234...    # dikey konum (normalize)
z: -0.021...   # derinlik (kameraya yakınlık, göreceli)
visibility: 0.998...  # görünürlük skoru
```

Bu satır her karede 33 kez çalışır → terminalde çok hızlı akan veri üretir. Geliştirme aşamasında değerleri görmek için kullanışlı, ama performansı biraz düşürür.

---

### 11. Baş Noktasına Özel Daire

```python
        if id == 0:
            cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
```

Sadece **0 numaralı nokta** (baş / burun noktası) için özel bir daire çizer.

- `if id == 0` → döngü 0. noktaya geldiğinde bu bloğa girer
- `cv2.circle(görüntü, merkez, yarıçap, renk, kalınlık)` parametreleri:
  - `frame` → dairenin çizileceği görüntü
  - `(cx, cy)` → dairenin merkezi (baş noktasının piksel koordinatları)
  - `10` → yarıçap 10 piksel
  - `(255, 0, 0)` → BGR mavi renk (255 mavi, 0 yeşil, 0 kırmızı)
  - `cv2.FILLED` → dairenin içi dolu olsun (`-1` ile aynı anlam)

> 💡 Diğer noktalara da özel işlem yapmak için `if id == 11:` (sol omuz), `if id == 23:` (sol kalça) gibi koşullar eklenebilir.

---

### 12. Görüntüyü Ekranda Göster

```python
    cv2.imshow("poz kestirimi", frame)
```

İşlenmiş kareyi **"poz kestirimi"** başlıklı bir pencerede gösterir. `frame` artık üzerine iskelet çizilmiş ve baş noktası mavi daire ile işaretlenmiş halde. Her döngüde bu satır çalıştığı için pencere sürekli yenilenir ve akıcı video izlenimi oluşur.

---

### 13. Çıkış Kontrolü

```python
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

Her karede klavye girdisini dinler:

- `cv2.waitKey(1)` → 1 milisaniye bekle ve bu sürede basılan tuşun kodunu döndür. Bu satır aynı zamanda OpenCV'nin görüntüyü render etmesi için zorunludur.
- `& 0xFF` → Bit maskeleme. Bazı sistemlerde `waitKey` 32-bit değer döndürür, `0xFF` ile AND işlemiyle sadece son 8 bit alınır → platform bağımsız güvenilir çalışma.
- `ord("q")` → `"q"` harfinin ASCII karşılığı olan `113` sayısını döndürür.
- Kullanıcı `q` tuşuna basarsa koşul `True` → `break` ile döngü sonlanır.

---

### 14. Kaynakları Serbest Bırak

```python
vide_cam.release()
```

Kamerayı kapatır ve işletim sistemine geri verir. Bu satır çalışmadan program kapanırsa kamera kilitli kalabilir ve bir sonraki açılışta "kamera kullanımda" hatası oluşabilir.

```python
cv2.destroyAllWindows()
```

Açık olan tüm OpenCV pencerelerini kapatır ve ekran belleğini temizler. Bu olmadan pencere ekranda donuk halde kalabilir.

---

## 🦴 MediaPipe Poz — 33 Nokta Referansı

MediaPipe Pose modeli vücutta tam olarak **33 adet landmark** tespit eder:

| ID  | Nokta           | ID  | Nokta                |
| --- | --------------- | --- | -------------------- |
| 0   | Burun (Nose)    | 17  | Sol bilek            |
| 1   | Sol iç göz      | 18  | Sağ bilek            |
| 2   | Sol göz         | 19  | Sol el başparmak ucu |
| 3   | Sol dış göz     | 20  | Sağ el başparmak ucu |
| 4   | Sağ iç göz      | 21  | Sol el serçe ucu     |
| 5   | Sağ göz         | 22  | Sağ el serçe ucu     |
| 6   | Sağ dış göz     | 23  | Sol kalça            |
| 7   | Sol kulak       | 24  | Sağ kalça            |
| 8   | Sağ kulak       | 25  | Sol diz              |
| 9   | Sol ağız köşesi | 26  | Sağ diz              |
| 10  | Sağ ağız köşesi | 27  | Sol ayak bileği      |
| 11  | Sol omuz        | 28  | Sağ ayak bileği      |
| 12  | Sağ omuz        | 29  | Sol topuk            |
| 13  | Sol dirsek      | 30  | Sağ topuk            |
| 14  | Sağ dirsek      | 31  | Sol ayak parmak ucu  |
| 15  | Sol el bileği   | 32  | Sağ ayak parmak ucu  |
| 16  | Sağ el bileği   |     |                      |

---

## 🔄 Programın Genel Akışı

```
Başla
  │
  ├─► Kamerayı aç
  ├─► MediaPipe Pose modelini hazırla
  │
  └─► DÖNGÜ (sonsuz)
        │
        ├─► Kameradan kare oku
        ├─► BGR → RGB dönüştür
        ├─► MediaPipe ile poz tespiti yap
        │
        ├─► Poz tespit edildi mi?
        │     ├─ EVET →
        │     │    ├─ Tüm iskelet çizgilerini çiz (draw_landmarks)
        │     │    └─ 33 nokta için döngü:
        │     │         ├─ Normalize koordinat → piksel koordinatına çevir
        │     │         ├─ Koordinatları terminale yazdır
        │     │         └─ ID=0 ise → mavi daire çiz (baş noktası)
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

- **Belirli eklemleri vurgulama:** `if id == 11:` (sol omuz), `if id == 23:` (sol kalça) gibi koşullarla istenen noktalara farklı renkler ve boyutlar verilebilir.
- **Açı hesaplama:** İki vektör arasındaki açıyı hesaplayarak dirsek bükülme açısı, diz açısı gibi değerler elde edilebilir — egzersiz sayacı yapılabilir.
- **Görünürlük filtresi:** `lm.visibility > 0.5` kontrolü ile sadece kameraya yeterince görünen noktalar işlenebilir.
- **FPS göstergesi:** `cv2.putText()` ile saniyede kaç kare işlendiği ekranda gösterilebilir.
- **Duruş analizi:** Omuz ve kalça noktaları karşılaştırılarak dik mi eğik mi oturulduğu tespit edilebilir.
- **Kamera yansıtma:** El takibi kodundaki gibi `cv2.flip(frame, 1)` ile ayna etkisi eklenebilir.

---

## ⚠️ Sık Karşılaşılan Sorunlar

| Sorun                     | Olası Neden                                 | Çözüm                                                       |
| ------------------------- | ------------------------------------------- | ----------------------------------------------------------- |
| Kamera açılmıyor          | Başka uygulama kamerayı kullanıyor          | Diğer uygulamaları kapat                                    |
| Poz tespit edilmiyor      | Vücudun tamamı görünmüyor                   | Kameradan uzaklaş, tam vücut çerçevede olsun                |
| Terminal çok hızlı akıyor | `print(id, lm)` her karede 33 kez çalışıyor | Sadece belirli ID için print ekle: `if id == 0: print(...)` |
| `mediapipe` bulunamadı    | Kütüphane kurulu değil                      | `pip install mediapipe` çalıştır                            |
| Görüntü donuk kalıyor     | `destroyAllWindows()` çağrılmadı            | `q` ile düzgün çıkıldığından emin ol                        |

---

## 🔀 El Takibi ile Farkı

Bu kod bir önceki el takibi koduyla aynı yapıyı kullanır. Temel farklar:

| Özellik             | El Takibi              | Poz Kestirimi       |
| ------------------- | ---------------------- | ------------------- |
| Model               | `mp.solutions.hands`   | `mp.solutions.pose` |
| Tespit edilen nokta | 21 el eklem noktası    | 33 vücut noktası    |
| Bağlantılar         | `HAND_CONNECTIONS`     | `POSE_CONNECTIONS`  |
| Landmarks           | `multi_hand_landmarks` | `pose_landmarks`    |
| Kapsam              | Sadece eller           | Tüm vücut           |
| Ayna efekti         | Var (`cv2.flip`)       | Yok (eklenmemiş)    |
