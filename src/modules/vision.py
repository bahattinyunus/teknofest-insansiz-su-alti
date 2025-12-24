class VisionSystem:
    def __init__(self):
        self.active = False
        print("[BAŞLATILDI] Görüntü İşleme Sistemi Çevrimiçi")

    def detect_object(self, object_name):
        print(f"[GÖRÜNTÜ] {object_name} için tarama yapılıyor...")
        # YOLO/OpenCV mantığı yer tutucusu
        return {"detected": True, "coordinates": (100, 200)}
