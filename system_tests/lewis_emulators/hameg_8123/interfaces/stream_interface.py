from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder

from ..device import SimulatedHameg8123


@has_log
class Hameg8123StreamInterface(StreamInterface):
    in_terminator = "\r"
    out_terminator = "\r"

    def __init__(self):
        super(Hameg8123StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_idn).escape("IDN").eos().build(),
            CmdBuilder(self.get_results).escape("XMT").eos().build(),
            CmdBuilder(self.get_func).escape("FN?").eos().build(),
            CmdBuilder(self.get_gate_time).escape("SMT?").eos().build(),
            CmdBuilder(self.set_gate_time).escape("SMT").int().eos().build(),
            CmdBuilder(self.set_pulses_per_rev).escape("NPC").int().eos().build(),
            CmdBuilder(self.trigger).escape("TRG").eos().build(),
            CmdBuilder(self.start).escape("STR").eos().build(),
            CmdBuilder(self.stop).escape("STP").eos().build(),
            CmdBuilder(self.reset).escape("RES").eos().build(),
            CmdBuilder(self.set_trigger_level).escape("LV").arg("A|B").float().eos().build(),
            CmdBuilder(self.get_trigger_level).escape("LV").arg("A|B").escape("?").eos().build(),
            CmdBuilder(self.set_func)
            .arg("FRA|FRB|FRC|PRA|WDA|RAB|DTA|TI1|TIA|PHA|RPM|TOT")
            .eos()
            .build(),
            CmdBuilder(self.get_channel_settings).escape("M").arg("A|B").escape("?").eos().build(),
            CmdBuilder(self.set_atten).escape("A").arg("A|B").arg("0|1|2").eos().build(),
            CmdBuilder(self.set_slope).escape("S").arg("A|B").arg("0|1").eos().build(),
            CmdBuilder(self.set_low_pass).escape("F").arg("A|B").arg("0|1").eos().build(),
            CmdBuilder(self.set_coupling).arg("AC|DC").arg("A|B").eos().build(),
            CmdBuilder(self.set_impedance).escape("O").arg("A|B").arg("H|L").eos().build(),
        }

        self.device: SimulatedHameg8123 = self.device

    def set_atten(self, channel, atten):
        self.device.channels[channel].attenuation = atten

    def set_slope(self, channel, slope):
        self.device.channels[channel].slope = "+" if slope == "0" else "-"

    def set_low_pass(self, channel, lowpass):
        self.device.channels[channel].lowpass = bool(lowpass)

    def set_coupling(self, coupling, channel):
        self.device.channels[channel].coupling = coupling

    def set_impedance(self, channel, impedance):
        self.device.channels[channel].impedance = impedance

    def get_channel_settings(self, channel):
        channel_obj = self.device.channels[channel]
        imp = "50" if channel_obj.impedance == "L" else "1 M"
        lowpass = "ON" if channel_obj.lowpass else "OFF"
        att = str(int(channel_obj.attenuation) + 1)
        return (
            f"Z:{imp} CPL:{str(channel_obj.coupling)} FL:{lowpass} ATT:{att} SLP{channel_obj.slope}"
        )

    def get_idn(self):
        return self.device.get_idn()

    def get_func(self):
        return self.device.func

    def set_func(self, func):
        self.device.func = func

    def get_gate_time(self):
        return self.device.get_gate_time()

    def get_results(self):
        return self.device.get_results()

    def set_gate_time(self, gate_time):
        self.device.gate_time = gate_time

    def set_pulses_per_rev(self, pulses_per_rev):
        self.device.pulses_per_rev = pulses_per_rev

    def set_trigger_level(self, channel, trigger_level):
        self.device.channels[channel].trigger_level = trigger_level

    def get_trigger_level(self, channel):
        return self.device.channels[channel].trigger_level

    def reset(self):
        self.device.reset = True

    def start(self):
        self.device.started = True

    def stop(self):
        self.device.stopped = True

    def trigger(self):
        self.device.triggered = True

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))
