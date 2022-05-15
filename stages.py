'''
Cualquier variable que contenga _group en su nombre se usará para guardar sprites, y posteriormente 
ser llamada para mandar una instrucción general a dichos sprites
Cualquier variable que contenga _bacground o _battle y no sea una funcion se usará para generar un
fondo.

'''
import pygame, time, random, sys
import function, sprites
from pygame.locals import *
from function import funciones, WIDTH, HEIGHT

def main_stage(FPS, player1, clock): #Este es el escenario donde comieza el juego y las batallas normales
    function.music('Music/backGround.mp3') #Activa la música de escenario
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creación de la pantalla
    bucle = True

    #-----------------groups-------------------
    all_sprites_group = pygame.sprite.Group()#creacion de grupos para llamados generales de variables
    words_group = pygame.sprite.Group()#creacion de grupos para llamados generales de variables
    enemy_group = pygame.sprite.Group()#creacion de grupos para llamados generales de variables

    #-----------------sprites------------------
    background_image = function.load_image('Images/wallBackground.png', WIDTH, HEIGHT+(HEIGHT*(1/5)))#coloca una imagen de fondo
    fight_background = function.load_image('Images/fight 1.png', WIDTH, HEIGHT)#coloca la imagen usada de fondo para las batallas
    

    for n in range(5): #Cración de enemigos
        enemy = sprites.Bicho('Images/enemy.png',( random.randint(((1/2)*WIDTH*(1/60)//1), (WIDTH-(WIDTH*(1/65)//1))), random.randint((WIDTH*(1/6.6)//1), (HEIGHT-WIDTH*(1/6.3)//1))), (350, 350), 20, 10, random.choice(['card', 'bolt']))
        enemy_group.add(enemy) # agregar enemigos al grupo "enemy_groups"

    # Text
    hp = sprites.Words(f'HP {player1.hp}', 30, function.RED, (WIDTH/6, HEIGHT/20), True)#crea un objeto que muestra la informacion
    words_group.add(hp)#añade al grupo


    all_sprites_group.add(player1)

    pygame.mouse.set_visible(False)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while bucle:
        collides = None
        clock.tick(FPS)

        #----------------drawing sprites on screen----------------
        screen.blit(background_image, (0, 0))#actualiza la pantalla
        all_sprites_group.draw(screen) #hace que se muestren la imagen del objeto
        enemy_group.draw(screen) #hace que se muestren la imagen del objeto
        words_group.draw(screen) #hace que se muestren la imagen del objeto

        #----------------detecting keyboards inputs---------------
        for event in pygame.event.get(): #se usa para cerrar el juego con la tecla scape
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        #----------------updating sprites on screen-----------------
        all_sprites_group.update() #actualiza los sprites
        enemy_group.update()    
        words_group.update()
        hp.text = f'HP {player1.hp}'

        #--------------------Examinando coliciones------------------
        collides = pygame.sprite.spritecollide(player1, enemy_group, False,)

        if collides: #cuando detecta que las posiciones de dos objetos se sobreponen, los envia a una tupla
            player1.collide()
            player1.update()
            pygame.display.flip()
            time.sleep(1)
            screen.blit(fight_background, (0, 0)) #Coloca el fondo de batalla
            pygame.display.flip()

            for collide in collides: #envía el enemigo a la funcion battle.
                result = battle(player1, collide, screen, clock)
                if result == 'win!':
                    collide.kill()
            collides.clear()

        if function.enemys_deleted == 5: #verifica la cantidad de enemigos derrotados y, si son todos los enemigos, termina el bucle
            bucle = False
        
        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

def equation(screen, clock, player):#Este es el escenario en el cual se muestra la ecuación y se pide solucionarla
    function.music('Music/equation.mp3') #Activa la música de escenario
    FPS = 60
    tup = funciones[random.randint(0, len(funciones)-1)] #recupera la funcion

    true_result = tup[1] #recupera el resultado de la ecuación
    bucle = True
    player_answer = '' # variable para guardar la respuesta del jugador
    verificate = False #variable para verificar el ingreso de la respuesta

    #----------groups--------------
    words_group = pygame.sprite.Group() 
    buttons_group = pygame.sprite.Group() 
    stars_group = pygame.sprite.Group() 
    
    #---------------------sprites-----------------------
    #Backgrounds
    win_background = function.load_image('Images/Correcto!.png', WIDTH, HEIGHT)
    lose_background = function.load_image('Images/Error.png', WIDTH, HEIGHT)
    #Background stars
    for n in range(100): #crea las estrellas que se usarán para el fondo del escenario
        star = sprites.Stars()
        stars_group.add(star)
    
    # Buttons
    for number in range(0, 14):
        positions = ( #lista de posiciones para los botones
            (2.6, 2), (2, 2), (1.6, 2), 
            (2.6, 1.7), (2, 1.7), (1.6, 1.7), 
            (2.6, 1.49), (2, 1.49), (1.6, 1.49), 
            (2.6, 1.32), (2, 1.32), (1.6, 1.32),
            (1.2, 1.6), (2, 1.18)
            )
        position = positions[number]

        if number <= 9:#genera los botones de los numeros del 1 al 9
            number_button = sprites.Buttons(number, (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(number_button)#añade los sprites al grupo

        elif number == 10: #genera el boton menos
            number_button = sprites.Buttons('minius', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(number_button)#añade los sprites al grupo

        elif number == 11: #genera el boton de division
            number_button = sprites.Buttons('split', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(number_button)#añade los sprites al grupo

        elif number == 12: #genera el boton ok
            ok_button = sprites.Buttons('ok', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(ok_button)#añade los sprites al grupo

        elif number == 13: #genera el boton de borrar
            ok_button = sprites.Buttons('delete', (WIDTH/position[0], HEIGHT/position[1]))
            buttons_group.add(ok_button) #añade los sprites al grupo

    # Text
    ecuacion = sprites.Words(tup[0],70, function.RED,(WIDTH/2, HEIGHT/6)) #genera el texto de la ecuacion
    solution = sprites.Words(f'{true_result}', 70, function.RED, (WIDTH/2, HEIGHT/4)) #genera el texto de la solución real
    text_in_screen = sprites.Words(player_answer, 100, function.RED, (WIDTH/8, HEIGHT/3)) #genera el texto donde aparecerá la respuesta del jugador
    words_group.add(ecuacion, text_in_screen) #añade los sprites al grupo
   

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(True)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while bucle:
        clock.tick(FPS)

        #----------------drawing sprites on screen--------------
        #screen.blit(background_image, (0, 0))
        screen.fill(function.BLUE)# coloca un fondo azul
        stars_group.draw(screen) #muestra los objetos del grupo en pantalla
        buttons_group.draw(screen)#muestra los objetos del grupo en pantalla
        words_group.draw(screen)#muestra los objetos del grupo en pantalla

        #------------------------input events-------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
            #-----buttons input-----
            for button in buttons_group: #revisa si alguno de los botones es presionado
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
                            verificate = True

        #-------------------update sprites on screen--------------
        stars_group.update() #actualiza los objetos del grupo
        buttons_group.update() #actualiza los objetos del grupo
        words_group.update() #actualiza los objetos del grupo
        text_in_screen.text = f'Tu respuesta: {player_answer}' #actualiza el texto en pantalla

        if verificate:
            solution.draw(screen)
            solution.update()
            time.sleep(1)
            if true_result == player_answer:
                player.luck += 1
                screen.blit(win_background, (0, 0))# actualiza el fondo para mostrar la pantalla de correcto
                pygame.display.flip() #actualiza la pantalla
                time.sleep(1) #hace que el programa espere 1 segundo 
            else:
                player.hp -= 3
                player.luck -= 1
                screen.blit(lose_background, (0, 0)) # actualiza el fondo para mostrar la pantalla de error
                pygame.display.flip()#actualiza la pantalla
                time.sleep(1) #hace que el programa espere 1 segundo 
            bucle = False
        
        pygame.display.flip() #Actualizar contenido en pantalla

def battle(player, enemy, screen, clock):  #Esta función carga el scenario de batalla
    FPS = 60
    turn_attack = 'player'
    function.music('Music/battle.mp3') #llama a la función que activa la musica
    
    #----------groups--------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------
    player_example = sprites.Player((WIDTH/6, HEIGHT/3), (900, 900), 3, 100) #genera un sprite del jugador
    for n in range(100): #genera las estrellas que serán utilizadas luego en el fondo
        star = sprites.Stars()
        stars_group.add(star)
    #images
    background_image = function.load_image('Images/battle_stage.png', WIDTH, HEIGHT,True)
    enemy.location = (WIDTH-(WIDTH/5), HEIGHT/3.5)#coloca al enemigo en la posición
    enemy.area = (2000, 2000)#aumenta el area del enemigo

    # Buttons
    button_attack = sprites.Buttons('attack', (WIDTH/4, HEIGHT-HEIGHT/6)) #crea el boton de ataque
    button_spell = sprites.Buttons('spell', (WIDTH/2, HEIGHT-HEIGHT/6))#crea el boton de spell
    button_luck = sprites.Buttons('luck', (WIDTH-WIDTH/4, HEIGHT-HEIGHT/6))#crea el boton de luck

    # Text
    hp_player = sprites.Words(f'Tu vida {player.hp}', 40, function.RED, (WIDTH/6, HEIGHT/20)) #crea un obeto para mostrar la información
    hp_enemy = sprites.Words(f'Vida del rival {enemy.hp}', 40, function.RED, (WIDTH/1.3, HEIGHT/20))#crea un obeto para mostrar la información
    potions = sprites.Words(f'Pociones disponibles: {player._potions}', 20, function.RED, (WIDTH/2, HEIGHT-HEIGHT/9))#crea un obeto para mostrar la información
    mana = sprites.Words(f'Mana: {player._mana}', 20, function.BLUE, (WIDTH-WIDTH/4, HEIGHT-HEIGHT/9))#crea un obeto para mostrar la información
    
    #adding to groups
    buttons_group.add(button_attack, button_spell, button_luck)#añade los sprites al grupo
    words_group.add(hp_enemy, hp_player, potions, mana)#añade los sprites al grupo
    all_sprites_group.add(player_example, enemy)#añade los sprites al grupo

    pygame.mouse.set_visible(True) #Pone el mouse visible
    pygame.event.set_grab(True) #Bloquea el mouse para que no se salga de la pantalla

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while player.hp > 0 or enemy.hp > 0: # Bucle principal
        clock.tick(FPS)

        #------------drawing sprites on screen------------
        screen.fill(function.DARK_BLUE) #coloca un color azul oscuro de fondo
        stars_group.draw(screen)#situa las estrellas en el fondo
        screen.blit(background_image, (0, 0))#actualiza el fondo de la pantalla

        buttons_group.draw(screen)#muestra los objetos del grupo en pantalla
        words_group.draw(screen)#muestra los objetos del grupo en pantalla
        all_sprites_group.draw(screen)#muestra los objetos del grupo en pantalla

        #------------------------input events-------------------------
        for event in pygame.event.get():
            if event.type == QUIT:#cierra el programa cuando se presiona esc
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

            #-----battle-----
            if button_attack.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:#mira si el boton presionado es attack
                    function.damage(player, enemy)#llama a la funcion damage
                    turn_attack = 'enemy'#coloca el turno del enemigo
                    pygame.mouse.set_visible(False)#se hace invisible el mouse
                    player._mana+=5

            elif button_spell.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if player._potions>0 and player._hp<100: 
                        function.use_potion(player) #llama a la funcion use_potion
                        turn_attack = 'enemy'#coloca el turno del enemigo
                        pygame.mouse.set_visible(False)
                        player._mana+=5

            elif button_luck.rect.collidepoint(pygame.mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and player._mana>=30:
                    function.SpecialDamage(player,enemy) #llama a la funcion SpecialDamage
                    turn_attack = 'enemy'#coloca el turno del enemigo
                    pygame.mouse.set_visible(False)


        #-------------update sprites on screen--------------
        hp_player.text = f'Tu vida: {player.hp}'#muestra la vida del jugador
        hp_enemy.text = f'Vida del rival: {enemy.hp}'#muestra la vida del rival
        if player._potions > 0: 
            potions.text = f"Pociones disponibles: {player._potions}"#muestra el numero de pociones
        else:
            potions.text=f'No se puede curar'

        if (player._mana-30) >= 0: 
            mana.text = f'Mana: {player._mana}'#muestra el mana restante
        else:
            mana.text = f'Sin mana suficiente'
        
        player_example.animation('right')
        enemy.animation()
        buttons_group.update()#actualiza los sprites
        words_group.update()#actualiza los sprites
        stars_group.update()#actualiza los sprites

        if enemy.hp <= 0:
            break

        if turn_attack == 'enemy': #Ataque del enemigo
            enemy.damage = random.randint(100, 600)*(1/100)
            player.hp -= enemy.damage
            turn_attack = 'player'#cambia el turno al jugador
            pygame.mouse.set_visible(True)
            
        if player.hp <= 0:
            dead(FPS, clock)#llama a la funcion dead
        
        pygame.display.flip() #Actualizar contenido en pantalla

    equation(screen, clock, player) #llama a la funcion ecuation
    function.music('Music/backGround.mp3')
    function.enemys_deleted += 1 #registra la desaparición del enemigo en cuestión.
    return 'win!'

def end_scenario(FPS, player1, clock):
    function.music('Music/intro.mp3') #Activa la música de escenario
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creación de la pantalla

    #-----------------groups-------------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    points_group = pygame.sprite.Group()

    #-----------------sprites------------------
    background_image = function.load_image('Images/fondo_poker.png', WIDTH, HEIGHT)
    fight_background = function.load_image('Images/battle_stage.png', WIDTH, HEIGHT)
    
    #stars
    for n in range(100): #crea las estrellas para el fondo
        star = sprites.Stars()
        stars_group.add(star) #añade las estrellas al grupo

    #points
    for n in range(100): #crea los puntos para el fondo
        points = sprites.Points()
        points_group.add(points) #añade los puntos al grupo

    #enemy
    
    boss = sprites.Boss(WIDTH/2, HEIGHT/2.2,(450,300))
    enemy_group.add(boss) # agregar enemigos al grupo "enemy_groups"
    
    # Text
    hp = sprites.Words(f'HP {player1.hp}', 30, function.RED, (WIDTH/6, HEIGHT/20), True)
    words_group.add(hp)#añade el sprite al grupo
    
    all_sprites_group.add(player1) #añade el sprite al grupo

    pygame.mouse.set_visible(False)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while True:
        collides = None
        clock.tick(FPS)

        #----------------drawing sprites on screen----------------
        
        screen.fill(function.colors_list[random.randint(2, len(function.colors_list)-3)])#llena el fondo de un color aleatorio
        stars_group.draw(screen) #muestra los objetos del grupo en pantalla
        points_group.draw(screen) #muestra los objetos del grupo en pantalla
        screen.blit(background_image, (0, 0))
        all_sprites_group.draw(screen) #muestra los objetos del grupo en pantalla
        enemy_group.draw(screen) #muestra los objetos del grupo en pantalla
        words_group.draw(screen) #muestra los objetos del grupo en pantalla

        #----------------detecting keyboards inputs---------------
        for event in pygame.event.get(): #hace que cuando se presione la tecla scape se salga del programa
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        #----------------updating sprites on screen-----------------
        all_sprites_group.update() #actualiza los sprites
        points_group.update()#actualiza los sprites
        enemy_group.update()#actualiza los sprites
        words_group.update()#actualiza los sprites
        stars_group.update()#actualiza los sprites
        hp.text = f'HP {player1.hp}' #actualiza el texto

        #--------------------Examinando coliciones------------------
        collides = pygame.sprite.spritecollide(player1, enemy_group, False,) #Variable para saber las coliciones entre player1 y el grupo de enemigos

        if collides: #Comprueba si han existido coliciones
            player1.collide()
            player1.update()
            pygame.display.flip()
            time.sleep(1) #Detiene la ejecución del programa durante un segundo
            screen.blit(fight_background, (0, 0)) #Coloca el fondo de batalla
            pygame.display.flip()

            #Prueba colición por colición para saber cual enemigo ha sido el que ha colicionado con el personaje
            for collide in collides: 
                result = Final_battle(player1, collide, screen, clock) #Activa la batalla final
                if result == 'win!': #Si el resultado de la batalla final es una victoria se activan los creditos del juego
                    credits(FPS, clock)
            collides.clear() #Limpia las coliciones
                
        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

def Final_battle(player, enemy, screen, clock):     #Función de la batalla contra el enemigo final
    FPS = 60
    turn_attack = 'player'  #Esta variable define el turno de ataque. Si es igual a "player", le toca atacar al jugador. Si es igual a "enemy", ataca el enemigo.
    function.music('Music/battle.mp3') #llama a la función que activa la musica
    
    #----------groups--------------
    all_sprites_group = pygame.sprite.Group()
    words_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    stars_group = pygame.sprite.Group()
    
    #---------------------sprites-----------------------                                                                #####
    player_example = sprites.Player((WIDTH/6, HEIGHT/3), (900, 900), 3, 100)                                                #
    for n in range(100):                                                                                                    #
        star = sprites.Stars()                                                                                              #
        stars_group.add(star)                                                                                               #
                                                                                                                            #
    #images                                                                                                                 #
    background_image = function.load_image('Images/battle_stage.png', WIDTH, HEIGHT,True)                                   #
    hit = function.load_image('Images/golpe.png', 200, 80, True)                                                            #
    enemy.rect.centerx = WIDTH-(WIDTH/5)                                                                                    #
    enemy.rect.centery = HEIGHT/3.5                                                                                         #
    enemy._area = (2000, 2000)                                                                                              #-------Creación de Sprites
                                                                                                                            #
    # Buttons                                                                                                               #
    button_attack = sprites.Buttons('attack', (WIDTH/4, HEIGHT-HEIGHT/6))                                                   #
    button_spell = sprites.Buttons('spell', (WIDTH/2, HEIGHT-HEIGHT/6))                                                     #
    button_luck = sprites.Buttons('luck', (WIDTH-WIDTH/4, HEIGHT-HEIGHT/6))                                                 #
                                                                                                                            #
    # Text                                                                                                                  #
    hp_player = sprites.Words(f'Tu vida {player.hp}', 40, function.RED, (WIDTH/6, HEIGHT/20))                               #
    hp_enemy = sprites.Words(f'Vida del rival {enemy.hp}', 40, function.RED, (WIDTH/1.3, HEIGHT/20))                        #
    potions = sprites.Words(f'Pociones disponibles: {player._potions}', 20, function.RED, (WIDTH/2, HEIGHT-HEIGHT/9))       #
    mana = sprites.Words(f'Mana: {player._mana}', 20, function.BLUE, (WIDTH-WIDTH/4, HEIGHT-HEIGHT/9))                      #
                                                                                                                        #####
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
        #Esto sirve para dibujar todos los sprites en la pantalla
        screen.fill(function.DARK_BLUE)
        stars_group.draw(screen)
        screen.blit(background_image, (0, 0))

        buttons_group.draw(screen)
        words_group.draw(screen)
        all_sprites_group.draw(screen)

        #------------------------input events-------------------------
        for event in pygame.event.get(): #Analiza cada evento durante el juego 
            if event.type == QUIT: #Si un evento es de tipo "QUIT", cierra el programa
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN: #Si el evento es igual a presionar una tecla de teclado
                if event.key == K_ESCAPE: #Si la tecla presionada es la tecla de escape, entonces se cierra el programa
                    sys.exit(0)

            #-----battle-----
            if button_attack.rect.collidepoint(pygame.mouse.get_pos()): #Ayuda a detectar si el mouse está encima del botón de ataque
                if event.type == MOUSEBUTTONDOWN and event.button == 1: #Detecta si el tipo de evento es un click del mouse y si es especificamente el click izquierdo
                   if player.luck>=5:
                       enemy.hp-=30
                   elif player.luck<=0:
                       player.hp-=20
                   else:
                        function.damage(player, enemy)
                        turn_attack = 'enemy'
                        pygame.mouse.set_visible(False)
                        player._mana+=5
                       

            elif button_spell.rect.collidepoint(pygame.mouse.get_pos()): #Ayuda a detectar si el mouse está encima del botón de ataque
                if event.type == MOUSEBUTTONDOWN and event.button == 1: #Detecta si el tipo de evento es un click del mouse y si es especificamente el click izquierdo
                    
                    #Si el jugador tiene pociones y su vida está por debajo de 100, entonces el jugador puede usar pociones y aumenta el mana del personaje
                    if player._potions > 0 and player._hp < 100: 
                        function.use_potion(player)
                        turn_attack = 'enemy'
                        pygame.mouse.set_visible(False)
                        player._mana+=5

            elif button_luck.rect.collidepoint(pygame.mouse.get_pos()): #Ayuda a detectar si el mouse está encima del botón de ataque
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and player._mana>=30: #Detecta si el tipo de evento es un click del mouse y si es especificamente el click izquierdo, y también si el mana del personaje es mayor o igual a 30
                    function.SpecialDamage(player,enemy)
                    turn_attack = 'enemy'
                    pygame.mouse.set_visible(False)


        #-------------update sprites on screen--------------
        hp_player.text = f'Tu vida: {player.hp}' #Actualiza en la pantalla la vida del personaje
        hp_enemy.text = f'Vida del rival: {enemy.hp}' #Actualiza en la pantalla la vida del enemigo
        
        #Muesta en pantalla la cantidad de pociones que tiene el personaje, o de lo contrario muestra un letrero diciendo que no se puede curar
        if player._potions > 0: 
            potions.text = f"Pociones disponibles: {player._potions}"
        else:
            potions.text=f'No se puede curar'
        
        #Muesta en pantalla el mana que tiene el personaje, y si no tiene muestra un mensaje diciendo que no tiene mana suficiente
        if (player._mana-30) >= 0: 
            mana.text = f'Mana: {player._mana}'
        else:
            mana.text = f'Sin mana suficiente'
        
        player_example.animation('right') #Activa la animación del personaje principal mirando hacia la derecha
        enemy.animation() #Activa la animación del enemigo

                                #####
        buttons_group.update()      #
        words_group.update()        #-----Actualización de los sprites en cada uno de los grupos
        stars_group.update()        #
                                #####

        if enemy.hp <= 0: #Si la vida del enemigo es cero o menor, entonces se termina el ciclo para dar paso a las ecuaciones
            break

        #Define el ataque del enemigo si la funcion "turn_attack" asi lo define
        if turn_attack == 'enemy': 
            enemy.damage = random.randint(100, 600)*(1/100)
            player.hp -= enemy.damage
            turn_attack = 'player'
            pygame.mouse.set_visible(True)
            
        if player.hp <= 0: #Si la vida del personje principal es cero o menor entonces se llama la función dead para definir el fin de la partida
            dead(FPS, clock)
        
        pygame.display.flip() #Actualizar contenido en pantalla
        
    function.music('Music/backGround.mp3')
    function.enemys_deleted += 1 #suma uno cada vez que se mata un enemigo, esto para llavar la cuenta de los enemigos eliminados
    return 'win!' #Retorna la palabra "win!"

def transicion(FPS, player1, clock):    #Es el escenario donde se entra despues de haber derrotado todos los enemigos, donde está el portal que te lleva a el enemigo final
    function.music('Music/intro.mp3') #Activa la música de escenario
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creación de la pantalla

    #-----------------groups-------------------
    #Los grupos sirven para poder agrupar esprites en una especie de lista, y que de esta forma sea más fácil manejarlos
    all_sprites_group = pygame.sprite.Group() #Grupo para almacenar todos los sprites
    words_group = pygame.sprite.Group()     #Grupo para almacenar todos los sprites de tipo "Word"
    enemy_group = pygame.sprite.Group()     #Grupo para almacenar todos los sprites de tipo "Bicho", que sería igual a los enemigos del juego
    stars_group = pygame.sprite.Group()     #Grupo para almacenar todos los sprites de tipo "Star"
    points_group = pygame.sprite.Group()    #Grupo para almacenar todos los sprites de tipo "Points"

    #-----------------sprites------------------
    background_image = function.load_image('Images/BackgroundEnd.png', WIDTH, HEIGHT+(HEIGHT*(1/5)), True)
    
    #stars
    #Creación de estrallas (sprites), que simulan una lluvia de estrellas, y su único objetivo es la decoración del escenario
    for n in range(100):
        star = sprites.Stars()
        stars_group.add(star)

    #points
    #Creación de puntos (sprites), que simulan una cascada de puntos, y su único objetivo es la decoración del escenario
    for n in range(100):
        points = sprites.Points()
        points_group.add(points)

    #enemy
    colision = sprites.Bicho('Images/Colission.png',(WIDTH-(WIDTH/2), HEIGHT/2), (400, 400), 0, 0, 'x')     #Sprite que funciona para detectar cuando el personaje principal está
    colision.image = function.load_image('Images/Colission.png', WIDTH/1, HEIGHT/5, True)                   #parado en una zona especifica del escenario
    colision.location=(WIDTH/6,HEIGHT/2)
    
    # Text
    hp = sprites.Words(f'HP {player1.hp}', 30, function.RED, (WIDTH/6, HEIGHT/20), True)
    words_group.add(hp)
    
    enemy_group.add(colision)   #agregar enemigos al grupo "enemy_groups"

    all_sprites_group.add(player1) #Agrega el sprite "player1" al grupo de sprites "all_sprites_groups"

    pygame.mouse.set_visible(False)

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while True:
        collides = None     #Esta variable sirve para que las coliciones se reinicien a cada inicio del ciclo
        clock.tick(FPS)     #Indica las veces que se va a actualizar la pantalla

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
        collides = pygame.sprite.spritecollide(player1, enemy_group, False)


        if collides:
            end_scenario(FPS, player1, clock)
        
        pygame.display.flip() #Actualizar contenido en pantalla
    return 'game over'

def dead(FPS, clock):   #Pantalla de muerte, la cual aparece cuando el personaje principal muere, o lo que es lo mismo, su vida es menor o igual a 0
    function.music('Music/game_over_song.mp3')  #Activa la música de escenario
    bucle = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))   #Creación de la pantalla

    #-----------------groups-------------------
    words_group = pygame.sprite.Group()

    #-----------------sprites------------------
    game_over_img = function.load_image('Images/Game over.png', WIDTH, HEIGHT, True)    #Carga la imagen de game over
    
    pygame.mouse.set_visible(False)     #Hace que el mouse sea visible en esta pantalla

    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------
    while bucle:
        clock.tick(FPS)

        #----------------drawing sprites on screen----------------
        screen.fill(function.BLACK)
        words_group.draw(screen)
        screen.blit(game_over_img, (0, 0))

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

def credits(FPS,clock): #Pantalla donde se muestran los creditos del juego
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creación de la pantalla
    bucle = True
    
    words_group=pygame.sprite.Group() #grupo para almacenar los sprites de tipo "Word"

    #----------------------------sprites de tipo word-------------------------------
    creditos = sprites.Words('CREDITOS', 40, function.RED, (WIDTH/2, HEIGHT/20))
    elprogramador = sprites.Words('Santiago Melo', 40, function.RED, (WIDTH/2, HEIGHT/4.5))
    elasistentedeprogramador = sprites.Words('Jose Rios', 40, function.RED, (WIDTH/2, HEIGHT/3))
    elpesomuerto = sprites.Words('Sara Salazar', 40, function.RED, (WIDTH/2, HEIGHT/2))
    palosprofes = sprites.Words('Gracias por jugar!', 40, function.RED, (WIDTH/2, (HEIGHT-(HEIGHT/4))))
    salgasedeaca = sprites.Words('Presiona [scape] para salir', 40, function.RED, (WIDTH/2, (HEIGHT-(HEIGHT/6))))
    
    words_group.add(creditos, elprogramador, elasistentedeprogramador,elpesomuerto,palosprofes,salgasedeaca)
    
    while bucle:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)

        words_group.draw(screen)
        pygame.display.flip()