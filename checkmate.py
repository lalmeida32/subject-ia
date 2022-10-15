from lib import knightMoves, isValidMove, commandsToString
import numpy as np
import operator as op
import queue
import heapq


def canMove(pos, enemy, enemyPos, sizeOfBoard):
  if (pos == enemyPos):
    return True
  if (pos[0] < 0 or pos[0] >= sizeOfBoard or pos[1] < 0 or pos[1] >= sizeOfBoard):
    return False
  if (enemy == 'pawn' and (pos == [enemyPos[0] - 1, enemyPos[1] - 1] or pos == [enemyPos[0] - 1, enemyPos[1] + 1])):
    return False
  if (enemy == 'bishop' and abs(pos[0] - enemyPos[0]) == abs(pos[1] - enemyPos[1])):
    return False
  if (enemy == 'rook' and (pos[0] == enemyPos[0] or pos[1] == enemyPos[1])):
    return False
  if (enemy == 'queen' and (pos[0] == enemyPos[0] or pos[1] == enemyPos[1] or abs(pos[0] - enemyPos[0]) == abs(pos[1] - enemyPos[1]))):
    return False
  if (enemy == 'king' and abs(enemyPos[0] - pos[0]) <= 1 and abs(enemyPos[1] - pos[1]) <= 1):
    return False

  return True


class Node():
  """A node class for A* Pathfinding"""

  def __init__(self, parent=None, position=None):
    self.parent = parent
    self.position = position

    self.g = 0
    self.h = 0
    self.f = 0

  def __eq__(self, other):
    return self.position == other.position

  def __repr__(self):
    return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

  # defining less than for purposes of heap queue
  def __lt__(self, other):
    return self.f < other.f

  # defining greater than for purposes of heap queue
  def __gt__(self, other):
    return self.f > other.f


def heuristica(pos, goal):
  dist = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

  return dist / 3


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
    pos = self.initialPosition
    enemy = self.enemyType
    enemyPos = self.enemyPosition
    size = self.boardSize

    self.commands = []

    numVisits = 0
    found = None
    # Valid position
    board = self.__createBoard()
    if board[pos] == 0:
      board[pos] = 1
      numVisits = 1

    # Win position
    elif board[pos] == -3 or board[pos] == -2:
      board[pos] = 1
      numVisits = 1
      found = pos
    else:
      print('Invalid starting position, knight is being attacked')
      return

    start_node = Node(None, pos)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, enemyPos)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    while len(open_list) > 0:
      numVisits += 1

      cur = heapq.heappop(open_list)
      self.commands.append([(cur.position, 1)])
      closed_list.append(cur)

      if cur == end_node:
        path = []
        current = cur
        while current is not None:
          path.append(current.position)
          current = current.parent
        for i, row in enumerate(board):
          for j, element in enumerate(row):
            if element == 1 or element == -3:
              board[i][j] = 0

        level = 0
        path = path[::-1]
        for i in path:
          level += 1
          board[i] = level
        board[enemyPos] = -2
        self.board = board
        return numVisits  # Return reversed path

      # Generate children
      children = []

      for new_position in knightMoves:  # Adjacent squares

          # Get node position
        nextPos = (cur.position[0] + new_position[0],
                   cur.position[1] + new_position[1])

        # Make sure within range
        if isValidMove(nextPos, size) and canMove(nextPos, enemy, enemyPos, size):
            # Create new node
          new_node = Node(cur, nextPos)
          # Append
          children.append(new_node)

      # Loop through children
      for child in children:
        # Child is on the closed list
        if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
          continue

        # Create the f, g, and h values
        child.g = cur.g + 1
        child.h = heuristica([child.position[0], child.position[1]], enemyPos)
        child.f = child.g + child.h

        # Child is already in the open list
        if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
          continue

        # Add the child to the open list
        heapq.heappush(open_list, child)

    return None

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

# print('The algorithm visited', checkmate.runBfs(), 'nodes.')
# print('The algorithm visited', checkmate.runAstar(), 'nodes.')
# checkmate.print()

checkmate.runBfs()
# checkmate.runAstar()
print(commandsToString(checkmate.getCommands(), checkmate.boardSize))
