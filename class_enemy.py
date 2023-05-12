import pygame
import random
import math

from class_particle import particles, create_particle

class Enemy:
    def __init__(self, screen_width, screen_height, player):
        self.side = random.randint(1, 4)
        if self.side == 1:  # Spawn from the top
            self.x = random.randint(0, screen_width)
            self.y = 0
        elif self.side == 2:  # Spawn from the right
            self.x = screen_width
            self.y = random.randint(0, screen_height)
        elif self.side == 3:  # Spawn from the bottom
            self.x = random.randint(0, screen_width)
            self.y = screen_height
        else:  # Spawn from the left
            self.x = 0
            self.y = random.randint(0, screen_height)

        self.radius = 15
        self.color = (0,0, 0)
        self.speed = random.randint(1, 3)
        self.player = player

    def update(self, screen_width, screen_height):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class ZigzagEnemy:
    def __init__(self, screen_width, screen_height, player):
        self.side = random.randint(1, 4)
        if self.side == 1:  # Spawn from the top
            self.x = random.randint(0, screen_width)
            self.y = 0
        elif self.side == 2:  # Spawn from the right
            self.x = screen_width
            self.y = random.randint(0, screen_height)
        elif self.side == 3:  # Spawn from the bottom
            self.x = random.randint(0, screen_width)
            self.y = screen_height
        else:  # Spawn from the left
            self.x = 0
            self.y = random.randint(0, screen_height)

        self.radius = 15
        self.color = (255, 0, 0)
        self.speed = 5
        self.player = player
        self.zigzag_speed = 0.5
        self.max_zigzag_width = random.randint(10, 20)
        self.current_zigzag_pos = 0
    def update(self, screen_width, screen_height):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            # Move towards the player
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed
            self.zigzag_width = self.max_zigzag_width - distance/500
            # Calculate the offset for the zigzag movement
            angle = math.atan2(dy, dx)
            zigzag_offset = math.sin(self.current_zigzag_pos / self.zigzag_width * 2 * math.pi) * self.zigzag_width / 2
            self.current_zigzag_pos += self.zigzag_speed

            # Apply the offset to the enemy position
            self.x += math.cos(angle + math.pi / 2) * zigzag_offset
            self.y += math.sin(angle + math.pi / 2) * zigzag_offset

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Missile:
    def __init__(self, x, y,player):
        self.x = x
        self.y = y
        self.radius = 2.5
        self.color = (255, 0, 0)
        self.speed = 2.5
        self.player = player
    def update(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            # Move towards the player
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed
        create_particle(5,2,0.1,(self.x,self.y),(192,192,192),1)
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class MissileEnemy:
    def __init__(self, screen_width, screen_height, player):

        self.radius = 15
        self.color = (0, 255, 0)
        self.player = player
        self.missiles = []
        have_pos = False
        while not have_pos:
            test_x = random.randint(self.radius,screen_width-self.radius)
            test_y = random.randint(self.radius, screen_height - self.radius)
            dx = self.player.x - test_x
            dy = self.player.y - test_y
            distance = max(math.sqrt(dx ** 2 + dy ** 2), 1)
            if distance > 300:
                have_pos = True
                self.x = test_x
                self.y = test_y
            else:
                pass



    def update(self, screen_width, screen_height):
        if len(self.missiles) == 0:  # Shoot missiles every 30 ticks
            self.missiles.append(Missile(self.x, self.y,self.player))
        for missile in self.missiles:
            dx = missile.x - self.x
            dy = missile.y - self.y
            distance = max(math.sqrt(dx ** 2 + dy ** 2), 1)
            if distance > 500:
                create_particle(10, 6,0.2 , (missile.x, missile.y), (255, 165, 0))
                self.missiles.remove(missile)
        # Remove missiles that are off the screen or hit the player
        for missile in self.missiles[:]:
            if missile.x < 0 or missile.x > screen_width or missile.y < 0 or missile.y > screen_height:
                self.missiles.remove(missile)
            elif math.dist((missile.x, missile.y), (self.player.x, self.player.y)) < self.player.radius:
                self.missiles.remove(missile)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        for missile in self.missiles:
            missile.update()
            missile.draw(screen)
