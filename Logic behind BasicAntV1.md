# Logic behind BasicAntV1.py
by Eric Zhao
## Navigation
 - uses floodfill algorithm
 - goes in a random direction if it doesn't find any food
 - if it does find a food, it will use the floodfill board to find the shortest path

internal board - a internal representation of the actual board  
flood board - a 2d array with the distance values in every cell. 0 means food as the distance from it to food is 0 distance  

## FLOODFILL ALGORITHM
The floodfill algorithm is a reliable way to deduce the shortest path.  
It works by first providing it the target coordinates, then it fills in all the other cells 
with the distance from it to the target coordinates.  
The ant can go the shortest path by just finding the smallest value in its vision which means that cell is the closest to the target.  
This algorithm also updates based on what the ant sees. If you add walls or it sees new foods, it updates them in the internal board and the flood board.  

ex.  
before flood fill (0 is the food)  
. . . . .  
. . # # .  
. . . # .  
. 0 . . .  
. . . . .  

first iteration of flood fill  
. . . . .  
. . # # .  
1 1 1 # .  
1 0 1 . .  
1 1 1 . .  

2nd iteration  
. . . . .  
2 2 # # .  
1 1 1 # .  
1 0 1 2 .  
1 1 1 2 .  

3rd iteration  
3 3 3 . .  
2 2 # # .  
1 1 1 # 3  
1 0 1 2 3  
1 1 1 2 3  

4th iteration  
3 3 3 4 .  
2 2 # # 4  
1 1 1 # 3  
1 0 1 2 3  
1 1 1 2 3  

RESULT  
3 3 3 4 5  
2 2 # # 4  
1 1 1 # 3  
1 0 1 2 3  
1 1 1 2 3  

so even if the ant starts anywhere, if it follows the smallest numbers, it will go down the shortest path

Veritasium has a great explation of this 
https://youtu.be/ZMQbHMgK2rw?si=mEJO8ORqdlvtDCAz&t=366

