import pygame, random, time, asyncio
import functions
from pygame.locals import *


color = (12,31,124)



#---------------------------------------------------------------------------------------------------------------------
#-------------------------------------Defina aquí todos los sprites del juego-----------------------------------------
#---------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, imagen, location, area, hp, luck):
        super().__init__()
        self._hp = hp
        self._luck = luck
        self._attack = random.randint(100, 600)*(1/self._luck)

        self.image = functions.load_image(imagen, area[0], area[1], True)
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
        if self.rect.top > functions.HEIGHT-functions.WIDTH*(1/6.3):
            self.rect.top = functions.HEIGHT-functions.WIDTH*(1/6.3)

        elif self.rect.bottom < functions.WIDTH*(1/6.6):
            self.rect.bottom = functions.WIDTH*(1/6.6)

        elif self.rect.right > functions.WIDTH-(functions.WIDTH*(1/65)):
            self.rect.right = functions.WIDTH-(functions.WIDTH*(1/65))

        elif self.rect.left < functions.WIDTH*(1/60):
            self.rect.left = functions.WIDTH*(1/60)
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bicho(pygame.sprite.Sprite):
    def __init__(self, imagen, location, area, hp, damage):
        super().__init__()
        self._hp = hp
        self._damage = damage
        self._location = location
        self._area = area
        self.imagen = imagen

        self.image = functions.load_image(self.imagen, self.area[0], self.area[1], True)
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
    def location(self):
        return self._location

    @location.setter
    def location(self, location:tuple):
        self.rect.centerx = location[0]
        self.rect.centery = location[1]

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        self.image = functions.load_image(self.imagen, area[0], area[1], True)


    def update(self):
        x = random.choice(['x', 'y'])

        if x == 'x':
            for n in range(10):
                self.rect.centerx += 2
        else:
            for n in range(10):
                self.rect.centery += 2
                
        if self.rect.top < 0:
            self.rect.bottom = functions.HEIGHT

        elif self.rect.bottom > functions.HEIGHT:
            self.rect.top = 0

        elif self.rect.left <= 0:
            self.rect.right = functions.WIDTH
        
        elif self.rect.right > functions.WIDTH:
            self.rect.left = 0
         


    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = functions.load_image('Images/hand.jpg', 60, 60, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = (functions.WIDTH/4)-(functions.WIDTH*(1/11))
        self.rect.centery = functions.HEIGHT-(functions.HEIGHT/4)
        self.speed = 0

    def update(self):
        self.rect.centerx += self.speed
        self.speed = 0

        if self.rect.top < 0:
            self.rect.bottom = functions.HEIGHT

        elif self.rect.bottom > functions.HEIGHT:
            self.rect.top = 0

        elif self.rect.left <= 0:
            self.rect.right = (functions.WIDTH-functions.WIDTH/4)-160
        
        elif self.rect.right > functions.WIDTH:
            self.rect.left = (functions.WIDTH/4)-180

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Words(pygame.sprite.Sprite, pygame.font.Font):
    def __init__(self, text: str, size: int, color, location, multicolor=False):
        super().__init__()

        self.fond = pygame.font.Font(None, size)
        self._text = text
        self._color = color
        self.multicolor = multicolor
        self.image = self.fond.render(text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = location[0]
        self.rect.centery = location[1]

    #--------setters and getters---------
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color



    def update(self):
        x = random.randint(0, len(functions.list_colors)-1)

        if self.multicolor:
            self.color = functions.list_colors[x]
        self.image = self.fond.render(self.text, 1 , self.color)
        return self.image

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Buttons(pygame.sprite.Sprite):
    def __init__(self, type_button, position: tuple):
        super().__init__()
        self.sheet = functions.load_image('Images/Botones de control 1.png', 300, 300, True)
        if type_button == 'attack':
            self.sheet.set_clip(pygame.Rect(8, 6, 330, 80))
        elif type_button == 'spell':
            self.sheet.set_clip(pygame.Rect(10, 108, 235, 88))
        elif type_button == 'luck':
            self.sheet.set_clip(pygame.Rect(9, 202, 220, 90))
        self.image = self.sheet.subsurface(self.sheet.get_clip())


        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

