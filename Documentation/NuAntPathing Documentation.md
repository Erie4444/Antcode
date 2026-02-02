# NuAntPathing Documentation
This explains each method in the NuAntPathing class  

### initializing the class
Inputs: rows, cols, x, y, targets  
rows - integer: the amount of rows in the board  
cols - integer: the amount of columns in the board  
x - integer: the x position of the ant  
y - integer: the y position of the ant  
targets - list: a list of coordinates that the pathing should target  
Outputs: None  
Just initializes the boards & instance variables  
### initQueue
Inputs: None  
Outputs:  None  
This method initializes the queue used for floodfill and marks the targets in `self.floodBoard`  
### resetFloodBoard
Inputs: None  
Outputs: None  
This just clears the `self.floodBoard` variable as a new empty 2d matrix size `self.rows` by `self.cols`  
### resetWallBoard
Inputs: None  
Outputs: None  
This just clears the `self.wallBoard` variable as a new empty 2d matrix size `self.rows` by `self.cols`  
### addWall
Inputs: x, y  
x - integer: the x position of the wall  
y - integer: the y position of the wall  
Outputs: None  
This adds a wall at (x,y) in `self.wallBoard`  
### getPrettyFloodBoard
Inputs: None  
Outputs: string - a formatted version of the `self.floodBoard` matrix for easier visualization  
### updateFloodBoard
Inputs: None  
Outputs: None  
Updates the floodboard values based on `self.targets`  
### updatePosition
Inputs: x, y  
x - integer: the x position of the ant  
y - integer: the y position of the ant  
Ouputs: None  
Just updates `self.x` and `self.y` with x and y respectively  
### generateValidDirections
Input: None  
Outputs: list - a list of length 2, 1st item is if the ant can see the destination, the 2nd item is a list of cardinal directions the ant should travel  
Calculates and outputs a list of options of cardinal directions the ant can travel for the fastest path to the destination. If the and can see the destination, then it also returns `True` as the first term in the list  
### update
Inputs: None  
Outputs: list - a list of length 2, 1st item is if the ant can see the destination, the 2nd item is a list of cardinal directions the ant should travel  
Just a quality of life method that combines the execution of `self.updateFloodBoard()` and `self.generateValidDirections()` into one method. Returns the output of `generateValidDirections()` 