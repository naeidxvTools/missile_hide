import pygame
import sys
import traceback
import myplan
import enemy
from pygame.locals import *
from random import *
from missile import *
from mymap import *
import bullet
import supply
import os


#初始化pygame和混音模块（mixer）
pygame.init()
pygame.mixer.init()

bg_size = width,height = 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")
#background = pygame.image.load("images/background.png").convert()

#创建地图对象
bg1 = MyMap(0,0)
bg2 = MyMap(0,700)
#获得当前路径
path = os.getcwd()
flage = os.path.isfile(path+"\\record.txt")
if not flage:
    file = open(path+"\\record.txt","w")
    file.write(str(0))
    file.close()
    
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
#载入游戏背景音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.3)
#载入游戏音效
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_middle_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.MiddleEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc

#导弹相关
missile = Missile(bg_size,screen)
missile.load(0,0,50)
#用于打印导弹的
missile_group = pygame.sprite.Group()
#用于打印导弹爆炸的
missile_fire = pygame.sprite.Group()
#用于存储总的导弹数量
missile_all = pygame.sprite.Group()
#missile_group.add(missile)
#导弹相关
for i in range(10):
    missile1 = Missile(bg_size,screen)
    missile1.load(randint(0,width),randint(-3*height,0),80)
    missile_all.add(missile1)

#relay = 100 #用于延时
image = None
flag = True

#主程序        
def main():

    me_destroy_index = 0
    en1_destroy_index = 0
    en2_destroy_index = 0
    en3_destroy_index = 0
    #播放游戏背景音效
    pygame.mixer.music.play(-1)#-1为循环播放
    clock = pygame.time.Clock()
    me =myplan.MyPlane(bg_size)
    
    #创建一个数组存放所有的精灵即敌机
    enemies = pygame.sprite.Group()
    #分别创建小中大三个敌机分组
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)
    
    middle_enemies = pygame.sprite.Group()
    add_middle_enemies(middle_enemies,enemies,4)
    
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,2)

    #子弹数组和宏
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    #超级子弹数组和宏
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33,me.rect.centery -50 )))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 33,me.rect.centery -50 )))
    bullets = []

    #超级子弹和炸弹补给;首先实例化
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT#这里USEREVENT是个常量值24
    pygame.time.set_timer(SUPPLY_TIME,30*1000)
    #超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1
    #无敌消息事件
    INVINCIBLE_TIME = USEREVENT + 2
    #标志是否使用子弹
    double_bullet = False
    #已方飞机数量
    me_num = 5
    #加载我方飞机图片
    me_life = pygame.image.load("images/life.png").convert_alpha()
    me_life_rect = me_life.get_rect()
    me_life_rect.left,me_life_rect.top = width-me_life_rect.width,height-me_life_rect.height
    
    #用以标识游戏暂停状态
    pause = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_press_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_press_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left,pause_rect.top = width - pause_rect.width,10
    pause_image = pause_nor_image
    
    #用于计分和字体的定义
    score = 0
    #用于阻止重复打开记录文件
    recorded = False
    #游戏难度初始值
    level = 1
    score_font = pygame.font.Font("font/kaileenw.ttf",33)#个性字体
    #默认字体
    font = pygame.font.get_default_font()
    #score_font = pygame.font.Font(font,33)
    #全屏炸弹的显示定义
    bomb_num = 10
    bomb_font = pygame.font.Font("font/font.ttf",38)
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left,bomb_rect.top = 10,height - bomb_rect.height-10
    #用于延迟
    delay = 100
    running = True
    #用于切换飞机
    plane_flage = True
    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()
    
    while running:
        
        #获得ticks时间，用于miessle对象爆炸更新帧
        ticks = pygame.time.get_ticks()
        bg1.map_update(screen)
        bg2.map_update(screen)
        bg1.map_rolling()
        bg2.map_rolling()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type ==MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    pause = not pause
                    #背景音乐和音效停止
                    if pause:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image = resume_press_image
                    else:
                        pause_image = pause_press_image
                else:
                    if pause:
                        pause_image = resume_nor_image
                    else:
                        pause_image = pause_nor_image
            #全屏爆炸
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        for e in enemies:
                            if e.rect.bottom > 0:
                                e.active = False
                        for m in missile_group:
                            if m.rect.bottom >0:
                                m.active = 2
                                missile_group.remove(m)
                                missile_fire.add(m)
                        
            #自定义的补给消息事件
            elif event.type == USEREVENT:
                supply_sound.play()
                if choice([True,False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME,0)

        if not pause and me_num:

            #检查用户的键盘操作
            key_press = pygame.key.get_pressed()
            if key_press[K_w] or key_press[K_UP]:
                me.moveup()
            if key_press[K_s] or key_press[K_DOWN]:
                me.movedown()
            if key_press[K_a] or key_press[K_LEFT]:
                me.moveleft()
            if key_press[K_d] or key_press[K_RIGHT]:
                me.moveright()

            #绘出炸弹及检测是否得到炸弹
            if bomb_supply.active ==True:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num < 10:
                        bomb_num += 1
                    bomb_supply.active = False
            #绘出超级子弹及检测是否得到超级子弹
            if bullet_supply.active ==True:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    #发谢超级子弹
                    double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,18*1000)
                    bullet_supply.active = False
                
            #延迟处理       
            if not (delay % 5):
                plane_flage = not plane_flage
            if not delay:
                delay = 100
            delay -= 1

            #screen.blit(background,(0,0))
            #绘制大型敌机
            for each in big_enemies:
                if each.active: 
                    each.move()
                    if each.hit:
                        screen.blit(each.image3,each.rect)
                    else:
                        if plane_flage:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)
                    #绘制血槽
                    pygame.draw.lines(screen,BLACK,True,\
                                      [(each.rect.left,each.rect.top-5),\
                                        (each.rect.right,each.rect.top-5)],3)
                    #当血量大于0.2时为绿色小于0.2时显示红色
                    xueliang = each.xcao / enemy.BigEnemy.XCAO
                    if xueliang > 0.2:
                        pygame.draw.lines(screen,GREEN,True,\
                                      [(each.rect.left,each.rect.top-5),\
                                        (each.rect.left + xueliang*each.rect.width,each.rect.top - 5)],3)
                    else:
                        pygame.draw.lines(screen,RED,True,\
                                      [(each.rect.left,each.rect.top-5),\
                                        (each.rect.right ,each.rect.top-5)],3)
                        #大型敌机出现，伴随着音乐
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:#毁灭
                    if not (delay % 5):
                        if en3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[en3_destroy_index],each.rect)
                        en3_destroy_index = (en3_destroy_index+1) % 6
                        if en3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.rest()
                
            
            #绘制中型敌机
            for each in middle_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image1,each.rect)
                    else: 
                        screen.blit(each.image,each.rect)
                else:
                    if not (delay % 5):
                        if en2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[en2_destroy_index],each.rect)
                        en2_destroy_index = (en2_destroy_index+1) % 4
                        if en2_destroy_index == 0:
                            score += 6000
                            each.rest()
                #绘制血槽
                pygame.draw.lines(screen,BLACK,True,\
                                  [(each.rect.left,each.rect.top-5),\
                                    (each.rect.right,each.rect.top-5)],3)
                #当血量大于0.2时为绿色小于0.2时显示红色
                xueliang1 = each.xcao / enemy.MiddleEnemy.XCAO
                if xueliang1 > 0.2:
                    pygame.draw.lines(screen,GREEN,True,\
                                  [(each.rect.left,each.rect.top-5),\
                                    (each.rect.left + xueliang1*each.rect.width,each.rect.top-5)],3)
                else:
                    pygame.draw.lines(screen,RED,True,\
                                      [(each.rect.left,each.rect.top-5),\
                                        (each.rect.right ,each.rect.top-5)],3)
                        
            #绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)    
                else:#
                    if not (delay % 5):
                        if en1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[en1_destroy_index],each.rect)
                        en1_destroy_index = (en1_destroy_index+1) % 4
                        if en1_destroy_index == 0:
                            #加分
                            score += 1000
                            each.rest()
            #增加难度
            
            if score > 10000 and level == 1:
                level = 2

                i = 0
                for each in missile_all:
                    i += 1
                    each.rest()
                    missile_group.add(each)
                    if i == 5:
                        break
                        """

                for i in range(level):
                    missile1 = Missile(bg_size,screen)
                    missile1.load(randint(0,width),randint(-3*height,0),80)
                    missile_group.add(missile1)"""
                    
                add_small_enemies(small_enemies,enemies,3)
                add_middle_enemies(middle_enemies,enemies,2)
                add_big_enemies(big_enemies,enemies,1)
                #inc_speed(small_enemies,1)
            elif score > 30000 and level == 2:
                level = 3
                i = 0
                for each in missile_all:
                    i += 1
                    each.rest()
                    missile_group.add(each)
                    if i == 6:
                        break
                """
                for i in range(level):
                    missile1 = Missile(bg_size,screen)
                    missile1.load(randint(0,width),randint(-3*height,0),80)
                    missile_group.add(missile1)"""
                    
                add_small_enemies(small_enemies,enemies,5)
                add_middle_enemies(middle_enemies,enemies,3)
                add_big_enemies(big_enemies,enemies,2)
                #inc_speed(small_enemies,1)
                #inc_speed(middle_enemies,1)
            elif score > 60000 and level == 3:
                level = 4
                i = 0
                for each in missile_all:
                    i += 1
                    each.rest()
                    missile_group.add(each)
                    if i == 7:
                        break
                    
                add_small_enemies(small_enemies,enemies,5)
                add_middle_enemies(middle_enemies,enemies,3)
                add_big_enemies(big_enemies,enemies,2)
                #inc_speed(small_enemies,1)
                #inc_speed(middle_enemies,1)
                #inc_speed(big_enemies,1)
            elif score > 100000 and level == 4:
                level = 5
                i = 0
                for each in missile_all:
                    i += 1
                    each.rest()
                    missile_group.add(each)
                    if i == 8:
                        break
                    
                add_small_enemies(small_enemies,enemies,5)
                add_middle_enemies(middle_enemies,enemies,3)
                add_big_enemies(big_enemies,enemies,2)
                #inc_speed(small_enemies,1)
                #inc_speed(middle_enemies,1)
                #inc_speed(big_enemies,1)
            elif score > 150000 and level == 5:
                level = 6
                i = 0
                for each in missile_all:
                    i += 1
                    each.rest()
                    missile_group.add(each)
                    if i == 9:
                        break
                    
                add_small_enemies(small_enemies,enemies,5)
                add_middle_enemies(middle_enemies,enemies,3)
                add_big_enemies(big_enemies,enemies,2)
                inc_speed(small_enemies,1)
                inc_speed(middle_enemies,1)
                inc_speed(big_enemies,1)
                
            if delay % 3 == 0:
                image = missile.image1
            elif delay % 3 == 1:
                image = missile.image2
            elif delay % 3 == 2:
                image = missile.image3
            missile_group.update(me.rect.centerx,me.rect.centery,image,ticks)

            #检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
               me.active = False
               for each in enemies_down:
                   each.active =False
            enemies_down = []
            
            #print("后",len(missile_group))
                
            #转换成surface并绘制得分
            score_text = score_font.render("score %s" % str(score),True,WHITE)
            screen.blit(score_text,(5,5))
            #绘制我方飞机
            if me.active:
                if plane_flage :
                    screen.blit(me.image1,me.rect)
                else:
                    screen.blit(me.image2,me.rect)
            else:
                #飞机毁灭
                if not (delay % 6):#6次循环进入一次
                    me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index],each.rect)
                    me_destroy_index = (me_destroy_index+1) % 4
                    #print("外",me_destroy_index)
                    if (me_destroy_index == 0):#24次循环进入一次能过6次*4得来的
                        #print("1")
                        me_num -= 1
                        me.rest()
                        pygame.time.set_timer(INVINCIBLE_TIME,3*1000)
                        



            #绘制和移动子弹相关：
            #这个条件分支下只负责每颗子弹的初始位置便于下面移动后画出来
            if not (delay % 10 ):
                bullet_sound.play()
                if double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33,me.rect.centery - 50))
                    bullets[bullet2_index+1].reset((me.rect.centerx + 33,me.rect.centery - 50))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM

                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            for b in bullets:
                if b.active and me.active:
                    b.move()#移动后并输出屏幕上
                    screen.blit(b.image,b.rect)
                    #碰撞检测mask非透明图层检测
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,\
                                pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in middle_enemies or e in big_enemies:
                                e.hit = True
                                e.xcao -= 1
                                if e.xcao == 0:
                                    e.active = False
                            else:
                                e.active = False
            #检测导弹是否被子弹击中
            for b in bullets:
                missile_hit = pygame.sprite.spritecollide(b,missile_group,False,\
                                pygame.sprite.collide_mask)
                if missile_hit:
                    b.active = False
                    for m in missile_hit:
                        m.active = 2
                        missile_group.remove(m)
                        missile_fire.add(m)
            missile_hit = []
            #检查我方飞机是否被导弹击中
            enemies_missile = pygame.sprite.spritecollide(me,missile_group,False,pygame.sprite.collide_mask)
            if enemies_missile:
                for each in enemies_missile:
                    each.active =2
                    missile_group.remove(each)
                    missile_fire.add(each)
                
                
            if enemies_missile and not me.invincible:
               me.active = False
               
                   
            enemies_missile = []
            if missile_group:
                
                missile_group.draw(screen)
                
            if missile_fire:
                for each in missile_fire:
                    if each.active == 3:
                        missile_fire.remove(each)

            missile_fire.update(0,0,image,ticks)
            
            plane_flage = not plane_flage
            #绘制全屏炸弹图标
            bomb_text = bomb_font.render("×%d" % bomb_num,True,WHITE)
            screen.blit(bomb_image,bomb_rect)
            screen.blit(bomb_text,(bomb_rect.right + 5,bomb_rect.top + 5))
            #绘制我方表示生命的飞机
            for m in range(me_num):
                screen.blit(me_life,((width - me_life_rect.width*(m+1)),height - me_life_rect.height))

        elif not me_num:
            #running = False
            #背景音乐和音效停止
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            #停止发放补给
            pygame.time.set_timer(SUPPLY_TIME,0)
            if not recorded:
                recorded = True
                #读取历史最高分
                with open("record.txt","r") as f:
                    record_score = int(f.read())
                #判断如果不是最高分则存档
                if score > record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
            #绘制结束画面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                             (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                             (width - gameover_text2_rect.width) // 2, \
                             gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)
            again_rect.left, again_rect.top = \
                         (width - again_rect.width) // 2, \
                         gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                            (width - again_rect.width) // 2, \
                            again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                    #running = True
                # 如果用户点击“结束游戏”            
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()    

        #绘制暂停按钮
        screen.blit(pause_image,pause_rect)                
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
