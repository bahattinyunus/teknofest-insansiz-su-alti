class KalmanFilter:
    """
    Basit Tek Boyutlu Kalman Filtresi (1D Kalman Filter).
    Gürültülü sensör verilerini optimize etmek için kullanılır.
    """
    def __init__(self, process_variance=1e-5, measurement_variance=1e-1, initial_value=0.0):
        self.process_variance = process_variance      # Sistemdeki tahmin belirsizliği (Q)
        self.measurement_variance = measurement_variance # Sensördeki gürültü payı (R)
        self.estimated_value = initial_value
        self.error_covariance = 1.0 # Başlangıç hata payı (P)
        print(f"[KALMAN] Filtre Başlatıldı (R={measurement_variance}, Q={process_variance})")

    def update(self, measurement):
        """
        Filtreyi yeni bir ölçümle günceller ve optimize edilmiş değeri döndürür.
        """
        # 1. Tahmin Adımı (Prediction Step)
        # 1D sabit değer modelinde değer aynı kalır, hata payı artar.
        self.error_covariance += self.process_variance

        # 2. Güncelleme Adımı (Update Step) - Kalman Kazancı (K)
        kalman_gain = self.error_covariance / (self.error_covariance + self.measurement_variance)
        
        # Optimize edilmiş yeni değer
        self.estimated_value += kalman_gain * (measurement - self.estimated_value)
        
        # Hata payını güncelle
        self.error_covariance *= (1 - kalman_gain)

        return round(self.estimated_value, 4)

    def reset(self, value=0.0):
        self.estimated_value = value
        self.error_covariance = 1.0
