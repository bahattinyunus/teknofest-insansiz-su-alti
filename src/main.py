import time
from modules.navigation import NavigationSystem
from modules.vision import VisionSystem
from modules.sonar import SonarSystem
from modules.failsafe import FailsafeSystem

class MainBrain:
    def __init__(self):
        print("=== MAVİ VATAN OPERASYONU: STRATEJİK KOMUTA MERKEZİ ===")
        self.nav = NavigationSystem()
        self.vision = VisionSystem()
        self.sonar = SonarSystem()
        self.failsafe = FailsafeSystem()
        self.state = "STANDBY"
        self.mission_complete = False

    def state_machine(self):
        while not self.mission_complete:
            self.failsafe.watchdog_reset()
            integrity_ok, msg = self.failsafe.check_integrity()
            
            if not integrity_ok:
                print(msg)
                self.state = "SURFACE"
                self.failsafe.kill_switch()
                self.failsafe.trigger_drop_weight()

            if self.state == "STANDBY":
                self.handle_standby()
            elif self.state == "DIVING":
                self.handle_diving()
            elif self.state == "WAYPOINT_NAV":
                self.handle_navigation()
            elif self.state == "OBJECT_DETECTION":
                self.handle_detection()
            elif self.state == "SURFACE":
                self.handle_surface()
                break
            
            time.sleep(1)

    def handle_standby(self):
        print("[STATE: STANDBY] Pre-flight Kontrolleri ve Sensör Kalibrasyonu...")
        time.sleep(2)
        self.state = "DIVING"

    def handle_diving(self):
        print("[STATE: DIVING] Dinamik Dalış ve Derinlik Stabilizasyonu Başlatıldı.")
        self.nav.maintain_depth(5.0)
        time.sleep(2)
        self.state = "WAYPOINT_NAV"

    def handle_navigation(self):
        print("[STATE: WAYPOINT_NAV] Ölü Hesaplama (Dead Reckoning) ile Rota Navigasyonu.")
        self.nav.move_to_target(10, 20)
        time.sleep(2)
        self.state = "OBJECT_DETECTION"

    def handle_detection(self):
        print("[STATE: OBJECT_DETECTION] YOLO v11 ile Alansal Görev İcrası.")
        target = self.vision.detect_object("Çember")
        if target['detected']:
            meta = target['metadata']
            print(f"[MISSION] Hedef Tespit Edildi: {target['coordinates']}")
            print(f"[MISSION] Nesne Tipi: {meta['type']} | Öncelik: {meta['priority']} | Güven: %{target['confidence']*100:.1f}")
        self.state = "SURFACE"

    def handle_surface(self):
        print("[STATE: SURFACE] Emniyetli Tahliye Protokolü ve Yüzeye Çıkış.")
        self.mission_complete = True
        print("Operasyon Derin Mavi Tamamlandı.")

if __name__ == "__main__":
    brain = MainBrain()
    brain.state_machine()
