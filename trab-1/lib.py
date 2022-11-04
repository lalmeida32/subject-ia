# Libraries and utility

knightMoves = ((2, 1), (1, 2), (-1, 2), (-2, 1),
               (-2, -1), (-1, -2), (1, -2), (2, -1))


def isValidMove(newPos, size):
  return newPos[0] >= 0 and newPos[1] >= 0 and newPos[0] < size and newPos[1] < size

def heuristicaNextMoveTour(pos, sizeOfBoard, visited):
  minVal=9
  minMove=()
  for i in range(8):
    next=(pos[0]+knightMoves[i][0], pos[1]+knightMoves[i][1])
    if(next[0]>=0 and next[0]<sizeOfBoard and next[1]>=0 and next[1]<sizeOfBoard and visited[next]==0):
      numberOfNextMoves=0
      for j in range(8):
        next2=(next[0]+knightMoves[j][0], next[1]+knightMoves[j][1])
        if(next2[0]>=0 and next2[0]<sizeOfBoard and next2[1]>=0 and next2[1]<sizeOfBoard and visited[next2]==0):
          numberOfNextMoves+=1
      if(numberOfNextMoves<minVal):
        minVal=numberOfNextMoves
        minMove=next
  return minMove

def commandsToString(commands, boardSize):
  if commands is None:
    return ''
  result = f'{boardSize}\n'
  for commandLine in commands:
    line = ''
    for command in commandLine:
      if command == 'slow':
        line += 'slow;'
        continue
      pos = command[0]
      val = command[1]
      line += f'{pos} {val};'.replace('(', '').replace(')',
                                                       '').replace(', ', ',')
    result += line + '\n'
  return result
