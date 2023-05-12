import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 2
        self.vx = 0
        self.vy = 0
        self.color = (0, 255, 0)
        self.FRICTION = 0.1

    def move(self, keys, screen_width, screen_height):
        # update velocity based on key presses
        if keys[pygame.K_w]:
            self.vy -= self.speed
        if keys[pygame.K_s]:
            self.vy += self.speed
        if keys[pygame.K_a]:
            self.vx -= self.speed
        if keys[pygame.K_d]:
            self.vx += self.speed

        # apply friction
        self.vx *= (1 - self.FRICTION)
        self.vy *= (1 - self.FRICTION)

        # update position based on velocity
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        # check if new position is outside the window
        if new_x < self.radius:
            new_x = self.radius
            self.vx = 0
        elif new_x > screen_width - self.radius:
            new_x = screen_width - self.radius
            self.vx = 0
        if new_y < self.radius:
            new_y = self.radius
            self.vy = 0
        elif new_y > screen_height - self.radius:
            new_y = screen_height - self.radius
            self.vy = 0

        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def shoot(self, bullets):
        mouse_pos = pygame.mouse.get_pos()
        bullet = Bullet(self.x, self.y, math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x))
        bullets.append(bullet)

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 12
        self.radius = 2.5
        self.color = (255, 0, 0)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, screen):
        if self.x > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
