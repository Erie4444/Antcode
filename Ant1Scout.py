from EricScoutV1 import EricScout

class Ant1(EricScout):
    def __init__(self, max_x, max_y, anthill):
        self.id = 1
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass


    def receive_info(self, messages):
        super().receive_info(messages)

    def send_info(self):
        return super().send_info()
    
    def one_step(self, x, y, vision, food):
        return super().one_step(x,y,vision,food)
