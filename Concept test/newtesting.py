import pygame
import random

#Inicializando o pygame
pygame.init()

#Criando janela do jogo
largura = 800 #width
altura = 600 #height
tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Journey to the Fairy City')
frames = pygame.time.Clock()

# Define as cores utilizadas no jogo
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

#define as imagens usadas no jogo
fundo = pygame.image.load(r'graphics/first_map.png')
arvore = pygame.image.load(r'graphics/arvore.png')

#fontes pro HUD
font = pygame.font.SysFont(None, 30)

#variaveis e grupos de sprites
score = 0
attack_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
arvore_grupo = pygame.sprite.Group()
monstro_grupo = pygame.sprite.Group()
char_grupo = pygame.sprite.Group()
todos_grupos = [arvore_grupo,monstro_grupo]

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, obstaculo):
            super().__init__()
            self.image = pygame.image.load(r'graphics/char.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = screen_width / 2
            self.rect.y = screen_height / 2
            self.old_rect = self.rect.copy()
            self.health = 50
            self.direction = 'right'
            self.speed = 2
            self.obstaculo = obstaculo #Pra detectar colisão com as arvores

    def collision(self,direction):
            collision_sprites = pygame.sprite.spritecollide(self,self.obstaculo,False)
            if collision_sprites:
                if direction == 'horizontal':
                    for sprite in collision_sprites:
                        # collision on the right
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            v.right = True
                            self.rect.right = sprite.rect.left
                            self.pos.x = self.rect.x
                        else:
                            v.right = False

                        # collision on the left
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            v.left = True
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.x
                        else:
                            v.left = False

                if direction == 'vertical':
                    for sprite in collision_sprites:
                        # collision on the bottom
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            v.bottom = True
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y
                        else:
                            v.bottom = False

                        # collision on the top
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            v.top = True
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.y
                        else:
                            v.top = False
     

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

    def update(self, dx, dy):
            self.pos.x += self.direction.x * self.speed
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.pos.y += self.direction.y * self.speed
            self.rect.y = round(self.pos.y)
            self.collision('vertical')

        # Mantém o jogador dentro da tela
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > screen_width - 50:
                self.rect.x = screen_width - 50
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > screen_height - 50:
                self.rect.y = screen_height - 50

    def attack(self):               
            ax = self.rect.x +25
            ay = self.rect.y +25
            adir = self.direction
            attack = Attack(ax,ay,adir)
            attack_group.add(attack)
            all_sprites.add(attack_group)

    def morreu(self):
            if self.hp <= 0:
                self.rect = self.old_rect
                self.image = pygame.image.load(r'graphics/charmorto.png').convert_alpha()
                end_game = pygame.image.load(r'graphics/endgame.png')
                tela.blit(end_game,(0,0))
                continue_game = pygame.image.load(r'graphics/continue.png')
                tela.blit(continue_game,(220,300))
                sim_bot = pygame.image.load(r'graphics/YES.png')
                nao_bot = pygame.image.load(r'graphics/NO.png')
                tela.blit(sim_bot,(350,350))
                tela.blit(nao_bot,(450,350))
                clicou_sim = pygame.Rect(350,350,50,50)
                clicou_nao = pygame.Rect(450,350,50,50)
                if pygame.mouse.get_pressed() == (1,0,0):
                    mouseposition = pygame.mouse.get_pos()
                    if clicou_sim.collidepoint(mouseposition):
                        tela.fill((0,0,0))
                        pygame.display.update()
                        v.game = False
                        v.menu = True
                        v.run_game = False
                        v.machadinho = True
                        v.equipamento = False
                        import main
                    if clicou_nao.collidepoint(mouseposition):
                        pygame.quit()
                        sys.exit()

class Arvore(pygame.sprite.Sprite):
        def __init__(self,pos):
            super().__init__()
            self.image = pygame.image.load(r'graphics/arvore.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()


#dentro do while:
            '''
char = Personagem(350,200,arvore_grupo)
char_grupo.add(char)
machadinho_no_chao = pygame.image.load(r'graphics/machado.png')
machado_rect = machadinho_no_chao.get_rect(topleft=(350,300))


####COLOCAR AS ARVORES DAQUI E CONTINUAR DAI!!!!!! DPS ADICIONAR MAIS INFOS DO CODIGO DO CHATGPT####
