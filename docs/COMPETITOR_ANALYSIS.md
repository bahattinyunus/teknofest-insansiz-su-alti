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

## 🌊 Küresel Açık Kaynak Repo Kütüphanesi (Mega Link List)

Aşağıda, dünyadaki en başarılı AUV takımlarının ve yarışma otoritelerinin paylaştığı kaynak kodlar listelenmiştir. Bu kütüphane, **Mavi Vatan** projesinin küresel standartları nasıl takip ettiğinin bir kanıtıdır.

### 🇺🇸 RoboSub Şampiyonları & Devler
- **Cornell University (CUAUV):** 
  - [Ana Yazılım Yığını (Open Source)](https://github.com/cuauv/software)
  - [Scylla & Orion Modülleri](https://github.com/cuauv)
- **National University of Singapore (Bumblebee):**
  - [Bumblebee Autonomous Systems Organization](https://github.com/Bumblebee-Autonomous-Systems)
  - [ROS DevContainer & Simulation](https://github.com/Bumblebee-Autonomous-Systems/ros-devcontainer)
- **Duke Robotics:**
  - [RoboSub-ROS (Legacy)](https://github.com/DukeRobotics/robosub-ros)
  - [RoboSub-ROS 2 (Next Gen)](https://github.com/DukeRobotics/robosub-ros2)
- **UC Berkeley:**
  - [Berkeley AUV (RoboSub WS)](https://github.com/berkeleyauv/robosub_ws)
- **MIT ORCA:**
  - [Project ORCA Historical Code](https://github.com/topics/orca-auv)
- **University of Florida (UF-MIL):**
  - [MIL Monorepo (AUV & Projeler)](https://github.com/uf-mil/mil)
- **Ohio State University (OSU-UWRT):**
  - [Riptide Setup & Navigation](https://github.com/osu-uwrt/riptide_setup)
- **University of Southern Florida (USC):**
  - [Barracuda Control System](https://github.com/usc-robosub/barracuda-control)
  - [Barracuda Vision Pipeline](https://github.com/usc-robosub/barracuda-vision)

### 🇸🇬 SAUVC (Singapore AUV Challenge) Kaynakları
- **SAUVC Official:**
  - [SAUVC Organization (Tüm Yıllar)](https://github.com/sauvc)
  - [Rulebooks & Technical Docs](https://github.com/sauvc/rulebook)
- **Team Hydronautics (BMSTU):**
  - [Stingray Framework (AUV Core)](https://github.com/hydronautics-team/stingray)
  - [SAUVC Specific Implementation](https://github.com/hydronautics-team/sauvc)
- **SAUVC Simulators:**
  - [Adnan Sabbir - CV Simulator](https://github.com/adnansabbir/SAUVC-Simulator)
  - [AUV Society - Gazebo Simulations](https://github.com/auvsociety/sauvc-simulations)

### 🇪🇺 Avrupa & Diğer Global Projeler
- **Vortex NTNU (Norveç):**
  - [Vortex AUV Guidance & Control](https://github.com/vortexntnu/vortex-auv)
  - [AUV Simulator Extension](https://github.com/vortexntnu/vortex-auv-simulator)
- **BYU AUVSI:**
  - [Metis Path Planning](https://github.com/byu-auvsi/metis)
  - [Theseus Navigation Algorithms](https://github.com/byu-auvsi/theseus)
- **Team Inspiration:**
  - [2024 RoboSub Open Source](https://github.com/InspirationRobotics/inspiration_robosub)
  - [2025 Graph-Based Planner](https://github.com/InspirationRobotics/robosub_2025)

---

---

## 🚩 Mavi Vatan'ın Stratejik Avantajları

1. **Şartnameye Tam Adaptasyon:** Rakipler genel RoboSub kurallarına odaklanırken, Mavi Vatan **TEKNOFEST 2026** temalarına (Mini ROV, Torpido Atışı, Koordinat Nav.) doğrudan entegre edilmiştir.
2. **Hafifletilmiş Mimari:** Dünya devleri 25-50 kg bandında araçlar üretirken, Mavi Vatan **11.5 kg** ağırlığı ile mobilite ve puanlama (Weight Bonus) avantajına sahiptir.
3. **Akademik Hazırlık:** Rakiplerin çoğunda bulunmayan detaylı `MATH_MODELS.md` dökümantasyonu ile sistemin matematiksel temeli şeffaf bir şekilde sunulmuştur.
4. **Hibrit Teknoloji:** Geleneksel PID kontrolü ile modern Yapay Zeka (YOLOv11) ve Bezier eğrilerini harmanlayan "Yalın ve Güçlü" bir mimariye sahiptir.

---

> [!TIP]
> **Stratejik Hedef:** Milli Teknoloji Hamlesi vizyonuyla geliştirilen projemiz, küresel rakiplerin karmaşıklığını, yarışma şartnamesine odaklanmış "Yalın ve Etkin" bir mimari ile dengelemektedir.
