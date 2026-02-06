from EricAntV2 import EricAntV2
import random

class Ant1(EricAntV2):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.priority = 1

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        super().receive_info(messages)

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return super().send_info()
    
    def one_step(self, x, y, vision, food):
        '''Calculate and return a randomly chosen, but valid, next move.'''
        return super().one_step(x,y,vision,food)
