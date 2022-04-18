import pygame
import sys, time
from pygame.locals import *
import functions
import sprites


FPS = 60

def main():
    screen = pygame.display.set_mode((functions.WIDTH, functions.HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Bad dice')
    fuente = pygame.font.Font(None, 50)

    background_image = functions.load_image('Images/wallBackground.jpg', functions.WIDTH, functions.HEIGHT)

    all_sprites_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    player1 = sprites.Player('Images/main_character.png', (200, 500), (100, 100), 3, 100)
    all_sprites_group.add(player1)

    #-----------------------texto en pantalla-------------------------
    hp = sprites.Words(f'{player1.hp}', 50, functions.RED, (70, 20))
    life = sprites.Words('HP: ', 50, functions.RED, (30, 20))
    #life = fuente.render('Hp: ', 1, funtions.RED)
    all_sprites_group.add(life, hp)

    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('Images/enemy.png', (50,50), 20, 10)
        enemy_group.add(enemy)


    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        
        screen.blit(background_image, (0, 0))
        #screen.blit(vida, (0, 0))
        #screen.blit(hp, (70, 0))

        functions.move(player1, 5)
        all_sprites_group.update()
        enemy_group.update()

        
        #pygame.font.init()

        
        collide = pygame.sprite.spritecollide(player1, enemy_group, False)
        if collide:
            time.sleep(2)
            functions.battle(player1, enemy, screen, clock, FPS, functions.WIDTH, functions.HEIGHT)
            
        
        all_sprites_group.draw(screen)

        enemy_group.draw(screen)

        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

if __name__ == '__main__':
    pygame.init()
    main()