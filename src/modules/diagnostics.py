import random

class DiagnosticsSystem:
    """
    AUV Sistem Diagnostik ve Sağlık İzleme Birimi.
    Sensörlerin, iticilerin ve haberleşme modüllerinin çalışma durumlarını denetler.
    """
    def __init__(self):
        self.health_status = "HEALTHY"
        self.subsystems = {
            "sensors": "OK",
            "thrusters": "OK",
            "comms": "OK",
            "battery": "OK"
        }
        print("[DIAGNOSTICS] Sistem Sağlık İzleyicisi Aktif.")

    def run_check(self):
        """ Tüm alt sistemleri tarar ve genel sağlık durumunu döndürür. """
        # Simüle edilmiş arıza olasılıkları
        failure_chance = random.random()
        
        if failure_chance < 0.05: # %5 ihtimalle batarya sorunu
            self.subsystems["battery"] = "LOW_VOLTAGE"
            self.health_status = "WARNING"
        elif failure_chance < 0.01: # %1 ihtimalle kritik itici hatası
            self.subsystems["thrusters"] = "JAMMED"
            self.health_status = "CRITICAL"
        else:
            self.health_status = "HEALTHY"
            
        return self.health_status, self.subsystems

    def get_report(self):
        """ Detaylı sağlık raporu oluşturur. """
        report = f"[DIAG] Genel Durum: {self.health_status} | "
        report += " | ".join([f"{k}: {v}" for k, v in self.subsystems.items()])
        return report
