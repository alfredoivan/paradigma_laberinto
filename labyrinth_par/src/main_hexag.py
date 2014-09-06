# -*- coding: utf-8 -*-

import pygame
from pygame.locals import * # @UnusedWildImport
import vectorSimple
import vars_tmaze
import math
import worldManager
import time
import signal
import sys
import os

gvars = vars_tmaze.vars_tmaze() #variables del juego a ser accedidas "globalmente"

HEXAG_VERSION = "1.3.1"
CYCLE_LOOP_NUMBER = 2 #cantidad de ciclos que deben pasar para que se ejecuten los movimientos en el mapa 3D
IMG_WIN_MONEY = pygame.image.load('pics/items/money.png')
IMG_LOSE_SADFACE = pygame.image.load('pics/items/sadface.gif')
FPS = 8
WHITE_SQUARE = Rect(0, 0, 100, 100)

vectorInstantaneo = vectorSimple.vectorSimple() #vector con el instantáneo de movimiento, x e y dependen del estado de joystick.




def mainFunction():
    pygame.mixer.init()
    pygame.init()
    pygame.display.set_caption("Laberinto Virtual - Hexágono v"+ (HEXAG_VERSION) )
    
    #size = w, h = 1600,900
    size = width_screen, height_screen = 1366,768
    
    #window = pygame.display.set_mode(size)
    pygame.display.set_mode(size, pygame.FULLSCREEN)
    
    
    screen = pygame.display.get_surface()
    #pixScreen = pygame.surfarray.pixels2d(screen)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    
    # Initialize the joysticks
    joystick_working = False
    try:
        pygame.joystick.init()
        my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()
        joystick_working = True
    except:
        #log_to_file("Joystick incompatible o no encontrado.")
        joystick_working = False
    
    
    
    #################################################################
    #declaro unas variables útiles para calcular deltas de movimiento
    #################################################################
    #t = threading.Timer(4.0, socketTimer)
    #t.start() # luego de 4 segundos arranca.
    time.sleep(1.5)
    
    #################################################################
    ### Elección de puerta que tiene recompensa.
    #################################################################
    from random import randint
    rndnum = randint(0,5)
                
    gvars.set_num_puerta(rndnum)
                
    if (rndnum == 0):
                    gvars.set_posx_to_set(10.518899) 
                    gvars.set_posy_to_set(48.553612)
    elif rndnum == 1:
                    gvars.set_posx_to_set(1.831244 )
                    gvars.set_posy_to_set(26.49384 )
    elif rndnum == 2:
                    gvars.set_posx_to_set(10.08041 )
                    gvars.set_posy_to_set(4.028711 )
    elif rndnum == 3:
                    gvars.set_posx_to_set(40.0201579 )
                    gvars.set_posy_to_set(4.1025887 )
    elif rndnum == 4:
                    gvars.set_posx_to_set(48.131992 )
                    gvars.set_posy_to_set(26.51180 )
    elif rndnum == 5:
                    gvars.set_posx_to_set(39.487556 )
                    gvars.set_posy_to_set(48.143990 )
                
    for i in range(0, len(gvars.sprite_positions)):
                    _texnum_=gvars.sprite_positions[i].__getitem__(2)
                    if (_texnum_ == 14):
                        gvars.sprite_positions[i] = (gvars.get_posx_to_set(), gvars.get_posy_to_set(), 14)
    
    ########################
    wm = worldManager.WorldManager(gvars.worldMap,gvars.sprite_positions, 25, 25.5, -1, 0, 0, 1)
    ###
    time.sleep(0.2) #added t.sleep just in case.
    initial_latency = 7 #7 latency frames to smooth the initialization.
    
    #===========================================================================
    # #variables de logeo: strobe_value, win_value. Se graban en archivo de log al final del bucle
    #===========================================================================
    strobe_value = 0 # 0=Negro 1=Blanco
    win_value = 0 #0=en juego , 1=perdió , 2=ganó
    win_value_f = 0 #se guarda en memoria si se gana o pierde, y se pone en log sólo cuando hay un strobe
    keep_log = False #true=logear este ciclo. Permite no logear los intersticios de 
    #tiempo en donde ya se sabe que ganó y hasta el siguiente strobe de reinicio..
    gvars.set_anim_count( 61)
    pygame.time.delay(500)
    wm.draw(screen)
    while(True):
        if (initial_latency > 0):
            initial_latency -= 1
        wm.draw(screen)
        clock.tick(60)
        
        strobe_value = 0 
        # timing for input and FPS counter
        
        frameTime = float(clock.get_time()) / 1000.0 # frameTime is the time this frame has taken, in seconds
        #text = f.render(str(clock.get_fps()), False, (255, 255, 0))
        #screen.blit(text, text.get_rect(), text.get_rect())
        pass
        #=======================================================================
        # ##dibujo barra de puntaje
        #=======================================================================
        pygame.draw.rect(screen, (0,0,235), (50-5,height_screen/2-5-gvars.get_player_score(),15+10,gvars.get_player_score()+1+8), 0)
        pygame.draw.rect(screen, (0,0,255), (50,height_screen/2-gvars.get_player_score(),15,gvars.get_player_score()+1), 0)
        #=======================================================================
        # # Animación de ganaste / perdiste:
        #=======================================================================
        #retardo hasta mostrar animación de ganaste o perdiste
        
        if (gvars.get_anim_count() > 200 and gvars.get_anim_count() < 210):
            gvars.set_anim_count(gvars.get_anim_count()+1)
        if (gvars.get_anim_count() == 210):
            gvars.set_anim_count (1)
        if (gvars.get_anim_count() > 270 and gvars.get_anim_count() < 280):
            gvars.set_anim_count(gvars.get_anim_count()+1)
        if (gvars.get_anim_count() == 280):
            gvars.set_anim_count (71)
            
        #animación durante 60 ciclos, de ganaste o perdiste
        if (gvars.get_anim_count() >0 and gvars.get_anim_count() < 60):
                vars_tmaze.blit_alpha(screen, IMG_WIN_MONEY, (width_screen/2 -250,0), 255-gvars.get_anim_count()*4)
                gvars.set_anim_count(gvars.get_anim_count()+4)
        if (gvars.get_anim_count() >70 and gvars.get_anim_count() < 130):
                vars_tmaze.blit_alpha(screen, IMG_LOSE_SADFACE, (width_screen/2 -250,0), 255-(gvars.get_anim_count()-70)*4)
                gvars.set_anim_count(gvars.get_anim_count()+4)
        if (gvars.get_anim_count() == 61 or gvars.get_anim_count() == 131):
            gvars.set_anim_count (0) #fin animación, reiniciamos experimento.
            #############################################
            #reincio de experimento
            #############################################
            #log_to_file("Reinicio de experimento.")
            gvars.set_door_anim (0)
            # Restablecer valores de puerta cerrada, no haría falta en sprite_positions
            for i in range(0, len(gvars.sprite_positions)):
                _texnum_=gvars.sprite_positions[i].__getitem__(2)
                if ( _texnum_ > 7 and  _texnum_ < 14):
                    gvars.sprite_positions[i] = ( gvars.sprite_positions[i].__getitem__(0), gvars.sprite_positions[i].__getitem__(1), 7 )
            #time.sleep(0.05)
            wm = worldManager.WorldManager(gvars.worldMap,gvars.sprite_positions, 25, 25.5, -1, 0, 0, 1)
            ########################
            #randomizar la cámara:
            ########################
            temp_rand_num = randint(0,30)
            flt_num = (temp_rand_num *2*3.1415)/ 30
            #en flt_num tengo un ángulo aleatorio entre 0 y 2pi
            oldDirX = wm.camera.dirx
            wm.camera.dirx = wm.camera.dirx * math.cos(flt_num) - wm.camera.diry * math.sin(flt_num)
            wm.camera.diry = oldDirX * math.sin(flt_num) + wm.camera.diry * math.cos(flt_num)
            oldPlaneX = wm.camera.planex
            wm.camera.planex = wm.camera.planex * math.cos(flt_num) - wm.camera.planey * math.sin(flt_num)
            wm.camera.planey = oldPlaneX * math.sin(flt_num) + wm.camera.planey * math.cos(flt_num)
            ###
            #remuevo el ítem de ganado, para que no se vea entre las texturas de puerta:
            for i in range(0, len(gvars.sprite_positions)):
                    _texnum_=gvars.sprite_positions[i].__getitem__(2)
                    if (_texnum_ == 14):
                        gvars.sprite_positions[i] = (0.5, 0.5, 14)
            #en cada reinicio: se pone cuadrado blanco
            gvars.set_init_whitebox(0) #en 2 ciclos se pondrá efectivamente el cuadrado blanco.
            win_value = 0
            win_value_f = 0

        ###############################################
        # speed modifiers (desplazamiento, rotación)
        ###############################################
        moveSpeed = frameTime * 10.2 # the constant value is in squares / second
        rotSpeed = frameTime * 1.5 # the constant value is in radians / second
        
        if (gvars.get_door_anim() > 0):
            if (gvars.get_door_anim() < 10):
                for i in range(0, len(wm.sprite_positions)):
                    if (wm.sprite_positions[i].__getitem__(2) == gvars.get_door_anim()+6):
                        wm.sprite_positions[i] = ( wm.sprite_positions[i].__getitem__(0), wm.sprite_positions[i].__getitem__(1), gvars.get_door_anim()+7 )
            if (gvars.get_door_anim() == 60):
                gvars.set_door_anim(6)
                #para ver el cuadrado blanco ya:
                gvars.set_init_whitebox(0)
            if (gvars.get_door_anim() == 5):
                gvars.set_door_anim(60)
            if (gvars.get_door_anim() == 50):
                gvars.set_door_anim(5)
            if (gvars.get_door_anim() == 4):
                gvars.set_door_anim(50)
            if (gvars.get_door_anim() == 40):
                gvars.set_door_anim(4)
            if (gvars.get_door_anim() == 3):
                gvars.set_door_anim(40)
            if (gvars.get_door_anim() == 30):
                gvars.set_door_anim(3)
            if (gvars.get_door_anim() == 2):
                gvars.set_door_anim(30)
            if (gvars.get_door_anim() == 20):
                gvars.set_door_anim(2)
            if (gvars.get_door_anim() == 1):
                gvars.set_door_anim(20) #para enlentecer un poco la animación
                #acá pongo el gráfico de ítem ganado, no se pone antes para que no se vea entre intersticios de puerta
                for i in range(0, len(gvars.sprite_positions)):
                    _texnum_=gvars.sprite_positions[i].__getitem__(2)
                    if (_texnum_ == 14):
                        gvars.sprite_positions[i] = (gvars.get_posx_to_set(), gvars.get_posy_to_set(), 14)
                
            
        
        ############################################
        # Toma de datos de Joystick
        ############################################
        #x e y
        x=0
        y=0
        if (joystick_working==True and gvars.get_door_anim() == 0 and keep_log == True):
            x = my_joystick.get_axis(0)
            y = my_joystick.get_axis(1)
        x_ax1= int(x )
        x_ax2 = int(x +0.1)
        x_ax = 0
        if x_ax1 == -1:
            x_ax = -1
        if x_ax2 == 1:
            x_ax = 1
        y_ax1= int(y )
        y_ax2 = int(y +0.1)
        y_ax = 0
        if y_ax1 == -1:
            y_ax = -1
        if y_ax2 == 1:
            y_ax = 1
        global vectorInstantaneo
        vectorInstantaneo.x = int(2.2*x_ax)
        vectorInstantaneo.y = int(2.2*y_ax)
        #=======================================================================
        # #Analizo vector Instantáneo (datos tomados de joystick)
        #=======================================================================
        if vectorInstantaneo.x < 0:
            #for each rotation unit divided by 30 (maximum vector module allowed)
            # rotate to the left
            # both camera direction and camera plane must be rotated
            oldDirX = wm.camera.dirx
            wm.camera.dirx = wm.camera.dirx * math.cos(rotSpeed) - wm.camera.diry * math.sin(rotSpeed)
            wm.camera.diry = oldDirX * math.sin(rotSpeed) + wm.camera.diry * math.cos(rotSpeed)
            oldPlaneX = wm.camera.planex
            wm.camera.planex = wm.camera.planex * math.cos(rotSpeed) - wm.camera.planey * math.sin(rotSpeed)
            wm.camera.planey = oldPlaneX * math.sin(rotSpeed) + wm.camera.planey * math.cos(rotSpeed)
        if vectorInstantaneo.y < 0:
            #print "movió arriba"
            moveX = wm.camera.x + wm.camera.dirx * moveSpeed
            if(gvars.worldMap[int(moveX)][int(wm.camera.y)]==0 and gvars.worldMap[int(moveX + 0.1)][int(wm.camera.y)]==0):wm.camera.x += wm.camera.dirx * moveSpeed
            moveY = wm.camera.y + wm.camera.diry * moveSpeed
            if(gvars.worldMap[int(wm.camera.x)][int(moveY)]==0 and gvars.worldMap[int(wm.camera.x)][int(moveY + 0.1)]==0):wm.camera.y += wm.camera.diry * moveSpeed
        if vectorInstantaneo.x > 0:
            #print "movió derecha"
            # rotate to the right
            # both camera direction and camera plane must be rotated
            oldDirX = wm.camera.dirx
            wm.camera.dirx = wm.camera.dirx * math.cos(- rotSpeed) - wm.camera.diry * math.sin(- rotSpeed)
            wm.camera.diry = oldDirX * math.sin(- rotSpeed) + wm.camera.diry * math.cos(- rotSpeed)
            oldPlaneX = wm.camera.planex
            wm.camera.planex = wm.camera.planex * math.cos(- rotSpeed) - wm.camera.planey * math.sin(- rotSpeed)
            wm.camera.planey = oldPlaneX * math.sin(- rotSpeed) + wm.camera.planey * math.cos(- rotSpeed)
        if vectorInstantaneo.y > 0:
            #print "movió abajo"
            # move backwards if no wall behind you
            if(gvars.worldMap[int(wm.camera.x - wm.camera.dirx * moveSpeed)][int(wm.camera.y)] == 0):wm.camera.x -= wm.camera.dirx * moveSpeed
            if(gvars.worldMap[int(wm.camera.x)][int(wm.camera.y - wm.camera.diry * moveSpeed)] == 0):wm.camera.y -= wm.camera.diry * moveSpeed
        
        ####################################################################   
        ##################################################################
        # Análisis áreas. Colisiones:
        ##################################################################
        
        colision_puerta = False
        DOOR_RADIUS_POW2 = 9.9225 #radio 3.15
        
        #Puerta que está en: (12.1535  , 47.025, 7),
        if ( pow(abs(wm.camera.x  - 12.1535), 2) < DOOR_RADIUS_POW2 and  pow(abs(wm.camera.y  - 47.025), 2 ) < DOOR_RADIUS_POW2   ):
            colision_puerta = True
            if (gvars.get_num_puerta() == 0):
                #print "ganaste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (201)
                    win_value_f = 2
                    add_score()
            else:
                #print "perdiste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (271)
                    win_value_f = 1
        
        
        #Puerta que está en: (3.2796 , 26.6061, 7),
        if (pow(abs(wm.camera.x  - 3.2796),2) < DOOR_RADIUS_POW2 and  pow(abs(wm.camera.y  - 26.6061),2 ) < DOOR_RADIUS_POW2 ):
            colision_puerta = True
            if (gvars.get_num_puerta() == 1):
                #print "ganaste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (201)
                    win_value_f = 2
                    add_score()
            else:
                #print "perdiste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (271)
                    win_value_f = 1
            
        #Puerta que está en: (11.0158 , 5.1344, 7),
        if (  pow(abs(wm.camera.x  - 11.0158), 2) < DOOR_RADIUS_POW2 and  pow(abs(wm.camera.y  - 5.1344),2) < DOOR_RADIUS_POW2 ):
            colision_puerta = True
            if (gvars.get_num_puerta() == 2):
                #print "ganaste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (201)
                    win_value_f = 2
                    add_score()
            else:
                #print "perdiste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (271)
                    win_value_f = 1
        
        #Puerta que está en: (38.9078 , 4.8715, 7),
        if ( pow(abs(wm.camera.x  - 38.9078), 2) < DOOR_RADIUS_POW2 and  pow(abs(wm.camera.y  - 4.8715), 2) < DOOR_RADIUS_POW2 ):
            colision_puerta = True
            if (gvars.get_num_puerta() == 3):
                #print "ganaste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (201)
                    win_value_f = 2
                    add_score()
            else:
                #print "perdiste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (271)
                    win_value_f = 1
            
        #Puerta que está en: (47.41795 , 26.33015, 7),
        if ( pow(abs(wm.camera.x  - 47.41795) ,2 ) < DOOR_RADIUS_POW2 and  pow(abs(wm.camera.y  - 26.33015) ,2 ) < DOOR_RADIUS_POW2 ):
            colision_puerta = True
            if (gvars.get_num_puerta() == 4):
                #print "ganaste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (201)
                    win_value_f = 2
                    add_score()
            else:
                #print "perdiste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (271)
                    win_value_f = 1
        
        #Puerta que está en: (37.95235 , 46.89345, 7)
        if ( pow(abs(wm.camera.x  - 37.95235) , 2) < DOOR_RADIUS_POW2 and  pow(abs(wm.camera.y  - 46.89345), 2) < DOOR_RADIUS_POW2 ):
            colision_puerta = True
            if (gvars.get_num_puerta() == 5):
                #print "ganaste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (201)
                    win_value_f = 2
                    add_score()
            else:
                #print "perdiste"
                if (gvars.get_anim_count () == 0):
                    gvars.set_anim_count (271)
                    win_value_f = 1
                
            
        
        if (colision_puerta):
            #print "colsión"
            if (gvars.get_door_anim () == 0):
                    gvars.set_door_anim (1)
        
        #############################
        ## Eventos de Pygame (handle del quit)
        #############################
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                finalize_log()
                os.kill(os.getpid(), signal.SIGINT)
                sys.exit()
                return 
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    finalize_log()
                    os.kill(os.getpid(), signal.SIGINT)
                    sys.exit()
                    return
                #elif event.key == K_SPACE:
                #    #resetAll()
                #    print """"""      
            else:
                pass 
        
        #=======================================================================
        # # Entradas de Teclado.
        #=======================================================================
        if (gvars.get_delay_reboot_button() > 0):
            gvars.set_delay_reboot_button(gvars.get_delay_reboot_button()+1)
            
        if (gvars.get_delay_reboot_button() == 12):
            gvars.set_delay_reboot_button(0)
        if (gvars.get_door_anim() == 0 and keep_log == True):
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                #Forzar Reinicio: como si hubiera ganado o perdido.
                if (gvars.get_delay_reboot_button() ==0):
                    gvars.set_delay_reboot_button(1)
                    gvars.set_anim_count (61)
            ###############
            # Desplazarse con UP DOWN LEFT RIGHT
            if keys[K_UP]:
                # move forward if no wall in front of you
                moveX = wm.camera.x + wm.camera.dirx * moveSpeed
                if(gvars.worldMap[int(moveX)][int(wm.camera.y)]==0 and gvars.worldMap[int(moveX + 0.1)][int(wm.camera.y)]==0):wm.camera.x += wm.camera.dirx * moveSpeed
                moveY = wm.camera.y + wm.camera.diry * moveSpeed
                if(gvars.worldMap[int(wm.camera.x)][int(moveY)]==0 and gvars.worldMap[int(wm.camera.x)][int(moveY + 0.1)]==0):wm.camera.y += wm.camera.diry * moveSpeed
            if keys[K_DOWN]:
                # move backwards if no wall behind you
                if(gvars.worldMap[int(wm.camera.x - wm.camera.dirx * moveSpeed)][int(wm.camera.y)] == 0):wm.camera.x -= wm.camera.dirx * moveSpeed
                if(gvars.worldMap[int(wm.camera.x)][int(wm.camera.y - wm.camera.diry * moveSpeed)] == 0):wm.camera.y -= wm.camera.diry * moveSpeed
            if (keys[K_RIGHT] and not keys[K_DOWN]) or (keys[K_LEFT] and keys[K_DOWN]):
                # rotate to the right
                # both camera direction and camera plane must be rotated
                oldDirX = wm.camera.dirx
                wm.camera.dirx = wm.camera.dirx * math.cos(- rotSpeed) - wm.camera.diry * math.sin(- rotSpeed)
                wm.camera.diry = oldDirX * math.sin(- rotSpeed) + wm.camera.diry * math.cos(- rotSpeed)
                oldPlaneX = wm.camera.planex
                wm.camera.planex = wm.camera.planex * math.cos(- rotSpeed) - wm.camera.planey * math.sin(- rotSpeed)
                wm.camera.planey = oldPlaneX * math.sin(- rotSpeed) + wm.camera.planey * math.cos(- rotSpeed)
            if (keys[K_LEFT] and not keys[K_DOWN]) or (keys[K_RIGHT] and keys[K_DOWN]): 
                # rotate to the left
                # both camera direction and camera plane must be rotated
                oldDirX = wm.camera.dirx
                wm.camera.dirx = wm.camera.dirx * math.cos(rotSpeed) - wm.camera.diry * math.sin(rotSpeed)
                wm.camera.diry = oldDirX * math.sin(rotSpeed) + wm.camera.diry * math.cos(rotSpeed)
                oldPlaneX = wm.camera.planex
                wm.camera.planex = wm.camera.planex * math.cos(rotSpeed) - wm.camera.planey * math.sin(rotSpeed)
                wm.camera.planey = oldPlaneX * math.sin(rotSpeed) + wm.camera.planey * math.cos(rotSpeed)
            
        ##########################
        # Cuadrado blanco:
        ##########################
        pygame.draw.rect(screen, Color('black'), WHITE_SQUARE)
        if (gvars.get_init_whitebox()< 8):
            pygame.draw.rect(screen, Color('black'), WHITE_SQUARE)
            if (gvars.get_init_whitebox() == 2):
                pygame.draw.rect(screen, Color('white'), WHITE_SQUARE)
                pygame.display.flip()   #Update screen
                pygame.time.delay(100)
                strobe_value = 1
                win_value = win_value_f
            gvars.set_init_whitebox( gvars.get_init_whitebox()+1 )
        
        
        ##########################
        #pygame.display.update()
        ##########################
        if (initial_latency == 0):
            pygame.display.flip()
        #=======================================================================
        # ## Log to file:
        #=======================================================================
        
        milis = (pygame.time.get_ticks())
        
        if (keep_log or strobe_value >0):
            log_to_file("%d,%f,%f,%f,%f,%d,%d" % (milis, wm.camera.x, wm.camera.y, wm.camera.dirx, wm.camera.diry, strobe_value, win_value) )
        #print (wm.camera.x), wm.camera.y
        if (strobe_value == 1 and win_value == 0):
            #empezar a logear
            keep_log = True
        elif (strobe_value ==1 and win_value >0):
            keep_log = False

def add_score():
    #log_to_file("Sujeto GANA.")
    gvars.set_player_score(gvars.get_player_score() +10)

def log_to_file(string_to_log=""):
    #if (gvars.get_log_to_file_counter() < 30):
        gvars.log_to_file_matrix.append(string_to_log+'\n')
        gvars.set_log_to_file_counter(gvars.get_log_to_file_counter()+1)
#     else:
#         gvars.log_to_file_matrix.append(string_to_log+'\n')
#         gvars.set_log_to_file_counter(gvars.get_log_to_file_counter()+1)
#         for i in range(0,gvars.get_log_to_file_counter()):
#             gvars.get_log_file().write(gvars.log_to_file_matrix[i]) # python will convert \n to os.linesep
#         gvars.set_log_to_file_counter(0)
#         gvars.log_to_file_matrix=[]
        pass

def finalize_log():
    for i in range(0,gvars.get_log_to_file_counter()):
        gvars.get_log_file().write(gvars.log_to_file_matrix[i]) # python will convert \n to os.linesep
    gvars.get_log_file().close()
    print "Archivo de log cerrado."

def load_image(image, darken, colorKey = None):
    ret = []
    if colorKey is not None:
        image.set_colorkey(colorKey)
    if darken:
        image.set_alpha(127)
    for i in range(image.get_width()):
        s = pygame.Surface((1, image.get_height())).convert()
        #s.fill((0,0,0))
        s.blit(image, (- i, 0))
        if colorKey is not None:
            s.set_colorkey(colorKey)
        ret.append(s)
    return ret
 
def init_hexag_training():
    def init_worldmap():
        gvars.worldMap=[
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,2,0,0,0,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,0,0,4,0,4,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,4,4,4,0,0,4],
          [4,0,4,0,0,0,4,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,4,4,0,0,4,0,4],
          [4,4,0,0,0,0,0,4,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,4,4,0,0,0,0,4,4],
          [4,0,4,0,0,0,0,0,4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,4,4,0,0,0,0,0,4,4],
          [4,0,0,4,0,0,0,0,0,4,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4,4,0,0,0,0,0,4,4,4],
          [4,0,0,0,4,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,4,4,0,4],
          [4,0,0,4,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,4,4,0,0,4],
          [4,0,0,0,4,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,4],
          [4,0,0,0,0,4,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,4],
          [4,0,0,0,0,0,4,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,4,0,0,0,0,4],
          [4,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,4],
          [4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,4],
          [4,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,4],
          [4,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4],
          [4,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4],
          [4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
          [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
          [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
          [4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
          [4,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4],
          [4,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4],
          [4,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4,4],
          [4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,4,4],
          [4,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,4],
          [4,0,0,0,0,0,4,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,0,0,0,0,0,4],
          [4,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,4],
          [4,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,4],
          [4,0,0,4,4,4,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,4,4,0,0,4],
          [4,0,4,4,4,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,4,4,0,4],
          [4,4,0,4,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4,4,0,0,0,0,0,4,4,4],
          [4,0,4,0,0,0,0,0,4,4,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,4,4,0,0,0,0,0,4,4],
          [4,4,0,0,0,0,0,4,4,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,4,4,0,0,0,0,4,4],
          [4,0,4,0,0,0,4,4,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,4,4,0,0,4,0,4],
          [4,0,0,4,0,4,4,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,4,4,4,0,0,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,2,0,0,0,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
          [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
        ];
        
        gvars.sprite_positions=[
                    (25.07466, 50.187876, 4), #círculo
                    (42.308263, 20.924262, 5),  #cuadrado
                    (7.947716, 20.924262, 6), #triángulo
                    (12.787, 47.724, 7), (12.1535  , 47.01, 7), (11.520  , 46.326, 7), (12.1535  , 47.025, 7), #puerta 1, circ.izq.
                    (3.275 , 25.2751, 7),( 3.277 , 25.8751, 7),  (3.2796 , 26.6061, 7), (3.2896 , 27.2061, 7),  (3.3097, 27.937, 7),#triang.der.
                    (11.8644, 4.1717, 7), (11.4644, 4.7717, 7), (11.0158  , 5.1, 7), (11.0158 , 5.1344, 7), (10.6158 , 5.8344, 7), (10.1672 , 6.097, 7),#triang.izq.
                    (39.7025, 5.7654, 7),  (39.3078 , 5.1215, 7),(38.9078 , 4.8715, 7),(38.6078 , 4.3715, 7), (38.1130 , 3.9775, 7), #cuad.der.
                    (47.4633 , 27.6493, 7), (47.4333 , 27.0493, 7),  (47.41795 , 26.33015, 7), (47.39595 , 25.73015, 7), (47.3726, 25.0110, 7), #cuad.izq.
                    (37.1405 , 47.7401, 7), (37.4605 , 47.3401, 7), (37.95235 , 46.89345, 7), (38.35235 , 46.45345, 7),  (38.7642, 46.0468, 7),   #puerta 6, circ.der.
                    (0.01 , 0.01, 14) #sprite recompensa, se reposiciona al elegir puerta
        ];
        pass
    #inicializo algunas variables...
    
    gvars.set_log_to_file_counter( 0 )
    gvars.log_to_file_matrix = []
    init_worldmap();
    #####################################
    #inicializo log y declaro el archivo.
    #####################################
    subject_name = str(raw_input("Ingrese nombre de sujeto: "))
    gvars.set_log_file(subject_name)
    from time import strftime, localtime
    cad_temp = strftime("%Y%m%d", localtime())
    #cad_temp = strftime("%Y%m%d %H_%M_%S", localtime())
    file_count_1 = 0
    for i in range(0,999):
        if os.path.isfile("logs/"+gvars.get_log_file()+" "+"%s_hexag_%d.csv"%(cad_temp, i)):
            file_count_1 +=1
           
    print file_count_1 #cantidad de archivos de log que existen de mismo experimento y sujeto en el día actual.
    cad_temp = "logs/"+gvars.get_log_file()+" "+"%s_hexag_%d.csv"%(cad_temp, file_count_1)
    #cad_temp = str('%s log_file.txt' % datetime.datetime.isoformat('_') ) 
    gvars.set_log_file( open(cad_temp,'a') )
    log_to_file("TIME,X,Y,DIRX,DIRY,STROBE,WIN")
    #####################################
    #main thread.
    #####################################
    import threading
    mainThread = threading.Thread(target=mainFunction)
    mainThread.start()

if __name__ == '__main__':
    init_hexag_training()
