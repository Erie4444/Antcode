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
        self.wallCoords = []
        self.priorityTarget = ()
        self.removedCoords = ()
        self.anthillCoord = findAnthillCoord(anthill,max_x,max_y)

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        for message in messages:
            if message["POSE"] != (self.x,self.y): #not your own message
                self.foodCoords = list(set(self.foodCoords+message["FOOD"]))
                self.wallCoords = list(set(self.wallCoords+message["WALLS"]))
                if message["TARGET"] and message["TARGET"] in self.foodCoords:
                    self.foodCoords.remove(message["TARGET"])
                for coord in message["REMOVED"]:
                    if coord in self.foodCoords:
                        self.foodCoords.remove(coord)

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return [{"POSE":(self.x,self.y),"FOOD":self.foodCoords,"WALLS":self.wallCoords,"TARGET":self.priorityTarget,"REMOVED":self.removedCoords}]
    
    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        action = ''
        self.pathing.updatePosition(x,y)
        self.parseVision(vision)

        if food:
            self.pathing.clearTargets()
            self.priorityTarget = ()
            self.pathing.targets.append(self.anthillCoord)
        else:
            if not self.priorityTarget in self.foodCoords and self.foodCoords:
                self.priorityTarget = random.choice(self.foodCoords)
                self.pathing.clearTargets()
                self.pathing.targets.append(self.priorityTarget)

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
        print([self.pathing.targets,self.priorityTarget,food,action])
        return action


    def parseVision(self,vision):
        for y, row in enumerate(transpose(vision)):
            for x, item in enumerate(row):
                if item == self.wall: ##if it is a wall
                    self.pathing.addWall(x-1+self.x,y-1+self.y)
                    self.wallCoords.append((x-1+self.x,y-1+self.y))
                    self.wallCoords = list(set(self.wallCoords))
                elif item.isalpha(): ## if it is another ant
                    self.pathing.tempWalls.append((x-1+self.x,y-1+self.y))
                elif item != self.empty and not item in self.anthills: ## if it is a food pile
                    self.foodCoords.append((x-1+self.x,y-1+self.y))
                    self.foodCoords = list(set(self.foodCoords))
                else: ## it is empty or an anthill
                    if (x-1+self.x,y-1+self.y) in self.foodCoords:
                        self.foodCoords.remove((x-1+self.x,y-1+self.y))
                        self.removedCoords = (x-1+self.x,y-1+self.y)