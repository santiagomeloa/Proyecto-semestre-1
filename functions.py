import subprocess, pygame, platform, ctypes, sys, random
import sprites
from pygame.locals import *

#------------colors-------------
YELLOW = (249, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (16, 19, 115)
DARK_PURPLE = (101, 5, 135)
RED = (255, 3, 0)
MARRON = (109, 4, 4)
list_colors = [YELLOW, GREEN, BLUE, DARK_BLUE, DARK_PURPLE, RED, MARRON]

#-------------functional variables---------------
sistema = platform.system() #Obtiene el sistema operativo del pc desde donde se esté ejecutando

def music(file): # Función para activar la musica que se le pase como parametro (Solo archivos mp3)
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)


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
    global true_result
    FPS = 60
    tup = funciones[random.randint(0, len(funciones)-1)]
    true_result += tup[1]

    #----------groups--------------
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    #background_image = load_image('Images/wallBackground.png', WIDTH, HEIGHT)
    for n in range(100):
        star = sprites.Stars()
        stars_group.add(star)
    
    # Buttons
    
    for number in range(0, 10):
        positions = (
            (2.6, 2), (2, 2), (1.6, 2), 
            (2.6, 1.7), (2, 1.7), (1.6, 1.7), 
            (2.6, 1.49), (2, 1.49), (1.6, 1.49), 
            (2.6, 1.32)
            )
        #for position in positions:
        position = positions[number]
        number_button = sprites.Buttons(number, ((WIDTH/position[0]), HEIGHT/position[1]))
        buttons_group.add(number_button)

    # Text
    ecuacion = sprites.Words(tup[0],70, RED,(WIDTH/2, HEIGHT/6))
    solution=sprites.Words('12000', 70, RED, (WIDTH/2, HEIGHT/4) )
    words_group.add(ecuacion, solution)
   


    pygame.mouse.set_visible(True)
    #pygame.event.set_grab(True)

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
            
        #----------------drawing sprites on screen--------------
        #screen.blit(background_image, (0, 0))
        screen.fill(BLUE)
        stars_group.draw(screen)
        buttons_group.draw(screen)

        words_group.draw(screen)

        #-------------------update sprites on screen--------------
        stars_group.update()
        #buttons_group.update()
        
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

def SpecialDamage(player,enemy):
        player.attack = random.randint(90,160)/player._luck
        enemy.hp -= player.attack
        player._mana-=30
    
def battle(player, enemy, screen, clock):
    FPS = 60
    turn_attack = 'player'
    
    #----------groups--------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    background_image = load_image('Images/battle_stage.png', WIDTH, HEIGHT,True)
    player_example = sprites.Player((WIDTH/6, HEIGHT/3), (900, 900), 3, 100)
    enemy.location = (WIDTH-(WIDTH/5), HEIGHT/3.5)
    enemy.area = (2000, 2000)
    for n in range(100):
        star = sprites.Stars()
        stars_group.add(star)

    # Buttons
    button_attack = sprites.Buttons('attack', (WIDTH/4, HEIGHT-HEIGHT/6))
    button_spell = sprites.Buttons('spell', (WIDTH/2, HEIGHT-HEIGHT/6))
    button_luck = sprites.Buttons('luck', (WIDTH-WIDTH/4, HEIGHT-HEIGHT/6))

    # Text
    hp_player = sprites.Words(f'Tu vida {player.hp}', 40, RED, (WIDTH/6, HEIGHT/20))
    hp_enemy = sprites.Words(f'Vida del rival {enemy.hp}', 40, RED, (WIDTH/1.3, HEIGHT/20))
    potions = sprites.Words(f'Pociones disponibles: {player._potions}', 20, RED, (WIDTH/2, HEIGHT-HEIGHT/9))
    mana = sprites.Words(f'Mana: {player._mana}', 20, BLUE, (WIDTH-WIDTH/4, HEIGHT-HEIGHT/9))
    
    #adding to groups
    buttons_group.add(button_attack, button_spell, button_luck)
    words_group.add(hp_enemy, hp_player, potions, mana)
    all_sprites_group.add(player_example, enemy)

    pygame.mouse.set_visible(True) #Pone el mouse visible
    pygame.event.set_grab(True) #Bloquea el mouse para que no se salga de la pantalla

    music('Music/battle.mp3') #llama a la función que activa la musica

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
                    player._mana+=5
            elif button_spell.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if player._potions>0 and player._hp<100:
                        use_potion(player)
                        turn_attack = 'enemy'
                        pygame.mouse.set_visible(False)
                        player._mana+=5    
            elif button_luck.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and player._mana>=30:
                    SpecialDamage(player,enemy)
                    turn_attack = 'enemy'
                    pygame.mouse.set_visible(False)

        #------------drawing sprites on screen------------
        screen.fill(DARK_BLUE)
        stars_group.draw(screen)
        screen.blit(background_image, (0, 0))
        buttons_group.draw(screen)
        words_group.draw(screen)
        all_sprites_group.draw(screen)

        #-------------update sprites on screen--------------
        hp_player.text = f'Tu vida: {player.hp}'
        hp_enemy.text = f'Vida del rival: {enemy.hp}'
        if player._potions>0: 
            potions.text = f"Pociones disponibles: {player._potions}"
        else:
            potions.text=f'No se puede curar'
        if (player._mana-30)>=0: 
            mana.text = f'Mana: {player._mana}'
        else:
            mana.text = f'Sin mana suficiente'
        
        
        player_example.animation('right')
        enemy.animation()
        buttons_group.update()
        words_group.update()
        stars_group.update()

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
    solution= equation(screen,clock)
    return 'win!'

def use_potion(player):
    if player.hp<100 and player.hp>=80 and player._potions>0:
        player.hp=100
        player._potions-=1
    elif player.hp<80 and player._potions>0:
        player.hp+=20
        player._potions-=1

