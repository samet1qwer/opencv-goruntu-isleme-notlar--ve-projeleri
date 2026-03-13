# 🐍 Python Görüntü İşleme Notları

> **NumPy · Pandas · Matplotlib · OpenCV** ile kapsamlı görüntü işleme rehberi  
> Her kod satırının altında ne yaptığı açıklanmıştır.

---

## 📋 İçindekiler

1. [NumPy — Temel Dizi İşlemleri](#1-numpy--temel-dizi-i̇şlemleri)
2. [Pandas — Veri Analizi](#2-pandas--veri-analizi)
3. [Matplotlib — Grafik ve Görselleştirme](#3-matplotlib--grafik-ve-görselleştirme)
4. [OpenCV — Resim Okuma ve Kaydetme](#4-opencv--resim-okuma-ve-kaydetme)
5. [OpenCV — Resim Boyutlandırma ve Kırpma](#5-opencv--resim-boyutlandırma-ve-kırpma)
6. [OpenCV — Şekil ve Metin Çizme](#6-opencv--şekil-ve-metin-çizme)
7. [OpenCV — Resim Birleştirme (hstack / vstack)](#7-opencv--resim-birleştirme-hstack--vstack)
8. [OpenCV — Resim Karıştırma (Blending)](#8-opencv--resim-karıştırma-blending)
9. [OpenCV — Video Okuma ve Oynatma](#9-opencv--video-okuma-ve-oynatma)
10. [OpenCV — Kamera ve Video Kaydetme](#10-opencv--kamera-ve-video-kaydetme)
11. [OpenCV — Görüntü Bulanıklaştırma (Blur)](#11-opencv--görüntü-bulanıklaştırma-blur)
12. [OpenCV — Görüntü Eşikleme (Thresholding)](#12-opencv--görüntü-eşikleme-thresholding)
13. [OpenCV — Kenar Bulma (Edge Detection)](#13-opencv--kenar-bulma-edge-detection)
14. [OpenCV — Morfolojik İşlemler](#14-opencv--morfolojik-i̇şlemler)
15. [OpenCV — Histogram İşlemleri](#15-opencv--histogram-i̇şlemleri)
16. [OpenCV — Perspektif Düzeltme](#16-opencv--perspektif-düzeltme)
17. [OS Modülü — Dosya ve Klasör İşlemleri](#17-os-modülü--dosya-ve-klasör-i̇şlemleri)

---

## 1. NumPy — Temel Dizi İşlemleri

> NumPy (Numerical Python), sayısal hesaplamalar ve matris işlemleri için kullanılan temel kütüphanedir. Görüntüler de aslında birer NumPy dizisidir.

---

### 📌 1.1 — Array Oluşturma ve Shape

```python
import numpy as np
```

> `numpy` kütüphanesini `np` kısaltmasıyla içe aktarıyoruz. Bu standart bir gelenektir.

```python
dizi = np.array([1, 2, 3, 4, 5, 6, 78, 9, 8, 7])
```

> `np.array(...)` → Python listesini NumPy dizisine dönüştürür.  
> Normal Python listelerinden farkı: tüm elemanlar aynı tipte olur ve matematiksel işlemler çok daha hızlıdır.

```python
print(dizi.shape)
```

> `.shape` → dizinin boyutlarını tuple olarak verir.  
> Bu dizi 10 elemanlı ve tek boyutlu olduğu için çıktı `(10,)` şeklindedir.  
> 2D bir dizi için örnek çıktı: `(2, 5)` → 2 satır, 5 sütun

---

### 📌 1.2 — Reshape (Yeniden Boyutlandırma)

```python
dizi2 = dizi.reshape(2, 5)
```

> `.reshape(satır, sütun)` → mevcut diziyi yeniden şekillendirir.  
> Burada 10 elemanlı 1D dizi → 2 satır, 5 sütunluk 2D diziye dönüştürülür.  
> ⚠️ Toplam eleman sayısı değişmez: `2 × 5 = 10` ✓

```python
print(dizi2.ndim)
```

> `.ndim` → kaç boyutlu olduğunu verir. 2D dizi için `2` döner.

```python
print(dizi2.dtype.name)
```

> `.dtype.name` → dizideki elemanların veri tipini verir.  
> Tam sayılardan oluştuğu için genellikle `int64` döner.

```python
print(dizi2.size)
```

> `.size` → dizideki toplam eleman sayısını verir. Burada `10`.

---

### 📌 1.3 — Sıfır, Bir ve Boş Matrisler

```python
np.zeros((3, 5))
```

> Tüm elemanları `0.0` olan 3 satır 5 sütunluk bir matris oluşturur.  
> Görüntü işlemede "boş/siyah bir tuval" oluşturmak için sık kullanılır.

```python
np.ones((4, 6))
```

> Tüm elemanları `1.0` olan 4×6'lık matris. Maske oluşturmada işe yarar.

```python
np.empty((2, 3))
```

> Boyutu belirtilmiş ama içi **rastgele ve tanımsız** değerlerle dolu bir dizi.  
> `zeros`'tan daha hızlıdır çünkü sıfırlama yapmaz — değerleri sonradan dolduracaksanız kullanın.

---

### 📌 1.4 — Aralık Dizileri

```python
np.arange(10, 500, 10)
```

> `arange(başlangıç, bitiş, adım)` → 10'dan başlayıp 500'e kadar (500 dahil değil) 10'ar 10'ar gider.  
> Çıktı: `[10, 20, 30, ..., 490]`

```python
np.linspace(10, 20, 20)
```

> `linspace(başlangıç, bitiş, adet)` → 10 ile 20 arasında **eşit aralıklı** tam olarak 20 nokta üretir.  
> `arange`'den farkı: adım yerine **kaç tane nokta** istediğinizi belirtirsiniz.

---

### 📌 1.5 — Matematiksel İşlemler

```python
np.max(dizi)
```

> Dizideki en büyük değeri bulur. `dizi.max()` şeklinde de yazılabilir.

```python
np.min(dizi)
```

> Dizideki en küçük değeri bulur.

```python
np.sum(dizi)
```

> Tüm elemanları toplar.

```python
np.median(dizi)
```

> Diziyi sıralayıp ortadaki değeri (medyanı) döndürür. Ortalamadan farklıdır — aykırı değerlerden etkilenmez.

```python
np.sqrt(dizi)
```

> Her elemanın karekökünü alır (eleman bazlı işlem).  
> Örnek: `[1, 4, 9]` → `[1.0, 2.0, 3.0]`

---

### 📌 1.6 — Rastgele Dizi ve Düzleştirme

```python
rastgele = np.random.random((3, 5))
```

> 0 ile 1 arasında rastgele float değerler içeren 3×5'lik matris oluşturur.

```python
vektor = rastgele.ravel()
```

> `.ravel()` → çok boyutlu diziyi **tek boyutlu** (1D) düz bir diziye çevirir.  
> 3×5'lik matris → 15 elemanlı 1D dizi haline gelir.  
> `.flatten()` ile benzerdir ama `ravel()` mümkünse kopyalamadan çalışır (daha verimli).

---

## 2. Pandas — Veri Analizi

> Pandas, Excel benzeri tablo (DataFrame) yapılarında veri işleme kütüphanesidir.

---

### 📌 2.1 — DataFrame Oluşturma

```python
import pandas as pd
```

> Pandas'ı `pd` kısaltmasıyla içe aktarıyoruz.

```python
dictionary = {
    "isim": ["ali", "veli", "ayşe"],
    "yas" : [12, 34, 23],
    "maas": [111, 1232, 3455],
}
```

> Veri kaynağımız bir Python sözlüğü (dict).  
> Her **anahtar** bir sütun adı, her **liste** o sütunun değerleridir.

```python
veri = pd.DataFrame(dictionary)
```

> `pd.DataFrame(...)` → sözlüğü satır-sütun yapısına (tabloya) dönüştürür.

---

### 📌 2.2 — Temel Bilgi Fonksiyonları

```python
veri.head()
```

> Tablonun ilk 5 satırını gösterir. `head(10)` dersek ilk 10 satırı gösterir.

```python
veri.columns
```

> Tüm sütun adlarını bir liste gibi döndürür.

```python
veri.info()
```

> Her sütunun adını, kaç adet dolu (non-null) değer içerdiğini ve veri tipini gösterir.

```python
veri.describe()
```

> Sayısal sütunlar için istatistiksel özet: ortalama, std, min, max, çeyrekler.

---

### 📌 2.3 — Sütun Ekleme

```python
veri["sehir"] = ["ankara", "istanbul", "konya"]
```

> `veri["yeni_sutun"] = [...]` → tabloya yeni bir sütun ekler.  
> Liste uzunluğu satır sayısıyla eşit olmalıdır, aksi hâlde hata alınır.

---

### 📌 2.4 — loc ve iloc ile Seçim

```python
veri.loc[:2, "yas"]
```

> `loc[satır_aralığı, sütun_adı]` → etiket (isim) bazlı seçim yapar.  
> `:2` → 0, 1, 2. satırları seçer. **Not:** `loc`'ta son değer dahildir!

```python
veri.loc[:2, "yas":"sehir"]
```

> Birden fazla sütunu aralık olarak seçer: yaş'tan şehir'e kadar tüm sütunlar (her ikisi de dahil).

```python
veri.loc[::-1, :]
```

> `::-1` → tüm satırları ters sırada getirir (son satır önce). `:` → tüm sütunlar.

```python
veri.iloc[:, 1]
```

> `iloc[satır, sütun]` → **konum** (indeks numarası) bazlı seçim yapar.  
> `:` → tüm satırlar. `1` → 1. indeksteki sütun.  
> `loc`'tan farkı: sütun adı değil, sıra numarası kullanır.

---

### 📌 2.5 — Filtreleme

```python
veri[veri["yas"] > 30]
```

> `veri["yas"] > 30` → her satır için True/False üretir.  
> Bu True/False maskesini tabloya uygulayınca sadece `True` olan satırlar gelir.

```python
veri[veri["maas"] > 3000]
```

> Maaşı 3000'den büyük olan satırları filtreler.

```python
veri[veri["sehir"] == "ankara"]
```

> Şehri tam olarak "ankara" olan satırları filtreler.

---

### 📌 2.6 — Gruplama ve Sıralama

```python
veri.groupby("sehir")["maas"].mean()
```

> `.groupby("sehir")` → aynı şehirdeki kişileri gruplar.  
> `["maas"]` → grupların maaş sütununu seç.  
> `.mean()` → her grup için ortalama maaşı hesapla.

```python
veri.sort_values("maas")
```

> Tabloyu maaş sütununa göre küçükten büyüğe sıralar.

```python
veri.sort_values("yas", ascending=False)
```

> `ascending=False` → büyükten küçüğe (azalan) sıralar.

---

### 📌 2.7 — Birleştirme

```python
birlesik = pd.concat([veri, veri2])
```

> İki tabloyu **alt alta** (satır bazlı) birleştirir. Sütun adları aynı olmalıdır.

```python
merge = pd.merge(data1, data2, on="isim")
```

> İki tabloyu **"isim" sütununu ortak anahtar** kabul ederek yan yana birleştirir.  
> SQL'deki `JOIN` işlemine benzer.

---

### 📌 2.8 — CSV Okuma / Yazma

```python
veri.to_csv("veri.csv", index=False)
```

> Tabloyu CSV dosyasına yazar.  
> `index=False` → satır numaralarını (0,1,2...) ayrı sütun olarak **yazma** anlamına gelir.

```python
okunan = pd.read_csv("veri.csv")
```

> CSV dosyasını okuyup tekrar DataFrame'e dönüştürür.

---

## 3. Matplotlib — Grafik ve Görselleştirme

---

### 📌 3.1 — Temel Çizgi ve Scatter Grafik

```python
import matplotlib.pyplot as plt
import numpy as np
```

```python
x = np.array([1, 2, 3, 4, 5, 6])
y = np.array([6, 5, 4, 3, 2, 1])
```

> Grafikte kullanacağımız x ve y eksen değerleri.

```python
plt.figure()
```

> Yeni boş bir grafik penceresi (canvas) açar. Birden fazla grafik çiziyorsak her birinden önce çağırılmalıdır.

```python
plt.plot(x, y, color="red", alpha=0.7, label="line")
```

> Noktaları birleştiren çizgi grafiği çizer.  
> `color="red"` → çizgi rengi kırmızı.  
> `alpha=0.7` → %70 opaklık (0=tamamen şeffaf, 1=tamamen opak).  
> `label="line"` → lejanda görünecek isim.

```python
plt.scatter(x, y, color="blue", alpha=0.5, label="scatter")
```

> Her noktayı ayrı ayrı nokta olarak çizer, çizgi çizmez.  
> `plot()` ile birlikte aynı grafiğe üst üste eklenebilir.

```python
plt.title("Grafik Başlığı")
plt.xlabel("X Ekseni")
plt.ylabel("Y Ekseni")
```

> Sırasıyla başlık, X ekseni etiketi ve Y ekseni etiketi ekler.

```python
plt.grid(True)
```

> Arka planda ızgara (grid) çizgileri gösterir. Değerleri okumayı kolaylaştırır.

```python
plt.xticks([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8])
```

> X ekseninde hangi değerlerde işaret (tick) olacağını manuel olarak belirler.

```python
plt.legend()
```

> Grafikteki her elemanın `label=` ile tanımladığı isimleri bir kutu içinde gösterir.

```python
plt.show()
```

> Grafiği ekrana çizer ve gösterir. Bu satır olmadan grafik görünmez.

---

### 📌 3.2 — Pandas ile Grafik Türleri

```python
df.plot()
```

> DataFrame'deki tüm sayısal sütunları tek grafikte çizgi olarak çizer.

```python
df.plot.scatter(x="A", y="B")
```

> "A" sütununu X, "B" sütununu Y ekseni olarak kullanıp dağılım grafiği çizer.

```python
df["A"].plot.hist(bins=20)
```

> "A" sütunundaki değerlerin dağılımını histogram olarak gösterir.  
> `bins=20` → değer aralığını 20 eşit dilime böler.

```python
df.head().plot.bar()
```

> İlk 5 satırı çubuk grafik olarak gösterir.

---

### 📌 3.3 — Görüntü Gösterme

```python
resim = np.random.rand(50, 50)
plt.imshow(resim)
plt.colorbar()
plt.show()
```

> `np.random.rand(50,50)` → 50×50 piksellik rastgele değerli gri görüntü.  
> `plt.imshow(resim)` → görüntüyü renkli harita (colormap) ile gösterir.  
> `plt.colorbar()` → sağ tarafa renk skalasını gösteren çubuk ekler.

```python
resim_rgb = np.random.rand(100, 100, 3)
plt.imshow(resim_rgb)
```

> `(100, 100, 3)` → 100×100 piksel, 3 kanal (R, G, B). Renkli görüntü.

> ⚠️ **Kritik Fark:** OpenCV görüntüleri **BGR** sırasında saklar, Matplotlib **RGB** bekler.  
> Dönüşüm: `img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`

---

## 4. OpenCV — Resim Okuma ve Kaydetme

---

### 📌 4.1 — Resim Okuma

```python
import cv2
```

> OpenCV kütüphanesini `cv2` adıyla içe aktarır.

```python
img = cv2.imread("resim.jpg")
```

> `imread(dosya_yolu)` → görüntüyü diskten okuyup NumPy dizisi olarak döndürür.  
> Varsayılan olarak renkli (BGR) okur.  
> ⚠️ Dosya bulunamazsa hata vermez — `None` döner. Kontrol etmek önemlidir.

```python
img = cv2.imread("resim.jpg", 0)
```

> `0` = `cv2.IMREAD_GRAYSCALE` → gri tonlamalı (siyah-beyaz) okur.  
> Gri görüntünün shape'i `(yükseklik, genişlik)` olur — 3. kanal yoktur.

```python
img = cv2.imread("resim.jpg", -1)
```

> `-1` = `cv2.IMREAD_UNCHANGED` → alfa kanalıyla birlikte okur.  
> PNG gibi şeffaflık destekleyen formatlarda 4 kanallı `(H, W, 4)` dizi döner.

---

### 📌 4.2 — Resim Gösterme ve Tuş Kontrolü

```python
cv2.imshow("pencere_adi", img)
```

> `imshow(pencere_adı, görüntü)` → belirtilen isimde bir pencere açar ve görüntüyü içinde gösterir.

```python
k = cv2.waitKey(0) & 0xFF
```

> `waitKey(0)` → bir tuşa basılana kadar bekler.  
> `0` yerine ms değeri verilirse o kadar bekler (örn. `waitKey(25)` = 25ms).  
> Basılan tuşun ASCII kodunu döndürür.  
> `& 0xFF` → bazı sistemlerde üst bitler anlamsız olur, maskeleme ile sadece alt 8 biti alıyoruz.

```python
if k == 27:
    cv2.destroyAllWindows()
```

> `27` → ESC tuşunun ASCII kodu. ESC'ye basılırsa tüm pencereleri kapat.

```python
elif k == ord('s'):
    cv2.imwrite("kaydedilen.png", img)
    cv2.destroyAllWindows()
```

> `ord('s')` → 's' harfinin ASCII kodunu verir (115).  
> `imwrite(dosya_adı, görüntü)` → görüntüyü diske yazar.  
> Format, dosya uzantısından otomatik anlaşılır: .png, .jpg, .bmp vb.

---

## 5. OpenCV — Resim Boyutlandırma ve Kırpma

---

### 📌 5.1 — Boyut Bilgisi

```python
print(img.shape)
```

> Görüntü aslında bir NumPy dizisidir.  
> `.shape` → `(yükseklik, genişlik, kanal_sayısı)` döner.  
> Örnek çıktı: `(480, 640, 3)` → 480px yüksek, 640px geniş, 3 kanallı (BGR).  
> Gri görüntü için: `(480, 640)` — 3. boyut yoktur.

---

### 📌 5.2 — Boyut Değiştirme

```python
imgResized = cv2.resize(img, (800, 800))
```

> `resize(görüntü, (yeni_genişlik, yeni_yükseklik))` → görüntüyü yeniden boyutlandırır.  
> ⚠️ **Dikkat:** `shape`'ten farklı olarak burada önce **genişlik**, sonra **yükseklik** yazılır!

---

### 📌 5.3 — Kırpma (Crop)

```python
imgCropped = img[:200, 100:]
```

> Görüntü NumPy dizisi olduğu için NumPy dilimleme (slicing) kullanılır.  
> Sözdizimi: `img[y_başlangıç : y_bitiş, x_başlangıç : x_bitiş]`  
> `:200` → y ekseninde 0'dan 200'e kadar (ilk 200 satır).  
> `100:` → x ekseninde 100'den sonuna kadar (100. pikselden itibaren).  
> ⚠️ Önce **satır (y)**, sonra **sütun (x)** yazılır!

---

## 6. OpenCV — Şekil ve Metin Çizme

---

### 📌 6.1 — Boş (Siyah) Resim Oluşturma

```python
import numpy as np
img = np.zeros((512, 512, 3), np.uint8)
```

> `np.zeros(...)` → tüm piksel değerleri 0 olan siyah bir görüntü oluşturur.  
> `(512, 512, 3)` → 512px yükseklik, 512px genişlik, 3 kanal (BGR).  
> `np.uint8` → pikseller 0–255 arasında 8-bit tam sayı olarak saklanır.  
> Üzerine şekil çizmek için "boş tuval" görevi görür.

---

### 📌 6.2 — Çizgi

```python
cv2.line(
    img,          # üzerine çizileceği görüntü
    (0, 0),       # başlangıç noktası (x, y)
    (212, 212),   # bitiş noktası (x, y)
    (0, 0, 255),  # renk: BGR formatında → bu kırmızıdır
    3             # çizgi kalınlığı piksel cinsinden
)
```

> `line(görüntü, pt1, pt2, renk, kalınlık)` → iki nokta arasına düz çizgi çizer.  
> Koordinatlar `(x, y)` şeklindedir — sol üst köşe `(0, 0)`'dır.  
> OpenCV'de renkler **BGR** sırasındadır (Blue, Green, Red — RGB'nin tersi!).

---

### 📌 6.3 — Dikdörtgen

```python
cv2.rectangle(
    img,
    (100, 100),      # sol üst köşe (x, y)
    (200, 200),      # sağ alt köşe (x, y)
    (121, 200, 50),  # renk (BGR)
    3                # kalınlık → -1 verilirse içi dolu dikdörtgen olur
)
```

> İki köşe noktası verilerek dikdörtgen çizilir.  
> `kalınlık = -1` → dikdörtgenin içi tamamen belirtilen renkle doldurulur.

---

### 📌 6.4 — Çember

```python
cv2.circle(
    img,
    (300, 300),     # merkez noktası (x, y)
    45,             # yarıçap piksel cinsinden
    (230, 120, 32), # renk (BGR)
    3               # kalınlık → -1 verilirse içi dolu çember olur
)
```

> Merkez ve yarıçap verilerek çember çizilir.

---

### 📌 6.5 — Metin Yazma

```python
cv2.putText(
    img,
    "Merhaba",                 # yazılacak metin
    (230, 250),                # metnin sol alt köşesinin konumu (x, y)
    cv2.FONT_HERSHEY_COMPLEX,  # font tipi
    1,                         # font ölçeği (büyüklük çarpanı)
    (255, 255, 255),           # renk (BGR) → beyaz
    2                          # kalınlık piksel
)
```

> `putText(...)` → görüntünün üzerine metin yazar.  
> Konum, metnin **sol alt** köşesini belirtir.  
> Font tipleri: `FONT_HERSHEY_SIMPLEX`, `FONT_HERSHEY_COMPLEX`, `FONT_HERSHEY_DUPLEX` vb.

---

### 📌 BGR Renk Tablosu

| Renk    | BGR Değeri        |
| ------- | ----------------- |
| Kırmızı | `(0, 0, 255)`     |
| Yeşil   | `(0, 255, 0)`     |
| Mavi    | `(255, 0, 0)`     |
| Beyaz   | `(255, 255, 255)` |
| Siyah   | `(0, 0, 0)`       |
| Sarı    | `(0, 255, 255)`   |
| Mor     | `(255, 0, 255)`   |

---

## 7. OpenCV — Resim Birleştirme (hstack / vstack)

---

```python
img = cv2.imread("resim.png")
```

> Birleştirmek istediğimiz resmi okuyoruz.

```python
hor = np.hstack((img, img))
```

> `np.hstack(...)` → resimleri **yatay** olarak (yan yana) birleştirir.  
> "horizontal stack" → sağa doğru ekler.  
> ⚠️ Resimlerin **yükseklikleri** aynı olmalıdır.

```python
ver = np.vstack((img, img))
```

> `np.vstack(...)` → resimleri **dikey** olarak (alt alta) birleştirir.  
> "vertical stack" → aşağıya doğru ekler.  
> ⚠️ Resimlerin **genişlikleri** aynı olmalıdır.

```python
cv2.waitKey(0)
cv2.destroyAllWindows()
```

> `waitKey(0)` → herhangi bir tuşa basılana kadar pencereleri açık tut.  
> `destroyAllWindows()` → tuşa basıldıktan sonra tüm OpenCV pencerelerini kapat.

---

## 8. OpenCV — Resim Karıştırma (Blending)

---

```python
img1 = cv2.imread("img1.jpg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
```

> `cvtColor(görüntü, dönüşüm_kodu)` → renk uzayını dönüştürür.  
> OpenCV BGR okur, Matplotlib RGB gösterir — bu satır olmadan renkler yanlış görünür.

```python
img1 = cv2.resize(img1, (600, 600))
img2 = cv2.resize(img2, (600, 600))
```

> `addWeighted` için iki resmin **boyutları eşit** olmak zorundadır.  
> Her ikisini de 600×600'e getiriyoruz.

```python
blended = cv2.addWeighted(
    img1, 0.8,   # img1 ve ağırlığı → %80 görünür
    img2, 0.2,   # img2 ve ağırlığı → %20 görünür
    0.0          # gamma: her piksele eklenecek sabit parlaklık değeri
)
```

> `addWeighted(src1, alpha, src2, beta, gamma)` → iki görüntüyü karıştırır.  
> Formülü: `çıktı = (img1 × 0.8) + (img2 × 0.2) + 0.0`  
> `alpha + beta = 1.0` olması önerilir; toplamları 1'den büyükse görüntü aşırı parlak olur.  
> `gamma` → tüm piksel değerlerine eklenen sabit parlaklık offseti. Genellikle `0.0` bırakılır.

---

## 9. OpenCV — Video Okuma ve Oynatma

---

```python
cap = cv2.VideoCapture("video.mp4")
```

> `VideoCapture(kaynak)` → video dosyası veya kamera açar.  
> Bu işlem videoyu RAM'e **yüklemez** — kareler sonradan tek tek okunur.

```python
print(cap.get(3))   # genişlik
print(cap.get(4))   # yükseklik
```

> `cap.get(özellik_numarası)` → video hakkında bilgi döndürür.  
> `3` = `CAP_PROP_FRAME_WIDTH` → genişlik  
> `4` = `CAP_PROP_FRAME_HEIGHT` → yükseklik  
> Diğer özellikler: `5` = FPS, `7` = toplam kare sayısı

```python
if cap.isOpened() == False:
    print("video acilirken hata olustu")
```

> `isOpened()` → video/kamera başarıyla açıldı mı? `True/False` döner.  
> Dosya bulunamazsa ya da codec desteklenmiyorsa `False` döner.

```python
while True:
    res, frame = cap.read()
```

> `cap.read()` → videodan bir sonraki kareyi okur.  
> İki değer döndürür:  
> `res` → okuma başarılı mı? (`True`/`False`)  
> `frame` → okunan kare (NumPy dizisi olarak görüntü)

```python
    if res == True:
        time.sleep(0.01)
        cv2.imshow("video", frame)
```

> `res == True` → kare başarıyla okunduysa göster.  
> `time.sleep(0.01)` → 10ms bekle. Video çok hızlı oynuyorsa yavaşlatmak için kullanılır.  
> `imshow` → kareyi pencerede gösterir. Döngüde her turda aynı pencere güncellenir.

```python
    else:
        break
```

> `res == False` → video bitti veya okuma hatası → döngüden çık.

```python
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

> `waitKey(1)` → 1ms bekle ve tuş kontrolü yap.  
> Video oynatırken küçük bir değer verilmelidir — büyük değer videoyu takıltır.  
> Q tuşuna basılırsa döngüden çık.

```python
cap.release()
cv2.destroyAllWindows()
```

> `cap.release()` → video dosyasını serbest bırakır, sistem kaynağını geri verir.  
> Bu satır olmadan dosya kilitli kalabilir.

---

## 10. OpenCV — Kamera ve Video Kaydetme

---

```python
cap = cv2.VideoCapture(0)
```

> `0` → bilgisayardaki ilk (varsayılan) kamerayı açar. `1` ikinci kamerayı açar.

```python
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
```

> Kameranın çözünürlüğünü alıyoruz.  
> `int(...)` → `cap.get()` float döndürür, `VideoWriter` tam sayı ister.

```python
writer = cv2.VideoWriter(
    "kayit.mp4",                       # kaydedilecek dosyanın adı
    cv2.VideoWriter_fourcc(*"DIVX"),   # video codec (sıkıştırma formatı)
    20,                                 # FPS: saniyede kaç kare kaydedilsin
    (width, height)                     # çözünürlük (genişlik, yükseklik)
)
```

> `VideoWriter(...)` → video kayıt nesnesi oluşturur.  
> `VideoWriter_fourcc(*"DIVX")` → DIVX codec kodunu 4 karakterden üretir.  
> `*"DIVX"` ifadesi `'D','I','V','X'` şeklinde açılır (string unpacking).  
> `20` FPS → 20 kare/saniye. Gerçek zamanlı kaydediyorsak kameranın FPS değeriyle eşleşmeli.

```python
writer.write(frame)
```

> `write(kare)` → döngünün her turunda kareyi video dosyasına ekler.

```python
writer.release()
```

> Video dosyasını kapatır ve diske yazar. Bu satır olmadan dosya bozuk olabilir!

---

## 11. OpenCV — Görüntü Bulanıklaştırma (Blur)

> Bulanıklaştırma, piksel değerini komşularıyla birleştirerek keskin geçişleri yumuşatır. Gürültü azaltma ve kenar tespiti öncesi ön işlem olarak kullanılır.

---

```python
img = cv2.imread("resim.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

> Resmi okuyup BGR → RGB'ye çeviriyoruz (Matplotlib ile göstereceğiz diye).

### 📌 11.1 — Ortalama Blur

```python
dst = cv2.blur(img, (3, 3))
```

> Her pikselin değerini, etrafındaki 3×3 piksel alanının **ortalamasıyla** değiştirir.  
> `(3, 3)` → kernel (filtre penceresi) boyutu. Büyüdükçe bulanıklaşma artar.  
> Basit ve hızlıdır ama kenarları da bulanıklaştırır.

---

### 📌 11.2 — Gaussian Blur ⭐

```python
gb = cv2.GaussianBlur(
    img,
    (3, 3),   # kernel boyutu — tek sayı olmalı: 3, 5, 7...
    sigmaX=7  # x yönündeki Gaussian standart sapması
)
```

> Ortalama blur'dan farkı: merkeze yakın piksellere **daha fazla ağırlık** verir (Gaussian dağılımı).  
> Bu sayede doğal ve yumuşak bir bulanıklık elde edilir.  
> `sigmaX` büyüdükçe bulanıklaşma artar. `0` verilirse kernel boyutundan otomatik hesaplanır.  
> Görüntü işlemede en yaygın kullanılan blur yöntemidir.

---

### 📌 11.3 — Medyan Blur

```python
mb = cv2.medianBlur(img, 3)
```

> Her pikseli, komşu alandaki **medyan (ortanca)** değerle değiştirir.  
> Tuz-biber (salt & pepper) gürültüsüne karşı çok etkilidir.  
> `3` → kernel boyutu — tek sayı olmak zorunda: 3, 5, 7...  
> Ortalama yerine medyan alır, bu yüzden aykırı (gürültü) piksellerden etkilenmez.

---

## 12. OpenCV — Görüntü Eşikleme (Thresholding)

> Eşikleme: her pikseli bir eşikle karşılaştırıp siyah veya beyaz yaparak ikili (binary) görüntü oluşturur. Nesne tespiti için temeldir.

---

```python
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

> Threshold işlemleri tek kanallı (gri) görüntüde yapılır.  
> BGR görüntüyü gri tonlamaya çevirir. Shape `(H, W, 3)` → `(H, W)` olur.

### 📌 12.1 — Basit Eşikleme

```python
_, thresh_img = cv2.threshold(
    img,
    thresh=60,             # eşik değeri (0–255 arası)
    maxval=255,            # eşiği geçen piksele atanacak değer
    type=cv2.THRESH_BINARY
)
```

> `threshold(...)` → iki değer döndürür: kullanılan eşik sayısı ve eşiklenmiş görüntü.  
> `_` → ilk değeri (eşik sayısını) yok sayıyoruz.  
> `THRESH_BINARY` kuralı: piksel > 60 ise → 255 (beyaz), piksel ≤ 60 ise → 0 (siyah).  
> Sonuç: görüntü siyah-beyaza dönüşür.

---

### 📌 12.2 — Adaptif Eşikleme

```python
thresh_img2 = cv2.adaptiveThreshold(
    img,
    255,                           # eşiği geçen piksele atanacak değer
    cv2.ADAPTIVE_THRESH_MEAN_C,    # her bölge için eşiği komşuların ortalamasından hesapla
    cv2.THRESH_BINARY,             # binary threshold uygula
    11,                            # blok boyutu: kaç×kaç piksel alanda yerel eşik hesaplanır
    8                              # C sabiti: hesaplanan eşikten çıkarılır (ince ayar)
)
```

> **Neden adaptif?** Aydınlatma her yerde eşit değilse sabit bir eşik işe yaramaz.  
> Adaptif yöntem görüntüyü küçük bloklara böler, her blok için ayrı eşik hesaplar.  
> `blok boyutu = 11` → her piksel için 11×11'lik komşuluk alanı kullanılır (tek sayı olmalı).  
> `C = 8` → hesaplanan ortalamadan 8 çıkarılır. Sonucu ince ayar yapmak için kullanılır.

---

## 13. OpenCV — Kenar Bulma (Edge Detection)

> Kenar, bir görüntüde piksel yoğunluğunun hızlı değiştiği bölgedir. Kenar tespiti bu değişimleri bulmak için türev hesaplar.

---

### 📌 13.1 — Sobel Operatörü

```python
sobelx = cv2.Sobel(img, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
```

> `Sobel(görüntü, derinlik, dx, dy, ksize)`  
> `ddepth=cv2.CV_64F` → çıktı görüntünün piksel derinliği 64-bit float olsun. Negatif değerleri kaybetmemek için gereklidir.  
> `dx=1, dy=0` → x yönünde birinci türevi al, y yönünde türev alma. Bu **dikey kenarları** bulur.  
> `ksize=5` → Sobel filtresinin boyutu (5×5). Büyüdükçe daha geniş kenarlar bulunur.

```python
sobely = cv2.Sobel(img, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
```

> `dx=0, dy=1` → y yönünde türev alır. **Yatay kenarları** bulur.

---

### 📌 13.2 — Laplacian Operatörü

```python
laplacian = cv2.Laplacian(img, cv2.CV_64F)
```

> Laplacian, ikinci türevi kullanır ve tüm yönlerdeki kenarları aynı anda bulur.  
> Sobel'in aksine hem yatay hem dikey kenarları tek seferde tespit eder.  
> Gürültüye daha duyarlıdır — öncesinde `GaussianBlur` uygulamak iyi bir pratiktir.

> 💡 **İpucu:** En iyi sonuç için Sobel X ve Y'yi birleştir:
>
> ```python
> magnitude = np.sqrt(sobelx**2 + sobely**2)
> ```

---

## 14. OpenCV — Morfolojik İşlemler

> Morfolojik işlemler, binary/gri görüntülerde şekil tabanlı dönüşümler yapar.

---

```python
img = cv2.imread("resim.jpg", 0)   # 0 → gri olarak oku
kernel = np.ones((5, 5), np.uint8)
```

> `np.ones((5,5), np.uint8)` → içi tamamen 1'lerden oluşan 5×5'lik kernel.  
> Kernel (yapısal eleman), görüntü üzerinde kaydırılan filtre matrisidir.  
> Boyutu büyüdükçe işlemin etkisi artar.

---

### 📌 14.1 — Erozyon (Erosion)

```python
result = cv2.erode(img, kernel, iterations=2)
```

> Kerneli görüntü üzerinde kaydırır. Bir bölgedeki tüm pikseller beyaz değilse o bölgeyi siyah yapar.  
> **Efekt:** beyaz alanları küçültür, ince çizgileri ve küçük gürültüleri siler.  
> `iterations=2` → işlemi 2 kez uygular. Daha fazla iterasyon = daha fazla erozyon.

---

### 📌 14.2 — Genişleme (Dilation)

```python
genisleme = cv2.dilate(img, kernel, iterations=1)
```

> Kerneli kaydırır. Bölgede en az bir piksel beyazsa tüm bölgeyi beyaz yapar.  
> **Efekt:** beyaz alanları büyütür, kırık çizgileri birleştirir, boşlukları doldurur.  
> Erozyonun tam tersi etkiyi yapar.

---

### 📌 14.3 — Opening, Closing, Gradient

```python
acilma = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
```

> **Opening = Erosion → Dilation**  
> Önce erozyon (küçük beyaz gürültüleri siler), sonra dilation (asıl nesneyi geri getirir).  
> Kullanım: görüntüdeki küçük beyaz lekeleri/gürültüleri temizlemek.

```python
kapatma = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
```

> **Closing = Dilation → Erosion**  
> Önce dilation (siyah delikleri kapatır), sonra erosion (asıl şekli geri getirir).  
> Kullanım: nesnelerin içindeki küçük siyah boşlukları kapatmak.

```python
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
```

> **Gradient = Dilation − Erosion**  
> Genişletilmiş görüntüden erozyonlanmış görüntüyü çıkarır.  
> **Efekt:** nesnenin yalnızca kenar çizgisini ortaya çıkarır.

---

## 15. OpenCV — Histogram İşlemleri

> Histogram: görüntüdeki her piksel yoğunluk değerinden (0–255) kaç tane olduğunu gösteren grafiktir.

---

### 📌 15.1 — Tek Kanal Histogram

```python
hist = cv2.calcHist(
    [img],          # görüntü — liste içinde verilmeli
    channels=[0],   # hangi kanal: 0=Blue, 1=Green, 2=Red
    mask=None,      # None = tüm görüntü kullanılır
    histSize=[256], # kaç adet bin: 256 → her değer için bir bin
    ranges=[0, 256] # piksel değer aralığı
)
```

> `calcHist(...)` → verilen kanalın histogram verisini döndürür.  
> Çıktı `(256, 1)` boyutlu bir dizi — her indeks o yoğunlukta kaç piksel olduğunu söyler.

---

### 📌 15.2 — RGB Kanal Histogramı

```python
color = ("b", "g", "r")
for i, c in enumerate(color):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(hist, color=c)
```

> `enumerate(color)` → hem indeks `i` hem de renk adı `c` alınır.  
> Her kanal için ayrı histogram hesaplanıp aynı grafiğe çizilir.  
> R, G, B kanallarının dağılımı ayrı ayrı görülmüş olur.

---

### 📌 15.3 — Mask ile Histogram

```python
mask = np.zeros(img.shape[:2], np.uint8)
```

> `img.shape[:2]` → `(yükseklik, genişlik)` — `[:2]` ile kanal sayısını almıyoruz.  
> Sıfırlardan oluşan (tamamen siyah) tek kanallı bir maske oluşturur.

```python
mask[100:300, 200:400] = 255
```

> Maskenin belirlenen bölgesini 255 (beyaz) yapar.  
> Bu beyaz bölge "dikkate alınacak alan" anlamına gelir. Geri kalanı (siyah) yok sayılır.

```python
masked_img = cv2.bitwise_and(img, img, mask=mask)
```

> `bitwise_and(src1, src2, mask)` → maskenin beyaz olduğu yerlerde orijinal görüntüyü, siyah olduğu yerlerde 0 döndürür.  
> Sonuç: görüntünün sadece seçili bölgesi görünür, geri kalanı siyah olur.

---

### 📌 15.4 — Histogram Equalization

```python
img_gray = cv2.imread("resim.jpg", 0)
eq_img = cv2.equalizeHist(img_gray)
```

> Gri görüntünün piksel dağılımını tüm 0–255 aralığına yayar.  
> **Efekt:** karanlık görüntülerde kontrastı artırır, detayları daha belirgin yapar.  
> ⚠️ Yalnızca gri (tek kanallı) görüntülerde çalışır.

---

## 16. OpenCV — Perspektif Düzeltme

> Kameraya eğik açıyla görünen nesneleri sanki tam önden bakıyormuşuz gibi düzleştirir.

---

```python
img = cv2.imread("kart.png")
width = 400    # üretilecek görüntünün genişliği
height = 500   # üretilecek görüntünün yüksekliği
```

```python
pts1 = np.float32([
    [230,   1],   # sol ust
    [  1, 472],   # sol alt
    [540, 150],   # sag ust
    [338, 617]    # sag alt
])
```

> Orijinal eğik görüntüdeki 4 köşe noktasının koordinatları `(x, y)`.  
> Bu noktalar genellikle fare ile tıklanarak veya görüntü incelenerek bulunur.  
> `np.float32` → `getPerspectiveTransform` fonksiyonu bu formatı gerektirir.  
> ⚠️ Sıralama kritiktir: `pts1` ve `pts2`'de aynı sıra kullanılmalıdır.

```python
pts2 = np.float32([
    [     0,      0],   # sol ust
    [     0, height],   # sol alt
    [ width,      0],   # sag ust
    [ width, height]    # sag alt
])
```

> Çıktı görüntüsünde noktaların gitmesini istediğimiz konumlar.  
> Bu noktalar dikdörtgenin 4 köşesi — yani düzleştirilmiş hali temsil eder.

```python
matrix = cv2.getPerspectiveTransform(pts1, pts2)
```

> `getPerspectiveTransform(kaynak, hedef)` → 3×3'lük bir dönüşüm matrisi hesaplar.  
> Bu matris, her kaynak pikselin hedefte nereye gideceğini matematiksel olarak tarif eder.

```python
output = cv2.warpPerspective(img, matrix, (width, height))
```

> `warpPerspective(görüntü, matris, çıktı_boyutu)` → hesaplanan matrisi uygular.  
> Her piksel koordinatı dönüştürülerek yeni görüntü oluşturulur.  
> Sonuç: eğik nesne düz bir dikdörtgen halinde karşımıza çıkar.

---

## 17. OS Modülü — Dosya ve Klasör İşlemleri

> `os` modülü, işletim sistemiyle etkileşim kurmak için kullanılır.

---

### 📌 17.1 — Temel Dosya Sistemi İşlemleri

```python
import os
```

```python
os.getcwd()
```

> "get current working directory" → Python'un şu an çalıştığı klasörün tam yolunu döndürür.  
> Örnek çıktı: `/home/kullanici/proje`

```python
os.mkdir("yeni_klasor")
```

> Belirtilen isimde yeni bir klasör oluşturur.  
> ⚠️ Klasör zaten varsa `FileExistsError` hatası alınır. Önce `os.path.exists()` ile kontrol edin.

```python
os.rmdir("klasor")
```

> Boş bir klasörü siler.  
> ⚠️ Klasörün içinde dosya varsa hata verir. İçi dolu klasörler için `shutil.rmtree()` kullanılır.

```python
os.listdir()
```

> Mevcut klasördeki tüm dosya ve klasörlerin isimlerini liste olarak döndürür.

---

### 📌 17.2 — Yol (Path) İşlemleri

```python
os.path.join("klasor", "dosya.txt")
```

> Yol parçalarını işletim sistemine uygun şekilde birleştirir.  
> Windows'ta `\`, Linux/Mac'te `/` kullanır.  
> Sonuç: `"klasor/dosya.txt"` (Linux) veya `"klasor\dosya.txt"` (Windows).  
> Manuel olarak `/` eklemek yerine bu fonksiyon tercih edilmeli — platform bağımsız çalışır.

```python
os.path.exists("yol")
```

> Belirtilen yol (dosya veya klasör) var mı? `True`/`False` döner.

```python
os.path.isfile("dosya.txt")
```

> Belirtilen yol bir **dosya** mı? `True`/`False` döner.

```python
os.path.isdir("klasor")
```

> Belirtilen yol bir **klasör** mü? `True`/`False` döner.

---

### 📌 17.3 — Pratik Kullanım Örneği

```python
# Klasor yoksa olustur (hata vermeden)
if not os.path.exists("output"):
    os.mkdir("output")
```

> `os.mkdir` öncesinde kontrol yaparak `FileExistsError` hatasını önleriz.

```python
# Bulunulan klasordeki tum .jpg dosyalarini listele
dosyalar = [f for f in os.listdir(".") if f.endswith(".jpg")]
print(dosyalar)
```

> `os.listdir(".")` → mevcut klasördeki tüm öğeleri listele.  
> `if f.endswith(".jpg")` → sadece .jpg uzantılı olanları al.  
> Bu liste kavrama (list comprehension), tek satırda hem döngü hem filtreleme yapar.

---

## Genel Hatırlatmalar

| Konu                       | Hatırlatma                                                                                |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| **Renk Formatı**           | OpenCV → **BGR** \| Matplotlib → **RGB**. Dönüşüm: `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` |
| **`img.shape` Sırası**     | `(yükseklik, genişlik, kanal)` — önce satır, sonra sütun                                  |
| **`resize()` Sırası**      | `(genişlik, yükseklik)` — shape'in tersi!                                                 |
| **Kırpma Sırası**          | `img[y1:y2, x1:x2]` — önce satır (y), sonra sütun (x)                                     |
| **Kernel Boyutu**          | Blur ve morfolojik işlemlerde **tek sayı** olmalı: 3, 5, 7...                             |
| **`waitKey()`**            | Video döngüsünde `waitKey(1)`, statik görüntüde `waitKey(0)` kullan                       |
| **Kaynak Serbest Bırakma** | `cap.release()` ve `writer.release()` **her zaman** çağırılmalı                           |
| **Pencere Kapatma**        | `cv2.destroyAllWindows()` — tüm OpenCV pencerelerini kapatır                              |
| **Dosya Bulunamazsa**      | `cv2.imread()` hata vermez, `None` döner — kontrol et!                                    |
| **Threshold → Gri**        | Eşikleme işlemi tek kanallı (gri) görüntüde yapılmalıdır                                  |

---

_Notlar tamamdır. Her bölüm bağımsız olarak çalıştırılabilir._
