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
    assert len(planner.waypoints) == 2
    assert planner.waypoints[0]["task"] == "NAVIGATE"
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
