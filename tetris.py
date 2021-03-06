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
screen_Shape_Format = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]


Z_Shape_Format = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I_Shape_Format = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O_Shape_Format = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J_Shape_Format = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L_Shape_Format = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T_Shape_Format = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [screen_Shape_Format, Z_Shape_Format, I_Shape_Format, O_Shape_Format, J_Shape_Format, L_Shape_Format, T_Shape_Format]
shapeColors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
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
            if col == '0':
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

def drawTextMiddle(text, size, color, surface):
    font = pygame.font.SysFont('arial', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + game_width/2 - (label.get_width() / 2), top_left_y + game_height/2 - label.get_height()/2))

def drawGrid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (1,128,128), (sx, sy+ i*30), (sx + game_width, sy + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (255,255,255), (sx + j * 30, sy), (sx + j * 30, sy + game_height))

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

def drawNextShape(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next', 1, (255,255,255))

    sx = top_left_x + game_width + 50
    sy = top_left_y + game_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))
def drawWindow(surface):
    surface.fill((0,0,0))
    font = pygame.font.SysFont('arial', 60)
    label = font.render('TETRIS', 1, (255,255,255))

    surface.blit(label, (top_left_x + game_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    drawGrid(surface, 20, 10)
    pygame.draw.rect(surface, (0, 0, 230), (top_left_x, top_left_y, game_width, game_height), 5)

def main():
    global grid

    blockPositions = {}
    grid = createGrid(blockPositions)

    change_piece = False
    run = True
    current_piece = getShape()
    next_piece = getShape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27

        grid = createGrid(blockPositions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Piece falling logic
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (validSpace(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.disgame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not validSpace(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not validSpace(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not validSpace(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not validSpace(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convertShapeFormat(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                blockPositions[p] = current_piece.color
            current_piece = next_piece
            next_piece = getShape()
            change_piece = False

            # call four times to check for multiple clear rows
            clearRows(grid, blockPositions)

        drawWindow(win)
        drawNextShape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if checkLost(blockPositions):
            run = False

    drawTextMiddle("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def mainMenu():
    run = True
    while run:
        win.fill((0,0,0))
        drawTextMiddle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

mainMenu()  # start
