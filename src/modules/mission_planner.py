import json
import os

class MissionPlanner:
    """
    AUV Görev Yöneticisi (Mission Planner).
    Dışarıdan JSON tabanlı bir görev dosyası okuyarak birden fazla hedef noktasına (waypoints) otonom seyir planlaması yapar.
    """
    def __init__(self, mission_file="config/mission_waypoints.json"):
        self.mission_file = mission_file
        self.waypoints = []
        self.current_index = 0
        self.mission_loaded = False
        print("[PLANNER] Görev Planlayıcı Modülü Başlatıldı.")

    def load_mission(self, file_path=None):
        """ JSON dosyasından görev rotasını okur veya varsayılanı yükler. """
        path = file_path if file_path else self.mission_file
        
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.waypoints = json.load(f)
                print(f"[PLANNER] Görev dosyası yüklendi: {len(self.waypoints)} hedef.")
                self.mission_loaded = True
            except Exception as e:
                print(f"[PLANNER-ERR] Görev yüklenirken hata: {e}")
                self.load_default_mission()
        else:
            print(f"[PLANNER-ERR] Görev dosyası bulunamadı: {path}")
            self.load_default_mission()
        
        self.current_index = 0

    def load_default_mission(self):
        """ TEKNOFEST 2026 Şartname Görevleri için varsayılan rotayı oluşturur. """
        self.waypoints = [
            {"id": 1, "task": "PIPELINE_INSPECTION", "x": 10, "y": 5, "depth": 3.0},
            {"id": 2, "task": "COORDINATE_NAV", "lat": 41.0082, "lon": 28.9784, "depth": 5.0},
            {"id": 3, "task": "TARGET_ENGAGEMENT", "x": 20, "y": 20, "depth": 2.0}
        ]
        print("[PLANNER] Şartname varsayılan görevi oluşturuldu.")
        self.current_index = 0
        self.mission_loaded = True

    def get_next_waypoint(self):
        """ Sıradaki hedef noktayı döndürür. """
        if self.current_index < len(self.waypoints):
            wp = self.waypoints[self.current_index]
            self.current_index += 1
            return wp
        return None

    def reset_mission(self):
        """ Görevi başa sarar. """
        self.current_index = 0
        print("[PLANNER] Görev başa sarıldı.")
