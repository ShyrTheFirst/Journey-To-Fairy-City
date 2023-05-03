import pygame
import random

#Inicializando o pygame
pygame.init()

#Criando janela do jogo
largura = 800 #width
altura = 600 #height
tela = pygame.display.set_mode((largura,altura))]
pygame.display.set_caption('Journey to the Fairy City')

# Define as cores utilizadas no jogo
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

#fontes pro HUD
font = pygame.font.SysFont(None, 30)

#variaveis e grupos de sprites
score = 0
attack_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, obstaculo):
            super().__init__()
            self.image = pygame.image.load(r'graphics/char.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = screen_width / 2
            self.rect.y = screen_height / 2
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
     

    def update(self, dx, dy):
            self.rect.x += dx
            self.rect.y += dy

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
