import pygame, sys, random


#Iniciar o pygame###########
pygame.init()
tela = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Shyr's Adventure")
frames = pygame.time.Clock()
############################

#Cores######################
verde_escuro = (51,102,0)
verde_claro = (128,255,0)
azul_celeste = (102,178,255)
azul_tempestade = (0,76,153)
amarelo_deserto = (255,255,102)
amarelo_pantano = (153,153,0)
verde_arvore = (25,51,0)
cinza_pedra = (64,64,64)
cinza_tempestade = (128,128,128)

fundo = pygame.image.load(r'graphics/first_map.png')
arvore = pygame.image.load(r'graphics/arvore.png')
############################


equipamento = False
#Classes####################
class Personagem(pygame.sprite.Sprite):
    def __init__(self,charx,chary):
        super().__init__()
        self.image = pygame.image.load('graphics/char.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = charx
        self.rect.y = chary
        self.direction = pygame.math.Vector2() #preciso aprender sobre isso :v
        self.speed = 3 #a velocidade do movimento

    def entrada(self): #Verifica as teclas pressionadas para dar comandos
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:            
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

            
        
    def update(self): #tem que chamar update por conta do sprite.Group
        self.entrada()
        self.rect.center += self.direction * self.speed

    def cortar(self,grupo):
        if pygame.sprite.spritecollide(self, grupo, True):
            print("monstrinho buh")
            #return True

    def colidir(self,direcao):
        pass

    def equipamento(self):
        if equipamento == True:
            self.image = pygame.image.load('graphics/charequipado.png').convert_alpha()
            print("equipou")

    

class Arvore(pygame.sprite.Sprite):
    def __init__(self,posx,posy):
        super().__init__()
        self.image = pygame.image.load(r'graphics/arvore.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [posx,posy]
        self.direction = pygame.math.Vector2()
        
'''
PRECISO DEFINIR AQUI OS MONSTROS SURGINDO ALEATORIAMENTE DEPOIS DE CORTAR UMA ARVORE
ESCOLHER IMAGEM ALEATORIA DO MONSTRO
DEFINIR DANO E FREQUENCIA DO ATAQUE
MOVER 25px PRA FRENTE E VOLTAR PRA SINALIZAR DANO?
MESMO PRO PERSONAGEM QUANDO CORTA E ATAQUE

class Monstro(pygame.sprite.Sprite):
    def __init__(self,posx,posy):
        super().__init__()
        self.image = pygame.image.load('graphics/monstro.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [posx,posy]
'''
        

############################

#Criando o Sprite.group######
arvore_grupo = pygame.sprite.Group()
monstro_grupo = pygame.sprite.Group()
char_grupo = pygame.sprite.Group()
############################

#Criando os itens###########
char = Personagem(350,200)
char_grupo.add(char)

arvore1 = Arvore(0,0)
arvore_grupo.add(arvore1)
############################
#game loop##################
pygame.display.update()

run_game = True
while run_game:
    
####descobrindo a posicao para as arvores####
    #fileira 1#
    tela.blit(fundo,(0,0))
    tela.blit(arvore,(50,0))
    tela.blit(arvore,(100,0))
    tela.blit(arvore,(150,0))
    tela.blit(arvore,(200,0))
    tela.blit(arvore,(250,0))
    tela.blit(arvore,(300,0))
    tela.blit(arvore,(350,0))
    tela.blit(arvore,(400,0))
    tela.blit(arvore,(450,0))
    tela.blit(arvore,(500,0))
    tela.blit(arvore,(550,0))
    tela.blit(arvore,(600,0))
    tela.blit(arvore,(650,0))
    tela.blit(arvore,(700,0))
    tela.blit(arvore,(750,0))
    
    #coluna 1#
    tela.blit(arvore,(0,50))
    tela.blit(arvore,(0,100))
    tela.blit(arvore,(0,150))
    tela.blit(arvore,(0,200))
    tela.blit(arvore,(0,250))
    tela.blit(arvore,(0,300))
    tela.blit(arvore,(0,350))
    tela.blit(arvore,(0,400))
    tela.blit(arvore,(0,450))
    tela.blit(arvore,(0,500))
    tela.blit(arvore,(0,550))

    tela.blit(arvore,(50,50))
    tela.blit(arvore,(100,50))
    tela.blit(arvore,(150,50))
    tela.blit(arvore,(200,50))
    tela.blit(arvore,(250,50))
    tela.blit(arvore,(300,50))
    tela.blit(arvore,(350,50))
    tela.blit(arvore,(400,50))
    tela.blit(arvore,(450,50))
    tela.blit(arvore,(500,50))
    tela.blit(arvore,(550,50))
    tela.blit(arvore,(600,50))
    tela.blit(arvore,(650,50))
    tela.blit(arvore,(700,50))
    tela.blit(arvore,(750,50))

    tela.blit(arvore,(50,100))
    tela.blit(arvore,(100,100))
    tela.blit(arvore,(150,100))
    tela.blit(arvore,(200,100))
    tela.blit(arvore,(250,100))
    tela.blit(arvore,(300,100))
    tela.blit(arvore,(350,100))
    tela.blit(arvore,(400,100))
    tela.blit(arvore,(450,100))
    tela.blit(arvore,(500,100))
    tela.blit(arvore,(550,100))
    tela.blit(arvore,(600,100))
    tela.blit(arvore,(650,100))
    tela.blit(arvore,(700,100))
    tela.blit(arvore,(750,100))
    

    tela.blit(arvore,(50,150))    
    tela.blit(arvore,(100,150))
    tela.blit(arvore,(150,150))
    tela.blit(arvore,(200,150))
    tela.blit(arvore,(250,150))
    tela.blit(arvore,(300,150))
    tela.blit(arvore,(350,150))
    tela.blit(arvore,(400,150))
    tela.blit(arvore,(450,150))
    tela.blit(arvore,(500,150))
    tela.blit(arvore,(550,150))
    tela.blit(arvore,(600,150))
    tela.blit(arvore,(650,150))
    tela.blit(arvore,(700,150))
    tela.blit(arvore,(750,150))
    
###########proximo da fogueira#########
    #antes da fogueira#
    tela.blit(arvore,(50,200))
    tela.blit(arvore,(100,200))
    tela.blit(arvore,(150,200))
    tela.blit(arvore,(200,200))
    tela.blit(arvore,(250,200))
    #passou a fogueira#
    tela.blit(arvore,(550,200))
    tela.blit(arvore,(600,200))
    tela.blit(arvore,(650,200))
    tela.blit(arvore,(700,200))
    tela.blit(arvore,(750,200))

    #antes da fogueira#
    tela.blit(arvore,(50,250))
    tela.blit(arvore,(100,250))
    tela.blit(arvore,(150,250))
    tela.blit(arvore,(200,250))
    tela.blit(arvore,(250,250))
    #passou a fogueira#
    tela.blit(arvore,(550,250))
    tela.blit(arvore,(600,250))
    tela.blit(arvore,(650,250))
    tela.blit(arvore,(700,250))
    tela.blit(arvore,(750,250))
    
    #antes da fogueira#
    tela.blit(arvore,(50,300))
    tela.blit(arvore,(100,300))
    tela.blit(arvore,(150,300))
    tela.blit(arvore,(200,300))
    tela.blit(arvore,(250,300))
    #passou a fogueira#
    tela.blit(arvore,(550,300))
    tela.blit(arvore,(600,300))
    tela.blit(arvore,(650,300))
    tela.blit(arvore,(700,300))
    tela.blit(arvore,(750,300))

    #antes da fogueira#
    tela.blit(arvore,(50,350))
    tela.blit(arvore,(100,350))
    tela.blit(arvore,(150,350))
    tela.blit(arvore,(200,350))
    tela.blit(arvore,(250,350))
    #passou a fogueira#
    tela.blit(arvore,(550,350))
    tela.blit(arvore,(600,350))
    tela.blit(arvore,(650,350))
    tela.blit(arvore,(700,350))
    tela.blit(arvore,(750,350))

######################################

    tela.blit(arvore,(50,400))   
    tela.blit(arvore,(100,400))
    tela.blit(arvore,(150,400))
    tela.blit(arvore,(200,400))
    tela.blit(arvore,(250,400))
    tela.blit(arvore,(300,400))
    tela.blit(arvore,(350,400))
    tela.blit(arvore,(400,400))
    tela.blit(arvore,(450,400))
    tela.blit(arvore,(500,400))
    tela.blit(arvore,(550,400))
    tela.blit(arvore,(600,400))
    tela.blit(arvore,(650,400))
    tela.blit(arvore,(700,400))
    tela.blit(arvore,(750,400))

    tela.blit(arvore,(50,450))   
    tela.blit(arvore,(100,450))
    tela.blit(arvore,(150,450))
    tela.blit(arvore,(200,450))
    tela.blit(arvore,(250,450))
    tela.blit(arvore,(300,450))
    tela.blit(arvore,(350,450))
    tela.blit(arvore,(400,450))
    tela.blit(arvore,(450,450))
    tela.blit(arvore,(500,450))
    tela.blit(arvore,(550,450))
    tela.blit(arvore,(600,450))
    tela.blit(arvore,(650,450))
    tela.blit(arvore,(700,450))
    tela.blit(arvore,(750,450))

    tela.blit(arvore,(50,500))   
    tela.blit(arvore,(100,500))
    tela.blit(arvore,(150,500))
    tela.blit(arvore,(200,500))
    tela.blit(arvore,(250,500))
    tela.blit(arvore,(300,500))
    tela.blit(arvore,(350,500))
    tela.blit(arvore,(400,500))
    tela.blit(arvore,(450,500))
    tela.blit(arvore,(500,500))
    tela.blit(arvore,(550,500))
    tela.blit(arvore,(600,500))
    tela.blit(arvore,(650,500))
    tela.blit(arvore,(700,500))
    tela.blit(arvore,(750,500))

    tela.blit(arvore,(50,550))   
    tela.blit(arvore,(100,550))
    tela.blit(arvore,(150,550))
    tela.blit(arvore,(200,550))
    tela.blit(arvore,(250,550))
    tela.blit(arvore,(300,550))
    tela.blit(arvore,(350,550))
    tela.blit(arvore,(400,550))
    tela.blit(arvore,(450,550))
    tela.blit(arvore,(500,550))
    tela.blit(arvore,(550,550))
    tela.blit(arvore,(600,550))
    tela.blit(arvore,(650,550))
    tela.blit(arvore,(700,550))
    tela.blit(arvore,(750,550))
    
##################################################  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            char_grupo.clear(tela,fundo)
            run_game = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                char.cortar(arvore_grupo)
                char.rect.y += 5
                if char.cortar(arvore_grupo) == True:
                    pass
                equipamento = True
                char.equipamento()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                char.rect.y -= 5
        
    
   

    
    
    char_grupo.draw(tela)
    arvore_grupo.draw(tela)
    char_grupo.update()
    
    pygame.display.update()


    frames.tick(60)
############################
