import time
from modules.navigation import NavigationSystem
from modules.vision import VisionSystem
from modules.sonar import SonarSystem
from modules.failsafe import FailsafeSystem
from modules.communication import CommunicationSystem
from modules.logger import DataLogger
from modules.mission_planner import MissionPlanner

class MainBrain:
    def __init__(self):
        print("=== MAVİ VATAN OPERASYONU: STRATEJİK KOMUTA MERKEZİ ===")
        self.nav = NavigationSystem()
        self.vision = VisionSystem()
        self.sonar = SonarSystem()
        self.failsafe = FailsafeSystem()
        self.comms = CommunicationSystem()
        
        # Phase 2: Yeni Sistemler
        self.logger = DataLogger()
        self.planner = MissionPlanner()
        self.planner.load_mission()
        
        self.state = "STANDBY"
        self.mission_complete = False

        # Telemetri başlangıç değerleri
        self.current_depth = 0.0
        self.current_heading = 0.0
        self.target_locked = False

    def state_machine(self):
        # Başlangıç Log'u
        self.logger.log_state(self.state, self.current_depth, self.current_heading, True, event="Mission Started")
        
        while not self.mission_complete:
            self.failsafe.watchdog_reset()
            integrity_ok, msg = self.failsafe.check_integrity()
            
            if not integrity_ok:
                print(msg)
                self.logger.log_state(self.state, self.current_depth, self.current_heading, False, event=f"FAILSAFE: {msg}")
                self.state = "SURFACE"
                self.failsafe.kill_switch()
                self.failsafe.trigger_drop_weight()

            # Telemetri ve Log yayınlama
            self.comms.send_telemetry(self.state, self.current_depth, self.current_heading, self.target_locked)
            self.logger.log_state(self.state, self.current_depth, self.current_heading, True)

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
        
        # Otonom Planlayıcıdan ilk hedef derinliği al
        if len(self.planner.waypoints) > 0:
             self.current_depth = self.planner.waypoints[0].get("depth", 5.0)
        else:
             self.current_depth = 5.0
             
        self.nav.maintain_depth(self.current_depth)
        time.sleep(2)
        self.state = "WAYPOINT_NAV"

    def handle_navigation(self):
        print("[STATE: WAYPOINT_NAV] Ötonom Görev Yöneticisine Devrediliyor.")
        
        # Mission Planner üzerinden tüm route'u gez
        while True:
            wp = self.planner.get_next_waypoint()
            if not wp:
                print("[PLANNER] Tüm hedef noktalarına başarıyla ulaşıldı.")
                break
                
            task_type = wp.get("task", "UNKNOWN")
            target_x = wp.get("x", 0)
            target_y = wp.get("y", 0)
            target_depth = wp.get("depth", self.current_depth)
            
            print(f"[PLANNER] Sıradaki Hedef W[{wp.get('id', '?')}]: (X:{target_x}, Y:{target_y}) - Görev: {task_type}")
            
            # Eğer derinlik değişecekse
            if target_depth != self.current_depth:
                self.current_depth = target_depth
                self.nav.maintain_depth(self.current_depth)

            # Navigasyon sağla
            self.nav.move_to_target(target_x, target_y)
            self.logger.log_state(self.state, self.current_depth, 45.0, True, event=f"Reaching Waypoint: {wp.get('id')}")
            time.sleep(1)
            
        self.current_heading = 45.0
        time.sleep(1)
        self.state = "OBJECT_DETECTION"


    def handle_detection(self):
        print("[STATE: OBJECT_DETECTION] YOLO v11 ile Alansal Görev İcrası.")
        target = self.vision.detect_object("Çember")
        if target['detected']:
            self.target_locked = True
            meta = target['metadata']
            print(f"[MISSION] Hedef Tespit Edildi: {target['coordinates']}")
            print(f"[MISSION] Nesne Tipi: {meta['type']} | Öncelik: {meta['priority']} | Güven: %{target['confidence']*100:.1f}")
        self.state = "SURFACE"

    def handle_surface(self):
        print("[STATE: SURFACE] Emniyetli Tahliye Protokolü ve Yüzeye Çıkış.")
        self.current_depth = 0.0
        self.target_locked = False
        # Son tahliye telemetrisi
        self.comms.send_telemetry(self.state, self.current_depth, self.current_heading, self.target_locked)
        self.mission_complete = True
        print("Operasyon Derin Mavi Tamamlandı.")

if __name__ == "__main__":
    brain = MainBrain()
    brain.state_machine()
