from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice

class SimulatedHameg8123(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.idn="HAMEG HM8123"
        self.func = "FRA"
        self.gate_time = 400
        self.count = 0
        self.count_unit = "Hz"
        self.channels = {
            "A": HamegChannel("A"),
            "B": HamegChannel("B")
        }
        self.started = False
        self.stopped = False 
        self.reset = False
        self.triggered = True
        self.pulses_per_rev = 100


    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    
    def get_idn(self) -> str:
        return self.idn
    
    def get_gate_time(self) -> int:
        return self.gate_time
    
    def get_results(self) -> str:
        return f"{self.count}, {self.count_unit}"
    

class HamegChannel():
    coupling = "AC"
    lowpass = True
    attenuation = "1"
    slope = "+"
    impedance = "L"
    trigger_level = 1

    def __init__(self, chan: str):
        self.chan = chan
