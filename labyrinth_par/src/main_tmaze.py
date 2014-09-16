# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *  # @UnusedWildImport

from rect_cl import Rectangle  # @UnresolvedImport
from vectorSimple import vectorSimple  # @UnresolvedImport

#from vars_tmaze import vars_tmaze # @UnresolvedImport

import vars_tmaze
gvars = vars_tmaze.vars_tmaze() #variables del juego a ser accedidas "globalmente"
from vars_tmaze import blit_alpha
from random import randint

import time
import os.path
from pygame.locals import *  # @UnusedWildImport
import threading
import math
import worldManager  # @UnresolvedImport

TMAZE_VERSION = "1.3.0"
CYCLE_LOOP_NUMBER = 2 #cantidad de ciclos que deben pasar para que se ejecuten los movimientos en el mapa 3D
IMG_WIN_MONEY = pygame.image.load('pics/items/money.png')
IMG_LOSE_SADFACE = pygame.image.load('pics/items/sadface.gif')
IMG_RED_FRACTAL = 16 #index de la matriz en worldManager.
IMG_GREEN_FRACTAL = 17 #index..
FPS = 8
WHITE_SQUARE = Rect(0, 0, 100, 100)
LEFT_RECTANGLE = Rectangle(0,8,0,4)
RIGHT_RECTANGLE = Rectangle(0,8,19,999)

vectorInstantaneo = vectorSimple() #vector con el instantáneo de movimiento, x e y dependen del estado de joystick.


gvars.worldMap=[
  [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
  [4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4,4],
  [4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,8],
  [4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,8],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,4],
  [4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,4],
  [4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,4],
  [4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,4],
  [4,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,4],
  [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
];

gvars.sprite_positions=[ ];
 
 
def mainFunction():
    pygame.mixer.init()
    pygame.init()
    pygame.display.set_caption("Laberinto Virtual - T Maze v"+TMAZE_VERSION )
    #pygame.mixer.music.load("MuseUprising.mp3")
    #pygame.mixer.music.play(-1)
    #size = w, h = 1600,900
    size = width_screen, height_screen = 1366,768
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
    
    
    #     weapons = [Weapon("fist"),
    #                Weapon("pistol"),
    #                Weapon("shotgun"),
    #                Weapon("dbshotgun"),
    #                Weapon("chaingun"),
    #                Weapon("plasma"),
    #                Weapon("rocket"),
    #                Weapon("bfg"),
    #                Weapon("chainsaw")
    #                ]
    #weapon_numbers = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_0]
    #weapon = weapons[0]
    
    time.sleep(0.5)
    #wm = worldManager.WorldManager(worldMap,sprite_positions, 12, 11.5, -1, 0, 0, .66)
    wm = worldManager.WorldManager(gvars.worldMap,gvars.sprite_positions, 70, 11.5, -1, 0, 0, 1)
    keep_log = False
    
    #se determina la asociación inicial de fractal con color:
    a= randint(0,99)
    if (a > 50):
        IMG_RED_FRACTAL = 16
        IMG_GREEN_FRACTAL = 17
    else:
        IMG_RED_FRACTAL = 17
        IMG_GREEN_FRACTAL = 16
    
    
    while(True):
        clock.tick(60)
        wm.draw(screen)
        
        #variables de logeo: strobe_value, win_value. Se graban en archivo de log al final del bucle
        strobe_value = 0 # 0=Negro 1=Blanco
        win_value = 0 #0=en juego , 1=perdió , 2=ganó
        #=======================================================================
        # ## Cuadrado blanco con delay 100
        #=======================================================================
        pygame.draw.rect(screen, Color('black'), WHITE_SQUARE)
        if (gvars.get_init_whitebox() < 8):
            pygame.draw.rect(screen, Color('black'), WHITE_SQUARE)
            if (gvars.get_init_whitebox() == 2):
                pygame.draw.rect(screen, Color('white'), WHITE_SQUARE)
                pygame.display.flip()   #Update screen
                pygame.time.delay(100)
                strobe_value = 1
            gvars.set_init_whitebox(gvars.get_init_whitebox()+1)
        
        #=======================================================================
        # # timing for input and FPS counter
        #=======================================================================
        frameTime = float(clock.get_time()) / 1000.0 # frameTime is the time this frame has taken, in seconds
        #text = f.render(str(clock.get_fps()), False, (255, 255, 0))
        #screen.blit(text, text.get_rect(), text.get_rect())

        #=======================================================================
        # ##dibujo barra de puntaje
        #=======================================================================
        pygame.draw.rect(screen, (0,0,235), (50-5,height_screen/2-5-gvars.get_player_score(),15+10,gvars.get_player_score()+1+8), 0)
        pygame.draw.rect(screen, (0,0,255), (50,height_screen/2-gvars.get_player_score(),15,gvars.get_player_score()+1), 0)
        #dibujo arma (la mano)
        #weapon.draw(screen, t)
        #=======================================================================
        # # Animación de ganaste / perdiste:
        #=======================================================================
        if (gvars.get_anim_count() >0 and gvars.get_anim_count() < 60):
                blit_alpha(screen, IMG_WIN_MONEY, (width_screen/2 -250,0), 255-gvars.get_anim_count()*4)
                gvars.set_anim_count(gvars.get_anim_count()+5)
        if (gvars.get_anim_count() >70 and gvars.get_anim_count() < 130):
                blit_alpha(screen, IMG_LOSE_SADFACE, (width_screen/2 -250,0), 255-(gvars.get_anim_count()-70)*4)
                gvars.set_anim_count(gvars.get_anim_count()+5)
        if (gvars.get_anim_count() == 61 or gvars.get_anim_count() == 131):
            gvars.set_anim_count(0)
        
        if (  (gvars.get_experiment_ended() == True) and (gvars.get_anim_count() == 0) ):
            #comienza animación
            #log_to_file("Reinicio de experimento.")
            gvars.set_delay_reboot_button(1)
            gvars.set_init_whitebox(0) #para que en breve ponga la luz blanca.
            gvars.set_user_won(False)
            gvars.set_experiment_ended(False)
            gvars.set_lights_on ( False )
            gvars.set_light_sample(False)
            gvars.sprite_positions=[]
            wm = worldManager.WorldManager(gvars.worldMap,gvars.sprite_positions, 70, 11.5, -1, 0, 0, 1)
            time.sleep(0.1)
        #=======================================================================
        # # speed modifiers (desplazamiento, rotación)
        #=======================================================================
        
        moveSpeed = frameTime * 10.2 # the constant value is in squares / second
        rotSpeed = frameTime * 1.5 # the constant value is in radians / second
        
        #=======================================================================
        # # Toma de datos de Joystick
        #=======================================================================
        #x e y
        x=0
        y=0
        if (joystick_working==True and gvars.get_experiment_ended()==False and keep_log == True ):
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
        
        vectorInstantaneo.x = int(2.2*x_ax)
        vectorInstantaneo.y = int(2.2*y_ax)
        pass
        #=======================================================================
        # #Analizo vector Instantáneo
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
        
        pass
        #=======================================================================
        # #Análisis áreas del juego: región donde activa luces, región de ganar / perder..
        #=======================================================================
        if ( (LEFT_RECTANGLE.contains((wm.camera.x), (wm.camera.y))  ==True) and (gvars.get_experiment_ended() == False)) :
            #log_to_file("Sujeto ingresa a área IZQUIERDA.")
            pygame.draw.rect(screen, Color('white'), WHITE_SQUARE)
            strobe_value = 1
            if ((gvars.get_green_right() == 1 and gvars.get_color_experiment() == 0) or (gvars.get_green_right()==0 and gvars.get_color_experiment() == 1) ):
                gvars.set_user_won(True)
                add_score()
                #log_to_file("Fin experimento.")
                gvars.set_anim_count(1)
                win_value = 2
            else:
                #log_to_file("Sujeto PIERDE.")
                #log_to_file("Fin experimento.")
                win_value = 1
                gvars.set_user_won(False)
                gvars.set_anim_count(71)
        
        
        if ( ( RIGHT_RECTANGLE.contains((wm.camera.x), (wm.camera.y)) ==True)  and (gvars.get_experiment_ended() == False) ):
            #log_to_file("Sujeto ingresa a área DERECHA.")
            pygame.draw.rect(screen, Color('white'), WHITE_SQUARE)
            strobe_value = 1

            
            if ((gvars.get_green_right() == 1 and gvars.get_color_experiment() == 1) or (gvars.get_green_right() == 0 and gvars.get_color_experiment() == 0) ):
                gvars.set_user_won(True)
                gvars.set_anim_count(1)
                add_score()
                win_value = 2
            else:
                #log_to_file("Sujeto PIERDE.")
                win_value = 1
                gvars.set_user_won(False)
                gvars.set_anim_count(71)
        
        if (wm.camera.x < 36 and gvars.get_lights_on() == False):
            #log_to_file("Se encienden señales de COMPARISSON")
            pygame.draw.rect(screen, Color('white'), WHITE_SQUARE)
            strobe_value = 1
            gvars.set_lights_on( True )
            if (gvars.get_green_right() == 0 and gvars.get_color_experiment() == 1):
                    gvars.sprite_positions=[
                      #Tres luces: Sample, y las dos para comparisson
                      #(9.5, 7.3, IMG_GREEN_FRACTAL), #comparisson izquierda
                      #(9.5, 16.7, IMG_RED_FRACTAL), #comparisson derecha
                      (9.5, 7.9, IMG_GREEN_FRACTAL), #comparisson izquierda
                      (9.5, 16.1, IMG_RED_FRACTAL), #comparisson derecha
                      #(40, 16.7, 2), #sample
                    ]
            if (gvars.get_green_right() == 1 and gvars.get_color_experiment() == 1):
                    gvars.sprite_positions=[
                      #Tres luces: Sample, y las dos para comparisson
                      (9.5, 7.9, IMG_RED_FRACTAL), #comparisson izquierda
                      (9.5, 16.1, IMG_GREEN_FRACTAL), #comparisson derecha
                      #(40, 16.7, 2), #sample
                    ]
            if (gvars.get_green_right() == 0 and gvars.get_color_experiment() == 0):
                    gvars.sprite_positions=[
                      #Tres luces: Sample, y las dos para comparisson
                      (9.5, 7.9, IMG_GREEN_FRACTAL), #comparisson izquierda
                      (9.5, 16.1, IMG_RED_FRACTAL), #comparisson derecha
                      #(40, 16.7, 3), #sample
                    ]
            if (gvars.get_green_right() == 1 and gvars.get_color_experiment() == 0):
                    gvars.sprite_positions=[
                      #Tres luces: Sample, y las dos para comparisson
                      (9.5, 7.9, IMG_RED_FRACTAL), #comparisson izquierda
                      (9.5, 16.1, IMG_GREEN_FRACTAL), #comparisson derecha
                      #(40, 16.7, 3), #sample
                    ]
            wm = worldManager.WorldManager(gvars.worldMap,gvars.sprite_positions, wm.camera.x, wm.camera.y, wm.camera.dirx, wm.camera.diry, 0, 1)
            
        #=======================================================================
        # #Se enciende luz de SAMPLE
        #=======================================================================
        if (wm.camera.x < 57 and gvars.get_light_sample() == False):
                gvars.set_light_sample(True)
                #log_to_file("Se encienden señales de SAMPLE")
                pygame.draw.rect(screen, Color('white'), WHITE_SQUARE)
                strobe_value = 1
                gvars.set_color_experiment ( randint(0,99) )
                #determino si el color que debe seguir el usuario es el rojo o verde
                #color_experiment = 1 significa VERDE
                #color_experiment = 0 significa ROJO
                #green_right = 0 significa SEÑAL VERDE EN LADO IZQUIERDO
                #green_right = 1 significa SEÑAL VERDE EN LADO DERECHO
                if (gvars.get_color_experiment() > 49):
                    gvars.set_color_experiment ( 1 ) #GREEN
                    #log_to_file("Color a seguir en el laberinto: VERDE")
                else:
                    gvars.set_color_experiment ( 0 ) #RED
                    #log_to_file("Color a seguir en el laberinto: ROJO")
                                
                #se establece otro número aleatorio para la posición de los colores. Rojo izq, verde der, o al revés:
                gvars.set_green_right( randint(0,99) )
                if (gvars.get_green_right() > 49):
                    gvars.set_green_right( 1 ) #GREEN derecha
                    #log_to_file("Posición del color verde: DERECHA")
                    #log_to_file("Posición del color rojo: IZQUIERDA")
                else:
                    gvars.set_green_right( 0 ) #GREEN izquierda
                    #log_to_file("Posición del color verde: IZQUIERDA")
                    #log_to_file("Posición del color rojo: DERECHA")
                if (gvars.get_green_right() == 0 and gvars.get_color_experiment() == 1):
                        gvars.sprite_positions=[
                          #Tres luces: Sample, y las dos para comparisson
                          #(9.5, 7.3, 2), #comparisson izquierda
                          #(9.5, 16.7, 3), #comparisson derecha
                          (40, 16.7, 2), #sample
                        ]
                if (gvars.get_green_right() == 1 and gvars.get_color_experiment() == 1):
                        gvars.sprite_positions=[
                          #Tres luces: Sample, y las dos para comparisson
                          #(9.5, 7.3, 3), #comparisson izquierda
                          #(9.5, 16.7, 2), #comparisson derecha
                          (40, 16.7, 2), #sample
                        ]
                if (gvars.get_green_right() == 0 and gvars.get_color_experiment() == 0):
                        gvars.sprite_positions=[
                          #Tres luces: Sample, y las dos para comparisson
                          #(9.5, 7.3, 2), #comparisson izquierda
                          #(9.5, 16.7, 3), #comparisson derecha
                          (40, 16.7, 3), #sample
                        ]
                if (gvars.get_green_right() == 1 and gvars.get_color_experiment() == 0):
                        gvars.sprite_positions=[
                          #Tres luces: Sample, y las dos para comparisson
                          #(9.5, 7.3, 3), #comparisson izquierda
                          #(9.5, 16.7, 2), #comparisson derecha
                          (40, 16.7, 3), #sample
                        ]
                wm = worldManager.WorldManager(gvars.worldMap,gvars.sprite_positions, wm.camera.x, wm.camera.y, wm.camera.dirx, wm.camera.diry, 0, 1) 
        
        #############################
        ## Eventos de Pygame (handle del quit)
        #############################
        for event in pygame.event.get(): 

            if event.type == QUIT: 
                import signal
                import sys
                os.kill(os.getpid(), signal.SIGINT)
                sys.exit()
                return 
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    finalize_log()
                    import signal  # @Reimport
                    os.kill(os.getpid(), signal.SIGINT)
                    sys.exit()
                    return
                #elif event.key == K_SPACE:
                #    #resetAll()
                #    print """"""
#                 elif event.key in weapon_numbers:
#                     weapon.stop()
#                     weapon = weapons[weapon_numbers.index(event.key)            
            else:
                pass 
        
        ############################
        # Entradas de Teclado.
        ############################
        if (gvars.get_delay_reboot_button() > 0):
            gvars.set_delay_reboot_button(gvars.get_delay_reboot_button()+1)
        if (gvars.get_delay_reboot_button() == 12):
            gvars.set_delay_reboot_button(0)
        if (gvars.get_experiment_ended()==False):
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                if (gvars.get_delay_reboot_button() ==0):
                    gvars.set_delay_reboot_button(1)
                    #log_to_file("Reinicio de experimento.")
                    gvars.set_init_whitebox(0)
                    gvars.set_user_won(False)
                    gvars.set_experiment_ended(False)
                    gvars.set_lights_on(False)
                    gvars.set_light_sample( False )
                    gvars.sprite_positions=[]
                    wm = worldManager.WorldManager(gvars.worldMap,gvars.sprite_positions, 70, 11.5, -1, 0, 0, 1)
                    time.sleep(0.1)
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
        #pygame.display.update()
        ##########################
        pygame.display.flip()
        if (strobe_value == 1 and win_value == 0):
            keep_log = True
        if (gvars.get_experiment_ended()==False and keep_log==True):
            #tiempo = now.strftime("%H:%M:%S.%f")
            milis = (pygame.time.get_ticks())
            #log_to_file(strftime("%Y-%m-%d  %H:%M:%S", localtime()))
            log_to_file("%d,%f,%f,%f,%f,%d,%d" % (milis, wm.camera.x, wm.camera.y, wm.camera.dirx, wm.camera.diry, strobe_value, win_value) )
        if (win_value > 0):
            gvars.set_experiment_ended(True)
        if (strobe_value == 1 and win_value >0):
            keep_log = False

def add_score():
    #log_to_file("Sujeto GANA.")
    gvars.set_player_score( gvars.get_player_score()+10 )

def log_to_file(string_to_log=""):
    if (gvars.get_log_to_file_counter() < 30):
        gvars.log_to_file_matrix.append(string_to_log+'\n')
        gvars.set_log_to_file_counter( gvars.get_log_to_file_counter()+1 )
    else:
        gvars.log_to_file_matrix.append(string_to_log+'\n')
        gvars.set_log_to_file_counter( gvars.get_log_to_file_counter()+1 )
        for i in range(0,gvars.get_log_to_file_counter()):
            gvars.get_log_file().write(gvars.log_to_file_matrix[i]) # python will convert \n to os.linesep
        gvars.set_log_to_file_counter(0)
        gvars.log_to_file_matrix=[]
        
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


if __name__ == '__main__':
    subject_name = str(raw_input("Ingrese nombre de sujeto: "))
    gvars.set_log_file(  subject_name  )
    gvars.set_log_to_file_counter(0)
    gvars.log_to_file_matrix = []
    
    cad_temp = time.strftime("%Y%m%d", time.localtime())
    #cad_temp = strftime("%Y%m%d %H_%M_%S", localtime())
    file_count_1 = 0
    for i in range(0,999):
        if os.path.isfile("logs/"+gvars.get_log_file()+" "+"%s_tmaze_%d.csv"%(cad_temp, i)):
            file_count_1 +=1
           
    print "Cantidad de archivos de log encontrados: ", file_count_1
    cad_temp_nolog = gvars.get_log_file() +" "+"%s_tmaze_%d.csv"%(cad_temp, file_count_1)
    cad_temp = "logs/"+ gvars.get_log_file() +" "+"%s_tmaze_%d.csv"%(cad_temp, file_count_1)
    #cad_temp = str('%s log_file.txt' % datetime.datetime.isoformat('_') ) 
    try:
        gvars.set_log_file( open(cad_temp,'a') )
    except:
        print "Couldn't set log file. Trying to set log in a different folder."
        try:
            gvars.set_log_file( open(cad_temp_nolog,'a') )
        except:
            print "Log file setup failed."
    
    log_to_file("TIME,X,Y,DIRX,DIRY,STROBE,WIN")
    # Create a thread with game engine.
    #log_to_file("Laberinto: experimento iniciado.")
    mainThread = threading.Thread(target=mainFunction)
    mainThread.start()
    pass
