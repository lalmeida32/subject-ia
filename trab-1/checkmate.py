from math import sqrt
from lib import knightMoves, isValidMove, commandsToString
import numpy as np
import operator as op
import queue


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
      checkMove((1, 1))
      checkMove((1, -1))

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
      self.commands.append([(current, 1)])

      for move in moves:
        newPos = tuple(map(op.add, current, move))
        if isValidMove(newPos, size):

          if board[newPos] == 0:
            board[newPos] = 1
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
    size = self.boardSize
    pos = self.initialPosition
    moves = [*knightMoves]
    goal = self.enemyPosition

    self.commands = []

    board = self.__createBoard()
    parent = dict()
    cost = dict()
    next = queue.PriorityQueue()

    numVisits = 0
    found = None

    def heuristica(pos):
      nonlocal goal
      return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    # Valid position
    if board[pos] == 0:
      board[pos] = 1
      self.commands.append([(pos, 1)])
      numVisits = 1
      parent[pos] = None
      cost[pos] = 0
      next.put((heuristica(pos), pos))

    # Win position
    elif board[pos] == -3 or board[pos] == -2:
      board[pos] = 1
      self.commands.append([(pos, 1)])
      numVisits = 1
      parent[pos] = None
      cost[pos] = 0
      found = pos

    # Algorithm
    while not next.empty():
      _, current = next.get()
      self.commands.append([(current, 1)])

      for move in moves:
        newPos = tuple(map(op.add, current, move))
        if isValidMove(newPos, size):

          if board[newPos] == 0:
            board[newPos] = 1
            numVisits += 1
            parent[newPos] = current
            cost[newPos] = cost[current] + 3
            next.put((cost[newPos] + heuristica(newPos), newPos))

          elif board[newPos] == -3:
            board[newPos] = 1
            self.commands.append([(newPos, 1)])
            numVisits += 1
            parent[newPos] = current
            cost[newPos] = cost[current] + 3
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
checkmate = Checkmate(30, (0, 0), (25, 28), 'queen')

print('The algorithm visited', checkmate.runBfs(), 'nodes.')
# print('The algorithm visited', checkmate.runAstar(), 'nodes.')
checkmate.print()

# checkmate.runBfs()
# checkmate.runAstar()
# print(commandsToString(checkmate.getCommands(), checkmate.boardSize))
