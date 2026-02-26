import json
import os
from datetime import datetime

class DataLogger:
    """
    AUV Veri Kayıt Sistemi (Blackbox).
    Araç içi tüm sensör verilerini, sistem durumunu ve görev günlüğünü JSON formatında kalıcı olarak kaydeder.
    """
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"flight_log_{timestamp}.json")
        self.session_data = []
        print(f"[LOGGER] Kara Kutu Aktif. Loglar {self.log_file} dosyasına yazılacak.")

    def log_state(self, state, depth, heading, mission_active, event=None):
        """ Sistemin o anki snapshot'ını alıp belleğe (veya doğrudan dosyaya) yazar. """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "telemetry": {
                "depth": depth,
                "heading": heading
            },
            "mission_status": "ACTIVE" if mission_active else "COMPLETED",
        }
        
        if event:
            entry["event"] = event

        self.session_data.append(entry)
        self._flush()

    def _flush(self):
        """ Bellekteki verileri log dosyasına kalıcı olarak yazar. """
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump({"flight_session": self.session_data}, f, indent=4)
        except Exception as e:
            print(f"[LOGGER-ERR] Log dosyası yazılamadı: {e}")
