def transpose(matrix: list):
    return [[matrix[x][y]for x in range(len(matrix))]for y in range(len(matrix))]

def findAnthillCoord(anthill: str,rows: int, cols: int):
    if anthill == "@":
        return (int((cols-1)/2), 1)
    else:
        return (rows-(int((cols-1)/2))-1, rows-2)