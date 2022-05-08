import sys
import pygame
import random #random
import os   #para sonidos

from config import *
from cody import Cody
from redes import Redes
from estrellas import Estrellas
from pathlib import Path

#Controlar fotogramas
clock = pygame.time.Clock()

#CArgar archivo .txt
current_path = Path.cwd()
file_path = current_path / 'puntaje_alto.txt'

#Clase Principal
class Main: 
    def __init__(self):
        pygame.init()
        
        self.ventana = pygame.display.set_mode( (WIDTH,HEIGHT) )
        
        #Titulo del juego
        pygame.display.set_caption(TITLE)

        #Icono del juego
        dir_images = os.path.join('recursos/img')
        icono = pygame.image.load(os.path.join(dir_images, 'escenario.png'))
        pygame.display.set_icon(icono)

        #Cargar ruta de las imagenes del juego
        self.dir_images = os.path.join('recursos/img')

        #Obtener fuente
        self.font = pygame.font.match_font(FONT)

        self.dir = os.path.dirname(__file__)
        self.dir_sounds = os.path.join(self.dir, 'recursos/music')

        #Atributo que permite ver si la aplicación se esta ejecutando o no
        self.running = True 

        #Creacion de variable de puntaje alto
        try:
    
            self.puntaje_alto = int(self.get_high_score())
    
        except:
            self.puntaje_alto = 0

        
    def start(self): #inicia videojuego
        self.menu()
        self.new()
        
    def new(self): #Iniciar un nuevo juego
        self.score = 0
        self.nivel = 0
        self.playing = True
        self.fondo = pygame.image.load(os.path.join(self.dir_images, 'escenario.png'))
        self.generate_elements()
        self.run()
        

    def generate_elements(self):
    
        self.cody_bebe = Cody(self.dir_images)
        
        self.sprites = pygame.sprite.Group()
        self.redes = pygame.sprite.Group()
        self.estrellas = pygame.sprite.Group()
        
        self.sprites.add (self.cody_bebe)

        self.generate_redes()
        self.generate_estrellas()
        
    def generate_redes(self):

        if  len(self.redes) == 0:

            for i in range(0, MAX_REDES):
                pos_x = random.randrange(10, 400 )  #edge detection de las redes
                pos_y = random.randrange (-500,-100)
                speed = random.randrange(1,SPEED)   #velocidad de las redes en cada level
                red = Redes(pos_x,pos_y,speed,self.dir_images)
                self.sprites.add(red)
                self.redes.add(red)
                
                sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'nivel.wav'))
                sound.play()
                
            self.nivel +=1
    
    def generate_estrellas(self):

        if  len(self.estrellas) == 0:

            for s in range(0, MAX_ESTRELLAS):
                pos_x = random.randrange(10, 400 )  #edge detection de las redes
                pos_y = random.randrange (-500,-100)
                speed = random.randrange(1,SPEED)   #velocidad de las redes en cada level
                estrella = Estrellas(pos_x,pos_y,speed,self.dir_images)
                self.sprites.add(estrella)
                self.estrellas.add(estrella)

    def run(self): #Ejecutar videojuego
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.get_high_score() #Para que inicie el puntaje alto 
    
    def events(self): #Llamar eventos que puedan aparecer

        #Cerrar pantalla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   
                sys.exit()
        
        key_pressed = pygame.key.get_pressed()   

        if key_pressed[pygame.K_LEFT]:
            self.cody_bebe.left()  

        if key_pressed[pygame.K_RIGHT]:
            self.cody_bebe.right()

        if key_pressed[pygame.K_c] and not self.playing:
            self.new()

    def draw(self): #Dibujar diferentes elementos del videojuego
        self.ventana.blit(self.fondo,(0,0))
    
        self.sprites.draw(self.ventana)
        self.redes.draw(self.ventana)
                
        self.draw_text()
        pygame.display.flip()

    def update(self): #Actualizar pantalla
        if not self.playing:
            return
            
        red = self.cody_bebe.collide_with(self.redes)
        if red:
            self.stop()
            sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'game_over.wav'))
            sound.play()

        estrella = self.cody_bebe.collide_with_estrella(self.estrellas)
        if estrella:
            self.score +=5
            estrella.kill()
            sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'estrella.wav'))
            sound.play()

        #condición para sobreescribir puntaje alto
        if (self.puntaje_alto < self.score):
                self.puntaje_alto = self.score 

        with open(file_path, 'w') as file:
            file.write(str(self.puntaje_alto))
        
        self.display_text ('Puntaje Alto: '+ str(self.puntaje_alto),22,WHITE,76,38)

        self.sprites.update()
        self.redes.update()
        self.update_elements(self.redes)
        self.update_elements_estrella(self.estrellas)
        self.generate_redes()
        self.generate_estrellas()
        self.get_high_score() #Actualizar puntaje alto

    def update_elements(self,red):
        for redes in red:
            if redes.rect.y > HEIGHT:
                redes.kill()

                self.score +=1    

        for redes in red:
            redes.down()

    def update_elements_estrella(self,estrella):
        for estrellas in estrella:
            if estrellas.rect.y > HEIGHT:
                estrellas.kill()             

        for estrellas in estrella:
            estrellas.down()
            
            
    def stop(self): #Método que detendra videojuego
        self.cody_bebe.stop()
        self.stop_elements(self.redes)

        self.playing = False
    
    def stop_elements(self,elements):
        for element in elements:
            element.stop()

    def score_format(self):
        return 'Puntaje: {}'.format(self.score)

    def level_format(self):
        return 'Nivel: {}'.format(self.nivel)

    def puntaje_alto_format(self):
        return 'Puntaje Alto: {}'.format(self.puntaje_alto)
    

    def draw_text(self): #Presentar texto de nivel y score
       self.display_text(self.score_format(),26,BLACK, WIDTH // 1.9,20)
       self.display_text(self.level_format(),26,BLACK, WIDTH // 1.1,20 )
       self.display_text(self.puntaje_alto_format(),26, MORADO,WIDTH // 6,20) 

        #Condición para presentar mensaje de perdiste o superaste el puntaje alto dependiendo de la puntuación
       if not self.playing:  
            if self.puntaje_alto <= self.score:
               self.display_text('¡¡¡ Felicidades !!!',56,MORADO,WIDTH // 2,200) 
               self.display_text('Superaste Puntaje',36,BLACK,WIDTH // 2,280)
               self.display_text(self.puntaje_alto_format(),36, BLACK,WIDTH // 2, 350)
               self.display_text('Presiona C para comenzar de nuevo',26,BLACK, WIDTH // 2, 450)
            else:
                self.display_text('Perdiste',46,BLACK, WIDTH // 2, HEIGHT//2 )
                self.display_text('Presiona C para comenzar de nuevo',26,BLACK, WIDTH // 2, 300)
        
    def display_text(self, text, size,color,pos_x,pos_y): #Método para crear fuente
        fuente = pygame.font.Font(self.font, size)

        text = fuente.render(text,True,color)
        rect = text.get_rect()
        rect.midtop = (pos_x,pos_y)

        self.ventana.blit(text,rect)

    def menu(self): # Método de menu
        self.portada = pygame.image.load(os.path.join(self.dir_images,'portada.png'))
        self.ventana.blit(self.portada,(0,0))

        #Presentar en pantalla el Puntaje alto
        self.puntaje_alto_format()
        self.display_text(self.puntaje_alto_format() ,26,MORADO, WIDTH//2,445)
        self.display_text('Presiona una tecla para comenzar',26,BLACK, WIDTH//2,410)

        pygame.display.flip()
        self.wait()

    def wait(self): #Para que el menu no se cierre automaticamente
        wait = True
        while wait:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYUP:
                wait = False

    #Leer el archivo .txt 
    def get_high_score(self):
        with open(file_path, 'r') as file:
            return file.read()
