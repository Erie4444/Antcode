from collections import deque
class NuAntPathing():
    empty = ''
    wall = '#'
    maxInternalBoardItemLength = 1
    maxFloodBoardItemLength = 2
    offsetToDirections = {(-1,-1):"NORTHWEST",(-1,0):"WEST",(-1,1):"SOUTHWEST",(0,-1):"NORTH",(0,1):"SOUTH",(1,-1):"NORTHEAST",(1,0):"EAST",(1,1):"SOUTHEAST"}
    directionsToOffset = {"NORTHWEST":(-1,-1),"WEST":(-1,0),"SOUTHWEST":(-1,1),"NORTH":(0,-1),"SOUTH":(0,1),"NORTHEAST":(1,-1),"EAST":(1,0),"SOUTHEAST":(1,1)}
    def __init__(self,rows: int,cols: int,x: int, y: int,targets: list = []):
        self.targets = targets
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y
        self.resetFloodBoard()
        self.resetWallBoard()

    def initQueue(self):
        self.floodQueue = deque(self.targets)
        for target in self.targets:
            self.floodBoard[target[1]][target[0]] = 0

    def resetFloodBoard(self):
        self.floodBoard = [[self.empty for x in range(self.cols)] for y in range(self.rows)]

    def resetWallBoard(self):
        self.wallBoard = [[self.empty if 0<x and x<self.cols-1 and 0<y and y<self.rows-1 else self.wall for x in range(self.cols)] for y in range(self.rows)]

    def addWall(self,x: int,y: int):
        self.wallBoard[y][x] = self.wall

    def getPrettyFloodBoard(self):
         return "\n".join([" ".join([" "*(self.maxFloodBoardItemLength-len(str(item)))+str(item) for item in row]) for row in self.floodBoard])

    def __repr__(self):
        return self.getPrettyFloodBoard()

    def updateFloodBoard(self):
        self.resetFloodBoard()
        self.initQueue()
        while self.floodQueue:
            cell = self.floodQueue.popleft()
            Cellx,Celly = cell[0],cell[1]
            for xOffset,yOffset in self.offsetToDirections.keys():
                xCurrent,yCurrent = Cellx+xOffset,Celly+yOffset
                if self.wallBoard[yCurrent][xCurrent] != self.wall and self.floodBoard[yCurrent][xCurrent] == self.empty:
                    self.floodBoard[yCurrent][xCurrent] = self.floodBoard[Celly][Cellx]+1
                    self.floodQueue.append((xCurrent,yCurrent))
    
    def updatePosition(self,x: int,y: int):
        self.x = x
        self.y = y

    ##returns a list [bool, list]
    ##1st item is if the destination is within the ant's vision
    ##2nd item is the direction(s) that the ant should go (returns empty if it didn't detect anything)
    def generateValidDirections(self):
        validDirections = []
        smallestDistance = 9999
        canSeeDestination = False
        for offset,direction in self.offsetToDirections.items():
            xOffset,yOffset = offset
            if self.floodBoard[self.y+yOffset][self.x+xOffset] != self.empty:
                if self.floodBoard[self.y+yOffset][self.x+xOffset] < smallestDistance:
                    smallestDistance = self.floodBoard[self.y+yOffset][self.x+xOffset]
                    validDirections = [direction]
                elif self.floodBoard[self.y+yOffset][self.x+xOffset] == smallestDistance:
                    validDirections.append(direction)
        if smallestDistance == 0:
            canSeeDestination = True
        return (canSeeDestination,validDirections)