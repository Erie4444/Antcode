from Strategies.ScoutStrategy import ScoutStrategy
from Util import *
import random

class EricScout (ScoutStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill)
        self.target = ()
        self.foodCoords = []
        self.wallCoords = []
        self.removedCoords = []
        self.id = 0
        self.patrolCoords = [(3,3),(max_x-3,max_y-3),(3,max_y-3),(max_x-3,3)]
        self.patrolIndex = 0

    def receive_info(self, messages):
        blackListedCoords = []
        removedCoords = []

        ##going through all the messages
        for message in messages:
            if message["ID"] != self.id: #not your own message
                ##adding all the foodCoords and wallCoords to internal lists (sets ensure there are no repeats)
                self.foodCoords = list(set(self.foodCoords+message["FOOD"]))
                self.wallCoords = list(set(self.wallCoords+message["WALLS"]))

                ##make sure to blacklist the coordinates other ants are targetting
                if message["TARGET"]:
                    blackListedCoords.append(message["TARGET"])

                ##removing coodinates the other ants have removed (took the last food in the pile)
                for coord in message["REMOVED"]:
                    if coord in self.foodCoords:
                        removedCoords.append(message["REMOVED"])
        
        ##remove blacklisted and removed coords from the internal foodCoords variable
        for coord in blackListedCoords:
            if coord in self.foodCoords:
                self.foodCoords.remove(coord)
            if coord == self.target:
                self.target = ()
        for coord in removedCoords:
            if coord in self.foodCoords:
                self.foodCoords.remove(coord)
            if coord == self.target:
                self.target = ()

    def send_info(self):
        return [{"ID":self.id,"FOOD":self.foodCoords,"WALLS":self.wallCoords,"TARGET":(),"REMOVED":self.removedCoords}]

    
    def one_step(self, x, y, vision, food):
        return super().one_step(x,y,vision,food)

    def patrolAlgorithm(self):
        super().patrolAlgorithm()
        if (self.x,self.y) == self.patrolCoords[self.patrolIndex] or not self.pathing.targets:
            self.patrolIndex = self.patrolIndex + 1 if self.patrolIndex < len(self.patrolCoords)-1 else 0
            self.pathing.clearTargets()
            self.pathing.targets.append(self.patrolCoords[self.patrolIndex])
    
    def stuckAlgorithm(self):
        super().stuckAlgorithm()
    
    def step(self):
        super().step()
        return random.choice(self.directions)
    
    def parseVision(self, vision):
        for y, row in enumerate(transpose(vision)):
            for x, item in enumerate(row):
                if item == self.wall:
                    self.pathing.addWall(x-1+self.x,y-1+self.y)
                    self.wallCoords.append((x-1+self.x,y-1+self.y))
                    self.wallCoords = list(set(self.wallCoords))

                ## if it is another ant (doesn't need annoyingAnt protection)
                elif item.isalpha() and not item in self.anthills: 
                    self.pathing.tempWalls.append((x-1+self.x,y-1+self.y))
                ##it found a food
                elif item != self.empty and not item in self.anthills:
                    self.foodCoords.append((x-1+self.x,y-1+self.y))
                    self.foodCoords = list(set(self.foodCoords))
                else: ## it is empty or an anthill, remove the coordinate from foodCoords if its there
                    if (x-1+self.x,y-1+self.y) in self.foodCoords:
                        self.foodCoords.remove((x-1+self.x,y-1+self.y))
                        self.removedCoords = (x-1+self.x,y-1+self.y)
    
    def log(self):
        pass