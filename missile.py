import pygame
from math import *
from random import *


class Missile(pygame.sprite.Sprite):#需要变向的精灵类
    def __init__(self,bg_size,screen):
        pygame.sprite.Sprite.__init__(self)

        self.invincible = False
        self.active = 1
        self.image = None
        self.remove = False
        self.pos = []
        self.x1,self.y1 = 0,0
        self.velocity = 0
        self.time = 1/10
        self.missiled = None
        self.distance = None
        self.A = ()
        self.B = ()
        self.C = ()
        self.rect =0,0
        self.mask = None
        self.screen = screen
        self.width,self.height = bg_size[0],bg_size[1]

        #self.mask = pygame.mask.from_surface(self.image1)

    def load(self,x,y,speed):#(x,y)是原始出发点

        self.x1,self.y1 = (x,y)
        self.velocity = speed
        self.image1 = pygame.image.load("element/m1.png").convert_alpha()
        self.image2 = pygame.image.load("element/m2.png").convert_alpha()
        self.image3 = pygame.image.load("element/m3.png").convert_alpha()
        #生成爆炸对象
        self.blast = MySprite(self.screen)
        self.blast.load("element\mm.png", 128, 128, 6)
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.w,self.h = self.rect.width ,self.rect.height

    def update(self,x,y,image,ticks):
        #1表示导弹正常飞行状态
        if self.active == 1:
            self.pos =[]
            #x1,y1 = self.x1,self.y1
            self.image = None
            self.distance=sqrt(pow(self.x1-x,2)+pow(self.y1-y,2))      #两点距离公式
            section=self.velocity*self.time               #每个时间片需要移动的距离
            sina=(self.y1-y)/self.distance
            cosa=(x-self.x1)/self.distance
            angle=atan2(y-self.y1,x-self.x1)              #两点间线段的弧度值
            fangle=degrees(angle)               #弧度转角度
            self.x1,self.y1=(self.x1+section*cosa,self.y1-section*sina)
            self.missiled=pygame.transform.rotate(image,-(fangle))
            
            if 0<=-fangle<=90:
                self.A=(self.w*cosa+self.x1-self.w,self.y1-self.h/2)        
                self.B=(self.A[0]+self.h*sina,self.A[1]+self.h*cosa)

            if 90<-fangle<=180:
                self.A = (self.x1 - self.w, self.y1 - self.h/2+self.h*(-cosa))
                self.B = (self.x1 - self.w+self.h*sina, self.y1 - self.h/2)

            if -90<=-fangle<0:
                self.A = (self.x1 - self.w+self.missiled.get_width(), self.y1 - self.h/2+self.missiled.get_height()-self.h*cosa)
                self.B = (self.A[0]+self.h*sina, self.y1 - self.h/2+self.missiled.get_height())

            if -180<-fangle<-90:
                self.A = (self.x1-self.w-self.h*sina, self.y1 - self.h/2+self.missiled.get_height())
                self.B = (self.x1 - self.w,self.A[1]+self.h*cosa )
            
            self.C = ((self.A[0] + self.B[0]) / 2, (self.A[1] + self.B[1]) / 2)
            self.pos=((self.x1-self.w+(self.x1-self.C[0])),(self.y1-self.h/2+(self.y1-self.C[1])))
            self.rect.left,self.rect.top = self.pos
            self.image = self.missiled
            self.mask = pygame.mask.from_surface(self.image)
        #2表示导弹毁灭过程，更新爆炸图片
        elif self.active == 2:
            
            self.blast.update(ticks)
            self.screen.blit(self.blast.image,self.rect)
            
        #下面当爆炸对象更新完一遍后退出更新爆炸图片
        if self.blast.frame == 29:
                self.active = 3

    def rest(self):
        self.active = 1
        self.blast.frame = 0
        self.x1,self.y1 = randint(0,self.width - self.rect.width),\
                                       randint(-3*self.height,0)

                
class MySprite(pygame.sprite.Sprite):#序列精灵图类
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        
        self.frame = -1
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = 200,200,width,height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=60):
        
        #如果时间过去了rate这么多时间就怎样：
        if current_time > self.last_time + rate:
            #print( self.last_time + rate)
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            #用%取余数对每一行的每桢遍历；有//整除取整实现对整行的固定次的停留。
            #相当于先取余遍历，再取整对每行的遍历
            frame_x = (self.frame % self.columns) * self.frame_width
            #print("frame_x", frame_x,"=",("self.frame",self.frame ,"%","self.columns", self.columns), "*", "self.frame_width",self.frame_width)
            frame_y = (self.frame // self.columns) * self.frame_height
            #print("frame_x:",frame_x,",","frame_y:",frame_y)
            rect = ( frame_x, frame_y, self.frame_width, self.frame_height )

            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

