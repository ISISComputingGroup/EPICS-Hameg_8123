import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc
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

    def test_gate_time_on_device_matches_rbv(self):
        gate_time = 300
        self._lewis.backdoor_set_on_device("gate_time", gate_time)
        self.ca.assert_that_pv_is("GATETIME", gate_time)
    
    def test_gate_time_on_device_matches_rbv_after_sp_set(self):
        gate_time = 301
        self.ca.set_pv_value("GATETIME:SP", gate_time)
        self.ca.assert_that_pv_is("GATETIME", gate_time)
    
    def test_func_on_device_matches_rbv(self):
        func = "FRB"
        self._lewis.backdoor_set_on_device("func", func)
        self.ca.assert_that_pv_is("FUNCTION", func)
    
    def test_count_and_unit_on_device_matches_rbv(self):
        count = 51
        unit = "S"
        self._lewis.backdoor_set_on_device("count", count)
        self._lewis.backdoor_set_on_device("count_unit", unit)
        self.ca.assert_that_pv_is("COUNTS", count)
        self.ca.assert_that_pv_is("COUNTS.EGU", unit)

