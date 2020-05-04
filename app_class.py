import pygame
import sys
from settings import *
from player_class import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.player = Player(self, PLAYER_START_POSITION)
        self.walls = []

        self.load()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_update()
                self.playing_draw()
                self.playing_events()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

########################################### HELPER FUNCTIONS ###########################################
    def draw_text(self, words, screen, position, size, color, font_name, center=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if center:
            position[0] = position[0] - text_size[0]//2
            position[1] = position[1] - text_size[1]//2
        screen.blit(text, position)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(
            self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Making walls array
        with open("walls.txt", 'r',) as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
        print(len(self.walls))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(
                self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(
                self.background, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))


########################################### INTRO FUNCTIONS ###########################################


    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('HIGH SCORE', self.screen, [4, 0], START_TEXT_SIZE,
                       (255, 255, 255), START_FONT)
        self.draw_text('PUSH SPACE TO START', self.screen, [WIDTH//2, HEIGHT//2 - 50], START_TEXT_SIZE,
                       (170, 132, 58), START_FONT, center=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2 + 5], START_TEXT_SIZE,
                       (33, 137, 156), START_FONT, center=True)
        self.draw_text('SELECT LEVEL ', self.screen, [WIDTH//2 - 15, HEIGHT//2 + 55], START_TEXT_SIZE,
                       (247, 243, 242), START_FONT, center=True)
        pygame.display.update()

########################################### PLAYING FUNCTIONS ###########################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(
            self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_grid()
        self.draw_text('CURRENT SCORE: 0', self.screen,
                       [60, 0], 18, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen,
                       [WIDTH//2 + 60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        pygame.display.update()
