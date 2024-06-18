from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

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
        }

        self.device: SimulatedHameg8123 = self.device

    
    def get_idn(self):
        return self.device.get_idn()


    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))