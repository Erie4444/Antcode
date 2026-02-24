from AntStrategy import AntStrategy
import random

class betterStraightHomeStrat(AntStrategy):
    '''When carrying food, find fastest move to anthill.'''
   
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill)
        self.inbox = []
        self.outbox = []
        self.direction = "WEST"
        if anthill == "@":
            self.anthill_xy = (int((max_x-1)/2), 1)
        else:
            self.anthill_xy = (max_x-(int((max_x-1)/2))-1, max_y-2)
        self.visited = [] # When going to anthill, cells that have already been visited
       
        self.lastx=None
        self.lasty=None

    def receive_info(self, messages): #Ant sends out a message when it sees a wall
        '''
        Receive messages sent by teammates in the last round. Called by game.
        You may add to this method, but do not call it yourself.
        '''
        def recieve_info(self, messages):
            for m in messsages:
                words=m.split()
                if len(words) !=3:
                    print("Message incorrectly formatted: "+ m)
                    continue
                x, y, agent=words
                self.grid[int(x)][int(y)]=agent

    def send_info(self):
        '''
        Send messages. Called by game to get queued messages
        You may add to this method, but do not call it yourself.
        '''
        #return ["ANT1 FOOD"+str(self.food)]
        to_return = self.outbox # lists are a reference type--does this need to be copy()?
        self.outbox = []
        return to_return
   
    def one_step(self, x, y, vision, food):
        '''Calculate and return a randomly chosen, but valid, next move.'''
        # Dictionary of string directions to (x, y) indices in vision
        cardinals = { "NORTH": (1, 0),
                "SOUTH": (1, 2),
                "EAST": (2, 1),
                "WEST": (0, 1),
                "NORTHEAST": (2, 0),
                "SOUTHEAST": (2, 2),
                "SOUTHWEST": (0, 2),
                "NORTHWEST": (0, 0),
                "HERE": (1,1) }
               
        directionList=["GO"+ " " +"EAST", "GO"+ " " +"WEST", "GO"+ " " +"NORTH", "GO"+ " " +"SOUTH",  "GO"+ " " +"NORTHEAST", "GO"+ " " +"SOUTHEAST", "GO"+ " " +"SOUTHWEST", "GO"+ " " +"NORTHWEST"]
        #Code to avoid repeating collision
        if self.lastx==None:
            self.lastx=x
       
        if self.lasty==None:
            self.lasty=y
           
        if self.lastx==x and self.lasty==y:
            self.lastx=x
            self.lasty=y
            move= random.choice(["NORTH", "NORTHEAST", "EAST", "SOUTHEAST", "SOUTH", "SOUTHWEST", "WEST", "NORTHWEST"])
       
           
        self.lastx=x
        self.lasty=y
           
        # Move towards anthill with food, GET if find food while not carrying
        min_distance = 100000000000
        move = (x, y, "HERE")
        for direction, coords in cardinals.items():
            for agent in vision[coords[0]][coords[1]]:
                if food:
                    if agent == self.anthill:
                        self.visited = []
                        return "DROP " + direction
                    else:
                        new_x = x + coords[0] - 1
                        new_y = y + coords[1] - 1
                        if agent != "#" and (new_x, new_y) not in self.visited:
                            distance = abs(new_x - self.anthill_xy[0]) + abs(new_y - self.anthill_xy[1])
                            if distance < min_distance:
                                min_distance = distance
                                move = (new_x, new_y, direction)
                if not food and agent.isdigit():
                    return "GET " + direction

        if food:
            self.visited.append((move[0], move[1]))
            return move[2]

        # Otherwise move randomly
        while True:
            move = random.choice(["NORTH", "NORTHEAST", "EAST", "SOUTHEAST", "SOUTH", "SOUTHWEST", "WEST", "NORTHWEST"])
            coords = cardinals[move]
            if "#" not in vision[coords[0]][coords[1]]:
                return move