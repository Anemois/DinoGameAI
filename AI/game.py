import pygame
import dino
import random
import sprite_updater as bg

#-------------------------------------
pygame.init()
screenW, screenH = 1600, 400
screen = pygame.display.set_mode((screenW, screenH))#screen
pygame.display.set_caption("Dino Game")#set Title
clock = pygame.time.Clock()                #clock
small_font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 60)
#colors
white = (255,255,255)
black = (0,0,0)
gray = (142,142,142)

start_y = 270
start_runVel = 20
start_jumpVel = 20
start_jumpVelDec = 1

Player = dino.Dino(start_y, start_runVel, start_jumpVel, start_jumpVelDec)

main = False

def get_state():#input : speed, obsticle_dist, obsticle_width, obsticle_gap, paper_plane height
    obsticles = bg.get_obstacles();
    obs_width = obsticles[0][2].get_width() if len(obsticles)>=1 else 0
    obs_dist = obsticles[0][0]-20.0 if len(obsticles)>=1 else 10000000
    pplane = 315-obsticles[0][1] if len(obsticles)>=1 and obsticles[0][3] == 1 else 240
    obs_gap = obsticles[1][0]-obsticles[0][0] if len(obsticles)>=2 else 10000000
    P_y = Player.y
    #print(obs_dist

    return [Player.runVel, obs_dist, obs_width, obs_gap, pplane, P_y]

def draw_text(text, font, color, pos):
    img = font.render(text, True, color)
    screen.blit(img, pos)

def update():
    if main:
        bg.mainUpdate(screen, Player.runVel, Player.score)
        draw_text(str(int(Player.score)), small_font, black, (1500, 10))
    else:
        bg.mainUpdate(screen, 0, Player.score)
        draw_text("Score : " + str(int(Player.score)), big_font, black, (700, 170))

    screen.blit(Player.sprite, (20, Player.y))
    #pygame.draw.rect(screen, black, Player.sprite.get_rect(x=20, y=Player.y))
    #pygame.draw.rect(screen, black, pygame.Rect(26, Player.y, 80, 44))
    #pygame.draw.rect(screen, black, pygame.Rect(30, Player.y+44, 37, 55))
    pygame.display.update()
    clock.tick(60)

def reset():
    global Player
    Player = dino.Dino(start_y, start_runVel, start_jumpVel, start_jumpVelDec)
    bg.reset()

def death():
    PRect = Player.sprite.get_rect(x=20, y=Player.y)
    PRect1 = pygame.Rect(26, Player.y, 80, 44)
    PRect2 = pygame.Rect(30, Player.y+44, 37, 55)
    #cactus = bg.get_cac_sprite()
    for pos in bg.get_obstacles():
        CRect = pos[2].get_rect(x=pos[0], y=pos[1])
        #print(PRect, CRect)
        if Player.isCrouch:
            if pygame.Rect.colliderect(PRect, CRect):
                return False
        elif pygame.Rect.colliderect(PRect1, CRect) or pygame.Rect.colliderect(PRect2, CRect):
            return False
    return True

running = True
#while True:
#    pass
#-------------------------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main == False:
                    main = True
                    reset()
                Player.Jump()
    
    if main:
        Player.gas()
        Player.Crouch(pygame.key.get_pressed()[pygame.K_DOWN])
        Player.Update()
        main = death()
        
    update()
    
#-------------------------------------
pygame.quit()