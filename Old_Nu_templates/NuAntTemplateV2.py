from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
'''
Eric Zhao
2/1/2026
new V2 template using NuAntPathing.py for easier readability
'''


class TemplateAnt(AntStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.pathing = NuAntPathing(max_x,max_y)

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        pass

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return []
    

    def one_step(self, x, y, vision, food):
        pass