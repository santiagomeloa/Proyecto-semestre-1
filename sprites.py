import pygame, random
import funtions

color = (12,31,124)

#-------Tamaño de la pantalla------

WIDTH = funtions.screen_size()[0]
HEIGHT = funtions.screen_size()[1]
#WIDTH = 1200
#HEIGHT = 675

#---------------------------------------------------------------------------------------------------------------------
#-------------------------------------Defina aquí todos los sprites del juego-----------------------------------------
#---------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, imagen, area, hp, luck):
        super().__init__()
        self._hp = hp
        self._luck = luck

        self.image = funtions.load_image(imagen, area[0], area[1], True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
    
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
        if self.rect.top > HEIGHT-80:
            self.rect.top = HEIGHT-80

        elif self.rect.bottom < 0+80:
            self.rect.bottom = 0+80

        elif self.rect.right > WIDTH+5:
            self.rect.right = WIDTH+5

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
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
    
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, hp):
        self._hp = hp


    def update(self):
        self.rect.y += 2
        self.rect.x += 2
        if self.rect.top > HEIGHT:
            #self.rect.top = random.randint(0, HEIGHT)
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(0, HEIGHT)
        elif self.rect.bottom < 0:
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(0, HEIGHT)
            #self.rect.top = random.randint(0, HEIGHT)
        elif self.rect.left < 0:
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(0, HEIGHT)
            #self.rect.left = random.randint(0, WIDTH)
        elif self.rect.right > WIDTH:
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.centery = random.randint(0, HEIGHT)
            #self.rect.right = random.randint(0, WIDTH)


    def draw(self, surface):
        surface.blit(self.image, self.rect)