# Libraries and utility
from tabnanny import check
import numpy as np
import operator as op
import queue

knightMoves = ((2, 1), (1, 2), (-1, 2), (-2, 1),
               (-2, -1), (-1, -2), (1, -2), (2, -1))


def isValidMove(newPos, size):
  return newPos[0] >= 0 and newPos[1] >= 0 and newPos[0] < size and newPos[1] < size


def commandsToString(commands):
  if commands is None:
    return ''
  result = ''
  for commandLine in commands:
    line = ''
    for command in commandLine:
      pos = command[0]
      val = command[1]
      line += f'{pos} {val};'.replace('(', '').replace(')',
                                                       '').replace(', ', ',')
    result += line + '\n'
  return result


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

    self.commands = commands
    if dfsImpl(pos):
      self.board = board
    return numVisits

  def runHeuristic(self):
    # TODO
    return 0

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
# tour = KnightTour(5, (0, 0))
# print('The algorithm visited', tour.runDfs(), 'nodes.')
# tour.print()


# Checkmate functions
class Checkmate:

  def __init__(self, boardSize, initialPosition, enemyPosition, enemyType):
    self.boardSize = boardSize
    self.initialPosition = initialPosition
    self.enemyPosition = enemyPosition
    self.enemyType = enemyType
    self.board = None
    self.commands = None

  def __createBoard(self):
    size = self.boardSize
    enemy = self.enemyType
    enPos = self.enemyPosition

    board = np.zeros(shape=(size, size)).astype(int)

    self.commands.append([])
    # Checkmate positions marked as -3
    for move in knightMoves:
      newPos = tuple(map(op.add, enPos, move))
      if isValidMove(newPos, size):
        board[newPos] = -3
        self.commands[0].append((newPos, -3))

    # Enemy possible positions marked as -1
    possiblePos = []

    def checkMove(move):
      newPos = tuple(map(op.add, enPos, move))
      if isValidMove(newPos, size):
        possiblePos.append(newPos)
        return True
      return False

    if enemy == 'pawn':
      checkMove((1, 0))

    elif enemy == 'king':
      moves = ((1, 0), (0, 1), (1, 1), (-1, 0),
               (-1, 1), (0, -1), (1, -1), (-1, -1))
      for move in moves:
        checkMove(move)

    if enemy == 'rook' or enemy == 'queen':
      for i in range(size):
        possiblePos.append((enPos[0], i))
        possiblePos.append((i, enPos[1]))

    if enemy == 'bishop' or enemy == 'queen':
      partMoves = ((1, 1), (-1, -1), (1, -1), (-1, 1))
      for pm in partMoves:
        for i in range(1, size):
          move = tuple(i * coord for coord in pm)
          if not checkMove(move):
            break

    for pos in possiblePos:
      board[pos] = -1
      self.commands[0].append((pos, -1))

    # Enemy position marked as -2
    board[enPos] = -2
    self.commands[0].append((enPos, -2))

    return board

  def runBfs(self):
    size = self.boardSize
    pos = self.initialPosition
    moves = [*knightMoves]

    self.commands = []

    board = self.__createBoard()
    parent = dict()
    next = queue.Queue()

    numVisits = 0
    found = None

    # Valid position
    if board[pos] == 0:
      board[pos] = 1
      self.commands.append([(pos, 1)])
      numVisits = 1
      parent[pos] = None
      next.put(pos)

    # Win position
    elif board[pos] == -3 or board[pos] == -2:
      board[pos] = 1
      self.commands.append([(pos, 1)])
      numVisits = 1
      parent[pos] = None
      found = pos

    # Algorithm
    while not next.empty():
      current = next.get()

      for move in moves:
        newPos = tuple(map(op.add, current, move))
        if isValidMove(newPos, size):

          if board[newPos] == 0:
            board[newPos] = 1
            self.commands.append([(newPos, 1)])
            numVisits += 1
            parent[newPos] = current
            next.put(newPos)

          elif board[newPos] == -3:
            board[newPos] = 1
            self.commands.append([(newPos, 1)])
            numVisits += 1
            parent[newPos] = current
            found = newPos
            break

      if not found is None:
        break

    if found is None:
      self.board = None
    else:
      # Clearing board and finding path
      self.commands.append([])
      last = len(self.commands) - 1
      for i, row in enumerate(board):
        for j, element in enumerate(row):
          if element == 1 or element == -3:
            board[i][j] = 0
            self.commands[last].append(((i, j), 0))
      path = queue.LifoQueue()
      while not found is None:
        path.put(found)
        found = parent[found]
      level = 0
      while not path.empty():
        level += 1
        posPath = path.get()
        board[posPath] = level
        self.commands.append([(posPath, 1)])
      self.board = board

    return numVisits

  def runAstar(self):
    # TODO
    return 0

  def getCommands(self):
    return self.commands

  def print(self):
    if self.board is None:
      print('No path found.')
      return

    board = self.board
    for row in board:
      for element in row:
        if element == -1:
          element = 'I'
        if element == -2:
          element = 'E'
        print(f'{element:^3}', end=' ')
      print()


# Running checkmate
checkmate = Checkmate(10, (0, 0), (4, 3), 'pawn')
print('The algorithm visited', checkmate.runBfs(), 'nodes.')
checkmate.print()
print(commandsToString(checkmate.getCommands()))
