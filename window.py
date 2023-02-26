import pyglet
import time
import mazeGen


def addToBatchFromLog(log,step,batch,topLeft,pixelSize):
    outputSquares = []
    if step >= len(log):
        return []
    for position in log[step]:
        x = topLeft[1]+(position[1]*pixelSize)
        y = topLeft[0]-((position[0]+1)*pixelSize)
        outputSquares.append(pyglet.shapes.Rectangle( x = x,  y = y
                                                    ,width = pixelSize, height = pixelSize
                                                    ,color = (1,1,1),batch = batch))
    return outputSquares

def createBatchFromMaze(maze,mazeSquareCoordinates,pixelSize,mazeSquareHeight,startCol = 1):
    output = pyglet.graphics.Batch()
    mazeArr = [[0 for i in range(len(maze[0]))]for j in range(len(maze))]
    for i in range(len(mazeArr)):
        for j in range(len(mazeArr[i])):
            mazeArr[i][j] = pyglet.shapes.Rectangle( x = mazeSquareCoordinates[1]+(j*pixelSize),  y = mazeSquareCoordinates[0]+mazeSquareHeight-((i+1)*pixelSize)
                                                    ,width = pixelSize, height = pixelSize
                                                    ,color = (77,77,startCol+j*1+i*1),batch = output)
    return output,mazeArr

def createWindow(mazeObj,height = None, width = None, pixelSize = 20, xBorder=100,yBorder = 100):
    maze = mazeObj.maze
    if pixelSize %2 != 0:
        pixelSize += 1

    if height == None:
        numPixelsY = len(maze)
    else:
        numPixelsY = height
    if width == None:
        numPixelsX = len(maze[0])
    else:
        numPixelsX = width

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
    counter =0
    arr = []
    def update(dt):
        #dt: delta parameter necessary for schedule function
        nonlocal counter
        nonlocal mazeBatch
        nonlocal arr
        log = mazeObj.createHistory
        #log = [[(1,1)],[(2,2)],[(3,3)]]
        print(f"{counter} {time.time()}")
        arr += addToBatchFromLog(log,counter,mazeBatch,mazeTopLeftCorner,pixelSize)
        counter += 1

    pyglet.clock.schedule_interval(update,0.1)
    

    @window.event
    def on_draw():
        bgBatch.draw() #drawing Background
        mazeBatch.draw() #drawing maze

    pyglet.app.run()


maze = mazeGen.mazeClass(31,31)
print(maze)
#createWindow(maze)
createWindow(maze)
