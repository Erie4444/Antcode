from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
from Util import *
import random
'''
Eric Zhao
2/2/2026
A test and using NuAntTemplateV2
'''
class EricAntV2(AntStrategy):
    empty = '.'
    wall = '#'
    anthills = '@X'
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.pathing = NuAntPathing(max_x,max_y)
        self.foodCoords = []
        self.anthillCoord = findAnthillCoord(anthill,max_x,max_y)

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        pass

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return []
    
    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        action = ''
        self.pathing.updatePosition(x,y)
        self.parseVision(vision)
        self.pathing.clearTargets()

        if food:
            self.pathing.targets.append(self.anthillCoord)
        else:
            self.pathing.targets.extend(self.foodCoords)

        if not self.pathing.targets:
            self.pathing.targets.append((10,10))

        inVision,directions = self.pathing.update()
        pickedDirection = random.choice(directions)
        if inVision:
            if food:
                action = "DROP "
            else:
                action = "GET "
        action+=pickedDirection
        print(self.pathing.targets)
        print(self.pathing)
        print(action)
        return action


    def parseVision(self,vision):
        for y, row in enumerate(transpose(vision)):
            for x, item in enumerate(row):
                if item == self.wall: ##if it is a wall
                    self.pathing.addWall(x-1+self.x,y-1+self.y)
                elif item.isalpha(): ## if it is another ant
                    self.pathing.tempWalls.append((x-1+self.x,y-1+self.y))
                elif item != self.empty and not item in self.anthills: ## if it is a food pile
                    self.foodCoords.append((x-1+self.x,y-1+self.y))
                    self.foodCoords = list(set(self.foodCoords))
                else: ## it is empty or an anthill
                    print((x-1+self.x,y-1+self.y))
                    if (x-1+self.x,y-1+self.y) in self.foodCoords:
                        self.foodCoords.remove((x-1+self.x,y-1+self.y))