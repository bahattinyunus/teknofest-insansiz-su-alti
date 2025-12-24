# Sistem Mimarisi

## Genel Bakış
Sistem, Teknofest İSA yarışma ortamında yüksek uyum yeteneği için tasarlanmış modüler, olay güdümlü bir mimariyi takip eder.

## Modüller

### 1. Ana Beyin (`main.py`)
- Merkezi orkestratör olarak hareket eder.
- Durum geçişlerini yönetir (Bekleme -> Dalış -> Görev -> Yüzeye Çıkış).
- Modüller arası iletişimi sağlar.

### 2. Navigasyon (`modules/navigation.py`)
- Otonom hareketten sorumludur.
- Stabilizasyon için PID kontrolcüleri uygular.
- Yol planlama mantığını yönetir.

### 3. Görüntü İşleme (`modules/vision.py`)
- Ön ve alt kameralardan gelen video akışlarını işler.
- Nesne tespiti için YOLO/OpenCV kullanır (kapı geçişi, hedef tespiti).

### 4. Sonar (`modules/sonar.py`)
- Mesafe ölçümü için akustik sinyalleri işler.
- Engelden kaçınma ve hassas özel görevler için kullanılır.

## Veri Akışı
Sensör Verisi -> Donanım Arayüzü -> Ana Beyin -> Karar Mantığı -> Motor Sürücüleri
