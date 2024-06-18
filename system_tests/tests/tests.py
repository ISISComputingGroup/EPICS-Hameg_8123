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