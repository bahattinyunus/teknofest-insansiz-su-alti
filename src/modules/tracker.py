class ObjectTracker:
    """
    Gelişmiş Hedef Takip Birimi.
    Vision sisteminden gelen koordinatları kullanarak hedefi merkezde tutar.
    """
    def __init__(self, frame_size=(640, 480)):
        self.frame_center = (frame_size[0] // 2, frame_size[1] // 2)
        self.is_locked = False
        print("[TRACKER] Hedef Takip Sistemi Çevrimiçi.")

    def calculate_tracking_error(self, target_coords):
        """
        Hedef koordinatların ekran merkezine olan uzaklığını (hata payı) hesaplar.
        """
        if not target_coords:
            return 0.0, 0.0
            
        error_x = target_coords[0] - self.frame_center[0]
        error_y = target_coords[1] - self.frame_center[1]
        
        return error_x, error_y

    def get_correction_commands(self, target_coords):
        """
        Hata payına göre AUV'ye verilecek düzeltme komutlarını üretir.
        """
        ex, ey = self.calculate_tracking_error(target_coords)
        
        commands = {
            "yaw_adj": round(ex * 0.1, 2),   # Yatay eksen düzeltme
            "pitch_adj": round(-ey * 0.1, 2) # Dikey eksen düzeltme
        }
        
        self.is_locked = abs(ex) < 10 and abs(ey) < 10
        return commands
