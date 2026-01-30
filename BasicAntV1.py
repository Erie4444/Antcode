from AntStrategy import AntStrategy
import random
from collections import deque
'''
Eric Zhao
1/29/2026
A basic ant with flood fill algorithm for pathfinding
Just pathing, no other actions
'''


class BasicAnt(AntStrategy):
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
        self.stringDirections=["SOUTHEAST","EAST","NORTHEAST","SOUTH","NORTH","SOUTHWEST","WEST","NORTHWEST"]
        self.x=""
        self.y=""
        self.resetFloodBoard()
        self.resetInternalBoard()

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        pass

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        return []
    
    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        ##converting it so y is the row and x is the column (0,0) is the top left corner
        actualVision = [[vision[x][y]for x in range(len(vision))]for y in range(len(vision))]
        ##marks where it is
        self.internalBoard[y][x] = "A"
        ##updates the internalBoard with what it sees
        self.updateInternalBoard(actualVision)

        ##debug
        self.printFloodBoard()
        
        ##====PATH GENERATION====
        if not food:
            ##to track where the shortest path is (distance for the value in the floodboard and index for the index in the direction lists)
            smallestDistance = 999999
            smallestIndex=10
            for index,offsetTuple in enumerate(self.directions):
                xOffset = offsetTuple[0]
                yOffset = offsetTuple[1]
                ##checking if the cell has a smaller floodvalue than the smallest one stored
                if self.floodBoard[self.y+yOffset][self.x+xOffset]!="" and self.floodBoard[self.y+yOffset][self.x+xOffset] < smallestDistance:
                    ##setting the values
                    smallestIndex = index
                    smallestDistance=self.floodBoard[self.y+yOffset][self.x+xOffset]
            ##checking if a direction was found (index of the direction list is 8 so 10 means it didnt change anything)
            if smallestIndex !=10:
                print(self.stringDirections[smallestIndex])
                return self.stringDirections[smallestIndex]
            
            ##if no food detected go in a random direction
            while True:
                index = random.randrange(0,len(self.directions))
                xOffset = self.directions[index][0]
                yOffset = self.directions[index][1]
                ##to not collide into walls or other ants
                if self.internalBoard[self.y+yOffset][self.x+xOffset] != "#" and not self.internalBoard[self.y+yOffset][self.x+xOffset].isalpha():
                    print(self.stringDirections[index])
                    return self.stringDirections[index]

    def generateFloodVision(self):
        vision = [['' for i in range(3)] for j in range(3)]
        for xOffset,yOffset in self.directions:
            vision[1+yOffset][1+xOffset] = self.floodBoard[self.y+yOffset][self.x+xOffset]
        return vision

    def generateNewCoord(self):
        self.targetCoord = (random.randrange(1,self.max_x-1), random.randrange(1,self.max_y-1))
        self.targets.append(self.targetCoord)

    def initQueue(self):
        self.cellsToCheck = deque(self.targets)
    
    def addWalls(self,count):
        for i in range(count):
            self.internalBoard[random.randrange(1,self.max_y)][random.randrange(1,self.max_x-1)] = "#"
    
    def updateInternalBoard(self,vision):
        for xOffset, yOffset in self.directions:
            ##updating the internal board based on vision
            self.internalBoard[self.y+yOffset][self.x+xOffset] = vision[1+yOffset][1+xOffset]
            ##checking if there is any food in vision
            if vision[1+yOffset][1+xOffset].isnumeric():
                ##adds the food as a target
                self.targets.append((self.x+xOffset,self.y+yOffset))
        self.updateFloodFill()

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
    
    def printTargets(self):
        print(self.targets)
    
    def resetFloodBoard(self):
        self.floodBoard = [[self.empty for i in range(self.max_x)] for j in range(self.max_y)]
        for x,y in self.targets:
            self.floodBoard[y][x]=0

    def resetInternalBoard(self):
        self.internalBoard = [["." if i>0 and i<self.max_x-1 and j>0 and j<self.max_y-1 else self.wall for i in range(self.max_x)] for j in range(self.max_y)]