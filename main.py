import pygame
import sys
import random
import math
from pygame import mixer

# initializing the program

pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 400))

# Title and icon
pygame.display.set_caption('Space Invaders')
# icon=pygame.image.load()
# pygame.display.set_icon(icon)

# now this will not clse your window
# background
background = pygame.image.load('space.png')

# background sound
mixer.music.load('space.mp3')
mixer.music.play(-1)
# player
playerImage = pygame.image.load('spaceship.png')
# plyer position
playerX = 370
playerY = 320
player_change = 0
player_Ychange = 0

enemyImg = []
enemyX = []
enemyY = []
enemy_Xchange = []
enemy_Ychange = []
number_of_enemies = 6

for i in range(number_of_enemies):
    # Enemy
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(10, 100))
    enemy_Xchange.append(3)
    enemy_Ychange.append(30)

# bullet
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 320
# bullet_Xchange=0 bullet will not move in y position
bullet_Ychange = 5
# bullet is not fired yet and you can't see it
bullet_state = 'ready'
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    over = over_font.render("GAME OVER", True, (225, 225, 225))
    screen.blit(over, (200, 170))


def view_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    #  .blit means to draw the player image
    screen.blit(playerImage, (x - 15, y - 10))


def enemy(x, y, i):
    #  .blit means to draw the player image
    screen.blit(enemyImg[i], (x, y))


def fired_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))

    if distance <= 27:
        return True
    return False


running = True
# game loop
while running:
    # rgb color filling 0-255
    screen.fill((0, 252, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False
        # let's check the key even whihc is pressed
        if event.type == pygame.KEYDOWN:  # keydown means key pressed
            if event.key == pygame.K_LEFT:
                player_change = -3
            if event.key == pygame.K_RIGHT:
                player_change = 3
            # if event.key == pygame.K_UP:
            #     player_Ychange = -0.1
            # if event.key == pygame.K_DOWN:
            #     player_Ychange = 0.1
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fired_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:  # keyup means releasing the key
            if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP or pygame.K_DOWN:
                player_Ychange = 0
                player_change = 0

    playerX += player_change
    playerY += player_Ychange
    # changing the boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 740:
        playerX = 740
    for i in range(number_of_enemies):
        if enemyY[i] >= 300:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemy_Xchange[i]
        if enemyX[i] <= 0:
            enemy_Xchange[i] = 2
            enemyY[i] += enemy_Ychange[i]
        elif enemyX[i] >= 736:
            enemy_Xchange[i] = -2

            enemyY[i] += enemy_Ychange[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 320
            bullet_state = 'ready'
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(10, 100)
            score_value += 1
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 320
        bullet_state = 'ready'
    # bullet movement
    if bullet_state == 'fire':
        fired_bullet(bulletX, bulletY)
        bulletY -= bullet_Ychange

    player(playerX, playerY)
    view_score(textX, textY)

    # we always need to update the display
    pygame.display.update()
