from AntStrategy import AntStrategy
import random

##trying to make a flood fill pathfinding algo
class StarterStrat(AntStrategy):
    """An ant's strategy (brains) for moving during the game.
    
    See superclass documentation for more about this class's methods and
    attributes. This is a file you can copy to start making your own strategies.
    """
    
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.max_x = max_x
        self.max_y = max_y
        self.generateNewCoord()
        self.floodBoard = [["_" for i in range(max_x)] for j in range(max_y)]

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        pass

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return []
    
    def one_step(self, x, y, vision, food):
        '''Calculate and return a randomly chosen, but valid, next move.'''
        return "PASS"

    def generateNewCoord(self):
        self.targetCoord = (random.randrange(0,self.max_x),random.randrange(0,self.max_y))
    
    def updateFloodFill(self):
        for y, row in enumerate(self.floodBoard):
            for x, item in enumerate(row):
                pass
                ##bro flood fill pathfinding kills my brain
