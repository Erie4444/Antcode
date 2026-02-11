from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
from Util import *
import random
import json

'''
Sherjil Khan
2/2/2026
Uses NuAntTemplateV2. Modified to grab one piece of food and then scout full tame afterwards.
'''

class NuScoutStrat(AntStrategy):
    empty = '.'
    wall = '#'
    anthills = '@X'

    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill)

        self.pathing = NuAntPathing(max_x, max_y)
        self.foodCoords = []
        self.wallCoords = []
        self.priorityTarget = ()
        self.removedCoords = []             
        self.blackListedCoords = []          
        self.anthillCoord = findAnthillCoord(anthill, max_x, max_y)
        self.priority = 0

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        blackListedCoords = []
        removedCoords = []
        for message in messages:
            if message["ID"] != self.priority: #not your own message
                self.foodCoords = list(set(self.foodCoords+message["FOOD"]))
                self.wallCoords = list(set(self.wallCoords+message["WALLS"]))
                if message["TARGET"]:
                    blackListedCoords.append(message["TARGET"])
                for coord in message["REMOVED"]:
                    if coord in self.foodCoords:
                        removedCoords.append(message["REMOVED"])
        for coord in blackListedCoords:
            if coord in self.foodCoords:
                self.foodCoords.remove(coord)
        for coord in removedCoords:
            if coord in self.foodCoords:
                self.foodCoords.remove(coord)

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return [{"ID":self.priority,"FOOD":self.foodCoords,"WALLS":self.wallCoords,"TARGET":self.priorityTarget,"REMOVED":self.removedCoords}]

    def assignNewTarget(self):
        if self.foodCoords:
            self.priorityTarget = random.choice(self.foodCoords)
            self.pathing.clearTargets()
            self.pathing.targets.append(self.priorityTarget)

    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        action = ''

        self.pathing.updatePosition(x, y)
        self.parseVision(vision)

        if food:
            self.pathing.clearTargets()
            self.priorityTarget = ()
            self.pathing.targets.append(self.anthillCoord)
        else:
            if self.foodCoords and self.priorityTarget not in self.foodCoords:
                self.assignNewTarget()

        if not self.pathing.targets:
            self.pathing.targets.append((10, 10))

        inVision, directions, _ = self.pathing.update()
        if not directions:
            directions = ["N", "E", "W", "S"]
        pickedDirection = random.choice(directions)
        

        if inVision and len(directions) == 1:
            action = "DROP " if food else "GET "

        action += pickedDirection
        print([self.pathing.targets, self.priorityTarget, food, action])
        return action

    def parseVision(self, vision):
        for y, row in enumerate(transpose(vision)):
            for x, item in enumerate(row):
                worldX = x - 1 + self.x
                worldY = y - 1 + self.y

                if item == self.wall:
                    self.pathing.addWall(worldX, worldY)
                    self.wallCoords.append((worldX, worldY))
                    self.wallCoords = list(set(self.wallCoords))

                elif item.isalpha():
                    self.pathing.tempWalls.append((worldX, worldY))

                elif item != self.empty and item not in self.anthills:
                    self.foodCoords.append((worldX, worldY))
                    self.foodCoords = list(set(self.foodCoords))

                else:
                    if (worldX, worldY) in self.foodCoords:
                        self.foodCoords.remove((worldX, worldY))
                        self.removedCoords.append((worldX, worldY))
