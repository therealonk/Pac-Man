import pygame
import sys
from pygame.math import Vector2 as vec
from src import player
from src import enemies
from src import config


class Controller:

    def __init__(self):
        ''' Initializes the game the sprites Pacman and the Ghosts. Sets the default value of
         background as 610x670 and displays the maze.png. Also Pacman will always be in a moving state until the game ends
         with self.running. '''
        pacman = player.Pacman
        ghosts = enemies.Ghosts
        self.state = "Initialization"
        self.screen = pygame.display.set_mode((610, 670))
        self.maze_width = 560 // 28
        self.maze_height = 620 // 30
        self.running = True
        pygame.init()
        self.background = pygame.image.load('maze.png')
        self.loading()
        self.pacmanposition = vec(21, 4)
        self.ghosts = enemies.Ghosts
        self.ghost = ghosts(self, vec(15,15))
        self.pacman = pacman(self, self.pacmanposition)

    def loading(self):
        '''Opens the boundaries.txt file and creates the walls list with coordinates
        of the walls by storing it as a vector. Also makes the box_width and box_height
        for when a grid is made.'''
        self.coins = []
        self.boundaries = []
        with open("boundaries.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.boundaries.append(vec(xidx, yidx))
                    if char == "C":
                        self.coins.append(vec(xidx, yidx))

    def drawMaze(self):
        ''' Creates the maze or grid using the box_width and box_height.'''
        for i in range(config.SCREEN_WIDTH // self.maze_width):
            pygame.draw.line(self.background, config.WHITE, (i * self.maze_width, 0),
                             (i * self.maze_height, config.SCREEN_HEIGHT))
        for i in range(config.SCREEN_HEIGHT // self.maze_height):
            pygame.draw.line(self.background, config.WHITE, (0, i * self.maze_height),
                             (config.SCREEN_WIDTH, i * self.maze_height))

    def mainloop(self):
        '''Sets up the three game states, menu, playing the game, and the end screen. Currently
        the game is stuck on the In-Game state. '''
        while self.running == True:
            if self.state == "Initialization":
                self.menuEvents()
                self.menuDraw()
            elif self.state == "In-Game":
                self.gameEvents()
                self.gameUpdate()
                self.gameDraw()
            elif self.state == "Game-Over":
                self.gameoverevent()
                self.gameoverloop()
        pygame.quit()
        sys.exit()

    def menuEvents(self):
        ''' The main menu screen and pressing space starts the game.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = "In-Game"

    def menuDraw(self):
        ''' Creates text that says "PUSH SPACE BAR" in the center of the screen.'''
        self.type('PUSH SPACE BAR', self.screen, [
            800 // 2 - 170, 600 // 2 - 50], 15, (170, 132, 58), "arial black", centered=True)
        pygame.display.update()

    def type(self, characters, screen, position, size, color, font_name, centered=True):
        '''Method used for the pygame.type function and displays the characters on the screen given a position, font size, font color,
        and font'''
        font = pygame.font.SysFont(font_name, size)
        text = font.render(characters, False, color)
        text_size = text.get_size()
        screen.blit(text, position)

    def gameEvents(self):
        '''Creates the movement of Pacman with arrow keys'''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.pacman.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.pacman.move(vec(0, -1))
                if event.key == pygame.K_LEFT:
                    self.pacman.move(vec(-1, 0))
                if event.key == pygame.K_DOWN:
                    self.pacman.move(vec(0, 1))

    def drawCoins(self):
        '''Draws coins on the background using the maze (not drawn) and places the coins according to positions on the grid.'''
        for coins in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coins.x * self.maze_width) + self.maze_width // 2 + config.EMPTY_SPACE // 2,
                                int(coins.y * self.maze_height) + self.maze_height // 2 + config.EMPTY_SPACE // 2),
                               5)

    def gameUpdate(self):
        '''Updates the movement of Pacman and the ghost'''
        self.pacman.update()
        self.ghost.update()
        '''Checks if the ghost coordinates is equal to Pacman's coordinates, if so, Pacman loses a life and ends the game state. 
        This starts the 'Game-Over' state.'''
        print(self.ghost.pixel_position)
        print(self.pacman.pixel_position)
        if self.pacman.pixel_position == self.ghost.pixel_position:
            self.loseLife()

    def gameDraw(self):
        '''Draws Pacman, the game screen, coins on the board, and also draws the SCORE: text on the top left of the game window.'''
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (25, 25))
        self.pacman.draw()
        self.drawCoins()
        self.type('SCORE: {}'.format(self.pacman.score),
                  self.screen, [60, 0], 18, config.WHITE, config.FONT)

        self.ghost.draw()
        pygame.display.update()

    def loseLife(self):
        '''Pacman loses a life, thus ending the game and updates the game state to 'Game-Over'.'''
        self.pacman.lives -= 1
        if self.pacman.lives == 0:
            self.state = "Game-Over"

    def gameoverevent(self):
        "Game-Over state of the game. Stops Pacman from moving and pressing escape closes the game window."
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def gameoverloop(self):
        '''Game over state of the game. Displays the text "GAME OVER"'''
        self.screen.fill(config.BLACK)
        self.type("GAME OVER", self.screen, [400 // 2, 600 // 2], 52,
                  config.WHITE,
                  "arial", centered=True)
        pygame.display.update()
