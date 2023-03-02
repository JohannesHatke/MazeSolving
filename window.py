import pyglet
import time

from pyglet.graphics import Batch
import mazeGen
import mazeSolving

def addToBatchFromLog(log: list,step: int,batch: Batch,topLeft: tuple ,pixelSize: int, color = (1,1,1), colorProgress = False):
    outputSquares = []
    if colorProgress:
        r,b,g = color
        color = (r+1*step,b+1*step,g+1*step)

    if step >= len(log):
        return False,[]

    for position in log[step]:
        x = topLeft[1]+(position[1]*pixelSize)
        y = topLeft[0]-((position[0]+1)*pixelSize)
        outputSquares.append(pyglet.shapes.Rectangle( x = x,  y = y
                                                    ,width = pixelSize, height = pixelSize
                                                    ,color = color,batch = batch))
    return True,outputSquares

def singleWindow(mazeObj: mazeGen.mazeClass,solvingAlgorithm,pixelSize,speed):
    xBorder = 100
    yBorder = 100
    
    maze = mazeObj.maze 
    if pixelSize %2 != 0:
        pixelSize += 1

    numPixelsY = len(maze)
    numPixelsX = len(maze[0])
    solveLog,path = solvingAlgorithm(mazeObj)


    window = pyglet.window.Window((2*xBorder + numPixelsX * pixelSize),(2*yBorder + numPixelsY * pixelSize))
    bgBatch = pyglet.graphics.Batch()
    mazeSquareWidth = numPixelsX * pixelSize
    mazeSquareHeight =numPixelsY * pixelSize

    mazeBatch = pyglet.graphics.Batch()
    mazeSquareCoordinates = ((window.height // 2)- (mazeSquareHeight // 2),(window.width // 2 )- (mazeSquareWidth // 2))
    mazeTopLeftCorner = (mazeSquareCoordinates[0] + mazeSquareHeight,mazeSquareCoordinates[1])
    borderWidth = 10

    backGroundSquare = pyglet.shapes.Rectangle( x = 0,  y = 0,width = window.width, height = window.height ,
                                               color = ( 255,255,255),batch = bgBatch)
    mazeOutlineSquare = pyglet.shapes.Rectangle( x = ((window.width+borderWidth) // 2 )- ((mazeSquareWidth+borderWidth) // 2)-(borderWidth // 2),
                                                y = (window.height // 2)- (mazeSquareHeight // 2)-(borderWidth // 2)
                                                ,width = mazeSquareWidth+borderWidth, height = mazeSquareHeight+borderWidth ,
                                                color = ( 1,1,1),batch = bgBatch)

    mazeSquare = pyglet.shapes.Rectangle( x = mazeSquareCoordinates[1],y = mazeSquareCoordinates[0],
                                         width = mazeSquareWidth, height = mazeSquareHeight ,
                                         color = ( 255,255,255),batch = bgBatch)

    
    solveBatch = pyglet.graphics.Batch()
    storageArr = [] #needed to keep squares of maze in scope
    createLog = mazeObj.createHistory
    #createLog = mazeSolving.breadthFirstSearch(mazeObj)
    phases = [createLog, solveLog,[path] ]
    phaseColors = [(1,1,1), (33,17,76),(204,16,16) ]
    phaseProgression = [False, True,False]
    phaseBatches = [mazeBatch,solveBatch,solveBatch]

    
    phaseCount = 0
    updateNecessary = True
    phaseStep = 0
    updateInterval = 0.1 # TODO make speed necessary


    def update(dt):
        nonlocal storageArr
        nonlocal phaseCount
        nonlocal phases
        nonlocal updateNecessary
        nonlocal phaseStep
        nonlocal phaseBatches
        #dt: delta parameter necessary for schedule function
        #log = [[(1,1)],[(2,2)],[(3,3)]]
        phaseRunning,output = addToBatchFromLog(phases[phaseCount],phaseStep,phaseBatches[phaseCount],mazeTopLeftCorner,pixelSize, color =  phaseColors[phaseCount], colorProgress=phaseProgression[phaseCount])
        if not phaseRunning:
            #breakpoint()
            phaseCount += 1
            phaseStep = -1
            if phaseCount >= len(phases):
                updateNecessary = False


            
        storageArr += output
        #if not didAnything: currPhase =( currPhase +1) % len(phases)
        #print(f"{counter}\t {time.time()}\t{phaseRunning}\t{currPhase}")
        phaseStep += 1

    pyglet.clock.schedule_interval(update,updateInterval)
    

    @window.event
    def on_draw():
        if not updateNecessary: pyglet.clock.unschedule(update)
        bgBatch.draw() #drawing Background
        mazeBatch.draw() #drawing maze
        solveBatch.draw() #drawing maze

    pyglet.app.run()


def comparisonWindow():
    pass

def launchWindow(typ :str, mazeObj: mazeGen.mazeClass, solvingAlgorithm , pixelSize: int, speed: int):
    d = {"single":singleWindow,"comparison": comparisonWindow} # type of window
    # single is one maze
    # comparison are multiple
    if typ not in d.keys():
        return None # error
    
    d[typ](mazeObj, solvingAlgorithm, pixelSize, speed)
    
   
    


def createBatchFromMaze(maze,mazeSquareCoordinates,pixelSize,mazeSquareHeight,startCol = 1):
    output = pyglet.graphics.Batch()
    mazeArr = [[0 for i in range(len(maze[0]))]for j in range(len(maze))]
    for i in range(len(mazeArr)):
        for j in range(len(mazeArr[i])):
            mazeArr[i][j] = pyglet.shapes.Rectangle( x = mazeSquareCoordinates[1]+(j*pixelSize),
                                                    y = mazeSquareCoordinates[0]+mazeSquareHeight-((i+1)*pixelSize)
                                                    ,width = pixelSize, height = pixelSize
                                                    ,color = (77,77,startCol+j*1+i*1),batch = output)
    return output,mazeArr


maze = mazeGen.mazeClass(61,61)
print(maze)
#createWindow(maze)
#createWindow(maze)
def testFunc(a):
    return [[]]
#createWindow(maze,pixelSize=10)

#def launchWindow(typ :str, mazeObj: mazeGen.mazeClass, solvingAlgorithm: function, pixelSize: int, speed: int):
launchWindow("single",maze, mazeSolving.breadthFirstSearch,10,0)
