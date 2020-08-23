import pygame

#定义一个滚动地图类
class MyMap(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.bg = pygame.image.load("images/background.png").convert_alpha()
    def map_rolling(self):
        if self.y < -695:
            self.y = 695
        else:
            self.y -=3
    def map_update(self,screen):
        screen.blit(self.bg, (self.x,self.y))
    def set_pos(x,y):
        self.x =x
        self.y =y
