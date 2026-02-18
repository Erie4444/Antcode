from AntStrategy import AntStrategy
from NuAntPathing import NuAntPathing
from Util import *
'''
Eric Zhao
2/10/2026

'''


class WorkerStrategy(AntStrategy):
    empty = '.'
    wall = '#'
    anthills = "@X"
    def __init__(self, max_x, max_y, anthill):
        super().__init__(max_x, max_y, anthill) # Call constructor in superclass
        self.initLog()
        self.pathing = NuAntPathing(max_y,max_x)
        self.roundCounter = 0
        self.state = "default"
        self.anthillCoord = findAnthillCoord(anthill,max_y,max_x)


    def receive_info(self, messages):
        """Receive messages sent by teammates in the last round."""
        raise NotImplementedError

    def send_info(self):
        """Send messages to teammates at the end of a round."""
        raise NotImplementedError
    
    def one_step(self, x, y, vision, food):
        self.x = x
        self.y = y
        self.food = food
        self.pathing.updatePosition(x,y)
        self.parseVision(vision)
        self.assignTarget()
        self.roundCounter+=1
        self.log()
        return self.step()


    ##algorithms to assign targets
    def seekingAlgorithm(self):
        self.state = "seeking"

    def retreatAlgorithm(self):
        self.state = "retreat"

    def defaultAlgorithm(self):
        self.state = "default"
    
    def stuckAlgorithm(self):
        self.state = "stuck"

    def assignTarget(self):
        if self.food:
            self.retreatAlgorithm()
        else:
            self.seekingAlgorithm()

        if not self.pathing.targets or self.state == "default":
            self.defaultAlgorithm()

    def step(self):
        self.inVision,self.directions,self.isStuck = self.pathing.update()
        if self.isStuck:
            self.stuckAlgorithm()
            self.inVision,self.directions,self.isStuck = self.pathing.update()

    def parseVision(self, vision:list):
        raise NotImplementedError
    
    def log(self):
        raise NotImplementedError
    
    def initLog(self):
        log = open(f"Ant{self.id}Log.txt","w")
        log.write("")
        log.close()
        log = open("AntLog.txt","w")
        log.write("")
        log.close()

    