from random import randint 

isEmpty = (lambda n: True if  n==None or n <= 0 else False)

Step = 0

class mazeGenError(Exception):
    pass
class mazeClass():
    def __init__(self,dimensiony,dimensionx, maze = None,StoreHistory = False):
        #throw self.mazeGenerationException
        self.maze = []
        self.backTrack = []
        if maze == None:
            self.genself(dimensiony,dimensionx)
        elif len(maze) == dimensiony and len(maze[0]) == dimensionx:
            self.maze = maze.copy

        self.step = 0
        self.maze = self.maze
        self.createHistory = []
        self.solveHistory = []
    def genmaze(self):
        pass

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

    def neighbourIsBorder(self,y,x):
        if not isEmpty(self.maze[y][x]):
            return False
        if y > 0 and not isEmpty(self.maze[y-1][x]): return True #y-1|x
        if y < len(self.maze)-1 and not isEmpty(self.maze[y+1][x]): return True #y+1|x
        if x > 0 and not isEmpty(self.maze[y][x-1]): return True #y|x-1
        if x < len(self.maze[y])-1 and not isEmpty(self.maze[y][x+1]): return True #y|x+1

        return False

    def getFreeNeighbours(self,pos):
        y,x = pos
        ls = []
        if y > 0 and (self.maze[y-1][x] == 0 or self.maze[y-1][x]==-1): ls.append((y-1,x))
        if y < len(self.maze)-1 and (self.maze[y+1][x]==0 or self.maze[y+1][x]==-1): ls.append((y+1,x))
        if x > 0 and (self.maze[y][x-1] == 0 or self.maze[y][x-1] ==-1):ls.append((y,x-1))
        if x < len(self.maze[y])-1 and (self.maze[y][x+1] ==0 or self.maze[y][x+1] == -1): ls.append((y,x+1))
        
        return ls
     
    def getNeighbourValues(self,pos):
        def inBounds(p):
            print(p)
            a,b = p
            if len(self.maze) >= a or a < 0: return False
            if len(self.maze[a]) >= b or b < 0: return False
            return True


        y,x = pos
        directH = [x for x in [(y+1,x),(y,x+1),(y-1,x),(y,x-1)]]
        #directH = list(filter(inBounds,directH))
        diagonalsH = [x for x in [(y+1,x+1),(y-1,x+1),(y-1,x-1),(y+1,x-1)]]
        #directH = list(filter(inBounds,directH))
        direct = [((a,b),self.maze[a][b]) for (a,b) in directH]
        diagonals = [((a,b),self.maze[a][b]) for (a,b) in diagonalsH]

        return diagonals,direct

    def lower(self,pos,fac=1):
        y,x = pos
        if self.maze[y][x] <= 0: self.maze[y][x] += (-1)*(fac)

    def accessible(self,a):
        if a == None: return False
        #print(f"a mit typ:\t{type(a)}")
        #print(f"a mit inhalt:\t{a}")
        (y,x) = a
        return (self.maze[y][x] == 0 or self.maze[y][x] == -1)
        #= (lambda a: True if self.maze[a[0]][a[1]] == 0 or self.maze[a[0]][a[1]] == -1 else False)



    def genRecursively(self,curr,path = None,debug = False): #needs to be refactored
        #print(f"gen\t {debug}")
        debugOutput = ""
        cy,cx = curr
        old = (None,None)
        if not self.accessible(curr):
            return

        self.maze[cy][cx] = 5
        if debug: 
            global Step
            debugOutput += (f"\nstep{Step}\n"+ self.mazeToString(debug))
            Step += 1
        diagonalN, directN = self.getNeighbourValues(curr)
        for el in directN:
            if el[1] >0: old = el[0]
            else: self.lower(el[0])

        i = 1     #to replace while
        if i == 1: #to replace while
            i = 0#to replace while
            next = None
            while not(self.accessible(next)) and len(directN) != 0:
                next = (directN.pop(randint(0,len(directN)-1)))[0]

            if not(self.accessible(next)):
                #print(f"new end at {curr}")
                for element in diagonalN:
                    self.lower(element[0])
                #print("final state:")
                #print(self.mazeToString(True))
                return

            oldy,oldx = old
            curry,currx = curr
            nexty,nextx = next
            #if oldy == curry == nexty or oldx == currx == nextx : #straight
            if not (oldy == nexty or oldx == nextx) : #not straight, need to gen edge
                self.createCorner(old,curr,next)
                if debug:
                    #debugOutput += f"\n-----creating border in next step------\nold : {old}\tcurr: {curr}\tnext:{next}\n\t\tedge:{border}"
                    debugOutput += f"\n\n"
                    print(debugOutput)

            self.genRecursively(next,debug = debug)

            # backtracking
            self.genRecursively(curr,debug = debug)
            diagonalN, directN = self.getNeighbourValues(curr)
            #self.backTrack = []
            for element in directN:
                self.backTrack.append(element[0])
                #self.genRecursively(element[0])
                

    def genself(self,height,width,debug = False):
        
        self.maze = [[0 for i in range(width)] for j in range(height)]
        #gen Border:
        for j in range(len(self.maze[0])):
            self.maze[0][j] = 1
            self.maze[-1][j] = 1
        for i in range(len(self.maze)):
            self.maze[i][0] = 1
            self.maze[i][-1] = 1

        #pick starting point
        startx = randint(1,width-2)
        stopx = randint(1,width-2)

        #dont delete yet
        """
        self.maze[0][startx] = -2
        self.maze[1][startx] = -2
        self.maze[-1][stopx] = -2
        self.maze[-2][stopx] = -2
        startPoint = (0,startx)
        stopPoint = (len(self.maze)-1,startx)
        """

        #init gen starting points:
        genStart = []
        for j in range(2,len(self.maze)-2):
            genStart.append((j,0))
            genStart.append((j,len(self.maze)-1))
            
        for j in range(2,len(self.maze[0])-2):
            if j != startx: genStart.append((0,j))
            if j != stopx: genStart.append((len(self.maze)-1,j))
        """
        for (y,x) in genStart:
            self.maze[y][x] = 2
        """

        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.neighbourIsBorder(y,x): self.maze[y][x] = -1
        self.maze[1][1] = -2
        self.maze[-2][1] = -2
        self.maze[1][-2] = -2
        self.maze[-2][-2] = -2
        
        startFromBorderAmount = ((height + width) * 2) // 5
        i = 0
        while i < startFromBorderAmount and genStart:
            start = None
            while not start and genStart:
                start = genStart.pop(randint(0,len(genStart)-1))
                start = self.getFreeNeighbours(start)
            if start: self.genRecursively(start[0],debug=debug)
            i += 1
        print(f"\n\nstarting backtracking\nwith lenght of backtracking queue: {len(self.backTrack)}\n{self.backTrack}\n")
        """
        while self.backTrack:
            x = self.backTrack.pop(0)
            print(x)
            if x:
                neighbours = self.getFreeNeighbours(x)
                for start in neighbours:
                    print(start)
                    self.genRecursively(start)
        """
        while self.backTrack:
            x = self.backTrack.pop(0)
            if x:
                self.genRecursively(x)
        #self.genRecursively((3,1),debug=debug)

        freePoints = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] <= 0:
                    self.maze[i][j] = 0
                    freePoints.append((i,j))
                else:
                    self.maze[i][j] = 255

        start = freePoints.pop(randint(0,len(freePoints)-1))
        stop = freePoints.pop(randint(0,len(freePoints)-1))
        

    def mazeToString(self,debug = False):

        output = ""
        #print(f"toString\t{self.maze}")
        conv = (lambda x: "  " if isEmpty(x) else "##") 
        #if debug: conv = (lambda x: "  " if isEmpty(x) else str(x) + " " ) 
        if debug:
            #conv = (lambda x:". " if x == -1 else str(x)+" ")
            #conv = (lambda x:" "+str(x) if x >= 0 else str(x))
            conv = (lambda x:"VV" if x == None else ( "##" if x > 0 else ("  " if x == 0 else ("()" if x == -1 else "[]"))))
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
    X = mazeClass(31,31)
    print(X)