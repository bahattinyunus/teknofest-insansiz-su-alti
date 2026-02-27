class PIDTuner:
    """
    Dinamik PID Parametre Yönetim Birimi.
    Görev anında aracın kontrol hassasiyetini değiştirmeye olanak tanır.
    """
    def __init__(self):
        self.profiles = {
            "STABLE": {"kp": 0.8, "ki": 0.1, "kd": 0.05},
            "AGRESSIVE": {"kp": 1.2, "ki": 0.2, "kd": 0.1},
            "PRECISION": {"kp": 0.5, "ki": 0.05, "kd": 0.02}
        }
        self.current_profile = "STABLE"
        print("[TUNER] PID Dinamik Kontrolcüsü Başlatıldı.")

    def get_params(self, profile=None):
        """ Belirtilen profilin PID parametrelerini döndürür. """
        profile = profile or self.current_profile
        return self.profiles.get(profile, self.profiles["STABLE"])

    def set_profile(self, profile):
        """ Aktif PID profilini değiştirir. """
        if profile in self.profiles:
            self.current_profile = profile
            print(f"[TUNER] Kontrol Profili Değiştirildi: {profile}")
            return True
        return False
