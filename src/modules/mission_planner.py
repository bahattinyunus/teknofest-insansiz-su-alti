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
        self.current_wp_index = 0
        self.mission_loaded = False
        print("[PLANNER] Görev Planlayıcı Modülü Başlatıldı.")

    def load_mission(self):
        """ JSON dosyasından görev rotasını okur. """
        if not os.path.exists(self.mission_file):
            print(f"[PLANNER-ERR] Görev dosyası bulunamadı: {self.mission_file}")
            print("[PLANNER] Varsayılan görev haritası yükleniyor...")
            self.waypoints = [
                {"id": 1, "x": 10, "y": 20, "depth": 5.0, "task": "NAVIGATE"},
                {"id": 2, "x": 15, "y": 30, "depth": 6.0, "task": "DETECT_GATE"}
            ]
        else:
            try:
                with open(self.mission_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.waypoints = data.get("waypoints", [])
                    print(f"[PLANNER] {len(self.waypoints)} adet hedef noktası başarıyla yüklendi.")
            except Exception as e:
                print(f"[PLANNER-ERR] Dosya okuma hatası: {e}")
                return False
        
        self.mission_loaded = True
        return True

    def get_next_waypoint(self):
        """ Sıradaki hedef noktayı döndürür. """
        if not self.mission_loaded or self.current_wp_index >= len(self.waypoints):
            return None
        
        wp = self.waypoints[self.current_wp_index]
        self.current_wp_index += 1
        return wp

    def reset_mission(self):
        self.current_wp_index = 0
        print("[PLANNER] Görev başa sarıldı.")
