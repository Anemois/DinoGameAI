import pygame
import neat
import os
import dino
import random
import sprite_updater as bg
import pickle
pygame.init()
#-------------------------------------
class DinoGame:
    def __init__(self, screenW, screenH, screen):
        self.screenW, self.screenH = screenW, screenH
        self.screen = screen
        pygame.display.set_caption("Dino Game")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (142, 142, 142)
        self.start_y = 270
        self.start_runVel = 100
        self.start_jumpVel = 23.6
        self.start_jumpVelDec = 1.5
        self.Player = dino.Dino(
            self.start_y, self.start_runVel, self.start_jumpVel, self.start_jumpVelDec
        )
        self.main = False

    def draw_text(self, text, font, color, pos):
        img = font.render(text, True, color)
        self.screen.blit(img, pos)

    def update(self, main, blit):
        if main:
            bg.mainUpdate(self.screen, self.Player.runVel, self.Player.score, blit)
            if blit:
                self.draw_text(str(int(self.Player.score)), self.small_font, self.black, (1500, 10))
        else:
            bg.mainUpdate(self.screen, 0, self.Player.score, blit)
            self.draw_text("Score : " + str(int(self.Player.score)), self.big_font, self.black, (700, 170))
        if blit:
            self.screen.blit(self.Player.sprite, (20, self.Player.y))
            pygame.display.update()
            self.clock.tick(self.fps)

    def reset(self):
        self.Player = dino.Dino(
            self.start_y, self.start_runVel, self.start_jumpVel, self.start_jumpVelDec
        )
        bg.reset()

    def death(self):
        PRect = self.Player.sprite.get_rect(x=20, y=self.Player.y)
        PRect1 = pygame.Rect(26, self.Player.y, 80, 44)
        PRect2 = pygame.Rect(30, self.Player.y + 44, 37, 55)
        for pos in bg.get_obstacles():
            CRect = pos[2].get_rect(x=pos[0], y=pos[1])
            if self.Player.isCrouch:
                if pygame.Rect.colliderect(PRect, CRect):
                    return True
            elif pygame.Rect.colliderect(PRect1, CRect) or pygame.Rect.colliderect(PRect2, CRect):
                return True
        return False
    
    def noice(self):
        DRect = self.Player.sprite.get_rect(x=20, y=self.Player.y+130)
        URect = self.Player.sprite.get_rect(x=20, y=self.Player.y-100)
        for pos in bg.get_obstacles():
            CRect = pos[2].get_rect(x=pos[0], y=pos[1])
            if pygame.Rect.colliderect(DRect, CRect):
                return 1
            if pygame.Rect.colliderect(URect, CRect):
                return 2
        return 0
    
    def get_state(self):
        obsticles = bg.get_obstacles()
        #obs_width = obsticles[0][2].get_width() if len(obsticles) >= 1 else -100
        findX = 10000   
        for i in obsticles:
            if i[0] >= 20:
                findX = i[0]
                break
        obs_dist = findX
        pplane = 315 - obsticles[0][1] if len(obsticles) >= 1 and obsticles[0][3] == 1 else 0
        obs_gap = obsticles[1][0] - obsticles[0][0] if len(obsticles) >= 2 else 10000  
        return (self.Player.runVel, obs_dist, obs_gap, pplane)

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            state = self.get_state()
            print(state)
            output = net.activate(state)
            action = output.index(max(output))

            match action:
                case 0:
                    self.Player.Crouch(False)
                case 1:
                    self.Player.Crouch(False)
                    self.Player.Jump()
                case 2:
                    self.Player.Crouch(True)
            self.Player.Update()
            self.update(True, True)

            if self.death():
                quit()

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output = net.activate(self.get_state())
            action = output.index(max(output))

            match action:
                case 0:
                    self.Player.Crouch(False)
                case 1:
                    self.Player.Crouch(False)
                    self.Player.Jump()
                case 2:
                    self.Player.Crouch(True)
            genome.fitness += self.noice()
            self.Player.Update()
            self.update(True, False)

            if self.Player.score > 25000 or self.death():
                self.calc_fitness(genome, self.Player.score)
                self.reset()
                break

        #pygame.quit()

    def calc_fitness(self, genome, score):
        genome.fitness += score*0.1

def eval_genomes(genomes, config):
    screen = pygame.display.set_mode((1600, 400))

    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        game = DinoGame(1600, 400, screen)
        game.train_ai(genome, config)

def run_neat(config):
    #pop = neat.Checkpointer.restore_checkpoint('')
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(100))

    technoblade = pop.run(eval_genomes, 500)
    with open("technoblade.pickle", "wb") as f:
        pickle.dump(technoblade, f)

def god_ai(config):
    screen = pygame.display.set_mode((1600, 400))
    with open("technoblade.pickle", "rb") as f:
        technoblade = pickle.load(f)
    
    game = DinoGame(1600, 400, screen)
    game.test_ai(technoblade, config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                         neat.DefaultStagnation, config_path)

    #run_neat(config)
    god_ai(config)