# Libraries and utility

knightMoves = ((2, 1), (1, 2), (-1, 2), (-2, 1),
               (-2, -1), (-1, -2), (1, -2), (2, -1))


def isValidMove(newPos, size):
  return newPos[0] >= 0 and newPos[1] >= 0 and newPos[0] < size and newPos[1] < size


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
