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
    fuente = pygame.font.Font(None, 50)

    background_image = functions.load_image('Images/wallBackground.png', functions.WIDTH, functions.HEIGHT+(functions.HEIGHT*(1/5)))

    all_sprites_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    player1 = sprites.Player('Images/main_character.png', (200, 500), (300, 300), 3, 100)
    all_sprites_group.add(player1)

    #-----------------------texto en pantalla-------------------------
    hp = sprites.Words(f'{player1.hp}', 50, functions.RED, (70, 20))
    life = sprites.Words('HP: ', 50, functions.RED, (30, 20))
    #life = fuente.render('Hp: ', 1, funtions.RED)
    all_sprites_group.add(life, hp)

    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('Images/enemy.png',(random.randint(0, functions.WIDTH/3), random.randint(0, functions.HEIGHT/3)), (350, 350), 20, 10, random.choice(['card', 'bolt']))
        enemy_group.add(enemy)

    pygame.mouse.set_visible(False)
    
    while True:
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

        functions.move(keys, player1, 5)
        all_sprites_group.draw(screen)
        enemy_group.draw(screen)


        all_sprites_group.update()
        enemy_group.update()

        
        #pygame.font.init()

        
        collide = pygame.sprite.spritecollide(player1, enemy_group, False)
        if collide:
            player1.collide()
            time.sleep(1)
            functions.battle(player1, enemy, screen, clock, FPS, functions.WIDTH, functions.HEIGHT)
            
        


        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

if __name__ == '__main__':
    pygame.init()
    main()