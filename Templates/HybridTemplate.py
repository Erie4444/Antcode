from Strategies.HybridStrategy import HybridStrategy
from Util import *
'''
Eric Zhao
2/10/2026

'''


class HybridTemplate(HybridStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x,max_y,anthill)


    def receive_info(self, messages):
        pass

    def send_info(self):
        return []
    
    def one_step(self, x, y, vision, food):
        return super().one_step()

    def assignTarget(self):
        super().assignTarget()

    def step(self):
        super().step()

    def parseVision(self, vision:list):
        pass
    
    def log(self):
        pass    


    