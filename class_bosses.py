import pygame
import random
import math

from class_particle import particles, create_particle


class Splinter:
    def __init__(self, screen_width, screen_height, player):
        self.x = screen_width
        self.y = screen_height / 2
        self.player = player
        self.health = 500
        self.speed = 0.5
        self.size = self.health / 2
        self.color = (255 ,48, 0)
        self.pieces = []
        self.split_point = (self.x,self.y)
        self.split_ready = True
        self.total_size_pieces = 0
        self.lastSplit = self.size

    def update(self, screen_width, screen_height):
        print(self.total_size_pieces)
        print(self.lastSplit - 10)
        self.total_size_pieces = 0
        for piece in self.pieces:
            self.total_size_pieces += piece.size
        if self.total_size_pieces < (self.lastSplit - 10):
            self.asseble()
        if self.size < (self.lastSplit - 10) and self.split_ready == True:
            self.split()

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def split(self):
        self.split_ready = False
        self.lastSplit = self.size
        pieces = random.randint(10,20)
        new_size = self.size / pieces
        for i in range(pieces):
            chanceX = random.random()
            chanceY = random.random()

            if chanceX < 0.5:
                chanceX = -1
            else:
                chanceX = 1
            if chanceY < 0.5:
                chanceY = -1
            else:
                chanceY = 1

            piece = Boss_bits(self.x+int(self.size)*chanceX, self.y+int(self.size)*chanceY, new_size,self.player)
            self.pieces.append(piece)
            self.size -= new_size
        self.x = 10**3
        self.y = 0
        self.size = 0
        self.split_point = (self.x,self.y)

    def asseble(self):
        for piece in self.pieces:
            self.size += piece.size
            self.x = self.split_point[0]
            self.y = self.split_point[1]
            self.pieces.remove(piece)
        self.split_ready = True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Boss_bits:
    def __init__(self,x,y,size,player):
        self.size = size
        self.x = x
        self.y = y
        self.color = (255 ,48, 0)
        self.speed = 3
        self.player = player
    def update(self, screen_width, screen_height):

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
