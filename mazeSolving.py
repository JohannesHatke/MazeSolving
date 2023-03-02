from threading import currentThread
import mazeGen
# all solving algorithms should return list of searched of positions and then path
# TODO increase performance 

def getNextTrace(mazeObj: mazeGen.mazeClass,pos: tuple):
    #breakpoint()
    y,x = pos
    currVal = mazeObj.getVal(pos)
    n = [(y,x+1),(y+1,x),(y,x-1),(y-1,x)]
    n = list(filter(mazeObj.inBounds,n))
    ls = []

    minPos = None
    minVal = None
    for position in n:
        posVal = mazeObj.getVal(position)
        if posVal >0 and  posVal < currVal:
            if minVal == None or posVal < minVal:
                minVal = posVal
                minPos = position

    return minPos


    


def traceBag(mazeObj: mazeGen.mazeClass) -> list:
    curr = mazeObj.stop
    output = [curr]

    while (curr != mazeObj.start):
        #breakpoint()
        curr = getNextTrace(mazeObj,curr)
        output.append(curr)
        print(f"trying to unpack\t{curr}")
        y,x = curr
        mazeObj.maze[y][x] += 3

    return output
        

def visitedOrAccessible(mazeObj: mazeGen.mazeClass, pos: tuple, step: int = 0) -> bool:
    #breakpoint()
    if not mazeObj.inBounds(pos):
        return False

    if (val:= mazeObj.getVal(pos)) <= -10: return False
    if val < step and val > 0: return False
    return True
    
def getNextNeighbours(mazeObj: mazeGen.mazeClass,pos: tuple, step: int = 0):
    #breakpoint()
    y,x = pos
    n = [(y,x+1),(y+1,x),(y,x-1),(y-1,x)]
    n = list(filter(mazeObj.inBounds,n))
    output = []
    for position in n:
        if visitedOrAccessible(mazeObj,position,step): output.append(position)

    return output
        

def breadthFirstSearch(mazeObj):
    start = mazeObj.start
    stop = mazeObj.stop
    step = 1
    visited = [[start]]
    C = [start]
    N = []

    print(start)
    #breakpoint()
    finished = False
    while C and not finished:
        for currPos in C:
            if currPos == stop: finished = True
            N += getNextNeighbours(mazeObj,currPos,step)
            y,x = currPos
            mazeObj.maze[y][x] = step

        visited.append(N)
        C = N.copy()
        N = []
        step += 1

    return visited,traceBag(mazeObj)


if __name__ == "__main__":
    X = mazeGen.mazeClass(31,31)
    print(X)
    print("\n\n\n")
    print(breadthFirstSearch(X))
