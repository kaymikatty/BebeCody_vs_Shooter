import pygame
import os
from config import *

class Redes(pygame.sprite.Sprite):
    

    def __init__(self, pos_x, pos_y,speed,dir_images ):
        pygame.sprite.Sprite.__init__(self)
    
        #Cargarimagen de redes
        self.image = pygame.image.load(os.path.join(dir_images,'red.png'))

        self.rect = self.image.get_rect()
        
        #posiciones de las redes  
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed

        self.vel_x = self.speed
        
    #Hacer redes
    def update(self):
        self.rect.y += self.vel_x

    #Caer redes
    def down(self):
        self.rect.y += self.speed

    #Dibujar redes 
    def draw(self,ventana):
        ventana.blit(self.image,self.rect)
    
    #Función de parar
    def stop(self):
        self.vel_x = 0

    
