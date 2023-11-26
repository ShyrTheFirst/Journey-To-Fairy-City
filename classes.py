import pygame, sys, math
import var as v

class Damage_Show:    
    def infos(self,x,y,damage,color):
        self.float_text = []
        self.x = x
        self.y = y
        self.damage = damage
        self.color = color
        self.timer = 0.0
        self.alphinha = 255

    def create_text(self,font):
        text = font.render(str(self.damage),True,self.color)
        text_rect = text.get_rect()
        text_rect.center = (self.x,self.y)

        self.float_text.append((text,text_rect))

    def draw(self, delta_time,tela):
        self.timer += delta_time
        for i, (text,rect) in enumerate(self.float_text):
            data = (text,rect)
            if self.timer <= 1.0:                
                    text.set_alpha(self.alphinha)
                    tela.blit(text,rect)
                    rect.y -= 1
                    self.alphinha -= 10
                    self.float_text[i] = (text, rect)
                    self.timer = 0.0
            else:                
                self.float_text.remove(data)


class Player(pygame.sprite.Sprite):
        def __init__(self,x,y,tela):
                super().__init__()
                
                #movimentação do personagem
                self.images = {
                'down':[pygame.image.load(r'Graphics\Character\charbaixo1.png'),pygame.image.load(r'Graphics\Character\charbaixo2.png'),pygame.image.load(r'Graphics\Character\charbaixo3.png')],                            
                'up':[pygame.image.load(r'Graphics\Character\charcima1.png'),pygame.image.load(r'Graphics\Character\charcima2.png'),pygame.image.load(r'Graphics\Character\charcima3.png')],
                'left':[pygame.image.load(r'Graphics\Character\charleft1.png'),pygame.image.load(r'Graphics\Character\charleft2.png'),pygame.image.load(r'Graphics\Character\charleft1.png')],
                'right':[pygame.image.load(r'Graphics\Character\charright1.png'),pygame.image.load(r'Graphics\Character\charright2.png'),pygame.image.load(r'Graphics\Character\charright1.png')],
                'ataque':{'down':pygame.image.load(r'Graphics\Character\charbaixo_ataque.png'),'up':pygame.image.load(r'Graphics\Character\charcima_ataque.png'),'left':pygame.image.load(r'Graphics\Character\charleft_ataque.png'),'right':pygame.image.load(r'Graphics\Character\charright_ataque.png')}
                }
                self.image = self.images['down'][0]
                
                #Definições da imagem e pos do personagem
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.old_rect = self.rect.copy()
                self.dir = pygame.math.Vector2() #vetor de direção
                self.speed = 100 #velocidade
                
                #definições das animações e movimentos
                self.animation_timer = 0.0 #timer de animação
                self.animation_index = 0 #index da animação atual
                self.direction = 'stand' #direção do personagem
                self.last_direction = 'stand' #registra a ultima direção do personagem
                self.atacando = False #Define se o personagem está realizando um ataque
                self.ataque_dir = 'down' #Define o lado de ataque do personagem
                self.key_down = False
                
                #Definições de atributos
                self.nivel = 1 #nivel do personagem
                self.health = 50 #define a vida do personagem
                self.max_health = 50 #define o limite de vida do personagem
                
                #definição da tela
                self.tela = tela

        def inventario(self): #À ser implementado
                pass

        def mostrar_vida(self, tela):
                
            frac_hp = int((50*self.health)/self.max_health)
            pygame.draw.rect(tela, (255,0,0), (10, 50, frac_hp*5, 15)) #ALTERAR ISSO CONFORME A IMAGEM DO HUD

        def colisao(self,obstaculo,damage_show,font,delta_time,tela):
            
                colisao_sprites = pygame.sprite.spritecollide(self,obstaculo,False)
                if colisao_sprites:
                        for sprite in colisao_sprites:
                                if sprite.type == 'monstro':
                                        self.health -= sprite.dano #gerar dano no personagem conforme o dano do inimigo
                                        
                                        #criar animação do dano
                                        damage_show.infos(self.rect.x+40, self.rect.y, sprite.dano,(255,0,0))
                                        damage_show.create_text(font)
                                        damage_show.draw(delta_time, tela)                                        
                                        
                                # colisão na direita
                                if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                                        self.rect.right = sprite.rect.left
                                        self.dir.x = self.rect.x
                                        if sprite.type == 'monstro':
                                                sprite.rect.x += 7
                                                
                                # colisão na esquerda
                                if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                                        self.rect.left = sprite.rect.right
                                        self.dir.x = self.rect.x
                                        if sprite.type == 'monstro':
                                                sprite.rect.x -= 7

                                # colisão em baixo
                                if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                                        self.rect.bottom = sprite.rect.top
                                        self.dir.y = self.rect.y
                                        if sprite.type == 'monstro':
                                                sprite.rect.y += 7
                                                
                                # colisão em cima
                                if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                                        self.rect.top = sprite.rect.bottom
                                        self.dir.y = self.rect.y
                                        if sprite.type == 'monstro':
                                                sprite.rect.y -= 7

        def equipamento_atual(self,axe_images,helmet_images,armor_images):
                #Definição dos equipamentos que estão sendo usados
                
                #adicionar machado
                self.axe_images = axe_images    
                self.axe_image = self.axe_images['down'][0]
                
                #adicionar capacete
                self.helmet_images = helmet_images
                self.helmet_image = self.helmet_images['down'][0]
                
                #adicionar peitoral
                self.armor_images = armor_images  
                self.armor_image = self.armor_images['down'][0]
                

        def equipado(self):
                if v.axe_equip == True:
                        #definir imagem do axe, helmet e armor com a direção parada       
                        if self.direction == 'stand':
                                pass
                        
                        if not self.direction == 'stand':
                                #definir imagem do axe, helmet e armor conforme a direction
                                self.axe_image = self.axe_images[self.direction][self.animation_index]
                                self.helmet_image = self.helmet_images[self.direction][self.animation_index]
                                self.armor_image = self.armor_images[self.direction][self.animation_index]                               
                        
                        #blitar a imagem do axe atual
                        self.tela.blit(self.helmet_image,(self.rect.x,self.rect.y))
                        self.tela.blit(self.armor_image,(self.rect.x,self.rect.y))
                        self.tela.blit(self.axe_image,(self.rect.x,self.rect.y))
                                
                else:
                        #não fazer nada se não estiver com o axe equipado
                        pass
                  
        def update(self,delta_time, tela):
                
                self.equipado()#'equipa' os itens

                self.mostrar_vida(tela)

                self.old_rect = self.rect.copy() #mantém a cópia da rect anterior atualizada - para caso de colisão
                
                keys = pygame.key.get_pressed()#verificar as teclas apertadas
                #Movimentar para CIMA
                if keys[pygame.K_UP]:
                        self.direction = 'up'
                        self.ataque_dir = 'up'                        
                        self.last_direction = self.direction
                        self.dir.y = -1
                        
                #Movimentar para BAIXO        
                elif keys[pygame.K_DOWN]:
                        self.direction = 'down'
                        self.ataque_dir = 'down'
                        self.last_direction = self.direction
                        self.dir.y = 1
                        
                else:
                        self.dir.y = 0 #Se não há movimento vertical, y=0
                        
                #Movimentar para ESQUERDA
                if keys[pygame.K_LEFT]:
                    
                    if keys[pygame.K_UP]:
                        self.ataque_dir = 'leftup'
                        
                    elif keys[pygame.K_DOWN]:
                        self.ataque_dir = 'leftdown'
                        
                    elif keys[pygame.K_UP] == False or keys[pygame.K_DOWN] == False:
                        self.ataque_dir = 'left'

                    self.direction = 'left'                        
                    self.last_direction = self.direction
                    self.dir.x = -1
                        
                #Movimentar para DIREITA        
                elif keys[pygame.K_RIGHT]:
                    
                    if keys[pygame.K_UP]:
                        self.ataque_dir = 'rightup'
                        
                    elif keys[pygame.K_DOWN]:
                        self.ataque_dir = 'rightdown'
                        
                    else:
                        self.ataque_dir = 'right'
                        
                    self.direction = 'right'
                    self.last_direction = self.direction
                    self.dir.x = 1

                
                        
                else:
                        self.dir.x = 0 #Se não há movimento horizontal, x=0

                #Se não há movimento em nenhuma direção, definir como 'PARADO'
                if self.dir.x == 0 and self.dir.y == 0:
                        self.direction = 'stand'      

                #Realizar animações conforme a direção
                #PARADO
                if self.direction == 'stand':
                        pass
                
                if not self.direction == 'stand': #caso direction seja stand, dará erro, portanto verifica que a direction não ocassione erro
                        
                        self.animation_timer += delta_time #Definir timer da animação, conforme delta_time
                        if self.animation_timer >= 0.05: #Definir tempo para mudar animação
                                self.animation_timer = 0.0 #Zerar o timer para calcular a proxima mudança
                                self.animation_index = (self.animation_index + 1) % len(self.images[self.direction]) #definir o index da animação para escolher o sprite
                                self.image = self.images[self.direction][self.animation_index] #Definir o sprite da animação atual conforme a direction

                if self.key_down == True: #Detecção de tecla clicada no loop principal do jogo
                        if not self.last_direction == 'stand': #and not (coordenada do mapa para a cidade aqui)
                                self.image = self.images['ataque'][self.last_direction] #Definir o sprite da animação atual
                                self.axe_image = self.axe_images['ataque'][self.last_direction] #Definir o sprite do axe da animação atual
                                if self.last_direction == 'left' or self.last_direction == 'right': #Definir o sprite da armor caso o personagem esteja de lado
                                        self.armor_image = self.armor_images['ataque'][self.last_direction]
                                        
                                #Impede a animação do personagem enquanto executa o ataque
                                self.dir.x = 0
                                self.dir.y = 0
                                self.direction = 'stand'                                                
                                                
                else:
                        #Quando soltar a tecla, retornar o sprite ao estado atual e realizar o ataque
                        if not self.last_direction == 'stand':
                                self.image = self.images[self.last_direction][self.animation_index]
                                self.axe_image = self.axe_images[self.last_direction][self.animation_index]
                                self.armor_image = self.armor_images[self.last_direction][self.animation_index]
                                
                                #if not (coordenada do mapa para a cidade aqui) == True:
                                        #Definir aqui o ataque em sí, dano ao inimigo, detecção de colisão etc                                       
                                        
                                #if (coordenada do mapa para a cidade aqui) == True:
                                        #criar interação ao invés de ataque

                #aplicar a direção multiplicada pela velocidade e delta_time
                self.rect.x += self.dir.x * self.speed * delta_time 
                self.rect.y += self.dir.y * self.speed * delta_time
           
class Equipamentos():
        def __init__(self):
                self.axe_nv = 0
                self.helmet_nv = 0
                self.armor_nv = 0
                
                #Define os valores iniciais para a imagem do machado do personagem
                self.axe_images={
                        'down':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_baixo3.png')],
                        'up':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_cima3.png')],
                        'left':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_left1.png')],
                        'right':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_right1.png')],
                        'ataque':{'down':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_down.png'),'up':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_up.png'),'left':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_left.png'),'right':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_right.png')}
                        }
                
                #Define os valores iniciais para a imagem do elmo do personagem
                self.helmet_images={
                'down':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_baixo3.png')],
                'up':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_cima3.png')],
                'left':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_left1.png')],
                'right':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_right1.png')]
                }

                #Define os valores iniciais para a imagem do peito do personagem
                self.armor_images={
                'up':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_baixo3.png')],
                'down':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_cima3.png')],
                'left':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left1.png')],
                'right':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right1.png')],
                'ataque':{'right':pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right_ataque.png'),'left':pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left_ataque.png')}
                }

        def definir_nivel(self):
                #Definir equipamentos de nv1
                if self.helmet_nv >= 1 and self.helmet_nv < 5:
                        self.helmet_images={
                        'down':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_baixo3.png')],
                        'up':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_cima3.png')],
                        'left':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_left1.png')],
                        'right':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_right1.png')]
                        }

                if self.armor_nv >= 1 and self.armor_nv < 5 :
                        self.armor_images={
                        'down':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_baixo1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_baixo2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_baixo3.png')],
                        'up':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_cima1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_cima2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_cima3.png')],
                        'left':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left1.png')],
                        'right':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right1.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right2.png'),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right1.png')],
                        'ataque':{'right':pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right_ataque.png'),'left':pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left_ataque.png')}
                        }

                #Definir equipamentos de nv5
                if self.axe_nv >= 5 and self.axe_nv < 10:
                        pass
                '''
                        self.axe_images={
                        'down':[],
                        'up':[],
                        'left':[],
                        'right':[]
                        }
                '''
                if self.helmet_nv >= 5 and self.helmet_nv < 10:
                        pass
                '''
                        self.helmet_images={
                        'down':[],
                        'up':[],
                        'left':[],
                        'right':[]
                        }
                '''
                if self.armor_nv >= 5 and self.armor_nv < 10 :
                        pass
                '''
                        self.armor_images={
                        'down':[],
                        'up':[],
                        'left':[],
                        'right':[]
                        }
                '''

        def definir_equipamentos(self,character):
                character.equipamento_atual(self.axe_images,self.helmet_images,self.armor_images)

class Inimigos(pygame.sprite.Sprite):
        def __init__(self,x,y,race='aranha'):
                super().__init__()
                #Imagens inicial, pra dar o init sem problema
                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_parada.png'),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerda.png'),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direita.png'),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_cima.png'),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_baixo.png'),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdabaixo.png'),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdacima.png'),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitabaixo.png'),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitacima.png')
                                       }
                self.image = self.images['parada'] #imagem inicial
                
                #Definições da rect e posição do inimigo 
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.pos = pygame.math.Vector2(self.rect.topleft) #Vetor de posição
                self.old_rect = self.rect.copy() #para detectar colisao e saber onde estava
                
                #movimentação do inimigo
                self.dx = 0 
                self.dy = 0

                #Definições do inimigo
                self.maxhealth = 50
                self.health = 50
                self.speed = 1  
                self.type = 'monstro'
                self.race = race
                self.dano = 1
                self.level = 0

        def draw_health(self,tela, x, y):
            # Desenha a barra de vida do inimigo acima dele
            frac_hp_aranha = int((50*self.health)/self.maxhealth)
            pygame.draw.rect(tela, (255,0,0), (x, y, frac_hp_aranha, 1)) #talvez a cor sofra alteração caso não esteja bom com o fundo

        def tipo(self):
                if self.race == 'aranha':
                        if self.level < 10:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_parada.png'),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerda.png'),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direita.png'),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_cima.png'),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_baixo.png'),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdabaixo.png'),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdacima.png'),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitabaixo.png'),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitacima.png')
                                               }
                                
                        if self.level >= 10 and self.level < 20:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_parada.png'),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_esquerda.png'),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_direita.png'),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_cima.png'),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_baixo.png'),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_esquerdabaixo.png'),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_esquerdacima.png'),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_direitabaixo.png'),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_direitacima.png')
                                               }
                                self.maxhealth = 100
                                self.health = self.maxhealth
                                
                        if self.level >= 20 and self.level < 30:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_parada.png'),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_esquerda.png'),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_direita.png'),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_cima.png'),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_baixo.png'),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_esquerdabaixo.png'),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_esquerdacima.png'),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_direitabaixo.png'),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_direitacima.png')
                                               }
                                self.maxhealth = 150
                                self.health = self.maxhealth
                                
                        if self.level >= 30 and self.level < 50:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_parada.png'),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_esquerda.png'),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_direita.png'),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_cima.png'),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_baixo.png'),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_esquerdabaixo.png'),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_esquerdacima.png'),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_direitabaixo.png'),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_direitacima.png')
                                               }
                                self.maxhealth = 300
                                self.health = self.maxhealth
                                
                        if self.level >= 50:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_parada.png'),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_esquerda.png'),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_direita.png'),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_cima.png'),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_baixo.png'),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_esquerdabaixo.png'),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_esquerdacima.png'),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_direitabaixo.png'),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_direitacima.png')
                                               }
                                self.maxhealth = 500
                                self.health = self.maxhealth                              
      
                ####Aqui colocar todas as sprites, definir o inimigo através do tipo dele e não ter uma class pra cada tipo

        def update(self,tela,player):
                
                self.old_rect = self.rect.copy() #copia da rect pra colisao
                
                # Movimenta o inimigo em direção ao jogador
                player_pos = player.rect.center
                enemy_pos = self.rect.center
                dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
                dist = math.sqrt(dx ** 2 + dy ** 2)
                if dist != 0:
                        dx, dy = dx / dist, dy / dist
                self.dx, self.dy = dx * self.speed, dy * self.speed
                self.rect.x += self.dx
                self.rect.y += self.dy

                self.draw_health(tela,self.rect.x,self.rect.y) #gera a barra de vida em cima da aranha

                if round(self.dx,0) == 0 and round(self.dy,0) == 0:
                        self.image = self.images['parada']

                if round(self.dx,0) < 0 and round(self.dy,0) == 0:
                        #indo pra esquerda
                        self.image = self.images['esquerda']
                        
                if round(self.dx,0) > 0 and round(self.dy,0) == 0:
                        #indo pra direita
                        self.image = self.images['direita']

                if round(self.dy,0) < 0 and round(self.dx,0) == 0:
                        #indo pra cima
                        self.image = self.images['cima']

                if round(self.dy,0) > 0 and round(self.dx,0) == 0:
                        #indo pra baixo
                        self.image = self.images['baixo']

                if round(self.dy,0) < 0 and round(self.dx,0) < 0:
                        #esquerda e cima
                        self.image = self.images['esquerdacima']

                if round(self.dy,0) > 0 and round(self.dx,0) > 0:
                        #direita e baixo
                        self.image = self.images['direitabaixo']

                if round(self.dy,0) < 0 and round(self.dx,0) > 0:
                        #direita e cima
                        self.image = self.images['direitacima']

                if round(self.dy,0) > 0 and round(self.dx,0) < 0:
                        #esquerda e baixo
                        self.image = self.images['esquerdabaixo']

#############################################################################################################################################################################################################################################################################################################################################################################################################################################    
  
class Menu:
    def __init__(self):
        self.load = pygame.image.load(r'graphics/Menu/loadgame.png')
        self.save = pygame.image.load(r'graphics/Menu/savegame.png')
        self.quit = pygame.image.load(r'graphics/Menu/quitgame.png')
        self.menu = pygame.image.load(r'graphics/Menu/menu_jogo.png')
        
    def abrir(self, tela):        
        tela.blit(self.menu, (0,0))
        tela.blit(self.load,(40,150))
        tela.blit(self.save,(300,250))
        tela.blit(self.quit,(40,350))
        clicou_load = pygame.Rect(40,150,250,50)
        clicou_save = pygame.Rect(300,250,250,50)
        clicou_quit = pygame.Rect(40,350,250,50)
        pygame.display.update()
        if pygame.mouse.get_pressed() == (1,0,0):
            mouseposition = pygame.mouse.get_pos()
            if clicou_load.collidepoint(mouseposition):
                self.loadgame()
            if clicou_save.collidepoint(mouseposition):
                self.savegame()                
            if clicou_quit.collidepoint(mouseposition):
                self.quitgame()

    def loadgame(self):
        ##########DAR UM SINAL DE QUE O CLIQUE FUNCIONOU
        pass
        '''
        try:
            dados_jogo = {}
            with open('savegame.dat', 'rb') as arquivo:
                dados_jogo = pickle.load(arquivo)
                
                ##########DAR UM SINAL DE QUE O LOAD FUNCIONOU
                ############## ALTERAR TODOS ESSES DADOS
            v.score = dados_jogo['score']
            v.score_aranha = dados_jogo['score_aranha']
            ############# DADOS DE EXEMPLO PRA LEMBRAR
            

        except FileNotFoundError:
            pass #Mostrar que não há save para carregar
        #imagem cinza do load e som de erro?
        '''
                           

            
        
    def savegame(self):
        pass
        ##########DAR UM SINAL DE QUE O CLIQUE FUNCIONOU
        '''
        if v.Norte == 0 and v.Sul == 0 and v.Leste == 0 and v.Oeste == 0:
            dados_mapa = 0
        if v.Norte != 0 or v.Sul != 0 or v.Leste != 0 or v.Oeste != 0:
            dados_mapa = 1
        if v.Norte == 1 and v.Oeste == 2:
            dados_mapa = 2
        if v.Norte == 1 and v.Oeste == 3:
            dados_mapa = 3
            #Isso aqui serve pra definir qual o mapa carregar, salvando ele como um numero. Mas ainda não defini como vai funcionar a mudança de mapa, portanto talvez seja inutil
            
        #exemplo pra lembrar como que salva
        dados_jogo = {
            'score' : v.score,
            'score_aranha' : v.score_aranha
            }
        
        with open('savegame.dat', 'wb') as arquivo:
            pickle.dump(dados_jogo, arquivo)
            ##########DAR UM SINAL DE QUE O SAVE FUNCIONOU
        '''

    def quitgame(self):
        #criar pop up perguntando se tem certeza?
        pygame.quit()
        sys.exit()
        
#############################################################################################################################################################################################################################################################################################################################################################################################################################################    
  
class Attack(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
            self.rect = self.image.get_rect()
            
        def criar(self, x, y, direction,level):
            #Definição de posição do ataque
            self.rect.x = x
            self.rect.y = y

            #Outras definições
            self.speed = 15
            self.direction = direction
            self.level = level
            self.dano = 1

        def equipamentos(self):
            pass
        #Se equipamento lvl 1 --> dano = 1
        #Se equipamento lvl 10 --> dano = x
        #Se equipamento lvl 50 --> dano = 1000
            
        def update(self,player,npc,inimigo,arvore,damage_show,delta_time,tela,font):
            if self.level == 1:
                self.dano = 1
                
            if self.level == 2:
                self.dano = 1
                
            elif self.level > 2:
                self.dano = int(round((self.level*0.5), 1))
                
            # Movimenta o ataque na direção em que o jogador está se movendo
            if self.direction == 'left':
                    self.rect.x -= self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\left.png')
                    
            elif self.direction == 'right':
                    self.rect.x += self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\right.png')
                    
            elif self.direction == 'up':
                    self.rect.y -= self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\up.png')
                    
            elif self.direction == 'down':
                    self.rect.y += self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\down.png')

            elif self.direction == 'rightdown':
                    self.rect.y += self.speed
                    self.rect.x += self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\rightdown.png')
                    
            elif self.direction == 'rightup':
                    self.rect.y -= self.speed
                    self.rect.x += self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\rightup.png')
                    
            elif self.direction == 'leftdown':
                    self.rect.y += self.speed
                    self.rect.x -= self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\leftdown.png')
                    
            elif self.direction == 'leftup':
                    self.rect.y -= self.speed
                    self.rect.x -= self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\leftup.png')

########################################################################################################################################################################################################################################
            #npc_hit = pygame.sprite.spritecollide(self,npc_grupo,False)
            #for npc in npc_hit:
                #npc.acao() #pra abrir a janela de conversa com o NPC quando eu criar eles kk
                
            #verifica se o ataque corta a arvore - Que eu ainda preciso por
            #if v.axe_equip:
                #spriteszinhos = pygame.sprite.spritecollide(self, arvore, True)
                #if spriteszinhos:
                   # if v.randomgen() == 'monstro':
                        
                        #for sprites in spriteszinhos:
                           # v.monstrinhox = sprites.old_rect.x
                            #v.monstrinhoy = sprites.old_rect.y
                            
                            #v.criar_monstro = True
                    #elif v.randomgen() == 'troncos':
                        ####################################GERAR AQUI UMA ANIMAÇÃO DE ITEM
                       #v.troncos += random.randrange(0,4)
########################################################################################################################################################################################################################################

            # Verifica colisão com os inimigos
            hit_enemies = pygame.sprite.spritecollide(self, inimigo, False)
            for enemy in hit_enemies:
                enemy.health -= self.dano        
                #criar animação do dano
                damage_show.infos(enemy.rect.x, enemy.rect.y, self.dano,(255,0,0))
                damage_show.create_text(font)
                damage_show.draw(delta_time, tela)
                
                if self.direction == 'right':
                    enemy.rect.x += 4
                    
                if self.direction == 'left':
                    enemy.rect.x -= 4
                    
                if self.direction == 'up':
                    enemy.rect.y -= 4
                    
                if self.direction == 'down':
                    enemy.rect.y += 4

                #Vou precisar por todas as 4 direcoes :( 
                    
                if enemy.health <= 0:
                    enemy.kill()
                    '''
                    if v.aranha_on == True:
                        v.score_aranha += 1
                    if v.urso_on == True:
                        v.score_urso += 1
                    if v.lobo_on == True:
                        v.score_lobo += 1
                    if v.rainha_aranha_on == True:
                        v.score_rainha_aranha += 1
                    v.score = v.score_aranha + v.score_urso + v.score_lobo + v.score_rainha_aranha
                    v.exp += v.exp_mob
                    ''' #Ajeitar questão do score

            # Remove o ataque da v.tela quando atinge o limite da distância                          
            player_pos = player.rect.center
            player_posxd = player_pos[0] +3 #direita
            player_posyb = player_pos[1] +3 #baixo
            player_posxe = player_pos[0] - 43 #esquerda
            player_posyc = player_pos[1] - 43 #cima
            if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                self.kill()

#############################################################################################################################################################################################################################################################################################################################################################################################################################################    

#
