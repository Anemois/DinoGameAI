import pygame
import random
#import os

#dir = os.path.abspath( os.path.dirname( __file__ ) )

white = (255,255,255)
black = (0,0,0)
gray = (142,142,142)

bg_cloud = pygame.image.load("bg/cloud.png")
bg_ground = pygame.image.load("bg/ground.png")
bg_cactus = [pygame.image.load("bg/cactus1.png"), pygame.image.load("bg/cactus2.png"), pygame.image.load("bg/cactus3.png")]
bg_plane = pygame.image.load("bg/paper_plane_big.png")

clouds = []
ground = [0, 2400]
obstacles = []

def get_obstacles():
    return obstacles

def obstacle_update(screen, vel, score, blit):
    if vel >= 100:
        chance = 30//(vel//100)
    else:
        chance = 30
    if (len(obstacles) == 0 and random.randint(1, chance) == 5) or (len(obstacles) != 0 and obstacles[-1][0] < 200 and random.randint(1, chance*3) == 5):
        #if score <= 100:
        #    obstacles.append([1650, 315 - (2*80), bg_plane, 1])
        if random.randint(1, 2) == 1 or score <= 1000:
            obstacles.append([1650, 275, bg_cactus[random.randint(0, 2)], 0])
        else:
            obstacles.append([1650, 315 - (random.randint(0, 2)*80), bg_plane, 1])
            
    for obstacle in obstacles:
        obstacle[0] -= vel/2
        if blit:
            screen.blit(obstacle[2], (obstacle[0], obstacle[1]))

    if(len(obstacles) > 0 and obstacles[0][0] < -500):
        obstacles.pop(0)
    #print(len(cactuses))     

def ground_update(screen, vel, blit):
    #pygame.draw.rect(screen, gray, pygame.Rect(0, 391, 1600, 9))
    for i in range(2):
        #print(ground[i])
        if ground[i] <= -2400:
            ground[i] = ground[(i+1)%2]+2400
        
        ground[i] -= vel/2
        if blit:
            screen.blit(bg_ground, (ground[i], 370))

def cloud_update(screen, vel, blit):
    if (len(clouds) == 0 or clouds[-1][0]) < 1000 and random.randint(1, 300) == 50:
        clouds.append([1650, random.randint(10, 150)])

    for cloud in clouds:
        cloud[0] -= vel/4
        if(cloud[0] < -200):
            clouds.pop(0)
            continue
        if blit:
            screen.blit(bg_cloud, (cloud[0], cloud[1]))

def mainUpdate(screen, vel, score, blit=True):
    if blit:
        screen.fill(white)
    cloud_update(screen, vel, blit=blit)
    obstacle_update(screen, vel, score, blit=blit)
    ground_update(screen, vel, blit=blit)

def reset():
    global clouds
    global ground
    global obstacles
    clouds = []
    ground = [0, 2400]
    obstacles = []