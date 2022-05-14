import subprocess, pygame, platform, ctypes, sys, random
from pygame.locals import *

#------------colors-------------
WHITE = (255, 255, 255)
YELLOW = (249, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (16, 19, 115)
DARK_PURPLE = (101, 5, 135)
RED = (255, 3, 0)
MARRON = (109, 4, 4)
BLACK = (0, 0, 0)
colors_list = [YELLOW, GREEN, BLUE, DARK_BLUE, DARK_PURPLE, RED, MARRON, BLACK]

#-------------functional variables---------------
sistema = platform.system() #Obtiene el sistema operativo del pc desde donde se esté ejecutando

enemys_deleted = 0 #Variable para saber cuantos enemigos se han eliminado

def music(file): # Función para activar la musica que se le pase como parametro (Solo archivos mp3)
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)


funciones={
    0: ('20 - 7x = 6x - 6', '2'),
    1: ('7x + 2 = 10x + 5', '-1'),
    2: ('6x - 5 = 8x + 2', '-7/2'),
    3: ('4x + 4 + 9x + 18 = 12 (x+2)', '2'),
    4: ('2 - x = x - 8', '5'),
    5: ('2x - 1 = 5x + 8', '-3'),
    6: ('5x - 10 = 10', '4'),
    7: ('4y - 5 = 3y + 1', '6'),
    8: ('2(2x - 3) = 2x - 10', '-2'),
    9: ('3x - 4 = 3(2x - 2) - 7', '3'),
    10: ('2(t + 2) - 5 = 5(t - 4) + 13', '2')
    }


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
    player.attack = random.randint(100, 600)*(1/player.luck)
    enemy.hp -= player.attack

def SpecialDamage(player,enemy):
        player.attack = random.randint(1,6)*10/player.luck
        enemy.hp -= player.attack
        player.mana -= 30
    
def use_potion(player):
    if player.hp<100 and player.hp>=80 and player._potions>0:
        player.hp=100
        player._potions-=1
    elif player.hp<80 and player._potions>0:
        player.hp+=20
        player._potions-=1

def movement():
    point=random.randint(-50, 50)
    return point