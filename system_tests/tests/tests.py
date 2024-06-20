import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc
from parameterized import parameterized, parameterized_class

DEVICE_PREFIX = "HAMEG8123_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("HAMEG8123"),
        "macros": {},
        "emulator": "hameg_8123",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class Hameg8123Tests(unittest.TestCase):
    """
    Tests for the _Device_ IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("hameg_8123", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_wait_time=0.0)

    def test_get_idn(self):
        self.ca.assert_that_pv_is("IDN", "HAMEG HM8123")

    @parameterized.expand([
        ("GATETIME", "GATETIME:SP", 301),
        ("FUNCTION", "FUNCTION:SP", "WDA")
    ])
    def test_gate_time_on_device_matches_rbv_after_sp_set(self, rbv,sp,expected):
        self.ca.set_pv_value(sp, expected)
        self.ca.assert_that_pv_is(rbv, expected)
    
    @parameterized.expand([
        ("GATETIME", "gate_time", 300),
        ("FUNCTION", "func", "FRB"),
        ("COUNTS", "count", 51),
        ("COUNTS.EGU", "count_unit", "S"),
    ])
    def test_gate_time_on_device_matches_rbv(self, pv, lewis_var, expected):
        self._lewis.backdoor_set_on_device(lewis_var, expected)
        self.ca.assert_that_pv_is(pv, expected)

    @parameterized.expand([
        ("START_COUNTING:SP", "started", True),
        ("STOP_COUNTING:SP", "stopped", True),
        ("RESET_COUNTS:SP", "reset", True),
        ("TRIGGER:SP", "triggered", True),
        ("PULSES_PER_REV:SP", "pulses_per_rev", 2000)
    ])
    def test_set_only_controls_affect_device(self, sp_pv, lewis_var, expected):
        self.ca.set_pv_value(sp_pv, expected)
        self._lewis.assert_that_emulator_value_is(lewis_var, str(expected))

    
    # def test_set_channel_commands_status_is_correct(self):
