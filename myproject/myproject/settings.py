# screen settings
from pygame.math import Vector2 as vec
WIDTH, HEIGHT = 1150, 650
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER
size = (WIDTH, HEIGHT)
FPS = 30

#color settings
BLACK = (0,0,0)
RED = (208, 22, 22)
GREY = (107,107,107)
WHITE = (255,255,255)
PACMAN_COLOUR = (190,194,15)
WALL_COLOUR = (112,55,163)
COINS_COLOUR = (167,179,34)
#pacman settings
def get_pix_pos(position):
    cell_width = MAZE_WIDTH//28
    cell_height = MAZE_HEIGHT//30
    return vec(position.x*cell_width+cell_width//2,
                position.y*cell_height+cell_height//2)
PACMAN_START_POS = vec(1,1)
PACMAN_END_POS = vec(9,17)
#font settings

START_TEXT_SIZE = 20
START_FONT = ' arial black'

# mob settings
