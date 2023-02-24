import pyglet
counter = 1

def createBatch(maze,mazeSquareCoordinates,pixelSize,mazeSquareHeight,startCol = 1):
    output = pyglet.graphics.Batch()
    mazeArr = [[0 for i in range(len(maze[0]))]for j in range(len(maze))]
    for i in range(len(mazeArr)):
        for j in range(len(mazeArr[i])):
            mazeArr[i][j] = pyglet.shapes.Rectangle( x = mazeSquareCoordinates[1]+(j*pixelSize),  y = mazeSquareCoordinates[0]+mazeSquareHeight-((i+1)*pixelSize),width = pixelSize, height = pixelSize ,color = (77,77,counter+j*1+i*1),batch = output)
    return output,mazeArr

def createWindow(maze, height = None, width = None, pixelSize = 20,xBorder=100,yBorder = 100): #height and width refer to amount of squares in each maze

    # making sure paramers wont cause issues
    if pixelSize %2 != 0:
        pixelSize += 1
    if type(maze) != type([]) or type(maze[0]) != type([]):
        raise Exception
    
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
    borderWidth = 10

    mazeArr = [[0 for i in range(len(maze[0]))]for j in range(len(maze))]

    for i in range(len(mazeArr)):
        for j in range(len(mazeArr[i])):
            mazeArr[i][j] = pyglet.shapes.Rectangle( x = mazeSquareCoordinates[1]+(j*pixelSize),  y = mazeSquareCoordinates[0]+mazeSquareHeight-((i+1)*pixelSize),width = pixelSize, height = pixelSize ,color = (77,77,77+j*1+i*1),batch = mazeBatch)

        """
        color = {
                }
        """ #dict to assign different color values to walls and free spaces or paths

#declaring groups:
#background = pyglet.graphics.Group(0)


#label = pyglet.text.Label("Whoa",font_name="Times New Roman",font_size = 36, x = window.width // 2,  y = window.height // 2, anchor_x="center",anchor_y="center",color = (1,1,1,1))
#square = pyglet.shapes.Rectangle( x = window.width // 2,  y = window.height // 2,width = 100, height = 100 ,color = ( 158,206,106))

    backGroundSquare = pyglet.shapes.Rectangle( x = 0,  y = 0,width = window.width, height = window.height ,color = ( 255,255,255),batch = bgBatch)
    mazeOutlineSquare = pyglet.shapes.Rectangle( x = ((window.width+borderWidth) // 2 )- ((mazeSquareWidth+borderWidth) // 2)-(borderWidth // 2),  y = (window.height // 2)- (mazeSquareHeight // 2)-(borderWidth // 2),width = mazeSquareWidth+borderWidth, height = mazeSquareHeight+borderWidth ,color = ( 1,1,1),batch = bgBatch)

    mazeSquare = pyglet.shapes.Rectangle( x = mazeSquareCoordinates[1],y = mazeSquareCoordinates[0],
                                         width = mazeSquareWidth, height = mazeSquareHeight ,
                                         color = ( 255,255,255),batch = bgBatch)
    
    mazeBatch,arr = createBatch(maze,mazeSquareCoordinates,pixelSize,mazeSquareHeight)
#createMazeGraphics()
    def update(dt):
        global counter
        nonlocal mazeBatch
        nonlocal arr
        print("a")
        mazeBatch,arr = createBatch(maze,mazeSquareCoordinates,pixelSize,mazeSquareHeight,counter)
        counter += 1
    #dt: delta necessary
    pyglet.clock.schedule_interval(update,0.1)
    

    #mazeBatch.unset_state() #drawing maze
    @window.event
    def on_draw():
        bgBatch.draw() #drawing Background
        mazeBatch.draw() #drawing maze

    pyglet.app.run()

maze = [[0 for i in range(60)] for j in range(40)]
#createWindow(maze,height = 20, width = 20)
createWindow(maze)
