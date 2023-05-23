import pygame
import random
from .config import *
from pygame.math import Vector2 as vec


class Ghosts:
    def __init__(self, controller, coordinates):
        """
        Ghost class constructor. 
        Controller (class) Controller class is called. Used to work with the controller for drawing on the screen, grabbing screen data, and acessing the boundaries layout to be used with the player
        coordinates (variable) Vector grid location of ghost (enemy)
        identity (int) identity variable ranging from 1-4
        """
        self.controller = controller
        self.coordinates = coordinates
        self.pixel_position = self.getPosition()
        self.direction = vec(0,0)
        self.speed = SPEED
    
    def draw(self):
        """
        Method that draws an enemy on the screen with a designated color, specified pixel position, and width.
        """
        pygame.draw.circle(self.controller.screen, (190, 194, 15), (int(self.pixel_position.x), int(self.pixel_position.y)), WIDTH)

    def update(self):
        """
        Handles movement updates.
        """
        self.coordinates += self.direction*self.speed
        self.randomMovement()

    def randomMovement(self):
        """
        Sets enemy direction to a randomly generated one.
        """
        self.direction = self.randomDirection()

    def randomDirection(self):
        """
        Randomly generates direction. Queues a position with a generated random direction.
        return (int) Vector directional value, using (xdirection, ydirection)
        """
        number = random.randint(0, 3)
        if number == 1:
            xdirection, ydirection = 1, 0
        elif number == 0:
            xdirection, ydirection = 0, 1
        elif number == 2:
            xdirection, ydirection = -1, 0
        else:
            xdirection, ydirection = 0, -1
        return vec(xdirection, ydirection)

    def getPosition(self):
        """
        Method that calculates a pixel position vector value given an object grid-based coordinates. Uses the "boxes" of the screen (grid).
        Return : Vector value to be used as the object's pixel position
        """
        return vec(self.coordinates.x*self.controller.maze_width, self.coordinates.y*self.controller.maze_height)

"""
    def Centered(self):
        
        Method that checks if the enemies's pixel position is in the middle of the "grid" by comparing it to the "box" size. Does this for both the x-axis and y-axis. Prevents enemies from moving mid box.
        return: (boolean) True/False statement. Returns true if the enemy is centered within the box/grid.
        
        if int(self.pixel_position) % self.controller.box_width == 0:
            if self.direction ==  vec(1,0) or self.direction == (-1,0) or self.direction == vec(0,0):
                return True
        if int(self.pixel_position.y) % self.controller.box_height == 0:
            if self.direction ==  vec(1,0) or self.direction == (-1,0) or self.direction == vec(0,0):
               return True
        return False
"""

""" def setColor(self):
        
        Method that returns a color based on the enemy's identity.
        return (color) color.
        
        if self.identity == 4:
            return (100, 200, 30)
        if self.identity == 3:
            return (75, 50, 84)
        if self.identity == 2:
            return (200, 100, 3)
        if self.identity == 1:
            return (34, 159, 103)
"""

