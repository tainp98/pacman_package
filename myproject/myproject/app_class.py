import pygame, sys, random, os
from .settings import *
import numpy as np
from .pacman_class import Pacman
pygame.init()
vec = pygame.math.Vector2
from .astar import *
# config path for background
dir_list = []
current_path = os.path.dirname(__file__)
print("current_path",current_path)
# print("sys_path",sys.path)
# current_path_list = current_path.split('/')
# for indx in range(len(current_path_list)):
#     if current_path_list[indx] == 'env' or current_path_list[indx] == '.local':
#         dir_list = current_path_list[1:indx] + [current_path_list[-1]] + ['myproject']
#         break
# path = '/'
# for a in dir_list:
#     path += a
#     path += '/'
# path_list = list(path)
# path_list.pop(-1)
# path = "".join(path_list)
path = os.path.join(current_path, 'background.png')

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//55
        self.cell_height = MAZE_HEIGHT//30
        self.wall = []
        self.empty_coins = []
        self.coins = []
        self.astar = []
        self.pacman = Pacman(self, vec(1,1))
        self.fini = False
        self.stop = False
        self.load()
          
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
                
                
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
####### HELPER FUNCTION
    def draw_text(self, words, screen, pos, size, colour,font_name, centered=False):
        font = pygame.font.SysFont(font_name,size)
        text = font.render(words,False,colour)
        text_size = text.get_size()
        if centered == True:
            pos[0] = pos[0] - text_size[0]//2 
            pos[1] = pos[1] - text_size[1]//2 
        screen.blit(text,pos)

    def load(self):
        self.background = pygame.image.load(path)
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH,MAZE_HEIGHT))
        # opening wall.txt
        #creating wall list with coordinate of wall
        # with open("wall.txt","r") as file:
        #     for yidx,line in enumerate(file):
        #         for xinx, char in enumerate(line):
        #             if char == "1":
        #                 self.wall.append(vec(xinx, yidx))
        #             if char == "0":
        #                 self.empty_coins.append(vec(xinx, yidx))
        self.random_wall(17,10)
        
        # self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),5)]
        # print(self.coins)
        # self.astar = astar(PACMAN_START_POS, self.coins[0], self.wall)

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),(x*self.cell_width, HEIGHT))
        for y in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, y*self.cell_height),(WIDTH, y*self.cell_height))
        # draw wall
        for wall in self.wall:
            pygame.draw.rect(self.background, WALL_COLOUR, 
                        (wall.x*self.cell_width,wall.y*self.cell_height,self.cell_width,self.cell_height))
# draw coins
    def draw_coin(self):
        
        for coin in self.coins:
            pix_coin = self.pacman.get_pix_pos(coin)
            pygame.draw.circle(self.background, PACMAN_COLOUR, 
                            (int(pix_coin.x),int(pix_coin.y)),5)
    def random_wall(self,num_col,num_row):
        width_list = [i for i in range(int(MAZE_WIDTH/self.cell_width))]
        height_list = [i for i in range(int(MAZE_HEIGHT/self.cell_height))]
        rad = np.random.choice(range(int(MAZE_WIDTH/self.cell_width)),num_col,replace=False)
        for xinx in rad:
            y = np.random.choice(range(int(MAZE_HEIGHT/self.cell_height)),num_row,replace=False)
            y_ = [i for i in height_list if i not in y]
            for yidx in y:
                self.wall.append(vec(xinx, yidx))
            for y_idx in y_:
                self.empty_coins.append(vec(xinx, y_idx))
        rad_ = [i for i in width_list if i not in rad]
        for xinx in rad_:
            for yidx in height_list:
                self.empty_coins.append(vec(xinx, yidx))
####### START FUNCTION
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False          
            if event.type == pygame.KEYDOWN or event.type == pygame.K_SPACE or event.type == pygame.KEYDOWN:
                
                self.state = 'playing'
    def start_update(self):
        pass
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("PUSH SPACE BAR", self.screen, [WIDTH//2, HEIGHT//2], 
        START_TEXT_SIZE, (170,132,58), START_FONT, centered=True)
        self.draw_text("1 PLAYER ONLY", self.screen, [WIDTH//2, HEIGHT//2+50], 
        START_TEXT_SIZE, (44,167,198), START_FONT, centered=True)
        self.draw_text("HIGH SCORE", self.screen, [4,0], 
        START_TEXT_SIZE, (255,255,255), START_FONT)
        pygame.display.update()

####### PLAYING FUNCTION
    def playing_events(self):
        k_1 = False
        k_2 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False                
            if event.type == pygame.KEYDOWN:
                # if event.key== pygame.K_1:
                #     k_1 = True
                #     print(k_1)
                # if event.key== pygame.K_2:
                #     k_2 = True
                #     print(k_2)
                # keys = pygame.key.get_pressed()
                if event.key == pygame.K_p:
                    self.stop = True
                if event.key == pygame.K_1:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),1)]
                    self.pacman.step = 0
                if event.key == pygame.K_2:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),2)]
                    self.pacman.step = 0
                if event.key == pygame.K_3:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),3)]
                    self.pacman.step = 0
                if event.key == pygame.K_4:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),4)]
                    self.pacman.step = 0
                if event.key == pygame.K_5:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),5)]
                    self.pacman.step = 0
                if event.key == pygame.K_6:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),6)]
                    self.pacman.step = 0
                if event.key == pygame.K_7:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),7)]
                    self.pacman.step = 0
                if event.key == pygame.K_8:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),8)]
                    self.pacman.step = 0
                if event.key == pygame.K_9:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),9)]
                    self.pacman.step = 0
                if event.key == pygame.K_q:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),10)]
                    self.pacman.step = 0
                if event.key == pygame.K_w:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),11)]
                    self.pacman.step = 0
                if event.key == pygame.K_e:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),12)]
                    self.pacman.step = 0
                if event.key == pygame.K_r:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),13)]
                    self.pacman.step = 0
                if event.key == pygame.K_a:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),14)]
                    self.pacman.step = 0
                if event.key == pygame.K_s:
                    self.coins = [self.empty_coins[i] for i in random.sample(range(0,len(self.empty_coins)),15)]
                    self.pacman.step = 0
    def playing_update(self):
        self.pacman.update()
    def playing_draw(self):
        self.screen.fill(BLACK)
        
        self.screen.blit(self.background,(TOP_BOTTOM_BUFFER//2,TOP_BOTTOM_BUFFER//2))
        self.background.fill(BLACK)
        self.draw_coin()
        self.draw_grid()
        self.draw_text("STEP : {}".format(self.pacman.step), self.screen, [10,2], 
        START_TEXT_SIZE, WHITE, START_FONT)
        self.draw_text("ALGORITHM : A*", self.screen, [WIDTH//2,2], 
        START_TEXT_SIZE, WHITE, START_FONT)
        self.pacman.draw()
        pygame.display.update()