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

    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        pass

    def send_info(self):
        return []
    

    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        self.pathing.updatePosition(x,y)
        # make random coordinates to head towards if not holding food and no food in vision
        # Choose a random target within interior map borders (avoid wall edges)
        if self.max_x > 2:
            random_x = random.randint(1, self.max_x - 2)
        else:
            random_x = 0
        if self.max_y > 2:
            random_y = random.randint(1, self.max_y - 2)
        else:
            random_y = 0
        
        #pick up visible food if not currently carrying
        if not food:
            found_food = next(((vx, vy) for vx, row in enumerate(vision) for vy, item in enumerate(row) if item and item.isdigit() and int(item) > 0), None)
            if found_food:
                dx, dy = found_food[0] - 1, found_food[1] - 1
                direction = NuAntPathing.offsetToDirections.get((dx, dy), "HERE")
                return "GET " + direction

        if food:
            #if holding food and anthill in vision, drop food in anthill
            found_hill = next(((vx, vy) for vx, row in enumerate(vision) for vy, item in enumerate(row) if item == self.anthill), None)
            if found_hill:
                dx, dy = found_hill[0] - 1, found_hill[1] - 1
                direction = NuAntPathing.offsetToDirections.get((dx, dy), "HERE")
                return "DROP " + direction
            #otherwise head for anthill
            self.pathing.clearTargets()
            self.pathing.targets.append(self.anthillCoord)
        else:
            self.pathing.clearTargets()
            self.pathing.targets.append((random_x, random_y))

        inVision, directions = self.pathing.update()
        if directions:
            return random.choice(directions)
        return "HERE"