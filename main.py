# import pygame and some key presses
import random

import pygame
import pygame.mixer
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KEYUP,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)

# initialize pygame
pygame.init()

# define dimensions of screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800

# create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set icon and title of window
pygame.display.set_caption('meadows game')
icon = pygame.image.load('assets/meadows-icon.png')
pygame.display.set_icon(icon)

# load background
background = pygame.image.load('assets/classroom.jpg')

# player
playerImg = pygame.image.load('assets/meadows-player.png')
playerX = 300
playerY = 650
playerX_change = 0

# enemies
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
enemy_amount = 4

for i in range(enemy_amount):
    if i == 1 or i == 3:
        enemyImg.append(pygame.image.load('assets/ink-chicken.png'))
    else:
        enemyImg.append(pygame.image.load('assets/newton-rabbit.png'))
    enemyX.append(random.randint(0, 600))
    enemyY.append(-125)
    enemyY_change.append(0.2)

# ruler
rulerImg = pygame.image.load('assets/ruler.png')
rulerX = 0
rulerY = 650
rulerY_change = -2.5
ruler_ready = True

# score
score_value = 0
font = pygame.font.Font('assets/comicbd.ttf', 28)

# load sounds and music
chicken_sound = pygame.mixer.Sound('assets/chicken-sound.mp3')
rabbit_sound = pygame.mixer.Sound('assets/rabbit-sound.mp3')
woosh = pygame.mixer.Sound('assets/woosh.mp3')
pygame.mixer.music.load('assets/numb.mp3')
music_playing = False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def throw_ruler(x, y):
    global ruler_ready
    ruler_ready = False
    screen.blit(rulerImg, (x + 62, y - 75))


def check_collision(enemyX, enemyY, rulerX, rulerY):
    x_collide = enemyX <= rulerX <= enemyX + 82
    y_collide = enemyY <= rulerY <= enemyY + 125
    if x_collide and y_collide:
        return True


def show_score():
    score = font.render("score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (10, 10))


game_over_font = pygame.font.Font('assets/comicbd.ttf', 72)


def game_over():
    game_over_text = font.render("GAME OVER", True, (0, 0, 0))
    kill_count = font.render("you killed " + str(score_value) + " little rascals", True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (150, 250, 400, 250))
    screen.blit(game_over_text, (250, 300))
    screen.blit(kill_count, (175, 400))


# MAIN LOOP
running = True
while running:

    # draw background
    screen.blit(background, (0, 0))

    # event handler
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                playerX_change = -0.75
            if event.key == K_RIGHT:
                playerX_change = 0.75
            if event.key == K_SPACE and ruler_ready:
                rulerX = playerX + 62
                woosh.play()
                throw_ruler(rulerX, rulerY)
            if event.key == K_ESCAPE:
                running = False

        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                playerX_change = 0

        # end program when window is closed
        if event.type == QUIT:
            running = False

    # update position of player
    playerX += playerX_change

    # handle enemy movement and collision
    for i in range(enemy_amount):
        # game over
        if enemyY[i] >= 800:
            for j in range(enemy_amount):
                enemyY[j] = 2000
            if not music_playing:
                pygame.mixer.music.play(-1)
                music_playing = True
            game_over()
            break

        enemyY[i] += enemyY_change[i]
        # detect collision
        collision = check_collision(enemyX[i], enemyY[i], rulerX, rulerY)
        if collision:
            if i == 1 or i == 3:
                chicken_sound.play()
            else:
                rabbit_sound.play()
            rulerY = 650
            ruler_ready = True
            enemyX[i] = random.randint(0, 600)
            enemyY[i] = -150
            score_value += 1
        enemy(enemyX[i], enemyY[i], i)

    # add boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 575:
        playerX = 575

    # handle movement of ruler
    if not ruler_ready:
        throw_ruler(rulerX - 62, rulerY)
        rulerY += rulerY_change
    if rulerY <= 0:
        rulerY = 650
        ruler_ready = True

    # draw
    player(playerX, playerY)

    # increases enemy speed over time
    for i in range(enemy_amount):
        enemyY_change[i] += 0.000015

    # display score
    show_score()

    # update screen
    pygame.display.flip()
