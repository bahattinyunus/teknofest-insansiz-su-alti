import pytest
from src.modules.failsafe import FailsafeSystem
from src.modules.navigation import NavigationSystem

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
