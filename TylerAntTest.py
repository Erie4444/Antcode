import random
from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
from Util import *
'''
Tyler Hwang
2/3/2026
Using NuAntTemplateV2.py as a base for my ant strategy'''


class TylerAnt(AntStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) #call constructor in superclass
        self.pathing = NuAntPathing(max_x,max_y)
        self.anthillCoord = findAnthillCoord(anthill, max_x, max_y)
        self.x = 0
        self.y = 0
        self.id = 0
        self.foods = []
        self.walls = []
        self.target = ()
        self.removed = []

    def receive_info(self, messages):
        self.foods,self.walls,self.target = parseMessages(messages,self.id,self.foods,self.walls,self.target)

    def send_info(self):
        return sendMessage(self.id,self.foods,self.walls,self.target,self.removed)

    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        cardinals = [(0, -1), (1, 0), (0, 1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
        self.pathing.clearTargets()
        

        if (self.x, self.y) == self.anthillCoord:
            if food:
                return "DROP HERE"
            return NuAntPathing.offsetToDirections[random.choice(cardinals)]
        self.pathing.update()
        if not food:
            for i in range(3):
                for j in range(3):
                    if vision[i][j] and vision[i][j].isdigit():
                        return "GET " + NuAntPathing.offsetToDirections[(i - 1, j - 1)]
            return NuAntPathing.offsetToDirections[random.choice(cardinals)]

        for i in range(3):
            for j in range(3):
                if vision[i][j] == self.anthill:
                    return "DROP " + NuAntPathing.offsetToDirections[(i - 1, j - 1)]

        offset = (
            0 if self.anthillCoord[0] == self.x else (1 if self.anthillCoord[0] > self.x else -1),
            0 if self.anthillCoord[1] == self.y else (1 if self.anthillCoord[1] > self.y else -1)
        )
        return NuAntPathing.offsetToDirections[offset]