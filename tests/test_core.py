import pytest
from src.modules.failsafe import FailsafeSystem
from src.modules.navigation import NavigationSystem
from src.modules.communication import CommunicationSystem
from src.modules.sonar import SonarSystem
from src.modules.vision import VisionSystem

def test_failsafe_integrity():
    failsafe = FailsafeSystem()
    status, msg = failsafe.check_integrity()
    assert status is True
    assert "TAM" in msg

def test_failsafe_leak_detection():
    failsafe = FailsafeSystem()
    failsafe.leak_detected = True
    status, msg = failsafe.check_integrity()
    assert status is False
    assert "SIZINTI" in msg

def test_navigation_depth():
    nav = NavigationSystem()
    assert nav.maintain_depth(5.0) is True

def test_navigation_movement():
    nav = NavigationSystem()
    assert nav.move_to_target(10, 20) is True

def test_communication_initialization():
    comms = CommunicationSystem()
    assert comms.connected is True
    assert comms.telemetry_freq == 1.0

def test_communication_send_telemetry():
    comms = CommunicationSystem()
    # İlk başta zaman geçmediği için bekle
    import time
    time.sleep(1.0)
    result = comms.send_telemetry("STANDBY", 0.0, 0.0, False)
    assert result is True

def test_sonar_scan():
    sonar = SonarSystem()
    result = sonar.scan_environment()
    assert isinstance(result, list)
    assert len(result) > 0
    assert "angle" in result[0]
    assert "distance" in result[0]

def test_vision_detect():
    import random
    random.seed(42) # RNG'yi sabitle
    vision = VisionSystem()
    result = vision.detect_object("Çember")
    assert "detected" in result
    assert "confidence" in result
    if result["detected"]:
        assert len(result["coordinates"]) == 2
        assert result["metadata"]["type"] == "MISSION_GATE"

def test_logger_creation():
    from src.modules.logger import DataLogger
    import os
    logger = DataLogger(log_dir="tests/test_logs")
    logger.log_state("STANDBY", 0.0, 0.0, False, event="Test Log")
    assert os.path.exists("tests/test_logs")
    assert len(logger.session_data) == 1
    assert logger.session_data[0]["state"] == "STANDBY"

def test_mission_planner_default():
    from src.modules.mission_planner import MissionPlanner
    # Var olmayan bir dosya yüklenirse default rotayı getirmeli
    planner = MissionPlanner(mission_file="invalid_path.json")
    planner.load_mission()
    assert len(planner.waypoints) == 3
    assert planner.waypoints[0]["task"] == "PIPELINE_INSPECTION"
    wp = planner.get_next_waypoint()
    assert wp["id"] == 1

def test_diagnostics_report():
    from src.modules.diagnostics import DiagnosticsSystem
    diag = DiagnosticsSystem()
    status, details = diag.run_check()
    assert status in ["HEALTHY", "WARNING", "CRITICAL"]
    assert "battery" in details
    assert "sensors" in details

def test_pid_tuner_profiles():
    from src.modules.pid_tuner import PIDTuner
    tuner = PIDTuner()
    params = tuner.get_params("PRECISION")
    assert params["kp"] == 0.5
    assert params["ki"] == 0.05
    assert tuner.set_profile("AGRESSIVE") is True
    assert tuner.current_profile == "AGRESSIVE"

def test_path_planner_smooth():
    from src.modules.path_planner import PathPlanner
    planner = PathPlanner()
    path = planner.generate_smooth_path((0, 0), (10, 10))
    assert len(path) == 6
    assert path[0] == (0.0, 0.0)
    assert path[-1] == (10.0, 10.0)

def test_object_tracker_error():
    from src.modules.tracker import ObjectTracker
    tracker = ObjectTracker(frame_size=(640, 480))
    ex, ey = tracker.calculate_tracking_error((330, 250))
    assert ex == 10 # 330 - 320
    assert ey == 10 # 250 - 240
    commands = tracker.get_correction_commands((325, 245))
    assert tracker.is_locked is True

def test_kalman_filter_convergence():
    from src.modules.kalman_filter import KalmanFilter
    kf = KalmanFilter(measurement_variance=0.1)
    # Sabit bir değer (5.0) etrafında gürültülü ölçümler verelim
    measurements = [5.1, 4.9, 5.2, 4.8, 5.0]
    final_estimate = 0
    for m in measurements:
        final_estimate = kf.update(m)
    
    # Filtrelenmiş değerin gerçek değere (5.0) yakın olması beklenir
    assert abs(final_estimate - 5.0) < 0.1

def test_mini_rov_mission():
    from src.modules.mini_rov_manager import MiniROVManager
    rov = MiniROVManager()
    assert rov.deploy() is True
    assert rov.scan_pipeline() in ["Kırmızı", "Yeşil", "Mavi"]
    assert rov.retract() is True

def test_torpedo_fire_logic():
    from src.modules.torpedo_sys import TorpedoSystem
    system = TorpedoSystem(capacity=5)
    for _ in range(5):
        assert system.fire() is True
    assert system.fire() is False # Mühimmat bitti
    system.reload()
    assert system.remaining == 5
