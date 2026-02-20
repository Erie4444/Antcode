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
        self.pathing = NuAntPathing(max_y,max_x)
        self.anthillCoord = findAnthillCoord(anthill, max_y, max_x)
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
        self.pathing.updatePosition(self.x, self.y)

        if not food:
            for i in range(3):
                for j in range(3):
                    if vision[i][j] and vision[i][j].isdigit():
                        self.pathing.clearTargets()
                        self.pathing.targets.append((self.x + i - 1, self.y + j - 1))
        elif food:
            self.pathing.clearTargets()
            self.pathing.targets.append(self.anthillCoord)
        
        if not self.pathing.targets:
            self.pathing.clearTargets()
            self.pathing.targets.append((self.max_x-2, self.max_y-2))

        print(self.pathing.targets)
        inVision, directions, isStuck = self.pathing.update()
        if inVision:
            if food:
                self.pathing.clearTargets()
                return "DROP "+random.choice(directions)
            else:
                return "GET "+random.choice(directions)
        else:
            return random.choice(directions)