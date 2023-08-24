import pygame
import math
#import os

class Dino:
    def __init__(self, y, runVel, jumpVelStart, jumpVelDecrease):
        #self.dir = os.path.abspath(os.path.dirname( __file__ ))
        self.sinCount = 0
        self.normalSprite = pygame.image.load("player/normal.png")
        self.crouchSprite = pygame.image.load("player/crouch.png")
        self.deathSprite = pygame.image.load("player/death.png")
        self.sprite = self.normalSprite
        self.originalY = y
        self.y = y
        self.isJump = False
        self.isCrouch = False
        self.runVel = runVel
        self.jumpVelStart = jumpVelStart
        self.jumpVelDecrease = jumpVelDecrease
        self.jumpVel = 0
        self.score = 0

    def death(self):
        self.sprite = self.deathSprite
        

    def gas(self):
        self.runVel = min(self.runVel+0.01, 200)
        #print(self.runVel)

    def Jump(self):
        if self.isJump == False and self.isCrouch == False:
            self.isJump = True
            self.jumpVel = self.jumpVelStart
    
    def Crouch(self, isCrouch):
        self.isCrouch = isCrouch
    
    def Update(self):
        self.gas()
        self.sinCount += 0.05
        self.score += self.runVel//20
        if self.isJump:
            self.sprite = self.normalSprite
            self.jumpVel -= self.jumpVelDecrease
            if self.isCrouch:
                self.y += self.jumpVelStart
                self.jumpVel = min(0, self.jumpVel)
            else:
                self.y -= self.jumpVel

            if(self.y > self.originalY + math.sin(self.sinCount)*8):
                self.isJump = False
                self.y = self.originalY + math.sin(self.sinCount)*8
                self.jumpVel = 0

        else:
            if self.isCrouch:
                self.sprite = self.crouchSprite
                #self.y = self.originalY + math.sin(self.sinCount)*8 + 54
            else:
                self.sprite = self.normalSprite
            self.y = self.originalY + math.sin(self.sinCount)*8 + self.isCrouch*54

        