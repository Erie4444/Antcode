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
    with open(r"AntLog.txt", "w") as log:
        log.write("")
    empty = '.'
    wall = '#'
    anthills = '@X'
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.roundCounter = 0
        self.pathing = NuAntPathing(max_x,max_y)
        self.foodCoords = []
        self.wallCoords = []
        self.priorityTarget = ()
        self.removedCoords = ()
        self.priority = 0
        self.anthillCoord = findAnthillCoord(anthill,max_x,max_y)

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        for message in messages:
            if message["ID"] != self.priority: #not your own message
                self.foodCoords = list(set(self.foodCoords+message["FOOD"]))
                self.wallCoords = list(set(self.wallCoords+message["WALLS"]))
                if message["TARGET"] and message["TARGET"] in self.foodCoords:
                    self.foodCoords.remove(message["TARGET"])
                for coord in message["REMOVED"]:
                    if coord in self.foodCoords:
                        self.foodCoords.remove(coord)

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return [{"ID":self.priority,"FOOD":self.foodCoords,"WALLS":self.wallCoords,"TARGET":self.priorityTarget,"REMOVED":self.removedCoords}]
    
    def assignNewTarget(self):
        self.priorityTarget = random.choice(self.foodCoords)
        self.pathing.clearTargets()
        self.pathing.targets.append(self.priorityTarget)

    def one_step(self, x, y, vision, food):
        try:
            self.x = x
            self.y = y
            action = ''
            self.pathing.updatePosition(x,y)
            self.parseVision(vision)

            if food:
                self.pathing.clearTargets()
                self.priorityTarget = () ##so the other ants can still go towards the anthill
                self.pathing.targets.append(self.anthillCoord)
            else:
                ##if its trying to go to the anthill when it needs food, it clears all targets so it goes back to (10,10)
                if self.pathing.targets == [self.anthillCoord]:
                    self.pathing.clearTargets()
                ##choosing a new target
                if not self.priorityTarget in self.foodCoords and self.foodCoords:
                    self.assignNewTarget()
            inVision,directions,isStuck = self.pathing.update()

            if isStuck: ##if its stuck, pick a new random food and go towards there
                self.assignNewTarget()
                inVision,directions,isStuck = self.pathing.update()

            if not self.pathing.targets or not self.foodCoords:
                self.pathing.clearTargets()
                self.pathing.targets.append((self.max_x-2,self.max_y-2))
                inVision,directions,isStuck = self.pathing.update()
                
            pickedDirection = random.choice(directions)
            if inVision:
                if food:
                    action = "DROP "
                else:
                    action = "GET "
            action+=pickedDirection
            self.roundCounter+=1
            with open(r"AntLog.txt","a") as log:
                log.write(" ".join([f"Ant{self.priority}",str(self.roundCounter),str(self.x),str(self.y),str(self.foodCoords),str(self.pathing.targets),str(self.priorityTarget),str(food),str(action)])+"\n")
            print([f"Ant{self.priority}",self.x,self.y,self.pathing.targets,self.priorityTarget,food,action])
            return action
        except Exception as e:
            with open(r"AntLog.txt","a") as log:
                log.write(f"Ant{self.priority} Error: {e} \n")


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