import pygame
import random


pygame.font.init()

screen_width = 800
screen_height = 700
game_width = 300
game_height = 600
block_size = 30

top_left_x = (screen_width - game_width) // 2
top_left_y = screen_height - game_height

#Creating Shape Formats To Convert

S_Shape_Format = [[\'.....\',
      \'.....\',
      \'..00.\',
      \'.00..\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..00.\',
      \'...0.\',
      \'.....\']]

Z_Shape_Format = [[\'.....\',
      \'.....\',
      \'.00..\',
      \'..00.\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'.00..\',
      \'.0...\',
      \'.....\']]

I_Shape_Format = [[\'..0..\',
      \'..0..\',
      \'..0..\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'0000.\',
      \'.....\',
      \'.....\',
      \'.....\']]

O_Shape_Format = [[\'.....\',
      \'.....\',
      \'.00..\',
      \'.00..\',
      \'.....\']]

J_Shape_Format = [[\'.....\',
      \'.0...\',
      \'.000.\',
      \'.....\',
      \'.....\'],
     [\'.....\',
      \'..00.\',
      \'..0..\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'.....\',
      \'.000.\',
      \'...0.\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..0..\',
      \'.00..\',
      \'.....\']]

L_Shape_Format = [[\'.....\',
      \'...0.\',
      \'.000.\',
      \'.....\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..0..\',
      \'..00.\',
      \'.....\'],
     [\'.....\',
      \'.....\',
      \'.000.\',
      \'.0...\',
      \'.....\'],
     [\'.....\',
      \'.00..\',
      \'..0..\',
      \'..0..\',
      \'.....\']]

T_Shape_Format = [[\'.....\',
      \'..0..\',
      \'.000.\',
      \'.....\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'..00.\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'.....\',
      \'.000.\',
      \'..0..\',
      \'.....\'],
     [\'.....\',
      \'..0..\',
      \'.00..\',
      \'..0..\',
      \'.....\']]

shapes = [S_Shape_Format, Z_Shape_Format, I_Shape_Format, O_Shape_Format, J_Shape_Format, L_Shape_Format, T_Shape_Format]
shapeColors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Tetris(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shapeColors[shapes.index(shape)]
        self.rotation = 0


def createGrid(staticPositions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in staticPositions:
                c = staticPositions[(j,i)]
                grid[i][j] = c
    return grid

def convertShapeFormat(shape):
    blockPositions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == \'0\':
                blockPositions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(blockPositions):
        blockPositions[i] = (pos[0] - 2, pos[1] - 4)

    return blockPositions

def validSpace(shape, grid):
    acceptedPositions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    acceptedPositions = [j for sub in acceptedPositions for j in sub]
    formatted = convertShapeFormat(shape)

    for pos in formatted:
        if pos not in acceptedPositions:
            if pos[1] > -1:
                return False

    return True
def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def getShape():
    global shapes, shapeColors

    return Piece(5, 0, random.choice(shapes))

def drawGrid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + game_width, sy + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + game_height))

def clearRows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
