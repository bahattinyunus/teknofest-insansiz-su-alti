import time
import json

class CommunicationSystem:
    """
    Yer Kontrol İstasyonu (GCS) ile telemetri ve komut haberleşmesini simüle eden modül.
    MQTT veya benzeri protokollerin mantıksal soyutlamasını içerir.
    """
    def __init__(self):
        self.connected = False
        self.telemetry_freq = 1.0  # Hz
        self.last_send_time = time.time()
        print("[COMMS] Yer Kontrol İstasyonu Bağlantısı Başlatılıyor...")
        self.connect()

    def connect(self):
        """ GCS ile bağlantı kurma simülasyonu """
        time.sleep(0.5)
        self.connected = True
        print("[COMMS] GCS Bağlantısı Kuruldu (10.0.0.5:1883)")

    def send_telemetry(self, state, depth, heading, target_detected):
        """ Telemetri paketini hazırlayıp gönderme simülasyonu """
        if not self.connected:
            print("[COMMS-ERR] GCS Bağlantısı Yok, Paket İletilemedi!")
            return False

        current_time = time.time()
        if current_time - self.last_send_time >= (1.0 / self.telemetry_freq):
            packet = {
                "timestamp": round(current_time, 2),
                "state": state,
                "sensors": {
                    "depth": depth,
                    "heading": heading
                },
                "mission": {
                    "target_locked": target_detected
                }
            }
            # Simüle edilmiş JSON payload
            payload = json.dumps(packet)
            print(f">>> [TELEMETRY_TX] {payload}")
            self.last_send_time = current_time
            return True
        return False

    def receive_command(self):
        """ GCS'den gelecek olası komutları dinleme """
        # Simülasyon gereği şimdilik pasif
        pass
