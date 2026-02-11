from WorkerStrategy import WorkerStrategy
from Util import *
import random

class EricAntV3 (WorkerStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill)
        self.target = ()
        self.foodCoords = []
        self.wallCoords = []
        self.removedCoords = []
    
    def initTargets(self):
        self.pathing.clearTargets()
        if self.target:
            self.pathing.targets.append(self.target)
        
    def resetTargets(self):
        self.pathing.clearTargets()
        self.target = ()

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
                        self.removedCoords.append(message["REMOVED"])
        
        ##remove blacklisted and removed coords from the internal foodCoords variable
        for coord in blackListedCoords:
            if coord in self.foodCoords:
                self.foodCoords.remove(coord)
            if coord == self.target:
                self.target = ()
        for coord in self.removedCoords:
            if coord in self.foodCoords:
                self.foodCoords.remove(coord)
            if coord == self.target:
                self.target = ()

    def send_info(self):
        return [{"ID":self.id,"FOOD":self.foodCoords,"WALLS":self.wallCoords,"TARGET":self.target,"REMOVED":self.removedCoords}]
    
    def one_step(self, x, y, vision, food):
        return super().one_step(x,y,vision,food)
    
    def seekingAlgorithm(self):
        super().seekingAlgorithm()
        if not self.target:
            self.target = random.choice(self.foodCoords) if self.foodCoords else ()
        self.initTargets()
    
    def retreatAlgorithm(self):
        super().retreatAlgorithm()
        self.target = self.anthillCoord
        self.initTargets()
    
    def defaultAlgorithm(self):
        super().defaultAlgorithm()
        self.pathing.clearTargets()
        self.pathing.targets.append((10,10))
    
    def step(self):
        action = ""
        super().step()
        if self.inVision:
            if self.food:
                action = "DROP "
                self.resetTargets()
            else:
                action = "GET "
        action+=random.choice(self.directions)
        print(action, self.target)
        return action
    
    def parseVision(self, vision):
        for y, row in enumerate(transpose(vision)):
            for x, item in enumerate(row):
                if item == self.wall:
                    self.pathing.addWall(x-1+self.x,y-1+self.y)
                    self.wallCoords.append((x-1+self.x,y-1+self.y))
                    self.wallCoords = list(set(self.wallCoords))

                ## if it is another ant NOTE: 2nd part of the statement is to ignore if its the anthill to mitigate the AnnoyingAnt
                elif item.isalpha() and not item in self.anthills and (x-1+self.x,y-1+self.y) != self.anthillCoord: 
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