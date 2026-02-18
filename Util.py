def transpose(matrix: list):
    return [[matrix[x][y]for x in range(len(matrix))]for y in range(len(matrix))]

def findAnthillCoord(anthill: str,rows: int, cols: int):
    if anthill == "@":
        return (int((cols-1)/2), 1)
    else:
        return (cols-(int((cols-1)/2))-1, rows-2)

def parseMessages(messages,id,foodCoords,wallCoords,target,):
    blackListedCoords = []
    removedCoords = []

    ##going through all the messages
    for message in messages:
        if message["ID"] != id: #not your own message
            ##adding all the foodCoords and wallCoords to internal lists (sets ensure there are no repeats)
            foodCoords = list(set(foodCoords+message["FOOD"]))
            wallCoords = list(set(wallCoords+message["WALLS"]))

            ##make sure to blacklist the coordinates other ants are targetting
            if message["TARGET"]:
                blackListedCoords.append(message["TARGET"])

            ##removing coodinates the other ants have removed (took the last food in the pile)
            for coord in message["REMOVED"]:
                if coord in foodCoords:
                    removedCoords.append(message["REMOVED"])
    
    ##remove blacklisted and removed coords from the internal foodCoords variable
    for coord in blackListedCoords:
        if coord in foodCoords:
            foodCoords.remove(coord)
        if coord == target:
            target = ()
    for coord in removedCoords:
        if coord in foodCoords:
            foodCoords.remove(coord)
        if coord == target:
            target = ()
    return [foodCoords,wallCoords,target]

def sendMessage(id,foodCoords,wallCoords,target,removedCoords):
    return [{"ID":id,"FOOD":foodCoords,"WALLS":wallCoords,"TARGET":target,"REMOVED":removedCoords}]
