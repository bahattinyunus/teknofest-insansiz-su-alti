import time
from modules.navigation import NavigationSystem
from modules.vision import VisionSystem
from modules.sonar import SonarSystem
from modules.failsafe import FailsafeSystem
from modules.communication import CommunicationSystem
from modules.logger import DataLogger
from modules.mission_planner import MissionPlanner
from modules.diagnostics import DiagnosticsSystem
from modules.pid_tuner import PIDTuner
from modules.path_planner import PathPlanner
from modules.tracker import ObjectTracker
from modules.kalman_filter import KalmanFilter
from modules.mini_rov_manager import MiniROVManager
from modules.torpedo_sys import TorpedoSystem

class MainBrain:
    def __init__(self):
        print("=== MAVİ VATAN OPERASYONU: STRATEJİK KOMUTA MERKEZİ ===")
        self.nav = NavigationSystem()
        self.vision = VisionSystem()
        self.sonar = SonarSystem()
        self.failsafe = FailsafeSystem()
        self.comms = CommunicationSystem()
        
        # Phase 2: Otonomi & Kayıt
        self.logger = DataLogger()
        self.planner = MissionPlanner()
        self.planner.load_mission()

        # Phase 3: Diagnostik & Optimizasyon
        self.diag = DiagnosticsSystem()
        self.tuner = PIDTuner()

        # Phase 4: Akıllı Navigasyon & Takip
        self.path_smoother = PathPlanner()
        self.tracker = ObjectTracker()

        # Phase 5: Sensör Füzyonu
        self.kf_depth = KalmanFilter(measurement_variance=1e-2)

        # Phase 6: Şartname Görev Sistemleri
        self.mini_rov = MiniROVManager()
        self.torpedo = TorpedoSystem()
        
        self.state = "STANDBY"
        self.mission_complete = False

        # Telemetri başlangıç değerleri
        self.current_depth = 0.0
        self.filtered_depth = 0.0
        self.current_heading = 0.0
        self.current_pos = (0.0, 0.0)
        self.target_locked = False

    def state_machine(self):
        self.logger.log_state(self.state, self.current_depth, self.current_heading, True, event="Mission Started")
        
        while not self.mission_complete:
            self.failsafe.watchdog_reset()
            integrity_ok, msg = self.failsafe.check_integrity()
            
            health, details = self.diag.run_check()
            if health == "CRITICAL":
                print(f"[ALERT] KRİTİK SİSTEM HATASI: {details}")
                self.logger.log_state(self.state, self.current_depth, self.current_heading, False, event=f"DIAG_CRITICAL: {details}")
                self.state = "SURFACE"

            self.filtered_depth = self.kf_depth.update(self.current_depth)

            if not integrity_ok:
                print(msg)
                self.logger.log_state(self.state, self.filtered_depth, self.current_heading, False, event=f"FAILSAFE: {msg}")
                self.state = "SURFACE"
                self.failsafe.kill_switch()
                self.failsafe.trigger_drop_weight()

            self.comms.send_telemetry(self.state, self.filtered_depth, self.current_heading, self.target_locked)
            self.logger.log_state(self.state, self.filtered_depth, self.current_heading, True, event=self.diag.get_report())

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
        print("[STATE: STANDBY] Şartname Uyumu Kontrol Ediliyor...")
        time.sleep(1)
        self.state = "DIVING"

    def handle_diving(self):
        print("[STATE: DIVING] Göreve Başlanıyor.")
        if len(self.planner.waypoints) > 0:
             self.current_depth = self.planner.waypoints[0].get("depth", 5.0)
        else:
             self.current_depth = 5.0
        self.nav.maintain_depth(self.current_depth)
        time.sleep(1)
        self.state = "WAYPOINT_NAV"

    def handle_navigation(self):
        print("[STATE: WAYPOINT_NAV] Şartname Temaları İcra Ediliyor.")
        params = self.tuner.get_params("PRECISION")
        self.nav.update_pid_params(**params)

        while True:
            wp = self.planner.get_next_waypoint()
            if not wp:
                break
            
            task_name = wp.get("task", "DEFAULT")
            print(f"[MISSION] Mevcut Görev: {task_name}")

            # 1. TEMA: Hat Takibi ve Mini ROV
            if task_name == "PIPELINE_INSPECTION":
                self.nav.move_to_target(wp["x"], wp["y"])
                print("[MISSION] Boru Hattına Ulaşıldı. Mini ROV Salınıyor...")
                self.mini_rov.deploy()
                clue = self.mini_rov.scan_pipeline()
                self.mini_rov.retract()

            # 2. TEMA: Koordinat Bazlı Navigasyon
            elif task_name == "COORDINATE_NAV":
                print(f"[MISSION] Koordinat Tabana İntikal: Lat {wp['lat']}, Lon {wp['lon']}")
                # Koordinat dönüştürme simülasyonu
                self.nav.move_to_target(30, 30)

            # 3. TEMA: Hedefe Müdahale (Torpido)
            elif task_name == "TARGET_ENGAGEMENT":
                self.nav.move_to_target(wp["x"], wp["y"])
                print("[MISSION] Hedef Alanına Ulaşıldı. Atış Hazırlığı...")
                for _ in range(5): # Şartname: 5 torpido
                    self.torpedo.fire(target_color="Kırmızı")
                    time.sleep(0.5)

            # Standart Navigasyon (Yumuşatılmış Rota)
            else:
                target_x, target_y = wp.get("x", 0), wp.get("y", 0)
                smooth_points = self.path_smoother.generate_smooth_path(self.current_pos, (target_x, target_y))
                for step_pos in smooth_points:
                    self.nav.move_to_target(*step_pos)
                    self.current_pos = step_pos
                    time.sleep(0.1)

            self.logger.log_state(self.state, self.current_depth, 45.0, True, event=f"Complete: {task_name}")
            
        self.state = "OBJECT_DETECTION"

    def handle_detection(self):
        print("[STATE: OBJECT_DETECTION] Hedef Tespit ve Otonom Takip.")
        target = self.vision.detect_object("Çember")
        if target['detected']:
            self.target_locked = True
            correction = self.tracker.get_correction_commands(target['coordinates'])
            if self.tracker.is_locked:
                print("[TRACKER] Hedef Kilitli ve Merkezde.")
            time.sleep(1)
        self.state = "SURFACE"

    def handle_surface(self):
        print("[STATE: SURFACE] Mavi Vatan Görevi Tamamlandı. Yüzeye Çıkılıyor.")
        self.current_depth = 0.0
        self.mission_complete = True

if __name__ == "__main__":
    brain = MainBrain()
    brain.state_machine()
