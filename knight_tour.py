
from lib import knightMoves, isValidMove, commandsToString
import numpy as np
import operator as op


# Knight Tour functions
class KnightTour:

  def __init__(self, boardSize, initialPosition):
    self.boardSize = boardSize
    self.initialPosition = initialPosition
    self.board = None
    self.commands = None

  def runDfs(self):
    size = self.boardSize
    pos = self.initialPosition

    board = np.zeros(shape=(size, size)).astype(int)
    numVisits = 0
    numBlocked = 0

    # The reversed list is faster for board size 7
    moves = [*knightMoves]
    moves.reverse()

    commands = []

    def dfsImpl(current):
      nonlocal numVisits, board, size, numBlocked, moves, commands

      numVisits += 1
      numBlocked += 1
      board[current] = numBlocked
      commands.append([(current, 1)])

      if (numBlocked == size ** 2):
        return True

      next = []
      for move in moves:
        newPos = tuple(map(op.add, current, move))
        if isValidMove(newPos, size) and board[newPos] == 0:
          next.append(newPos)

      for newPos in next:
        foundPath = dfsImpl(newPos)
        if foundPath:
          return True

      board[current] = 0
      numBlocked -= 1
      commands.append([(current, 0)])
      return False

    if dfsImpl(pos):
      self.board = board
      commands.append(['slow'])
      commands.append([])
      last = len(commands) - 1
      path = [0 for _ in range(size**2)]
      for i, row in enumerate(board):
        for j, _ in enumerate(row):
          path[board[i][j] - 1] = (i, j)
          commands[last].append(((i, j), 0))
      for coord in path:
        commands.append([(coord, 1)])

    self.commands = commands
    return numVisits

  def runHeuristic(self):
    pos=self.initialPosition
    sizeOfBoard=self.boardSize
    numVisits=1

    board = np.zeros(shape=(sizeOfBoard, sizeOfBoard)).astype(int)
    board[pos]=numVisits
    commands = []
    commands.append([(pos, 1)])
    for i in range(sizeOfBoard*sizeOfBoard-1):
      numVisits+=1
      pos=heuristicaNextMoveTour(pos, sizeOfBoard, board)
      board[pos]=numVisits
      commands.append([(pos, 1)])
    self.commands = commands
    self.board = board
    return numVisits

  def getCommands(self):
    return self.commands

  def print(self):
    if self.board is None:
      print('No path found.')
      return

    board = self.board
    for row in board:
      for element in row:
        print(f'{element:^3}', end=' ')
      print()


# Running knight tour
tour = KnightTour(7, (0, 0))
# print('The algorithm visited', tour.runDfs(), 'nodes.')
# tour.print()
tour.runDfs()
print(commandsToString(tour.getCommands(), tour.boardSize))

tour.runHeuristic()
print(commandsToString(tour.getCommands(), tour.boardSize))
