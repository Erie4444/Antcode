from AntStrategy import AntStrategy
import random
from collections import deque

##trying to make a flood fill pathfinding algo
class FPAAnt(AntStrategy):
    empty = ""
    wall = "#"
    """An ant's strategy (brains) for moving during the game.
    
    See superclass documentation for more about this class's methods and
    attributes. This is a file you can copy to start making your own strategies.
    """
    
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.cellsToCheck = deque([])
        self.targets = []
        self.directions=[(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        self.resetFloodBoard()
        self.resetInternalBoard()
        self.generateNewCoord()
        self.generateNewCoord()
        self.generateNewCoord()

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        pass

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return []
    
    def one_step(self, x, y, vision, food):
        '''Calculate and return a randomly chosen, but valid, next move.'''
        return "PASS"

    def generateNewCoord(self):
        self.targetCoord = (random.randrange(1,self.max_x-1), random.randrange(1,self.max_y-1))
        self.targets.append(self.targetCoord)

    def initQueue(self):
        self.cellsToCheck = deque(self.targets)
    
    def addWalls(self,count):
        for i in range(count):
            self.internalBoard[random.randrange(1,self.max_y)][random.randrange(1,self.max_x-1)] = "#"
    
    def updateFloodFill(self):
        self.initQueue()
        self.resetFloodBoard()
        while self.cellsToCheck:
            cell = self.cellsToCheck.popleft()
            Cellx,Celly = cell[0],cell[1]
            for xOffset,yOffset in self.directions:
                xCurrent,yCurrent = Cellx+xOffset,Celly+yOffset
                if self.internalBoard[yCurrent][xCurrent] != self.wall and self.floodBoard[yCurrent][xCurrent] == self.empty:
                    self.floodBoard[yCurrent][xCurrent] = self.floodBoard[Celly][Cellx]+1
                    self.cellsToCheck.append((xCurrent,yCurrent))

    def printFloodBoard(self):
        for row in self.floodBoard:
            print(row)
    
    def printInternalBoard(self):
        for row in self.internalBoard:
            print(row)
    
    def printCellQueue(self):
        print(self.cellsToCheck)
    
    def printChosenCoord(self):
        print(self.targetCoord)
    
    def resetFloodBoard(self):
        self.floodBoard = [[self.empty for i in range(self.max_x)] for j in range(self.max_y)]
        for x,y in self.targets:
            self.floodBoard[y][x]=0

    def resetInternalBoard(self):
        self.internalBoard = [["." if i>0 and i<self.max_x-1 and j>0 and j<self.max_y-1 else self.wall for i in range(self.max_x)] for j in range(self.max_y)]

      

testAnt = FPAAnt(20,20,1)
testAnt.updateFloodFill()
testAnt.printFloodBoard()