import subprocess, pygame, platform, ctypes, sys, random

from pygame.event import Event
import sprites
from pygame.locals import *



#------------colors-------------

RED = (255, 3, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (249, 255, 0)
DARK_PURPLE = (101, 5, 135)

list_colors = [RED, GREEN, BLUE, YELLOW, DARK_PURPLE]

#-------------functional variables---------------



sistema = platform.system() #Obtiene el sistema operativo del pc desde donde se esté ejecutando

diccionario={'20 – 7x = 6x – 6':'2', '7x + 2 = 10x + 5':'-1','6x − 5 = 8x + 2': '– 7 /2' , '4x + 4 + 9x + 18 = 12 (x+2)':'2', '2 - x = x - 8':'5', '2x - 1 = 5x + 8':'-3-', '5x - 10 = 10': '4', '4y - 5 = 3y + 1': '6', '2(2x - 3) = 2x - 10':'-2', '3x - 4 = 3(2x - 2) - 7':'3', '2(t + 2) - 5 = 5(t - 4) + 13':'2'}

def screen_size(): # Obtine la resolución de la pantalla dependiendo del sistema operativo
    if sistema == 'Linux':
        size = (None, None)
        args = ["xrandr", "-q", "-d", ":0"]
        proc = subprocess.Popen(args,stdout=subprocess.PIPE)
        for line in proc.stdout:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
                if "Screen" in line:
                    size = (int(line.split()[7]),  int(line.split()[9][:-1]))
        return size
    else:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return WIDTH, HEIGHT

#-------Tamaño de la pantalla------

WIDTH = screen_size()[0]
HEIGHT = screen_size()[1]
#WIDTH = 1200
#HEIGHT = 675

def load_image(filename, width=None, height=None, transparent=False): #covierte las imagenes, les da las dimenciones deceadas y les quita el fondo
    try: imagen = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit
        
    if width != None or height != None:
        imagen = pygame.transform.scale(imagen, (width, height))

    imagen = imagen.convert()
    if transparent:
        color = pygame.PixelArray(imagen)
        imagen.set_colorkey(color[0, 0], RLEACCEL)
    return imagen


def move(keys, sprite, speed:int, hand=False, pos_x:int=0, pos_y:int=0):  #Permite el movimiento de cualquier sprite que se le pase como parametro

    if hand:
        #---------------------------------------
        if keys[K_RIGHT]:
            pos_x += 1


        elif keys[K_LEFT]:
            pos_x -= 1


        # elif keys[K_UP]:
        #     sprite.rect.y -= speed
        
        # elif keys[K_DOWN]:
        #     sprite.rect.y += speed


        #----------------------------------------
        if pos_x > 3:
            pos_x = 1

        elif pos_x < 1:
            pos_x = 3

        #----------------------------------------
        if pos_x == 1:
            sprite.rect.centerx = (WIDTH/4)-(WIDTH*(1/11))

        elif pos_x == 2:
            sprite.rect.centerx = (WIDTH/2)-(WIDTH*(1/11))

        elif pos_x == 3:
            sprite.rect.centerx = (WIDTH-WIDTH/4)-(WIDTH*(1/11))

        #-----------------------------------------
        return pos_x, pos_y
            
    else:
        if keys[K_LEFT]:
            sprite.rect.x -= speed
            if keys[K_UP]:
                sprite.rect.y -= speed
            elif keys[K_DOWN]:
                sprite.rect.y += speed

        elif keys[K_RIGHT]:
            sprite.rect.x += speed
            if keys[K_UP]:
                sprite.rect.y -= speed
            elif keys[K_DOWN]:
                sprite.rect.y += speed
            
        elif keys[K_UP]:
            sprite.rect.y -= speed
            if keys[K_RIGHT]:
                sprite.rect.x += speed
            elif keys[K_LEFT]:
                sprite.rect.x -= speed

        elif keys[K_DOWN]:
            sprite.rect.y += speed
            if keys[K_RIGHT]:
                sprite.rect.x += speed
            elif keys[K_LEFT]:
                sprite.rect.x -= speed

def damage(player, enemy):
        player._attack = random.randint(100, 600)*(1/player._luck)
        enemy._hp = enemy._hp-player._attack

def battle(player, enemy, screen, clock, FPS, WIDTH, HEIGHT):

    FPS = 60
    
    pos_x = 1
    pos_y = 1

    all_sprites_group = pygame.sprite.Group()
    background_image = load_image('Images/battle_stage.jpg', WIDTH, HEIGHT)
    #---------------------sprites-----------------------
    player_example = sprites.Player('Images/main_character.png', (WIDTH/6, HEIGHT/3), (900, 900), 3, 100)
    enemy.location = (WIDTH-(WIDTH/3), HEIGHT/2)
    enemy.area = (1200, 1200)
    button_attack = sprites.Buttons('attack', (WIDTH/4, HEIGHT-HEIGHT/4))
    button_spell = sprites.Buttons('spell', (WIDTH/2, HEIGHT-HEIGHT/4))
    button_luck = sprites.Buttons('luck', (WIDTH-WIDTH/4, HEIGHT-HEIGHT/4))
    hand = sprites.Hand()
    # Text
    hp_player = sprites.Words(f'Tu vida: {player.hp}', 100, RED, (165, 32))
    hp_enemy = sprites.Words(f'Vida del rival: {enemy.hp}', 100, RED, (1200, 32))


    all_sprites_group.add(player_example, hand, enemy, button_attack, button_spell, button_luck, hp_player, hp_enemy)

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(True)

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        pos_x, pos_y = move(keys, hand, 100, True, pos_x, pos_y)

        #------------------------keyboard-------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        if keys[K_KP_ENTER]:
            if pos_x == 1:
                damage(player, enemy)

        screen.blit(background_image, (0, 0))
        
        all_sprites_group.draw(screen)
        player_example.update()
        enemy.animation()

        hand.update()

        pygame.display.flip() #Actualizar contenido en pantalla


