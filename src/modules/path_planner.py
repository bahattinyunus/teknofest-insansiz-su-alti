import math

class PathPlanner:
    """
    AUV Yol Planlama ve Rota Yumuşatma Birimi.
    Keskin dönüşleri Bezier eğrileri veya ara noktalar (interpolation) ile akıcı hale getirir.
    """
    def __init__(self):
        print("[PLANNER] Yol Planlayıcı Aktif.")

    def generate_smooth_path(self, start_point, end_point, control_point=None):
        """
        İki nokta arasında yumuşatılmış bir rota (nokta listesi) oluşturur.
        Basit bir quadratic Bezier yaklaşımı kullanır.
        """
        if control_point is None:
            # Kontrol noktası verilmezse ortayı hafif saptırarak kavis oluştur
            control_point = (
                (start_point[0] + end_point[0]) / 2 + 2,
                (start_point[1] + end_point[1]) / 2 + 2
            )

        path = []
        steps = 5 # Rotayı 5 alt noktaya böl
        for i in range(steps + 1):
            t = i / steps
            # Bezier Formülü: (1-t)^2 * P0 + 2(1-t)t * P1 + t^2 * P2
            x = (1-t)**2 * start_point[0] + 2*(1-t)*t * control_point[0] + t**2 * end_point[0]
            y = (1-t)**2 * start_point[1] + 2*(1-t)*t * control_point[1] + t**2 * end_point[1]
            path.append((round(x, 2), round(y, 2)))
        
        return path

    def get_hydrodynamic_velocity(self, current_v, target_v):
        """ Akışkan hareket için hız geçişi simülasyonu. """
        return current_v + (target_v - current_v) * 0.1
