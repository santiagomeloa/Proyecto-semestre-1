import subprocess, pygame, platform, ctypes, sys, random, time

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

funciones={
    0: ('20 - 7x = 6x - 6', 2),
    1: ('7x + 2 = 10x + 5', -1),
    2: ('6x - 5 = 8x + 2', -7/2),
    3: ('4x + 4 + 9x + 18 = 12 (x+2)', 2),
    4: ('2 - x = x - 8', 5),
    5: ('2x - 1 = 5x + 8', -3),
    6: ('5x - 10 = 10', 4),
    7: ('4y - 5 = 3y + 1', 6),
    8: ('2(2x - 3) = 2x - 10',-2),
    9: ('3x - 4 = 3(2x - 2) - 7', 3),
    10: ('2(t + 2) - 5 = 5(t - 4) + 13', 2)
    }

true_result = 0


def equation(screen, clock):
    FPS = 60
    tup = funciones[random.randint(0, len(funciones))]
    true_result += tup[1]

    background_image = load_image('Images/wallBackground.png', WIDTH, HEIGHT)

    #----------groups--------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    

    # Buttons
    
    
    # Text
    ecuacion = sprites.Words(tup[0],100, RED,(WIDTH/2, HEIGHT/2))

    buttons_group.add()
    words_group.add(ecuacion)
    all_sprites_group.add()

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(True)

    while True:
        clock.tick(FPS)

        #------------------------input events-------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
            #-----????-----
            

        screen.blit(background_image, (0, 0))


        buttons_group.draw(screen)
        words_group.draw(screen)
        all_sprites_group.draw(screen)


    

        
        pygame.display.flip() #Actualizar contenido en pantalla

    
    

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


def damage(player, enemy):
    player.attack = random.randint(100, 600)*(1/player._luck)
    enemy.hp -= player.attack


def battle(player, enemy, screen, clock):
    FPS = 60
    turn_attack = 'player'

    background_image = load_image('Images/battle_stage.jpg', WIDTH, HEIGHT)
    #----------groups--------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    player_example = sprites.Player((WIDTH/6, HEIGHT/3), (900, 900), 3, 100)
    enemy.location = (WIDTH-(WIDTH/3), HEIGHT/2)
    enemy.area = (1200, 1200)

    # Buttons
    button_attack = sprites.Buttons('attack', (WIDTH/4, HEIGHT-HEIGHT/4))
    button_spell = sprites.Buttons('spell', (WIDTH/2, HEIGHT-HEIGHT/4))
    button_luck = sprites.Buttons('luck', (WIDTH-WIDTH/4, HEIGHT-HEIGHT/4))

    # Text
    hp_player = sprites.Words(f'Tu vida {player.hp}', 40, RED, (WIDTH/6, HEIGHT/20))
    hp_enemy = sprites.Words(f'Vida del rival {enemy.hp}', 40, RED, (WIDTH/1.3, HEIGHT/20))


    buttons_group.add(button_attack, button_spell, button_luck)
    words_group.add(hp_enemy, hp_player)
    all_sprites_group.add(player_example, enemy)

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(True)

    while player.hp > 0 or enemy.hp > 0:
        clock.tick(FPS)

        #------------------------input events-------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
            #-----battle-----
            if button_attack.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    damage(player, enemy)
                    turn_attack = 'enemy'
                    pygame.mouse.set_visible(False)

            elif button_spell.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pass

            elif button_luck.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pass

        screen.blit(background_image, (0, 0))
        buttons_group.draw(screen)
        words_group.draw(screen)
        all_sprites_group.draw(screen)

        hp_player.text = f'Tu vida: {player.hp}'
        hp_enemy.text = f'Vida del rival: {enemy.hp}'
        
        player_example.animation('right')
        enemy.animation()
        buttons_group.update()
        words_group.update()

        if enemy.hp <= 0:
            break

        if turn_attack == 'enemy': #Ataque del enemigo
            enemy.damage = random.randint(100, 600)*(1/100)
            player.hp -= enemy.damage
            turn_attack = 'player'
            pygame.mouse.set_visible(True)

        if player.hp <= 0:
            break
        
        pygame.display.flip() #Actualizar contenido en pantalla

    equation(screen,clock)
    return 'win!'


