import pygame
import os
import librosa

from class_bosses import Splinter
# Importing classes from separate files
from class_enemy import Enemy, ZigzagEnemy, MissileEnemy
from class_particle import *
from class_player import Player

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)  # 50% volume

# Set the screen size and title
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Function to check collisions between bullets and enemies

def checkPlayerDeath():# Check for player death
    for enemy in enemies:
        try:
            for missile in enemy.missiles:
                distance = math.sqrt((missile.x - player.x) ** 2 + (missile.y - player.y) ** 2)
                if distance < enemy.radius + player.radius:
                    game_over_screen()
        except:
            distance = math.sqrt((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2)
            if distance < enemy.radius + player.radius:
                game_over_screen()
    for boss in bosses:
        distance = math.sqrt((boss.x - player.x) ** 2 + (boss.y - player.y) ** 2)
        if distance < boss.size + player.radius:
                game_over_screen()
        for piece in boss.pieces:
            distance = math.sqrt((piece.x - player.x) ** 2 + (piece.y - player.y) ** 2)
            if distance < piece.size + player.radius:
                    game_over_screen()
        for particle in boss.particals:
            distance = math.sqrt((particle.x - player.x) ** 2 + (particle.y - player.y) ** 2)
            if distance < particle.size + player.radius:
                    game_over_screen()

def check_collisions():
    global score, spawn_enemies

    for bullet in bullets:
        for enemy in enemies:
            distance = math.sqrt((enemy.x - bullet.x) ** 2 + (enemy.y - bullet.y) ** 2)

            if distance < enemy.radius + bullet.radius:
                enemy.radius -= 5
                score += 1

                if enemy.radius <= 2:
                    create_particle(10, 5, 0.1, (enemy.x, enemy.y))
                    enemies.remove(enemy)
                    score += 5

                if bullet in bullets:
                    bullets.remove(bullet)

        for boss in bosses:
            distance = math.sqrt((boss.x - bullet.x) ** 2 + (boss.y - bullet.y) ** 2)

            if distance < boss.size + bullet.radius:
                boss.health -= 1
                boss.size -= 0.5

                if boss.size <= 2:
                    create_particle(4, 5, 0.5, (boss.x, boss.y))
                    bosses.remove(boss)
                    print("boss dead")
                    spawn_enemies = True
                    score += 50

                if bullet in bullets:
                    bullets.remove(bullet)

            for piece in boss.pieces:
                distance = math.sqrt((piece.x - bullet.x) ** 2 + (piece.y - bullet.y) ** 2)

                if distance < piece.size + bullet.radius:
                    piece.size -= 1

                    if piece.size <= 2:
                        create_particle(4, 5, 0.5, (piece.x, piece.y))
                        boss.pieces.remove(piece)
                        score += 10

                    if bullet in bullets:
                        bullets.remove(bullet)
# Function to display title screen and wait for user to start game
def title_screen():
    # Set the background color
    screen.fill((255, 255, 255))

    # Create a font object
    font = pygame.font.SysFont(None, 48)

    # Create a text surface with the title
    title_text = font.render("My Game", True, (0, 0, 0))
    title_rect = title_text.get_rect()
    title_rect.center = (screen_width // 2, screen_height // 4)

    # Create a text surface with the message
    message_text = font.render("Start", True, (0, 0, 0))
    message_rect = message_text.get_rect()
    message_rect.center = (screen_width // 2, screen_height // 2)

    # Create a text surface with the setting button text
    setting_text = font.render("Settings", True, (0, 0, 0))
    setting_rect = setting_text.get_rect()
    setting_rect.center = (screen_width // 2, screen_height * 3 // 4)

    # Draw the title and message on the screen
    screen.blit(title_text, title_rect)
    screen.blit(message_text, message_rect)
    screen.blit(setting_text, setting_rect)

    # Update the display
    pygame.display.update()

    # Wait for a button press to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if message_rect.collidepoint(mouse_pos):
                    waiting = False
                elif setting_rect.collidepoint(mouse_pos):
                    waiting = False

# Function to display game over screen and wait for player to choose option
def game_over_screen():
    # Stop playing music
    pygame.mixer.music.rewind()

    # Set the background color
    screen.fill((255, 255, 255))

    global player, bullets, enemies,bosses, score, beat_counter, zigzag, missile, enemy_missile_count, boss_spawn, spawn_enemies, has_boss_spawned
    player = Player(400, 300)
    bullets = []
    enemies = []
    bosses = []
    score = 0
    beat_counter = 0
    boss_spawn = False
    has_boss_spawned = False
    zigzag = False
    missile = False
    spawn_enemies = True
    enemy_missile_count = 0
    # Create a font object
    font = pygame.font.SysFont(None, 48)

    # Create a text surface with the message
    message_text = font.render("Game over", True, (0, 0, 0))
    message_rect = message_text.get_rect()
    message_rect.center = (screen_width // 2, screen_height // 4)

    # Create text surfaces for the options
    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_rect = restart_text.get_rect()
    restart_rect.center = (screen_width // 2, screen_height // 2)

    menu_text = font.render("Main menu", True, (0, 0, 0))
    menu_rect = menu_text.get_rect()
    menu_rect.center = (screen_width // 2, screen_height // 2 + 50)

    # Draw the message and options on the screen
    screen.blit(message_text, message_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(menu_text, menu_rect)

    # Update the display
    pygame.display.update()

    # Wait for the player to choose an option
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    # Restart the game
                    waiting = False
                elif menu_rect.collidepoint(mouse_pos):
                    # Return to the title screen
                    waiting = False
                    title_screen()

global player, bullets, enemies, score, beat_counter, zigzag, missile, enemy_missile_count, bosses, boss_spawn, spawn_enemies, has_boss_spawned
player = Player(400, 300)
bullets = []
enemies = []
bosses = []
score = 0

if not os.path.isfile("highscore.txt"):
    with open("highscore.txt", "w") as file:
        file.write("0")

with open("highscore.txt", "r") as file:
    highscore = int(file.read())

font = pygame.font.Font(None, 36)
score_surface = font.render("Score: " + str(score), True, (255, 255, 255))
screen.blit(score_surface, (10, 10))
highscore_text = font.render("High score: " + str(highscore), True, (255, 255, 255))
screen.blit(highscore_text, (screen_width - 100, 10))

next_color_time = 0
clock = pygame.time.Clock()
running = True

music_path = 'song1.mp3'
threshold = 0.4
y, sr = librosa.load(music_path, mono=True)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
beat_counter = 0

pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  # the -1 value means the music will loop indefinitely

ADD_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY_EVENT, 1200)

SHOOT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SHOOT_EVENT, 200)

title_screen()

new_color = (33, 73, 62)

zigzag = False
missile = False
boss_spawn = True
spawn_enemies = False
enemy_missile_count = 0
has_boss_spawned = False

mode_laptop = False

while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shoot(bullets)
        if event.type == SHOOT_EVENT and mode_laptop:
            player.shoot(bullets)
        elif event.type == ADD_ENEMY_EVENT:
            
            if score > 110 and has_boss_spawned == False:
                boss_spawn = True

            if boss_spawn == True:
                boss = Splinter(screen_width,screen_height,player)
                bosses.append(boss)
                boss_spawn = False
                has_boss_spawned = True
                spawn_enemies = False
                print("boss Spawned")

            
            if spawn_enemies:
                if score > 50:
                    missile = random.random() < 0.4
                
                if score > 100:
                    zigzag = random.random() < 0.2 # 20% change of zigzagg enemy
                if zigzag:
                    zigzag = False
                    enemies.append(ZigzagEnemy(screen_width, screen_height, player))
                elif missile and enemy_missile_count < 6:
                    missile = False
                    enemies.append(MissileEnemy(screen_width, screen_height, player))
                    enemy_missile_count += 1
                else:
                    missile = False
                    zigzag = False
                    enemies.append(Enemy(screen_width, screen_height, player))

    # Handle player movement
    keys_pressed = pygame.key.get_pressed()
    player.move(keys_pressed, screen_width, screen_height)





    # Check for collisions
    check_collisions()
    checkPlayerDeath()

    # Update high score
    with open("highscore.txt", "r") as file:
        highscore = int(file.read())
    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as file:
            file.write(str(highscore))

    # Draw everything
    screen.fill((0, 0, 0))
    for bullet in bullets:
        bullet.update()
        if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
            bullets.remove(bullet)
        bullet.draw(screen)
    for enemy in enemies:
        enemy.update(screen_width, screen_height)
        enemy.draw(screen)
        enemy.color = new_color
    for particle in particles:
        particle.update()
        particle.draw(screen)
    for boss in bosses:
        boss.draw(screen)
        boss.update(screen_width,screen_height)
        for bits in boss.pieces:
            bits.draw(screen)
            bits.update(screen_width,screen_height)
        for particle in boss.particals:
            particle.draw(screen)
    player.draw(screen)

    # Display score and high score
    score_surface = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    highscore_text = font.render("High score: " + str(highscore), True, (255, 255, 255))
    screen.blit(highscore_text, (screen_width - 200, 10))

    pygame.display.flip()
    if beat_counter < len(beat_times) and pygame.mixer.music.get_pos() / 1000 >= beat_times[beat_counter]:
        if onset_env[beat_frames[beat_counter]] > threshold:
            new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        beat_counter += 1
pygame.quit()
