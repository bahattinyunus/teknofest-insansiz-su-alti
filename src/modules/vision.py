import random

class VisionSystem:
    def __init__(self):
        self.active = True
        print("[BAŞLATILDI] Görüntü İşleme Sistemi Çevrimiçi")

    def detect_object(self, object_name):
        """YOLO v11 Inference Simülasyonu"""
        print(f"[GÖRÜNTÜ] {object_name} için CLAHE ve HSV taraması yapılıyor...")
        
        confidence = random.uniform(0.7, 0.98)
        detected = confidence > 0.82
        
        return {
            "detected": detected,
            "confidence": round(confidence, 2),
            "coordinates": (random.randint(50, 400), random.randint(50, 300)) if detected else None
        }
