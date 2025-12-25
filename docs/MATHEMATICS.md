# 📐 Projenin Matematiksel ve Fiziksel Temelleri

Bu döküman, TEKNOFEST İSA projesinin arkasında yatan ileri düzey mühendislik hesaplamalarını ve fiziksel kuralları içerir.

---

## 1. Akışkanlar Mekaniği ve Hidrodinamik

### 1.1. Sürüklenme Kuvveti (Drag Force)
Aracın su içindeki hareket direncini belirleyen temel denklem:
$$F_D = \frac{1}{2} \rho v^2 C_D A$$
Burada:
- $\rho$: Suyun yoğunluğu ($1025\text{ kg/m}^3$ deniz suyu için)
- $v$: Aracın hızı
- $C_D$: Sürüklenme katsayısı (Gövde formuyla optimize edilmiştir)
- $A$: Islak alan

### 1.2. Kaldırma Kuvveti ve Statik Kararlılık
Arşimet prensibi ve metasentrik yükseklik:
$$F_B = \rho \cdot g \cdot V_{total}$$
Kararlılık momenti ($M_R$):
$$M_R = (CB - CG) \cdot \sin(\theta) \cdot F_B$$

---

## 2. Kontrol Sistemleri (Aviyonik)

### 2.1. 6-DOF PID Kontrol
Aracın 6 serbestlik derecesindeki hata sönümleme algoritması:
$$u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt}$$

### 2.2. EKF (Extended Kalman Filter) Konum Tahmini
GPS'siz konumlandırmada durum güncelleme denklemi:
1. **Tahmin:** $\hat{x}_{k|k-1} = f(\hat{x}_{k-1|k-1}, u_k)$
2. **Kovaryans Tahmini:** $P_{k|k-1} = F_k P_{k-1|k-1} F_k^T + Q_k$

---

## 3. Akustik ve Optik Haberleşme

### 3.1. Su Altı Ses Hızı (Mackenzie Denklemi)
$$c = 1448.96 + 4.591T - 5.304 \times 10^{-2} T^2 + 2.374 \times 10^{-4} T^3 + \dots$$

### 3.2. Sinyal Sönümlenmesi (Attenuation)
Beer-Lambert Kanunu (Işık için):
$$I = I_0 e^{-\alpha d}$$
Burada $\alpha$ soğurma katsayısıdır ve mavi ışık (470nm) için en düşük değerdedir.

---

## 4. Otonom Rota Planlama

### 4.1. Yapay Potansiyel Alanları (APF)
Toplam potansiyel enerji:
$$U_{total} = U_{attractive} + U_{repulsive}$$
Kuvvet vektörü:
$$\vec{F} = -\nabla U_{total}$$
