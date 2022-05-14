import pygame, sys
from pygame.locals import *
import function, sprites, stages

from function import WIDTH, HEIGHT

FPS = 60

def main():
    function.music('Music/intro.mp3') #Activa la música de escenario
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Bad dice')

    #-----------------groups-------------------
    buttons_group = pygame.sprite.Group()

    #-----------------sprites------------------
    #buttons
    play_button = sprites.Buttons('play', (WIDTH/2, HEIGHT/2))

    #Player
    player1 = sprites.Player((200, 500), (300, 300), 50, 100)

    background_image = function.load_image(
        'Images/menu_screen.jpeg', WIDTH, HEIGHT
        )

    # Text
   
    #adding sprites to groups
    buttons_group.add(play_button)

    pygame.mouse.set_visible(True)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while True:
        clock.tick(FPS)
        #-------------drawing sprites on screen--------------
        screen.blit(background_image, (0, 0))
        play_button.draw(screen)

        #-------------detecting keyboards inputs-------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
            if play_button.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and function.enemys_deleted != 5:
                    stages.main_stage(FPS, player1, clock)
                    

        #--------------update sprites on screen---------------
        play_button.update()

        if function.enemys_deleted == 5:
            stages.end_battle(FPS, player1, clock)

        pygame.display.flip() #Actualizar contenido en pantalla

if __name__ == '__main__':
    pygame.init()
    main()
    