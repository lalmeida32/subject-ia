# Libraries and utility
import numpy as np
import operator as op
import queue

knightMoves = ((2, -1), (1, -2), (-1, -2), (-2, -1),
               (-2, 1), (-1, 2), (1, 2), (2, 1))


# Knight Tour functions
class KnightTour:

  def __init__(self, boardSize, initialPosition):
    self.boardSize = boardSize
    self.initialPosition = initialPosition
    self.result = None

  def runDfs(self):
    size = self.boardSize
    pos = self.initialPosition

    board = np.zeros(shape=(size, size)).astype(int)
    numVisits = 0
    count = 0

    def dfsImpl(current):
      nonlocal numVisits, board, size, count

      numVisits += 1
      count += 1
      board[current] = count

      if (count == size ** 2):
        return [current]

      next = []
      for move in knightMoves:
        newPos = tuple(map(op.add, current, move))
        valid = newPos[0] >= 0 and newPos[1] >= 0
        valid = valid and newPos[0] < size and newPos[1] < size
        valid = valid and board[newPos] == 0
        if (valid):
          next.append(newPos)

      for newPos in next:
        path = dfsImpl(newPos)
        if not path is None:
          return [current, *path]

      board[current] = 0
      count -= 1
      return None

    self.result = dfsImpl(pos)
    return numVisits

  def print(self):
    size = self.boardSize
    board = np.zeros(shape=(size, size)).astype(int)
    if not self.result is None:
      for i, pos in enumerate(self.result):
        board[pos] = i + 1

    for row in board:
      for element in row:
        print(f'{element:^3}', end=' ')
      print()


# Running knight tour
tour = KnightTour(7, (0, 0))
print('The algorithm visited', tour.runDfs(), 'nodes.')
tour.print()
