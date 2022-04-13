import pygame
import sys, os
from pygame.locals import *
import funtions, sprites


FPS = 60

def main():
    screen = pygame.display.set_mode((sprites.WIDTH, sprites.HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Prueba de juego')
    background_image = funtions.load_image('images/wallBackground.jpg', sprites.WIDTH, sprites.HEIGHT)

    all_sprites_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    player1 = sprites.Player('images/main_character.png', (100, 100), 3, 100, 100)



    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('images/enemy.png', (50,50), 20, 10)
        enemy_group.add(enemy)


    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        
        screen.blit(background_image, (0, 0))
        funtions.move(keys, player1)
        player1.update()
        enemy_group.update()

        
        collide = pygame.sprite.spritecollide(player1, enemy_group, False)
        if collide:
            player1.hp -= 1
            if player1.hp < 0:
                player1.kill()
        
        player1.draw(screen)

        enemy_group.draw(screen)

        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

if __name__ == '__main__':
    pygame.init()
    main()