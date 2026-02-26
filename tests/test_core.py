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
    assert "depth_clearance" in result
    assert "obstacles" in result

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
