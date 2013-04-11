# Programmer: Zackery C. Mason-Blaug
# Date: 2/17/2013
# Title: Zombie Wars

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
        self.rect.topleft = [ self.x, self.y ]

    def update(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.topleft = [ self.x, self.y ]

class ZPlayer(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.health = 50
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

def playSound(soundfile):
    sound = pygame.mixer.Sound(soundfile)
    
pygame.display.set_caption('Zombi Attack Force')

GREEN = (0,225,0)
FPS = 30
fpsClock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode([1040, 640])

#Create groups
missiles = pygame.sprite.Group()
missiles2 = pygame.sprite.Group()
strMissiles = pygame.sprite.Group()
blocks = pygame.sprite.Group()
baddies = pygame.sprite.Group()
bosses = pygame.sprite.Group()
bShots = pygame.sprite.Group()


#Powerups data
powerUps = pygame.sprite.Group()
powerTime = 0
powers = 0

#Weapons data
weapons = pygame.sprite.Group()
WTime = 0

#Create Players
tank = ZPlayer('RamboZombKiller.png', 500, 500, 0, 0)
soldier = ZPlayer('soldier.png', 400, 500, 0 ,0)

blocks.add(ZSprite('sandbag.png', 300, 200, 0, 0))
blocks.add(ZSprite('sandbag.png', 800, 200, 0, 0))

font = pygame.font.Font(None, 48)

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
BTime = 0
ZScore = 0
Difficulty = 100
DD = 60
difficultyTime = 0
lvl = 1
create = 1

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
    


def RESTART():
    tank.health = 50
    soldier.health = 50
    tank.x, tank.y = 500, 500
    soldier.x, soldier.y = 200, 500
    Difficulty = 100
    ZMode = 1
    tank.score = 0
    soldier.score = 0
    ZScore = 0
    tank.pAmmo = 0
    soldier.pAmmo = 0
    lvl = 1
    tank.spWep = None
    soldier.spWep = None
    create = 1
    for zombi in baddies:
        baddies.remove(zombi)
        zombi.kill()
    for Boss in bosses:
        bosses.remove(Boss)
        Boss.kill()

def spreadShot(player):
    pellet = missiles.add(ZSprite('pellet.png', player.x + 40, player.y, random.randint(-4,4) ,-20+random.randint(-3,3)))
    pellet = missiles.add(ZSprite('pellet.png', player.x + 40, player.y, random.randint(-4,4) ,-20+random.randint(-3,3)))
    pellet = missiles.add(ZSprite('pellet.png', player.x + 40, player.y, random.randint(-4,5) ,-20+random.randint(-3,3)))
    pellet = missiles.add(ZSprite('pellet.png', player.x + 40, player.y, random.randint(-4,4) ,-20+random.randint(-3,3)))
    pellet = missiles.add(ZSprite('pellet.png', player.x + 40, player.y, random.randint(-4,4) ,-20+random.randint(-3,3)))

def Help():
    tank.health = 50
    soldier.health = 50
    tank.pAmmo = 1000
    soldier.pAmmo = 1000
    tank.spWep = 'Flamer'
    soldier.spWep = 'Flamer'
    
while True:
    screen.fill(GREEN)
    keyPressed = False
    screen.blit(tank.image, tank.rect)
    screen.blit(soldier.image, soldier.rect)
    death = None
    death2 = None

    if soldier.health <= 0:
        soldier.health = 'Dead'
        
    if tank.health <= 0:
        tank.health = "Dead"

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
        
    #Update groups
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
        if zombi.hp <= 0:
            baddies.remove(zombi)
            zombi.kill()

    for demon in baddies:
        screen.blit(demon.image, demon.rect)
        demon.update()
        if demon.y >= 660:
            baddies.remove(demon)
            demon.kill()
            ZScore += 1
        if demon.hp <= 0:
            baddies.remove(demon)
            demon.kill()

    for Boss in bosses:
        screen.blit(Boss.image, Boss.rect)
        Boss.update()
        if Boss.y >= 0:
            Boss.dy = 0
        if Boss.x >= 600:
            Boss.dx *= -1
        if Boss.x <= 400:
            Boss.dx *= -1
        if pygame.time.get_ticks() - BTime > 200:
            fireBall = bShots.add(ZSprite('napalm.png', Boss.x + 53, Boss.y + 25, random.randint(-7, 7), random.randint(5, 10)))
            fireBall = bShots.add(ZSprite('napalm.png', Boss.x + 115, Boss.y + 85, random.randint(-7, 7), random.randint(5, 10)))
            fireBall = bShots.add(ZSprite('napalm.png', Boss.x + 10, Boss.y + 85, random.randint(-7, 7), random.randint(5, 10)))
            BTime = pygame.time.get_ticks()
        if Boss.hp <= 0:
            ZMode = 1
            Difficulty = 100
            ZTime = pygame.time.get_ticks()
            bosses.remove(Boss)
            Boss.kill()
        drawText('Boss Health: %s' % (Boss.hp), font, screen, 500, 600)

    for fireBall in bShots:
        fireBall.update()
        screen.blit(fireBall.image, fireBall.rect)
        if fireBall.y >= 700:
            bShots.remove(fireBall)
            fireBall.kill()

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
            
    #Check buttons pressed
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            break

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
                        spreadShot(soldier)
                        
                if soldier.spWep == 'Flamer':
                    if soldier.pAmmo > 0:
                        firing3 = 1
        
            elif event.key == K_n:
                if tank.spWep == 'Shotgun':
                    if tank.pAmmo > 0:
                        tank.pAmmo -= 1
                        spreadShot(tank)
                        
                if tank.spWep == 'Flamer':
                    if tank.pAmmo > 0:
                        firing4 = 1

            elif event.key == K_RETURN:
                RESTART()
                
            elif event.key == K_i:
                tank.x, tank.y = 500, 500
                soldier.x, soldier.y = 400, 600

            elif event.key == K_5:
                Difficulty = 25

            elif event.key == K_7:
                Help()
                
            elif event.key == K_4:
                lvl = 10

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

        if pygame.joystick.get_count() > 0:
            if event.type == pygame.locals.JOYBUTTONDOWN:
                if joy1.get_button(5):
                    firing = 1

                if joy1.get_button(4):
                    if tank.spWep == 'Shotgun':
                        if tank.pAmmo > 0:
                            tank.pAmmo -= 1
                            spreadShot(tank)
                            
                    if tank.spWep == 'Flamer':
                        if tank.pAmmo > 0:
                            firing4 = 1

                if joy1.get_button(7):
                    RESTART()

            elif event.type == pygame.locals.JOYBUTTONUP:
                if joy1.get_button(5) == False:
                    firing = 0

                if joy1.get_button(4) == False:
                    firing4 = 0

            elif event.type == pygame.locals.JOYAXISMOTION:
                if joy1.get_axis(1) > 0.3:
                    tank.dy = 10
                else:
                    tank.dy = 0
                if joy1.get_axis(1) < -0.3:
                    tank.dy = -10
                    
                if joy1.get_axis(0) > .2:
                    tank.dx = 10
                else:
                    tank.dx = 0

                if joy1.get_axis(0) < -0.2:
                    tank.dx = -10

            elif event.type == pygame.locals.JOYHATMOTION:
                if joy1.get_hat == (0, -1):
                    tank.x, tank.y = 500, 500
                    soldier.x, soldier.y = 200, 200
                    print 'fail'
                    

        if pygame.joystick.get_count() > 1:
            if event.type == pygame.locals.JOYBUTTONDOWN:

                if joy2.get_button(5):
                    firing2 = 1

                if joy2.get_button(4):
                    if soldier.spWep == 'Shotgun':
                        if soldier.pAmmo > 0:
                            soldier.pAmmo -= 1
                            spreadShot(soldier)
                            
                    if soldier.spWep == 'Flamer':
                        if soldier.pAmmo > 0:
                            firing3 = 1

            elif event.type == pygame.locals.JOYBUTTONUP:    
                if joy2.get_button(5) == False:
                    firing2 = 0

                if joy2.get_button(4) == False:
                    firing3 = 0

            elif event.type == pygame.locals.JOYAXISMOTION:
                if joy2.get_axis(1) < -0.2:
                    soldier.dy = -10
                elif joy2.get_axis(1) > 0.2:
                    soldier.dy = 10
                else:
                    soldier.dy = 0
                if joy2.get_axis(0) > .2:
                    soldier.dx = 10
                else:
                    soldier.dx = 0
                if joy2.get_axis(0) < -0.2:
                    soldier.dx = -10
            
            

                
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

    #Store collision into lists
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
    b_collide = pygame.sprite.groupcollide(missiles, bosses, True, False)
    B_collide = pygame.sprite.groupcollide(missiles2, bosses, True, False)
    collision00 = pygame.sprite.spritecollide(tank, bShots, True)
    collision01 = pygame.sprite.spritecollide(soldier, bShots, True)

    #On-Screen Text
    drawText1('Left Player: %s Kills: %s Ammo: %s' % (tank.health, tank.score, tank.pAmmo), font, screen,10,0)
    drawText1('Right Player: %s Kills: %s Ammo: %s' % (soldier.health, soldier.score, soldier.pAmmo), font, screen, 10, 30)
    drawText('Zombies Escaped: %s' % (ZScore), font, screen, 10, 600)
    drawText1('Level: %s' % (lvl), font, screen, 900, 600)
    drawText('%s' % (tank.health), font, screen, tank.x+4, tank.y+60)
    drawText2('%s' % (soldier.health), font, screen, soldier.x+4, soldier.y+60)

    #
    #Check Collisions
    #
    if len(collision5) >= 1:
        tank.health += 5
        powers -= 1
        collision5 = 0

    if len(collision6) >= 1:
        soldier.health += 5
        powers -= 1
        collision6 = 0

    if len(collision3) >= 1:
        if tank.spWep != collision3[0].gun:
            tank.pAmmo = 0
        tank.pAmmo += collision3[0].ammo
        tank.spWep = collision3[0].gun
        weapons.remove(collision3[0])
        collision3 = 0

    if len(collision4) >= 1:
        if soldier.spWep != collision4[0].gun:
            soldier.pAmmo = 0
        soldier.pAmmo += collision4[0].ammo
        soldier.spWep = collision4[0].gun
        weapons.remove(collision4[0])
        collision4 = 0

    if len(collision00) >= 1:
        tank.health -= 1
        collision00 = 0
        screen.fill(textcolor)

    if len(collision01) >= 1:
        soldier.health -= 1
        collision01 = 0
        screen.fill(textcolor)

    if len(collision) >= 1:
        soldier.health -= 1
        collision = 0
        screen.fill(textcolor)

    if len(collision0) >= 1:
        tank.health -= 1
        collsion0 = 0
        screen.fill(textcolor)

    if len(collision1) >= 1:
        tank.score += 1
        collision1 = 0

    if len(collision2) >= 1:
        soldier.score += 1
        collision2 = 0

    if len(b_collide) >= 1:
        b_collide = 0
        Boss.hp -= 1
        if Boss.hp == 0:
            tank.score += 1000

    if len(B_collide) >= 1:
        B_collide = 0
        Boss.hp -= 1
        if Boss.hp == 0:
            soldier.score += 1000

    if tank.pAmmo == 0:
        tank.spWep = None

    if soldier.pAmmo == 0:
        soldier.spWep = None
        
    if tank.health <= 0 and death is None:
        death = ZSurface('fire.png', tank.x, tank.y, 0,0)
        tank.x , tank.y = -700, -700
        if soldier.health <= 0:
            if ZMode == 1:
                ZMode = 0
            for zombi in baddies:
                zombi.dy = 0
        
    if death != None:
        screen.blit(death.image, death.rect)
        
    if soldier.health <= 0.0 and death2 is None:
        death2 = ZSurface('fire.png', soldier.x, soldier.y, 0,0)
        soldier.x, soldier.y = -700, -700
        if tank.health <= 0:
            if ZMode == 1:
                ZMode = 0
            for zombi in baddies:
                zombi.dy = 0

    if death2 != None:
        screen.blit(death2.image, death2.rect)

    #Automatic Firing
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
        
    #Create Healing Powerup
    if pygame.time.get_ticks() - powerTime > random.randint(10000, 15000):
        if powers == 0:
            powers += 1
            powerUps.add(ZSprite('health.png', random.randint(100,1000), random.randint(0,600), 0,0))
            powerTime = pygame.time.get_ticks()

    #Create weapons
    if pygame.time.get_ticks() - WTime > 15000:
        GChoice = random.randint(1,2)
        if GChoice == 1:
            shotgun = weapons.add(Gun('shotgun.png', random.randint(100,1000), random.randint(50, 600), 30, 'Shotgun'))
            WTime = pygame.time.get_ticks()
        if GChoice == 2:
            flamer = weapons.add(Gun('flamethrower.png', random.randint(100,1000), random.randint(50, 600), 200, 'Flamer'))
            WTime = pygame.time.get_ticks()

    #Create Zombies
    if pygame.time.get_ticks() - ZTime > Difficulty:
        if ZMode == 1:
            zombi = baddies.add(ZZombies('zombie.png', random.randint(1,1000), 0, random.randint(-1,1), random.randint(2,5), 2))
            if Difficulty <= 35:
                
                if pygame.time.get_ticks() - DTime > DD:
                    DTime = pygame.time.get_ticks()
                    demon = baddies.add(ZZombies('Demon.png', random.randint(1,1000), 0, 0, random.randint(3,9), 2))
        ZTime = pygame.time.get_ticks()

    if lvl >= 10:
        ZMode = 2
        
    #Boss Level
    if ZMode == 2:
        if create == 1:
            Boss = bosses.add(ZZombies('MyBoss.png', 500, -100, 3, 3, 750))
            create -= 1
            if tank.health <= 59 and tank.health > 0:
                tank.health = 60
            if soldier.health <= 59 and soldier.health > 0:
                soldier.health = 60

    if create == 0:
        for Boss in bosses:
            if Boss.hp <= 0:
                ZMode = 1
                Difficulty = 100
                ZTime = pygame.time.get_ticks()
                bosses.remove(Boss)
                Boss.kill()

        
    pygame.display.update()
    fpsClock.tick(FPS) 
    tank.update()
    soldier.update()
