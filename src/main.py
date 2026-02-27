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
        
        self.state = "STANDBY"
        self.mission_complete = False

        # Telemetri başlangıç değerleri
        self.current_depth = 0.0
        self.current_heading = 0.0
        self.current_pos = (0.0, 0.0)
        self.target_locked = False

    def state_machine(self):
        # Başlangıç Log'u
        self.logger.log_state(self.state, self.current_depth, self.current_heading, True, event="Mission Started")
        
        while not self.mission_complete:
            self.failsafe.watchdog_reset()
            integrity_ok, msg = self.failsafe.check_integrity()
            
            # Sistem Sağlık Kontrolü
            health, details = self.diag.run_check()
            if health == "CRITICAL":
                print(f"[ALERT] KRİTİK SİSTEM HATASI: {details}")
                self.logger.log_state(self.state, self.current_depth, self.current_heading, False, event=f"DIAG_CRITICAL: {details}")
                self.state = "SURFACE"

            if not integrity_ok:
                print(msg)
                self.logger.log_state(self.state, self.current_depth, self.current_heading, False, event=f"FAILSAFE: {msg}")
                self.state = "SURFACE"
                self.failsafe.kill_switch()
                self.failsafe.trigger_drop_weight()

            # Telemetri ve Log yayınlama
            self.comms.send_telemetry(self.state, self.current_depth, self.current_heading, self.target_locked)
            self.logger.log_state(self.state, self.current_depth, self.current_heading, True, event=self.diag.get_report())

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
        time.sleep(1)
        self.state = "DIVING"

    def handle_diving(self):
        print("[STATE: DIVING] Dinamik Dalış ve Derinlik Stabilizasyonu Başlatıldı.")
        if len(self.planner.waypoints) > 0:
             self.current_depth = self.planner.waypoints[0].get("depth", 5.0)
        else:
             self.current_depth = 5.0
        self.nav.maintain_depth(self.current_depth)
        time.sleep(1)
        self.state = "WAYPOINT_NAV"

    def handle_navigation(self):
        print("[STATE: WAYPOINT_NAV] Gelişmiş Navigasyon Modu (Path Smoothing Active)")
        params = self.tuner.get_params("PRECISION")
        self.nav.update_pid_params(**params)

        while True:
            wp = self.planner.get_next_waypoint()
            if not wp:
                print("[PLANNER] Tüm hedef noktalarına ulaşıldı.")
                break
                
            target_x, target_y = wp.get("x", 0), wp.get("y", 0)
            target_depth = wp.get("depth", self.current_depth)
            
            # Bezier ile yumuşatılmış rota oluştur
            smooth_points = self.path_smoother.generate_smooth_path(self.current_pos, (target_x, target_y))
            print(f"[NAV] Rota Planlandı: {len(smooth_points)} ara nokta üzerinden geçilecek.")

            if target_depth != self.current_depth:
                self.current_depth = target_depth
                self.nav.maintain_depth(self.current_depth)

            for step_pos in smooth_points:
                self.nav.move_to_target(*step_pos)
                self.current_pos = step_pos
                time.sleep(0.2) # Akıcı gösterim için kısa bekleme

            self.logger.log_state(self.state, self.current_depth, 45.0, True, event=f"Reaching Waypoint: {wp.get('id')}")
            
        self.current_heading = 45.0
        self.state = "OBJECT_DETECTION"

    def handle_detection(self):
        print("[STATE: OBJECT_DETECTION] Hedef Tespit ve Otonom Takip.")
        target = self.vision.detect_object("Çember")
        
        if target['detected']:
            self.target_locked = True
            coords = target['coordinates']
            print(f"[MISSION] Hedef Kilitlendi: {coords}")
            
            # Otonom Takip (Tracker) devreye giriyor
            correction = self.tracker.get_correction_commands(coords)
            print(f"[TRACKER] Hizalama Komutları: {correction}")
            
            if self.tracker.is_locked:
                print("[TRACKER] Hedef Merkezlendi. Görev İcrası Tamam.")
            
            self.logger.log_state(self.state, self.current_depth, 45.0, True, event="Target Tracked & Centered")
            time.sleep(2)
            
        self.state = "SURFACE"

    def handle_surface(self):
        print("[STATE: SURFACE] Yüzeye Çıkış.")
        self.current_depth = 0.0
        self.target_locked = False
        self.comms.send_telemetry(self.state, self.current_depth, self.current_heading, self.target_locked)
        self.mission_complete = True
        print("Mavi Vatan Operasyonu Başarıyla Tamamlandı.")

if __name__ == "__main__":
    brain = MainBrain()
    brain.state_machine()
