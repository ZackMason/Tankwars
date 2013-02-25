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
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.score = 0
        self.pAmmo = 0
        self.spWep = None
        self.rect.topleft = [ self.x, self.y ]

    def update(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.topleft = [ self.x, self.y ]

class ZZombies(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, dx, dy, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.hp = hp
        self.rect.topleft = [ self.x, self.y ]

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = [ self.x, self.y ]
    
class Gun(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, ammo, gun):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.ammo = ammo
        self.gun = gun
        self.rect.topleft = [self.x , self.y]

    def update(self):
        screen.blit(self.image, self.rect)


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

textcolor = (225, 225, 0)

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

def drawText1(text, font, surface,x, y):
    textobj = font.render(text, 1, textcolor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
pygame.display.set_caption('Tank Buster')

GREEN = (0,225,0)
FPS = 30
fpsClock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode([1040, 640])

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

missiles = pygame.sprite.Group()
missiles2 = pygame.sprite.Group()
strMissiles = pygame.sprite.Group()
blocks = pygame.sprite.Group()
baddies = pygame.sprite.Group()

powerUps = pygame.sprite.Group()
powerTime = 0
powers = 0

weapons = pygame.sprite.Group()
WTime = 0


tank = ZSprite('RamboZombKiller.png', 500, 500, 0, 0)
tankHealth = 50
soldier = ZSprite('soldier.png', 400, 500, 0 ,0)
soldierHealth = 50

blocks.add(ZSprite('sandbag.png', 300, 200, 0, 0))
blocks.add(ZSprite('sandbag.png', 800, 200, 0, 0))

font = pygame.font.SysFont(None, 48)

firing = 0
fireTime = 0
firing2 = 0
fireTime2 = 0
firing3 = 0
fireTime3 = 0
firing4 = 0
fireTime4 = 0
red = (255,0,0)
GChoice = 0
ZMode = 1
ZTime = 0
DTime = 0
ZScore = 0
Difficulty = 100
DD = 60
difficultyTime = 0
lvl = 0


while True:
    screen.fill(GREEN)
    keyPressed = False
    screen.blit(tank.image, tank.rect)
    screen.blit(soldier.image, soldier.rect)
    death = None
    death2 = None
    TH = tankHealth
    BTH = soldierHealth

    if soldierHealth <= 0:
        BTH = 'Dead'
        
    if tankHealth <= 0:
        TH = "Dead"

    if tank.y >= 620:
        tank.dy = 0

    if tank.x >= 1020:
        tank.dx = 0

    if tank.x <= 0:
        tank.dx = 0

    if soldier.y >= 620:
        soldier.dy = 0

    if soldier.x >= 1020:
        soldier.dx = 0

    if soldier.x <= 0:
        soldier.dx = 0
        
    for block in blocks:
        screen.blit(block.image, block.rect)

    for zombi in baddies:
        screen.blit(zombi.image, zombi.rect)
        zombi.update()
        if zombi.y >= 660:
            baddies.remove(zombi)
            zombi.kill()
            ZScore += 1
        if zombi.x >= 1020:
            zombi.dx *= -1
        if zombi.x <= 0:
            zombi.dx *= -1

    for demon in baddies:
        screen.blit(demon.image, demon.rect)
        demon.update()
        if demon.y >= 660:
            baddies.remove(demon)
            demon.kill()
            ZScore += 1

    for shotgun in weapons:
        shotgun.update()
        
    for flamer in weapons:
        flamer.update()
        
    for powerUp in powerUps:
        screen.blit(powerUp.image, powerUp.rect)

    for missile in missiles:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y < -100:
            missiles.remove(missile)
            missile.kill()

    for pellet in missiles:
        pellet.update()
        if pellet.y < -100:
            missiles.remove(pellet)
            pellet.kill()
                        
    for missile in missiles2:
        missile.update()
        screen.blit(missile.image, missile.rect)
        if missile.y < -100:
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

            elif event.key == K_d:
                tank.dx = 10

            elif event.key == K_a:
                tank.dx = -10

            elif event.key == K_UP:
                soldier.dy = -10

            elif event.key == K_DOWN:
                soldier.dy = 10

            elif event.key == K_RIGHT:
                soldier.dx = 10

            elif event.key == K_LEFT:
                soldier.dx = -10

            elif event.key == K_m:
                firing = 1

            elif event.key == K_KP1:
                firing2 = 1

            elif event.key == K_KP0:
                if soldier.spWep == 'Shotgun':
                    if soldier.pAmmo > 0:
                        soldier.pAmmo -= 1
                        pellet = missiles2.add(ZSprite('pellet.png', soldier.x + 33, soldier.y, random.randint(-4,4) ,-20))
                        pellet = missiles2.add(ZSprite('pellet.png', soldier.x + 33, soldier.y, random.randint(-4,4) ,-20))
                        pellet = missiles2.add(ZSprite('pellet.png', soldier.x + 33, soldier.y, random.randint(-4,5) ,-20))
                        pellet = missiles2.add(ZSprite('pellet.png', soldier.x + 33, soldier.y, random.randint(-4,4) ,-20))
                        pellet = missiles2.add(ZSprite('pellet.png', soldier.x + 33, soldier.y, random.randint(-4,4) ,-20))
                if soldier.spWep == 'Flamer':
                    if soldier.pAmmo > 0:
                        firing3 = 1
        
            elif event.key == K_n:
                if tank.spWep == 'Shotgun':
                    if tank.pAmmo > 0:
                        tank.pAmmo -= 1
                        pellet = missiles.add(ZSprite('pellet.png', tank.x + 40, tank.y, random.randint(-4,4) ,-20))
                        pellet = missiles.add(ZSprite('pellet.png', tank.x + 40, tank.y, random.randint(-4,4) ,-20))
                        pellet = missiles.add(ZSprite('pellet.png', tank.x + 40, tank.y, random.randint(-4,5) ,-20))
                        pellet = missiles.add(ZSprite('pellet.png', tank.x + 40, tank.y, random.randint(-4,4) ,-20))
                        pellet = missiles.add(ZSprite('pellet.png', tank.x + 40, tank.y, random.randint(-4,4) ,-20))
                if tank.spWep == 'Flamer':
                    if tank.pAmmo > 0:
                        firing4 = 1
                        

            elif event.key == K_RETURN:
                tankHealth = 50
                soldierHealth = 50
                tank.x, tank.y = 500, 500
                soldier.x, soldier.y = 200, 200
                Difficulty = 100
                ZMode = 1
                tank.score = 0
                soldier.score = 0
                ZScore = 0
                tank.pAmmo = 0
                soldier.pAmmo = 0
                lvl = 1
                for zombi in baddies:
                    baddies.remove(zombi)
                    zombi.kill()

            elif event.key == K_i:
                tank.x, tank.y = 500, 500
                soldier.x, soldier.y = 400, 600

            elif event.key == K_l:
                Difficulty = 25

            elif event.key == K_7:
                tankHealth = 50
                soldierHealth = 50
                tank.pAmmo = 300
                soldier.pAmmo = 300
                tank.spWep = 'Flamer'
                soldier.spWep = 'Flamer'

            elif event.key == K_6:
                tankHealth = 50
                soldierHealth = 50

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
                soldier.dy = 0

            elif event.key == K_DOWN:
                soldier.dy = 0

            elif event.key == K_RIGHT:
                soldier.dx = 0

            elif event.key == K_LEFT:
                soldier.dx = 0

            elif event.key == K_KP1:
                firing2 = 0

            elif event.key == K_m:
                firing = 0

            elif event.key == K_KP0:
                firing3 = 0

            elif event.key == K_n:
                firing4 = 0



    collision5 = pygame.sprite.spritecollide(tank, powerUps, True)
    collision6 = pygame.sprite.spritecollide(soldier, powerUps, True)
    collision = pygame.sprite.spritecollide(soldier, baddies, True)
    collision0 = pygame.sprite.spritecollide(tank, baddies, True)
    collision1 = pygame.sprite.groupcollide(baddies, missiles, True, True)
    collision2 = pygame.sprite.groupcollide(baddies, missiles2, True, True)
    collision3 = pygame.sprite.spritecollide(tank, weapons, True)
    collision4 = pygame.sprite.spritecollide(soldier, weapons, True)
    pygame.sprite.groupcollide(blocks ,missiles, False, True)
    pygame.sprite.groupcollide(blocks ,missiles2, False, True)


    drawText('Left Player: %s Kills: %s Ammo: %s' % (TH, tank.score, tank.pAmmo), font, screen,10,0)
    drawText2('Right Player: %s Kills: %s Ammo: %s' % (BTH, soldier.score, soldier.pAmmo), font, screen, 10, 30)
    drawText('Zombies Escaped: %s' % (ZScore), font, screen, 10, 600)
    drawText1('Level: %s' % (lvl), font, screen, 900, 600)
    
    if len(collision5) >= 1:
        tankHealth += 5
        powers -= 1
        collision5 = 0

    if len(collision6) >= 1:
        soldierHealth += 5
        powers -= 1
        collision6 = 0

    if len(collision3) >= 1:
        tank.pAmmo += shotgun.ammo
        tank.spWep = shotgun.gun
        collision3 = 0

    if len(collision4) >= 1:
        soldier.pAmmo += shotgun.ammo
        soldier.spWep = shotgun.gun
        collision4 = 0

    if len(collision) >= 1:
        soldierHealth -= 1
        collision = 0

    if len(collision0) >= 1:
        tankHealth -= 1
        collsion0 = 0

    if len(collision1) >= 1:
        collision1 = 0
        tank.score += 1
        #print(tank.score)

    if len(collision2) >= 1:
        collision2 = 0
        soldier.score += 1
        #print(soldier.score)

    if tank.pAmmo == 0:
        tank.spWep = None

    if soldier.pAmmo == 0:
        soldier.spWep = None
        
    if tankHealth <= 0 and death is None:
        death = ZSurface('fire.png', tank.x, tank.y, 0,0)
        tank.x , tank.y = -700, -700
        if soldierHealth <= 0:
            if ZMode == 1:
                ZMode = 0
                print("Tank got " + str(tank.score) + " kills. " + str(ZScore) + " Zombies escaped, Your kill percentage is: " + str(int(tank.score/(tank.score + ZScore) * 100 )))
                print("Soldier got " + str(soldier.score) + " kills. " + str(ZScore) + " Zombies escaped, Your kill percentage is: " + str(int(soldier.score/(tank.score + ZScore) * 100)))
            for zombi in baddies:
                zombi.dy = 0
        
    if death != None:
        screen.blit(death.image, death.rect)
        
    if soldierHealth <= 0.0 and death2 is None:
        death2 = ZSurface('fire.png', soldier.x, soldier.y, 0,0)
        soldier.x, soldier.y = -700, -700
        if tankHealth <= 0:
            if ZMode == 1:
                ZMode = 0
                print("Tank got " + str(tank.score) + " kills. " + str(ZScore) + " Zombies escaped, Your kill percentage is: " + str(int(tank.score + 1/(tank.score + ZScore) * 100 )))
                print("Soldier got " + str(soldier.score) + " kills. " + str(ZScore) + " Zombies escaped, Your kill percentage is: " + str(int(soldier.score/(soldier.score + ZScore) * 100)))
            for zombi in baddies:
                zombi.dy = 0

    if death2 != None:
        screen.blit(death2.image, death2.rect)

    if firing == 1:
        if pygame.time.get_ticks() - fireTime > 35:
            missiles.add(ZSprite('bolt.png', tank.x + 40, tank.y, random.randint(-1,1) ,-10))
            fireTime = pygame.time.get_ticks()

    if firing2 == 1:
        if pygame.time.get_ticks() - fireTime2 > 35:
            missiles2.add(ZSprite('bullet.png', soldier.x + 33, soldier.y, random.randint(-1,1) ,-20))
            fireTime2 = pygame.time.get_ticks()

    if firing3 == 1:
        if pygame.time.get_ticks() - fireTime3 > 25:
            if soldier.pAmmo > 0:
                soldier.pAmmo -= 1
                missiles2.add(ZSprite('napalm.png', soldier.x + 33, soldier.y, random.randint(-2,2), -10))
                fireTime3 = pygame.time.get_ticks()

    if firing4 == 1:
        if pygame.time.get_ticks() - fireTime4 > 25:
            if tank.pAmmo > 0:
                tank.pAmmo -= 1
                missiles.add(ZSprite('napalm.png', tank.x + 40, tank.y, random.randint(-2,2), -5))
                fireTime4 = pygame.time.get_ticks()
            
    if pygame.time.get_ticks() - difficultyTime > 40000:
        Difficulty -= 10
        lvl += 1
        if Difficulty <= 20:
            Difficulty = 25
            DD -= 10
            if DD <= 20:
                DD = 20
        difficultyTime = pygame.time.get_ticks()
        print(Difficulty)
        

    if pygame.time.get_ticks() - powerTime > 20000:
        if powers == 0:
            powers += 1
            powerUps.add(ZSprite('health.png', random.randint(100,1000), random.randint(0,600), 0,0))
        powerTime = pygame.time.get_ticks()

    if pygame.time.get_ticks() - WTime > 15000:
        GChoice = random.randint(1,2)
        if GChoice == 1:
            shotgun = weapons.add(Gun('shotgun.png', random.randint(100,1000), random.randint(50, 600), 30, 'Shotgun'))
            WTime = pygame.time.get_ticks()
        if GChoice == 2:
            flamer = weapons.add(Gun('flamethrower.png', random.randint(100,1000), random.randint(50, 600), 200, 'Flamer'))
            WTime = pygame.time.get_ticks()

    if pygame.time.get_ticks() - ZTime > Difficulty:
        if ZMode == 1:
            zombi = baddies.add(ZZombies('zombie.png', random.randint(1,1000), 0, random.randint(-1,1), random.randint(2,5), 2))
            if Difficulty <= 35:
                
                if pygame.time.get_ticks() - DTime > DD:
                    DTime = pygame.time.get_ticks()
                    demon = baddies.add(ZZombies('Demon.png', random.randint(1,1000), 0, 0, random.randint(3,9), 3))
        ZTime = pygame.time.get_ticks()
            
        
    pygame.display.update()
    fpsClock.tick(FPS)

    tank.update()
    soldier.update()
