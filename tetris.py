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


class Tetris(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, col, row, shape):
        self.x = col
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
