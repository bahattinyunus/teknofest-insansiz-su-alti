# 📊 Stratejik Rakip Analizi (Global Benchmarking)

Bu döküman, **Mavi Vatan** projesinin dünyadaki en başarılı AUV ekipleri (RoboSub ve SAUVC şampiyonları) ile teknik karşılaştırmasını ve projemizin bu devler arasındaki konumunu analiz eder.

---

## 🏎️ Karşılaştırma Matrisi

| Kriter | Cornell (CUAUV) | NUS (Bumblebee) | Duke Robotics | **Mavi Vatan (TR)** |
| :--- | :--- | :--- | :--- | :--- |
| **Yazılım Mimarisi** | Custom (Asynchronous) | ROS / ROS 2 | ROS 2 | **Python / Modular State Machine** |
| **Sensör Füzyonu** | EKF & DVL Fusion | Error State KF (ESKF) | PID & Feedforward | **Kalman Filter (Fused Depth)** |
| **Kontrol Mantığı** | Numerical Optimization | State Feedback | PID + Num. Allocation | **PID Tuner (Dynamic Profiles)** |
| **Donanım Stack** | Custom Transducer / BMS | Intel Core i7 / NVMe | Dual Power Grids | **Lightweight Embedded** |
| **Görev Yönetimi** | Modular Autonomy | Behavior Trees | State Machines | **Bezier Path + Mission Planner** |
| **Görüntü İşleme** | Custom Vision | OpenCV / YOLO | Stereo Vision | **YOLOv11 / Vision-Tracker** |

---

## 🧠 Teknik Analiz ve Çıkarımlar

### 1. Yazılım ve Kontrol (CUAUV vs Mavi Vatan)
- **CUAUV:** Çok karmaşık bir sayısal optimizasyon (Thrust Allocation) kullanıyor. Bu, enerji verimliliğini artırsa da yüksek işlem gücü gerektirir.
- **Mavi Vatan:** Bizim `PIDTuner` modülümüz, çalışma anında profil değiştirebilme (Stable/Agressive) yeteneği ile operasyonel esneklik sunar.

### 2. Algılama ve Füzyon (NUS vs Mavi Vatan)
- **BBAUV (NUS):** Error State Kalman Filter (ESKF) ve DVL kullanarak milimetrik konumlandırma yapıyor.
- **Mavi Vatan:** `KalmanFilter` modülümüz, derinlik dalgalanmalarını süzerek şartnamedeki (Theme 2) otonom intikal için kararlı bir temel oluşturur.

### 3. Görev Planlama (Duke vs Mavi Vatan)
- **Duke:** Robot-agnostic (robottan bağımsız) bir ROS 2 mimarisi üzerine kurulu.
- **Mavi Vatan:** `PathPlanner` (Bezier eğrileri) modülümüz, Duke'un mimarisine benzer şekilde hidrodinamik yumuşatma sağlayarak aracın sarsıntısız ilerlemesini sağlar.

---

## 🚩 Mavi Vatan'ın Stratejik Avantajları

1. **Şartnameye Tam Adaptasyon:** Rakipler genel RoboSub kurallarına odaklanırken, Mavi Vatan **TEKNOFEST 2026** temalarına (Mini ROV, Torpido Atışı, Koordinat Nav.) doğrudan entegre edilmiştir.
2. **Hafifletilmiş Mimari:** Dünya devleri 25-50 kg bandında araçlar üretirken, Mavi Vatan **11.5 kg** ağırlığı ile mobilite ve puanlama (Weight Bonus) avantajına sahiptir.
3. **Akademik Hazırlık:** Rakiplerin çoğunda bulunmayan detaylı `MATH_MODELS.md` dökümantasyonu ile sistemin matematiksel temeli şeffaf bir şekilde sunulmuştur.

---

> [!TIP]
> **Stratejik Hedef:** Milli Teknoloji Hamlesi vizyonuyla geliştirilen projemiz, küresel rakiplerin karmaşıklığını, yarışma şartnamesine odaklanmış "Yalın ve Etkin" bir mimari ile dengelemektedir.
