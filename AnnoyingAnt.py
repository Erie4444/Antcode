from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
from Util import *
import random
'''
Eric Zhao
2/8/2026
this mf just plants himself on the opponent's anthill
'''


class AnnoyingAnt(AntStrategy):
    wall = "#"
    anthills = "@X"
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.pathing = NuAntPathing(max_x,max_y)
        ##setting its target as the opponent's anthill
        self.pathing.targets.append(findAnthillCoord("X" if anthill == "@" else "@",max_y,max_x))

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        pass

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return []
    

    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        if x != self.pathing.targets[0][0] or y != self.pathing.targets[0][1]:
            self.parseVision(vision)
            self.pathing.updatePosition(x,y)
            inVision, directions, stuck = self.pathing.update()
            return random.choice(directions)
        return "PASS"
    
    def parseVision(self,vision):
        for y, row in enumerate(transpose(vision)):
            for x, item in enumerate(row):
                if item == self.wall: ##if it is a wall
                    self.pathing.addWall(x-1+self.x,y-1+self.y)
                elif item.isalpha() and not item in self.anthills: ## if it is another ant
                    self.pathing.tempWalls.append((x-1+self.x,y-1+self.y))