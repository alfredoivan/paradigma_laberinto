# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *  # @UnusedWildImport
from random import randint
import vectorSimple
import vars_tmaze
import math
import worldManager
import time
import signal
import sys  # @UnusedImport
import os
from rect_cl import Rectangle  # @UnresolvedImport
from Tkinter import *  # @UnusedWildImport




class labyrinth_training():
    
    
    gvars = vars_tmaze.vars_tmaze()  # variables del juego a ser accedidas "globalmente"
    
    PROGRAM_VERSION = "1.3.2"
    CYCLE_LOOP_NUMBER = 2  # cantidad de ciclos que deben pasar para que se ejecuten los movimientos en el mapa 3D
    IMG_WIN_MONEY = pygame.image.load('pics/items/money.png')
    IMG_LOSE_SADFACE = pygame.image.load('pics/items/sadface.gif')
    # FPS = 8
    WHITE_SQUARE = Rect(0, 0, 100, 100)
    IMG_RED_FRACTAL = 16  # index de la matriz en worldManager.
    IMG_GREEN_FRACTAL = 17  # index..
    LEFT_RECTANGLE = Rectangle(0, 8, 0, 4)
    RIGHT_RECTANGLE = Rectangle(0, 8, 19, 999)
    ALL_WINDOW = Rect(0, 0, 1024, 768)
    INTERTRIAL_FRAMES_DELAY = 165
    
    vectorInstantaneo = vectorSimple.vectorSimple()  # vector con el instantáneo de movimiento, x e y dependen del estado de joystick.
    
    
    
    def __init__(self):
        import Tkinter
        import tkMessageBox
        
        top = Tkinter.Tk()
        
        top.title("Paradigma laberinto")
        labyrinth_training.gvars.lab_type = ""
        def hexCallBack():
            tkMessageBox.showinfo("Selection: Hexagon", "Hexagon selected")
            labyrinth_training.gvars.lab_type = "hexag"
            print e1.get()
            labyrinth_training.gvars.subject_name = e1.get()
            top.destroy()
        
        def tmCallBack():
            tkMessageBox.showinfo("Selection: T-Maze", "T-Maze selected")
            labyrinth_training.gvars.lab_type = "tmaze"
            print e1.get()
            labyrinth_training.gvars.subject_name = e1.get()
            top.destroy()
        
        B = Tkinter.Button(top, text="Hexagon", command=hexCallBack, height=5, width=40)
        C = Tkinter.Button(top, text="T-Maze", command=tmCallBack, height=5, width=40)
        
        e1 = Entry(top, width=40)
        e1.delete(0, END)
        e1.insert(0, "Nombre")
        
        
        
        B.pack()
        C.pack()
        e1.pack()
        top.mainloop()
        
        if (labyrinth_training.gvars.lab_type == "hexag"):
            labyrinth_training.init_hexag_training();
        elif labyrinth_training.gvars.lab_type == "tmaze":
            labyrinth_training.init_tmaze_training();
        else:
            # probablemente no eligió ninguno de los dos. cerrar programa.
            sys.exit()
    
    @staticmethod
    def mainFunction():
        labyrinth_training.initPygame()
        
        labyrinth_training.initJoystick()
        
        if labyrinth_training.gvars.lab_type == "hexag":
            labyrinth_training.initHexagMaze()
        elif labyrinth_training.gvars.lab_type == "tmaze":
            labyrinth_training.initTMazeMaze()
        
        
        initial_frames_latency = 7  # 7 latency frames to smooth the initialization.
        #===========================================================================
        # #variables de logeo: strobe_value, win_value. Se graban en archivo de log al final del bucle
        #===========================================================================
        labyrinth_training.gvars.strobe_value = 0  # 0=Negro 1=Blanco
        labyrinth_training.gvars.win_value = 0  # 0=en juego , 1=perdió , 2=ganó
        labyrinth_training.gvars.win_value_f = 0  # se guarda en memoria si se gana o pierde, y se pone en log sólo cuando hay un strobe
        #labyrinth_training.gvars.keep_log = False  # true=logear este ciclo. Permite no logear los intersticios de
        #                       tiempo en donde ya se sabe que ganó y hasta el siguiente strobe de reinicio..
        labyrinth_training.gvars.screen = ( pygame.display.get_surface() )  # again, else tmaze will crash.
        pygame.time.delay(500)
        
        #initially put a intertrial to the user.
        labyrinth_training.gvars.putInterTrial = True
        
        while(True):
            if (initial_frames_latency > 0):
                initial_frames_latency -= 1
            pygame.event.clear() #to remove (presumably old) events from the queue
            
            
            
            labyrinth_training.gvars.wm.draw(labyrinth_training.gvars.screen) #draw everything related to maze, to the surface
            #labyrinth_training.gvars.clock.tick(60)
            labyrinth_training.gvars.clock.tick_busy_loop(60)
            
            
            labyrinth_training.gvars.strobe_value = 0 
            
            
            labyrinth_training.drawScoreBar();
            
            if labyrinth_training.gvars.lab_type == "hexag":
                labyrinth_training.evalHexagWin()
            elif labyrinth_training.gvars.lab_type == "tmaze":
                labyrinth_training.evalTmazeWin()
            
            labyrinth_training.movementSpeedCalculation()
            
            if labyrinth_training.gvars.lab_type == "hexag":
                labyrinth_training.hexagDoorAnimations()
            elif labyrinth_training.gvars.lab_type == "tmaze":
                labyrinth_training.tmazeWLAnimations()
            
            
            
            labyrinth_training.joystickInput()
            
            if labyrinth_training.gvars.lab_type == "hexag":
                labyrinth_training.analyzeHexagCollisions()
            
            labyrinth_training.pyEventsHandle()
            
            labyrinth_training.keyboardInput()
            
            labyrinth_training.drawInterTrial()
            
            labyrinth_training.evalWhiteSquare()
            
            
            
            ##########################
            # pygame.display.update()
            ##########################
            if (initial_frames_latency == 0):
                pygame.display.flip()
                #pygame.time.delay(20)
            
            labyrinth_training.log_frame();
    
    @staticmethod
    def init_hexag_training():
        def init_worldmap_hexag():
            labyrinth_training.gvars.worldMap = [
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 0, 0, 0, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 4],
              [4, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 0, 4],
              [4, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4, 4],
              [4, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4],
              [4, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 4],
              [4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 4],
              [4, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4],
              [4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4],
              [4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4],
              [4, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 4],
              [4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4],
              [4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4],
              [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4],
              [4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4],
              [4, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
              [4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 4, 4],
              [4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4],
              [4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4],
              [4, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4],
              [4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 4],
              [4, 4, 0, 4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 4],
              [4, 0, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4],
              [4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4, 4],
              [4, 0, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 0, 4],
              [4, 0, 0, 4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 0, 0, 0, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
            ];
            
            labyrinth_training.gvars.sprite_positions = [
                        (25.07466, 50.187876, 4),  # círculo
                        (42.308263, 20.924262, 5),  # cuadrado
                        (7.947716, 20.924262, 6),  # triángulo
                        (12.787, 47.724, 7), (12.1535  , 47.01, 7), (11.520  , 46.326, 7), (12.1535  , 47.025, 7),  # puerta 1, circ.izq.
                        (3.275 , 25.2751, 7), (3.277 , 25.8751, 7), (3.2796 , 26.6061, 7), (3.2896 , 27.2061, 7), (3.3097, 27.937, 7),  # triang.der.
                        (11.8644, 4.1717, 7), (11.4644, 4.7717, 7), (11.0158  , 5.1, 7), (11.0158 , 5.1344, 7), (10.6158 , 5.8344, 7), (10.1672 , 6.097, 7),  # triang.izq.
                        (39.7025, 5.7654, 7), (39.3078 , 5.1215, 7), (38.9078 , 4.8715, 7), (38.6078 , 4.3715, 7), (38.1130 , 3.9775, 7),  # cuad.der.
                        (47.4633 , 27.6493, 7), (47.4333 , 27.0493, 7), (47.41795 , 26.33015, 7), (47.39595 , 25.73015, 7), (47.3726, 25.0110, 7),  # cuad.izq.
                        (37.1405 , 47.7401, 7), (37.4605 , 47.3401, 7), (37.95235 , 46.89345, 7), (38.35235 , 46.45345, 7), (38.7642, 46.0468, 7),  # puerta 6, circ.der.
                        (0.01 , 0.01, 14)  # sprite recompensa, se reposiciona al elegir puerta
            ];
            pass
        
        
        pass
        # inicializo algunas variables...
        
        labyrinth_training.gvars.set_log_to_file_counter(0)
        labyrinth_training.gvars.log_to_file_matrix = []
        init_worldmap_hexag();
        #####################################
        # inicializo log y declaro el archivo.
        #####################################
        # subject_name = str(raw_input("Ingrese nombre de sujeto: "))
        labyrinth_training.gvars.set_log_file(labyrinth_training.gvars.subject_name)
        from time import strftime, localtime
        cad_temp = strftime("%Y%m%d", localtime())
        # cad_temp = strftime("%Y%m%d %H_%M_%S", localtime())
        file_count_1 = 0
        for i in range(0, 999):
            if os.path.isfile("logs/" + labyrinth_training.gvars.get_log_file() + " " + "%s_hexag_%d.csv" % (cad_temp, i)):
                file_count_1 += 1
               
        print "previous files found: %d" % file_count_1  # cantidad de archivos de log que existen de mismo experimento y sujeto en el día actual.
        cad_temp = "logs/" + labyrinth_training.gvars.get_log_file() + " " + "%s_hexag_%d.csv" % (cad_temp, file_count_1)
        # cad_temp = str('%s log_file.txt' % datetime.datetime.isoformat('_') ) 
        labyrinth_training.gvars.set_log_file(open(cad_temp, 'a'))
        labyrinth_training.log_to_file("TIME,X,Y,DIRX,DIRY,STROBE,WIN")
        #####################################
        # main thread.
        #####################################
        import threading
        mainThread = threading.Thread(target=labyrinth_training.mainFunction)
        mainThread.start()
    
    @staticmethod
    def init_tmaze_training():
        def init_worldmap_tmaze():
            labyrinth_training.gvars.worldMap = [
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
              [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
              [4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4],
              [4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 8],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4],
              [4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4],
              [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
            ];
            
            labyrinth_training.gvars.sprite_positions = [(25.07466, 50.187876, 4)  ];
            pass
        
        
        pass
        # inicializo algunas variables...
        
        labyrinth_training.gvars.set_log_to_file_counter(0)
        labyrinth_training.gvars.log_to_file_matrix = []
        init_worldmap_tmaze();
        #####################################
        # inicializo log y declaro el archivo.
        #####################################
        # subject_name = str(raw_input("Ingrese nombre de sujeto: "))
        labyrinth_training.gvars.set_log_file(labyrinth_training.gvars.subject_name)
        from time import strftime, localtime
        cad_temp = strftime("%Y%m%d", localtime())
        # cad_temp = strftime("%Y%m%d %H_%M_%S", localtime())
        file_count_1 = 0
        for i in range(0, 999):
            if os.path.isfile("logs/" + labyrinth_training.gvars.get_log_file() + " " + "%s_tmaze_%d.csv" % (cad_temp, i)):
                file_count_1 += 1
               
        print "previous files found: %d" % file_count_1  # cantidad de archivos de log que existen de mismo experimento y sujeto en el día actual.
        cad_temp = "logs/" + labyrinth_training.gvars.get_log_file() + " " + "%s_tmaze_%d.csv" % (cad_temp, file_count_1)
        # cad_temp = str('%s log_file.txt' % datetime.datetime.isoformat('_') ) 
        labyrinth_training.gvars.set_log_file(open(cad_temp, 'a'))
        labyrinth_training.log_to_file("TIME,X,Y,DIRX,DIRY,STROBE,WIN")
        #####################################
        # main thread.
        #####################################
        import threading
        mainThread = threading.Thread(target=labyrinth_training.mainFunction)
        mainThread.start()
    
    @staticmethod
    def initHexagMaze():
        labyrinth_training.gvars.set_anim_count(61)  # to reset on initialization.
        #################################################################
        # ## Elección de puerta que tiene recompensa.
        #################################################################
        rndnum = randint(0, 5)  # @UnusedVariable
        #print rndnum
        rndnum = randint(0, 5)  # @UnusedVariable
        #print rndnum
        rndnum = randint(0, 5)  # @UnusedVariable
        #print rndnum
        rndnum = randint(0, 5)  # @UnusedVariable
        #print rndnum
        rndnum = randint(0, 5)  # @UnusedVariable
        #print rndnum
        
        labyrinth_training.gvars.set_num_puerta(rndnum)
                    
        if rndnum == 0:
                        #print "círculo a la izquierda"
                        labyrinth_training.gvars.set_posx_to_set(10.518899) 
                        labyrinth_training.gvars.set_posy_to_set(48.553612)
        elif rndnum == 1:
                        #print "triángulo a la derecha"
                        labyrinth_training.gvars.set_posx_to_set(1.831244)
                        labyrinth_training.gvars.set_posy_to_set(26.49384)
        elif rndnum == 2:
                        #print "triángulo a la izquierda"
                        labyrinth_training.gvars.set_posx_to_set(10.08041)
                        labyrinth_training.gvars.set_posy_to_set(4.028711)
        elif rndnum == 3:
                        #print "cuadrado a la derecha"
                        labyrinth_training.gvars.set_posx_to_set(40.0201579)
                        labyrinth_training.gvars.set_posy_to_set(4.1025887)
        elif rndnum == 4:
                        #print "cuadrado a la izquierda"
                        labyrinth_training.gvars.set_posx_to_set(48.131992)
                        labyrinth_training.gvars.set_posy_to_set(26.51180)
        elif rndnum == 5:
                        #print "círculo a la derecha"
                        labyrinth_training.gvars.set_posx_to_set(39.487556)
                        labyrinth_training.gvars.set_posy_to_set(48.143990)
        
        # put "money" sprite:
        for i in range(0, len(labyrinth_training.gvars.sprite_positions)):
                        _texnum_ = labyrinth_training.gvars.sprite_positions[i].__getitem__(2)
                        if (_texnum_ == 14):
                            labyrinth_training.gvars.sprite_positions[i] = (labyrinth_training.gvars.get_posx_to_set(), labyrinth_training.gvars.get_posy_to_set(), 14)
        ########################
        # worldmap for hexag.
        # ##
        labyrinth_training.gvars.wm = worldManager.WorldManager(labyrinth_training.gvars.worldMap, labyrinth_training.gvars.sprite_positions, 25, 25.5, -1, 0, 0, 1)
        
    
    @staticmethod
    def initTMazeMaze():
        a = randint(0, 200)
        global IMG_RED_FRACTAL
        global IMG_GREEN_FRACTAL
        if (a > 100):
                
                IMG_RED_FRACTAL = 16
                IMG_GREEN_FRACTAL = 17
        else:
                IMG_RED_FRACTAL = 17
                IMG_GREEN_FRACTAL = 16
        labyrinth_training.randomizeTMazeLights();
        # labyrinth_training.gvars.wm = worldManager.WorldManager(labyrinth_training.gvars.worldMap,labyrinth_training.gvars.sprite_positions, 70, 11.5, -1, 0, 0, 1)
        labyrinth_training.gvars.wm = worldManager.WorldManager(labyrinth_training.gvars.worldMap, labyrinth_training.gvars.sprite_positions, 70, 11.5, -1, 0, 0, 1)
        
    
    @staticmethod
    def evalTmazeWin():
        #=======================================================================
        # #Análisis áreas del juego: región donde activa luces, región de ganar / perder..
        #=======================================================================
        if ((labyrinth_training.LEFT_RECTANGLE.contains(
        (labyrinth_training.gvars.wm.camera.x), (labyrinth_training.gvars.wm.camera.y)) == True) and (
                                            labyrinth_training.gvars.get_experiment_ended() == False)) :
            # log_to_file("Sujeto ingresa a área IZQUIERDA.")
            pygame.draw.rect(labyrinth_training.gvars.screen, Color('white'), labyrinth_training.WHITE_SQUARE)
            # labyrinth_training.gvars.strobe_value = 1
            
            if (labyrinth_training.gvars.get_anim_count() == 0):
                if ((labyrinth_training.gvars.get_green_right() == 1 and labyrinth_training.gvars.get_color_experiment() == 0) or (labyrinth_training.gvars.get_green_right() == 0 and labyrinth_training.gvars.get_color_experiment() == 1)):
                    #sujeto gana
                    labyrinth_training.gvars.set_user_won(True)
                    labyrinth_training.add_score()
                    # log_to_file("Fin experimento.")
                    labyrinth_training.gvars.set_anim_count(1)
                    labyrinth_training.gvars.win_value = 2
                    labyrinth_training.gvars.win_value_f = 2
                    labyrinth_training.gvars.set_init_whitebox(0)
                else:
                    # log_to_file("Sujeto PIERDE.")
                    # log_to_file("Fin experimento.")
                    labyrinth_training.gvars.win_value = 1
                    labyrinth_training.gvars.win_value_f = 1
                    labyrinth_training.gvars.set_user_won(False)
                    labyrinth_training.gvars.set_anim_count(71)
                    labyrinth_training.gvars.set_init_whitebox(0)
        
        
        if ((labyrinth_training.RIGHT_RECTANGLE.contains(
            (labyrinth_training.gvars.wm.camera.x), (labyrinth_training.gvars.wm.camera.y)) == True)  and (
                                    labyrinth_training.gvars.get_experiment_ended() == False)):
            # log_to_file("Sujeto ingresa a área DERECHA.")
            pygame.draw.rect(labyrinth_training.gvars.screen, Color('white'), labyrinth_training.WHITE_SQUARE)
            # labyrinth_training.gvars.strobe_value = 1
            
            
            if (labyrinth_training.gvars.get_anim_count() == 0):
                if ((labyrinth_training.gvars.get_green_right() == 1 and labyrinth_training.gvars.get_color_experiment() == 1) or (labyrinth_training.gvars.get_green_right() == 0 and labyrinth_training.gvars.get_color_experiment() == 0)):
                    #sujeto gana
                    labyrinth_training.gvars.set_user_won(True)
                    labyrinth_training.gvars.set_anim_count(1)
                    labyrinth_training.add_score()
                    labyrinth_training.gvars.win_value = 2
                    labyrinth_training.gvars.win_value_f = 2
                    labyrinth_training.gvars.set_init_whitebox(0)
                else:
                    # log_to_file("Sujeto PIERDE.")
                    labyrinth_training.gvars.win_value = 1
                    labyrinth_training.gvars.win_value_f = 1
                    labyrinth_training.gvars.set_user_won(False)
                    labyrinth_training.gvars.set_anim_count(71)
                    labyrinth_training.gvars.set_init_whitebox(0)
        
        if (labyrinth_training.gvars.wm.camera.x < 36 and labyrinth_training.gvars.get_lights_on() == False):
            # log_to_file("Se encienden señales de COMPARISSON") #los fractales.
            pygame.draw.rect(labyrinth_training.gvars.screen, Color('white'), labyrinth_training.WHITE_SQUARE)
            labyrinth_training.gvars.set_init_whitebox(0)
            # labyrinth_training.gvars.strobe_value = 1
            labyrinth_training.gvars.set_lights_on(True)
            if (labyrinth_training.gvars.get_green_right() == 0 and labyrinth_training.gvars.get_color_experiment() == 1):
                    labyrinth_training.gvars.sprite_positions = [
                      # Tres luces: Sample, y las dos para comparisson
                      # (9.5, 7.3, IMG_GREEN_FRACTAL), #comparisson izquierda
                      # (9.5, 16.7, IMG_RED_FRACTAL), #comparisson derecha
                      (9.5, 7.9, IMG_GREEN_FRACTAL),  # comparisson izquierda
                      (9.5, 16.1, IMG_RED_FRACTAL),  # comparisson derecha
                      # (40, 16.7, 2), #sample
                    ]
            if (labyrinth_training.gvars.get_green_right() == 1 and labyrinth_training.gvars.get_color_experiment() == 1):
                    labyrinth_training.gvars.sprite_positions = [
                      # Tres luces: Sample, y las dos para comparisson
                      (9.5, 7.9, IMG_RED_FRACTAL),  # comparisson izquierda
                      (9.5, 16.1, IMG_GREEN_FRACTAL),  # comparisson derecha
                      # (40, 16.7, 2), #sample
                    ]
            if (labyrinth_training.gvars.get_green_right() == 0 and labyrinth_training.gvars.get_color_experiment() == 0):
                    labyrinth_training.gvars.sprite_positions = [
                      # Tres luces: Sample, y las dos para comparisson
                      (9.5, 7.9, IMG_GREEN_FRACTAL),  # comparisson izquierda
                      (9.5, 16.1, IMG_RED_FRACTAL),  # comparisson derecha
                      # (40, 16.7, 3), #sample
                    ]
            if (labyrinth_training.gvars.get_green_right() == 1 and labyrinth_training.gvars.get_color_experiment() == 0):
                    labyrinth_training.gvars.sprite_positions = [
                      # Tres luces: Sample, y las dos para comparisson
                      (9.5, 7.9, IMG_RED_FRACTAL),  # comparisson izquierda
                      (9.5, 16.1, IMG_GREEN_FRACTAL),  # comparisson derecha
                      # (40, 16.7, 3), #sample
                    ]
            labyrinth_training.gvars.wm = worldManager.WorldManager(labyrinth_training.gvars.worldMap, labyrinth_training.gvars.sprite_positions, labyrinth_training.gvars.wm.camera.x,
                                                 labyrinth_training.gvars.wm.camera.y, labyrinth_training.gvars.wm.camera.dirx, labyrinth_training.gvars.wm.camera.diry, 0, 1)
            
        #=======================================================================
        # #Se enciende luz de SAMPLE
        #=======================================================================
        if (labyrinth_training.gvars.wm.camera.x < 57 and labyrinth_training.gvars.get_light_sample() == False):
                    labyrinth_training.gvars.set_light_sample(True)
                    # log_to_file("Se encienden señales de SAMPLE") #la luz verde/roja
                    pygame.draw.rect(labyrinth_training.gvars.screen, Color('white'), labyrinth_training.WHITE_SQUARE)
                    # labyrinth_training.gvars.strobe_value = 1
                    labyrinth_training.gvars.set_init_whitebox(0)
                    
                    if (labyrinth_training.gvars.get_green_right() == 0 and labyrinth_training.gvars.get_color_experiment() == 1):
                            labyrinth_training.gvars.sprite_positions = [
                              # Tres luces: Sample, y las dos para comparisson
                              # (9.5, 7.3, 2), #comparisson izquierda
                              # (9.5, 16.7, 3), #comparisson derecha
                              (40, 16.7, 2),  # sample
                            ]
                    if (labyrinth_training.gvars.get_green_right() == 1 and labyrinth_training.gvars.get_color_experiment() == 1):
                            labyrinth_training.gvars.sprite_positions = [
                              # Tres luces: Sample, y las dos para comparisson
                              # (9.5, 7.3, 3), #comparisson izquierda
                              # (9.5, 16.7, 2), #comparisson derecha
                              (40, 16.7, 2),  # sample
                            ]
                    if (labyrinth_training.gvars.get_green_right() == 0 and labyrinth_training.gvars.get_color_experiment() == 0):
                            labyrinth_training.gvars.sprite_positions = [
                              # Tres luces: Sample, y las dos para comparisson
                              # (9.5, 7.3, 2), #comparisson izquierda
                              # (9.5, 16.7, 3), #comparisson derecha
                              (40, 16.7, 3),  # sample
                            ]
                    if (labyrinth_training.gvars.get_green_right() == 1 and labyrinth_training.gvars.get_color_experiment() == 0):
                            labyrinth_training.gvars.sprite_positions = [
                              # Tres luces: Sample, y las dos para comparisson
                              # (9.5, 7.3, 3), #comparisson izquierda
                              # (9.5, 16.7, 2), #comparisson derecha
                              (40, 16.7, 3),  # sample
                            ]
                    labyrinth_training.gvars.wm = worldManager.WorldManager(labyrinth_training.gvars.worldMap, labyrinth_training.gvars.sprite_positions, labyrinth_training.gvars.wm.camera.x, labyrinth_training.gvars.wm.camera.y,
                                                          labyrinth_training.gvars.wm.camera.dirx, labyrinth_training.gvars.wm.camera.diry, 0, 1) 
            
    
    @staticmethod
    def evalHexagWin():
            #=======================================================================
            # # Animación de ganaste / perdiste:
            #=======================================================================
            # retardo hasta mostrar animación de ganaste o perdiste
            
            if (labyrinth_training.gvars.get_anim_count() > 200 and labyrinth_training.gvars.get_anim_count() < 210):
                labyrinth_training.gvars.set_anim_count(labyrinth_training.gvars.get_anim_count() + 1)
            if (labyrinth_training.gvars.get_anim_count() == 210):
                labyrinth_training.gvars.set_anim_count (1)
            if (labyrinth_training.gvars.get_anim_count() > 270 and labyrinth_training.gvars.get_anim_count() < 280):
                labyrinth_training.gvars.set_anim_count(labyrinth_training.gvars.get_anim_count() + 1)
            if (labyrinth_training.gvars.get_anim_count() == 280):
                labyrinth_training.gvars.set_anim_count (71)
                
            # animación durante 60 ciclos, de ganaste o perdiste
            if (labyrinth_training.gvars.get_anim_count() > 0 and labyrinth_training.gvars.get_anim_count() < 60):
                    vars_tmaze.blit_alpha(labyrinth_training.gvars.screen, labyrinth_training.IMG_WIN_MONEY, (labyrinth_training.gvars.width_screen / 2 - 250, 0), 255 - labyrinth_training.gvars.get_anim_count() * 4)
                    labyrinth_training.gvars.set_anim_count(labyrinth_training.gvars.get_anim_count() + 4)
            if (labyrinth_training.gvars.get_anim_count() > 70 and labyrinth_training.gvars.get_anim_count() < 130):
                    vars_tmaze.blit_alpha(labyrinth_training.gvars.screen, labyrinth_training.IMG_LOSE_SADFACE, (labyrinth_training.gvars.width_screen / 2 - 250, 0), 255 - (labyrinth_training.gvars.get_anim_count() - 70) * 4)
                    labyrinth_training.gvars.set_anim_count(labyrinth_training.gvars.get_anim_count() + 4)
            if (labyrinth_training.gvars.get_anim_count() == 61 or labyrinth_training.gvars.get_anim_count() == 131):
                labyrinth_training.gvars.set_anim_count (0)  # fin animación, reiniciamos experimento.
                #############################################
                # reincio de experimento
                #############################################
                # log_to_file("Reinicio de experimento.")
                pass
                #print "reinicio de experimento"
                labyrinth_training.gvars.drawInterTrial = labyrinth_training.INTERTRIAL_FRAMES_DELAY;
                labyrinth_training.gvars.set_door_anim (0)
                # Restablecer valores de puerta cerrada, no haría falta en sprite_positions
                for i in range(0, len(labyrinth_training.gvars.sprite_positions)):
                    _texnum_ = labyrinth_training.gvars.sprite_positions[i].__getitem__(2)
                    if (_texnum_ > 7 and  _texnum_ < 14):
                        labyrinth_training.gvars.sprite_positions[i] = (labyrinth_training.gvars.sprite_positions[i].__getitem__(0), labyrinth_training.gvars.sprite_positions[i].__getitem__(1), 7)
                # time.sleep(0.05)
                labyrinth_training.gvars.wm = worldManager.WorldManager(labyrinth_training.gvars.worldMap, labyrinth_training.gvars.sprite_positions, 25, 25.5, -1, 0, 0, 1)
                ########################
                # randomizar la cámara:
                ########################
                temp_rand_num = randint(0, 30) #
                temp_rand_num = randint(0, 30)
                temp_rand_num = randint(0, 30)
                temp_rand_num = randint(0, 30)
                temp_rand_num = randint(0, 30)
                flt_num = (temp_rand_num * 2 * 3.1415) / 30
                # en flt_num tengo un ángulo aleatorio entre 0 y 2pi
                oldDirX = labyrinth_training.gvars.wm.camera.dirx
                labyrinth_training.gvars.wm.camera.dirx = labyrinth_training.gvars.wm.camera.dirx * math.cos(flt_num) - labyrinth_training.gvars.wm.camera.diry * math.sin(flt_num)
                labyrinth_training.gvars.wm.camera.diry = oldDirX * math.sin(flt_num) + labyrinth_training.gvars.wm.camera.diry * math.cos(flt_num)
                oldPlaneX = labyrinth_training.gvars.wm.camera.planex
                labyrinth_training.gvars.wm.camera.planex = labyrinth_training.gvars.wm.camera.planex * math.cos(flt_num) - labyrinth_training.gvars.wm.camera.planey * math.sin(flt_num)
                labyrinth_training.gvars.wm.camera.planey = oldPlaneX * math.sin(flt_num) + labyrinth_training.gvars.wm.camera.planey * math.cos(flt_num)
                # ##
                # remuevo el ítem de ganado, para que no se vea entre las texturas de puerta:
                for i in range(0, len(labyrinth_training.gvars.sprite_positions)):
                        _texnum_ = labyrinth_training.gvars.sprite_positions[i].__getitem__(2)
                        if (_texnum_ == 14):
                            labyrinth_training.gvars.sprite_positions[i] = (0.5, 0.5, 14)
                # en cada reinicio: se pone cuadrado blanco
                labyrinth_training.gvars.set_init_whitebox(0)  # en 2 ciclos se pondrá efectivamente el cuadrado blanco.
                labyrinth_training.gvars.win_value = 0
                labyrinth_training.gvars.win_value_f = 0
            pass
    
    @staticmethod
    def hexagDoorAnimations():
            # evaluates door animations and set win or lose.
            if (labyrinth_training.gvars.get_door_anim() > 0):
                if (labyrinth_training.gvars.get_door_anim() < 10):
                    for i in range(0, len(labyrinth_training.gvars.wm.sprite_positions)):
                        if (labyrinth_training.gvars.wm.sprite_positions[i].__getitem__(2) == labyrinth_training.gvars.get_door_anim() + 6):
                            labyrinth_training.gvars.wm.sprite_positions[i] = (labyrinth_training.gvars.wm.sprite_positions[i].__getitem__(0), labyrinth_training.gvars.wm.sprite_positions[i].__getitem__(1), labyrinth_training.gvars.get_door_anim() + 7)
                if (labyrinth_training.gvars.get_door_anim() == 60):
                    labyrinth_training.gvars.set_door_anim(6)
                    # para ver el cuadrado blanco ya:
                    labyrinth_training.gvars.set_init_whitebox(0)
                if (labyrinth_training.gvars.get_door_anim() == 5):
                    labyrinth_training.gvars.set_door_anim(60)
                if (labyrinth_training.gvars.get_door_anim() == 50):
                    labyrinth_training.gvars.set_door_anim(5)
                if (labyrinth_training.gvars.get_door_anim() == 4):
                    labyrinth_training.gvars.set_door_anim(50)
                if (labyrinth_training.gvars.get_door_anim() == 40):
                    labyrinth_training.gvars.set_door_anim(4)
                if (labyrinth_training.gvars.get_door_anim() == 3):
                    labyrinth_training.gvars.set_door_anim(40)
                if (labyrinth_training.gvars.get_door_anim() == 30):
                    labyrinth_training.gvars.set_door_anim(3)
                if (labyrinth_training.gvars.get_door_anim() == 2):
                    labyrinth_training.gvars.set_door_anim(30)
                if (labyrinth_training.gvars.get_door_anim() == 20):
                    labyrinth_training.gvars.set_door_anim(2)
                if (labyrinth_training.gvars.get_door_anim() == 1):
                    labyrinth_training.gvars.set_door_anim(20)  # para enlentecer un poco la animación
                    # acá pongo el gráfico de ítem ganado, no se pone antes para que no se vea entre intersticios de puerta
                    for i in range(0, len(labyrinth_training.gvars.sprite_positions)):
                        _texnum_ = labyrinth_training.gvars.sprite_positions[i].__getitem__(2)
                        if (_texnum_ == 14):
                            labyrinth_training.gvars.sprite_positions[i] = (labyrinth_training.gvars.get_posx_to_set(), labyrinth_training.gvars.get_posy_to_set(), 14)
            
            pass
    
    @staticmethod
    def tmazeWLAnimations():
        #=======================================================================
        # # Animación de ganaste / perdiste:
        #=======================================================================
        if (labyrinth_training.gvars.get_anim_count() > 0 and labyrinth_training.gvars.get_anim_count() < 60):
            labyrinth_training.gvars.notPlayable = True
            vars_tmaze.blit_alpha(labyrinth_training.gvars.screen, labyrinth_training.IMG_WIN_MONEY, (labyrinth_training.gvars.width_screen / 2 - 250, 0), 255 - labyrinth_training.gvars.get_anim_count() * 4)
            labyrinth_training.gvars.set_anim_count(labyrinth_training.gvars.get_anim_count() + 3)
        if (labyrinth_training.gvars.get_anim_count() > 70 and labyrinth_training.gvars.get_anim_count() < 130):
            labyrinth_training.gvars.notPlayable = True
            vars_tmaze.blit_alpha(labyrinth_training.gvars.screen, labyrinth_training.IMG_LOSE_SADFACE, (labyrinth_training.gvars.width_screen / 2 - 250, 0), 255 - (labyrinth_training.gvars.get_anim_count() - 70) * 4)
            labyrinth_training.gvars.set_anim_count(labyrinth_training.gvars.get_anim_count() + 3)
        if (labyrinth_training.gvars.get_anim_count() == 61 or labyrinth_training.gvars.get_anim_count() == 131):
            labyrinth_training.gvars.set_anim_count(0)
            labyrinth_training.gvars.set_experiment_ended(True)
        
        
        if ((labyrinth_training.gvars.get_experiment_ended() == True) and (labyrinth_training.gvars.get_anim_count() == 0)):
            # comienza animación
            # log_to_file("Reinicio de experimento.")
            labyrinth_training.randomizeTMazeLights();
            labyrinth_training.gvars.set_delay_reboot_button(1)
            labyrinth_training.gvars.set_init_whitebox(0)  # para que en breve ponga la luz blanca.
            labyrinth_training.gvars.putInterTrial = True
            labyrinth_training.gvars.set_user_won(False)
            labyrinth_training.gvars.set_experiment_ended(False)
            labyrinth_training.gvars.set_lights_on (False)
            labyrinth_training.gvars.set_light_sample(False)
            labyrinth_training.gvars.sprite_positions = []
            labyrinth_training.gvars.win_value = 3 #para intertrial
            labyrinth_training.gvars.win_value_f = 3 #para intertrial
            labyrinth_training.gvars.wm = worldManager.WorldManager(labyrinth_training.gvars.worldMap, labyrinth_training.gvars.sprite_positions, 70, 11.5, -1, 0, 0, 1)
            #time.sleep(0.1)
    
    @staticmethod
    def randomizeTMazeLights():
        labyrinth_training.gvars.set_color_experiment (randint(0, 200))
        # determino si el color que debe seguir el usuario es el rojo o verde
        # color_experiment = 1 significa VERDE
        # color_experiment = 0 significa ROJO
        # green_right = 0 significa SEÑAL VERDE EN LADO IZQUIERDO
        # green_right = 1 significa SEÑAL VERDE EN LADO DERECHO
        pass
        #print labyrinth_training.gvars.get_color_experiment()
        if (labyrinth_training.gvars.get_color_experiment() > 100):
            labyrinth_training.gvars.set_color_experiment (1)  # GREEN
            # log_to_file("Color a seguir en el laberinto: VERDE")
        else:
            labyrinth_training.gvars.set_color_experiment (0)  # RED
            # log_to_file("Color a seguir en el laberinto: ROJO")
        pass
        # se establece otro número aleatorio para la posición de los colores. Rojo izq, verde der, o al revés:
        labyrinth_training.gvars.set_green_right(randint(0, 200))
        if (labyrinth_training.gvars.get_green_right() > 100):
            labyrinth_training.gvars.set_green_right(1)  # GREEN derecha
            # log_to_file("Posición del color verde: DERECHA")
            # log_to_file("Posición del color rojo: IZQUIERDA")
        else:
            labyrinth_training.gvars.set_green_right(0)  # GREEN izquierda
            # log_to_file("Posición del color verde: IZQUIERDA")
            # log_to_file("Posición del color rojo: DERECHA")
        pass
    
    @staticmethod
    def analyzeHexagCollisions():
            ##################################################################
            # Análisis áreas. Colisiones:
            ##################################################################
            
            colision_puerta = False
            DOOR_RADIUS_POW2 = 9.9225  # radio 3.15
            
            # Puerta que está en: (12.1535  , 47.025, 7),
            if (pow(abs(labyrinth_training.gvars.wm.camera.x - 12.1535), 2) < DOOR_RADIUS_POW2 and  pow(abs(labyrinth_training.gvars.wm.camera.y - 47.025), 2) < DOOR_RADIUS_POW2):
                colision_puerta = True
                if (labyrinth_training.gvars.get_num_puerta() == 0):
                    # print "ganaste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (201)
                        labyrinth_training.gvars.win_value_f = 2
                        labyrinth_training.add_score()
                else:
                    # print "perdiste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (271)
                        labyrinth_training.gvars.win_value_f = 1
            
            
            # Puerta que está en: (3.2796 , 26.6061, 7),
            if (pow(abs(labyrinth_training.gvars.wm.camera.x - 3.2796), 2) < DOOR_RADIUS_POW2 and  pow(abs(labyrinth_training.gvars.wm.camera.y - 26.6061), 2) < DOOR_RADIUS_POW2):
                colision_puerta = True
                if (labyrinth_training.gvars.get_num_puerta() == 1):
                    # print "ganaste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (201)
                        labyrinth_training.gvars.win_value_f = 2
                        labyrinth_training.add_score()
                else:
                    # print "perdiste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (271)
                        labyrinth_training.gvars.win_value_f = 1
                
            # Puerta que está en: (11.0158 , 5.1344, 7),
            if (pow(abs(labyrinth_training.gvars.wm.camera.x - 11.0158), 2) < DOOR_RADIUS_POW2 and  pow(abs(labyrinth_training.gvars.wm.camera.y - 5.1344), 2) < DOOR_RADIUS_POW2):
                colision_puerta = True
                if (labyrinth_training.gvars.get_num_puerta() == 2):
                    # print "ganaste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (201)
                        labyrinth_training.gvars.win_value_f = 2
                        labyrinth_training.add_score()
                else:
                    # print "perdiste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (271)
                        labyrinth_training.gvars.win_value_f = 1
            
            # Puerta que está en: (38.9078 , 4.8715, 7),
            if (pow(abs(labyrinth_training.gvars.wm.camera.x - 38.9078), 2) < DOOR_RADIUS_POW2 and  pow(abs(labyrinth_training.gvars.wm.camera.y - 4.8715), 2) < DOOR_RADIUS_POW2):
                colision_puerta = True
                if (labyrinth_training.gvars.get_num_puerta() == 3):
                    # print "ganaste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (201)
                        labyrinth_training.gvars.win_value_f = 2
                        labyrinth_training.add_score()
                else:
                    # print "perdiste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (271)
                        labyrinth_training.gvars.win_value_f = 1
                
            # Puerta que está en: (47.41795 , 26.33015, 7),
            if (pow(abs(labyrinth_training.gvars.wm.camera.x - 47.41795) , 2) < DOOR_RADIUS_POW2 and  pow(abs(labyrinth_training.gvars.wm.camera.y - 26.33015) , 2) < DOOR_RADIUS_POW2):
                colision_puerta = True
                if (labyrinth_training.gvars.get_num_puerta() == 4):
                    # print "ganaste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (201)
                        labyrinth_training.gvars.win_value_f = 2
                        labyrinth_training.add_score()
                else:
                    # print "perdiste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (271)
                        labyrinth_training.gvars.win_value_f = 1
            
            # Puerta que está en: (37.95235 , 46.89345, 7)
            if (pow(abs(labyrinth_training.gvars.wm.camera.x - 37.95235) , 2) < DOOR_RADIUS_POW2 and  pow(abs(labyrinth_training.gvars.wm.camera.y - 46.89345), 2) < DOOR_RADIUS_POW2):
                colision_puerta = True
                if (labyrinth_training.gvars.get_num_puerta() == 5):
                    # print "ganaste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (201)
                        labyrinth_training.gvars.win_value_f = 2
                        labyrinth_training.add_score()
                else:
                    # print "perdiste"
                    if (labyrinth_training.gvars.get_anim_count () == 0):
                        labyrinth_training.gvars.set_anim_count (271)
                        labyrinth_training.gvars.win_value_f = 1
                    
                
            
            if (colision_puerta):
                # print "colsión"
                if (labyrinth_training.gvars.get_door_anim () == 0):
                        labyrinth_training.gvars.set_door_anim (1)
            pass
    
    @staticmethod
    def evalWhiteSquare():
        ##########################
        # Cuadrado blanco: se evalúa si dibujarlo o dibujar un cuadrado negro.
        ##########################
        pygame.draw.rect(labyrinth_training.gvars.screen, Color('black'), labyrinth_training.WHITE_SQUARE)
        if (labyrinth_training.gvars.get_init_whitebox() < 8):
            if (labyrinth_training.gvars.get_init_whitebox() == 0):
                labyrinth_training.gvars.hasStarted = True
                pygame.draw.rect(labyrinth_training.gvars.screen, Color('white'), labyrinth_training.WHITE_SQUARE)
                labyrinth_training.gvars.strobe_value = 1
                pygame.display.update(labyrinth_training.WHITE_SQUARE)
                pygame.time.delay(50)
                labyrinth_training.gvars.strobe_value = 1
                labyrinth_training.onlyLog();
                pygame.time.delay(50)
                pygame.draw.rect(labyrinth_training.gvars.screen, Color('black'), labyrinth_training.WHITE_SQUARE)
                pygame.display.update(labyrinth_training.WHITE_SQUARE)
                labyrinth_training.gvars.win_value = labyrinth_training.gvars.win_value_f
                labyrinth_training.gvars.strobe_value = 0
            labyrinth_training.gvars.set_init_whitebox(labyrinth_training.gvars.get_init_whitebox() + 1)
        pass
    
    @staticmethod
    def keyboardInput():
            if (labyrinth_training.gvars.strobe_value == 1):
                return;
            if (labyrinth_training.gvars.drawInterTrial > 0):
                return;
            if (labyrinth_training.gvars.notPlayable):
                return;
            #=======================================================================
            # # Entradas de Teclado.
            #=======================================================================
            if (labyrinth_training.gvars.get_delay_reboot_button() > 0):
                labyrinth_training.gvars.set_delay_reboot_button(labyrinth_training.gvars.get_delay_reboot_button() + 1)
                
            if (labyrinth_training.gvars.get_delay_reboot_button() == 12):
                labyrinth_training.gvars.set_delay_reboot_button(0)
            if (labyrinth_training.gvars.get_door_anim() == 0 ):
                keys = pygame.key.get_pressed()
                if keys[K_SPACE]:
                    # Forzar Reinicio: como si hubiera ganado o perdido.
                    if (labyrinth_training.gvars.get_delay_reboot_button() == 0):
                        labyrinth_training.gvars.set_delay_reboot_button(1)
                        labyrinth_training.gvars.set_anim_count (61)
                ###############
                # Desplazarse con UP DOWN LEFT RIGHT
                if keys[K_UP]:
                    # move forward if no wall in front of you
                    try:
                        moveX = labyrinth_training.gvars.wm.camera.x + labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed
                        if(labyrinth_training.gvars.worldMap[int(moveX)][int(labyrinth_training.gvars.wm.camera.y)] == 0 and labyrinth_training.gvars.worldMap[int(moveX + 0.1)][int(labyrinth_training.gvars.wm.camera.y)] == 0):labyrinth_training.gvars.wm.camera.x += labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed
                        moveY = labyrinth_training.gvars.wm.camera.y + labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed
                        if(labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x)][int(moveY)] == 0 and labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x)][int(moveY + 0.1)] == 0):labyrinth_training.gvars.wm.camera.y += labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed
                    except:
                        pass
                if keys[K_DOWN]:
                    # move backwards if no wall behind you
                    try:
                        if(labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x - labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed)][int(labyrinth_training.gvars.wm.camera.y)] == 0):labyrinth_training.gvars.wm.camera.x -= labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed
                        if(labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x)][int(labyrinth_training.gvars.wm.camera.y - labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed)] == 0):labyrinth_training.gvars.wm.camera.y -= labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed
                    except:
                        pass
                if (keys[K_RIGHT] and not keys[K_DOWN]) or (keys[K_LEFT] and keys[K_DOWN]):
                    # rotate to the right
                    # both camera direction and camera plane must be rotated
                    oldDirX = labyrinth_training.gvars.wm.camera.dirx
                    labyrinth_training.gvars.wm.camera.dirx = labyrinth_training.gvars.wm.camera.dirx * math.cos(-labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.diry * math.sin(-labyrinth_training.gvars.rotSpeed)
                    labyrinth_training.gvars.wm.camera.diry = oldDirX * math.sin(-labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.diry * math.cos(-labyrinth_training.gvars.rotSpeed)
                    oldPlaneX = labyrinth_training.gvars.wm.camera.planex
                    labyrinth_training.gvars.wm.camera.planex = labyrinth_training.gvars.wm.camera.planex * math.cos(-labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.planey * math.sin(-labyrinth_training.gvars.rotSpeed)
                    labyrinth_training.gvars.wm.camera.planey = oldPlaneX * math.sin(-labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.planey * math.cos(-labyrinth_training.gvars.rotSpeed)
                if (keys[K_LEFT] and not keys[K_DOWN]) or (keys[K_RIGHT] and keys[K_DOWN]): 
                    # rotate to the left
                    # both camera direction and camera plane must be rotated
                    oldDirX = labyrinth_training.gvars.wm.camera.dirx
                    labyrinth_training.gvars.wm.camera.dirx = labyrinth_training.gvars.wm.camera.dirx * math.cos(labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.diry * math.sin(labyrinth_training.gvars.rotSpeed)
                    labyrinth_training.gvars.wm.camera.diry = oldDirX * math.sin(labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.diry * math.cos(labyrinth_training.gvars.rotSpeed)
                    oldPlaneX = labyrinth_training.gvars.wm.camera.planex
                    labyrinth_training.gvars.wm.camera.planex = labyrinth_training.gvars.wm.camera.planex * math.cos(labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.planey * math.sin(labyrinth_training.gvars.rotSpeed)
                    labyrinth_training.gvars.wm.camera.planey = oldPlaneX * math.sin(labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.planey * math.cos(labyrinth_training.gvars.rotSpeed)
                
            
    
    @staticmethod
    def joystickInput():
            if (labyrinth_training.gvars.drawInterTrial > 0):
                return;
            if (labyrinth_training.gvars.strobe_value == 1):
                return;
            ############################################
            # Toma de datos de Joystick
            ############################################
            pass
            # x e y
            
            x = 0
            y = 0
            if (labyrinth_training.gvars.joystick_working == True and labyrinth_training.gvars.get_door_anim() == 0):
                x = labyrinth_training.gvars.my_joystick.get_axis(0)
                y = labyrinth_training.gvars.my_joystick.get_axis(1)
            x_ax1 = int(x)
            x_ax2 = int(x + 0.1)
            x_ax = 0
            if x_ax1 == -1:
                x_ax = -1
            if x_ax2 == 1:
                x_ax = 1
            y_ax1 = int(y)
            y_ax2 = int(y + 0.1)
            y_ax = 0
            if y_ax1 == -1:
                y_ax = -1
            if y_ax2 == 1:
                y_ax = 1
            labyrinth_training.vectorInstantaneo.x = int(2.2 * x_ax)
            labyrinth_training.vectorInstantaneo.y = int(2.2 * y_ax)
            labyrinth_training.forceInstantVectorAnalysis()
    
    @staticmethod
    def forceInstantVectorAnalysis():
            #=======================================================================
            # #Analizo vector Instantáneo (datos tomados de joystick)
            #=======================================================================
            if labyrinth_training.vectorInstantaneo.x < 0:
                # for each rotation unit divided by 30 (maximum vector module allowed)
                # rotate to the left
                # both camera direction and camera plane must be rotated
                oldDirX = labyrinth_training.gvars.wm.camera.dirx
                labyrinth_training.gvars.wm.camera.dirx = labyrinth_training.gvars.wm.camera.dirx * math.cos(labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.diry * math.sin(labyrinth_training.gvars.rotSpeed)
                labyrinth_training.gvars.wm.camera.diry = oldDirX * math.sin(labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.diry * math.cos(labyrinth_training.gvars.rotSpeed)
                oldPlaneX = labyrinth_training.gvars.wm.camera.planex
                labyrinth_training.gvars.wm.camera.planex = labyrinth_training.gvars.wm.camera.planex * math.cos(labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.planey * math.sin(labyrinth_training.gvars.rotSpeed)
                labyrinth_training.gvars.wm.camera.planey = oldPlaneX * math.sin(labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.planey * math.cos(labyrinth_training.gvars.rotSpeed)
            if labyrinth_training.vectorInstantaneo.y < 0:
                # print "movió arriba"
                moveX = labyrinth_training.gvars.wm.camera.x + labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed
                if(labyrinth_training.gvars.worldMap[int(moveX)][int(labyrinth_training.gvars.wm.camera.y)] == 0 and labyrinth_training.gvars.worldMap[int(moveX + 0.1)][int(labyrinth_training.gvars.wm.camera.y)] == 0):labyrinth_training.gvars.wm.camera.x += labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed
                moveY = labyrinth_training.gvars.wm.camera.y + labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed
                if(labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x)][int(moveY)] == 0 and labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x)][int(moveY + 0.1)] == 0):labyrinth_training.gvars.wm.camera.y += labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed
            if labyrinth_training.vectorInstantaneo.x > 0:
                # print "movió derecha"
                # rotate to the right
                # both camera direction and camera plane must be rotated
                oldDirX = labyrinth_training.gvars.wm.camera.dirx
                labyrinth_training.gvars.wm.camera.dirx = labyrinth_training.gvars.wm.camera.dirx * math.cos(-labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.diry * math.sin(-labyrinth_training.gvars.rotSpeed)
                labyrinth_training.gvars.wm.camera.diry = oldDirX * math.sin(-labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.diry * math.cos(-labyrinth_training.gvars.rotSpeed)
                oldPlaneX = labyrinth_training.gvars.wm.camera.planex
                labyrinth_training.gvars.wm.camera.planex = labyrinth_training.gvars.wm.camera.planex * math.cos(-labyrinth_training.gvars.rotSpeed) - labyrinth_training.gvars.wm.camera.planey * math.sin(-labyrinth_training.gvars.rotSpeed)
                labyrinth_training.gvars.wm.camera.planey = oldPlaneX * math.sin(-labyrinth_training.gvars.rotSpeed) + labyrinth_training.gvars.wm.camera.planey * math.cos(-labyrinth_training.gvars.rotSpeed)
            if labyrinth_training.vectorInstantaneo.y > 0:
                # print "movió abajo"
                # move backwards if no wall behind you
                if(labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x - labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed)][int(labyrinth_training.gvars.wm.camera.y)] == 0):labyrinth_training.gvars.wm.camera.x -= labyrinth_training.gvars.wm.camera.dirx * labyrinth_training.gvars.moveSpeed
                if(labyrinth_training.gvars.worldMap[int(labyrinth_training.gvars.wm.camera.x)][int(labyrinth_training.gvars.wm.camera.y - labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed)] == 0):labyrinth_training.gvars.wm.camera.y -= labyrinth_training.gvars.wm.camera.diry * labyrinth_training.gvars.moveSpeed
            #reset instant vector to 0
            labyrinth_training.vectorInstantaneo.x = 0
            labyrinth_training.vectorInstantaneo.y = 0
    
    @staticmethod
    def pyEventsHandle():
            #############################
            # # Eventos de Pygame (handle del quit)
            #############################
            for event in pygame.event.get(): 
                if event.type == QUIT: 
                    labyrinth_training.finalize_log()
                    os.kill(os.getpid(), signal.SIGINT)
                    sys.exit()
                    return 
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        labyrinth_training.finalize_log()
                        os.kill(os.getpid(), signal.SIGINT)
                        sys.exit()
                        return
                    # elif event.key == K_SPACE:
                    #    #resetAll()
                    #    print """"""      
                else:
                    pass 
    
    @staticmethod
    def movementSpeedCalculation():
            # timing for input and FPS counter
            frameTime = float(labyrinth_training.gvars.clock.get_time()) / 1000.0  # frameTime is the time this frame has taken, in seconds
            # text = f.render(str(clock.get_fps()), False, (255, 255, 0))
            # screen.blit(text, text.get_rect(), text.get_rect())
            ###############################################
            # speed modifiers (desplazamiento, rotación)
            ###############################################
            #labyrinth_training.gvars.moveSpeed = frameTime * 10.2  # the constant value is in squares / second
            #labyrinth_training.gvars.rotSpeed = frameTime * 1.5  # the constant value is in radians / second
            labyrinth_training.gvars.moveSpeed = frameTime * 6.63  # the constant value is in squares / second
            labyrinth_training.gvars.rotSpeed = frameTime * 0.975  # the constant value is in radians / second
    
    @staticmethod
    def initJoystick():
        # Initialize the joysticks
        labyrinth_training.gvars.joystick_working = False
        try:
            pygame.joystick.init()
            labyrinth_training.gvars.my_joystick = pygame.joystick.Joystick(0)
            labyrinth_training.gvars.my_joystick.init()
            labyrinth_training.gvars.joystick_working = True
        except:
            # log_to_file("Joystick incompatible o no encontrado.")
            labyrinth_training.gvars.joystick_working = False
        time.sleep(0.5)
    
    @staticmethod
    def initPygame():
        pygame.mixer.init()
        pygame.init()
        if labyrinth_training.gvars.lab_type == "hexag":
            st = "Hexágono";
        else:
            st = "T-Maze"
        pygame.display.set_caption("Laberinto Virtual - %s v%s" % (st , str(labyrinth_training.PROGRAM_VERSION)))
        
        # size = w, h = 1600,900
        labyrinth_training.gvars.size = labyrinth_training.gvars.width_screen, labyrinth_training.gvars.height_screen = 1366, 768
        #labyrinth_training.gvars.size = labyrinth_training.gvars.width_screen, labyrinth_training.gvars.height_screen = 640, 480
        
        global ALL_WINDOW
        ALL_WINDOW = Rect(0, 0, 1366, 768)
        #ALL_WINDOW = Rect(0, 0, 640, 480)
        
        # window = pygame.display.set_mode(size)
        labyrinth_training.gvars.mainWindow = pygame.display.set_mode(labyrinth_training.gvars.size, pygame.FULLSCREEN)
        # pygame.display.set_mode(labyrinth_training.gvars.size, pygame.RESIZABLE)
        
        
        labyrinth_training.gvars.screen = pygame.display.get_surface()
        # pixScreen = pygame.surfarray.pixels2d(screen)
        pygame.mouse.set_visible(False)
        labyrinth_training.gvars.clock = pygame.time.Clock()
        time.sleep(0.5)
    
    @staticmethod
    def drawScoreBar():
        #=======================================================================
        # ##dibujo barra de puntaje
        #=======================================================================
        pygame.draw.rect(labyrinth_training.gvars.screen, (0, 0, 235), (50 - 5, labyrinth_training.gvars.height_screen / 2 - 5 - labyrinth_training.gvars.get_player_score(), 15 + 10, labyrinth_training.gvars.get_player_score() + 1 + 8), 0)
        pygame.draw.rect(labyrinth_training.gvars.screen, (0, 0, 255), (50, labyrinth_training.gvars.height_screen / 2 - labyrinth_training.gvars.get_player_score(), 15, labyrinth_training.gvars.get_player_score() + 1), 0)
        pass
    
    @staticmethod
    def drawInterTrial():
        if (labyrinth_training.gvars.putInterTrial == True):
                labyrinth_training.gvars.drawInterTrial = labyrinth_training.INTERTRIAL_FRAMES_DELAY;
                labyrinth_training.gvars.putInterTrial = False;
                labyrinth_training.gvars.notPlayable = False
        pass
        if (labyrinth_training.gvars.drawInterTrial == labyrinth_training.INTERTRIAL_FRAMES_DELAY):
            # print "strobe start"
            labyrinth_training.gvars.set_init_whitebox(0)
        if (labyrinth_training.gvars.drawInterTrial == 1):
            # print "strobe end"
            labyrinth_training.gvars.set_init_whitebox(0)
            labyrinth_training.gvars.win_value = 0 #set to trial start
            labyrinth_training.gvars.win_value_f = 0 #set to trial start
            labyrinth_training.gvars.drawInterTrial = 0
            labyrinth_training.gvars.trialStarting = 1
            if (labyrinth_training.gvars.trainingStarting == 1 and labyrinth_training.gvars.lab_type == "hexag"):
                labyrinth_training.gvars.trainingStarting_f = 1
                labyrinth_training.gvars.trainingStarting = 0;
        if (labyrinth_training.gvars.drawInterTrial > 0):
            # pygame.draw.rect(labyrinth_training.gvars.screen, pygame.color.Color., Rect, width=0)
            # print "drawing intertrial: %d" %labyrinth_training.gvars.drawInterTrial
            pygame.draw.rect(labyrinth_training.gvars.screen, Color('black'), ALL_WINDOW)
            # pygame.draw.circle(labyrinth_training.gvars.screen, Color('white'), (labyrinth_training.gvars.width_screen / 2, labyrinth_training.gvars.height_screen/2), 10, width=10)
            pygame.draw.circle(labyrinth_training.gvars.screen, Color('white'), (labyrinth_training.gvars.width_screen / 2, labyrinth_training.gvars.height_screen / 2), 10, 0)
            # pygame.draw.rect(labyrinth_training.gvars.screen, Color('black'), ALL_WINDOW)
            labyrinth_training.gvars.drawInterTrial -= 1 
            
        pass
    
    @staticmethod
    def log_frame():
            #=======================================================================
            # ## Log to file:
            #=======================================================================
            # will only log during trial, after door opening and before trial starts again, no logging..
            if (labyrinth_training.gvars.hasStarted == False):
                return;
            if (labyrinth_training.gvars.drawInterTrial > 0 and labyrinth_training.gvars.strobe_value == 0):
                #intertrial, so put win_value 3
                labyrinth_training.gvars.win_value = 3
            labyrinth_training.onlyLog();
            # print (labyrinth_training.gvars.wm.camera.x), labyrinth_training.gvars.wm.camera.y
#             if (labyrinth_training.gvars.strobe_value == 1 and labyrinth_training.gvars.win_value == 0):
#                 # empezar a logear
#                 labyrinth_training.gvars.keep_log = True
#             elif (labyrinth_training.gvars.strobe_value == 1 and labyrinth_training.gvars.win_value > 0):
#                 labyrinth_training.gvars.keep_log = False
            pass
    
    @staticmethod
    def onlyLog():
        if (labyrinth_training.gvars.trialStarting == 1 and labyrinth_training.gvars.lab_type == "tmaze"):
                    #trial is just starting, in tmaze case, put type of trial in the strobe field.
                    labyrinth_training.gvars.strobe_value = 9;
                    if (labyrinth_training.gvars.get_color_experiment() == 1 and labyrinth_training.gvars.get_green_right() == 1):
                        #color verde, verde aparece a la derecha
                        labyrinth_training.gvars.strobe_value = 2;
                        #print "color verde, verde aparece a la derecha"
                        pass
                    if (labyrinth_training.gvars.get_color_experiment() == 1 and labyrinth_training.gvars.get_green_right() == 0):
                        #color verde, verde aparece a la izquierda
                        labyrinth_training.gvars.strobe_value = 3;
                        #print "color verde, verde aparece a la izquierda"
                        pass
                    if (labyrinth_training.gvars.get_color_experiment() == 0 and labyrinth_training.gvars.get_green_right() == 0):
                        #color rojo, rojo aparece a la derecha
                        labyrinth_training.gvars.strobe_value = 4;
                        #print "#color rojo, rojo aparece a la derecha"
                        pass
                    if (labyrinth_training.gvars.get_color_experiment() == 0 and labyrinth_training.gvars.get_green_right() == 1):
                        #color rojo, rojo aparece a la izquierda
                        labyrinth_training.gvars.strobe_value = 5;
                        #print "#color rojo, rojo aparece a la izquierda"
                        pass
                    
                    labyrinth_training.gvars.trialStarting = 0;
        if (labyrinth_training.gvars.trainingStarting_f == 1 and labyrinth_training.gvars.trainingStarting == 0):
                labyrinth_training.gvars.trainingStarting_f = 0
                labyrinth_training.gvars.strobe_value = labyrinth_training.gvars.get_num_puerta() + 2;
                print "first strobe with num: %d"%labyrinth_training.gvars.strobe_value
                pass
        milis = (pygame.time.get_ticks())
        labyrinth_training.log_to_file("%d,%f,%f,%f,%f,%d,%d" % (milis, labyrinth_training.gvars.wm.camera.x, labyrinth_training.gvars.wm.camera.y, labyrinth_training.gvars.wm.camera.dirx,
                                                       labyrinth_training.gvars.wm.camera.diry, labyrinth_training.gvars.strobe_value, labyrinth_training.gvars.win_value))
    
    @staticmethod
    def add_score():
        # log_to_file("Sujeto GANA.")
        labyrinth_training.gvars.set_player_score(labyrinth_training.gvars.get_player_score() + 10)
    
    @staticmethod
    def log_to_file(string_to_log=""):
        # if (labyrinth_training.gvars.get_log_to_file_counter() < 30):
            labyrinth_training.gvars.log_to_file_matrix.append(string_to_log + '\n')
            labyrinth_training.gvars.set_log_to_file_counter(labyrinth_training.gvars.get_log_to_file_counter() + 1)
    #     else:
    #         labyrinth_training.gvars.log_to_file_matrix.append(string_to_log+'\n')
    #         labyrinth_training.gvars.set_log_to_file_counter(labyrinth_training.gvars.get_log_to_file_counter()+1)
    #         for i in range(0,labyrinth_training.gvars.get_log_to_file_counter()):
    #             labyrinth_training.gvars.get_log_file().write(labyrinth_training.gvars.log_to_file_matrix[i]) # python will convert \n to os.linesep
    #         labyrinth_training.gvars.set_log_to_file_counter(0)
    #         labyrinth_training.gvars.log_to_file_matrix=[]
            pass
    
    @staticmethod
    def finalize_log():
        for i in range(0, labyrinth_training.gvars.get_log_to_file_counter()):
            labyrinth_training.gvars.get_log_file().write(labyrinth_training.gvars.log_to_file_matrix[i])  # python will convert \n to os.linesep
        labyrinth_training.gvars.get_log_file().close()
        print "Archivo de log cerrado."
    
    @staticmethod
    def load_image(image, darken, colorKey=None):
        ret = []
        if colorKey is not None:
            image.set_colorkey(colorKey)
        if darken:
            image.set_alpha(127)
        for i in range(image.get_width()):
            s = pygame.Surface((1, image.get_height())).convert()
            # s.fill((0,0,0))
            s.blit(image, (-i, 0))
            if colorKey is not None:
                s.set_colorkey(colorKey)
            ret.append(s)
        return ret
     
    

if __name__ == '__main__':
    a = labyrinth_training()
#     time.sleep(10)
#     while(True):
#         time.sleep(2)
#         a.vectorInstantaneo.y = 1
#         a.forceInstantVectorAnalysis()
        
