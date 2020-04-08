import math
import random
import time

import pygame


# Intialize the pygame
pygame.init()

# create the screen
surface = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_position = [0,0]
background_image = pygame.image.load("background.png").convert()


# Caption and Icon
pygame.display.set_caption("Space Invader")

# Player
gun= pygame.image.load('player.png')
gX = 370
gY = 480
gX_change = 0

# Enemy
enem = []
eX = []
eY = []
eX_change = []
eY_change = []
num = 6

for i in range(num):
    enem.append(pygame.image.load('enemy.png'))
    eX.append(random.randint(0, 736))
    eY.append(random.randint(50, 150))
    eX_change.append(4)
    eY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

b = pygame.image.load('bullet.png')
bX = 0
bY = 480
bX_change = 0
bY_change = 10
bst = "ready"

# Score

score = 0
text = pygame.font.Font('freesansbold.ttf', 32)

tX = 10
tY = 10

# Game Over
font = pygame.font.Font('freesansbold.ttf', 64)


def sc(x, y):
    s = font.render("Score : " + str(score), True, (255, 255, 255))
    surface.blit(s, (x, y))


def end():
    o = font.render("GAME OVER", True, (255, 255, 255))
    surface.blit(o, (200, 250))


def play(x, y):
    surface.blit(gun, (x, y))


def enemy(x, y, i):
    surface.blit(enem[i], (x, y))


def fb(x, y):
    global bst
    bst = "fire"
    surface.blit(b, (x + 16, y + 10))


def col(eX, eY, bX, bY):
    dist = math.sqrt(math.pow(eX - bX, 2) + (math.pow(eY - bY, 2)))
    if dist < 27:
        return True
    else:
        return False


# Game Loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done= True

        pygame.display.flip()
        clock.tick(60)
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gX_change = -5
            if event.key == pygame.K_RIGHT:
                gX_change = 5
            if event.key == pygame.K_SPACE:
                if bst is "ready":
                    # Get the current x cordinate of the spaceship
                    bX = gX
                    fb(bX, bY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                gX_change = 0



    gX += gX_change
    if gX <= 0:
        gX = 0
    elif gX >= 736:
        gX = 736

    # Enemy Movement
    for i in range(num):

        # Game Over
        if eY[i] > 440:
            for j in range(num):
                eY[j] = 2000
            end()
            break

        eX[i] += eX_change[i]
        if eX[i] <= 0:
            eX_change[i] = 4
            eY[i] += eY_change[i]
        elif eX[i] >= 736:
            eX_change[i] = -4
            eY[i] += eY_change[i]

        # Collision
        collision = col(eX[i], eY[i], bX, bY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score+= 1
            eX[i] = random.randint(0, 736)
            eY[i] = random.randint(50, 150)

        enemy(eX[i], eY[i], i)

    # Bullet Movement
    if bY <= 0:
        bY = 480
        bst = "ready"

    if bst is "fire":
        fb(bX, bY)
        bY -= bY_change

    play(gX, gY)
    sc(tX, tY)

    pygame.display.update()
    surface.fill((0,0,0))
    surface.blit(background_image, background_position)