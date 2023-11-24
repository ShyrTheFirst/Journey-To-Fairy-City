import pygame, random, sys
import var as v


#Inicializando o pygame
pygame.init()

#Criando janela do jogo
tela_Larg = 800
tela_Alt = 600

#Definições da tela do jogo
tela = pygame.display.set_mode((tela_Larg,tela_Alt))
pygame.display.set_caption('Journey to the Fairy City')
frames = pygame.time.Clock() 





#####Classes

class Player(pygame.sprite.Sprite):
        def __init__(self,x,y):
                super().__init__()
                #movimentação do personagem
                self.imagesbaixo = [pygame.image.load(r'Graphics\Character\charbaixo1.png'),pygame.image.load(r'Graphics\Character\charbaixo2.png'),pygame.image.load(r'Graphics\Character\charbaixo3.png')]                               
                self.imagescima = [pygame.image.load(r'Graphics\Character\charcima1.png'),pygame.image.load(r'Graphics\Character\charcima2.png'),pygame.image.load(r'Graphics\Character\charcima3.png')]
                self.imagesesquerda = [pygame.image.load(r'Graphics\Character\charleft1.png'),pygame.image.load(r'Graphics\Character\charleft2.png'),pygame.image.load(r'Graphics\Character\charleft1.png')]
                self.imagesdireita = [pygame.image.load(r'Graphics\Character\charright1.png'),pygame.image.load(r'Graphics\Character\charright2.png'),pygame.image.load(r'Graphics\Character\charright1.png')]
                self.image = self.imagesbaixo[0]
                #Definições da imagem e pos do personagem
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.dir = pygame.math.Vector2() #vetor de direção
                self.speed = 100 #velocidade 
                self.animation_timer = 0.0 #timer de animação
                self.animation_index = 0 #index da animação atual
                self.direction = 'stand' #direção do personagem
                self.nivel = 1 #nivel do personagem

        def equipamento_atual(self,axe_baixo,axe_cima,axe_esquerda,axe_direita,helmet_baixo,helmet_cima,helmet_esquerda,helmet_direita,armor_baixo,armor_cima,armor_esquerda,armor_direita):
                #Definição dos equipamentos que estão sendo usados
                #adicionar machado
                self.axe_imagebaixo = axe_baixo
                self.axe_imagecima = axe_cima
                self.axe_imageesquerda = axe_esquerda
                self.axe_imagedireita = axe_direita                
                self.axe_image = self.axe_imagebaixo[0]
                #adicionar capacete
                self.helmet_imagebaixo = helmet_baixo
                self.helmet_imagecima = helmet_cima
                self.helmet_imageesquerda = helmet_esquerda
                self.helmet_imagedireita = helmet_direita
                self.helmet_image = self.helmet_imagebaixo[0]
                #adicionar peitoral
                self.armor_imagebaixo = armor_baixo
                self.armor_imagecima = armor_cima
                self.armor_imageesquerda = armor_esquerda
                self.armor_imagedireita = armor_direita
                self.armor_image = self.armor_imagebaixo[0]
                

        def equipado(self):
                if v.axe_equip == True:                        
                        #definir imagem do axe com a direção pra cima
                        if self.direction == 'up':
                                self.axe_image = self.axe_imagecima[self.animation_index]
                                self.helmet_image = self.helmet_imagecima[self.animation_index]
                                self.armor_image = self.armor_imagecima[self.animation_index]
                                
                        #definir imagem do axe com a direção pra baixo        
                        if self.direction == 'down':                                
                                self.axe_image = self.axe_imagebaixo[self.animation_index]
                                self.helmet_image = self.helmet_imagebaixo[self.animation_index]
                                self.armor_image = self.armor_imagebaixo[self.animation_index]
                                
                        #definir imagem do axe com a direção pra esquerda        
                        if self.direction == 'left':
                                self.axe_image = self.axe_imageesquerda[self.animation_index]
                                self.helmet_image = self.helmet_imageesquerda[self.animation_index]
                                self.armor_image = self.armor_imageesquerda[self.animation_index]
                                
                        #definir imagem do axe com a direção pra direita        
                        if self.direction == 'right':
                                self.axe_image = self.axe_imagedireita[self.animation_index]
                                self.helmet_image = self.helmet_imagedireita[self.animation_index]
                                self.armor_image = self.armor_imagedireita[self.animation_index]
                                
                        #definir imagem do axe com a direção parada       
                        if self.direction == 'stand':
                                pass
                        
                        #blitar a imagem do axe atual
                        tela.blit(self.axe_image,(self.rect.x,self.rect.y))
                        tela.blit(self.helmet_image,(self.rect.x,self.rect.y))
                        tela.blit(self.armor_image,(self.rect.x,self.rect.y))
                                
                else:
                        #não fazer nada se não estiver com o axe equipado
                        pass
                

        def update(self,delta_time):
                
                self.equipado()#'equipa' os itens
                
                keys = pygame.key.get_pressed()#verificar as teclas apertadas
                #Movimentar para CIMA
                if keys[pygame.K_UP]:
                        self.direction = 'up'
                        self.dir.y = -1
                        self.dir.x = 0
                        
                #Movimentar para BAIXO        
                elif keys[pygame.K_DOWN]:
                        self.direction = 'down'
                        self.dir.y = 1
                        self.dir.x = 0
                        
                else:
                        self.dir.y = 0 #Se não há movimento vertical, y=0
                        
                #Movimentar para ESQUERDA
                if keys[pygame.K_LEFT]:
                        self.direction = 'left'
                        self.dir.x = -1
                        self.dir.y = 0
                        
                #Movimentar para DIREITA        
                elif keys[pygame.K_RIGHT]:
                        self.direction = 'right'
                        self.dir.x = 1
                        self.dir.y = 0
                        
                else:
                        self.dir.x = 0 #Se não há movimento horizontal, x=0

                #Se não há movimento em nenhuma direção, definir como 'PARADO'
                if self.dir.x == 0 and self.dir.y == 0:
                        self.direction = 'stand'

                
                #Realizar animações conforme a direção
                #CIMA
                if self.direction == 'up':
                        self.animation_timer += delta_time #Definir timer da animação, conforme delta_time
                        if self.animation_timer >= 0.05: #Definir tempo para mudar animação
                                self.animation_timer = 0.0 #Zerar o timer para calcular a proxima mudança
                                self.animation_index = (self.animation_index + 1) % len(self.imagescima) #definir o index da animação para escolher o sprite
                                self.image = self.imagescima[self.animation_index] #Definir o sprite da animação atual

                #BAIXO                
                elif self.direction == 'down':
                        self.animation_timer += delta_time
                        if self.animation_timer >= 0.05:
                                self.animation_timer = 0.0
                                self.animation_index = (self.animation_index + 1) % len(self.imagesbaixo)
                                self.image = self.imagesbaixo[self.animation_index]

                #ESQUERDA                
                elif self.direction == 'left':
                        self.animation_timer += delta_time
                        if self.animation_timer >= 0.05:
                                self.animation_timer = 0.0
                                self.animation_index = (self.animation_index + 1) % len(self.imagesesquerda)
                                self.image = self.imagesesquerda[self.animation_index]

                #DIREITA                
                elif self.direction == 'right':
                        self.animation_timer += delta_time
                        if self.animation_timer >= 0.05:
                                self.animation_timer = 0.0
                                self.animation_index = (self.animation_index + 1) % len(self.imagesdireita)
                                self.image = self.imagesdireita[self.animation_index]

                #PARADO
                elif self.direction == 'stand':
                        pass
                                
                #aplicar a direção multiplicada pela velocidade e delta_time
                self.rect.x += self.dir.x * self.speed * delta_time 
                self.rect.y += self.dir.y * self.speed * delta_time

                
                

class Equipamentos():
        def __init__(self):
                self.axe_nv = 0
                self.helmet_nv = 0
                self.armor_nv = 0
                #Define os valores iniciais para a imagem do machado do personagem
                self.axe_imagebaixo = [pygame.image.load(r'Graphics\Character\Equips\Axe\axe_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_baixo3.png')]
                self.axe_imagecima = [pygame.image.load(r'Graphics\Character\Equips\Axe\axe_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_cima3.png')]
                self.axe_imageesquerda = [pygame.image.load(r'Graphics\Character\Equips\Axe\axe_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_left1.png')]
                self.axe_imagedireita = [pygame.image.load(r'Graphics\Character\Equips\Axe\axe_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\axe_right1.png')]

                #Define os valores iniciais para a imagem do elmo do personagem
                self.helmet_imagebaixo = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_baixo3.png')]
                self.helmet_imagecima = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_cima3.png')]
                self.helmet_imageesquerda = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_left1.png')]
                self.helmet_imagedireita = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_right1.png')]

                #Define os valores iniciais para a imagem do peito do personagem
                self.armor_imagebaixo = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_baixo3.png')]
                self.armor_imagecima = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_cima3.png')]
                self.armor_imageesquerda = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_left1.png')]
                self.armor_imagedireita = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_right1.png')]

        def definir_nivel(self):
                #Definir equipamentos de nv1
                if self.helmet_nv == 1:
                        self.helmet_imagebaixo = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_baixo1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_baixo2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_baixo3nv1.png')]
                        self.helmet_imagecima = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_cima1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_cima2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_cima3nv1.png')]
                        self.helmet_imageesquerda = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_left1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_left2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_left1nv1.png')]
                        self.helmet_imagedireita = [pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_right1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_right2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\helmet_right1nv1.png')]

     
                if self.armor_nv == 1:
                        self.armor_imagebaixo = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_baixo1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_baixo2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_baixo3nv1.png')]
                        self.armor_imagecima = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_cima1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_cima2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_cima3nv1.png')]
                        self.armor_imageesquerda = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_left1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_left2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_left1nv1.png')]
                        self.armor_imagedireita = [pygame.image.load(r'Graphics\Character\Equips\Armor\armor_right1nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_right2nv1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\armor_right1nv1.png')]

                
                #Definir equipamentos de nv5
                if self.axe_nv == 5:
                        pass
                '''
                        self.axe_imagebaixo =
                        self.axe_imagecima =
                        self.axe_imageesquerda =
                        self.axe_imagedireita =
                '''
                if self.helmet_nv == 5:
                        pass
                '''
                        self.helmet_imagebaixo =
                        self.helmet_imagecima =
                        self.helmet_imageesquerda =
                        self.helmet_imagedireita =
                        '''
                if self.armor_nv == 5:
                        pass
                '''
                        self.armor_imagebaixo =
                        self.armor_imagecima =
                        self.armor_imageesquerda =
                        self.armor_imagedireita =
                        '''
                        
        def mudar_axe(self,axe_baixo,axe_cima,axe_esquerda,axe_direita):
                self.axe_imagebaixo = axe_baixo
                self.axe_imagecima = axe_cima
                self.axe_imageesquerda = axe_esquerda
                self.axe_imagedireita = axe_direita

        def mudar_helmet(self,helmet_baixo,helmet_cima,helmet_esquerda,helmet_direita):
                self.helmet_imagebaixo = helmet_baixo
                self.helmet_imagecima = helmet_cima
                self.helmet_imageesquerda = helmet_esquerda
                self.helmet_imagedireita = helmet_direita

        def mudar_armor(self,armor_baixo,armor_cima,armor_esquerda,armor_direita):
                self.armor_imagebaixo = armor_baixo
                self.armor_imagecima = armor_cima
                self.armor_imageesquerda = armor_esquerda
                self.armor_imagedireita = armor_direita

        def definir_equipamentos(self,character):
                character.equipamento_atual(self.axe_imagebaixo,self.axe_imagecima,self.axe_imageesquerda,self.axe_imagedireita,self.helmet_imagebaixo,self.helmet_imagecima,self.helmet_imageesquerda,self.helmet_imagedireita,self.armor_imagebaixo,self.armor_imagecima,self.armor_imageesquerda,self.armor_imagedireita)
                

                
                

#inicia o jogo de fato
run_game = True

#Grupos de sprites
player_grupo = pygame.sprite.Group()
todos_sprites = pygame.sprite.Group()

#Inicializar a class player
player1 = Player(10,10)
player_grupo.add(player1)
todos_sprites.add(player1)

#Inicializar a class Equipamentos
equip = Equipamentos()

#Definir equipamento inicial (usar isso no craft para mudar os equipamentos)
equip.definir_nivel()
equip.definir_equipamentos(player1)

#Inicializar a class NPC
#Em andamento - receber class 'player1' e 'equip'

while run_game:
        tela.fill((255,255,255)) #provisório para cor da tela
        frames.tick(60)#Define frame rate
        delta_time = frames.tick(60)/1000 #Define o delta_time com base no frame rate

        #Função do botão de sair do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                sys.exit()
                
        #desenhar sprites
        todos_sprites.draw(tela)
        
        #atualizar classes de sprites
        todos_sprites.update(delta_time)

        #Atualiza tela
        pygame.display.update()
        
        v.axe_equip = True #provisório - irá definir se o personagem está equipado ao pegar o machado do chão!
