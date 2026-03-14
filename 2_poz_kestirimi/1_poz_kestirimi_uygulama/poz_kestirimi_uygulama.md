# 💪 Otomatik Egzersiz Tekrar Sayacı (Bicep Curl Counter)

MediaPipe Pose ve OpenCV kullanarak video üzerinden dirsek açısını ölçen ve bicep curl (ön kol kıvırma) tekrarlarını otomatik sayan uygulama.

---

## 📸 Ne Yapar?

Bu program bir egzersiz videosunu analiz eder. Her karede kişinin sol ve sağ kolunun dirsek açısını hesaplar. Kol yeterince kıvrıldığında (açı < 130°) hareketi "yukarı" olarak, ardından yeterince indirildiğinde (açı > 160°) "aşağı" olarak işaretler ve bir tekrar tamamlandığını sayar. Ekranda tekrar sayısı, mevcut aşama ve anlık açı değeri canlı olarak gösterilir.

---

## 🧰 Kullanılan Kütüphaneler

| Kütüphane      | Ne İçin Kullanılıyor?                             |
| -------------- | ------------------------------------------------- |
| `cv2` (OpenCV) | Video okuma, görüntü işleme, metin ve şekil çizme |
| `mediapipe`    | Vücut iskelet noktalarını tespit etme (AI modeli) |
| `math`         | Açı hesabında trigonometrik fonksiyonlar          |

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
import math

def calculate_angle(a, b, c):
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - \
              math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(math.degrees(radians))
    if angle > 180:
        angle = 360 - angle
    return angle

video = cv2.VideoCapture("video.mp4")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

rep_count = 0
stage = None

ANGLE_UP   = 130
ANGLE_DOWN = 160

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        h, w, c = frame.shape
        lms = results.pose_landmarks.landmark

        def get_point(idx):
            lm = lms[idx]
            return (int(lm.x * w), int(lm.y * h))

        left_shoulder  = get_point(11)
        left_elbow     = get_point(13)
        left_wrist     = get_point(15)
        right_shoulder = get_point(12)
        right_elbow    = get_point(14)
        right_wrist    = get_point(16)

        left_angle  = calculate_angle(left_shoulder,  left_elbow,  left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        avg_angle   = (left_angle + right_angle) / 2

        cv2.putText(frame, f"{int(left_angle)}",
                    (left_elbow[0] - 40, left_elbow[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"{int(right_angle)}",
                    (right_elbow[0] + 10, right_elbow[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        if avg_angle < ANGLE_UP:
            stage = "up"
        elif avg_angle > ANGLE_DOWN and stage == "up":
            stage = "down"
            rep_count += 1

        cv2.rectangle(frame, (0, 0), (340, 90), (0, 0, 0), cv2.FILLED)
        cv2.putText(frame, f"Tekrar: {rep_count}", (10, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
        cv2.putText(frame, f"Asama: {stage if stage else '-'}  Aci: {int(avg_angle)}", (10, 78),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Sayac", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
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

OpenCV kütüphanesini dahil eder. Video okuma, görüntüyü çevirme, renk dönüşümü, metin ve dikdörtgen çizme işlemleri bu kütüphane üzerinden yapılır.

```python
import mediapipe as mp
```

Google'ın MediaPipe kütüphanesini `mp` kısaltmasıyla dahil eder. İçindeki Pose (poz) modeli, videodaki kişinin omuz, dirsek ve bileklerini tespit etmek için kullanılır.

```python
import math
```

Python'ın yerleşik matematik kütüphanesi. `atan2` (ark tanjant) ve `degrees` (radyandan dereceye çevirme) fonksiyonları açı hesabı için kullanılır.

---

### 2. Açı Hesaplama Fonksiyonu

Bu fonksiyon kodun en kritik parçasıdır. Üç nokta verildiğinde ortadaki noktadaki (dirsek) açıyı hesaplar.

```python
def calculate_angle(a, b, c):
```

Üç adet `(x, y)` koordinat çifti alır:

- `a` → birinci nokta (omuz)
- `b` → ikinci nokta, açının ölçüleceği köşe (dirsek)
- `c` → üçüncü nokta (bilek)

```python
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - \
              math.atan2(a[1] - b[1], a[0] - b[0])
```

`math.atan2(y, x)` → bir noktanın orijine göre yaptığı açıyı **radyan** cinsinden verir.

Burada iki ayrı vektörün açısı hesaplanıp farkı alınıyor:

- `math.atan2(c[1]-b[1], c[0]-b[0])` → **b'den c'ye** giden vektörün açısı (dirsekten bileğe)
- `math.atan2(a[1]-b[1], a[0]-b[0])` → **b'den a'ya** giden vektörün açısı (dirsekten omuza)

İki vektör arasındaki fark → aralarındaki gerçek açıyı verir.

`\` → satır devam karakteri, uzun formülü iki satıra böler, kod aynı şekilde çalışır.

```python
    angle = abs(math.degrees(radians))
```

- `math.degrees(radians)` → radyanı **dereceye** çevirir (0-360 değil, -180 ile +180 arası gelebilir)
- `abs(...)` → mutlak değer alır, negatif açıyı pozitife çevirir

```python
    if angle > 180:
        angle = 360 - angle
```

Açı hesabında bazen 200°, 270° gibi değerler çıkabilir (iki yönlü ölçümden dolayı). İnsan vücudundaki eklem açıları her zaman 0°-180° arasındadır. Bu satır, 180°'yi aşan değerleri `360 - açı` ile gerçek anatomik açıya dönüştürür. Örnek: 200° → `360 - 200 = 160°`

```python
    return angle
```

Hesaplanan açı değerini (0-180 arası float) döndürür.

---

### 3. Video Açma

```python
video = cv2.VideoCapture("video.mp4")
```

`"video.mp4"` adlı video dosyasını açar. Kamera yerine dosyadan okuma yapılıyor. Dosya aynı klasörde olmalı, yoksa tam yol verilmeli. Kamera kullanmak istersen `"video.mp4"` yerine `0` yaz.

---

### 4. MediaPipe Hazırlığı

```python
mp_pose = mp.solutions.pose
```

MediaPipe'ın Pose (poz) çözümüne erişim kapısını açar.

```python
mp_drawing = mp.solutions.drawing_utils
```

İskelet noktalarını ve bağlantılarını görüntü üzerine çizmek için çizim araçlarına erişir.

```python
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
```

Poz modelini oluşturur ve iki parametre ile yapılandırır:

- `min_detection_confidence=0.5` → Model, kişiyi en az %50 güvenle tespit ettiğinde kabul eder. Düşürülürse daha hassas ama yanlış tespitler artar. Yükseltilirse daha az ama daha güvenilir tespit.
- `min_tracking_confidence=0.5` → Önceki karede tespit edilen kişiyi takip ederken en az %50 güven aranır. Bu değerin altında kalınca model sıfırdan yeniden tespit yapar.

---

### 5. Sayaç Değişkenleri

```python
rep_count = 0
```

Tamamlanan tekrar sayısını tutar. Her tekrar tamamlandığında 1 artırılır. Program başında sıfırdan başlar.

```python
stage = None
```

Kolun şu anki konumunu (aşamasını) tutar. Üç olası değer:

- `None` → Henüz hiçbir hareket tespit edilmedi (başlangıç)
- `"up"` → Kol yukarı kıvrıldı (dirsek açısı küçük)
- `"down"` → Kol aşağı indirildi (dirsek açısı büyük)

Sayaç mantığı bu değişken üzerine kurulu. Bir tekrar sayılabilmesi için sıra `None/down → up → down` şeklinde olmalı.

---

### 6. Eşik Açı Sabitleri

```python
ANGLE_UP   = 130
ANGLE_DOWN = 160
```

Büyük harfle yazılmaları Python'da **sabit (constant)** olduklarını belirtir — değiştirilmemesi gerektiğini söyler.

- `ANGLE_UP = 130` → Ortalama dirsek açısı 130°'nin **altına** düşünce kol "yukarıda" sayılır (kol kıvrılmış)
- `ANGLE_DOWN = 160` → Ortalama dirsek açısı 160°'nin **üstüne** çıkınca kol "aşağıda" sayılır (kol indirilmiş)

Neden aynı değer değil? İki farklı eşik değeri kullanmak **histerezis** (titreme engeli) sağlar. Eğer tek bir eşik olsaydı (örn. 145°), kol tam o açıda salınırken sürekli up-down-up-down değişir ve yanlış tekrarlar sayılırdı. İki eşik arasında bir "güvenli bölge" bırakarak bu titreme engellenir.

---

### 7. Ana Döngü

```python
while True:
```

Program `q` tuşuna basılana veya video bitene kadar çalışır.

```python
    ret, frame = video.read()
```

Videodan bir sonraki kareyi okur:

- `ret` → okuma başarılı mı? `True/False`
- `frame` → okunan görüntü karesi

```python
    if not ret:
        break
```

`ret` False olursa (video bitti veya hata oluştuysa) döngüden çık. Önceki örneklerde bu kontrol yoktu; bu daha **güvenli ve doğru** bir kullanımdır. Video dosyasından okurken bu kontrol olmadan program son kare sonrası çöker.

---

### 8. Görüntü Hazırlama

```python
    frame = cv2.flip(frame, 1)
```

Görüntüyü yatay olarak aynalar (sol-sağ ters çevirir). `1` → yatay çevirme. Kameradan canlı çekilmiş videolarda ayna etkisi doğal hissettirir.

```python
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

OpenCV'nin BGR formatını MediaPipe'ın beklediği RGB formatına dönüştürür. `frame` → çizimler için BGR olarak korunur, `frame_rgb` → sadece MediaPipe'a verilir.

```python
    results = pose.process(frame_rgb)
```

RGB kareyi modele gönderir. Model 33 iskelet noktasını tespit eder ve `results` nesnesine yazar.

---

### 9. İskelet Çizimi ve Noktalar

```python
    if results.pose_landmarks:
```

Poz tespit edildi mi kontrol eder. `None` kontrolü yaparak olası çökmeden korur.

```python
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
```

Tüm 33 iskelet noktasını ve aralarındaki bağlantı çizgilerini `frame` üzerine çizer.

```python
        h, w, c = frame.shape
```

Görüntü boyutlarını alır:

- `h` → yükseklik (piksel)
- `w` → genişlik (piksel)
- `c` → kanal sayısı (renkli görüntüde her zaman 3)

```python
        lms = results.pose_landmarks.landmark
```

33 landmark nesnesinin listesini `lms` kısaltmasına atar. Her satırda `results.pose_landmarks.landmark[idx]` yazmak uzun olduğundan kısaltılmış.

---

### 10. Nokta Koordinatı Alma Fonksiyonu

```python
        def get_point(idx):
            lm = lms[idx]
            return (int(lm.x * w), int(lm.y * h))
```

Bu fonksiyon döngü içinde, her kare işlenirken **yeniden tanımlanıyor**. Çalışır ama ideal değil — normalde döngü dışında tanımlanmalı. Yine de işlevi şu:

- `idx` → istenen landmark'ın ID numarası (0-32)
- `lms[idx]` → o ID'ye ait landmark nesnesini al
- `lm.x` ve `lm.y` → normalize koordinatlar (0.0-1.0 arası)
- `lm.x * w` → normalize x'i gerçek piksel x koordinatına çevir
- `lm.y * h` → normalize y'yi gerçek piksel y koordinatına çevir
- `int(...)` → tam sayıya yuvarlama (OpenCV koordinat olarak tam sayı ister)
- Sonuç: `(cx, cy)` formatında piksel koordinat tuple'ı döner

---

### 11. Eklem Noktalarını Al

```python
        left_shoulder  = get_point(11)   # Sol omuz
        left_elbow     = get_point(13)   # Sol dirsek
        left_wrist     = get_point(15)   # Sol bilek
        right_shoulder = get_point(12)   # Sağ omuz
        right_elbow    = get_point(14)   # Sağ dirsek
        right_wrist    = get_point(16)   # Sağ bilek
```

Her değişken `(x, y)` piksel koordinatı içerir. MediaPipe ID numaraları sabit: 11=sol omuz, 12=sağ omuz, 13=sol dirsek, 14=sağ dirsek, 15=sol bilek, 16=sağ bilek.

---

### 12. Açı Hesaplama

```python
        left_angle  = calculate_angle(left_shoulder,  left_elbow,  left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
```

Her iki kol için dirsekteki açıyı hesaplar:

- Sol kol: omuz → dirsek → bilek üçgeni
- Sağ kol: omuz → dirsek → bilek üçgeni

Kol tamamen düzde → açı ~180°, kol tam kıvrılmış → açı ~30-40°

```python
        avg_angle = (left_angle + right_angle) / 2
```

Sol ve sağ kol açılarının ortalamasını alır. İki kolun ortalaması kullanılarak tek kolun kötü görüntülenmesi veya farklı açıda durması durumunda daha kararlı ve dengeli bir ölçüm elde edilir.

---

### 13. Açı Değerlerini Ekranda Göster

```python
        cv2.putText(frame, f"{int(left_angle)}",
                    (left_elbow[0] - 40, left_elbow[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
```

Sol dirsek açısını, sol dirseğin hemen yanına yazar:

- `f"{int(left_angle)}"` → açı değerini tam sayıya yuvarlayıp string'e çevirir
- `left_elbow[0] - 40` → dirsek noktasının 40 piksel soluna (yazı sola taşmaz)
- `left_elbow[1] - 10` → dirsek noktasının 10 piksel yukarısına
- `0.7` → font boyutu
- `(255, 255, 0)` → sarı renk (BGR: 255 mavi + 255 yeşil = sarı)
- `2` → yazı kalınlığı

```python
        cv2.putText(frame, f"{int(right_angle)}",
                    (right_elbow[0] + 10, right_elbow[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
```

Sağ dirsek açısını, sağ dirseğin 10 piksel sağına ve 10 piksel yukarısına yazar. Sol taraf `-40` iken sağ taraf `+10` — solda yazı dirsekle çakışmasın diye daha fazla öteleriz.

---

### 14. Tekrar Sayma Mantığı

```python
        if avg_angle < ANGLE_UP:
            stage = "up"
```

Ortalama açı 130°'nin altına düşünce `stage` "up" olarak işaretlenir. Bu "kol kıvrıldı, yukarıya ulaştı" anlamına gelir. Henüz tekrar sayılmaz, sadece "up" pozisyonu not edilir.

```python
        elif avg_angle > ANGLE_DOWN and stage == "up":
            stage = "down"
            rep_count += 1
```

Bu satır **iki koşulu birden** kontrol eder:

1. `avg_angle > ANGLE_DOWN` → Açı 160°'yi aştı mı? (kol aşağı indi)
2. `stage == "up"` → Daha önce "up" pozisyonuna ulaşıldı mı?

**Her iki koşul da True ise:** kol önce yukarı kıvrılmış, sonra aşağı indirilmiş → `1 tam tekrar tamamlandı` → `rep_count += 1`

`stage == "up"` koşulu olmasaydı ne olurdu? Video başında kol aşağıda dururken bile sayaç artardı. Bu koşul sayesinde sayaç sadece yukarı→aşağı sıralamasında çalışır.

---

### 15. Bilgi Paneli (HUD)

```python
        cv2.rectangle(frame, (0, 0), (340, 90), (0, 0, 0), cv2.FILLED)
```

Sol üst köşeye siyah bir dikdörtgen çizer. Bu yazıların arka planı, arkadaki hareketli görüntünün yazıyı okunamaz hale getirmesini önler:

- `(0, 0)` → sol üst köşe
- `(340, 90)` → sağ alt köşe (340px geniş, 90px yüksek)
- `(0, 0, 0)` → siyah renk
- `cv2.FILLED` → içi dolu dikdörtgen

```python
        cv2.putText(frame, f"Tekrar: {rep_count}", (10, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3)
```

Tekrar sayısını büyük yeşil yazıyla sol üst köşeye yazar:

- `f"Tekrar: {rep_count}"` → dinamik string, sayı her artışta güncellenir
- `(10, 48)` → yazının sol-alt başlangıç noktası (x=10, y=48)
- `1.3` → büyük font boyutu (diğer yazılardan büyük, önemli bilgi olduğu için)
- `(0, 255, 0)` → yeşil renk
- `3` → kalın yazı

```python
        cv2.putText(frame, f"Asama: {stage if stage else '-'}  Aci: {int(avg_angle)}", (10, 78),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
```

Mevcut aşamayı ve anlık açı değerini küçük beyaz yazıyla yazar:

- `stage if stage else '-'` → stage `None` ise tire göster, değer varsa değeri göster. Python'da None'ı doğrudan string içine koymak `"None"` yazar — bunun yerine `-` daha temiz görünür.
- `int(avg_angle)` → ondalıklı açıyı tam sayıya yuvarlar (daha temiz görünüm)
- `(10, 78)` → tekrar yazısının 30px altına konumlandırılmış
- `(255, 255, 255)` → beyaz renk

---

### 16. Görüntü Göster ve Çıkış

```python
    cv2.imshow("Sayac", frame)
```

Her kareyi "Sayac" başlıklı pencerede gösterir. Üzerinde iskelet, açı değerleri ve bilgi paneli bulunan işlenmiş kare ekrana yansır.

```python
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

1ms klavye dinler. `q` tuşuna basılırsa döngüden çıkar. `& 0xFF` bit maskeleme platforma bağımsız güvenilir çalışmayı sağlar.

---

### 17. Kaynakları Serbest Bırak

```python
video.release()
```

Video dosyasını kapatır ve sistem kaynaklarını serbest bırakır.

```python
cv2.destroyAllWindows()
```

Açık tüm OpenCV pencerelerini kapatır.

---

## 📐 Açı Hesabının Geometrik Mantığı

```
        OMUZ (a)
         \
          \   ← bu açı ölçülüyor
           \
          DİRSEK (b)  ← köşe noktası
           /
          /
         /
       BİLEK (c)
```

`atan2` fonksiyonu her iki kenarın yatay eksene göre açısını bulur, farkları alınca dirsekteki açı elde edilir.

| Kol Pozisyonu                   | Yaklaşık Açı |
| ------------------------------- | ------------ |
| Tamamen düz (aşağı sarkık)      | ~170-180°    |
| Hafif bükülmüş                  | ~130-160°    |
| Tam kıvrılmış (bicep curl üstü) | ~30-60°      |

---

## 🔄 Tekrar Sayma Mantığının Akışı

```
Başlangıç: stage = None, rep_count = 0

  Kol aşağıda (açı > 160°)
       │
       │  Kol kıvrılıyor...
       ▼
  Kol yukarıda (açı < 130°)
  → stage = "up"
       │
       │  Kol indiriliyor...
       ▼
  Kol aşağıda (açı > 160°) VE stage == "up"
  → stage = "down"
  → rep_count += 1  ✅ Tekrar sayıldı!
       │
       └── Döngü devam eder...
```

---

## 🔄 Programın Genel Akışı

```
Başla
  │
  ├─► Video dosyasını aç
  ├─► MediaPipe Pose modelini hazırla
  ├─► rep_count = 0, stage = None
  │
  └─► DÖNGÜ (video bitene veya q tuşuna kadar)
        │
        ├─► Video'dan kare oku
        ├─► Video bittiyse (ret=False) → döngüden çık
        ├─► Kareyi aynala (flip)
        ├─► BGR → RGB dönüştür
        ├─► MediaPipe ile poz tespiti yap
        │
        ├─► Poz tespit edildi mi?
        │     ├─ EVET →
        │     │    ├─ İskelet çiz
        │     │    ├─ 6 eklem noktasının koordinatını al (2 omuz, 2 dirsek, 2 bilek)
        │     │    ├─ Sol ve sağ dirsek açısını hesapla
        │     │    ├─ Ortalama açıyı hesapla
        │     │    ├─ Açı değerlerini dirseklerin yanına yaz
        │     │    ├─ Tekrar sayma mantığını çalıştır
        │     │    └─ Bilgi panelini (HUD) çiz
        │     └─ HAYIR → Atla
        │
        ├─► Kareyi ekranda göster
        │
        └─► Q tuşuna basıldı mı?
              ├─ EVET → Döngüden çık
              └─ HAYIR → Döngünün başına dön

Video dosyasını kapat
Pencereleri kapat
Bitir
```

---

## 🚀 Geliştirme Fikirleri

- **Farklı egzersizler:** Diz açısı ölçülerek squat sayacı, omuz açısıyla shoulder press sayacı yapılabilir.
- **Ses bildirimi:** `playsound` veya `beep` kütüphanesiyle her tekrarda ses çıkarılabilir.
- **Eşik ayarı:** `ANGLE_UP` ve `ANGLE_DOWN` değerlerini trackbar (kaydırma çubuğu) ile canlı değiştirilebilir hale getirmek mümkündür.
- **Kamera desteği:** `"video.mp4"` yerine `0` yazılırsa canlı kamera ile çalışır.
- **Tek kol modu:** Sadece sağ veya sol kol için ayrı sayaçlar oluşturulabilir.
- **Görünürlük kontrolü:** `lm.visibility > 0.6` koşuluyla sadece kameraya net görünen noktalar kullanılabilir.
- **CSV kaydı:** Her tekrarda zaman damgası ve açı değerlerini dosyaya yazarak antrenman geçmişi oluşturulabilir.

---

## ⚠️ Sık Karşılaşılan Sorunlar

| Sorun                            | Olası Neden                          | Çözüm                                                  |
| -------------------------------- | ------------------------------------ | ------------------------------------------------------ |
| `video.mp4` bulunamadı           | Dosya farklı klasörde                | Tam yol ver: `cv2.VideoCapture("C:/klasor/video.mp4")` |
| Sayaç çok hızlı artıyor          | `ANGLE_UP` ve `ANGLE_DOWN` çok yakın | Aralarındaki farkı büyüt (örn. 120 ve 170)             |
| Sayaç hiç artmıyor               | Açı eşikleri harekete uygun değil    | `print(avg_angle)` ile açıları izle, eşikleri ayarla   |
| İskelet yanlış çiziliyor         | Kişi kameraya tam dönük değil        | Kişinin tam olarak kameraya baktığı videoyu kullan     |
| Program video bitmeden kapanıyor | `if not ret: break` doğru çalışıyor  | Normal davranış, video bitince program kapanır         |

---

## 🔀 Önceki Kodlarla Karşılaştırma

| Özellik             | El Takibi      | Poz Kestirimi    | Egzersiz Sayacı     |
| ------------------- | -------------- | ---------------- | ------------------- |
| Kaynak              | Kamera (canlı) | Kamera (canlı)   | Video dosyası       |
| Model               | `hands`        | `pose`           | `pose`              |
| Tespit              | 21 el noktası  | 33 vücut noktası | 33 vücut noktası    |
| Ek hesap            | Yok            | Yok              | Açı hesabı (`math`) |
| Çıktı               | Görsel iskelet | Görsel iskelet   | Sayaç + açı bilgisi |
| Ayna efekti         | Var            | Yok              | Var                 |
| Video sonu kontrolü | Yok            | Yok              | Var (`if not ret`)  |
