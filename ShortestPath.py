from ipaddress import collapse_addresses
import math
import queue
import pygame

width = 1000
box = pygame.display.set_mode((width, width)) #display is square
pygame.display.set_caption("Path Finding Visualizer")

ORANGE = (253, 132, 31)
RED = (225, 77, 42)
PINK = (205, 16, 77)
PURPLE = (156, 44, 119)
DARKPURPLE = (65, 21, 48)
DARKYELLOW = (250, 194, 19)
BROWN = (135, 100, 69)
PEACH = (238, 195, 115)
BLACK = (74, 64, 58)
GREEN = (127, 183, 126)
LIGHT = (247, 246, 220)

class node:

    def __init__(self, row, col, width, rowsCount):
        self.adjacent = []
        self.xCordinate = row*width
        self.yCordinate = col*width
        self.row = row
        self.col = col
        self.rowsCount = rowsCount
        self.color = PEACH
    
    def getPosition(self):
        return self.row, self.col

    def blank(self):
        if self.color == LIGHT:
            return True
        else:
            return False
    
    def is_filled(self):
        if self.color == RED:
            return True
        else:
            return False
            
    
    def is_inSet(self):
        if self.color == GREEN:
            return True
        else:
            return False

    def is_blocked(self):
        if self.color == BLACK:
            return True
        else:
            return False

    def startingPoint(self):
        if self.color == ORANGE:
            return True
        else:
            return False

    def stopPoint(self):
        if self.color == PEACH:
            return True
        else:
            return False

    def stop(self):
        self.color = PEACH

    def block(self):
        self.color = BLACK

    def fill(self):
        self.color = RED

    def inSet(self):
        self.color = GREEN


