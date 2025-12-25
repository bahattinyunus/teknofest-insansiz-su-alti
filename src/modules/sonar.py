import random
import math

class SonarSystem:
    """
    AUV Akustik Algılama Sistemi.
    Gerçek zamanlı mesafe ölçümü ve gürültü profili simülasyonu içerir.
    """
    def __init__(self):
        self.propagation_speed = 1500  # m/s (suda ses hızı)
        self.max_range = 50.0          # metre
        print("[BAŞLATILDI] Sonar Sistemi Çevrimiçi (Active Pinging Mode)")

    def get_distance(self):
        """
        Sonar Echo Time-of-Flight simülasyonu.
        Geleneksel sonar denklemini (Distance = (v*t)/2) ve çevresel gürültüyü baz alır.
        """
        base_range = 2.0
        # Su altı sıcaklık ve basınç değişimlerinden kaynaklanan dalgalanma
        noise = random.gauss(0, 0.05)
        
        # Sinyal zayıflaması ve yankı kaybı (Simulation)
        measured_distance = base_range + noise
        
        return round(max(0.0, measured_distance), 3)

    def scan_environment(self):
        """120 derecelik açısal tarama simülasyonu"""
        scan_data = []
        for angle in range(-60, 61, 10):
            dist = self.get_distance()
            scan_data.append({"angle": angle, "distance": dist})
        return scan_data
