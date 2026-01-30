# NuAntTemplate.py Documentation
### This program is a basic ant that uses the flood fill algorithm (more in the Logic behind BasicAntV1) in order to navigate the board
Currently, the ant automatically updates the internal board with what it sees and will go towards specified target coordinates


### How to implement
In order for the ant to target something, update the `self.targets` variable with a list of coordinates (formatted as a 2-long tuple (x,y))

##### Example:
Lets say you want the ant to target coordinates (5,5) and (3,7).
before `self.updateInternalBoard(actualVision)` on line 44, add these tuples to the `self.targets` list.  
So you could do  
`self.targets.append((5,5))`  
`self.targets.append((3,7))`  
If you run `self.printTargets()`, it should print out `[(5,5),(3,7)]`

