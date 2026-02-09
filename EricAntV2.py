from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
from Util import *
import random
'''
Eric Zhao
2/2/2026
Eric's worker ant (food gathering)
Modified: 2/8/2026
'''
class EricAntV2(AntStrategy):
    ##clearing the log file
    with open(r"AntLog.txt", "w") as log:
        log.write("")
    
    ##internal constants
    empty = '.'
    wall = '#'
    anthills = '@X'

    def __init__(self, max_x, max_y, anthill):
        ##initializing variables
        super().__init__(max_x, max_y, anthill)
        self.roundCounter = 0
        self.pathing = NuAntPathing(max_x,max_y)
        self.patrolPoints = [(2,2),(max_x-2,max_y-2),(2,max_y-2),(max_x-2,2)]

        ##used for messages
        self.foodCoords = []
        self.wallCoords = []
        self.priorityTarget = ()
        self.removedCoords = ()
        self.priority = 0

        ##finding anthill coordinate
        self.anthillCoord = findAnthillCoord(anthill,max_x,max_y)

    def receive_info(self, messages):
        
        blackListedCoords = []
        removedCoords = []

        ##going through all the messages
        for message in messages:
            if message["ID"] != self.priority: #not your own message
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
        for coord in removedCoords:
            if coord in self.foodCoords:
                self.foodCoords.remove(coord)

    def send_info(self):
        return [{"ID":self.priority,"FOOD":self.foodCoords,"WALLS":self.wallCoords,"TARGET":self.priorityTarget,"REMOVED":self.removedCoords}]
    
    def assignNewTarget(self):
        ##picking a random coordinate
        if self.foodCoords:
            self.priorityTarget = random.choice(self.foodCoords)
        ##adding the coordinate to the pathing.targets variable
        self.pathing.clearTargets()
        self.pathing.targets.append(self.priorityTarget)

    def checkHasTarget(self):
        ##checking if we have a target
        if not self.pathing.targets or not self.foodCoords:
            ##adding the default coord (the one ants default if there nothing there)
            self.pathing.clearTargets()
            if self.anthill == "@":
                self.pathing.targets.append((self.max_x-2,self.max_y-2))
            else:
                self.pathing.targets.append((2,2))

    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        action = ''

        ##updating pathing & other variables
        self.pathing.updatePosition(x,y)
        self.parseVision(vision)

        if food:
            self.pathing.clearTargets()
            self.priorityTarget = () ##so the other ants can still go towards the anthill
            self.pathing.targets.append(self.anthillCoord)
        else:
            ##if its trying to go to the anthill when it needs food, it clears all targets (just a failsafe)
            if self.pathing.targets == [self.anthillCoord]:
                self.pathing.clearTargets()

            ##choosing a new target
            if not self.priorityTarget in self.foodCoords and self.foodCoords:
                self.assignNewTarget()
        
        ##checking if a target was assigned (if no goes to a default coord)
        self.checkHasTarget()
        ##updates pathing
        inVision,directions,isStuck = self.pathing.update()

        if isStuck: ##if its stuck, pick a new random food and go towards there
            self.assignNewTarget()
            self.checkHasTarget()
            inVision,directions,isStuck = self.pathing.update()
            
        pickedDirection = random.choice(directions)

        ##if it can see its destination, it adds the corresponding action ("GET" or "DROP")
        if inVision:
            if food:
                action = "DROP "
            else:
                action = "GET "
        action+=pickedDirection
        self.roundCounter+=1
        ##==just debugging stuff==
        ##with open(r"AntLog.txt","a") as log:
            ##log.write(" ".join([f"Ant{self.priority}",str(self.roundCounter),str(self.x),str(self.y),str(self.pathing.targets),str(food),str(action)])+"\n")
        ##print([f"Ant{self.priority} Side: {self.anthill} Anthill Coord: {self.anthillCoord} Invision {inVision}",self.x,self.y,self.pathing.targets,self.priorityTarget,food,action])
        return action

    def parseVision(self,vision):
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