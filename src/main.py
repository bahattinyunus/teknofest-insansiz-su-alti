import time
from modules.navigation import NavigationSystem
from modules.vision import VisionSystem
from modules.sonar import SonarSystem

class MainBrain:
    def __init__(self):
        print("=== TEKNOFEST İSA ANA BEYİN BAŞLATILIYOR ===")
        self.nav = NavigationSystem()
        self.vision = VisionSystem()
        self.sonar = SonarSystem()
        print("=== SİSTEM HAZIR ===")

    def run_mission(self):
        print("Görev Başlatılıyor: Operasyon Derin Mavi")
        self.nav.maintain_depth(5.0)
        target = self.vision.detect_object("Kırmızı Kapı")
        if target['detected']:
            self.nav.move_to_target(target['coordinates'][0], target['coordinates'][1])
        print("Görev Fazı 1 Tamamlandı")

if __name__ == "__main__":
    brain = MainBrain()
    brain.run_mission()
