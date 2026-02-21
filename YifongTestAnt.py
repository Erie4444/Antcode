import random
from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
from Util import *
'''
Yifong Liao
2/10/2026
'''



class YifongTestAnt(AntStrategy):
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) #call constructor in superclass
        # NuAntPathing expects rows (max_y) then columns (max_x)
        self.pathing = NuAntPathing(max_y, max_x)
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
        # Update pathing internal position to track movement and stuck status
        self.pathing.updatePosition(x, y)
        
        # Scan vision to update the pathfinder's knowledge of walls
        for i in range(3):
            for j in range(3):
                # vision[i][j] is a list or string; check if wall character is present
                if '#' in vision[i][j]:
                    self.pathing.addWall(x + (i - 1), y + (j - 1))

        for i in range(3):
            for j in range(3):
                cell_content = vision[i][j]
          
                direction = NuAntPathing.offsetToDirections.get((i - 1, j - 1))
                
              
                if not food and any(char.isdigit() for char in cell_content):
                    return "GET " + direction
                
               
                if food and self.anthill in cell_content:
                    return "DROP " + direction

       
        if food and self.anthillCoord:
            self.pathing.targets = [self.anthillCoord]
            
            can_see, valid_dirs, stuck = self.pathing.update()
            if valid_dirs:
                return random.choice(valid_dirs)

        
        cardinals = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return NuAntPathing.offsetToDirections[random.choice(cardinals)]
    #67th line code 
