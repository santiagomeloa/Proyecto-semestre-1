import pygame
import sys, time
from pygame.locals import *
import funtions
import sprites

#-------Tamaño de la pantalla------


FPS = 120

def main():
    screen = pygame.display.set_mode((funtions.WIDTH, funtions.HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Bad dice')

    background_image = funtions.load_image('Images/wallBackground.jpg', funtions.WIDTH, funtions.HEIGHT)

    all_sprites_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    player1 = sprites.Player('Images/main_character.png', (200, 500), (100, 100), 3, 100)
    all_sprites_group.add(player1)


    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('Images/enemy.png', (50,50), 20, 10)
        enemy_group.add(enemy)


    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        
        screen.blit(background_image, (0, 0))
        funtions.move(keys, player1, 5)
        all_sprites_group.update()
        enemy_group.update()

        
        collide = pygame.sprite.spritecollide(player1, enemy_group, False)
        #if collide:
        #    time.sleep(2)
        #    funtions.battle(player1, enemy, screen, clock, FPS, funtions.WIDTH, funtions.HEIGHT)
            
        
        all_sprites_group.draw(screen)

        enemy_group.draw(screen)

        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

if __name__ == '__main__':
    pygame.init()
    main()