class MiniROVManager:
    """
    AUV bünyesindeki Mini ROV (Remotely Operated Vehicle) kontrol birimi.
    Şartname Tema 1: Hat Takibi ve Kapalı Alan İncelemesi için tasarlanmıştır.
    """
    def __init__(self):
        self.is_deployed = False
        self.tether_length = 0.0 # m
        self.video_stream_active = False
        print("[MINI-ROV] Yönetim Birimi Hazır.")

    def deploy(self):
        """ Mini ROV'u ana araçtan salar. """
        self.is_deployed = True
        self.video_stream_active = True
        print("[MINI-ROV] Salınım Gerçekleştirildi. Video Aktarımı Başlatıldı.")
        return True

    def scan_pipeline(self):
        """ Boru hattı içindeki ipucunu tespit simülasyonu. """
        if not self.is_deployed:
            return None
        
        # Şartnameye göre ipucu bulma simülasyonu
        import random
        colors = ["Kırmızı", "Yeşil", "Mavi"]
        clue = random.choice(colors)
        print(f"[MINI-ROV] Boru Hattı Sonu İpucu Tespit Edildi: {clue}")
        return clue

    def retract(self):
        """ Mini ROV'u ana araca geri çeker. """
        self.is_deployed = False
        self.video_stream_active = False
        print("[MINI-ROV] Ana Araca Geri Çekildi.")
        return True
