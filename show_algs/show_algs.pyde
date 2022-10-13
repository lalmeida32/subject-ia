
boardSize = 0
canvaSize = 600
updateEvery = 5
fps = 60
commands = []
currentCommand = 1
lastPos = None
skipConst = None
finished = False

def printBoard():
    global boardSize, canvaSize, skipConst
    background(209, 168, 56)
    stroke(110, 84, 15)
    strokeWeight(2)
    skipConst = canvaSize / boardSize
    for i in range(1, boardSize):
        skip = skipConst * i
        line(0, skip, canvaSize, skip)
        line(skip, 0, skip, canvaSize)

def runNextCommand():
    global commands, boardSize, canvaSize, currentCommand, lastPos, updateEvery
    if currentCommand >= len(commands)-1:
        finished = True
        return
    
    if not lastPos is None:
        fill(71, 71, 63)
        square(skipConst * lastPos[0], skipConst * lastPos[1], skipConst)
    lastPos = None
    
    cs = commands[currentCommand].split(';')
    for c in cs:
        if c == '':
            continue
        if c == 'slow':
            updateEvery = fps
            continue
        (pos, val) = c.split(' ')
        val = int(val)
        pos = pos.split(',')
        pos = (int(pos[1]), int(pos[0]))
        if val == 1:
            fill(235, 122, 30)
            square(skipConst * pos[0], skipConst * pos[1], skipConst)
            lastPos = pos
        elif val == 0:
            fill(209, 168, 56)
            square(skipConst * pos[0], skipConst * pos[1], skipConst)
        elif val == -1:
            fill(71, 71, 63)
            square(skipConst * pos[0], skipConst * pos[1], skipConst)
        elif val == -2:    
            fill(207, 41, 35)
            square(skipConst * pos[0], skipConst * pos[1], skipConst)
        elif val == -3:
            fill(159, 240, 89)
            square(skipConst * pos[0], skipConst * pos[1], skipConst)
    
    currentCommand += 1

def setup():
    global canvaSize, boardSize, fps, commands
    size(canvaSize, canvaSize)
    frameRate(fps)
    commands = loadStrings("result.out")
    boardSize = int(commands[0])
    printBoard()

def draw():
    global updateEvery
    if (frameCount % updateEvery == 0 and not finished):
        runNextCommand()
    
    
