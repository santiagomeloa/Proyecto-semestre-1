import subprocess, pygame, platform, ctypes, sprites, random
from pygame.locals import *

sistema = platform.system() #Obtiene el sistema operativo del pc desde donde se esté ejecutando


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


def load_image(filename, width=None, height=None, transparent=False): #covierte las imagenes, les da las dimenciones deceadas y les quita el fondo
    try: imagen = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit
        
    if width != None or height != None:
        imagen = pygame.transform.scale(imagen, (width, height))

    imagen = imagen.convert()
    if transparent:
        #color = image.get_at((0, 0))
        color = pygame.PixelArray(imagen)
        imagen.set_colorkey(color[0, 0], RLEACCEL)
    return imagen


def move(keys, sprite):  #Permite el movimiento del personaje principal
    if keys[K_LEFT]:
        sprite.rect.x -= 5
        if keys[K_UP]:
            sprite.rect.y -= 5
        elif keys[K_DOWN]:
            sprite.rect.y += 5

    elif keys[K_RIGHT]:
        sprite.rect.x += 5
        if keys[K_UP]:
            sprite.rect.y -= 5
        elif keys[K_DOWN]:
            sprite.rect.y += 5
        
    elif keys[K_UP]:
        sprite.rect.y -= 5
        if keys[K_RIGHT]:
            sprite.rect.x += 5
        elif keys[K_LEFT]:
            sprite.rect.x -= 5

    elif keys[K_DOWN]:
        sprite.rect.y += 5
        if keys[K_RIGHT]:
            sprite.rect.x += 5
        elif keys[K_LEFT]:
            sprite.rect.x -= 5

