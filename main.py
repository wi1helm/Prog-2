import pygame
import os
import librosa

from class_bosses import Splinter
# Importing classes from separate files
from class_enemy import Enemy, ZigzagEnemy, MissileEnemy
from class_particle import *
from class_player import Player




# Initite pygame and pygame mixer
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.4)  # 40% volume

# Set the screen size and title
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Setup loading screen text
font = pygame.font.Font(None, 36)
loading_surface = font.render("Loading", True, (255, 255, 255))
screen.blit(loading_surface, (screen_width/2, screen_height/2))
pygame.display.flip()

# Function to check collisions between bullets and enemies

def checkPlayerDeath():# Check for collition between player and enemies on collotion, death
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
        for fragment in boss.fragments:
            distance = math.sqrt((fragment.x - player.x) ** 2 + (fragment.y - player.y) ** 2)
            if distance < fragment.radius + player.radius:
                    game_over_screen()

def check_collisions(): # Check for collitions between bullets and enemies. Removing size, creating particles on death and giving score
    global score, spawn_enemies

    for bullet in bullets:
        for enemy in enemies:
            distance = math.sqrt((enemy.x - bullet.x) ** 2 + (enemy.y - bullet.y) ** 2)

            if distance < enemy.radius + bullet.radius:
                enemy.radius -= 5
                score += 1

                if enemy.radius <= 2:
                    create_particle(10, 5, 0.1, (enemy.x, enemy.y),new_color)
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
                    create_particle(4, 5, 0.5, (boss.x, boss.y),new_color)
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
                        create_particle(4, 5, 0.5, (piece.x, piece.y),new_color)
                        boss.pieces.remove(piece)
                        score += 10

                    if bullet in bullets:
                        bullets.remove(bullet)
            for fragment in boss.fragments:
                distance = math.sqrt((fragment.x - bullet.x) ** 2 + (fragment.y - bullet.y) ** 2)

                if distance < fragment.radius + bullet.radius:
                    fragment.radius -= 7

                    if fragment.radius <= 2:
                        create_particle(4, 5, 0.5, (fragment.x, fragment.y),new_color)
                        boss.fragments.remove(fragment)
                        score += 10

                    if bullet in bullets:
                        bullets.remove(bullet)
# Function to display title screen and wait for user to start game
def title_screen():
    # Set the background color
    screen.fill((255, 255, 255))

    font = pygame.font.SysFont(None, 48)

    # Create a text surface with the title
    title_text = font.render("My Game", True, (0, 0, 0))
    title_rect = title_text.get_rect()
    title_rect.center = (screen_width // 2, screen_height // 4)

    # Create a text surface for the start button
    message_text = font.render("Start", True, (0, 0, 0))
    message_rect = message_text.get_rect()
    message_rect.center = (screen_width // 2, screen_height // 2)

    # Create a text surface with the setting button
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
                    pygame.mixer.music.load(music_paths[currentMusicID])
                    pygame.mixer.music.play(-1)
                elif setting_rect.collidepoint(mouse_pos):
                    waiting = False

# Function to display game over screen and wait for player to choose option
def game_over_screen():
    
    # Set the background color
    screen.fill((255, 255, 255))

    # Reset all varibles
    global player, bullets, enemies,bosses, score, beat_counter, zigzag, missile, enemy_missile_count, boss_spawn, spawn_enemies, has_boss_spawned, currentMusicID
    player = Player(400, 300)
    bullets = []
    enemies = []
    bosses = []
    score = 0
    currentMusicID = 0
    beat_counter = 0
    boss_spawn = False
    has_boss_spawned = False
    zigzag = False
    missile = False
    spawn_enemies = True
    enemy_missile_count = 0
    
    font = pygame.font.SysFont(None, 48)

    # Create a text surface with the game over message
    message_text = font.render("Game over", True, (0, 0, 0))
    message_rect = message_text.get_rect()
    message_rect.center = (screen_width // 2, screen_height // 4)

    # Create text surfaces for the resart button
    restart_text = font.render("Restart", True, (0, 0, 0))
    restart_rect = restart_text.get_rect()
    restart_rect.center = (screen_width // 2, screen_height // 2)

    # Create a text surface for the back to main menu button
    menu_text = font.render("Main menu", True, (0, 0, 0))
    menu_rect = menu_text.get_rect()
    menu_rect.center = (screen_width // 2, screen_height // 2 + 50)

    # Draw the message and options on the screen
    screen.blit(message_text, message_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(menu_text, menu_rect)

    #load the new song. And make it loop.
    pygame.mixer.music.load(music_paths[currentMusicID])
    pygame.mixer.music.play(-1)

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

# Create varibles and player.

global player, bullets, enemies, score, beat_counter, zigzag, missile, enemy_missile_count, bosses, boss_spawn, spawn_enemies, has_boss_spawned, currentMusicID
player = Player(400, 300)
bullets = []
enemies = []
bosses = []
score = 0

# If there is not highscore file create one with highscore 0
if not os.path.isfile("highscore.txt"):
    with open("highscore.txt", "w") as file:
        file.write("0")

# If there is a highscore file read the heighscore.
with open("highscore.txt", "r") as file:
    highscore = int(file.read())

# Draw the scores
score_surface = font.render("Score: " + str(score), True, (255, 255, 255))
screen.blit(score_surface, (10, 10))
highscore_text = font.render("High score: " + str(highscore), True, (255, 255, 255))
screen.blit(highscore_text, (screen_width - 100, 10))


# Set the minimum brightness threshold for the enemies color
brightness_threshold = 100  



clock = pygame.time.Clock()
running = True



# Load the music varibles.
music_paths = ["song1.mp3",'boss.mp3']

currentMusicID = 0
lastMusicID = currentMusicID
threshold = 0.4
pathIndex = 0
yList = []
srList = []
onset_envList = []
tempoList = []
beat_framesList = []
beat_timesList = []

#Load and analyze the music files. This was made by chatGPT
for paths in music_paths:
    y, sr = librosa.load(paths, mono=True)
    yList.append(y)
    srList.append(sr)
    onset_env = librosa.onset.onset_strength(y=yList[pathIndex], sr=srList[pathIndex])
    onset_envList.append(onset_env)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_envList[pathIndex], sr=srList[pathIndex])
    tempoList.append(tempo)
    beat_framesList.append(beat_frames)
    beat_times = librosa.frames_to_time(beat_framesList[pathIndex], sr=srList[pathIndex])
    beat_timesList.append(beat_times)
    beat_counter = 0
    pathIndex += 1

# Load and play the music on replau.
pygame.mixer.music.load(music_paths[currentMusicID])
pygame.mixer.music.play(-1)

#Add events and timer to those events.
ADD_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY_EVENT, 1200)

SHOOT_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SHOOT_EVENT, 200)

ATTACK_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(ATTACK_EVENT, 400)

FRAG_ATTACK_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(FRAG_ATTACK_EVENT, 1000)

# Enter the title screen.
title_screen()

#Set a defualt color for the enemies.
new_color = (33, 73, 62)

# Initiate if a type of enemiy should spawn.
zigzag = False
missile = False
boss_spawn = False
spawn_enemies = True
enemy_missile_count = 0
has_boss_spawned = False
# Laptop mode makes it auto shoot so you dont have to clikc on trackpad.
mode_laptop = True

# Main loop.
while running:
    clock.tick(60)

    # If the music id changed load and play the new music id
    if lastMusicID != currentMusicID:
        pygame.mixer.music.load(music_paths[currentMusicID])
        pygame.mixer.music.play(-1)
        beat_counter = 0
    lastMusicID = currentMusicID

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shoot(bullets)
        if event.type == ATTACK_EVENT: # Makes the boss split bits attack the player.
            if len(bosses) > 0:
                for boss in bosses:
                    randomPiece = random.randint(0,len(boss.pieces))
                    for i in range(len(boss.pieces)):
                        if i == randomPiece:
                            if boss.pieces[i].attack != True and boss.pieces[i].retreat != True:
                                boss.pieces[i].startAttack()
                                
        if event.type == FRAG_ATTACK_EVENT: # Makes the boss fragments attack if there is a boss
            if len(bosses) > 0:
                for boss in bosses:
                    if boss.normal:
                        boss.attack()


        if event.type == SHOOT_EVENT and mode_laptop: # Make the player auto shoot.
            player.shoot(bullets)
        elif event.type == ADD_ENEMY_EVENT:
            
            if score > 110 and has_boss_spawned == False: # If the score is highe and the boss has never spawned. Spawn the boss.
                boss_spawn = True

            if boss_spawn == True: # Spawn the boss
                currentMusicID = 1
                boss = Splinter(screen_width,screen_height,player)
                bosses.append(boss)
                boss_spawn = False
                has_boss_spawned = True
                spawn_enemies = False
                print("boss Spawned")

            
            if spawn_enemies: # If enemy spawn event is true. So a enemy should spawn.
                if score > 50: #If the score is higher then 50 there is a chance to spawn missile enemy.
                    missile = random.random() < 0.4
                
                if score > 100: # If the score is highet then 00 there is a chanche to spawn the zigzag enemy,
                    
                    zigzag = random.random() < 0.2 # 20% change of zigzagg enemy
                if zigzag:
                    zigzag = False
                    enemies.append(ZigzagEnemy(screen_width, screen_height, player))
                elif missile and enemy_missile_count < 6:
                    missile = False
                    enemies.append(MissileEnemy(screen_width, screen_height, player))
                    enemy_missile_count += 1
                else: # Spawn normal enemy.
                    missile = False
                    zigzag = False
                    enemies.append(Enemy(screen_width, screen_height, player))

    # Handle player movement
    keys_pressed = pygame.key.get_pressed()
    player.move(keys_pressed, screen_width, screen_height) # Move the player.





    # Check for collisions
    check_collisions()
    #checkPlayerDeath()

    # Update high score
    with open("highscore.txt", "r") as file:
        highscore = int(file.read())
    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as file:
            file.write(str(highscore))

    # Draw, update and get new color for all enemies and bullets.
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
        boss.color = new_color
        boss.update(screen_width,screen_height)
        for bits in boss.pieces:
            bits.draw(screen)
            bits.color = new_color
            bits.update(screen_width,screen_height,screen)
        for particle in boss.particals:
            particle.draw(screen)
        for fragment in boss.fragments:
            fragment.draw(screen)
            fragment.color = new_color
            if fragment.start_animating == True:
                fragment.start_animation()
            else:
                fragment.update(screen_width,screen_height)
    player.draw(screen) # Draw player

    # Display score and high score
    score_surface = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    highscore_text = font.render("High score: " + str(highscore), True, (255, 255, 255))
    screen.blit(highscore_text, (screen_width - 200, 10))

    pygame.display.flip()

    # If there is a new beat from the music analysis get a new color. This was made with chatGPT
    if beat_counter < len(beat_timesList[currentMusicID]) and pygame.mixer.music.get_pos() / 1000 >= beat_timesList[currentMusicID][beat_counter]:
        if onset_envList[currentMusicID][beat_framesList[currentMusicID][beat_counter]] > threshold:
            while True:
                new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # Check if the sum of RGB values is above the brightness threshold
                if sum(new_color) > brightness_threshold:
                    break
        beat_counter += 1
pygame.quit()




