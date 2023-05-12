import pygame
import random
import math

particles = []

class Particle:
    def __init__(self, x, y, size, speed,  color,normal_speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = normal_speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.remove_speed = speed

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.size -= self.remove_speed
        if self.size <= 0:
            particles.remove(self)

    def draw(self, screen):
        if self.x > 0 and self.y > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

def create_particle(amount, size, speed, pos, color=(255, 255, 255), normal_speed=random.randint(1, 5)):
    if amount > 15:
        amount = 15
    for i in range(amount):
        x, y = pos
        particle = Particle(x, y, random.randint(size-2, size + 2),speed, color,normal_speed)
        particles.append(particle)
