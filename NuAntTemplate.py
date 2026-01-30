from AntStrategy import AntStrategy
import random
from collections import deque
'''
Eric Zhao
1/29/2026
A basic ant with flood fill algorithm for pathfinding
Just pathing, no other actions
'''


class TemplateAnt(AntStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        ##DONT TOUCH THESE VARIABLES (USED FOR FLOODFILL)
        self.cellsToCheck = deque([])
        self.targets = []
        self.directions=[(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
        self.stringDirections=["SOUTHEAST","EAST","NORTHEAST","SOUTH","NORTH","SOUTHWEST","WEST","NORTHWEST"]
        self.x=""
        self.y=""

        ##initializing the internal boards
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
        
        ##====PATH GENERATION====
        direction = self.generateDirection()
        if direction != None:
            print(direction)
            return direction
        else:
            return "PASS"

    ##detecting the shortest path based on the flood fill
    def generateDirection(self):
        ##to track where the shortest path is (distance for the value in the floodboard and index for the index in the direction lists)
        smallestDistance = 999999
        validDirections = []
        for index,offsetTuple in enumerate(self.directions):
            xOffset = offsetTuple[0]
            yOffset = offsetTuple[1]
            ##checking if the cell has a smaller floodvalue than the smallest one stored
            if self.floodBoard[self.y+yOffset][self.x+xOffset]!="" and self.floodBoard[self.y+yOffset][self.x+xOffset] < smallestDistance:
                ##setting the values
                smallestDistance=self.floodBoard[self.y+yOffset][self.x+xOffset]
                validDirections = [self.stringDirections[index]]
            ## if it found another valid direction with the same smallest distance
            elif self.floodBoard[self.y+yOffset][self.x+xOffset]!="" and self.floodBoard[self.y+yOffset][self.x+xOffset] == smallestDistance:
                validDirections.append(self.stringDirections[index])
        ##checking if a direction was found
        if validDirections:
            chosenDirection = random.choice(validDirections)
            return chosenDirection  
        ##if no flood values, go in a random direction
        while True:
            index = random.randrange(0,len(self.directions))
            xOffset = self.directions[index][0]
            yOffset = self.directions[index][1]
            ##to not collide into walls or other ants
            if self.internalBoard[self.y+yOffset][self.x+xOffset] != "#" and not self.internalBoard[self.y+yOffset][self.x+xOffset].isalpha():
                print(self.stringDirections[index])
                return self.stringDirections[index]


    ##used for testing
    def generateNewCoord(self):
        self.targetCoord = (random.randrange(1,self.max_x-1), random.randrange(1,self.max_y-1))
        self.targets.append(self.targetCoord)

    ##initializes the queue for flood fill
    def initQueue(self):
        self.cellsToCheck = deque(self.targets)
    
    ##sets the current targets
    def initTargets(self):
        self.targets=self.targets
    
    def addWalls(self,count):
        for i in range(count):
            self.internalBoard[random.randrange(1,self.max_y)][random.randrange(1,self.max_x-1)] = "#"
    
    def updateInternalBoard(self,vision):
        for xOffset, yOffset in self.directions:
            ##updating the internal board based on vision
            self.internalBoard[self.y+yOffset][self.x+xOffset] = vision[1+yOffset][1+xOffset]
        self.updateFloodFill()

    ##flood fill
    def updateFloodFill(self):
        self.initTargets()
        self.initQueue()
        self.resetFloodBoard()
        while self.cellsToCheck:
            cell = self.cellsToCheck.popleft()
            Cellx,Celly = cell[0],cell[1]
            for xOffset,yOffset in self.directions:
                xCurrent,yCurrent = Cellx+xOffset,Celly+yOffset
                if self.internalBoard[yCurrent][xCurrent] != "#" and self.floodBoard[yCurrent][xCurrent] == "":
                    self.floodBoard[yCurrent][xCurrent] = self.floodBoard[Celly][Cellx]+1
                    self.cellsToCheck.append((xCurrent,yCurrent))
        self.floodBoard[self.y][self.x] = "A"

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
        self.floodBoard = [["" for i in range(self.max_x)] for j in range(self.max_y)]
        for x,y in self.targets:
            self.floodBoard[y][x]=0

    def resetInternalBoard(self):
        self.internalBoard = [["." if i>0 and i<self.max_x-1 and j>0 and j<self.max_y-1 else "#" for i in range(self.max_x)] for j in range(self.max_y)]