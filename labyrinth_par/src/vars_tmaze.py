# -*- coding: utf-8 -*-
import pygame
#Vars TMaze class: variables used in the TMaze and Hexagon program.
class vars_tmaze:
    worldMap=[]
    sprite_positions=[]
    log_to_file_matrix=[]
    
    
    def __init__(self):
        self.__anim_count = 0 #variable que indica el fotograma de la animación de fin de experimento.
        self.__door_anim = 0 #variable para animación de puerta abriéndose.
        self.__init_whitebox = 0
        self.__num_puerta = 0
        self.__posx_to_set = 0
        self.__posy_to_set = 0
        self.__log_to_file_counter = 0
        self.__delay_reboot_button = 0 #para que no rebote la pulsación del botón de reinicio.
        self.__player_score = 0 #puntuación del sujeto
        self.__log_file = "" #nombre del sujeto a logear en archivo.
        self.__color_experiment = 0 #0 = seguir rojo, 1= seguir verde
        self.__green_right = 0 #0 = rojo a la derecha, verde izquierda; 1= verde derecha, rojo izquierda
        self.__light_sample = False #Luz de sample encendida o no.
        self.__lights_on = False #si True, se encendieron luces de Comparisson.
        self.__experiment_ended = False #si True, finalizó esta experiencia (sujeto ganó o perdió)
        self.__user_won = False #True = ganó.
        
    ##Getters
    #def get_length(self):
    #    return self.__length
    def set_anim_count(self, nuevo):
        self.__anim_count = nuevo
    def get_anim_count(self):
        return self.__anim_count
    def get_door_anim(self):
        return self.__door_anim
    def set_door_anim(self, nuevo):
        self.__door_anim = nuevo
    def get_init_whitebox(self):
        return self.__init_whitebox
    def set_init_whitebox(self, nuevo):
        self.__init_whitebox = nuevo
    def get_num_puerta(self):
        return self.__num_puerta
    def set_num_puerta(self, nuevo):
        self.__num_puerta = nuevo
    def get_posx_to_set(self):
        return self.__posx_to_set
    def set_posx_to_set(self, nuevo):
        self.__posx_to_set = nuevo
    def get_posy_to_set(self):
        return self.__posy_to_set
    def set_posy_to_set(self, nuevo):
        self.__posy_to_set = nuevo
    def get_log_to_file_counter(self):
        return self.__log_to_file_counter
    def set_log_to_file_counter(self, nuevo):
        self.__log_to_file_counter = nuevo
    def get_delay_reboot_button(self):
        return self.__delay_reboot_button
    def set_delay_reboot_button(self, nuevo):
        self.__delay_reboot_button = nuevo
    def get_player_score(self):
        return self.__player_score
    def set_player_score(self, nuevo):
        self.__player_score = nuevo
    def get_log_file(self):
        return self.__log_file
    def set_log_file(self, nuevo):
        self.__log_file = nuevo
    def get_color_experiment(self):
        return self.__color_experiment
    def set_color_experiment(self, nuevo):
        self.__color_experiment = nuevo
    def get_green_right(self):
        return self.__green_right
    def set_green_right(self, nuevo):
        self.__green_right = nuevo
    def get_light_sample(self):
        return self.__light_sample
    def set_light_sample(self, nuevo):
        self.__light_sample = nuevo
    def get_lights_on(self):
        return self.__lights_on
    def set_lights_on(self, nuevo):
        self.__lights_on = nuevo
    def get_experiment_ended(self):
        return self.__experiment_ended
    def set_experiment_ended(self, nuevo):
        self.__experiment_ended = nuevo
    def get_user_won(self):
        return self.__user_won
    def set_user_won(self, nuevo):
        self.__user_won = nuevo


class Weapon(object):
    FPS = 60
    
    def __init__(self, weaponName="shotgun", frameCount = 5):
        self.images = []
        self.loop = False
        self.playing = False
        self.frame = 0
        self.oldTime = 0
        for i in range(frameCount):
            img = pygame.image.load("pics/weapons/%s%s.bmp" % (weaponName, i+1)).convert()
            img = pygame.transform.scale2x(img)
            img = pygame.transform.scale2x(img)
            img.set_colorkey(img.get_at((0,0)))
            self.images.append(img)
    def play(self):
        self.playing = True
        self.loop = True
    def stop(self):
        self.playing = False
        self.loop = False
    def draw(self, surface, time):
#         if(self.playing or self.frame > 0):
#             if(time > self.oldTime + 1./FPS):
#                 self.frame = (self.frame+1) % len(self.images)
#                 if self.frame == 0: 
#                     if self.loop:
#                         self.frame = 1
#                     else:
#                         self.playing = False
#                         
#                 self.oldTime = time
        img = self.images[self.frame]
        surface.blit(img, (surface.get_width()/2 - img.get_width()/2, surface.get_height()-img.get_height()))






def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)



