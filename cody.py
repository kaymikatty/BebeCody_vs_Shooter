import pygame
from config import *
import os


class Cody (pygame.sprite.Sprite):

    def __init__(self, dir_images):
        pygame.sprite.Sprite.__init__(self)

        #Cargar imagenes de bebecody
        self.images =(
            pygame.image.load(os.path.join(dir_images,'cody.png')),
            pygame.image.load(os.path.join(dir_images,'cody_red.png'))
        )
        
        self.image = self.images[0]
        
        #forma
        self.rect = self.image.get_rect()
        
        #posicion
        self.rect.x = WIDTH // 2
        self.rect.y = 431
        self.key_pressed = pygame.key.get_pressed() 

        self.playing = True

    #Condición para mostrar a bebecody en red cuando es atrapado por una red
    def collide_with(self,sprites):
        objeto = pygame.sprite.spritecollide(self,sprites,False)
        if objeto:
            self.image = self.images[1]
            return objeto[0]
    
    def collide_with_estrella(self,sprites):
        objeto = pygame.sprite.spritecollide(self,sprites,False)
        if objeto:
            self.image = self.images[0]
            return objeto[0]

    #Presentar en pantalla a bebeCody
    def draw(self,ventana):
        ventana.blit(self.image,self.rect)
    
    #controles + edge detection
    def left(self):
        if self.rect.x > 0 and  self.playing:
            self.rect.x -= 7

    def right(self):
        if self.rect.x < 500 - 65 and  self.playing:
            self.rect.x += 7  
    
    #Función de parar
    def stop(self):
        self.playing = False