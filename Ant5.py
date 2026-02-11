from EricAntV3 import EricAntV3

class Ant5(EricAntV3):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.id = 5

    def receive_info(self, messages):
        super().receive_info(messages)

    def send_info(self):
        return super().send_info()
    
    def one_step(self, x, y, vision, food):
        return super().one_step(x,y,vision,food)
