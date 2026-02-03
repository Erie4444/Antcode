'''
Eric Zhao
2/1/2026
Standalone pathing algorithm for ants
Just instantiate this in your ant, add any coordinates into self.targets, update the internal pos with updatePosition(x,y)
then run update() to get possible directions

this returns a list with 2 items
Item 1. type: boolean
Just says if the destination is within the vision of the ant

Item 2. type: list
Contains all possible cardinal directions
'''
from collections import deque
class NuAntPathing():
    empty = ''
    wall = '#'
    maxInternalBoardItemLength = 1
    maxFloodBoardItemLength = 2
    offsetToDirections = {(-1,-1):"NORTHWEST",(-1,0):"WEST",(-1,1):"SOUTHWEST",(0,-1):"NORTH",(0,1):"SOUTH",(1,-1):"NORTHEAST",(1,0):"EAST",(1,1):"SOUTHEAST"}
    def __init__(self,rows: int,cols: int):
        self.targets = []
        self.rows = rows
        self.cols = cols
        self.tempWalls = []
        self.resetFloodBoard()
        self.resetWallBoard()

    def initQueue(self):
        ##setting up the queue and marking the targets on the floodboard
        self.floodQueue = deque(self.targets)
        for target in self.targets:
            self.floodBoard[target[1]][target[0]] = 0

    def resetFloodBoard(self):
        self.floodBoard = [[self.empty for x in range(self.cols)] for y in range(self.rows)]

    def resetWallBoard(self):
        self.wallBoard = [[self.empty if 0<x and x<self.cols-1 and 0<y and y<self.rows-1 else self.wall for x in range(self.cols)] for y in range(self.rows)]

    def clearTargets(self):
        self.targets = []

    def addWall(self,x: int,y: int):
        self.wallBoard[y][x] = self.wall

    def getPrettyFloodBoard(self):
        return "\n".join([" ".join([" "*(self.maxFloodBoardItemLength-len(str(item)))+str(item) for item in row]) for row in self.floodBoard])

    def __repr__(self):
        return self.getPrettyFloodBoard()

    ##does the flood fill algo and updated floodBoard
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
            if self.floodBoard[self.y+yOffset][self.x+xOffset] != self.empty and not (self.x+xOffset,self.y+yOffset) in self.tempWalls:
                if self.floodBoard[self.y+yOffset][self.x+xOffset] < smallestDistance:
                    smallestDistance = self.floodBoard[self.y+yOffset][self.x+xOffset]
                    validDirections = [direction]
                elif self.floodBoard[self.y+yOffset][self.x+xOffset] == smallestDistance:
                    validDirections.append(direction)
        if smallestDistance == 0:
            canSeeDestination = True
        return (canSeeDestination,validDirections)

    def update(self):
        self.updateFloodBoard()
        directions = self.generateValidDirections()
        self.tempWalls=[]
        return directions