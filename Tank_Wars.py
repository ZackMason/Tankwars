# Programmer: Zackery C. Mason-Blaug
# Date: 2/17/2013
# Title: Tank Wars

import sys
import pygame
import random
import math
from pygame.locals import *

class ZSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y , dx, dy, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image0 = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rotation = 0
        self.angle = angle
        self.rect.topleft = [ self.x, self.y ]

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = [ self.x, self.y ]
        self.angle += self.rotation
        self.image = pygame.transform.rotate(self.image0, self.angle)

class Tank(ZSprite):
    def __init__(self, filename, x, y, dx, dy, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image0 = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.health = 50
        self.rotation = 0
        self.angle = angle
        self.rect.topleft = [ self.x, self.y ]
        self.s = 0
        self.reload = 1

    def update(self):
        theta = math.radians(self.angle)
        self.dx = - self.s * math.sin(theta)
        self.dy = - self.s * math.cos(theta)
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.topleft = [ self.x, self.y ]
        self.angle += self.rotation
        self.image = pygame.transform.rotate(self.image0, self.angle)

    def Fire(self, kind):
        s = 20
        if kind == 2:
            s = 10
        theta = math.radians(self.angle)
        dx = - s * math.sin(theta)
        dy = - s * math.cos(theta)
        if kind == 1:
            missile = missiles.add(ZSprite('tmissile.png', self.x + 14, self.y + 28 , dx, dy, self.angle))
        if kind == 2:
            strMissiles.add(ZSprite('tmissile.png', self.x + 14, self.y + 28, dx ,dy, self.angle))

class Tank1(ZSprite):
    def __init__(self, filename, x, y, dx, dy, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image0 = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.health = 50
        self.rotation = 0
        self.angle = angle
        self.rect.topleft = [ self.x, self.y ]
        self.s = 0
        self.reload = 1

    def update(self):
        theta = math.radians(self.angle)
        self.dx = - self.s * math.sin(theta)
        self.dy = - self.s * math.cos(theta)
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.topleft = [ self.x, self.y ]
        self.angle += self.rotation
        self.image = pygame.transform.rotate(self.image0, self.angle)

    def Fire(self, kind):
        s = 20
        if kind == 2:
            s = 10
        theta = math.radians(self.angle)
        dx =  s * math.sin(theta)
        dy =  s * math.cos(theta)
        if kind == 1:
            badMissiles.add(ZSprite('tmissile2.png', self.x + 14, self.y + 28 , dx, dy, self.angle))
        if kind == 2:
           strMissiles2.add(ZSprite('tmissile2.png', self.x + 14, self.y + 28, dx, dy, self.angle))
        
class ZPower(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, power):
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = [ self.x, self.y ]
        self.power = power


class ZSurface(pygame.Surface):
    def __init__(self, filename, x, y, dx, dy):
        pygame.Surface.__init__(self, (54, 30))
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.rect.topleft = [ self.x, self.y ]

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = [ self.x, self.y ]


TEXTCOLOR = (225, 0, 0)

textColor = (0, 0, 225)

def drawText(text, font, surface,x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def drawText2(text, font, surface,x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def cleanUp(missiles):
    if missile.y < -100:
        missiles.remove(missile)
        missile.kill()
    if missile.y > 700:
        missiles.remove(missile)
        missile.kill()
    if missile.x < -100:
        missiles.remove(missile)
        missile.kill()
    if missile.x > 1100:
        missiles.remove(missile)
        missile.kill()

def restart():
    tank.health = 50
    badTank.health = 50
    tank.x, tank.y = 500, 500
    badTank.x, badTank.y = 200, 200
    badTank.angle = 0
    tank.angle = 0
    tankMines = 4
    badTankMines = 4
    for mine in mines:
        mines.remove(mine)
        mine.kill()
    for mine in mines1:
        mines1.remove(mine)
        mine.kill()

pygame.display.set_caption('Tank Wars')

GREEN = (0,225,0)
FPS = 30
fpsClock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode([1040, 640])

missiles = pygame.sprite.Group()
missiles2 = pygame.sprite.Group()
badMissiles = pygame.sprite.Group()
badMissiles2 = pygame.sprite.Group()
strMissiles = pygame.sprite.Group()
strMissiles2 = pygame.sprite.Group()
mines = pygame.sprite.Group()
mines1 = pygame.sprite.Group()
blocks = pygame.sprite.Group()

powerUps = pygame.sprite.Group()
powerTime = 0
powers = 0

tank = Tank('tank.png', 500, 500, 0, 0, 0)
tankMines = 4
badTank = Tank1('tank2.png', 100, 100, 0 ,0, 0)
badTankMines = 4

blocks.add(ZSprite('sandbag.png', 300, 400, 0, 0, 0))
blocks.add(ZSprite('sandbag.png', 800, 200, 0, 0, 0))


font = pygame.font.SysFont(None, 48)
font.size(' ')

firing = 0
fireTime = 0
firing2 = 0
fireTime2 = 0
red = (255,0,0)
a = 1
b = 0

pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    if pygame.joystick.Joystick(0).get_name() == 'Controller (Rock Candy Gamepad for Xbox 360)':
        joy1 = pygame.joystick.Joystick(0)
        joy1.init()
        print "player RED: Blue Controller"
    if pygame.joystick.Joystick(0).get_name() == 'Controller (Afterglow Gamepad for Xbox 360)':
        joy2 = pygame.joystick.Joystick(0)
        joy2.init()
        print "Player RED: Clear Controller"
    
if pygame.joystick.get_count() > 1:  
    if pygame.joystick.Joystick(1).get_name() == 'Controller (Afterglow Gamepad for Xbox 360)':
        joy2 = pygame.joystick.Joystick(1)
        joy2.init()
        print "Player BLUE: Clear Controller"
    if pygame.joystick.Joystick(1).get_name() == 'Controller (Rock Candy Gamepad for Xbox 360)':
        joy1 = pygame.joystick.Joystick(1)
        joy1.init()
        print "Player BLUE: Blue Controller"

print('HOW TO PLAY \n Red Player: \n Moving: WASD \n Firing:\n M = machine gun = .5 dmg \n n = normal missile = 1 dmg \n b = slow missile = 3 dmg \n h = mine = 5 dmg')
print('HOW TO PLAY \n Blue Player: \n Moving: Arrow keys \n Firing:\n 3 = machine gun = .5 dmg \n 2 = normal missile = 1 dmg \n 1 = slow missile = 3 dmg \n 4 = mine = 5 dmg')

while a == 1:
    menu = ZSurface('StartTank.png', 0, 0, 0, 0)
    if b == 1:
        screen.blit(controlls.image, controlls.rect)
    if b == 0:
        screen.blit(menu.image, menu.rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            break

        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                a = 0
                break
            elif event.key == K_RSHIFT:
                controlls = ZSurface('Controlls.png', 0, 0, 0, 0)
                b = 1
    

while True:
    screen.fill(GREEN)
    keyPressed = False
    
    death = None
    death2 = None
    TH = tank.health
    BTH = badTank.health
    turn = False
    
    if badTank.health <= 0:
        BTH = 'Dead'
        
    if tank.health <= 0:
        TH = "Dead"

    for block in blocks:
        screen.blit(block.image, block.rect)

    for mine in mines:
        screen.blit(mine.image, mine.rect)
        mine.update()

    for mine in mines1:
        screen.blit(mine.image, mine.rect)
        mine.update()
        
    for powerUp in powerUps:
        screen.blit(powerUp.image, powerUp.rect)

    screen.blit(tank.image, tank.rect)
    screen.blit(badTank.image, badTank.rect)
    
    for missile in missiles:
        missile.update()
        screen.blit(missile.image, missile.rect)
        cleanUp(missiles)
                        
    for missile in missiles2:
        missile.update()
        screen.blit(missile.image, missile.rect)
        cleanUp(missiles)
            
    for missile in badMissiles:
        missile.update()
        screen.blit(missile.image, missile.rect)
        cleanUp(missiles)
            
    for missile in badMissiles2:
        missile.update()
        screen.blit(missile.image, missile.rect)
        cleanUp(missiles)

    for missile in strMissiles:
        missile.update()
        screen.blit(missile.image, missile.rect)
        cleanUp(missiles)
            
    for missile in strMissiles2:
        missile.update()
        screen.blit(missile.image, missile.rect)
        cleanUp(missiles)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            break

        elif event.type == KEYDOWN:
            keyPressed = True
            if event.key == K_w:
                tank.s = 10
                
            elif event.key == K_ESCAPE:
                pygame.quit()
                break

            elif event.key == K_s:
                tank.s = -10

            elif event.key == K_a:
                tank.rotation = 5
                if event.key == K_d:
                    tank.rotation = -5
                
            elif event.key == K_d:
                tank.rotation = -5
                if event.key == K_a:
                    tank.rotation = 5

            elif event.key == K_UP:
                badTank.s = -10

            elif event.key == K_DOWN:
                badTank.s = 10

            elif event.key == K_RIGHT:
                badTank.rotation = -5

            elif event.key == K_LEFT:
                badTank.rotation = 5

            elif event.key == K_n:
                tank.Fire(1)
                
            elif event.key == K_b:
                tank.Fire(2)

            elif event.key == K_m:
                firing2 = 1

            elif event.key == K_h:
                if tankMines > 0:
                    mines.add(ZSprite('landmine.png', tank.x, tank.y, 0 ,0, 0))
                    tankMines -= 1
                else:
                    continue
                
            elif event.key == K_KP2:
                badTank.Fire(1)

            elif event.key == K_KP1:
                badTank.Fire(2)
                
            elif event.key == K_KP3:
                firing = 1

            elif event.key == K_KP4:
                if badTankMines > 0:
                    mines1.add(ZSprite('landmine.png', badTank.x, badTank.y, 0, 0,0))
                    badTankMines -= 1
                else:
                    continue
                
            elif event.key == K_o:
                restart()
                tankMines = 4
                badTankMines = 4

            elif event.key == K_i:
                tank.x, tank.y = 500, 500
                badTank.x, badTank.y = 200, 200 

        elif event.type == KEYUP:
            if event.key == K_w:
                tank.dy = 0
                tank.dx = 0
                tank.s = 0
                
            elif event.key == K_s:
                tank.s = 0

            elif event.key == K_d:
                tank.rotation = 0

            elif event.key == K_a:
                tank.rotation = 0

            elif event.key == K_UP:
                badTank.s = 0

            elif event.key == K_DOWN:
                badTank.s = 0

            elif event.key == K_RIGHT:
                badTank.rotation = 0

            elif event.key == K_LEFT:
                badTank.rotation = 0

            elif event.key == K_KP3:
                firing = 0

            elif event.key == K_m:
                firing2 = 0

        if pygame.joystick.get_count() > 0:
            if event.type == pygame.locals.JOYBUTTONDOWN:
                if joy1.get_button(5):
                    tank.Fire(1)

                if joy1.get_button(4):
                    tank.Fire(2)

                if joy1.get_button(0):
                    firing2 = 1

                if joy1.get_button(1):
                    if tankMines > 0:
                        if tank.reload == 1:
                            mines.add(ZSprite('landmine.png', tank.x, tank.y, 0 ,0, 0))
                            tankMines -= 1
                            tank.reload = 0
                        else:
                            continue
                    else:
                        continue

                if joy1.get_button(7):
                    restart()
                    tankMines = 4
                    badTankMines = 4

                if joy1.get_button(6):
                    tank.health = 500
                    badTank.health = 500

            elif event.type == pygame.locals.JOYBUTTONUP:
                if joy1.get_button(0) == False:
                    firing2 = 0

                if joy1.get_button(1) == False:
                    tank.reload = 1

            elif event.type == pygame.locals.JOYAXISMOTION:
                if abs(joy1.get_axis(1)) > 0.3:
                    tank.s = joy1.get_axis(1) * -10
                else:
                    tank.s = 0
                if abs(joy1.get_axis(4)) > .2:
                    tank.rotation = joy1.get_axis(4) * -5
                else:
                    tank.rotation = 0

            elif event.type == pygame.locals.JOYHATMOTION:
                if joy1.get_hat == (0, -1):
                    tank.x, tank.y = 500, 500
                    badTank.x, badTank.y = 200, 200
                    print 'fail'
                    

        if pygame.joystick.get_count() > 1:
            if event.type == pygame.locals.JOYBUTTONDOWN:
                if joy2.get_button(5):
                    badTank.Fire(1)

                if joy2.get_button(4):
                    badTank.Fire(2)

                if joy2.get_button(0):
                    firing = 1

                if joy2.get_button(1):
                    if badTankMines > 0:
                        if badTank.reload == 1:
                            mines1.add(ZSprite('landmine.png', badTank.x, badTank.y, 0, 0,0))
                            badTankMines -= 1
                            badTank.reload = 0
                        else:
                            continue
                    else:
                        continue

            elif event.type == pygame.locals.JOYBUTTONUP:    
                if joy2.get_button(0) == False:
                    firing = 0

                if joy2.get_button(1) == False:
                    badTank.reload = 1
                    

            elif event.type == pygame.locals.JOYAXISMOTION:
                if joy2.get_axis(1) < -0.2:
                    badTank.s = -10
                elif joy2.get_axis(1) > 0:
                    badTank.s = 10
                else:
                    badTank.s = 0
                if abs(joy2.get_axis(4)) > .2:
                    badTank.rotation = joy2.get_axis(4) * -5
                else:
                    badTank.rotation = 0
            
            

                
        ''' Configuring controls:
        xbox:
            axis 1 = left vertical
            axis 4 = right horizantal
            axis 2 = triggers
            button 4 = left bumper
            button 5 = right bumper

        airflo:
            axis 1 = left vertical
            axis 3 = right horizantal
            button 6 = right trgger
            button 7 = left trigger
        '''

    collision = pygame.sprite.spritecollide(tank, badMissiles, True)
    collision2 = pygame.sprite.spritecollide(badTank, missiles, True)
    collision3 = pygame.sprite.spritecollide(tank, badMissiles2, True)
    collision4 = pygame.sprite.spritecollide(badTank, missiles2, True)
    collision0 = pygame.sprite.spritecollide(badTank, strMissiles, True)
    collision00 = pygame.sprite.spritecollide(tank, strMissiles2, True)
    collision5 = pygame.sprite.spritecollide(tank, powerUps, True)
    collision6 = pygame.sprite.spritecollide(badTank, powerUps, True)
    collision7 = pygame.sprite.spritecollide(tank, mines1, True)
    collision8 = pygame.sprite.spritecollide(badTank, mines, True)
    pygame.sprite.groupcollide(blocks ,missiles, False, True)
    pygame.sprite.groupcollide(blocks ,missiles2, False, True)
    pygame.sprite.groupcollide(blocks ,badMissiles, False, True)
    pygame.sprite.groupcollide(blocks ,badMissiles2, False, True)
    pygame.sprite.groupcollide(blocks ,strMissiles, False, True)
    pygame.sprite.groupcollide(blocks ,strMissiles2, False, True)
    pygame.sprite.groupcollide(missiles,powerUps, False, True)

    drawText('Red Player: %s Red Mines: %s' % (TH,tankMines), font, screen,10,0)
    drawText2('Blue Player: %s Blue Mines: %s' % (BTH, badTankMines), font, screen, 10, 30)
    drawText('%s' % (TH), font, screen, tank.x, tank.y+60)
    drawText2('%s' % (BTH), font, screen, badTank.x, badTank.y+60)
    


    
    if len(collision) >= 1:
        tank.health -= 1
        collision = 0

    if len(collision2) >= 1:
        badTank.health -= 1
        collision2 = 0

    if len(collision3) >= 1:
        tank.health -= .50
        collision = 0
        
    if len(collision4) >= 1:
        badTank.health -= .50
        collision2 = 0
        
    if len(collision0) >= 1:
        badTank.health -= 3
        collision0 = 0
        
    if len(collision00) >=1:
        tank.health -= 3
        collision00 = 0

    if len(collision5) >= 1:
        tank.health += 5
        powers -= 1
        collision5 = 0

    if len(collision6) >= 1:
        badTank.health += 5
        powers -= 1
        collision6 = 0

    if len(collision7) >= 1:
        tank.health -= 5
        badTankMines += 1
        collision7 = 0

    if len(collision8) >= 1:
        badTank.health -= 5
        tankMines += 1
        collision8 = 0
        
    if tank.health <= 0 and death is None:
        death = ZSurface('fire.png', tank.x, tank.y, 0,0)
        tank.x , tank.y = -700, -700
        
    if death != None:
        screen.blit(death.image, death.rect)
        
        
    if badTank.health <= 0.0 and death2 is None:
        death2 = ZSurface('fire.png', badTank.x - 10, badTank.y - 20, 0,0)
        badTank.x, badTank.y = -700, -700
        #badTank.kill()

    if death2 != None:
        screen.blit(death2.image, death2.rect)

    if firing == 1:
        if pygame.time.get_ticks() - fireTime > 35:
            s = 20
            theta = math.radians(badTank.angle)
            dx = s * math.sin(theta)
            dy = s * math.cos(theta)
            badMissiles2.add(ZSprite('bullet2.png', badTank.x + 14, badTank.y + 28, dx ,dy, badTank.angle))
            fireTime = pygame.time.get_ticks()

    if firing2 == 1:
        if pygame.time.get_ticks() - fireTime2 > 35:
            s = 20
            theta = math.radians(tank.angle)
            dx = - s * math.sin(theta)
            dy = - s * math.cos(theta)
            missiles2.add(ZSprite('bullet.png', tank.x + 14, tank.y + 28, dx ,dy, tank.angle))
            fireTime2 = pygame.time.get_ticks()

    if pygame.time.get_ticks() - powerTime > 20000:
        if powers == 0:
            powers += 1
            powerUps.add(ZSprite('health.png', random.randint(100,1000), random.randint(0,600), 0,0,0))
        powerTime = pygame.time.get_ticks()
        
        
    pygame.display.update()
    fpsClock.tick(FPS)

    tank.update()
    badTank.update()

