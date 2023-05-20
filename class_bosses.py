import pygame
import random
import math

from class_particle import particles, create_particle
from class_enemy import Enemy

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
        self.asseble_ready = False
        self.total_size_pieces = 0
        self.nextActionNumber = self.size - 20
        self.ending = False
        self.particals = []
        self.fragments = []
        self.normal = True
        self.shrink = False
        self.growth = False
    def update(self, screen_width, screen_height):

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
        
        print("split")
        self.split_ready = False
        self.lastSplit = self.size
        self.split_point = (self.x,self.y)
        pieces =  random.randint(10,15)
        new_size = (self.size / pieces)
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

            piece = Boss_bits(self.x+int(self.size)*chanceX*2+1, self.y+int(self.size)*chanceY*2+1, new_size,self.player, self, self.split_point)
            self.pieces.append(piece)
            self.size -= new_size
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
    
    def attack(self):

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

        fragment = Splinter_fragments(self.x + self.size * chanceX,self.y + self.size * chanceY,self.player,(self.player.x,self.player.y))
        self.fragments.append(fragment)
    
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Boss_bits:
    def __init__(self,x,y,size,player, boss, point):
        self.boss = boss
        self.size = size
        self.x = x
        self.y = y
        self.color = (255 ,48, 0)
        self.speed = random.randint(5,15)
        self.player = player
        self.attackRadius = 300
        self.angle = None
        self.assemble = False
        self.assemblePoint = point
        self.attack = False
        self.retreat = False
        self.attackPoint = (player.x,player.y)
        self.retreatPoint = None
        self.presiceAttackPoint = (player.x,player.y)
        self.attackSpeed = 8
        


    def startAttack(self):
        if self.attack == False and self.retreat == False:
            self.presiceAttackPoint = (self.player.x,self.player.y)
            self.retreatPoint = (self.x,self.y)
            self.attack = True


    def update(self, screen_width, screen_height,screen):
        
        dx = self.attackPoint[0] - self.x
        dy = self.attackPoint[1] - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        


        if self.assemble:

            dx = self.assemblePoint[0] - self.x
            dy = self.assemblePoint[1] - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

            if distance < 5:
                self.boss.asseble()


        elif self.attack :
            print("Crarche")
            print(self.presiceAttackPoint)
            ax, ay = self.presiceAttackPoint
            dx = ax - self.x
            dy = ay - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            print("attack distance ", distance)
            if distance > 5:
                self.x += dx / distance * self.attackSpeed
                self.y += dy / distance * self.attackSpeed
            else:
                print("we win")
                self.attack = False
                self.retreat = True

        elif self.retreat :
            print("You stupid")
            print(self.retreatPoint)
            rx, ry = self.retreatPoint
            dx = rx - self.x
            dy = ry - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            print("retread distance ", distance)
            if distance > 0.5:
                self.x += dx / distance * self.attackSpeed
                self.y += dy / distance * self.attackSpeed
            else:
                self.retreat = False

        elif distance > self.attackRadius:

            

            print("Orbit time")
            v = math.radians(180 - (math.degrees(math.asin(self.attackRadius/distance) + math.atan(dx/dy))))
            vod = math.radians((360 - math.degrees(math.asin(self.attackRadius/distance) + math.atan(dx/dy))))

            new_point_y = self.attackPoint[1] - (self.attackRadius * math.sin(v))
            new_point_x = self.attackPoint[0] - (self.attackRadius * math.cos(v))

            new_point_yod = self.attackPoint[1] - (self.attackRadius * math.sin(vod))
            new_point_xod = self.attackPoint[0] - (self.attackRadius * math.cos(vod))


            if self.attackPoint[1] > self.y:
                
                dy = new_point_y - self.y
                dx = new_point_x - self.x

                distance = math.sqrt(dx ** 2 + dy ** 2)

                self.x += dx / distance * self.speed
                self.y += dy / distance * self.speed
            else:
                dy = new_point_yod - self.y
                dx = new_point_xod - self.x

                distance = math.sqrt(dx ** 2 + dy ** 2)

                self.x += dx / distance * self.speed
                self.y += dy / distance * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Splinter_fragments(Enemy):
    def __init__(self,x,y,player, start_point):
        super().__init__(0,0,player)
        self.x = x
        self.y = y
        self.start_point = start_point
        self.start_animating = True
        self.animation_speed = 10
    def start_animation(self):
        sx, sy = self.start_point
        dx = sx - self.x
        dy = sy - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 5:
            self.x += dx / distance * self.animation_speed
            self.y += dy / distance * self.animation_speed
        else:
            self.start_animating = False




class particleCarrier:
    def __init__(self,x,y,size,player, angle, boss):
        self.size = size
        self.x = x
        self.y = y
        self.angle = angle
        self.color = (255 ,255, 255)
        self.speed = 5
        self.player = player
        self.boss = boss
    def update(self, screen_width, screen_height):

        dx = self.boss.x - self.x
        dy = self.boss.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if self.x > screen_width or self.x < 0 or self.y < 0 or self.y > screen_height or distance > 200:
            self.boss.particals.remove(self)
        create_particle(1,5,0.5,(self.x,self.y),(114,200,184),0.5)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
    
    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)