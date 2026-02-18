from Strategies.ScoutStrategy import ScoutStrategy

class ScoutTemplate (ScoutStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill)

    def receive_info(self, messages):
        pass

    def send_info(self):
        return []
    
    def one_step(self, x, y, vision, food):
        return super().one_step()

    def patrolAlgorithm(self):
        super().patrolAlgorithm()
    
    def stuckAlgorithm(self):
        super().stuckAlgorithm()
    
    def step(self):
        super().step()
    
    def parseVision(self, vision):
        pass
    
    def log(self):
        pass