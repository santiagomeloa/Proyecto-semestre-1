import pygame, sys
from pygame.locals import *
import function, sprites, stages

from function import WIDTH, HEIGHT

FPS = 60

def main():
    function.music('Music/intro.mp3')
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Bad dice')

    #-----------------groups-------------------
    buttons_group = pygame.sprite.Group()

    #-----------------sprites------------------
    play_button = sprites.Buttons('play', (WIDTH/2, HEIGHT/2))
    background_image = function.load_image(
        'Images/menu_screen.jpeg', WIDTH, HEIGHT
        )


    # Text
   
    #adding sprites to groups
    buttons_group.add(play_button)

    pygame.mouse.set_visible(True)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
            if play_button.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    stages.main_stage(FPS)

        screen.blit(background_image, (0, 0))
        play_button.draw(screen)
        play_button.update()

        
        pygame.display.flip() #Actualizar contenido en pantalla

if __name__ == '__main__':
    pygame.init()
    main()