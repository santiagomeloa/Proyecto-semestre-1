import pygame
import sys, time, random
from pygame.locals import *
import functions
import sprites


FPS = 60

def main():
    screen = pygame.display.set_mode((functions.WIDTH, functions.HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Bad dice')


    background_image = functions.load_image('Images/wallBackground.png', functions.WIDTH, functions.HEIGHT+(functions.HEIGHT*(1/5)))
    #-----------------groups-------------------
    all_sprites_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    #-----------------sprites------------------
    player1 = sprites.Player((200, 500), (300, 300), 100, 100)
    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('Images/enemy.png',(random.randint(0, functions.WIDTH), random.randint(0, functions.HEIGHT/3)), (350, 350), 20, 10, random.choice(['card', 'bolt']))
        enemy_group.add(enemy)

    # Text
    hp = sprites.Words(f'HP {player1.hp}', 30, functions.RED, (functions.WIDTH/6, functions.HEIGHT/20), True)

    all_sprites_group.add(hp)
    all_sprites_group.add(player1)


    pygame.mouse.set_visible(False)


    while True:
        collides = None
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
        screen.blit(background_image, (0, 0))
        #screen.blit(vida, (0, 0))
        #screen.blit(hp, (70, 0))

        #functions.move(keys, player1, 5)
        all_sprites_group.draw(screen)
        enemy_group.draw(screen)


        all_sprites_group.update()
        enemy_group.update()

        
        #pygame.font.init()

        
        
        collides = pygame.sprite.spritecollide(player1, enemy_group, False,)
        if collides:
            player1.collide()
            for collide in collides:
                result = functions.battle(player1, collide, screen, clock)
                time.sleep(1)
                if result == 'win!':
                    collide.kill()
            collides.clear()
            
        


        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

if __name__ == '__main__':
    pygame.init()
    main()