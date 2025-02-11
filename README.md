# 🧟‍♂️ Zombi Oyunu

Bu proje, **Python ve Pygame Zero** kullanılarak geliştirilmiş **bir zombi hayatta kalma oyunudur**. Oyuncu, ana karakteri yön tuşlarıyla kontrol eder ve **düşmanları etkisiz hale getirmek için bir bıçak fırlatabilir**. Oyunda **5 seviye (level)** bulunmaktadır ve her seviyede düşman sayısı artmaktadır.


- Oyun, **Pygame Zero kullanarak geliştirilmiştir**.
- **Ses efektleri ve müzikler** özel olarak eklenmiştir ve oyundaki olaylara göre tetiklenmektedir.
- **Düşmanlar rastgele yerleştirilmekte ve ana karaktere doğru yönelmektedir**.
- **Oyun içinde dinamik hız artışı** mevcuttur.
- **Animasyonlar, sprite çerçeveleri kullanılarak gerçekleştirilmiştir**.

## 🎮 Oyun Mekanikleri

### 🦸‍♂️ Ana Karakter (Oyuncu)
- **Can (HP):** 20
- **Hız:** 5
- **Güç:** 2
- **Yön Tuşları:** Hareket etmek için `← ↑ ↓ →` tuşlarını kullanın.
- **Bıçak Fırlatma:** `Enter` tuşuna basarak bıçağı yönünüze doğru atabilirsiniz.

### 🧟‍♂️ Düşman Türleri ve Özellikleri
Oyun **3 farklı düşman** içerir:
1. **Hayalet:** 
   - Güç: 3
   - Hız: 1 (En yavaş düşman)
   - Can: 6 (Orta dayanıklılık)
2. **Örümcek:** 
   - Güç: 2
   - Hız: 2 (Orta hız)
   - Can: 4 (Orta dayanıklılık)
3. **Batman:** 
   - Güç: 1
   - Hız: 4 (En hızlı düşman)
   - Can: 2 (En düşük dayanıklılık)

### 📈 Seviye (Level) Sistemi
- Oyun **5 seviyeden oluşur**.
- **Her seviyede düşman sayısı artar**:
  - **1. Seviye:** 1 Batman, 1 Hayalet, 1 Örümcek
  - **2. Seviye:** 2 Batman, 2 Hayalet, 2 Örümcek
  - **3. Seviye:** 3 Batman, 3 Hayalet, 3 Örümcek
  - **4. Seviye:** 4 Batman, 4 Hayalet, 4 Örümcek
  - **5. Seviye:** 5 Batman, 5 Hayalet, 5 Örümcek
- **Her yeni seviyede düşmanların hızı artar.**

---

## 🖼️ Kullanılan Dosyalar ve Assetler

### 📂 `images/enemy/` (Düşman Görselleri)
- **batman.png** → Batman düşmanı için sprite.
- **hayalet.png** → Hayalet düşmanı için sprite.
- **orumcek.png** → Örümcek düşmanı için sprite.

### 📂 `images/` (Ana Karakter ve Çevre)
- **anakarakter.png** → Ana karakterin duruşu.
- **anakarakter1.png** → Ana karakterin animasyon için alternatif sprite.
- **bicak.png** → Oyuncunun fırlattığı bıçak.
- **duvar.png** → Oyunda kullanılan duvar görselleri.

### 📂 `music/` (Müzikler)
- **music1.wav** → Ana menü müziği.
- **music2.wav** → Oyun içi müzik (Oyun başladığında çalar).

### 📂 `sounds/` (Ses Efektleri)
- **bicak.wav** → Bıçak fırlatma sesi (`Enter` tuşuna basıldığında çalar).
- **canazal.wav** → Karakterin canı azaldığında çalar.
- **dusmanoldu.wav** → Bir düşman öldüğünde çalar.



## 🎨 Oyun Mekanikleri & Animasyonlar

### 🎭 **Sprite Animasyonları**
- **Ana karakter ve düşmanlar için animasyonlu sprite kullanılır.** 
- **Karakter hareket ederken farklı sprite çerçeveleri geçiş yaparak gerçekçi bir hareket hissi oluşturur.**
- **Düşmanlar hareket ederken nefes alma veya farklı çerçevelerde değişim gösterir.**

---

## 🎯 Oyun Kazanma/Kaybetme Koşulları
- **Eğer karakterin canı sıfıra düşerse** → Oyun sona erer ve **ana menüye geri döner**.
- **Eğer oyuncu 5. seviyeyi tamamlayıp tüm düşmanları öldürürse** → **Oyunu kazanır!** 🎉

---

## 🔄 Oyun Döngüsü

1. Oyuncu **ana menüde başlar**.
2. **"Play Game"** butonuna basarak oyuna girer.
3. Oyuncu **hareket eder ve düşmanları bıçak fırlatarak öldürmeye çalışır**.
4. Tüm düşmanlar öldüğünde **bir sonraki seviyeye geçer**.
5. Oyuncu ölürse **ana menüye döner**.
6. **5. seviye tamamlandığında oyuncu oyunu kazanır**.
