# 👁️ Gerçek Zamanlı Göz Kırpma Sayacı (Blink Detection)

MediaPipe, OpenCV ve matematik ile kameradan canlı göz kırpma tespiti ve sayma uygulaması.

---

## 📸 Ne Yapar?

Bu program bilgisayarın kamerasını açar ve kare kare yüzü analiz eder. Gözün etrafındaki **4 adet kritik nokta** tespit edilerek gözün ne kadar açık olduğu matematiksel olarak hesaplanır. Göz kapandığında sayaç bir artırılır ve ekranın sol üst köşesinde anlık kırpma sayısı gösterilir.

Program ekranda şunları gösterir:

- 🕸️ **Yüz kontür çizgileri** — tüm yüz hatları
- 🔴 **4 adet kırmızı nokta** — göz köşeleri ve kapak noktaları
- 🟢 **Yeşil blink sayacı** — `Blinks: 5` gibi anlık sayım

---

## 🧠 Temel Fikir: EAR (Eye Aspect Ratio)

Göz kırpma tespitinin kalbi **EAR (Göz En-Boy Oranı)** formülüdür:

```
        dikey mesafe (üst kapak → alt kapak)
EAR = ─────────────────────────────────────────
        yatay mesafe (sol köşe → sağ köşe)
```

- **Göz açıkken:** dikey mesafe büyük → EAR yüksek (örn: `0.35`)
- **Göz kapanırken:** dikey mesafe küçülür → EAR düşer (örn: `0.10`)
- **EAR < 0.20** → göz kapalı sayılır → kırpma tespit edildi!
- **EAR > 0.25** → göz tekrar açık → bir sonraki kırpmaya hazır

---

## 🧰 Kullanılan Kütüphaneler

| Kütüphane      | Ne İçin Kullanılıyor?                                    |
| -------------- | -------------------------------------------------------- |
| `cv2` (OpenCV) | Kamera, aynalama, boyutlandırma, çizim, ekranda gösterme |
| `mediapipe`    | 468 noktalı yüz ağı tespiti                              |
| `math`         | İki nokta arası mesafe hesabı (`hypot`)                  |

### Kurulum

```bash
pip install opencv-python
pip install mediapipe
```

`math` Python'ın yerleşik kütüphanesidir, kurulum gerektirmez.

---

## 📄 Kodun Tamamı

```python
import cv2
import mediapipe as mp
import math

width = 400
height = 400

vide_cam = cv2.VideoCapture(0)

mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh()
mp_draw = mp.solutions.drawing_utils

blink_count = 0
blink_state = False

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

while True:
    ret, frame = vide_cam.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (width, height))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face.process(frame_rgb)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:

            mp_draw.draw_landmarks(frame, face_landmarks, mp_face.FACEMESH_CONTOURS)

            h, w, c = frame.shape
            points = {}

            for id, lm in enumerate(face_landmarks.landmark):
                if id in [33, 133, 159, 145]:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    points[id] = (cx, cy)
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

            if len(points) == 4:
                horizontal = distance(points[33],  points[133])
                vertical   = distance(points[159], points[145])
                ear = vertical / horizontal

                if ear < 0.2 and blink_state == False:
                    blink_count += 1
                    blink_state = True

                if ear > 0.25:
                    blink_state = False

    cv2.putText(frame, f"Blinks: {blink_count}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("Blink Detection", frame)

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

OpenCV kütüphanesi. Kamera açma, görüntü işleme, şekil ve metin çizme işlemleri bu kütüphaneden yapılır.

```python
import mediapipe as mp
```

Google'ın MediaPipe kütüphanesi. Yüzdeki 468 anatomik noktayı tespit eden FaceMesh modeli bu kütüphaneden gelir.

```python
import math
```

Python'ın yerleşik matematik kütüphanesi. Bu kodda yalnızca `math.hypot()` fonksiyonu için kullanılır — iki nokta arasındaki Öklid mesafesini hesaplar.

---

### 2. Boyut ve Kamera

```python
width = 400
height = 400
```

Görüntünün işleneceği ve gösterileceği piksel boyutu. `cv2.resize()` bu değerleri kullanacak.

```python
vide_cam = cv2.VideoCapture(0)
```

0 numaralı (varsayılan) kamerayı açar ve `vide_cam` nesnesine atar.

---

### 3. MediaPipe Hazırlığı

```python
mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh()
mp_draw = mp.solutions.drawing_utils
```

- `mp_face` → MediaPipe yüz ağı modülüne erişim kapısı
- `face` → FaceMesh modelini oluşturur ve çalışmaya hazır hale getirir (468 nokta tespiti)
- `mp_draw` → noktaları ve bağlantıları görüntüye çizen yardımcı araç

---

### 4. Sayaç Değişkenleri

```python
blink_count = 0
```

Toplam göz kırpma sayısını tutar. Program başladığında `0` olarak başlar, her kırpmada `+1` artar. Döngü boyunca sıfırlanmaz — programın tüm çalışma süresi boyunca birikimli sayar.

```python
blink_state = False
```

Gözün şu an kapalı olup olmadığını takip eden **durum bayrağı (state flag)**:

- `False` → göz açık, yeni kırpma sayılabilir
- `True` → göz hâlâ kapalı, aynı kırpma tekrar sayılmasın

**Bu değişken neden gerekli?**
Göz bir kez kapandığında kamera saniyede ~30 kare çekiyor. Göz kapalıyken her karede `blink_count += 1` yapılsaydı tek bir kırpma 10–15 sayılırdı. `blink_state` bunu önler:

- Göz kapanır → `blink_count += 1` → `blink_state = True` (artık sayma)
- Göz açılır → `blink_state = False` (artık yeni kırpma sayılabilir)

---

### 5. Mesafe Fonksiyonu

```python
def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])
```

İki nokta arasındaki **Öklid (düz çizgi) mesafesini** piksel cinsinden hesaplar.

`p1` ve `p2` birer koordinat demetidir: `(x, y)`

**`math.hypot` nasıl çalışır?**

İki nokta arasındaki mesafe Pisagor teoremiyle hesaplanır:

```
mesafe = √( (x2 - x1)² + (y2 - y1)² )
```

`math.hypot(a, b)` tam olarak `√(a² + b²)` hesaplar.

Yani:

```python
math.hypot(p2[0]-p1[0], p2[1]-p1[1])
#          └── Δx ──┘   └── Δy ──┘
# = √(Δx² + Δy²)
```

**Neden bu fonksiyon yazıldı?**
Aynı hesap kodda iki kez yapılacak (dikey ve yatay mesafe). Tekrar yazmak yerine fonksiyon tanımlanarak kod daha okunabilir ve bakımı kolay hale getirildi.

Örnek:

```python
distance((10, 20), (40, 60))
# Δx = 40 - 10 = 30
# Δy = 60 - 20 = 40
# mesafe = √(30² + 40²) = √(900 + 1600) = √2500 = 50.0
```

---

### 6. Ana Döngü — Kare Okuma ve Ön İşlem

```python
while True:
    ret, frame = vide_cam.read()
```

Sonsuz döngü başlar. `vide_cam.read()` kameradan bir sonraki kareyi okur:

- `ret` → okuma başarılı mı? (bu kodda kontrol edilmemiş)
- `frame` → BGR formatında NumPy dizisi olarak kare

```python
    frame = cv2.flip(frame, 1)
```

Görüntüyü yatay olarak aynalar. `1` = sol-sağ ters. Ayna etkisi: sağa eğilince ekranda da sağa eğilmiş görünürsün.

```python
    frame = cv2.resize(frame, (width, height))
```

Görüntüyü `(400, 400)` boyutuna getirir. Daha az piksel = daha hızlı işlem.

```python
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

BGR → RGB dönüşümü. MediaPipe RGB bekler, OpenCV BGR verir. `frame` (BGR) korunur — üzerine çizim yapılacak. `frame_rgb` yalnızca modele verilir.

```python
    result = face.process(frame_rgb)
```

RGB görüntüyü MediaPipe modeline verir. Model 468 yüz noktasını tespit eder, sonuçlar `result`'a yazılır.

---

### 7. Yüz Tespiti Kontrolü

```python
    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
```

Yüz tespit edildi mi kontrol edilir. Yüz yoksa `None` gelir, `None` üzerinde döngü açmak hata verir. `if` bu hatayı önler. Döngü tespit edilen her yüz için çalışır (varsayılan `max_num_faces=1`).

```python
            mp_draw.draw_landmarks(
                frame,
                face_landmarks,
                mp_face.FACEMESH_CONTOURS
            )
```

Tüm 468 yüz noktasının kontür çizgilerini `frame` üzerine çizer. Göz, kaş, dudak, burun ve yüz oval hatlarını gösterir.

---

### 8. Görüntü Boyutu ve Nokta Sözlüğü

```python
            h, w, c = frame.shape
```

Görüntü boyutlarını alır:

- `h` → yükseklik (400)
- `w` → genişlik (400)
- `c` → kanal sayısı (3: B, G, R)

Bir sonraki adımda normalize koordinatları piksel koordinatlarına çevirmek için `h` ve `w` kullanılacak.

```python
            points = {}
```

Sadece ihtiyacımız olan **4 noktanın koordinatlarını** saklamak için boş sözlük oluşturur. Anahtar: nokta ID'si, değer: `(cx, cy)` koordinat demeti.

Neden liste değil sözlük? ID numarasıyla doğrudan erişim için — `points[33]` ile sol göz köşesine anında ulaşılır, indeks saymaya gerek kalmaz.

---

### 9. Kritik 4 Nokta — Filtreleme ve Çizme

```python
            for id, lm in enumerate(face_landmarks.landmark):
                if id in [33, 133, 159, 145]:
```

468 noktanın tümü üzerinde döngü açılır ama yalnızca **4 tanesi** işlenir. `id in [33, 133, 159, 145]` koşuluyla diğer 464 nokta atlanır.

**Bu 4 nokta neden seçildi?**

MediaPipe FaceMesh'te sağ göz için şu noktalar kullanılır:

```
        159  ← üst kapak ortası
         │
33 ──────┼────── 133
(sol   │     (sağ
köşe)  │     köşe)
         │
        145  ← alt kapak ortası
```

| ID    | Konum                    | Rolü                       |
| ----- | ------------------------ | -------------------------- |
| `33`  | Gözün sol (iç) köşesi    | Yatay mesafenin başlangıcı |
| `133` | Gözün sağ (dış) köşesi   | Yatay mesafenin bitişi     |
| `159` | Üst göz kapağının ortası | Dikey mesafenin başlangıcı |
| `145` | Alt göz kapağının ortası | Dikey mesafenin bitişi     |

Bu 4 nokta sağ gözü temsil eder. Sol göz için farklı ID'ler gerekir (263, 362, 386, 374).

```python
                    cx, cy = int(lm.x * w), int(lm.y * h)
```

Normalize koordinatları (0.0–1.0) gerçek piksel koordinatlarına çevirir:

- `lm.x * w` → örn: `0.45 × 400 = 180` → x piksel konumu
- `lm.y * h` → örn: `0.30 × 400 = 120` → y piksel konumu
- `int()` → piksel koordinatı tam sayı olmalı

```python
                    points[id] = (cx, cy)
```

Hesaplanan koordinatı ID anahtarıyla sözlüğe ekler. Döngü bitince:

```python
points = {
    33:  (112, 198),   # sol köşe
    133: (176, 196),   # sağ köşe
    159: (142, 187),   # üst kapak
    145: (143, 205)    # alt kapak
}
```

```python
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
```

Her seçilen noktaya **kırmızı dolu daire** çizer:

- `(cx, cy)` → dairenin merkezi
- `4` → yarıçap 4 piksel (önceki versiyondan daha büyük — gözle görülebilsin)
- `(0, 0, 255)` → BGR kırmızı renk
- `-1` → `cv2.FILLED` ile aynı: daire içi dolu

---

### 10. EAR Hesabı — Göz Kırpma Tespiti

```python
            if len(points) == 4:
```

Sözlükte tam 4 nokta var mı kontrol eder. Bazı karelerde yüz kısmen dışarıda olabilir veya bir nokta tespit edilemeyebilir. 4'ten az nokta varsa bölme işlemi `KeyError` verebilir. Bu `if` o durumu önler.

```python
                horizontal = distance(points[33], points[133])
```

Sol köşe (33) ile sağ köşe (133) arasındaki **yatay mesafeyi** piksel olarak hesaplar. Bu değer gözün genişliğini temsil eder — başın eğilmesinden çok etkilenmez, kararlı bir referans değerdir.

```python
                vertical = distance(points[159], points[145])
```

Üst kapak (159) ile alt kapak (145) arasındaki **dikey mesafeyi** piksel olarak hesaplar. Göz açıkken büyük, kapanınca sıfıra yaklaşır.

```python
                ear = vertical / horizontal
```

**EAR (Eye Aspect Ratio)** değerini hesaplar:

```
        dikey   (üst kapak ↕ alt kapak)
EAR = ──────── = ──────────────────────────
       yatay    (sol köşe ↔ sağ köşe)
```

Örnek değerler:

```
Göz tamamen açık  → vertical ≈ 18px, horizontal ≈ 60px  → EAR ≈ 0.30
Göz yarı kapalı   → vertical ≈ 10px, horizontal ≈ 60px  → EAR ≈ 0.17
Göz tamamen kapalı→ vertical ≈  2px, horizontal ≈ 60px  → EAR ≈ 0.03
```

Yataya bölmenin amacı: kişiden kişiye göz boyutu farklı olabilir. Yatay mesafeye bölerek oran normalize edilir — büyük gözlü veya küçük gözlü herkes için aynı eşik değerleri çalışır.

---

### 11. Kırpma Sayma Mantığı

```python
                if ear < 0.2 and blink_state == False:
                    blink_count += 1
                    blink_state = True
```

**Kırpma tespit edildi mi?** iki koşulun aynı anda sağlanması gerekir:

- `ear < 0.2` → EAR eşik değerinin altına düştü, göz kapandı
- `blink_state == False` → bu kırpma daha önce sayılmadı (göz az önce açıktı)

Her iki koşul sağlanırsa:

- `blink_count += 1` → sayacı bir artır
- `blink_state = True` → "bu kırpma sayıldı" olarak işaretle, göz tekrar açılana kadar bir daha sayma

```python
                if ear > 0.25:
                    blink_state = False
```

**Göz tekrar açıldı mı?** EAR `0.25`'in üzerine çıktıysa göz açılmış demektir:

- `blink_state = False` → bir sonraki kırpmayı saymak için bayrağı sıfırla

**Neden kapatma eşiği `0.2`, açma eşiği `0.25`?**
İki farklı eşik değeri **histerezis (hysteresis)** oluşturur. `0.2` ile `0.25` arasında bir tampon bölge var. Eşik tek bir değer olsaydı (örn: her ikisi de `0.2`) gözün bu değerin tam üstünde-altında salınması her karede durum değiştirebilirdi → yanlış kırpma sayımı. Farklı eşikler bu "titreşimi" önler.

---

### 12. Sayacı Ekrana Yaz

```python
    cv2.putText(frame, f"Blinks: {blink_count}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
```

Kırpma sayısını ekranın sol üst köşesine yazar. Parametreler:

- `frame` → metnin yazılacağı görüntü
- `f"Blinks: {blink_count}"` → f-string ile sayaç değerini dinamik olarak metne ekler (örn: `"Blinks: 7"`)
- `(20, 60)` → metnin sol-alt başlangıç noktası: soldan 20px, yukarıdan 60px
- `cv2.FONT_HERSHEY_SIMPLEX` → sade, okunaklı font tipi
- `1.5` → font ölçeği (büyüklük çarpanı) — büyük ve okunabilir
- `(0, 255, 0)` → BGR yeşil renk — kırmızı noktalar ve beyaz çizgilerden ayrışır
- `3` → yazı kalınlığı 3 piksel

> ⚠️ Bu satır `if result.multi_face_landmarks:` bloğunun **dışında** — yüz tespit edilmese bile sayaç ekranda görünmeye devam eder. Yüz çerçeve dışına çıksa da sayaç silinmez.

---

### 13. Görüntüyü Göster ve Çıkış Kontrolü

```python
    cv2.imshow("Blink Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

İşlenmiş kareyi `"Blink Detection"` penceresinde gösterir. `waitKey(1)` hem 1ms bekler hem de `imshow`'un render edebilmesi için OpenCV event loop'unu çalıştırır. `q` tuşuna basılınca `break` ile döngüden çıkılır.

---

### 14. Kaynakları Serbest Bırak

```python
vide_cam.release()
cv2.destroyAllWindows()
```

- `vide_cam.release()` → kamerayı kapatır, işletim sistemine geri verir, LED söner
- `cv2.destroyAllWindows()` → tüm OpenCV pencerelerini kapatır, ekran belleğini temizler

---

## 🔄 Programın Genel Akışı

```
Başla
  │
  ├─► Kamerayı aç
  ├─► MediaPipe FaceMesh modelini hazırla
  ├─► blink_count = 0, blink_state = False
  │
  └─► DÖNGÜ (sonsuz)
        │
        ├─► Kameradan kare oku          (vide_cam.read)
        ├─► Kareyi yatay aynala         (cv2.flip)
        ├─► Kareyi 400×400'e getir      (cv2.resize)
        ├─► BGR → RGB dönüştür          (cv2.cvtColor)
        ├─► Yüz ağı tespiti yap         (face.process)
        │
        ├─► Yüz tespit edildi mi?
        │     └─ EVET → Her yüz için:
        │           │
        │           ├─► Kontür çizgilerini çiz   (draw_landmarks)
        │           ├─► Boş points = {} sözlüğü oluştur
        │           │
        │           └─► Her 468 nokta için:
        │                 ├─► ID 33, 133, 159, 145'ten biri mi?
        │                 │     ├─ EVET →
        │                 │     │    ├─► Piksel koordinatlarını hesapla (cx, cy)
        │                 │     │    ├─► points[id] = (cx, cy) olarak kaydet
        │                 │     │    └─► Kırmızı daire çiz
        │                 │     └─ HAYIR → Atla
        │           │
        │           ├─► points'te 4 nokta var mı?
        │                 └─ EVET →
        │                       ├─► Yatay mesafe hesapla (33 ↔ 133)
        │                       ├─► Dikey mesafe hesapla (159 ↔ 145)
        │                       ├─► EAR = dikey / yatay
        │                       │
        │                       ├─► EAR < 0.2 VE blink_state == False?
        │                       │     └─ EVET → blink_count += 1, blink_state = True
        │                       │
        │                       └─► EAR > 0.25?
        │                             └─ EVET → blink_state = False
        │
        ├─► Sayacı ekrana yaz           (cv2.putText)
        ├─► Kareyi ekranda göster       (cv2.imshow)
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

| Yenilik                          | Açıklama                                           |
| -------------------------------- | -------------------------------------------------- |
| `import math`                    | Mesafe hesabı için                                 |
| `blink_count`                    | Kırpma sayacı değişkeni                            |
| `blink_state`                    | Aynı kırpmayı tekrar saymayı önleyen durum bayrağı |
| `distance()` fonksiyonu          | İki nokta arası Öklid mesafesi hesabı              |
| `if id in [33,133,159,145]`      | 468 noktadan sadece 4'ünü seçme filtresi           |
| `points{}` sözlüğü               | Seçilen 4 noktayı ID ile saklama                   |
| `horizontal / vertical`          | Yatay ve dikey mesafe hesabı                       |
| `ear = vertical / horizontal`    | EAR (Eye Aspect Ratio) hesabı                      |
| `if ear < 0.2` / `if ear > 0.25` | Histerezisli kırpma tespiti                        |
| `cv2.putText`                    | Sayacı ekrana yazdırma                             |

---

## 🚀 Geliştirme Fikirleri

- **Her iki gözü izle:** Sol göz için `id in [263, 362, 386, 374]` noktaları eklenerek her iki göz ayrı ayrı takip edilebilir, ortalamaları alınabilir.
- **EAR değerini ekranda göster:** `cv2.putText(frame, f"EAR: {ear:.2f}", ...)` ile anlık EAR değeri ekrana yazdırılabilir — eşik ayarını kolaylaştırır.
- **Göz yorgunluğu uyarısı:** Belirli sayıda kırpmadan sonra (örn: 30 kırpma) ekranda uyarı mesajı gösterilebilir.
- **Uyuklama tespiti:** Göz çok uzun süre kapalı kalırsa (`blink_state == True` bir eşik süre aşılırsa) alarm tetiklenebilir.
- **Sürücü uyanıklık sistemi:** Araç içinde kamera ile kırpma sıklığı ölçülerek sürücünün uykuya dalmak üzere olduğu tespit edilebilir.
- **Sayacı sıfırlama:** `r` tuşuna basınca `blink_count = 0` yapılabilir.

---

## ⚠️ Sık Karşılaşılan Sorunlar

| Sorun                      | Olası Neden                        | Çözüm                                            |
| -------------------------- | ---------------------------------- | ------------------------------------------------ |
| Kırpmalar sayılmıyor       | EAR eşiği çok düşük                | `0.2` yerine `0.25` dene                         |
| Her kırpma 2–3 sayılıyor   | Eşik değerleri çok yakın           | `< 0.20` ve `> 0.30` gibi daha geniş aralık dene |
| Nokta yok, sadece çizgiler | `if id in [...]` koşulu eşleşmiyor | ID listesini kontrol et: `[33, 133, 159, 145]`   |
| ZeroDivisionError          | `horizontal == 0` (yüz tam yandan) | `if horizontal > 0:` kontrolü ekle               |
| Yüz tespit edilmiyor       | Karanlık ortam veya çok yakın      | İyi aydınlatma, 40–80 cm mesafe                  |
| `mediapipe` bulunamadı     | Kütüphane kurulu değil             | `pip install mediapipe` çalıştır                 |
