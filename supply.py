import pygame
from random import *

class Bullet_Supply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size
        self.rect.left,self.rect.bottom = randint(0,self.width-self.rect.width),-100
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.height:
            self.rect.bottom += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left,self.rect.bottom = randint(0,self.width-self.rect.width),-100

class Bomb_Supply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bomb_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size
        self.rect.left,self.rect.bottom = randint(0,self.width-self.rect.width),-100
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.bottom < self.height:
            self.rect.bottom += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left,self.rect.bottom = randint(0,self.width-self.rect.width),-100
