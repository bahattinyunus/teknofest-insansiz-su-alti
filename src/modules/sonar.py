import random

class SonarSystem:
    def __init__(self):
        print("[BAŞLATILDI] Sonar Sistemi Çevrimiçi")

    def get_distance(self):
        """Sonar Echo Time-of-Flight simülasyonu"""
        base_range = 2.0
        noise = random.uniform(-0.1, 0.1)
        return round(base_range + noise, 3)
