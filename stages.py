import pygame, time, random, sys
import function, sprites
from pygame.locals import *
from function import funciones, WIDTH, HEIGHT

def main_stage(FPS):
    function.music('Music/backGround.mp3')
    screen = pygame.display.set_mode((function.WIDTH, function.HEIGHT))
    clock = pygame.time.Clock()

    #-----------------groups-------------------
    all_sprites_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    #-----------------sprites------------------
    background_image = function.load_image('Images/wallBackground.png', function.WIDTH, function.HEIGHT+(function.HEIGHT*(1/5)))
    player1 = sprites.Player((200, 500), (300, 300), 100, 100)
    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('Images/enemy.png',(random.randint(0, function.WIDTH), random.randint(0, function.HEIGHT/3)), (350, 350), 20, 10, random.choice(['card', 'bolt']))
        enemy_group.add(enemy)

    # Text
    hp = sprites.Words(f'HP {player1.hp}', 30, function.RED, (function.WIDTH/6, function.HEIGHT/20), True)
    all_sprites_group.add(hp)
    all_sprites_group.add(player1)

    pygame.mouse.set_visible(False)

    while True:
        collides = None
        clock.tick(FPS)

        #----------------drawing sprites on screen----------------
        screen.blit(background_image, (0, 0))
        all_sprites_group.draw(screen)
        enemy_group.draw(screen)

        #----------------detecting keyboards inputs---------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
        
        all_sprites_group.update()
        enemy_group.update()

        #--------------------Examinando coliciones------------------
        collides = pygame.sprite.spritecollide(player1, enemy_group, False,)
        if collides:
            player1.collide()
            for collide in collides:
                result = battle(player1, collide, screen, clock)
                time.sleep(1)
                if result == 'win!':
                    collide.kill()
            collides.clear()
            
        if function.player_hits == 5:
            pass
        
        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

def equation(screen, clock, player):
    function.music('Music/equation.mp3')
    FPS = 60
    tup = funciones[random.randint(0, len(funciones)-1)]
    true_result = tup[1]

    #----------groups--------------
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    for n in range(100):
        star = sprites.Stars()
        stars_group.add(star)
    
    # Buttons
    for number in range(0, 13):
        positions = (
            (2.6, 2), (2, 2), (1.6, 2), 
            (2.6, 1.7), (2, 1.7), (1.6, 1.7), 
            (2.6, 1.49), (2, 1.49), (1.6, 1.49), 
            (2.6, 1.32), (2, 1.32), (1.6, 1.32),
            (1.2, 1.6)
            )
        position = positions[number]

        if number <= 9:
            number_button = sprites.Buttons(number, (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(number_button)

        elif number == 10:
            number_button = sprites.Buttons('minius', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(number_button)

        elif number == 11:
            number_button = sprites.Buttons('split', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(number_button)

        elif number == 12:
            ok_button = sprites.Buttons('ok', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(ok_button)

    # Text
    ecuacion = sprites.Words(tup[0],70, function.RED,(WIDTH/2, HEIGHT/6))
    solution = sprites.Words(f'{true_result}', 70, function.RED, (WIDTH/2, HEIGHT/4))
    words_group.add(ecuacion)
   

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(True)

    player_answer = ''
    bucle = True

    while bucle:
        clock.tick(FPS)

        #----------------drawing sprites on screen--------------
        #screen.blit(background_image, (0, 0))
        screen.fill(function.BLUE)
        stars_group.draw(screen)
        buttons_group.draw(screen)
        words_group.draw(screen)

        #------------------------input events-------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
            #-----buttons input-----
            for button in buttons_group:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:

                        if type(button.type_button) == int:
                            for numb in range(12):
                                if numb == button.type_button:
                                    player_answer += str(button.type_button)

                        elif button.type_button == 'minius':
                            player_answer += '-'

                        elif button.type_button == 'split':
                            player_answer += '/'
                        
                        elif button.type_button == 'ok':
                            solution.draw(screen)
                            if true_result == player_answer:
                                player.luck += 1
                                function.player_hits += 1
                            else:
                                player.hp -= 3
                                player.luck -= 1
                            solution.update()
                            time.sleep(1)
                            bucle = False

        #-------------------update sprites on screen--------------
        stars_group.update()
        buttons_group.update()

        pygame.display.flip() #Actualizar contenido en pantalla

def battle(player, enemy, screen, clock):
    global player_result
    FPS = 60
    turn_attack = 'player'
    function.music('Music/battle.mp3') #llama a la función que activa la musica
    
    #----------groups--------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    player_example = sprites.Player((WIDTH/6, HEIGHT/3), (900, 900), 3, 100)
    for n in range(100):
        star = sprites.Stars()
        stars_group.add(star)
    #images
    background_image = function.load_image('Images/battle_stage.png', WIDTH, HEIGHT,True)
    hit = function.load_image('Images/golpe.png', 200, 80, True)
    enemy.location = (WIDTH-(WIDTH/5), HEIGHT/3.5)
    enemy.area = (2000, 2000)

    # Buttons
    button_attack = sprites.Buttons('attack', (WIDTH/4, HEIGHT-HEIGHT/6))
    button_spell = sprites.Buttons('spell', (WIDTH/2, HEIGHT-HEIGHT/6))
    button_luck = sprites.Buttons('luck', (WIDTH-WIDTH/4, HEIGHT-HEIGHT/6))

    # Text
    hp_player = sprites.Words(f'Tu vida {player.hp}', 40, function.RED, (WIDTH/6, HEIGHT/20))
    hp_enemy = sprites.Words(f'Vida del rival {enemy.hp}', 40, function.RED, (WIDTH/1.3, HEIGHT/20))
    potions = sprites.Words(f'Pociones disponibles: {player._potions}', 20, function.RED, (WIDTH/2, HEIGHT-HEIGHT/9))
    mana = sprites.Words(f'Mana: {player._mana}', 20, function.BLUE, (WIDTH-WIDTH/4, HEIGHT-HEIGHT/9))
    
    #adding to groups
    buttons_group.add(button_attack, button_spell, button_luck)
    words_group.add(hp_enemy, hp_player, potions, mana)
    all_sprites_group.add(player_example, enemy)

    pygame.mouse.set_visible(True) #Pone el mouse visible
    pygame.event.set_grab(True) #Bloquea el mouse para que no se salga de la pantalla


    while player.hp > 0 or enemy.hp > 0: # Bucle principal
        clock.tick(FPS)

        #------------drawing sprites on screen------------
        screen.fill(function.DARK_BLUE)
        stars_group.draw(screen)
        screen.blit(background_image, (0, 0))

        buttons_group.draw(screen)
        words_group.draw(screen)
        all_sprites_group.draw(screen)

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
                    #screen.blit(hit, (WIDTH-(WIDTH/5), HEIGHT/3.5))
                    function.damage(player, enemy)
                    turn_attack = 'enemy'
                    pygame.mouse.set_visible(False)
                    player._mana+=5

            elif button_spell.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if player._potions>0 and player._hp<100:
                        function.use_potion(player)
                        turn_attack = 'enemy'
                        pygame.mouse.set_visible(False)
                        player._mana+=5

            elif button_luck.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and player._mana>=30:
                    function.SpecialDamage(player,enemy)
                    turn_attack = 'enemy'
                    pygame.mouse.set_visible(False)


        #-------------update sprites on screen--------------
        hp_player.text = f'Tu vida: {player.hp}'
        hp_enemy.text = f'Vida del rival: {enemy.hp}'
        if player._potions > 0: 
            potions.text = f"Pociones disponibles: {player._potions}"
        else:
            potions.text=f'No se puede curar'

        if (player._mana-30) >= 0: 
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
            #del hit
            
        if player.hp <= 0:
            break
        
        pygame.display.flip() #Actualizar contenido en pantalla

    equation(screen, clock, player)
    function.music('Music/backGround.mp3')
    return 'win!'

