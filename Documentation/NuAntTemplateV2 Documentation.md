# NuAntTemplateV2 Documentation
This is a walkthrough on how to use NuAntTemplate  
This template has pathing already implemented in the self.pathing instance variable  
## How to implement
First, in the `one_step()` method, update the position of the ant in the pathing class by running `updatePosition(x,y)` where `x` is the ant's current x pos and `y` is the ant's current y pos  

After the position is updated, append any coordinates you want the ant to target to the `pathing.targets` variable.  
The coordinates should be in the format of `(x,y)` which is a tuple of length 2 containing 2 integers `x` and `y` (`(0,0)` is in the top left corner)  
  
After adding all the targets, run the `pathing.update()` method which returns a list of length 2`[canSeeDestination,validDirections]`  
`canSeeDestination` is a boolean that states whether the ant can see the target in its vision (so the target is in the 3x3 vision matrix)  
`validDirections` is a list of cardinal directions where the ant can take the shortest path. If `validDirections` is empty, this means there were no targets specified so the pathing class doesn't know where the ant should go towards

##### Example implementation
`def one_step(self, x, y, vision, food):`  
`    pathing.updatePosition(x,y)`  
`    pathing.targets.append((5,5))`  
`    inVision, directions = pathing.update()`  
`    return random.choice(directions)`  
 
Line-by-line walkthrough  
`pathing.updatePosition(x,y)` updates the position in the `pathing` class to the current position  
`pathing.targets.append((5,5))` adds (5,5) as a target the ant should go to  
`inVision, directions = pathing.update()` this assigns `inVision` with `canSeeDirection` which says if the destination is in the ant's vision, and assigns `directions` with `validDirections` which is all the possible cardinal directions the ant can follow to go the fastest path  
`return random.choice(directions)` picks a random direction in the `directions` list and returns it

##### More advanced features
There is also a variable callsed `tempWalls` which is a list of coordinates for places the ant shouldn't go for ONLY this round, so the actual `self.wallBoard` doesn't block it out. This is useful for blocking out other ant's positions so there aren't any conflicting paths, but you don't want to permanently block that ant's position as they could move away from that position later on.  
This variable can be treated the same as `targets` so you would append any coordinates you want to be omitted this round