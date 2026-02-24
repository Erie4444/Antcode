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
    empty = '.'
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.pathing = NuAntPathing(max_y,max_x)
        ##setting its target as the opponent's anthill
        self.opponentAnthillCoord = findAnthillCoord("X" if anthill == "@" else "@",max_y,max_x)
        self.anthillCoord = findAnthillCoord(anthill,max_y,max_x)
        self.id = 3
        self.foodCoords = []
        self.wallCoords = []
        self.target = ()
        self.removedCoords = []
        self.state = "food"

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        self.foodCoords, self.wallCoords, self.target = parseMessages(messages,self.id, self.foodCoords,self.wallCoords,self.target)

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return sendMessage(self.id,self.foodCoords,self.wallCoords,self.target,self.removedCoords)
    

    def one_step(self, x, y, vision, food):
        ##debug logs
        print(self.pathing.targets)
        print(self.opponentAnthillCoord)
        self.x = x
        self.y = y
        ##updating internal stuff
        self.pathing.updatePosition(x,y)
        self.parseVision(vision)
        if self.state == "food":
            ##assigning coordinates
            if not food: ##find a food
                if self.foodCoords and not self.target:
                    ##adding a random coordinate from self.foodCoords
                    self.target = random.choice(self.foodCoords)
                    self.pathing.clearTargets()
                    self.pathing.targets.append(self.target)
                elif not self.target:
                    ##default just goes to (10,10)
                    self.pathing.clearTargets()
                    self.pathing.targets.append((10,10))
            elif food: ##go to our anthill
                ##adds the anthill coord to self.target
                self.target = self.anthillCoord
                self.pathing.clearTargets()
                self.pathing.targets.append(self.target)

            inVision, directions, stuck = self.pathing.update()
            
            ##Moving the ant
            if inVision: ##if the destination is inside its vision
                if food:
                    ##drops a food on the anthill and then sets its internal state to beeline to the opposing anthill
                    self.state = "time to make them regret their actions"
                    self.pathing.clearTargets()
                    self.target = ()
                    ##adds the opponent's anthill to the targets
                    self.pathing.targets.append(self.opponentAnthillCoord)
                    return "DROP "+random.choice(directions)
                elif not food:
                    return "GET "+random.choice(directions)
            else:
                ##returns a random valid direction
                if directions:
                    return random.choice(directions)
                else:
                    return "PASS"

        ##beelining to the other team's anthill
        elif self.state == "time to make them regret their actions":
            ##checking if it is already on the opponent's anthill
            if x != self.pathing.targets[0][0] or y != self.pathing.targets[0][1]:
                inVision, directions, stuck = self.pathing.update()
                return random.choice(directions)
            return "PASS"
        return "PASS"
    
    ##same parsevision code as most of my ants
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