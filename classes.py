import pygame, sys, math, random, pickle, datetime
import var as v

########################################################################################################################################################################################################################################

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

########################################################################################################################################################################################################################################
                
class Player(pygame.sprite.Sprite):
        def __init__(self,x,y,tela):
                super().__init__() 
                
                #movimentação do personagem
                self.images = {
                'down':[pygame.image.load(r'Graphics\Character\charbaixo1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charbaixo2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charbaixo3.png').convert_alpha()],                            
                'up':[pygame.image.load(r'Graphics\Character\charcima1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charcima2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charcima3.png').convert_alpha()],
                'left':[pygame.image.load(r'Graphics\Character\charleft1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charleft2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charleft1.png').convert_alpha()],
                'right':[pygame.image.load(r'Graphics\Character\charright1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charright2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\charright1.png').convert_alpha()],
                'ataque':{'down':pygame.image.load(r'Graphics\Character\charbaixo_ataque.png').convert_alpha(),'up':pygame.image.load(r'Graphics\Character\charcima_ataque.png').convert_alpha(),'left':pygame.image.load(r'Graphics\Character\charleft_ataque.png').convert_alpha(),'right':pygame.image.load(r'Graphics\Character\charright_ataque.png').convert_alpha()}
                }
                self.image = self.images['down'][0]
                
                #Definições da imagem e pos do personagem
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.old_rect = self.rect.copy()
                self.dir = pygame.math.Vector2() #vetor de direção
                self.speed = 100 #velocidade

                #variaveis de colisao
                self.colisao_direita = False
                self.colisao_esquerda = False
                self.colisao_baixo = False
                self.colisao_cima = False
                
                #definições das animações e movimentos
                self.animation_timer = 0.0 #timer de animação
                self.animation_index = 0 #index da animação atual
                self.lvlup_animation_timer = 0.0
                self.lvlup_animation_index = 0
                self.direction = 'stand' #direção do personagem
                self.last_direction = 'stand' #registra a ultima direção do personagem
                self.atacando = False #Define se o personagem está realizando um ataque
                self.ataque_dir = 'down' #Define o lado de ataque do personagem
                self.key_down = False

                #imagens hud
                self.char_health_img = pygame.image.load(r'Graphics\HUD\char_health_normal.png')
                self.char_health_damage_img = pygame.image.load(r'Graphics\HUD\char_health_damage.png')
                self.blit_health = self.char_health_img
                self.char_exp_img = pygame.image.load(r'Graphics\HUD\char_exp.png')
                self.char_exp_gain_img = pygame.image.load(r'Graphics\HUD\char_exp_gain.png')
                self.blit_exp = self.char_exp_img
                
                #Definições de atributos
                self.nivel = 1 #nivel do personagem
                self.exp = 0
                self.prox_exp = 100
                self.health = 50 #define a vida do personagem
                self.max_health = 50 #define o limite de vida do personagem

                #definições iniciais do inventário
                self.inventario = {'troncos':0,
                                   'metais':0,
                                   'tecidos':0,
                                   'couros':0,
                                   'ouro':0,
                                   'diamante':0,
                                   'ouro_vermelho':0,
                                   'ouro_negro':0,
                                   'troncos1':0,
                                   'troncos2':0,
                                   'troncos3':0,
                                   'troncos4':0,
                                   'troncos5':0,
                                   'metais1':0,
                                   'metais2':0,
                                   'metais3':0,
                                   'metais4':0,
                                   'tecidos1':0,
                                   'tecidos2':0,
                                   'tecidos3':0,
                                   'tecidos4':0,
                                   'couros1':0,
                                   'couros2':0,
                                   'couros3':0,
                                   'couros4':0,
                                   'pocao_pequena':0,
                                   'pocao_media':0,
                                   'pocao_grande':0
                                   }
                
                #definição da tela
                self.tela = tela

        def quest_principal(self):
            pass

        def evoluir(self, tela, delta_time):
            calc_lvlup = self.nivel * 100
            lvlup_cond = self.exp / calc_lvlup
            if lvlup_cond >= 1:
                som_lvl_up = pygame.mixer.Sound(r'sounds\lvlup.mp3')
                pygame.mixer.Sound.set_volume(som_lvl_up,0.1)
                pygame.mixer.Sound.play(som_lvl_up)
                #mostrar tela de lvlup
                lvlup1 = pygame.image.load(r'Graphics\Character\LevelUp\lvlup1.png').convert_alpha()
                lvlup2 = pygame.image.load(r'Graphics\Character\LevelUp\lvlup2.png').convert_alpha()
                lvlup3 = pygame.image.load(r'Graphics\Character\LevelUp\lvlup3.png').convert_alpha()
                lvlup_group = [lvlup1,lvlup2,lvlup3]

                self.lvlup_animation_timer += delta_time
                animation_count = 0
                while animation_count < 4:
                    if self.lvlup_animation_timer <= 0.5:                                  
                        tela.blit(lvlup_group[self.lvlup_animation_index],(self.rect.x,self.rect.y))
                        self.lvlup_animation_index = (self.lvlup_animation_index + 1) % len(lvlup_group)
                        pygame.display.flip()
                        self.animation_timer = 0.0
                        animation_count += 1
                        
                self.nivel += 1
                self.exp = 0
                self.prox_exp = self.nivel * 100
                self.max_health += 5
                self.health = self.max_health

        def mostrar_vida(self, tela):            
            frac_hp = int((50*self.health)/self.max_health)
            pygame.draw.rect(tela, (255,0,0), (320, 42, frac_hp*1.95, 13))
            tela.blit(self.blit_health,(317,0))

            frac_exp = int((50*self.exp)/self.prox_exp)
            pygame.draw.rect(tela,(0,255,255),(600,42,frac_exp*1.95,13))
            tela.blit(self.blit_exp,(597,25))

        def colisao(self,obstaculo,damage_show,font,delta_time,tela):
                    colisao_sprites = pygame.sprite.spritecollide(self,obstaculo,False)
                    if colisao_sprites:
                        for sprite in colisao_sprites:
                                if sprite.type == 'monstro':
                                        self.health -= sprite.dano #gerar dano no personagem conforme o dano do inimigo                                        
                                        #criar animação do dano
                                        self.blit_health = self.char_health_damage_img
                                        damage_show.infos(self.rect.x+40, self.rect.y, sprite.dano,(255,0,0))
                                        damage_show.create_text(font)
                                        damage_show.draw(delta_time, tela)
                                
                                #colisão na direita
                                if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                                                self.rect.right = sprite.rect.left
                                                self.dir.x = 0
                                                if sprite.type == 'monstro':
                                                        sprite.rect.x += 7
                                                        
                                #colisão na esquerda
                                if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                                                self.rect.left = sprite.rect.right
                                                self.dir.x = 0
                                                if sprite.type == 'monstro':
                                                        sprite.rect.x -= 7
                                #colisão em baixo
                                if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                                                self.rect.bottom = sprite.rect.top
                                                self.dir.y = 0
                                                if sprite.type == 'monstro':
                                                        sprite.rect.y += 7
                                                        
                                #colisão em cima
                                if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                                                self.rect.top = sprite.rect.bottom
                                                self.dir.y = 0
                                                if sprite.type == 'monstro':
                                                        sprite.rect.y -= 7
                    else:
                        self.blit_health = self.char_health_img
                        
                                            

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
                        
                        #blitar a imagem do axe, armor e helmet atual, conforme a direction para blitar no local correto
                        if not self.direction == 'stand':
                            ################################################################################################################################################ PRECISO VERIFICAR ARMOR E HELMET
                            if self.direction == 'right':
                                self.tela.blit(self.helmet_image,self.rect.topleft)
                                self.tela.blit(self.armor_image,self.rect.topleft)
                                self.tela.blit(self.axe_image,self.rect.topleft)
                                
                            if self.direction == 'left':
                                leftx = self.rect.x - 6
                                lefty = self.rect.y - 2
                                self.tela.blit(self.helmet_image,(leftx,lefty))
                                self.tela.blit(self.armor_image,(leftx,lefty))
                                self.tela.blit(self.axe_image,(leftx,lefty))

                            if self.direction == 'up':
                                upx = self.rect.x - 10
                                upy = self.rect.y - 2
                                self.tela.blit(self.helmet_image,(upx,upy))
                                self.tela.blit(self.armor_image,(upx,upy))
                                self.tela.blit(self.axe_image,(upx,upy))

                            if self.direction == 'down':
                                downx = self.rect.x - 10
                                downy = self.rect.y - 2
                                self.tela.blit(self.helmet_image,(downx,downy))
                                self.tela.blit(self.armor_image,(downx,downy))
                                self.tela.blit(self.axe_image,(downx,downy))
                                
                        elif self.direction == 'stand':
                            
                            if self.last_direction == 'right':
                                self.tela.blit(self.helmet_image,self.rect.topleft)
                                self.tela.blit(self.armor_image,self.rect.topleft)
                                self.tela.blit(self.axe_image,self.rect.topleft)
                                
                            if self.last_direction == 'left':
                                leftx = self.rect.x - 6
                                lefty = self.rect.y - 2
                                self.tela.blit(self.helmet_image,(leftx,lefty))
                                self.tela.blit(self.armor_image,(leftx,lefty))
                                self.tela.blit(self.axe_image,(leftx,lefty))

                            if self.last_direction == 'up':
                                upx = self.rect.x - 10
                                upy = self.rect.y - 2
                                self.tela.blit(self.helmet_image,(upx,upy))
                                self.tela.blit(self.armor_image,(upx,upy))
                                self.tela.blit(self.axe_image,(upx,upy))

                            if self.last_direction == 'down':
                                downx = self.rect.x - 10
                                downy = self.rect.y - 2
                                self.tela.blit(self.helmet_image,(downx,downy))
                                self.tela.blit(self.armor_image,(downx,downy))
                                self.tela.blit(self.axe_image,(downx,downy))
                                
                  
        def update(self,delta_time, tela):
                if self.inventario['ouro'] > 1000000:
                    self.inventario['ouro'] -= 1000000
                    self.inventario['diamante'] += 1
                if self.inventario['diamante'] > 1000000:
                    self.inventario['diamante'] -= 1000000
                    self.inventario['ouro_vermelho'] += 1
                if self.inventario['ouro_vermelho'] > 1000000:
                    self.inventario['ouro_vermelho'] -= 1000000
                    self.inventario['ouro_negro'] += 1
                      
                self.equipado()
                self.mostrar_vida(tela)
                self.evoluir(tela, delta_time)

                #Atualização da rect para a colisão coincidir com o sprite
                atualizar_rect = self.image.get_rect()
                self.rect.width = atualizar_rect[2]
                self.rect.height = atualizar_rect[3]

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

########################################################################################################################################################################################################################################
                
class Equipamentos():
        def __init__(self):
                self.axe_nv = 0
                self.helmet_nv = 0
                self.armor_nv = 0
                
                #Define os valores iniciais para a imagem do machado do personagem
                self.axe_images={
                        'down':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_baixo1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_baixo2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_baixo3.png').convert_alpha()],
                        'up':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_cima1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_cima2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_cima3.png').convert_alpha()],
                        'left':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_left1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_left2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_left1.png').convert_alpha()],
                        'right':[pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_right1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_right2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\axe_right1.png').convert_alpha()],
                        'ataque':{'down':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_down.png').convert_alpha(),'up':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_up.png').convert_alpha(),'left':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_left.png').convert_alpha(),'right':pygame.image.load(r'Graphics\Character\Equips\Axe\nv0\ataque_axe_right.png').convert_alpha()}
                        }
                
                #Define os valores iniciais para a imagem do elmo do personagem
                self.helmet_images={
                'down':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_baixo1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_baixo2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_baixo3.png').convert_alpha()],
                'up':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_cima1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_cima2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_cima3.png').convert_alpha()],
                'left':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_left1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_left2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_left1.png').convert_alpha()],
                'right':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_right1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_right2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv0\helmet_right1.png').convert_alpha()]
                }

                #Define os valores iniciais para a imagem do peito do personagem
                self.armor_images={
                'up':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_baixo1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_baixo2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_baixo3.png').convert_alpha()],
                'down':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_cima1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_cima2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_cima3.png').convert_alpha()],
                'left':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left1.png').convert_alpha()],
                'right':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right1.png').convert_alpha()],
                'ataque':{'right':pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_right_ataque.png').convert_alpha(),'left':pygame.image.load(r'Graphics\Character\Equips\Armor\nv0\armor_left_ataque.png').convert_alpha()}
                }

        def definir_nivel(self):
                #Definir equipamentos de nv1
                if self.helmet_nv >= 1 and self.helmet_nv < 5:
                        self.helmet_images={
                        'down':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_baixo1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_baixo2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_baixo3.png').convert_alpha()],
                        'up':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_cima1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_cima2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_cima3.png').convert_alpha()],
                        'left':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_left1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_left2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_left1.png').convert_alpha()],
                        'right':[pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_right1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_right2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Helmet\nv1\helmet_right1.png').convert_alpha()]
                        }

                if self.armor_nv >= 1 and self.armor_nv < 5 :
                        self.armor_images={
                        'down':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_baixo1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_baixo2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_baixo3.png').convert_alpha()],
                        'up':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_cima1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_cima2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_cima3.png').convert_alpha()],
                        'left':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left1.png').convert_alpha()],
                        'right':[pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right1.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right2.png').convert_alpha(),pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right1.png').convert_alpha()],
                        'ataque':{'right':pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_right_ataque.png').convert_alpha(),'left':pygame.image.load(r'Graphics\Character\Equips\Armor\nv1\armor_left_ataque.png').convert_alpha()}
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

########################################################################################################################################################################################################################################

class Inimigos(pygame.sprite.Sprite):
        def __init__(self,x,y,race='aranha'):
                super().__init__()
                #Imagens inicial, pra dar o init sem problema
                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_parada.png').convert_alpha(),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerda.png').convert_alpha(),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direita.png').convert_alpha(),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_cima.png').convert_alpha(),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_baixo.png').convert_alpha(),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdabaixo.png').convert_alpha(),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdacima.png').convert_alpha(),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitabaixo.png').convert_alpha(),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitacima.png').convert_alpha()
                                       }
                self.image = self.images['parada'] #imagem inicial
                
                #Definições da rect e posição do inimigo 
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.pos = pygame.math.Vector2(self.rect.topleft) #Vetor de posição
                self.old_rect = self.rect.copy() #para detectar colisao e saber onde estava
                self.mask = pygame.mask.from_surface(self.image)#Cria a mask pra detectar colisão
                
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
                self.exp = 0
                self.lvlup_cond = 0
                self.valor_exp = 10 + self.level

        def draw_health(self,tela, x, y):
            # Desenha a barra de vida do inimigo acima dele
            frac_hp_aranha = int((50*self.health)/self.maxhealth)
            pygame.draw.rect(tela, (255,0,0), (x, y, frac_hp_aranha, 1)) #talvez a cor sofra alteração caso não esteja bom com o fundo

        def levelup(self):
            if self.lvlup_cond >= 1:
                if self.race == 'aranha':
                    v.mob_aranha_level += 1
                    v.mob_aranha_exp = 0
                    self.dano += self.level
                    
                if self.race == 'lobo':
                    v.mob_lobo_level += 1
                    v.mob_lobo_exp = 0
                    self.dano += self.level
                    
                if self.race == 'urso':
                    v.mob_urso_level += 1
                    v.mob_urso_exp = 0
                    self.dano += self.level
                    
                if self.race == 'aranha_rainha':
                    v.mob_aranha_rainha_level += 1
                    v.mob_aranha_rainha_exp = 0
                    self.dano += self.level
            

        def tipo(self):
                if self.race == 'aranha':
                        self.level = v.mob_aranha_level
                        self.exp = v.mob_aranha_exp
                        self.dano += self.level
                        if not self.level == 0:
                            self.lvlup_cond = self.exp / (self.level*50)
                        else:
                            self.lvlup_cond = self.exp / 50
                        if self.level < 10:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_parada.png').convert_alpha(),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerda.png').convert_alpha(),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direita.png').convert_alpha(),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_cima.png').convert_alpha(),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_baixo.png').convert_alpha(),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdabaixo.png').convert_alpha(),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_esquerdacima.png').convert_alpha(),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitabaixo.png').convert_alpha(),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv0/aranha_direitacima.png').convert_alpha()
                                               }
                                
                        if self.level >= 10 and self.level < 20:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_parada.png').convert_alpha(),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_esquerda.png').convert_alpha(),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_direita.png').convert_alpha(),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_cima.png').convert_alpha(),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_baixo.png').convert_alpha(),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_esquerdabaixo.png').convert_alpha(),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_esquerdacima.png').convert_alpha(),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_direitabaixo.png').convert_alpha(),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv10/aranha_direitacima.png').convert_alpha()
                                               }
                                self.maxhealth = 100
                                self.health = self.maxhealth
                                self.valor_exp = 20
                                
                        if self.level >= 20 and self.level < 30:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_parada.png').convert_alpha(),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_esquerda.png').convert_alpha(),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_direita.png').convert_alpha(),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_cima.png').convert_alpha(),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_baixo.png').convert_alpha(),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_esquerdabaixo.png').convert_alpha(),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_esquerdacima.png').convert_alpha(),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_direitabaixo.png').convert_alpha(),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv20/aranha_direitacima.png').convert_alpha()
                                               }
                                self.maxhealth = 150
                                self.health = self.maxhealth
                                self.valor_exp = 50
                                
                        if self.level >= 30 and self.level < 50:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_parada.png').convert_alpha(),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_esquerda.png').convert_alpha(),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_direita.png').convert_alpha(),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_cima.png').convert_alpha(),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_baixo.png').convert_alpha(),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_esquerdabaixo.png').convert_alpha(),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_esquerdacima.png').convert_alpha(),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_direitabaixo.png').convert_alpha(),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv30/aranha_direitacima.png').convert_alpha()
                                               }
                                self.maxhealth = 300
                                self.health = self.maxhealth
                                self.valor_exp = 100
                                
                        if self.level >= 50:
                                self.images = {'parada' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_parada.png').convert_alpha(),
                'esquerda' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_esquerda.png').convert_alpha(),
                'direita' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_direita.png').convert_alpha(),
                'cima' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_cima.png').convert_alpha(),
                'baixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_baixo.png').convert_alpha(),
                'esquerdabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_esquerdabaixo.png').convert_alpha(),
                'esquerdacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_esquerdacima.png').convert_alpha(),
                'direitabaixo' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_direitabaixo.png').convert_alpha(),
                'direitacima' : pygame.image.load(r'Graphics/Mob/Aranha/nv50/aranha_direitacima.png').convert_alpha()
                                               }
                                self.maxhealth = 500
                                self.health = self.maxhealth
                                self.valor_exp = 200
      
                ####Aqui colocar todas as sprites, definir o inimigo através do tipo dele e não ter uma class pra cada tipo

        def update(self,tela,player):
                
                self.old_rect = self.rect.copy() #copia da rect pra colisao
                self.mask = pygame.mask.from_surface(self.image) #Atualiza a mask
                self.levelup()

                if self.race == 'aranha':
                    self.level = v.mob_aranha_level
                    self.exp = v.mob_aranha_exp
                    if not self.level == 0:
                        self.lvlup_cond = self.exp / (self.level*50)
                    else:
                        self.lvlup_cond = self.exp / 50
                        
                if self.race == 'lobo':
                    self.level = v.mob_lobo_level
                    self.exp = v.mob_lobo_exp
                    if not self.level == 0:
                        self.lvlup_cond = self.exp / (self.level*150)
                    else:
                        self.lvlup_cond = self.exp / 150
                    
                    
                if self.race == 'urso':
                    self.level = v.mob_urso_level
                    self.exp = v.mob_urso_exp
                    if not self.level == 0:
                        self.lvlup_cond = self.exp / (self.level*250)
                    else:
                        self.lvlup_cond = self.exp / 250
                    
                if self.race == 'aranha_rainha':
                    self.level = v.mob_aranha_rainha_level
                    self.exp = v.mob_aranha_rainha_exp
                    if not self.level == 0:
                        self.lvlup_cond = self.exp / (self.level*500)
                    else:
                        self.lvlup_cond = self.exp / 500                  
                    
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
        self.load = pygame.transform.scale(pygame.image.load(r'graphics/Menu/loadgame.png'),(200,50))
        self.save = pygame.transform.scale(pygame.image.load(r'graphics/Menu/savegame.png'),(200,50))
        self.quit = pygame.transform.scale(pygame.image.load(r'graphics/Menu/quitgame.png'),(200,50))
        self.menu = pygame.image.load(r'graphics/Menu/menu_jogo.png')
        self.loadgame_menu = False
        self.savegame_menu = False
        
    def abrir(self, tela, mouse_rect,mouse_button, fonte, jogador):        
        tela.blit(self.menu, (0,0))#
        tela.blit(self.load,(40,150))#
        tela.blit(self.save,(540,150))#
        tela.blit(self.quit,(280,450))#
        clicou_load = pygame.Rect(85,155,120,30) # +45 da pos x, +5 da pos y, -80 w, - 20 h para a rect ficar certa na imagem
        clicou_save = pygame.Rect(585,155,120,30)
        clicou_quit = pygame.Rect(325,455,120,30)
        
        pygame.draw.rect(tela,(255,255,255),clicou_quit,1)#Test da rect
        pygame.draw.rect(tela,(255,255,255),clicou_save,1)#Test da rect
        pygame.draw.rect(tela,(255,255,255),clicou_load,1)#Test da rect

        #RECT dos savegames 
        save1_rect = pygame.Rect(585,205,120,100)
        save2_rect = pygame.Rect(585,305,120,100)

        #RECT dos loadgames
        load1_rect = pygame.Rect(85,205,120,100)
        load2_rect = pygame.Rect(85,305,120,100)

        mouseposition = pygame.mouse.get_pos()                

        #Detectar colisao nos botões
        if clicou_load.collidepoint(mouseposition):
            self.load = pygame.transform.scale(pygame.image.load(r'graphics/Menu/loadgame_click.png'),(200,50))

        elif clicou_save.collidepoint(mouseposition):
            self.save = pygame.transform.scale(pygame.image.load(r'graphics/Menu/savegame_click.png'),(200,50))

        elif clicou_quit.collidepoint(mouseposition):
            self.quit = pygame.transform.scale(pygame.image.load(r'graphics/Menu/quitgame_click.png'),(200,50))

        else:
            self.load = pygame.transform.scale(pygame.image.load(r'graphics/Menu/loadgame.png'),(200,50))
            self.save = pygame.transform.scale(pygame.image.load(r'graphics/Menu/savegame.png'),(200,50))
            self.quit = pygame.transform.scale(pygame.image.load(r'graphics/Menu/quitgame.png'),(200,50))
        
        if self.loadgame_menu == True:
            self.load = pygame.transform.scale(pygame.image.load(r'graphics/Menu/loadgame_clicked.png'),(200,50))
            #rect do loadgame
            pygame.draw.rect(tela,(255,255,255),load1_rect)
            pygame.draw.rect(tela,(255,255,255),load2_rect)
            #delimitador das rects
            pygame.draw.rect(tela,(0,0,0),pygame.Rect(85,205,120,100),1)
            pygame.draw.rect(tela,(0,0,0),pygame.Rect(85,305,120,100),1)

            #mostrar dia e hora do save
            try:
                with open('save1.dat','rb') as arquivo1:
                    dados1 = pickle.load(arquivo1)
                    savetime_load = dados1['save_time']
                    escrever_dialogo(str(savetime_load),(90,255),fonte,tela,cor=(0,0,0))                    
            except FileNotFoundError:
                pass

            try:
                with open('save2.dat','rb') as arquivo2:
                    dados2 = pickle.load(arquivo2)
                    savetime_load2 = dados2['save_time']
                    escrever_dialogo(str(savetime_load2),(90,355),fonte,tela,cor=(0,0,0))
            except FileNotFoundError:
                pass

        if self.savegame_menu == True:
            self.save = pygame.transform.scale(pygame.image.load(r'graphics/Menu/savegame_clicked.png'),(200,50))
            #rect do savegame
            pygame.draw.rect(tela,(255,255,255),save1_rect)
            pygame.draw.rect(tela,(255,255,255),save2_rect)            
            #delimitador das rects
            pygame.draw.rect(tela,(0,0,0),pygame.Rect(585,205,120,100),1)
            pygame.draw.rect(tela,(0,0,0),pygame.Rect(585,305,120,100),1)

            #mostrar dia e hora do save
            try:
                with open('save1.dat','rb') as arquivo1:
                    dados1 = pickle.load(arquivo1)
                    savetime_load = dados1['save_time']
                    escrever_dialogo(str(savetime_load),(590,255),fonte,tela,cor=(0,0,0))                    
            except FileNotFoundError:
                pass

            try:
                with open('save2.dat','rb') as arquivo2:
                    dados2 = pickle.load(arquivo2)
                    savetime_load2 = dados2['save_time']
                    escrever_dialogo(str(savetime_load2),(590,355),fonte,tela,cor=(0,0,0))
            except FileNotFoundError:
                pass
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    v.abrir_menu = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseposition = pygame.mouse.get_pos()
                
                #Detectar colisao nos botões
                if clicou_load.collidepoint(mouseposition):
                    if not self.loadgame_menu == True:
                        self.loadgame_menu = True
                    else:
                        self.loadgame_menu = False            
                
                if clicou_save.collidepoint(mouseposition):
                    if not self.savegame_menu == True:
                        self.savegame_menu = True
                    else:
                        self.savegame_menu = False
                    
                if clicou_quit.collidepoint(mouseposition):
                    self.quitgame()

                else:
                    self.load = pygame.transform.scale(pygame.image.load(r'graphics/Menu/loadgame.png'),(200,50))
                    self.save = pygame.transform.scale(pygame.image.load(r'graphics/Menu/savegame.png'),(200,50))
                    
                #SELECIONAR OPÇÃO DO SAVEGAME
                if save1_rect.collidepoint(mouseposition) and self.savegame_menu == True:
                    save_time = datetime.datetime.now()
                    self.savegame(tela, mouse_rect, mouse_button, number=1, savetime=save_time, player=jogador)

                if save2_rect.collidepoint(mouseposition) and self.savegame_menu == True:
                    save_time = datetime.datetime.now()
                    self.savegame(tela, mouse_rect, mouse_button, number=2, savetime=save_time, player=jogador)

                #SELECIONAR OPÇÃO DO LOADGAME
                if load1_rect.collidepoint(mouseposition) and self.loadgame_menu == True:
                    self.loadgame(tela, mouse_rect, mouse_button, number= 1, player=jogador)

                if load2_rect.collidepoint(mouseposition) and self.loadgame_menu == True:
                    self.loadgame(tela, mouse_rect, mouse_button, number= 2, player=jogador)

        #Definir mouse do jogo
        mouse_rect.center = pygame.mouse.get_pos()
        tela.blit(mouse_button, mouse_rect)
        pygame.display.update()

    def loadgame(self, tela, mouse_rect, mouse_button, number, player):
        ##########DAR UM SINAL DE QUE O CLIQUE FUNCIONOU
        try:
            dados_jogo = {}
            with open(f'save{number}.dat','rb') as arquivo:
                dados_jogo = pickle.load(arquivo)
                v.score = dados_jogo['score']
                v.score_aranha = dados_jogo['score_aranha']
                v.score_lobo = dados_jogo['score_lobo']
                v.score_urso = dados_jogo['score_urso']
                v.score_rainha_aranha = dados_jogo['score_rainha_aranha']
                v.quest_em_progresso = dados_jogo['quest_em_progresso']
                v.quest_num = dados_jogo['quest_num']
                v.mob_atual = dados_jogo['mob_atual']
                v.score_atual_quest = dados_jogo['score_atual_quest']
                v.score_alvo_quest = dados_jogo['score_alvo_quest']
                v.mob_aranha_exp = dados_jogo['mob_aranha_exp']
                v.mob_aranha_level = dados_jogo['mob_aranha_level']
                v.mob_lobo_exp = dados_jogo['mob_lobo_exp']
                v.mob_lobo_level = dados_jogo['mob_lobo_level']
                v.mob_urso_exp = dados_jogo['mob_urso_exp']
                v.mob_urso_level = dados_jogo['mob_urso_level']
                v.mob_aranha_rainha_exp = dados_jogo['mob_aranha_rainha_exp']
                v.mob_aranha_rainha_level = dados_jogo['mob_aranha_rainha_level']
                v.axe_equip = dados_jogo['axe_equip']
                v.Norte = dados_jogo['Norte']
                v.Sul = dados_jogo['Sul']
                v.Leste =  dados_jogo['Leste']
                v.Oeste = dados_jogo['Oeste']
                player.rect.x = dados_jogo['rect.x']
                player.rect.y = dados_jogo['rect.y']
                player.nivel = dados_jogo['nivel']
                player.exp = dados_jogo['exp']
                player.prox_exp = dados_jogo['prox_exp']
                player.health = dados_jogo['health']
                player.max_health = dados_jogo['max_health']
                player.inventario = dados_jogo['inventario']                

        except FileNotFoundError:
            pass #Mostrar que não há save para carregar
        #imagem cinza do load e som de erro?
                           

            
        
    def savegame(self, tela, mouse_rect, mouse_button, number, savetime, player):
        ##########DAR UM SINAL DE QUE O CLIQUE FUNCIONOU
        dados_jogo = { 'score': v.score,
                       'score_aranha': v.score_aranha,
                       'score_lobo': v.score_lobo,
                       'score_urso': v.score_urso,
                       'score_rainha_aranha': v.score_rainha_aranha,
                       'quest_em_progresso': v.quest_em_progresso,
                       'quest_num': v.quest_num,
                       'mob_atual': v.mob_atual,
                       'score_atual_quest': v.score_atual_quest,
                       'score_alvo_quest': v.score_alvo_quest,
                       'mob_aranha_exp': v.mob_aranha_exp,
                       'mob_aranha_level': v.mob_aranha_level,
                       'mob_lobo_exp': v.mob_lobo_exp,
                       'mob_lobo_level': v.mob_lobo_level,
                       'mob_urso_exp': v.mob_urso_exp,
                       'mob_urso_level': v.mob_urso_level,
                       'mob_aranha_rainha_exp': v.mob_aranha_rainha_exp,
                       'mob_aranha_rainha_level': v.mob_aranha_rainha_level,
                       'axe_equip': v.axe_equip,
                       'Norte': v.Norte,
                       'Sul': v.Sul,
                       'Leste': v.Leste,
                       'Oeste': v.Oeste,
                       'rect.x': player.rect.x,
                       'rect.y': player.rect.y,
                       'nivel': player.nivel,
                       'exp': player.exp,
                       'prox_exp': player.prox_exp,
                       'health': player.health,
                       'max_health': player.max_health,
                       'inventario': player.inventario,
                       'save_time': savetime                       
                       }
        with open(f'save{number}.dat','wb') as arquivo:
            pickle.dump(dados_jogo,arquivo)
            ##########DAR UM SINAL DE QUE O SAVE FUNCIONOU

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
            self.animation = 0.0
            self.mask = pygame.mask.from_surface(self.image)#Cria a mask pra detectar colisão
            
        def criar(self, x, y, direction,level):
            #Definição de posição do ataque
            self.rect.x = x
            self.rect.y = y

            #Outras definições
            self.speed = 15
            self.direction = direction
            self.level = level
            self.dano = 100
            
        def equipamentos(self):
            pass
        #Se equipamento lvl 1 --> dano = 1
        #Se equipamento lvl 10 --> dano = x
        #Se equipamento lvl 50 --> dano = 1000
            
        def update(self, grupo_sprites, player, npc, inimigo, arvore, damage_show, delta_time, tela, font, grupo_obstaculos, equipamentos):

            self.mask = pygame.mask.from_surface(self.image) #Atualiza a mask
            
            if self.level == 1:
                self.dano = 1
                
            if self.level == 2:
                self.dano = 1
                
            elif self.level > 2:
                self.dano = int(round((self.level*0.5), 1))
                
            # Movimenta o ataque na direção em que o jogador está se movendo
            if self.direction == 'left':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.x -= self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\left.png')
                    
            elif self.direction == 'right':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.x += self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\right.png')
                    
            elif self.direction == 'up':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.y -= self.speed
                    self.rect.x = player.rect.x - 10
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\up.png')
                    
            elif self.direction == 'down':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.y += self.speed
                    self.rect.x = player.rect.x - 10
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\down.png')

            elif self.direction == 'rightdown':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.y += self.speed
                    self.rect.x += self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\rightdown.png')
                    
            elif self.direction == 'rightup':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.y -= self.speed
                    self.rect.x += self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\rightup.png')
                    
            elif self.direction == 'leftdown':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.y += self.speed
                    self.rect.x -= self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\leftdown.png')
                    
            elif self.direction == 'leftup':
                    if v.Norte == 3 and v.Oeste == 3:
                        self.image = pygame.image.load(r'Graphics\Character\Ataque\vazio.png')
                    self.rect.y -= self.speed
                    self.rect.x -= self.speed
                    self.image = pygame.image.load(r'Graphics\Character\Ataque\leftup.png')

###############################################
                    
            if pygame.sprite.spritecollide(self,npc,False):
                npc_hit = pygame.sprite.spritecollide(self,npc,False)
                for npc in npc_hit:
                    self.kill()
                    npc.update(tela,font, equipamentos, player)
                    

###############################################
                
            #verifica se o ataque corta a arvore
            if pygame.sprite.spritecollide(self, arvore, False):
                corte_arvore = pygame.sprite.spritecollide(self, arvore, False)
                if corte_arvore:
                    for arvore in corte_arvore:
                        arvore.health -= self.dano
                        if arvore.health <= 0:                            
                            ####################################GERAR AQUI UMA ANIMAÇÃO DE ITEM
                            player.inventario[arvore.tipo_tronco] += random.randrange(arvore.min_quant_tronco,arvore.quant_tronco)
                            arvore.kill()
                            
                            randomizando = random.randrange(0,10)
                            if randomizando <= 4:
                                for sprites in corte_arvore:
                                    inimigox = sprites.old_rect.x
                                    inimigoy = sprites.old_rect.y
                                    gerar_inimigo = Inimigos(inimigox,inimigoy)
                                    gerar_inimigo.tipo() #define o sprite quando o inimigo é criado, portanto usar junto com o init da class
                                    grupo_sprites.add(gerar_inimigo)
                                    grupo_obstaculos.add(gerar_inimigo)
                                    inimigo.add(gerar_inimigo)
                       
###############################################

            # Verifica colisão com os inimigos
            if pygame.sprite.spritecollide(self, inimigo, False):
                hit_enemies = pygame.sprite.spritecollide(self, inimigo, False, pygame.sprite.collide_mask)
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

                    if self.direction == 'rightdown':
                        enemy.rect.x += 2
                        enemy.rect.y += 2

                    if self.direction == 'rightup':
                        enemy.rect.x += 2
                        enemy.rect.y -= 2

                    if self.direction == 'leftdown':
                        enemy.rect.x -= 2
                        enemy.rect.y += 2

                    if self.direction == 'leftup':
                        enemy.rect.x -= 2
                        enemy.rect.y -= 2
                        
                    if enemy.health <= 0:
                        enemy.kill()                            
                        player.exp += enemy.valor_exp 
                        player.blit_exp = player.char_exp_gain_img #muda a imagem da barra de xp
                                    
                        if enemy.race == 'aranha':
                            v.mob_aranha_exp += 10
                            v.score_aranha += 1
                        if enemy.race == 'lobo':
                            v.mob_lobo_exp += 15
                            v.score_lobo += 1
                        if enemy.race == 'urso':
                            v.mob_urso_exp += 20
                            v.score_urso += 1
                        if enemy.race == 'aranha_rainha':
                            v.mob_rainha_aranha_exp += 50
                            v.score_aranha_rainha += 1
                        v.score = v.score_aranha + v.score_urso + v.score_lobo + v.score_rainha_aranha
            else:
                player.blit_exp = player.char_exp_img #retorna a imagem base da barra de xp

            # Remove o ataque da tela quando atinge o limite da distância                          
            player_pos = player.rect.center
            player_posxd = player_pos[0] + 7 #direita
            player_posyb = player_pos[1] + 7 #baixo
            player_posxe = player_pos[0] - 50 #esquerda
            player_posyc = player_pos[1] - 50 #cima
            if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                self.kill()

#############################################################################################################################################################################################################################################################################################################################################################################################################################################    

class HUD:
    def __init__(self,tela):
        pass

    def inventario(self,tela,personagem,fonte):
        #definindo o fundo do inventario
        fundo_inventario = pygame.image.load(r'Graphics\HUD\fundo.png')
        fundo_inventario.set_alpha(10)
        tela.blit(fundo_inventario,(0,0))

        #definindo os recursos do inventario
        recursos = {'troncos': pygame.image.load(r'Graphics\HUD\Inventario\tronco.png'),
                    'metais': pygame.image.load(r'Graphics\HUD\Inventario\metal.png'),
                    'tecidos': pygame.image.load(r'Graphics\HUD\Inventario\tecido.png'),
                    'couros': pygame.image.load(r'Graphics\HUD\Inventario\couro.png'),
                    'troncos1': pygame.image.load(r'Graphics\HUD\Inventario\tronco1.png'),
                    'troncos2': pygame.image.load(r'Graphics\HUD\Inventario\tronco2.png'),
                    'troncos3': pygame.image.load(r'Graphics\HUD\Inventario\tronco3.png'),
                    'troncos4': pygame.image.load(r'Graphics\HUD\Inventario\tronco4.png'),
                    'troncos5': pygame.image.load(r'Graphics\HUD\Inventario\tronco5.png'),
                    'metais1': pygame.image.load(r'Graphics\HUD\Inventario\metal1.png'),
                    'metais2': pygame.image.load(r'Graphics\HUD\Inventario\metal2.png'),
                    'metais3': pygame.image.load(r'Graphics\HUD\Inventario\metal3.png'),
                    'metais4': pygame.image.load(r'Graphics\HUD\Inventario\metal4.png'),
                    'tecidos1': pygame.image.load(r'Graphics\HUD\Inventario\tecido1.png'),
                    'tecidos2': pygame.image.load(r'Graphics\HUD\Inventario\tecido2.png'),
                    'tecidos3': pygame.image.load(r'Graphics\HUD\Inventario\tecido3.png'),
                    'tecidos4': pygame.image.load(r'Graphics\HUD\Inventario\tecido4.png'),
                    'couros1': pygame.image.load(r'Graphics\HUD\Inventario\couro1.png'),
                    'couros2': pygame.image.load(r'Graphics\HUD\Inventario\couro2.png'),
                    'couros3': pygame.image.load(r'Graphics\HUD\Inventario\couro3.png'),
                    'couros4': pygame.image.load(r'Graphics\HUD\Inventario\couro4.png'),
                    'pocao_pequena': pygame.transform.scale(pygame.image.load(r'Graphics\HUD\Inventario\pocao_pequena.png'),(30,30)),
                    'pocao_media': pygame.transform.scale(pygame.image.load(r'Graphics\HUD\Inventario\pocao_media.png'),(30,30)),
                    'pocao_grande': pygame.transform.scale(pygame.image.load(r'Graphics\HUD\Inventario\pocao_grande.png'),(30,30))
                    }
        
        #definindo os equipamentos do inventario
        axe = pygame.image.load(r'Graphics\HUD\Craft\axe_button.png') #########PROVISÓRIO precisa ser 100x100
        armor = pygame.image.load(r'Graphics\HUD\Craft\armor_button.png')  #########PROVISÓRIO precisa ser 100x100
        helmet = pygame.image.load(r'Graphics\HUD\Craft\helmet_button.png') #########PROVISÓRIO precisa ser 100x100

        #definindo os textos dos recursos
        posx_cont = 1
        posy_cont = 5
        for key in personagem.inventario:
            if not key == 'ouro' and not key == 'diamante' and not key == 'ouro_vermelho' and not key == 'ouro_negro':
                if not personagem.inventario[key] == 0:
                    quant_item = fonte.render(str(personagem.inventario[key]), True, (255,255,255))
                    
                    #blitando os recursos
                    if posx_cont > 1:
                        posx_image = (posx_cont*50) + (posx_cont*10)
                    else:
                        posx_image = (posx_cont*50)
                    posy_image = posy_cont*50
                    tela.blit(recursos[key],(posx_image,posy_image))
                    
                    #blitando as quantidades
                    if posx_cont > 1:
                        posx_text = (posx_cont*50) + 20 + (posx_cont*10)
                    else:
                        posx_text = (posx_cont*50) + 20
                    posy_text = posy_cont*50 + 20
                    tela.blit(quant_item,(posx_text,posy_text))          
                    if posy_cont > 9:
                        posy_cont = 5
                        posx_cont += 1
                    else:
                        posy_cont += 1
            else:
                #criar o ouro na tela do inventario aqui
                if not personagem.inventario['diamante'] == 0:
                    diamante = fonte.render(str(personagem.inventario['diamante']), True, (0,255,255))
                    diamante_icon = pygame.image.load(r'Graphics\HUD\Inventario\diamante.png')
                    diamante_icon = pygame.transform.scale(diamante_icon,(20,20))
                    tela.blit(diamante, (670,250))
                    tela.blit(diamante_icon, (640,253))
                    
                if not personagem.inventario['ouro_vermelho'] == 0:
                    ouro_vermelho = fonte.render(str(personagem.inventario['ouro_vermelho']), True, (255,0,0))
                    ouro_vermelho_icon = pygame.image.load(r'Graphics\HUD\Inventario\ouro_vermelho.png')
                    ouro_vermelho_icon = pygame.transform.scale(ouro_vermelho_icon,(20,20))
                    tela.blit(ouro_vermelho, (670,300))
                    tela.blit(ouro_vermelho_icon, (640,303))
                    
                if not personagem.inventario['ouro_negro'] == 0:
                    ouro_negro = fonte.render(str(personagem.inventario['ouro_negro']), True, (0,0,0))
                    ouro_negro_icon = pygame.image.load(r'Graphics\HUD\Inventario\ouro_negro.png')
                    ouro_negro_icon = pygame.transform.scale(ouro_negro_icon,(20,20))
                    tela.blit(ouro_negro, (670,350))
                    tela.blit(ouro_negro_icon, (640,353))
                            
                ouro = fonte.render(str(personagem.inventario['ouro']), True, (255,255,0))
                ouro_icon = pygame.image.load(r'Graphics\HUD\Inventario\ouro.png')
                ouro_icon = pygame.transform.scale(ouro_icon,(20,20))
                tela.blit(ouro, (670,200))
                tela.blit(ouro_icon, (640,203))
            

        #blitando os itens
        tela.blit(helmet,(450,200))
        tela.blit(armor,(450,300))
        tela.blit(axe,(350,300))

    def bussola(self,tela,fonte):
        bussola = pygame.image.load(r'Graphics\HUD\bussola.png') #Criar uma nova imagem de bussola, que condiz mais com o jogo? Talvez uma bussola tipo real, em pixel art?
        bussola.set_alpha(50)
        tela.fill((0,0,0))
        tela.blit(bussola, (0,0))

        #definindo a pos do personagem para a bussola
        #Norte
        norte_texto = fonte.render(str(v.Norte), True, (255,255,255))
        tela.blit(norte_texto, (400, 15))
        #Sul
        sul_texto = fonte.render(str(v.Sul), True, (255,255,255))
        tela.blit(sul_texto, (400, 560))
        #Leste
        leste_texto = fonte.render(str(v.Leste), True, (255,255,255))
        tela.blit(leste_texto, (660, 300))
        #Oeste
        oeste_texto = fonte.render(str(v.Oeste), True, (255,255,255))
        tela.blit(oeste_texto, (130, 320))

    def quest(self, tela, fonte, personagem): ###### Quest principal - armazenada no personagem
        quest = pygame.image.load(r'Graphics\HUD\Quests\fundoquest.png')
        quest.set_alpha(50)
        tela.blit(quest, (0,0))

        if v.quest_em_progresso == True:
            escrever_dialogo("PROGRESS", (325,150), fonte, tela)
            escrever_dialogo("You have to kill: ", (300,200), fonte, tela)
            escrever_dialogo(str(v.score_alvo_quest), (300,225), fonte, tela)
            escrever_dialogo(v.mob_atual, (300,250), fonte, tela)
            escrever_dialogo("You killed: ", (300,275), fonte, tela)
            score_real = 0
            if v.mob_atual == 'spiders':
                score_real = v.score_aranha - v.score_atual_quest              
            if v.mob_atual == 'wolfs':
                score_real = v.score_lobo - v.score_atual_quest
            if v.mob_atual == 'bears':
                score_real = v.score_urso - v.score_atual_quest
                
            if score_real >= v.score_alvo_quest :
                score_real = v.score_alvo_quest
            escrever_dialogo(str(score_real), (300,300), fonte, tela)
            
            #Criar lado esquerdo - MAIN QUEST
            
            #Lado direito da tela
            escrever_dialogo("Total score: ", (555,100), fonte, tela)
            escrever_dialogo(str(v.score),(555,120), fonte, tela)
            
            if v.score_aranha > 0:
                escrever_dialogo("Spiders killed: ", (555,150), fonte, tela)
                escrever_dialogo(str(v.score_aranha), (555,170), fonte, tela)
                
            if v.score_lobo > 0:
                escrever_dialogo("Wolfs killed: ", (555,200), fonte, tela)
                escrever_dialogo(str(v.score_lobo), (555,220), fonte, tela)
            if v.score_urso > 0:
                escrever_dialogo("Bears killed: ", (555,250), fonte, tela)
                escrever_dialogo(str(v.score_urso), (555,270), fonte, tela)
                
            if v.score_rainha_aranha > 0:
                escrever_dialogo("Spider Queens killed: ", (555,300), fonte, tela)
                escrever_dialogo(str(v.score_rainha_aranha), (555,320), fonte, tela)
                
            
        else:
            escrever_dialogo("You don't have any quests.", (275,150), fonte, tela)

            #Criar lado esquerdo - MAIN QUEST
            
            #Lado direito da tela
            escrever_dialogo("Total score: ", (555,100), fonte, tela)
            escrever_dialogo(str(v.score),(555,120), fonte, tela)
            
            if v.score_aranha > 0:
                escrever_dialogo("Spiders killed: ", (555,150), fonte, tela)
                escrever_dialogo(str(v.score_aranha), (555,170), fonte, tela)
                
            if v.score_lobo > 0:
                escrever_dialogo("Wolfs killed: ", (555,200), fonte, tela)
                escrever_dialogo(str(v.score_lobo), (555,220), fonte, tela)
            if v.score_urso > 0:
                escrever_dialogo("Bears killed: ", (555,250), fonte, tela)
                escrever_dialogo(str(v.score_urso), (555,270), fonte, tela)
                
            if v.score_rainha_aranha > 0:
                escrever_dialogo("Spider Queens killed: ", (555,300), fonte, tela)
                escrever_dialogo(str(v.score_rainha_aranha), (555,320), fonte, tela)
        



        
        pygame.display.update()

        #####colocar os scores de cada mob morto no total, no topo e embaixo as quests ativas*************** Vou precisar terminar o sistema de quest antes disso111111111111111111111111111111111111111111111111111111111111111111111

########################################################################################################################################################################################################################################

class Arvore(pygame.sprite.Sprite):
    def __init__(self, pos, tela, nivel=1):
            super().__init__()
            self.nivel = nivel
            self.normalimage = pygame.image.load(fr'Graphics\Mapa\Arvores\arvore{self.nivel}.png').convert_alpha()
            self.hitimage = pygame.image.load(fr'Graphics\Mapa\Arvores\arvore_hit{self.nivel}.png').convert_alpha()
            self.image = self.normalimage
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.old_rect = self.rect.copy()
            self.type = 'arvore'
            self.tipo_tronco = 'troncos'
            self.quant_tronco = 2
            self.min_quant_tronco = 1
            self.health = 1
            self.last_health = self.health
            self.animation = 0.0

    def atualizar_raridade(self):
        if self.nivel == 1:
            self.health = 1
        if self.nivel > 1:
            self.health = self.nivel*5
            self.last_health = self.health
            if self.nivel == 5:
                self.tipo_tronco = 'troncos_raros'
                self.quant_tronco = 5
                self.min_quant_tronco = 2
            elif self.nivel == 10:
                self.tipo_tronco = 'troncos_encantados'
                self.quant_tronco = 10
                self.min_quant_tronco = 5
            elif self.nivel == 50:
                self.tipo_tronco = 'troncos_lendarios'
                self.quant_tronco = 20
                self.min_quant_tronco = 5
            else:                
                self.tipo_tronco = 'troncos'
                self.quant_tronco = 5
                self.min_quant_tronco = 1

    def update(self, delta_time):
        
        if self.last_health > self.health:
            self.animation += delta_time
            self.image = self.hitimage
            
            if self.animation >= 0.1:
                self.last_health = self.health
                self.animation = 0.0
        else:
            self.image = self.normalimage
            
########################################################################################################################################################################################################################################

class Mapa_jogo():
    def __init__(self):
        self.mapa_atual = pygame.image.load(r'Graphics\Mapa\floresta_negra.png') ######
        
    def mudar_mapa(self, npc_grupo, inimigo_grupo, arvore_grupo):
        
        if not v.Norte == 3 and not v.Oeste == 3:
            for npc in npc_grupo:
                npc.kill()
        if v.Norte == 3 and v.Oeste == 3:
            self.mapa_atual = pygame.image.load(r'Graphics\Mapa\mapa_cidade1.png')
            #cria os NPCs
            npc1 = NPC((100,100),pygame.image.load(r'Graphics\NPC\npc1.png').convert_alpha(),quest=True)
            npc_grupo.add(npc1)
            #criar as casas e os muros
            
            #PARA CRIAR UM NPC:
            #pos = (100,100)
            #image = pygame.image.load(r'Graphics\NPC\npc1.png').convert_alpha()
            #criar_npc = NPC(pos,image) - esse é um ex de guarda, acrescentar o True para qual coisa o npc vai fazer, se não será guarda
            #npc_grupo.add(criar_npc)
        else:
            self.mapa_atual = pygame.image.load(r'Graphics\Mapa\floresta_negra.png')
            
            
        for inimigo in inimigo_grupo:
            inimigo.kill()
            
        for arvore in arvore_grupo:
            arvore.kill()

        ##### DEFINIR AQUI ONDE ESTÁ O PERSONAGEM, CHECAR COORDS PARA CONFIGURAR A VARIAVEL in_city  ENTRE OUTRAS FUNÇÕES

########################################################################################################################################################################################################################################

def gerar_arvore(player_pos,arvore_grupo, grupo_obstaculo, tela):
    #Define a o nivel das arvores conforme a localização do player
    #if pos_player >= Norte = 50, Sul = 50, Leste = 50, Oeste = 50:
        #chance_raridade = 50 #numero limite da aleatoridade
        #probabilidade_raridade = 10 #gerar arvore rara se aleatoridade for menor que esse numero
        #raridade = 3 #nivel que a arvore receberá
    #else:
    chance_raridade = 100
    probabilidade_raridade = 1
    raridade = 2
    
    num_arvores = random.randrange(15,50)
    if v.Norte == 3 and v.Oeste == 3:
        num_arvores = 0
    while num_arvores > 0:
        coordx = random.randint(0,750)
        coordy = random.randint(0,550)
        colliderect = pygame.Rect(300,200,200,200) #area do centro vazia
        collidehud = pygame.Rect(0,0,800,75) #topo do hud
        if not colliderect.collidepoint(coordx,coordy) and not collidehud.collidepoint(coordx,coordy) and not player_pos.collidepoint(coordx,coordy):
            criar_arvores = True
            if v.Norte == 2 and v.Oeste == 3:
                #mapa debaixo da cidade, colisao na area superior para o muro
                collidetop = pygame.Rect(0,0,800,175)
                if collidetop.collidepoint(coordx,coordy):
                    criar_arvores = False
                else:
                    criar_arvores = True
            if v.Norte == 3 and v.Oeste == 2:
                pass #mapa a direita da cidade, colisao na area esquerda para muro e guardas################################################111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
            if v.Norte == 4 and v.Oeste == 3:
                pass #mapa de cima da cidade, colisao na area inferior para o muro
            if v.Norte == 3 and v.Oeste == 4:
                pass #mapa a esquerda da cidade, colisao na area direita para muro e guardas

            if criar_arvores:
                arvore_rara = random.randint(0,chance_raridade)
                if arvore_rara <= probabilidade_raridade:
                    arvore1 = Arvore((coordx,coordy),tela,nivel=raridade)
                    arvore1.atualizar_raridade()
                    arvore_grupo.add(arvore1)
                    grupo_obstaculo.add(arvore1)
                    num_arvores -= 1
                else:
                    arvore1 = Arvore((coordx,coordy), tela)
                    arvore_grupo.add(arvore1)
                    grupo_obstaculo.add(arvore1)
                    num_arvores -= 1
    v.gerando_arvores = False

########################################################################################################################################################################################################################################

class Borda_topo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'Graphics\Mapa\bordas_horizontais.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 75

    def update(self, player_grupo, player, arvore_grupo, inimigo_grupo, mapa_jogo, npc_grupo):
        hit = pygame.sprite.spritecollide(self, player_grupo, False)
        for hits in hit:
            v.Norte += 1
            v.Sul -= 1
            player.rect.y = 540            
            for arvore in arvore_grupo:
                arvore.kill()
            for inimigo in inimigo_grupo:
                inimigo.kill()
            v.gerando_arvores = True
            self.passar_mapa(mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo)

    def passar_mapa(self, mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        pygame.mixer.Sound.set_volume(som_passar_mapa,0.05) #provisório
        pygame.mixer.Sound.play(som_passar_mapa)#provisório
        '''
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
        '''
        mapa_jogo.mudar_mapa(npc_grupo, inimigo_grupo, arvore_grupo)
################################################## BORDA TOPO ######################################################

################################################## BORDA BAIXO #####################################################
class Borda_baixo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'Graphics\Mapa\bordas_horizontais.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 590

    def update(self, player_grupo, player, arvore_grupo, inimigo_grupo, mapa_jogo, npc_grupo):
        hit = pygame.sprite.spritecollide(self, player_grupo, False)
        for hits in hit:
            v.Sul += 1
            v.Norte -= 1
            player.rect.y = 85            
            for arvore in arvore_grupo:
                arvore.kill()
            for inimigo in inimigo_grupo:
                inimigo.kill()
            v.gerando_arvores = True
            self.passar_mapa(mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo)

    def passar_mapa(self, mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        pygame.mixer.Sound.set_volume(som_passar_mapa,0.05) #provisório
        pygame.mixer.Sound.play(som_passar_mapa)#provisório
        '''
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
        '''
        mapa_jogo.mudar_mapa(npc_grupo, inimigo_grupo, arvore_grupo)
################################################## BORDA BAIXO #####################################################

################################################## BORDA ESQUERDA ##################################################
class Borda_esquerda(pygame.sprite.Sprite):                
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'Graphics\Mapa\bordas_verticais.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, player_grupo, player, arvore_grupo, inimigo_grupo, mapa_jogo, npc_grupo):
        hit = pygame.sprite.spritecollide(self, player_grupo, False)
        for hits in hit:
            v.Oeste += 1
            v.Leste -= 1
            player.rect.x = 740            
            for arvore in arvore_grupo:
                arvore.kill()
            for inimigo in inimigo_grupo:
                inimigo.kill()
            v.gerando_arvores = True
            self.passar_mapa(mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo)

    def passar_mapa(self, mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        pygame.mixer.Sound.set_volume(som_passar_mapa,0.05) #provisório
        pygame.mixer.Sound.play(som_passar_mapa)#provisório
        '''
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
        '''
        mapa_jogo.mudar_mapa(npc_grupo, inimigo_grupo, arvore_grupo)
                
################################################## BORDA ESQUERDA ##################################################

################################################## BORDA DIREITA ###################################################
class Borda_direita(pygame.sprite.Sprite):            
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'Graphics\Mapa\bordas_verticais.png')
        self.rect = self.image.get_rect()
        self.rect.x = 790
        self.rect.y = 0

    def update(self, player_grupo, player, arvore_grupo, inimigo_grupo, mapa_jogo, npc_grupo):
        hit = pygame.sprite.spritecollide(self, player_grupo, False)
        for hits in hit:
            v.Leste += 1
            v.Oeste -= 1
            player.rect.x = 10            
            for arvore in arvore_grupo:
                arvore.kill()
            for inimigo in inimigo_grupo:
                inimigo.kill()
            v.gerando_arvores = True
            self.passar_mapa(mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo)

    def passar_mapa(self, mapa_jogo, npc_grupo, inimigo_grupo, arvore_grupo):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        pygame.mixer.Sound.set_volume(som_passar_mapa,0.05) #provisório
        pygame.mixer.Sound.play(som_passar_mapa)#provisório
        '''
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
        '''
        mapa_jogo.mudar_mapa(npc_grupo, inimigo_grupo, arvore_grupo)
            
################################################## BORDA DIREITA ###################################################

########################################################################################################################################################################################################################################

def escrever_dialogo(texto,pos,fonte,tela,cor=(255,255,255)):
    texto_render = fonte.render(texto,1,cor)
    tela.blit(texto_render,pos)

def gerar_quant_mobs(x,y):
    quant = random.randrange(x,y)
    return quant

def escolher_mob():
    grupo_mobs = ['spiders','wolfs','bears']
    mob = random.randrange(0,3)
    return grupo_mobs[mob]

########################################################################################################################################################################################################################################

class NPC(pygame.sprite.Sprite):
    def __init__(self,pos,image,quest=False,craft=False,loja=False):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.type = 'npc'
            self.quest = quest
            self.craft = craft
            self.loja = loja
            self.NPChud = pygame.image.load(r'Graphics\HUD\fundo.png')
            self.NPChud.set_alpha(50)
            self.som_hey = pygame.mixer.Sound(r'sounds\saudacao.mp3')
            self.som_wcidfy = pygame.mixer.Sound(r'sounds\what_can_i_do_for_you.mp3')
            self.grupo_som = [self.som_hey,self.som_wcidfy]
            
    def quests(self,tela,fonte):
        random_som = random.randrange(0,2)
        pygame.mixer.Sound.set_volume(self.grupo_som[random_som],0.05)
        pygame.mixer.Sound.play(self.grupo_som[random_som])
        quest_on = True
        mob_quest = gerar_quant_mobs(10,80)
        mob = escolher_mob()
        while quest_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if v.quest_em_progresso == False:
            ##################################################REPETITIVE QUEST########################################################### 
                if v.quest_num == 0:
                    mob = 'spiders'
                    escrever_dialogo("Please, kill " + str(mob_quest) + " " + str(mob) + " for me", (250,400), fonte, tela)#Atualizar pos disso!
                   
                if v.quest_num >= 1:
                    escrever_dialogo("Please, kill " + str(mob_quest) + " " + str(mob) + " for me", (250,100), fonte, tela)#Atualizar pos disso!
            ##################################################REPETITIVE QUEST########################################################### 

                tela.blit(self.NPChud, (0,0))
                escrever_dialogo("Press 'Y' to accept", (250,450), fonte, tela)#Atualizar pos disso!
                escrever_dialogo("Press 'N' to exit", (250,475), fonte, tela)#Atualizar pos disso!
                pygame.display.update()
                
                
                if pygame.key.get_pressed()[pygame.K_y] == True:
                    v.quest_em_progresso = True
                    if mob == 'spiders': #Preciso ajeitar isso aqui
                        v.score_atual_quest = v.score_aranha
                        v.mob_atual = 'spiders'
                        v.score_alvo_quest = mob_quest
                    #elif mob == 'wolfs':
                        #v.score_atual_quest = v.score_lobo
                        #v.mob_atual = 'wolfs'
                        #v.score_alvo_quest = mob_quest
                    #elif mob == 'bears':
                        #v.score_atual_quest = v.score_urso
                        #v.mob_atual = 'bears'
                        #v.score_alvo_quest = mob_quest
                    quest_on = False
                        
                if pygame.key.get_pressed()[pygame.K_n] == True:
                    quest_on = False

                        
            if v.quest_em_progresso == True:
                tela.blit(self.NPChud, (0,0))
                pygame.display.update()                
                
                if v.mob_atual == 'spiders':
                    if v.score_aranha - v.score_atual_quest >= v.score_alvo_quest:
                        escrever_dialogo("Thank you so much!", (250,100), fonte, tela)#Atualizar pos disso!
                        escrever_dialogo("Here is your reward: ", (250,125), fonte, tela)#Atualizar pos disso!
                        escrever_dialogo("Press 'Y' to continue", (250,475), fonte, tela) #Atualizar pos disso!
                        #### BLITAR RECOMPENSA AQUI
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            quest_on = False
                            v.quest_num += 1
                            v.quest_em_progresso = False
                    else:
                        escrever_dialogo("Oops, you didn't finish the quest!", (250,100), fonte, tela) #Atualizar pos disso!
                        escrever_dialogo("Press 'Y' to continue", (250,475), fonte, tela)     #Atualizar pos disso!                                            
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            quest_on = False
                                            
                #elif v.mob_atual == 'wolfs':
                    #if v.score_lobo - v.score_atual_quest >= v.score_alvo_quest:
                     #   quests.escrever_dialogo("Thank you so much!", (250,100))
                      #  quests.escrever_dialogo("Here is your reward: ", (250,125))
                       # quests.escrever_dialogo("Press 'Y' to continue", (250,475))
                        ###BLITAR AQUI A RECOMPENSA
                        #pygame.display.update()
                        #if pygame.key.get_pressed()[pygame.K_y] == True:
                        #    quest_on = False
                        #    v.quest_num += 1
                        #    v.quest_em_progresso = False
                    #else:
                    #    quests.escrever_dialogo("Oops, you didn't finish the quest!", (250,100))
                    #    quests.escrever_dialogo("Press 'Y' to continue", (250,475))                                                 
                    #    pygame.display.update()
                    #    if pygame.key.get_pressed()[pygame.K_y] == True:
                    #        quest_on = False

                #elif v.mob_atual == 'bears':
                   # if v.score_urso - v.score_atual_quest >= v.score_alvo_quest:
                    #    quests.escrever_dialogo("Thank you so much!", (250,100))
                     #   quests.escrever_dialogo("Here is your reward: ", (250,125))
                      #  quests.escrever_dialogo("Press 'Y' to continue", (250,475)) 
                        ###BLITAR AQUI A RECOMPENSA
                      #  pygame.display.update()
                       # if pygame.key.get_pressed()[pygame.K_y] == True:
                        #    pygame.display.update()
                         #   quest_on = False
                          #  v.quest_num += 1
                           # v.quest_em_progresso = False
                    #else:
                     #   quests.escrever_dialogo("Oops, you didn't finish the quest!", (250,100))
                      #  quests.escrever_dialogo("Press 'Y' to continue", (250,475))                                                 
                       # pygame.display.update()
                        #if pygame.key.get_pressed()[pygame.K_y] == True:
                         #   quest_on = False
                            
###########################################################################
        
    def crafts(self,tela, fonte, equipamentos, player):
        random_som = random.randrange(0,2)
        pygame.mixer.Sound.set_volume(self.grupo_som[random_som],0.05)
        pygame.mixer.Sound.play(self.grupo_som[random_som])
        craft_on = True

        #definição dos niveis de equipamentos
        #exemplo para o axe:
        #if nv1 = 1 troncos e 1 metais
        #if nv2 = 5 troncos e 10 metais
        #if nv3 = 15 troncos e 20 metais       

        while craft_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #criar as infos aqui
            #cores dos botões
            cor_botao_head = (0,0,0)
            cor_botao_armor = (0,0,0)
            cor_botao_axe = (0,0,0)
            cor_botao_base = (150,0,0) ########### DEFINIR COR DO BOTAO
            cor_botao_cima = (100,0,0)
            cor_botao_clique = (0,100,0)
            cor_bloqueado = (0,0,0)
            
            tela.blit(self.NPChud, (0,0))
            
            botao_head_img = pygame.image.load(r'graphics/helmet_button.png')
            botao_armor_img = pygame.image.load(r'graphics/armor_button.png')
            botao_axe_img = pygame.image.load(r'graphics/axe_button.png')
            
            escrever_dialogo("Press 'ESC' to exit", (250,450), fonte, tela)
            
            botao_head = pygame.Rect(250,120,50,50) ##### DEFINIR MELHOR POSICAO (posx,posy) E TAMANHO (altura,largura)
            botao_armor = pygame.Rect(350,120,50,50)
            botao_axe = pygame.Rect(450,120,50,50)
            
            
            #if v.troncos >= 1: #verificar requisitos conforme o nivel e tudo mais. Estabelecer através de variaveis que vão verificar o mesmo que vai ser blitado na tela
                #cor_botao_head = cor_botao_base
            #else:
                #cor_botao_head = cor_bloqueado
                
            #if v.tecidos >= 1:
                #cor_botao_armor = cor_botao_base
            #else:
                #cor_botao_armor = cor_bloqueado
                
            #if v.metais >= 1:
                #cor_botao_axe = cor_botao_base
            #else:
                #cor_botao_axe = cor_bloqueado

            #troncos, tecidos, metais, couros
            
            #####TESTAR COLISAO COM MOUSE PRA ALTERAR FUNCOES DO BOTAO            
            '''mousepos = pygame.mouse.get_pos()
            if pygame.key.get_pressed()[pygame.K_h] == True:
                    if v.troncos >= 1:
                        cor_botao_head = cor_botao_clique
            if botao_head.collidepoint(mousepos) == True:
                cor_botao_head = cor_botao_cima
                if pygame.mouse.get_pressed() == (1,0,0):
                    if v.troncos >= 1:
                        cor_botao_head = cor_botao_clique
                        pass #verifica requisito de evolucao de equipamento e realiza a evolução se estiver OK.

            if pygame.key.get_pressed()[pygame.K_a] == True:
                    if v.troncos >= 1:
                        cor_botao_armor = cor_botao_clique                        
            if botao_armor.collidepoint(mousepos) == True:
                cor_botao_armor = cor_botao_cima
                if pygame.mouse.get_pressed() == (1,0,0):
                    if v.troncos >= 1:
                        cor_botao_armor = cor_botao_clique                        
                        pass #verifica requisito de evolucao de equipamento e realiza a evolução se estiver OK.

            if pygame.key.get_pressed()[pygame.K_w] == True:
                    if v.troncos >= 1:
                        cor_botao_axe = cor_botao_clique
            if botao_axe.collidepoint(mousepos) == True:
                cor_botao_axe = cor_botao_cima
                if pygame.mouse.get_pressed() == (1,0,0):
                    if v.troncos >= 1:
                        cor_botao_axe = cor_botao_clique
                        pass #verifica requisito de evolucao de equipamento e realiza a evolução se estiver OK.'''
                
            pygame.draw.rect(tela,cor_botao_head,botao_head)
            pygame.draw.rect(tela,cor_botao_armor,botao_armor)
            pygame.draw.rect(tela,cor_botao_axe,botao_axe)
            
            tela.blit(botao_head_img,(250,120))
            tela.blit(botao_armor_img,(350,120))
            tela.blit(botao_axe_img,(450,120))
            
            pygame.display.update()
            if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
                craft_on = False

            #criar janela do craft
            #criar botões (criar, encantar, desencantar, rebaixar)
            #criar "animação" do botão ao passar o mouse
            #ao lado dos botões deve aparecer o tipo de recursos e a quantidade que precisa para realizar a ação
                #verifica se há a quantidade de recursos disponíveis no inventario, caso negativo, aparecer em vermelho os recursos que não são suficientes.
            #fazer verificação dos níveis dos equipamentos antes de poder tomar qualquer ação aqui
            #Criar uma janela similar ao inventario, com icones que lembrem os equipamentos para que ao selecionar o equipamento, apareçam as 4 opções de botões?
                #ou cada botão irá aparecer no equipamento na tela e abaixo aparecerá os recursos para fazer cada ação ?
                #testar as duas formas 

            #criar aqui o sistema de craft
        
        #copiar do HUD (inventario), dar decisão para o player entre LOJA e CRAFT, cada um com sua função especifica.
    #criar craft aqui
        #Se craftar, alterar o equipamento no gamehud.(nome do equip).
        #Alterar Dano e HP do personagem quando alterar equips para mais fortes

###########################################################################

    def loja(self, player):
        pass
        
    def update(self,tela, fonte, equipamentos, player):
        if self.quest == True and self.craft == False and self.loja == False:
            self.quests(tela, fonte)
        if self.craft == True and self.quest == False and self.loja == False:
            self.crafts(tela, fonte,equipamentos, player)
        if self.craft == False and self.quest == False and self.loja == True:
            self.loja(player)
        if self.craft == False and self.quest == False and self.loja == False:
            pass
        ######CRIAR PERGUNTA ANTES DE CONTINUAR - se loja, craft ou quest
        if self.craft == True and self.quest == True and self.loja == False:
            self.quests(tela, fonte)
            self.crafts(tela, fonte, equipamentos, player)
        if self.craft == True and self.quest == False and self.loja == True:
            self.loja(player)
            self.craft(tela, fonte, equipamentos, player)
        if self.craft == False and self.quest == True and self.loja == True:
            self.loja(player)
            self.quest(tela, fonte)
        if self.craft == True and self.quest == True and self.loja == True:
            self.loja(player)
            self.craft(tela, fonte, equipamentos, player)
            self.quest(tela, fonte) 

########################################################################################################################################################################################################################################

#
