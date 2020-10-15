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

class Tetris(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, col, row, shape):
        self.x = col
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def createGrid(staticPositions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in staticPositions:
                c = staticPositions[(j,i)]
                grid[i][j] = c
    return grid
