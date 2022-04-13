import pygame, random, time, asyncio
import funtions

color = (12,31,124)



#---------------------------------------------------------------------------------------------------------------------
#-------------------------------------Defina aquí todos los sprites del juego-----------------------------------------
#---------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, imagen, location, area, hp, luck):
        super().__init__()
        self._hp = hp
        self._luck = luck

        self.image = funtions.load_image(imagen, area[0], area[1], True)
        self.rect = self.image.get_rect()
        self.rect.centerx = location[0]
        self.rect.centery = location[1]
    
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        self._hp = hp

    @property
    def luck(self):
        return self._luck
    
    @luck.setter
    def luck(self, luck):
        self._luck = luck
    
    def update(self):
        if self.rect.top > funtions.HEIGHT-80:
            self.rect.top = funtions.HEIGHT-80

        elif self.rect.bottom < 0+80:
            self.rect.bottom = 0+80

        elif self.rect.right > funtions.WIDTH+5:
            self.rect.right = funtions.WIDTH+5

        elif self.rect.left < 0-20:
            self.rect.left = 0-20
    def draw(self, surface):
        surface.blit(self.image, self.rect)



class Bicho(pygame.sprite.Sprite):
    def __init__(self, imagen, area, hp, damage):
        super().__init__()
        self._hp = hp
        self._damage = damage

        self.image = funtions.load_image(imagen, area[0], area[1], True)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, funtions.WIDTH)
        self.rect.centery = random.randint(0, funtions.HEIGHT)
    
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, hp):
        self._hp = hp


    def update(self):
        x = random.choice(['x', 'y'])
        print(x)

        if x == 'x':
            for n in range(10):
                self.rect.centerx += 2
        else:
            for n in range(10):
                self.rect.centery += 2
                
        if self.rect.top < 0:
            #self.rect.centerx = random.randint(0, funtions.WIDTH)
            self.rect.bottom = funtions.HEIGHT

        elif self.rect.bottom > funtions.HEIGHT:
            #self.rect.centerx = random.randint(0, funtions.WIDTH)
            self.rect.top = 0

        elif self.rect.left <= 0:
            self.rect.right = funtions.WIDTH
            #self.rect.centery = random.randint(0, funtions.HEIGHT)

        elif self.rect.right > funtions.WIDTH:
            self.rect.left = 0
            #self.rect.centery = random.randint(0, funtions.HEIGHT)


    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = funtions.load_image('Images/hand.jpg', 60, 60, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.centery = 500

    def draw(self, surface):
        surface.blit(self.image, self.rect)



