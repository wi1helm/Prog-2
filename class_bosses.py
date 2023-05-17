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
        self.size = self.health / 5
        self.color = (255 ,48, 0)
        self.pieces = []
        self.split_point = (self.x,self.y)
        self.split_ready = True
        self.asseble_ready = False
        self.total_size_pieces = 0
        self.nextActionNumber = self.size - 20
        self.ending = False

    def update(self, screen_width, screen_height):



        self.total_size_pieces = 0
        for piece in self.pieces:
            self.total_size_pieces += piece.size

        if self.total_size_pieces < 20 and self.size < 20 and self.ending == False:
            self.split_ready = False
            self.ending = True
            self.nextActionNumber = 0
            self.start_asseble()
        if self.total_size_pieces < self.nextActionNumber and self.asseble_ready == True:
            self.start_asseble()

        if self.size < self.nextActionNumber and self.split_ready == True:
            self.split()

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def split(self):
        print("split")
        self.asseble_ready = True
        self.split_ready = False
        self.lastSplit = self.size
        pieces =  2 #random.randint(10,15)
        print(pieces)
        new_size = (self.size / pieces) * 1.5
        self.split_point = (self.x,self.y)
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

            piece = Boss_bits(self.x+int(self.size)*chanceX*2, self.y+int(self.size)*chanceY*2, new_size,self.player, self, self.split_point )
            self.pieces.append(piece)
            self.size -= new_size
        
        print(self.size, self.nextActionNumber)
        for piece in self.pieces:
            self.total_size_pieces += piece.size
        self.nextActionNumber = self.total_size_pieces - 70
        self.x = 10**4
        self.y = 10**4
        self.size = 0
        self.speed = 0
        

    def start_asseble(self):
        for bits in self.pieces:
            bits.assemble = True

    def asseble(self):

        for bits in self.pieces:
            bits.assemble = False

        print("Avengers")
        self.asseble_ready = False
        pieces_copy = self.pieces[:]
        for piece in pieces_copy:
            self.size += (piece.size + 5)
            self.pieces.remove(piece)
            print(len(pieces_copy))
        self.size /= 1.5
        self.x = self.split_point[0]
        self.y = self.split_point[1]
        self.speed = 0.5
        print(self.size, self.nextActionNumber)
        self.nextActionNumber = self.size - 50

        if self.total_size_pieces >= 10:
            self.split_ready = True

    

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Boss_bits:
    def __init__(self,x,y,size,player, boss, point):
        self.boss = boss
        self.size = size
        self.x = x
        self.y = y
        self.color = (255 ,48, 0)
        self.speed = random.randint(5,7)
        self.player = player
        self.attackRadius = 300
        self.angle = None
        self.goCirle = False
        self.assemble = False
        self.assemblePoint = point
    def update(self, screen_width, screen_height):

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if self.assemble:

            dx = self.assemblePoint[0] - self.x
            dy = self.assemblePoint[1] - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

            if distance < 5:
                self.boss.asseble()

        elif distance > self.attackRadius + 200:
            self.goCirle = False
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

        elif distance > self.attackRadius and self.goCirle == False:
            
            v = math.radians(180 - math.degrees(math.asin(self.attackRadius/distance) + math.atan(dx/dy)))
            new_point_y = self.player.y + (self.attackRadius * math.sin(v))
            new_point_x = self.player.x - (self.attackRadius * math.cos(v))

            dy = new_point_y - self.y
            dx = new_point_x - self.x

            distance = math.sqrt(dx ** 2 + dy ** 2)

            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed
        else:
            
            self.goCirle = True
            self.angle = math.atan2(dx,dy)
            self.angle += 1.5
        
            new_dx = math.sin(self.angle) * self.attackRadius
            new_dy = math.cos(self.angle) * self.attackRadius
            new_distance = math.sqrt(new_dx ** 2 + new_dy ** 2)
            
            self.x += new_dx / new_distance * self.speed
            self.y += new_dy / new_distance * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
