import pygame, time, random, sys
import function, sprites
from pygame.locals import *
from function import funciones, WIDTH, HEIGHT

def main_stage(FPS, player1, clock):
    function.music('Music/backGround.mp3') #Activa la música de escenario
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creación de la pantalla
    bucle = True

    #-----------------groups-------------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    #-----------------sprites------------------
    background_image = function.load_image('Images/wallBackground.png', WIDTH, HEIGHT+(HEIGHT*(1/5)))
    fight_background = function.load_image('Images/fight 1.png', WIDTH, HEIGHT)
    

    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('Images/enemy.png',( random.randint(((1/2)*WIDTH*(1/60)//1), (WIDTH-(WIDTH*(1/65)//1))), random.randint((WIDTH*(1/6.6)//1), (HEIGHT-WIDTH*(1/6.3)//1))), (350, 350), 20, 10, random.choice(['card', 'bolt']))
        enemy_group.add(enemy) # agregar enemigos al grupo "enemy_groups"

    # Text
    hp = sprites.Words(f'HP {player1.hp}', 30, function.RED, (WIDTH/6, HEIGHT/20), True)
    words_group.add(hp)


    all_sprites_group.add(player1)

    pygame.mouse.set_visible(False)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while bucle:
        collides = None
        clock.tick(FPS)

        #----------------drawing sprites on screen----------------
        screen.blit(background_image, (0, 0))
        all_sprites_group.draw(screen)
        enemy_group.draw(screen)
        words_group.draw(screen)

        #----------------detecting keyboards inputs---------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        #----------------updating sprites on screen-----------------
        all_sprites_group.update()
        enemy_group.update()    
        words_group.update()
        hp.text = f'HP {player1.hp}'

        #--------------------Examinando coliciones------------------
        collides = pygame.sprite.spritecollide(player1, enemy_group, False,)

        if collides:
            player1.collide()
            player1.update()
            pygame.display.flip()
            time.sleep(1)
            screen.blit(fight_background, (0, 0)) #Coloca el fondo de batalla
            pygame.display.flip()

            for collide in collides:
                result = battle(player1, collide, screen, clock)
                if result == 'win!':
                    collide.kill()
            collides.clear()

        print(function.enemys_deleted)
        if function.enemys_deleted == 5:
            bucle = False
        
        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'


def equation(screen, clock, player):
    function.music('Music/equation.mp3') #Activa la música de escenario
    FPS = 60
    tup = funciones[random.randint(0, len(funciones)-1)]
    true_result = tup[1]
    bucle = True
    player_answer = ''
    ok = False

    #----------groups--------------
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    #Backgrounds
    win_background = function.load_image('Images/Correcto!.png', WIDTH, HEIGHT)
    lose_background = function.load_image('Images/Error.png', WIDTH, HEIGHT)
    #Background stars
    for n in range(100):
        star = sprites.Stars()
        stars_group.add(star)
    
    # Buttons
    for number in range(0, 14):
        positions = (
            (2.6, 2), (2, 2), (1.6, 2), 
            (2.6, 1.7), (2, 1.7), (1.6, 1.7), 
            (2.6, 1.49), (2, 1.49), (1.6, 1.49), 
            (2.6, 1.32), (2, 1.32), (1.6, 1.32),
            (1.2, 1.6), (2, 1.18)
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

        elif number == 13:
            ok_button = sprites.Buttons('delete', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(ok_button)

    # Text
    ecuacion = sprites.Words(tup[0],70, function.RED,(WIDTH/2, HEIGHT/6))
    solution = sprites.Words(f'{true_result}', 70, function.RED, (WIDTH/2, HEIGHT/4))
    text_in_screen = sprites.Words(player_answer, 100, function.RED, (WIDTH/8, HEIGHT/3))
    words_group.add(ecuacion, text_in_screen)
   

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(True)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
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

                        elif button.type_button == 'delete':
                            player_answer = player_answer[:-1]
                        
                        elif button.type_button == 'ok':
                            ok = True

        #-------------------update sprites on screen--------------
        stars_group.update()
        buttons_group.update()
        words_group.update()
        text_in_screen.text = f'Tu respuesta: {player_answer}'

        if ok:
            solution.draw(screen)
            solution.update()
            time.sleep(1)
            if true_result == player_answer:
                player.luck += 1
                screen.blit(win_background, (0, 0))
                pygame.display.flip()
                time.sleep(1)
            else:
                player.hp -= 3
                player.luck -= 1
                function.enemys_deleted += 1
                screen.blit(lose_background, (0, 0))
                pygame.display.flip()
                time.sleep(1)
            bucle = False

        pygame.display.flip() #Actualizar contenido en pantalla


def battle(player, enemy, screen, clock):
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

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
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
            
        if player.hp <= 0:
            dead(FPS, clock)
        
        pygame.display.flip() #Actualizar contenido en pantalla

    equation(screen, clock, player)
    function.music('Music/backGround.mp3')
    function.enemys_deleted += 1
    return 'win!'


def Final_battle(player, enemy, screen, clock):
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
    enemy.rect.centerx = WIDTH-(WIDTH/5)
    enemy.rect.centery = HEIGHT/3.5
    enemy._area = (2000, 2000)

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

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
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
                   if player.luck==5:
                       enemy.hp-=30
                   elif player.luck==0:
                       player.hp-=20
                   else:
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
            
        if player.hp <= 0:
            dead(FPS, clock)
        
        pygame.display.flip() #Actualizar contenido en pantalla

    equation(screen, clock, player)
    function.music('Music/backGround.mp3')
    function.enemys_deleted += 1
    return 'win!'


def end_battle(FPS, player1, clock):
    function.music('Music/intro.mp3') #Activa la música de escenario
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creación de la pantalla

    #-----------------groups-------------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    points_group = pygame.sprite.Group()

    #-----------------sprites------------------
    background_image = function.load_image('Images/BackgroundEnd.png', WIDTH, HEIGHT+(HEIGHT*(1/5)), True)
    fight_background = function.load_image('Images/fondo_poker.png', WIDTH, HEIGHT)
    #stars
    for n in range(100):
        star = sprites.Stars()
        stars_group.add(star)

    #points
    for n in range(1000):
        points = sprites.Points()
        points_group.add(points)

    #enemy
    boss = sprites.Boss(WIDTH/2, HEIGHT/2,(450,300))
    enemy_group.add(boss) # agregar enemigos al grupo "enemy_groups"

    # Text
    hp = sprites.Words(f'HP {player1.hp}', 30, function.RED, (WIDTH/6, HEIGHT/20), True)
    words_group.add(hp)


    all_sprites_group.add(player1)

    pygame.mouse.set_visible(False)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while True:
        collides = None
        clock.tick(FPS)

        #----------------drawing sprites on screen----------------
        
        screen.fill(function.colors_list[random.randint(2, len(function.colors_list)-3)])
        stars_group.draw(screen)
        points_group.draw(screen)
        screen.blit(background_image, (0, 0))
        all_sprites_group.draw(screen)
        enemy_group.draw(screen)
        words_group.draw(screen)

        #----------------detecting keyboards inputs---------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        #----------------updating sprites on screen-----------------
        all_sprites_group.update()
        points_group.update()
        enemy_group.update()    
        words_group.update()
        stars_group.update()
        hp.text = f'HP {player1.hp}'

        #--------------------Examinando coliciones------------------
        collides = pygame.sprite.spritecollide(player1, enemy_group, False,)

        if collides:
            player1.collide()
            player1.update()
            pygame.display.flip()
            time.sleep(1)
            screen.blit(fight_background, (0, 0)) #Coloca el fondo de batalla
            pygame.display.flip()

            for collide in collides:
                result = Final_battle(player1, collide, screen, clock)
                if result == 'win!':
                    collide.kill()
            collides.clear()
        
        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'


def dead(FPS, clock):
    function.music('Music/game_over_song.mp3') #Activa la música de escenario
    bucle = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creación de la pantalla

    #-----------------groups-------------------
    words_group = pygame.sprite.Group()

    #-----------------sprites------------------
    game_over_img = function.load_image('Images/Game over.png', 200, 200, True)

    # Text
    end_messenge = sprites.Words('Haz perdido :(', 50, function.WHITE, (WIDTH/2, HEIGHT/1.5))
    words_group.add(end_messenge)

    pygame.mouse.set_visible(False)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while bucle:
        clock.tick(FPS)

        #----------------drawing sprites on screen----------------
        screen.fill(function.BLACK)
        words_group.draw(screen)
        screen.blit(game_over_img, (WIDTH/2, HEIGHT/2))

        #----------------detecting keyboards inputs---------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        #----------------updating sprites on screen----------------- 
        words_group.update()

        
        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'