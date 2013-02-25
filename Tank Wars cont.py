# Programmer: Zackery C. Mason-Blaug
# Date: 2/17/2013
# Title: Tank Wars

import sys
import pygame
import random
from pygame.locals import *

class ZSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image0 = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.angle = 0
        self.rect.topleft = [ self.x, self.y ]

    def update(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.topleft = [ self.x, self.y ]
        self.image = pygame.transform.rotate(self.image0, self.angle)

class ZTank(pygame.sprite.Sprite):
    tankTurnSpeed = 8
    maxRotate = 360
    tankRotateLeft = False
    tankRotateRight = False
    def __init__(self, filename, x, y, dx, dy, angle=0):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(filename).convert_alpha()
        self.tankAngle = angle
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()
        self.tankturndirection = 0
        self.tankTurnSpeed = ZTank.tankTurnSpeed

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = [ self.x, self.y ]

        self.tankturndirection = 0
        if self.tankRotateLeft == True:
            self.tankturndirection += 1
        if self.tankRotateRight == True:
            self.tankturndirection -= 1

        self.tankAngle += self.tankturndirection * self.tankTurnSpeed

        oldcenter = self.rect.center
        oldrect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        

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

def lockOn(ZSprite, ZSprite1 , ZSprite2):
    xx = ZSprite.x
    yy = ZSprite.y 
    xx2 = ZSprite1.x
    yy2 = ZSprite1.y
    m = yy - yy2
    m2 = xx - xx2
    m3 = m + m2
    
    if m3 == 0:
        return
    print(str(m) +'+ '+ str(m2)+' ='+str(m3))
    m4 = int((m3)/1)
    print(m4)
    ZSprite2.dx = m2 / m3 * 20
    ZSprite2.dy = m / m3 * 20
    if m <= 0:
        ZSprite2.dy *= -1
    if m2 <= 0:
        ZSprite2.dx *= -1
    
    # coordinates are q4

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

    
pygame.display.set_caption('Tank Wars')

GREEN = (0,225,0)
FPS = 30
fpsClock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode([1040, 640])

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

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

tank = ZSprite('tank.png', 500, 500, 0, 0)
tankHealth = 50
tankMines = 4
badTank = ZSprite('tank2.png', 100, 100, 0 ,0)
badTankHealth = 50
badTankMines = 4

blocks.add(ZSprite('sandbag.png', 300, 400, 0, 0))
blocks.add(ZSprite('sandbag.png', 800, 200, 0, 0))

font = pygame.font.SysFont(None, 48)

firing = 0
fireTime = 0
firing2 = 0
fireTime2 = 0
red = (255,0,0)


while True:
    screen.fill(GREEN)
    keyPressed = False
    screen.blit(tank.image, tank.rect)
    screen.blit(badTank.image, badTank.rect)
    death = None
    death2 = None
    TH = tankHealth
    BTH = badTankHealth
    turn = False
    
    if badTankHealth <= 0:
        BTH = 'Dead'
        
    if tankHealth <= 0:
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

    for missile in missiles:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y < -100:
            missiles.remove(missile)
            missile.kill()
                        
    for missile in missiles2:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y < -100:
            missiles.remove(missile)
            missile.kill()

    for missile in badMissiles:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y > 1020:
            missiles.remove(missile)
            missile.kill()

    for missile in badMissiles2:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y > 1020:
            missiles.remove(missile)
            missile.kill()

    for missile in strMissiles:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y < -100:
            missiles.remove(missile)
            missile.kill()
            
    for missile in strMissiles2:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y > 1020:
            missiles.remove(missile)
            missile.kill()
    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            keyPressed = True
            if event.key == K_w:
                tank.dy = -10

            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == K_s:
                tank.dy = 10

            elif event.key == K_e:
                #tank.angle += 10
                turn = True
                
            elif event.key == K_q:
                tank.angle -= 10

            elif event.key == K_d:
                tank.dx = 10

            elif event.key == K_a:
                tank.dx = -10

            elif event.key == K_UP:
                badTank.dy = -10

            elif event.key == K_DOWN:
                badTank.dy = 10

            elif event.key == K_RIGHT:
                badTank.dx = 10

            elif event.key == K_LEFT:
                badTank.dx = -10

            elif event.key == K_n:
                missiles.add(ZSprite('tmissile.png', tank.x + 14, tank.y, 0 ,-20))

            elif event.key == K_y:
                strMissiles.add(ZSprite('tmissile.png', tank.x + 14, tank.y, 0 ,-5))

            elif event.key == K_m:
                firing2 = 1

            elif event.key == K_b:
                if tankMines > 0:
                    mines.add(ZSprite('landmine.png', tank.x, tank.y, 0 ,0))
                    tankMines -= 1
                else:
                    continue
                
            elif event.key == K_KP2:
                badMissiles.add(ZSprite('tmissile2.png', badTank.x + 14, badTank.y + 50, 0 ,20))

            elif event.key == K_KP7:
                strMissiles2.add(ZSprite('tmissile2.png', badTank.x + 14, badTank.y + 50, 0 ,5))

            elif event.key == K_KP3:
                firing = 1

            elif event.key == K_KP1:
                if badTankMines > 0:
                    mines1.add(ZSprite('landmine.png', badTank.x, badTank.y, 0, 0))
                    badTankMines -= 1
                else:
                    continue
                
            elif event.key == K_o:
                tankHealth = 50
                badTankHealth = 50
                tank.x, tank.y = 500, 500
                badTank.x, badTank.y = 200, 200
                tankMines = 4
                badTankMines = 4
                for mine in mines:
                    mines.remove(mine)
                    mine.kill()
                for mine in mines1:
                    mines1.remove(mine)
                    mine.kill()

            elif event.key == K_u:
                missiles.add(ZSprite('tmissile.png', tank.x + 14, tank.y, 0 ,-20))
                lockOn(tank, badTank, missiles)

            elif event.key == K_i:
                tank.x, tank.y = 500, 500
                badTank.x, badTank.y = 200, 200 

        elif event.type == KEYUP:
            if event.key == K_w:
                tank.dy = 0

            elif event.key == K_s:
                tank.dy = 0

            elif event.key == K_a:
                tank.dx = 0

            elif event.key == K_d:
                tank.dx = 0

            elif event.key == K_UP:
                badTank.dy = 0

            elif event.key == K_DOWN:
                badTank.dy = 0

            elif event.key == K_RIGHT:
                badTank.dx = 0

            elif event.key == K_LEFT:
                badTank.dx = 0

            elif event.key == K_KP3:
                firing = 0

            elif event.key == K_m:
                firing2 = 0

    if turn == True:
        tank.angle += 10


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



    
    if len(collision) >= 1:
        tankHealth -= 1
        collision = 0

    if len(collision2) >= 1:
        badTankHealth -= 1
        collision2 = 0

    if len(collision3) >= 1:
        tankHealth -= .50
        collision = 0
        
    if len(collision4) >= 1:
        badTankHealth -= .50
        collision2 = 0
        
    if len(collision0) >= 1:
        badTankHealth -= 3
        collision0 = 0
        
    if len(collision00) >=1:
        tankHealth -= 3
        collision00 = 0

    if len(collision5) >= 1:
        tankHealth += 5
        powers -= 1
        collision5 = 0

    if len(collision6) >= 1:
        badTankHealth += 5
        powers -= 1
        collision6 = 0

    if len(collision7) >= 1:
        tankHealth -= 5
        if len(collision7) >= 2:
            badTankMines += 1
            collision7 = 0

    if len(collision8) >= 1:
        badTankHealth -= 5
        if len(collision8) >= 2:
            tankMines += 1
            collision8 = 0
        
    if tankHealth <= 0 and death is None:
        death = ZSurface('fire.png', tank.x, tank.y, 0,0)
        tank.x , tank.y = -700, -700
        
    if death != None:
        screen.blit(death.image, death.rect)
        
        
    if badTankHealth <= 0.0 and death2 is None:
        death2 = ZSurface('fire.png', badTank.x - 10, badTank.y - 20, 0,0)
        badTank.x, badTank.y = -700, -700
        #badTank.kill()

    if death2 != None:
        screen.blit(death2.image, death2.rect)

    if firing == 1:
        if pygame.time.get_ticks() - fireTime > 35:
            badMissiles2.add(ZSprite('bullet2.png', badTank.x + 6, badTank.y + 50, 0 ,20))
            fireTime = pygame.time.get_ticks()

    if firing2 == 1:
        if pygame.time.get_ticks() - fireTime2 > 35:
            missiles2.add(ZSprite('bullet.png', tank.x + 6, tank.y, 0 ,-20))
            fireTime2 = pygame.time.get_ticks()

    if pygame.time.get_ticks() - powerTime > 20000:
        if powers == 0:
            powers += 1
            powerUps.add(ZSprite('health.png', random.randint(100,1000), random.randint(0,600), 0,0))
        powerTime = pygame.time.get_ticks()
        
        
    pygame.display.update()
    fpsClock.tick(FPS)

    tank.update()
    badTank.update()
