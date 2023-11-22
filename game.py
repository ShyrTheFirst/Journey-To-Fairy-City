import pygame, random, sys


#Inicializando o pygame
pygame.init()

#Criando janela do jogo
tela_Larg = 800
tela_Alt = 600

tela = pygame.display.set_mode((tela_Larg,tela_Alt))
pygame.display.set_caption('test')
frames = pygame.time.Clock()

#####Classes

class Player(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                self.imagesbaixo = [pygame.image.load(r'Graphics\Character\charbaixo1.png'),pygame.image.load(r'Graphics\Character\charbaixo2.png'),pygame.image.load(r'Graphics\Character\charbaixo3.png')]                               
                self.imagescima = [pygame.image.load(r'Graphics\Character\charcima1.png'),pygame.image.load(r'Graphics\Character\charcima2.png'),pygame.image.load(r'Graphics\Character\charcima3.png')]
                self.imagesesquerda = [pygame.image.load(r'Graphics\Character\charleft1.png'),pygame.image.load(r'Graphics\Character\charleft2.png')]
                self.imagesdireita = [pygame.image.load(r'Graphics\Character\charright1.png'),pygame.image.load(r'Graphics\Character\charright2.png')]
                self.image = self.imagesbaixo[0]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.dir = pygame.math.Vector2()
                self.speed = 100
                self.animation_timer = 0.0
                self.animation_index = 0
                self.direction = 'stand'
                

        def update(self,delta_time):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                        self.direction = 'up'
                        self.dir.y = -1
                        self.dir.x = 0
                        
                elif keys[pygame.K_DOWN]:
                        self.direction = 'down'
                        self.dir.y = 1
                        self.dir.x = 0
                        
                else:
                        self.dir.y = 0

                if keys[pygame.K_LEFT]:
                        self.direction = 'left'
                        self.dir.x = -1
                        self.dir.y = 0
                        
                elif keys[pygame.K_RIGHT]:
                        self.direction = 'right'
                        self.dir.x = 1
                        self.dir.y = 0
                        
                else:
                        self.dir.x = 0

                if self.dir.x == 0 and self.dir.y == 0:
                        self.direction = 'stand'

                

                if self.direction == 'up':
                        self.animation_timer += delta_time
                        if self.animation_timer >= 0.05:
                                self.animation_timer = 0.0
                                self.animation_index = (self.animation_index + 1) % len(self.imagescima)
                                self.image = self.imagescima[self.animation_index]
                                
                elif self.direction == 'down':
                        self.animation_timer += delta_time
                        if self.animation_timer >= 0.05:
                                self.animation_timer = 0.0
                                self.animation_index = (self.animation_index + 1) % len(self.imagesbaixo)
                                self.image = self.imagesbaixo[self.animation_index]
                                
                elif self.direction == 'left':
                        self.animation_timer += delta_time
                        if self.animation_timer >= 0.05:
                                self.animation_timer = 0.0
                                self.animation_index = (self.animation_index + 1) % len(self.imagesesquerda)
                                self.image = self.imagesesquerda[self.animation_index]
                                
                elif self.direction == 'right':
                        self.animation_timer += delta_time
                        if self.animation_timer >= 0.05:
                                self.animation_timer = 0.0
                                self.animation_index = (self.animation_index + 1) % len(self.imagesdireita)
                                self.image = self.imagesdireita[self.animation_index]
                elif self.direction == 'stand':
                        pass
                                

                self.rect.x += self.dir.x * self.speed * delta_time
                self.rect.y += self.dir.y * self.speed * delta_time

                
                

#inicia o jogo de fato
run_game = True
player_grupo = pygame.sprite.Group()
player1 = Player(10,10) 
player_grupo.add(player1)

while run_game:
        tela.fill((255,255,255))
        frames.tick(60)
        delta_time = frames.tick(60)/1000

        #padrão pro jogo rodar no while
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                sys.exit()
        player_grupo.draw(tela)
        player_grupo.update(delta_time)
        pygame.display.update()
