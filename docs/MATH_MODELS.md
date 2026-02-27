# 🧮 TEKNOFEST AUV: Matematiksel Alt Yapı ve Modeller

Bu döküman, Mavi Vatan projesinde otonom seyrüsefer ve veri işleme sırasında kullanılan temel matematiksel prensipleri ve algoritmaları açıklar.

---

## 1. Navigasyon ve Stabilizasyon (PID Kontrol)
AUV'nin derinlik kilitlenmesi ve yönelimi, klasik ama yüksek hassasiyetli bir **PID (Proportional-Integral-Derivative)** kontrolcü ile sağlanır.

### Denklemler
Derleme anındaki çıktı (Output) kontrolü şu formülle hesaplanır:

$$ u(t) = K_p e(t) + K_i \int e(t) dt + K_d \frac{de(t)}{dt} $$

- **$K_p$ (Proportional):** Mevcut hataya orantılı tepki verir.
- **$K_i$ (Integral):** Geçmişteki toplam hataları kompanse eder (offsetleri giderir).
- **$K_d$ (Derivative):** Hatadaki değişim hızına bakarak gelecekteki aşımı (overshoot) engeller.

---

## 2. Akıllı Rota Planlama (Bezier Eğrileri)
İki nokta arasındaki keskin dönüşleri hidrodinamik olarak yumuşatmak için **Quadratic Bezier** yöntemi kullanılır.

### Formülasyon
$P_0$ (başlangıç), $P_1$ (kontrol) ve $P_2$ (bitiş) noktaları için eğri denklemi:

$$ B(t) = (1-t)^2 P_0 + 2(1-t)t P_1 + t^2 P_2, \quad t \in [0, 1] $$

Bu yöntem, motorların ani dur-kalk yapmasını engelleyerek enerji tasarrufu ve akışkan hareket sağlar.

---

## 3. Sensör Füzyonu (Kalman Filtresi)
Sensörlerden gelen (Sonar, Basınç vb.) istatistiksel gürültüyü temizlemek için **Kalman Filtresi** kullanılır.

### Algoritma Basamakları

1.  **Prediction (Tahmin):** 
    - $\hat{x}_k^- = \hat{x}_{k-1}$
    - $P_k^- = P_{k-1} + Q$
2.  **Kalman Gain (Kazanç):**
    - $K_k = P_k^- / (P_k^- + R)$
3.  **Update (Güncelleme):**
    - $\hat{x}_k = \hat{x}_k^- + K_k (z_k - \hat{x}_k^-)$
    - $P_k = (1 - K_k) P_k^-$

---

## 4. Hedef Takip ve Hata Vektörü
Kamera merkezinden ($C_x, C_y$) hedefin merkezine ($T_x, T_y$) olan hata vektörü:

$$ \vec{E} = [T_x - C_x, T_y - C_y] $$

Bu vektör, `tracker.py` tarafından PID kontrolcü girişine beslenerek aracın otonom olarak hizalanmasını sağlar.

---

> [!NOTE]
> Bu modeller, TEKNOFEST 2026 yarışma standartlarına uygun hassasiyette ve Python ortamında performanslı bir şekilde koşturulmaktadır.
