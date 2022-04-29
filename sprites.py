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
        self.frame = 0 #Define en cual posición va a estar el personje

        #-------------------------------frames-------------------------
        self.sheet = functions.load_image(imagen, area[0], area[1], True)
        
        # Posición inicial
        self.sheet.set_clip(pygame.Rect(self.sheet.get_width()/9.3, self.sheet.get_height()/4.2, self.sheet.get_width()/4.5, self.sheet.get_height()/3.59))
        
        
        

        self.neutral_state = {
                            -1:(self.sheet.get_width()/13.4, self.sheet.get_height()/1.7, self.sheet.get_width()/3.8, self.sheet.get_height()/2.8),
                            0:(self.sheet.get_width()/9.3, self.sheet.get_height()/4.2, self.sheet.get_width()/4.5, self.sheet.get_height()/3.59),
                            8:(self.sheet.get_width()/1.65, self.sheet.get_height()/4.1, self.sheet.get_width()/4.33, self.sheet.get_height()/3.59),
                            16:(self.sheet.get_width()/1.66, self.sheet.get_height()/1.53, self.sheet.get_width()/4.4, self.sheet.get_height()/3.45)
                            }


        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self._hp = hp
        self._luck = luck
        self._attack = random.randint(100, 600)*(1/self._luck)

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

    def collide(self):
        # Posición de sorpresa
        self.sheet.set_clip(pygame.Rect(self.neutral_state[-1]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def animation(self):
        self.frame += 1
        #if self.frame > (len(self.neutral_state) - 1):
        if self.frame > 24:
            self.frame = 0
        if self.frame == 0 or self.frame == 8 or self.frame == 16:
            self.sheet.set_clip(pygame.Rect(self.neutral_state[self.frame]))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
    
    def update(self):
        self.animation()
 
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
    def __init__(self, imagen, location, area, hp, damage, enemy):
        super().__init__()
        self._hp = hp
        self._damage = damage
        self._location = location
        self._area = area
        self.imagen = imagen
        self.enemy = enemy

        #----------------------frames------------------------
        self.frame = 0
        self.sheet = functions.load_image(self.imagen, self.area[0], self.area[1], True)

        # Posición inicial card
        if self.enemy == 'card':
            self.sheet.set_clip(pygame.Rect(self.sheet.get_width()/11.1, self.sheet.get_height()/35, self.sheet.get_width()/2.7, self.sheet.get_height()/2.75))
        
        # Posición inicial bolt
        if self.enemy == 'bolt':
            self.sheet.set_clip(pygame.Rect(self.sheet.get_width()/11.56, self.sheet.get_height()/2.28, self.sheet.get_width()/3.44, self.sheet.get_height()/4.49))


        self.cardEnemy_moves = {
            0:(self.sheet.get_width()/11.1, self.sheet.get_height()/35, self.sheet.get_width()/2.7, self.sheet.get_height()/2.75),
            10:(self.sheet.get_width()/1.72, self.sheet.get_height()/35, self.sheet.get_width()/2.7, self.sheet.get_height()/2.75),
        }
        self.boltEnemy_moves = {
            0:(self.sheet.get_width()/11.56, self.sheet.get_height()/2.28, self.sheet.get_width()/3.44, self.sheet.get_height()/4.49),
            8:(self.sheet.get_width()/2.252, self.sheet.get_height()/2.305, self.sheet.get_width()/3.445, self.sheet.get_height()/4.355),
            16:(self.sheet.get_width()/9.721, self.sheet.get_height()/1.405, self.sheet.get_width()/3.62, self.sheet.get_height()/4.26),
            24:(self.sheet.get_width()/2.243, self.sheet.get_height()/1.416, self.sheet.get_width()/3.62, self.sheet.get_height()/4.26)
        }

        self.image = self.sheet.subsurface(self.sheet.get_clip())

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

    def animation(self):
        self.frame += 1
        if self.enemy == 'card':
            if self.frame > 20:
                self.frame = 0
            if self.frame == 0 or self.frame == 10:
                self.sheet.set_clip(pygame.Rect(self.cardEnemy_moves[self.frame]))
                self.image = self.sheet.subsurface(self.sheet.get_clip())
        if self.enemy == 'bolt':
            if self.frame > 32:
                self.frame = 0
            if self.frame == 0 or self.frame == 8 or self.frame == 16 or self.frame == 24:
                self.sheet.set_clip(pygame.Rect(self.boltEnemy_moves[self.frame]))
                self.image = self.sheet.subsurface(self.sheet.get_clip())

    def move(self):
        if self.enemy == 'card':
            if self.frame == 0:
                self.rect.x += 10

            elif self.frame == 15:
                self.rect.y += 10
                self.rect.x += 2
                self.rect.y -= 10
                
        elif self.enemy == 'bolt':
            if self.frame == 0:
                self.rect.x += 50

            elif self.frame == 8:
                self.rect.y += 80

            elif self.frame == 16:
                self.rect.x -= 86

            elif self.frame == 24:
                self.rect.y -= 32

    def update(self):
        self.animation()
        self.move()
        
                
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

