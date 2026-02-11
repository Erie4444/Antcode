from AntStrategy import AntStrategy
import random
'''
Yifong Liao
2/9/2026
using Eric's basic ant templete
defender ant
'''


class DefenderAnt(AntStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill)
        self.wallCoords = []
        self. tempObstacles = []
        self.priority = 0
        self.PatrolPoints = [
            (2,2),
            (max_x-3,2),
            (2,max_y-3),
            (max_x,max_y-3)
        ]
        self.currentTarget = random.choice(self.patrolPoints)

    def recive_info(self, messages):
        
        for msg in messages:
            self.wallCoords += msg.get("WALLS", [])
        self.wallCoords = list(set(self.wallCoords))

    def send_info(self):
        #sends information to teamates
        return [{"ID": self.priority, "FOOD": [], "WALLS": self.wallCoords, "TARGET": (), "REMOVED": ()}]
    
    def updateInternalBoard(self, vision):

        for dx, dy in self.directions:
            cellX = self.x + dx
            cellY = self.y + dy
            val = vision[1+dy][1+dx]

            #track walls
            if val == "#":
                if (cellX, cellY) not in self.wallCoords:
                    self.wallCoords.append((cellX, cellY))
            
            #track other ants
            elif val.isalpha() and val not in "@X":
                if (cellX, cellY) not in self.tempObstacles:
                    self.tempObstacles.append((cellX, cellY))

            #update board again
            self.internalBoard[cellY][cellX] = val


        self.updateFloodFill()

    def initTargets(self):

        self.targets = [self.currentTarget]

    
    def generateDirection(self):

        direction = super().generateDirection()

        if (self.x, self.y) == self.currectTarget:
            self.currentTarget = random.choice(self.patrolPoints)
            self.targets = [self.currentTarget]
            self.initQueue()
        return direction
    
                                           