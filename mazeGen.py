from random import randint 
#TODO fix long backtracking queue
#TODO remove methods that are only used once or twice

isEmpty = (lambda n: True if  n==None or n > -10 else False)

Step = 0

class mazeGenError(Exception):
    pass
class mazeClass():
    def __init__(self,dimensiony,dimensionx, maze = None,StoreHistory = False):
        self.start = None
        self.stop = None
        self.maze = [] #values below -9 are walls, if value is between -2 and -9 its not suitable for wall creation
        self.backTrack = []
        self.createHistory = []
        self.solveHistory = []
        if maze == None:
            self.genself(dimensiony,dimensionx)
        elif len(maze) == dimensiony and len(maze[0]) == dimensionx:
            self.maze = maze.copy

        self.step = 0
        self.maze = self.maze

    def createCorner(self,old,curr,next):
        a = (curr[0] - old[0],curr[1] - old[1])  #set old and next in relation to current
        b = (curr[0] - next[0],curr[1] - next[1])
        d = {
                ((0,-1),(1,0)):(-1,1),
                ((-1,0),(0,-1)):(1,1),
                ((0,1),(-1,0)):(1,-1),
                ((1,0),(0,1)):(-1,-1)}
        if (a,b) in d.keys():
            self.maze[curr[0] - d[(a,b)][0]][curr[1] - d[(a,b)][1]] = -2
            return
        elif (b,a) in d.keys():
            self.maze[curr[0] - d[(b,a)][0]][curr[1] - d[(b,a)][1]] = -2
            return
        else:
            return


    def getFreeNeighbours(self,pos):
        y,x = pos
        ls = []
        if y > 0 and (self.maze[y-1][x] == 0 or self.maze[y-1][x]==-1): ls.append((y-1,x))
        if y < len(self.maze)-1 and (self.maze[y+1][x]==0 or self.maze[y+1][x]==-1): ls.append((y+1,x))
        if x > 0 and (self.maze[y][x-1] == 0 or self.maze[y][x-1] ==-1):ls.append((y,x-1))
        if x < len(self.maze[y])-1 and (self.maze[y][x+1] ==0 or self.maze[y][x+1] == -1): ls.append((y,x+1))
        
        return ls
    def inBounds(self,p): #checks if position p= (y,x) is inside of maze
        a,b = p
        if len(self.maze) <= a or a < 0: return False
        if len(self.maze[a]) <= b or b < 0: return False
        return True
     
    def getNeighbourValues(self,pos):
        y,x = pos
        diagonalsH = [x for x in [(y+1,x+1),(y-1,x+1),(y-1,x-1),(y+1,x-1)]]
        directH = [x for x in [(y+1,x),(y,x+1),(y-1,x),(y,x-1)]]
        #removing inaccessible elements
        directH = list(filter(self.inBounds,directH))
        diagonalsH = list(filter(self.inBounds,diagonalsH))
        return diagonalsH,directH

    def lower(self,pos,fac=1):
        y,x = pos
        if self.maze[y][x] > -10: self.maze[y][x] += (-1)*(fac)

    def accessible(self,a):
        if a == None: return False
        if not self.inBounds(a): return False

        (y,x) = a
        return (self.maze[y][x] > -2)
    def createWallAndLog(self, pos):
        y,x = pos
        self.maze[y][x] = -10
        self.createHistory.append([pos])

    def getVal(self,pos):
        return self.maze[pos[0]][pos[1]]

    def genRecursively(self,curr,path = None,debug = False): #needs to be refactored
        cy,cx = curr
        old = (None,None)
        if not self.accessible(curr):
            return

        self.createWallAndLog(curr)

        diagonalN, directN = self.getNeighbourValues(curr)
        for el in directN:
            if self.getVal(el) < -9: old = el
            else: self.lower(el)

        next = None
        while not(self.accessible(next)) and len(directN) != 0:
            next = (directN.pop(randint(0,len(directN)-1)))

        if not(self.accessible(next)):
            for element in diagonalN:
                self.lower(element)
            return

        #checking if corner needs to be created
        oldy,oldx = old
        curry,currx = curr
        nexty,nextx = next
        if not (oldy == nexty or oldx == nextx): #not straight, need to gen edge
            self.createCorner(old,curr,next)

        self.genRecursively(next,debug = debug)

        # backtracking
        for element in directN:
            self.backTrack.append(element)
            #self.backTrack = [element] + self.backTrack 
               
    def getWallPositions(self):
        #return list of positions where walls are
        output = []
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] < -9 : output.append((y,x))

        return output

    def genself(self,height,width,debug = False):
        self.maze = [[0 for i in range(width)] for j in range(height)]
        #gen Border:
        startx = randint(1,width-2)
        stopx = randint(1,width-2)
        self.createHistory = [[]]


        for j in range(len(self.maze[0])):
            #walls: 
            if j != startx: 
                self.createHistory[0].append((0,j))
                self.maze[0][j] = -10
                
            if j != stopx: 
                self.maze[-1][j] = -10
                self.createHistory[0].append((len(self.maze)-1,j))
            #inaccessible spots surrounding walls:
            self.maze[1][j] = -1
            self.maze[-2][j] = -1

        for i in range(len(self.maze)):
            #walls: 
            self.maze[i][0] = -10
            self.createHistory[0].append((i,0))

            self.maze[i][-1] = -10
            self.createHistory[0].append((i,len(self.maze)-1))
            #inaccessible spots surrounding walls:
            self.maze[i][1] = -1
            self.maze[i][-2] = -1

        self.maze[0][1] = -10
        self.maze[-1][1] = -10
        self.maze[0][-2] = -10
        self.maze[-1][-2] = -10


        self.start = (0,startx)
        self.stop = (len(self.maze)-1,stopx)

        #init gen starting points:
        genStart = []
        for j in range(2,len(self.maze)-2):
            genStart.append((j,0))
            genStart.append((j,len(self.maze)-1))
            
        for j in range(2,len(self.maze[0])-2):
            if j != startx: 
                genStart.append((0,j))
            if j != stopx:
                genStart.append((len(self.maze)-1,j))


        #making corners and start/stoppoints inaccessible
        self.maze[1][1] = -2
        self.maze[-2][1] = -2
        self.maze[1][-2] = -2
        self.maze[-2][-2] = -2
        self.maze[0][startx] = -2
        self.maze[1][startx] = -2
        self.maze[-1][stopx] = -2
        self.maze[-2][stopx] = -2



        startFromBorderAmount = int(((height + width) * 2) // 32)
        if startFromBorderAmount < 6: startFromBorderAmount = 6
        #startFromBorderAmount = 5
        i = 0
        while i < startFromBorderAmount and genStart:
            start = None
            while not start and genStart:
                start = genStart.pop(randint(0,len(genStart)-1))
                start = self.getFreeNeighbours(start)
            if start: 
                self.genRecursively(start[0],debug=debug)
            i += 1

        print(f"\n\nstarting backtracking\nwith lenght of backtracking queue: {len(self.backTrack)}\n")
        while self.backTrack:
            x = self.backTrack.pop(-1)
            if x:
                self.genRecursively(x)
        

    def mazeToString(self,debug = False):
        conv = (lambda x:"##" if x < -9 else "  ")
        output = ""
        if debug:
            conv = (lambda x:"VV" if x == None else ( "##" if x < -9 else ("  " if x == 0 else ("()" if x == -1 else "[]"))))
            output += """
            0------------------------------0
            | v     |  displayed as:       |
            |------------------------------|
            | v > 0    | \"##\"              |
            | v = 0    | \"  \" (nothing)    |
            | v =-1    | \"()\"              |
            | v <-1    | \"[]\"              |
            | v = None | \"VV\" (debug)      |
            0------------------------------0
            \n"""
        
        for row in self.maze:
            for entry in row:
                output += conv(entry)
            output += "\n"
        return output[:-1]
    def __repr__(self):
        return self.mazeToString(True)


if __name__ == "__main__":
    X = mazeClass(61,61)
    print(X)
    print("printing")
    print(X.mazeToString())
    print(X.createHistory)
