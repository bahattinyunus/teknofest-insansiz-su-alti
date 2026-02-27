class TorpedoSystem:
    """
    AUV Torpido Fırlatma Birimi.
    Şartname Tema 3: Hedefe Müdahale Görevi için tasarlanmıştır.
    Kısıtlama: Patlayıcı, pnömatik ve hidrolik sistemler yasaktır. 
    Bu modül elektromekanik (yaylı) tetikleme mantığını simüle eder.
    """
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.remaining = capacity
        print(f"[TORPEDO] Sistem Aktif. Mühimmat: {capacity}/5")

    def fire(self, target_color=None):
        """ Torpido ateşleme lojiği. """
        if self.remaining <= 0:
            print("[TORPEDO] Mühimmat Bitti!")
            return False

        self.remaining -= 1
        print(f"[TORPEDO] Ateşlendi! Kalan: {self.remaining}. Hedef: {target_color}")
        return True

    def reload(self):
        """ Şartnameye göre havuz kenarında mühimmat tazeleme. """
        self.remaining = self.capacity
        print("[TORPEDO] Mühimmat Tazelendi (5/5).")
        return True
