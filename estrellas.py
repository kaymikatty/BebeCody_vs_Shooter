import pygame
import os
from config import *

class Estrellas(pygame.sprite.Sprite):
    

    def __init__(self, pos_x, pos_y,speed,dir_images ):
        pygame.sprite.Sprite.__init__(self)
    
        #Cargar imagen de estrellita
        self.image = pygame.image.load(os.path.join(dir_images,'estrella.png'))

        self.rect = self.image.get_rect()
        
        #posiciones de las estrellitas
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed

        self.vel_x = self.speed

    #Hacer estrellas
    def update(self):
        self.rect.y += self.vel_x

    #Caer estrellas
    def down(self):
        self.rect.y += self.speed

    #Dibujar estrellas
    def draw(self,ventana):
        ventana.blit(self.image,self.rect)
        
    #Función de para
    def stop(self):
        self.vel_x = 0