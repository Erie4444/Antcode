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

        self.pathing = NuAntPathing(max_y, max_x)
        self.foodCoords = []
        self.wallCoords = []
        self.priorityTarget = ()
        self.removedCoords = []             
        self.blackListedCoords = []          
        self.anthillCoord = findAnthillCoord(anthill, max_y, max_x)
        self.priority = 0
        self.delivered = False ##if the ant has delivered yet

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
            self.pathing.targets.append(self.priorityTarget) ##

    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        action = ''

        self.pathing.updatePosition(x, y)
        self.parseVision(vision)
        
        cardinals = { "NORTH": (1, 0), ##cardinals from smarter random strat
                "SOUTH": (1, 2),
                "EAST": (2, 1),
                "WEST": (0, 1),
                "NORTHEAST": (2, 0),
                "SOUTHEAST": (2, 2),
                "SOUTHWEST": (0, 2),
                "NORTHWEST": (0, 0),
                "HERE": (1,1) }
                
        if food and not self.delivered: ##if you are carrying food and haven't delivered food yet
            self.pathing.clearTargets() ##Stops going anywhere else
            self.priorityTarget = ()
            self.pathing.targets.append(self.anthillCoord) ##goes to anthill to drop the food

        elif (self.foodCoords and self.priorityTarget not in self.foodCoords) and not self.delivered:
            self.assignNewTarget()
            
        elif self.delivered: ##once you have delivered you just randomly wander around
            self.pathing.clearTargets()
            self.priorityTarget = ()
            while True: ##keeps checking every direction until not its not a wall or ant
                move = random.choice(["NORTH", "NORTHEAST", "EAST", "SOUTHEAST", "SOUTH", "SOUTHWEST", "WEST", "NORTHWEST"])
                coords = cardinals[move] ##checks the coordinates in the dictionary depending on the direction
                tile = vision[coords[0]][coords[1]]
                if tile != "#" and not tile.isalpha(): ##Tries not to run straight into another ants current location in it's vision if it passes to minimie chance of collision.
                    return move 
                
        if not self.pathing.targets:

            self.pathing.targets.append((10, 10)) ##if there is NO other targets, go to 10, 10 as a fallback

        inVision, directions, _ = self.pathing.update() 
        if not directions:
                direction = random.choice(["NORTH", "NORTHEAST", "EAST", "SOUTHEAST", "SOUTH", "SOUTHWEST", "WEST", "NORTHWEST", "HERE"])
        pickedDirection = random.choice(directions)
        

        if inVision and len(directions) == 1: ##if the target (anthill) is 
            if food and not self.delivered: ##if you are carrying food (which means you are going to your anthill) you drop it there.
                action = "DROP "
                self.delivered = True
            else:
                action = "GET " ##Your target is food since your not carrying it and have not delivered, so you can take it

        action += pickedDirection ##Action
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
