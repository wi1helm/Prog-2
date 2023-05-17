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
        self.particals = []
        self.isSpliting = False

    def update(self, screen_width, screen_height):

        global SPLIT_EVENT, new_size, pieces, pieceIndex
        
        if self.isSpliting:
            print(pieces)
            print(pieceIndex, self.isSpliting)
            for event in pygame.event.get():
                if event.type == SPLIT_EVENT and pieceIndex <= pieces:
                    print("Spliting")
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

                    piece = Boss_bits(self.x, self.y, new_size * 1.5,self.player, self, self.split_point, (self.x+int(self.size)*chanceX*4+1, self.y+int(self.size)*chanceY*4+1))
                    self.pieces.append(piece)
                    self.size -= new_size
                    pieceIndex += 1
                if pieceIndex > pieces:
                    print("Done")
                    self.splitDone()

        for particle in self.particals:
            particle.update(screen_width,screen_height)
        
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
        global SPLIT_EVENT, new_size, pieces, pieceIndex
        pieceIndex = 0
        SPLIT_EVENT = pygame.USEREVENT + 5
        pygame.time.set_timer(SPLIT_EVENT, 10)
        print("split")
        self.split_ready = False
        self.lastSplit = self.size
        self.split_point = (self.x,self.y)
        pieces =  random.randint(10,15)
        new_size = (self.size / pieces)
        self.isSpliting = True
        
    def splitDone(self):
        pygame.time.set_timer(SPLIT_EVENT, 0)
        self.isSpliting = False
        self.total_size_pieces = 0
        for piece in self.pieces:
            self.total_size_pieces += piece.size
        self.nextActionNumber = self.total_size_pieces - 70
        print(self.total_size_pieces,self.nextActionNumber)
        self.x = 10**4
        self.y = 10**4
        self.size = 0
        self.speed = 0
        self.asseble_ready = True

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
        self.shockWave()
        if self.total_size_pieces >= 10:
            self.split_ready = True
    
    def shockWave(self):
        for i in range(360):
            particle = particleCarrier(self.x + self.size * math.cos(math.radians(i)),self.y + self.size * math.sin(math.radians(i)),10,self.player,math.radians(i), self)
            self.particals.append(particle)
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Boss_bits:
    def __init__(self,x,y,size,player, boss, point, startPoint):
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
        self.start = True
        self.startPoint = startPoint
    def update(self, screen_width, screen_height):

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        sdx = self.startPoint[0] - self.x
        sdy = self.startPoint[1] - self.y
        start_distance = math.sqrt(sdx ** 2 + sdy ** 2)

        if self.start:
            self.x += sdx / start_distance * self.speed
            self.y += sdy / start_distance * self.speed
            if start_distance < 4:
                self.start = False




        elif self.assemble:

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


class particleCarrier:
    def __init__(self,x,y,size,player, angle, boss):
        self.size = size
        self.x = x
        self.y = y
        self.angle = angle
        self.color = (255 ,255, 255)
        self.speed = 10
        self.player = player
        self.boss = boss
    def update(self, screen_width, screen_height):

        dx = self.boss.x - self.x
        dy = self.boss.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if self.x > screen_width or self.x < 0 or self.y < 0 or self.y > screen_height or distance > 150:
            self.boss.particals.remove(self)
        create_particle(1,5,2,(self.x,self.y),(114,200,184),0.5)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
    
    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)