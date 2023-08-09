import pygame, random, sys
import var as v
import muros
import quests
import pickle


#imagem npcs
npc1 = pygame.image.load(r'graphics/npc1.png').convert_alpha()
npc2 = pygame.image.load(r'graphics/npc2.png').convert_alpha()
npc3 = pygame.image.load(r'graphics/npc3.png').convert_alpha()
guarda1  = pygame.image.load(r'graphics/guarda1.png').convert_alpha()

#Musicas e sons
pygame.mixer.init()

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            self.image = pygame.image.load(r'graphics/char.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = v.posinitix
            self.rect.y = v.posinitiy
            self.old_rect = self.rect.copy()
            self.max_health = 100
            self.health = 100
            self.direction = 'right'
            self.dir = pygame.math.Vector2()
            self.speed = 2
            self.obstaculo = v.colisao_grupo
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.exp = v.exp
            self.level = 1

    def levelup(self):
        calc_lvlup = self.level * 100
        lvlup_cond = self.exp / calc_lvlup
        if lvlup_cond >= 1:
            som_lvl_up = pygame.mixer.Sound(r'sounds\lvlup.mp3')
            pygame.mixer.Sound.set_volume(som_lvl_up,0.1)
            pygame.mixer.Sound.play(som_lvl_up)
            #mostrar tela de lvlup
            lvlup1 = pygame.image.load(r'graphics/efeito_LVLUP1.png').convert_alpha()
            lvlup2 = pygame.image.load(r'graphics/efeito_LVLUP1.png').convert_alpha()
            lvlup3 = pygame.image.load(r'graphics/efeito_LVLUP1.png').convert_alpha()
            lvlup_group = [lvlup1,lvlup2,lvlup3]
            tamanho = (len(lvlup_group)) -1

            ultima_att = pygame.time.get_ticks()
            animacao_cd = 50
            frame = 0
            while frame <= tamanho:
                v.tela.blit(lvlup_group[frame],(self.rect.x,self.rect.y))
                pygame.display.flip()
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - ultima_att >= animacao_cd:
                    frame += 1
                    
            self.level += 1
            v.level = self.level
            v.exp = 0
            self.max_health += v.score *2
            self.health = self.max_health
        

    def equipamento(self):
            self.image = pygame.image.load(r'graphics/charequipado.png').convert_alpha()
            v.equipamento = True

    def usar_pocao(self):
        pass

    def collision(self,direction):
            collision_sprites = pygame.sprite.spritecollide(self,self.obstaculo,False)
            if collision_sprites:
                if direction == 'horizontal':
                    for sprite in collision_sprites:
                        if sprite.type == 'monstro':
                            self.health -= sprite.dano
                        if sprite.type == 'arvore':
                            pass
                        if sprite.type == 'npc':
                            pass
                        if sprite.type == 'parede':
                            pass
                        # colisão na direita
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            self.rect.right = sprite.rect.left
                            self.pos.x = self.rect.x
                            if sprite.type == 'monstro':
                                sprite.rect.x += 7

                        # colisão na esquerda
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.x
                            if sprite.type == 'monstro':
                                sprite.rect.x -= 7
                            

                if direction == 'vertical':
                    for sprite in collision_sprites:
                        if sprite.type == 'monstro':                            
                            self.health -= sprite.dano
                        if sprite.type == 'arvore':
                            pass
                        if sprite.type == 'npc':
                            pass
                        if sprite.type == 'parede':
                            pass
                        # colisão em baixo
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y
                            if sprite.type == 'monstro':
                                sprite.rect.y += 7

                        # colisão em cima
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.y
                            if sprite.type == 'monstro':
                                sprite.rect.y -= 7
     

    

    def entrada(self): #Verifica as teclas pressionadas para dar comandos
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:            
                self.dir.y = -1
                self.direction = 'up'
                if v.equipamento == True:
                    self.image = pygame.image.load(r'graphics/charequipadocima.png').convert_alpha()
                else:
                    self.image = pygame.image.load(r'graphics/charcima.png').convert_alpha()
            elif keys[pygame.K_DOWN]:
                self.dir.y = 1
                self.direction = 'down'
                if v.equipamento == True:
                    self.image = pygame.image.load(r'graphics/charequipadobaixo.png').convert_alpha()
                else:
                    self.image = pygame.image.load(r'graphics/charbaixo.png').convert_alpha()
            else:
                self.dir.y = 0

            if keys[pygame.K_RIGHT]:
                self.dir.x = 1
                self.direction = 'right'
                if v.equipamento == True:
                    self.image = pygame.image.load(r'graphics/charequipadodireita.png').convert_alpha()
                else:
                    self.image = pygame.image.load(r'graphics/chardireita.png').convert_alpha()
            elif keys[pygame.K_LEFT]:
                self.dir.x = -1
                self.direction = 'left'
                if v.equipamento == True:
                    self.image = pygame.image.load(r'graphics/charequipadoesquerda.png').convert_alpha()
                else:
                    self.image = pygame.image.load(r'graphics/charesquerda.png').convert_alpha()
            else:
                self.dir.x = 0

    def update(self):
            self.exp = v.exp
            self.levelup()
            self.old_rect = self.rect.copy()
            self.entrada()
            self.pos.x += self.dir.x * self.speed
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.pos.y += self.dir.y * self.speed
            self.rect.y = round(self.pos.y)
            self.collision('vertical')

        # Mantém o jogador dentro da v.tela
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > v.screen_width - 50:
                self.rect.x = v.screen_width - 50
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > v.screen_height - 50:
                self.rect.y = v.screen_height - 50

    def attack(self):
        if self.direction == 'right':
            ax = self.rect.x +25
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir,self.level)
            v.attack_grupo.add(attack)
        if self.direction == 'left':
            ax = self.rect.x
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir,self.level)
            v.attack_grupo.add(attack)
        if self.direction == 'up':
            ax = self.rect.x
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir,self.level)
            v.attack_grupo.add(attack)
        if self.direction == 'down':
            ax = self.rect.x
            ay = self.rect.y +10
            adir = self.direction
            attack = Attack(ax,ay,adir,self.level)
            v.attack_grupo.add(attack)
  

class Arvore(pygame.sprite.Sprite):
        def __init__(self,pos):
            super().__init__()
            self.image = pygame.image.load(r'graphics/arvore.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.type = 'arvore'


class Muro(pygame.sprite.Sprite):
        def __init__(self,pos):
            super().__init__()
            self.image = pygame.image.load(r'graphics/muro.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.type = 'parede'

class Casa(pygame.sprite.Sprite):
        def __init__(self,pos):
            super().__init__()
            self.image = pygame.image.load(r'graphics/casa.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.type = 'parede'

class Ferreiro(pygame.sprite.Sprite):
        def __init__(self,pos):
            super().__init__()
            self.image = pygame.image.load(r'graphics/ferreiro.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.pos = pos
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.type = 'parede'

class NPC(pygame.sprite.Sprite): ############################################################
    def __init__(self,pos,image,quest,craft):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.type = 'npc'
            self.quest = quest
            self.craft = craft
    def quests(self):
        som_hey = pygame.mixer.Sound(r'sounds\saudacao.mp3')
        som_wcidfy = pygame.mixer.Sound(r'sounds\what_can_i_do_for_you.mp3')
        grupo_som = [som_hey,som_wcidfy]
        random_som = random.randrange(0,2)
        pygame.mixer.Sound.set_volume(grupo_som[random_som],0.05)
        pygame.mixer.Sound.play(grupo_som[random_som])
        quest_on = True
        mob_quest = quests.gerar_quant_mobs(10,80)
        mob = quests.escolher_mob()
        while quest_on:########################################## (250,y) sendo que 250 é dentro do quest.png
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if v.quest_em_progresso == False: ########################### dif y - entre cada linha é 25
                if v.quest_num < 6 :
                    quests.escrever_dialogo(quests.dialogo_quest(), (250,100)) ### MUDAR ISSO AQUI PARA ESCREVER O DIALOGO COM QUEBRA DE LINHA

                    ##################################################MAIN QUEST DEF###########################################################
                    ################################################## ADICIONAR CUTSCENES PARA CADA QUEST! ###################################
                    if v.quest_num == 0:
                        mob = 'spiders'
                        quests.escrever_dialogo("Please, kill " + str(mob_quest) + " " + str(mob) + " for me", (250,400))
                        
                    ##################################################MAIN QUEST DEF###########################################################


                ##################################################REPETITIVE QUEST###########################################################        
                if v.quest_num >= 6:
                    quests.escrever_dialogo("Please, kill " + str(mob_quest) + " " + str(mob) + " for me", (250,100))
                ##################################################REPETITIVE QUEST########################################################### 
                                
                quest = pygame.image.load(r'graphics/quest_craft.png')
                quest.set_alpha(50)
                v.tela.blit(quest, (0,0))
                quests.escrever_dialogo("Press 'Y' to accept", (250,450))
                quests.escrever_dialogo("Press 'N' to exit", (250,475))
                pygame.display.update()
                
                
                if pygame.key.get_pressed()[pygame.K_y] == True:
                    v.quest_em_progresso = True
                    if mob == 'spiders':
                        v.score_atual_quest = v.score_aranha
                        v.mob_atual = 'spiders'
                        v.score_alvo_quest = mob_quest
                    elif mob == 'wolfs':
                        v.score_atual_quest = v.score_lobo
                        v.mob_atual = 'wolfs'
                        v.score_alvo_quest = mob_quest
                    elif mob == 'bears':
                        v.score_atual_quest = v.score_urso
                        v.mob_atual = 'bears'
                        v.score_alvo_quest = mob_quest
                    quest_on = False
                        
                if pygame.key.get_pressed()[pygame.K_n] == True:
                    quest_on = False

                        
            if v.quest_em_progresso == True:
                quest = pygame.image.load(r'graphics/quest_craft.png')
                quest.set_alpha(50)
                v.tela.blit(quest, (0,0))
                pygame.display.update()
                
                
                if v.mob_atual == 'spiders':
                    if v.score_aranha - v.score_atual_quest >= v.score_alvo_quest:
                        quests.escrever_dialogo("Thank you so much!", (250,100))
                        quests.escrever_dialogo("Here is your reward: ", (250,125))
                        quests.escrever_dialogo("Press 'Y' to continue", (250,475)) 
                        #### BLITAR RECOMPENSA AQUI
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            quest_on = False
                            v.quest_num += 1
                            v.quest_em_progresso = False
                    else:
                        quests.escrever_dialogo("Oops, you didn't finish the quest!", (250,100))
                        quests.escrever_dialogo("Press 'Y' to continue", (250,475))                                                 
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            quest_on = False
                                            
                elif v.mob_atual == 'wolfs':
                    if v.score_lobo - v.score_atual_quest >= v.score_alvo_quest:
                        quests.escrever_dialogo("Thank you so much!", (250,100))
                        quests.escrever_dialogo("Here is your reward: ", (250,125))
                        quests.escrever_dialogo("Press 'Y' to continue", (250,475))
                        ###BLITAR AQUI A RECOMPENSA
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            quest_on = False
                            v.quest_num += 1
                            v.quest_em_progresso = False
                    else:
                        quests.escrever_dialogo("Oops, you didn't finish the quest!", (250,100))
                        quests.escrever_dialogo("Press 'Y' to continue", (250,475))                                                 
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            quest_on = False

                elif v.mob_atual == 'bears':
                    if v.score_urso - v.score_atual_quest >= v.score_alvo_quest:
                        quests.escrever_dialogo("Thank you so much!", (250,100))
                        quests.escrever_dialogo("Here is your reward: ", (250,125))
                        quests.escrever_dialogo("Press 'Y' to continue", (250,475)) 
                        ###BLITAR AQUI A RECOMPENSA
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            pygame.display.update()
                            quest_on = False
                            v.quest_num += 1
                            v.quest_em_progresso = False
                    else:
                        quests.escrever_dialogo("Oops, you didn't finish the quest!", (250,100))
                        quests.escrever_dialogo("Press 'Y' to continue", (250,475))                                                 
                        pygame.display.update()
                        if pygame.key.get_pressed()[pygame.K_y] == True:
                            quest_on = False
                            
#####################################################################################################################################################################################################################
        
    def crafts(self):
        som_hey = pygame.mixer.Sound(r'sounds\saudacao.mp3')
        som_wcidfy = pygame.mixer.Sound(r'sounds\what_can_i_do_for_you.mp3')
        grupo_som = [som_hey,som_wcidfy]
        random_som = random.randrange(0,2)
        pygame.mixer.Sound.set_volume(grupo_som[random_som],0.05)
        pygame.mixer.Sound.play(grupo_som[random_som])
        
        #copiar do HUD (inventario), dar decisão para o player entre LOJA e CRAFT, cada um com sua função especifica.
    #criar craft aqui
        #Se craftar, alterar o equipamento no gamehud.(nome do equip).
        #Alterar Dano e HP do personagem quando alterar equips para mais fortes
        
    def update(self):
        if self.quest == True and self.craft == False:
            self.quests()
        if self.craft == True and self.quest == False:
            self.crafts()
        if self.craft == True and self.quest == True: ######### Criar janela de pergunta antes de continuar
            self.quests()
            self.crafts()
        if self.craft == False and self.quest == False:
            pass


#######################################################################################  CLASSE DOS MONSTROS

class Aranha(pygame.sprite.Sprite):
    def __init__(self, posx,posy):
            super().__init__()
            self.image = pygame.image.load(r'graphics/aranha.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = posx
            self.rect.y = posy
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.maxhealth = 50
            self.health = 50
            self.speed = 1
            self.old_rect = self.rect.copy()
            self.jogador = char
            self.dx = 0
            self.dy = 0
            self.type = 'monstro'
            self.dano = 1
            self.old_level = 1
            self.level = 1
            

    def Ataque(self):      
        if v.score_aranha > 0:
            self.old_level = self.level
            self.level = v.score_aranha * 0.5
            self.dano = self.level
            if self.old_level < self.level:
                if self.level >= 10 and self.level <= 19.5:
                    self.maxhealth = 100
                    self.health = self.maxhealth
                if self.level >= 20 and self.level <= 29.5:
                    self.maxhealth = 150
                    self.health = self.maxhealth
                if self.level >= 30 and self.level <= 49.5:
                    self.maxhealth = 200
                    self.health = self.maxhealth
                if self.level >= 50:
                    self.maxhealth = 500
                    self.health = self.maxhealth
                    
        else:
            self.dano = 1
                
        ##############################################mudança aranha
        if self.level < 10:
            self.image = pygame.image.load(r'graphics/aranha.png').convert_alpha()
                
        if self.level >= 10 and self.level <= 19.5:
            self.image = pygame.image.load(r'graphics/aranha2.png').convert_alpha()
                
        if self.level >= 20 and self.level <= 29.5:
            self.image = pygame.image.load(r'graphics/aranha3.png').convert_alpha()            
                
        if self.level >= 30 and self.level <= 49.5:
            self.image = pygame.image.load(r'graphics/aranha4.png').convert_alpha()
                
        if self.level >= 50:
            self.image = pygame.image.load(r'graphics/aranha5.png').convert_alpha()
            
    
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            hp_aranha = self.health
            max_hp_aranha = self.maxhealth
            frac_hp_aranha = int((50*hp_aranha)/max_hp_aranha)
            pygame.draw.rect(v.tela, v.red, (x, y, frac_hp_aranha, 1))

    def update(self,x,y):
            v.exp_mob = self.level * 10
            self.Ataque()
            self.old_rect = self.rect.copy()
        # Movimenta o inimigo em direção ao jogador
            player_pos = char.rect.center
            enemy_pos = self.rect.center
            dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                    dx, dy = dx / dist, dy / dist
            self.dx, self.dy = dx * self.speed, dy * self.speed
            self.rect.x += self.dx
            self.rect.y += self.dy


#######################################################################################  FIM CLASSE ARANHA

class Lobo(pygame.sprite.Sprite):
    def __init__(self, posx,posy):
            super().__init__()
            self.image = pygame.image.load(r'graphics/lobo.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = posx
            self.rect.y = posy
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.maxhealth = 100
            self.health = 100
            self.speed = 1
            self.old_rect = self.rect.copy()
            self.jogador = char
            self.dx = 0
            self.dy = 0
            self.type = 'monstro'
            self.dano = 20
            self.old_level = 10
            self.level = 10
            

    def Ataque(self):
        if v.score_lobo > 0:
            self.old_level = self.level
            self.level = v.score_lobo * 0.5
            self.dano = self.level
            if self.old_level < self.level:
                if self.level >= 20 and self.level <= 39.5:
                    self.maxhealth = 200
                    self.health = self.maxhealth
                if self.level >= 40 and self.level <= 59.5:
                    self.maxhealth = 400
                    self.health = self.maxhealth
                if self.level >= 60 and self.level <= 79.5:
                    self.maxhealth = 600
                    self.health = self.maxhealth
                if self.level >= 80 and self.level <= 99.5:
                    self.maxhealth = 800
                    self.health = self.maxhealth
                if self.level >= 100:
                    self.maxhealth = 1000
                    self.health = self.maxhealth
                    
        else:
            self.dano = 20
                
        ##############################################mudança lobo
        if self.level >= 10 and self.level <= 19.5:
            self.image = pygame.image.load(r'graphics/lobo.png').convert_alpha()
                
        if self.level >= 20 and self.level <= 39.5:
            self.image = pygame.image.load(r'graphics/lobo2.png').convert_alpha()
                
        if self.level >= 40 and self.level <= 59.5:
            self.image = pygame.image.load(r'graphics/lobo3.png').convert_alpha()
                
        if self.level >= 60 and self.level <= 79.5:
            self.image = pygame.image.load(r'graphics/lobo4.png').convert_alpha()
            
        if self.level >= 80 and self.level <= 99.5:
            self.image = pygame.image.load(r'graphics/lobo5.png').convert_alpha()
            
        if self.level >= 100:
            self.image = pygame.image.load(r'graphics/lobo6.png').convert_alpha()

    
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            hp_lobo = self.health
            max_hp_lobo = self.maxhealth
            frac_hp_lobo = int((50*hp_lobo)/max_hp_lobo)
            pygame.draw.rect(v.tela, v.red, (x, y, frac_hp_lobo, 1))

    def update(self,x,y):
            v.exp_mob = self.level * 10
            self.Ataque()
            self.old_rect = self.rect.copy()
        # Movimenta o inimigo em direção ao jogador
            player_pos = char.rect.center
            enemy_pos = self.rect.center
            dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                    dx, dy = dx / dist, dy / dist
            self.dx, self.dy = dx * self.speed, dy * self.speed
            self.rect.x += self.dx
            self.rect.y += self.dy

#######################################################################################  FIM CLASSE LOBO

class Urso(pygame.sprite.Sprite):
    def __init__(self, posx,posy):
            super().__init__()
            self.image = pygame.image.load(r'graphics/urso.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = posx
            self.rect.y = posy
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.maxhealth = 1000
            self.health = 1000
            self.speed = 1
            self.old_rect = self.rect.copy()
            self.jogador = char
            self.dx = 0
            self.dy = 0
            self.type = 'monstro'
            self.dano = 100
            self.old_level = 50
            self.level = 50
            

    def Ataque(self):
        if v.score_urso > 0:
            self.old_level = self.level
            self.level = v.score_urso * 0.5
            self.dano = self.level
            if self.old_level < self.level:
                if self.level >= 100 and self.level <= 199.5:
                    self.maxhealth = 2000
                    self.health = self.maxhealth
                if self.level >= 200 and self.level <= 299.5:
                    self.maxhealth = 3000
                    self.health = self.maxhealth
                if self.level >= 300 and self.level <= 399.5:
                    self.maxhealth = 5000
                    self.health = self.maxhealth
                if self.level >= 400 and self.level <= 499.5:
                    self.maxhealth = 10000
                    self.health = self.maxhealth
                if self.level >= 500:
                    self.maxhealth = 50000
                    self.health = self.maxhealth
        else:
            self.dano = 100
                
        ##############################################mudança urso
        if self.level >= 50 and self.level <= 99.5:
            self.image = pygame.image.load(r'graphics/urso.png').convert_alpha()
                
        if self.level >= 100 and self.level <= 199.5:
            self.image = pygame.image.load(r'graphics/urso2.png').convert_alpha()
                
        if self.level >= 200 and self.level <= 299.5:
            self.image = pygame.image.load(r'graphics/urso3.png').convert_alpha()
                
        if self.level >= 300 and self.level <= 399.5:
            self.image = pygame.image.load(r'graphics/urso4.png').convert_alpha()
                
        if self.level >= 400 and self.level <= 499.5:
            self.image = pygame.image.load(r'graphics/urso5.png').convert_alpha()
                
        if self.level >= 500:
            self.image = pygame.image.load(r'graphics/urso6.png').convert_alpha()

    
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            hp_urso = self.health
            max_hp_urso = self.maxhealth
            frac_hp_urso = int((50*hp_urso)/max_hp_urso)
            pygame.draw.rect(v.tela, v.red, (x, y, frac_hp_urso, 1))

    def update(self,x,y):
            v.exp_mob = self.level * 10
            self.Ataque()
            self.old_rect = self.rect.copy()
        # Movimenta o inimigo em direção ao jogador
            player_pos = char.rect.center
            enemy_pos = self.rect.center
            dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                    dx, dy = dx / dist, dy / dist
            self.dx, self.dy = dx * self.speed, dy * self.speed
            self.rect.x += self.dx
            self.rect.y += self.dy

#######################################################################################  FIM CLASSE URSO

class Rainha_Aranha(pygame.sprite.Sprite):
    def __init__(self, posx,posy):
            super().__init__()
            self.image = pygame.image.load(r'graphics/rainha_aranha.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = posx
            self.rect.y = posy
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.maxhealth = 10000
            self.health = 10000
            self.speed = 1
            self.old_rect = self.rect.copy()
            self.jogador = char
            self.dx = 0
            self.dy = 0
            self.type = 'monstro'
            self.dano = 800
            self.level = 100

    
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            hp_rainha_aranha = self.health
            max_hp_rainha_aranha = self.maxhealth
            frac_hp_rainha_aranha = int((100*hp_rainha_aranha)/max_hp_rainha_aranha)
            pygame.draw.rect(v.tela, v.red, (x, y, frac_hp_rainha_aranha, 1))

    def update(self,x,y):
            v.exp_mob = self.level * 1000
            self.old_rect = self.rect.copy()
        # Movimenta o inimigo em direção ao jogador
            player_pos = char.rect.center
            enemy_pos = self.rect.center
            dx, dy = player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist != 0:
                    dx, dy = dx / dist, dy / dist
            self.dx, self.dy = dx * self.speed, dy * self.speed
            self.rect.x += self.dx
            self.rect.y += self.dy


#######################################################################################  FIM CLASSE RAINHA ARANHA


class Attack(pygame.sprite.Sprite):
        def __init__(self, x, y, direction,level):
            super().__init__()
            self.image = pygame.image.load(r'graphics/vazio.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 15
            self.direction = direction
            self.level = level
            self.dano = 1

        def equipamentos(self):
            pass
        #Se equipamento lvl 1 --> dano = 1
        #Se equipamento lvl 10 --> dano = x
        #Se equipamento lvl 50 --> dano = 1000
            
        def update(self,x,y):
            if self.level == 1:
                self.dano = 1
            if self.level == 2:
                self.dano = 1
            elif self.level > 2:
                self.dano = int(round((self.level*0.5), 1))
    # Movimenta o ataque na direção em que o jogador está se movendo
            if self.direction == 'left':
                    self.rect.x -= self.speed
                    self.image = pygame.image.load(r'graphics/left.png').convert_alpha()
            elif self.direction == 'right':
                    self.rect.x += self.speed
                    self.image = pygame.image.load(r'graphics/right.png').convert_alpha()
            elif self.direction == 'up':
                    self.rect.y -= self.speed
                    self.image = pygame.image.load(r'graphics/up.png').convert_alpha()
            elif self.direction == 'down':
                    self.rect.y += self.speed
                    self.image = pygame.image.load(r'graphics/down.png').convert_alpha()

            npc_hit = pygame.sprite.spritecollide(self,v.npc_grupo,False)
            for npc in npc_hit:
                npc.update()
                
    #verifica se o ataque corta a arvore
            if v.equipamento:
                spriteszinhos = pygame.sprite.spritecollide(self, v.arvore_grupo, True)
                if spriteszinhos:
                    if v.randomgen() == 'monstro':
                        
                        for sprites in spriteszinhos:
                            v.monstrinhox = sprites.old_rect.x
                            v.monstrinhoy = sprites.old_rect.y
                            
                            v.criar_monstro = True
                    elif v.randomgen() == 'troncos':
                        v.troncos += random.randrange(0,4)

    # Verifica colisão com os inimigos
            hit_enemies = pygame.sprite.spritecollide(self, v.monstro_grupo, False)
            for enemy in hit_enemies:
                enemy.health -= self.dano
                if self.direction == 'right':
                    enemy.rect.x += 2
                if self.direction == 'left':
                    enemy.rect.x -= 2
                if self.direction == 'up':
                    enemy.rect.y -= 2
                if self.direction == 'down':
                    enemy.rect.y += 2
                    
                if enemy.health <= 0:
                    enemy.kill()
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

    # Remove o ataque da v.tela quando atinge o limite da distância
            if v.Norte == 1 and v.Oeste == 3:
                player_pos = char.rect.center
                player_posxd = player_pos[0] + 5 #direita
                player_posyb = player_pos[1] + 5 #baixo
                player_posxe = player_pos[0] - 35 #esquerda
                player_posyc = player_pos[1] - 35 #cima
                if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                        self.kill()
            if v.Norte == 1 and v.Oeste == 2:
                player_pos = char.rect.center
                player_posxd = player_pos[0] + 5 #direita
                player_posyb = player_pos[1] + 5 #baixo
                player_posxe = player_pos[0] - 35 #esquerda
                player_posyc = player_pos[1] - 35 #cima
                if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                        self.kill()
                
            if v.Norte == 1 and v.Oeste == 4:
                player_pos = char.rect.center
                player_posxd = player_pos[0] + 5 #direita
                player_posyb = player_pos[1] + 5 #baixo
                player_posxe = player_pos[0] - 35 #esquerda
                player_posyc = player_pos[1] - 35 #cima
                if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                        self.kill()
                        
            else:                
                player_pos = char.rect.center
                player_posxd = player_pos[0] + 50 #direita
                player_posyb = player_pos[1] + 50 #baixo
                player_posxe = player_pos[0] - 80 #esquerda
                player_posyc = player_pos[1] - 80 #cima
                if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                        self.kill()


#Classe da HUD
class HUD:
    def __init__(self):
        self.capacete = pygame.image.load(r'graphics/capacetebasico.png')
        self.busto = pygame.image.load(r'graphics/busto_basico.png')
        self.bracelete = pygame.image.load(r'graphics/mao_esquerdabasico.png')# 1 = esquerda
        self.bracelete2 = pygame.image.load(r'graphics/mao_direitabasico.png')# 2 = direita
        self.pernas = pygame.image.load(r'graphics/perna_esquerdabasica.png')
        self.pernas2 = pygame.image.load(r'graphics/perna_direitabasica.png')
        self.arma = pygame.image.load(r'graphics/machadobasico.png')
        self.arma_secundaria = pygame.image.load(r'graphics/escudobasico.png')#para teste, inicial e vazia
        
    def draw(self):
# Desenha as informações na v.tela
            health_text = v.font.render('Health: ', True, v.red)
            #transformando a vida em % para não criar uma vida super gigante
            hp = char.health
            max_hp = char.max_health
            frac_hp = int((100*hp)/max_hp)
            #desenhando o restante
            pygame.draw.rect(v.tela, v.red, (10, 50, frac_hp*5, 5))
            score_text = v.font.render('Score: ' + str(v.score), True, v.white)
            level_text = v.font.render('Level: ' + str(char.level), True, v.blue)
            v.tela.blit(health_text, (10, 10))
            v.tela.blit(score_text, (v.screen_width - score_text.get_width() - 10, 10))
            v.tela.blit(level_text, (v.screen_width - level_text.get_width() - 10, 50))
            for i, enemy in enumerate(v.monstro_grupo.sprites()):
                    enemy.draw_health(enemy.rect.x, enemy.rect.y - 10)

    def inventario(self):
        caixa_inv = pygame.image.load(r'graphics/fundo_inv.png')
        caixa_inv.set_alpha(10)
        v.tela.blit(caixa_inv,(50,50))
        pygame.display.update()

        #definindo os recursos do inventario
        tronco = pygame.image.load(r'graphics/tronco.png')
        metal = pygame.image.load(r'graphics/metal.png')
        tecido = pygame.image.load(r'graphics/tecido.png')
        couro = pygame.image.load(r'graphics/couro.png')

        #definindo os textos dos recursos
        quant_tronco = v.font_inv.render(str(v.troncos),True, v.black)
        quant_metal = v.font_inv.render(str(v.metais),True, v.black)
        quant_tecido = v.font_inv.render(str(v.tecidos),True, v.black)
        quant_couro = v.font_inv.render(str(v.couros),True, v.black)

        #definindo os itens do inventario
        capacete = self.capacete
        busto = self.busto
        bracelete = self.bracelete
        bracelete2 = self.bracelete2
        pernas = self.pernas
        pernas2 = self.pernas2
        arma = self.arma
        arma_secundaria = self.arma_secundaria

        #blitando os recursos
        v.tela.blit(tronco,(70,200))
        v.tela.blit(quant_tronco,(80,185))
        v.tela.blit(metal,(70,240))
        v.tela.blit(quant_metal,(80,225))
        v.tela.blit(tecido,(70,280))
        v.tela.blit(quant_tecido,(80,265))
        v.tela.blit(couro,(70,320))
        v.tela.blit(quant_couro,(80,305))

        #blitando os itens
        v.tela.blit(capacete,(370,230))
        v.tela.blit(busto,(350,280))
        v.tela.blit(bracelete2,(320,330))#2
        v.tela.blit(bracelete,(420,330))#1
        v.tela.blit(pernas2,(350,370))#2
        v.tela.blit(pernas,(390,370))#1
        v.tela.blit(arma,(300,290))
        v.tela.blit(arma_secundaria,(440,290))

        #definindo os textos do inventario
        score_inv = v.font.render(str(v.score), True, v.white)
        level_inv = v.font.render(str(v.level), True, v.blue)
        gold_inv = v.font.render(str(v.gold), True, v.yellow)

        #blitando os textos do inventario
        v.tela.blit(score_inv, (150,50))
        v.tela.blit(level_inv, (150,110))
        v.tela.blit(gold_inv, (560,50))

    def bussola(self):
        bussola = pygame.image.load(r'graphics/bussola.png')
        bussola.set_alpha(50)
        v.tela.blit(bussola, (0,0))
        pygame.display.update()

        #definindo a pos do personagem para a bussola
        #v.Norte
        norte_texto = v.font.render(str(v.Norte), True, v.white)
        v.tela.blit(norte_texto, (400, 15))
        #v.Sul
        sul_texto = v.font.render(str(v.Sul), True, v.white)
        v.tela.blit(sul_texto, (400, 560))
        #v.Leste
        leste_texto = v.font.render(str(v.Leste), True, v.white)
        v.tela.blit(leste_texto, (660, 300))
        #v.Oeste
        oeste_texto = v.font.render(str(v.Oeste), True, v.white)
        v.tela.blit(oeste_texto, (130, 320))

    def quest(self):
        quest = pygame.image.load(r'graphics/quest_craft.png')
        quest.set_alpha(50)
        v.tela.blit(quest, (0,0))
        if v.quest_em_progresso == True:
            quests.escrever_dialogo("PROGRESS", (325,100))
            quests.escrever_dialogo("You have to kill: ", (300,150))
            quests.escrever_dialogo(str(v.score_alvo_quest), (300,175))
            quests.escrever_dialogo(v.mob_atual, (300,200))
            quests.escrever_dialogo("You killed: ", (300,225))
            score_real = 0
            if v.mob_atual == 'spiders':
                score_real = v.score_aranha - v.score_atual_quest              
            if v.mob_atual == 'wolfs':
                score_real = v.score_lobo - v.score_atual_quest
            if v.mob_atual == 'bears':
                score_real = v.score_urso - v.score_atual_quest
                
            if score_real >= v.score_alvo_quest :
                score_real = v.score_alvo_quest
            quests.escrever_dialogo(str(score_real), (300,250))
                
            
        else:
            quests.escrever_dialogo("You don't have any quests.", (275,150))
        



        
        pygame.display.update()

        #####colocar os scores de cada mob morto no total, no topo e embaixo as quests ativas*************** Vou precisar terminar o sistema de quest antes disso



class Menu:
    def __init__(self):
        self.load = pygame.image.load(r'graphics/loadgame.png')
        self.save = pygame.image.load(r'graphics/savegame.png')
        self.quit = pygame.image.load(r'graphics/quitgame.png')
        self.menu = pygame.image.load(r'graphics/menu_jogo.png')
        
    def abrir(self):        
        v.tela.blit(self.menu, (0,0))
        v.tela.blit(self.load,(40,150))
        v.tela.blit(self.save,(300,250))
        v.tela.blit(self.quit,(40,350))
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
        dados_jogo = {}
        with open('savegame.dat', 'rb') as arquivo:
            dados_jogo = pickle.load(arquivo)
            
            ##########DAR UM SINAL DE QUE O LOAD FUNCIONOU
        v.score = dados_jogo['score']
        v.score_aranha = dados_jogo['score_aranha']
        v.score_lobo = dados_jogo['score_lobo']
        v.score_urso = dados_jogo['score_urso']
        v.score_rainha_aranha = dados_jogo['score_rainha_aranha']
        v.exp = dados_jogo['exp']
        v.level = dados_jogo['level']
        v.exp_mob = dados_jogo['exp_mob']
        v.Norte = dados_jogo['Norte']
        v.Sul = dados_jogo['Sul']
        v.Leste = dados_jogo['Leste']
        v.Oeste = dados_jogo['Oeste']
        char.rect = dados_jogo['personagem']
        v.fase_atual = dados_jogo['fase_atual']
        v.gold = dados_jogo['gold']
        v.troncos = dados_jogo['troncos']
        v.metais = dados_jogo['metais']
        v.tecidos = dados_jogo['tecidos']
        v.couros = dados_jogo['couros']
        v.quest_num = dados_jogo['quest_num']
        v.quest_em_progresso = dados_jogo['quest_em_progresso']
        v.score_atual_quest = dados_jogo['score_atual_quest']
        v.score_alvo_quest = dados_jogo['score_alvo_quest']
        v.mob_atual = dados_jogo['mob_atual']
        v.rainha_aranha_on = dados_jogo['rainha_aranha_on']
        v.urso_on = dados_jogo['urso_on']
        v.lobo_on = dados_jogo['lobo_on']
        v.aranha_on = dados_jogo['aranha_on']
        v.machadinho = dados_jogo['machadinho']
                           

            
        
    def savegame(self):
        ##########DAR UM SINAL DE QUE O CLIQUE FUNCIONOU
        dados_jogo = {
            'score' : v.score
            'score_aranha' : v.score_aranha
            'score_lobo' : v.score_lobo
            'score_urso' : v.score_urso
            'score_rainha_aranha' : v.score_rainha_aranha
            'exp' : v.exp
            'level' : v.level
            'exp_mob' : v.exp_mob
            'Norte' : v.Norte
            'Sul' : v.Sul
            'Leste' : v.Leste
            'Oeste' : v.Oeste
            'personagem' : char.rect
            'fase_atual' : v.fase_atual
            'gold' : v.gold
            'troncos' : v.troncos
            'metais' : v.metais
            'tecidos' : v.tecidos
            'couros' : v.couros
            'quest_num' : v.quest_num
            'quest_em_progresso' : v.quest_em_progresso
            'score_atual_quest' : v.score_atual_quest
            'score_alvo_quest' : v.score_alvo_quest
            'mob_atual' : v.mob_atual
            'rainha_aranha_on' : v.rainha_aranha_on
            'urso_on' : v.urso_on
            'lobo_on' : v.lobo_on
            'aranha_on' : v.aranha_on
            'machadinho' : v.machadinho            
            }
        with open('savegame.dat', 'wb') as arquivo:
            pickle.dump(dados_jogo, arquivo)
            ##########DAR UM SINAL DE QUE O SAVE FUNCIONOU

    def quitgame(self):
        #criar pop up perguntando se tem certeza
        v.run_game = False
        pygame.quit()
        sys.exit()
        
#############################################################################################################################################################################################################################################################################################################################################################################################################################################    
              
        
        
        
        

################################################## BORDA TOPO ######################################################
class Borda_topo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800,10))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        hit = pygame.sprite.spritecollide(self, v.char_grupo, False)
        for hits in hit:
            v.Norte += 1
            v.Sul -= 1
            char.pos.y = 500            
            for arvore in v.arvore_grupo:
                arvore.kill()
            for spider in v.monstro_grupo:
                spider.kill()
            gerar_arvore()
            self.passar_mapa()

    def passar_mapa(self):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        if v.fase_atual == 'FN':
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FE.mudar_mapa()
################################################## BORDA TOPO ######################################################

################################################## BORDA BAIXO #####################################################
class Borda_baixo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((800,10))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 590

    def update(self):
            hit = pygame.sprite.spritecollide(self, v.char_grupo, False)
            for hits in hit:
                v.Sul += 1
                v.Norte -= 1
                char.pos.y = 50           
                for arvore in v.arvore_grupo:
                    arvore.kill()
                for spider in v.monstro_grupo:
                    spider.kill()
                gerar_arvore()
                self.passar_mapa()

    def passar_mapa(self):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        if v.fase_atual == 'FN':
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FE.mudar_mapa()
################################################## BORDA BAIXO #####################################################

################################################## BORDA ESQUERDA ##################################################
class Borda_esquerda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10,600))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
            hit = pygame.sprite.spritecollide(self, v.char_grupo, False)
            for hits in hit:
                v.Oeste += 1
                v.Leste -= 1
                char.pos.x = 700            
                for arvore in v.arvore_grupo:
                    arvore.kill()
                for spider in v.monstro_grupo:
                    spider.kill()
                gerar_arvore()
                self.passar_mapa()

    def passar_mapa(self):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        if v.fase_atual == 'FN':
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FE.mudar_mapa()
################################################## BORDA ESQUERDA ##################################################

################################################## BORDA DIREITA ###################################################
class Borda_direita(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10,600))
        self.rect = self.image.get_rect()
        self.rect.x = 790
        self.rect.y = 0

    def update(self):
        hit = pygame.sprite.spritecollide(self, v.char_grupo, False)
        for hits in hit:
            v.Leste += 1
            v.Oeste -= 1
            char.pos.x = 50             
            for arvore in v.arvore_grupo:
                arvore.kill()
            for spider in v.monstro_grupo:
                spider.kill()
            gerar_arvore()
            self.passar_mapa()

    def passar_mapa(self):
        som_passar_mapa = pygame.mixer.Sound(r'sounds\passar_mapa.mp3')
        som_cidade = pygame.mixer.Sound(r'sounds\som_cidade.mp3')
        if v.fase_atual == 'FN':
            if v.Norte == 1 and v.Oeste == 3:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            if v.Norte == 1 and v.Oeste == 4:
                pygame.mixer.Sound.set_volume(som_cidade,0.05)
                pygame.mixer.Sound.play(som_cidade)
            else:
                pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
                pygame.mixer.Sound.play(som_passar_mapa)
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
            pygame.mixer.Sound.set_volume(som_passar_mapa,0.05)
            pygame.mixer.Sound.play(som_passar_mapa)
            FE.mudar_mapa()
            
################################################## BORDA DIREITA ###################################################        

class Mapa_FN:
    def __init__(self):
        self.mapa_atual = pygame.image.load(r'graphics/first_map.png')
        
    def mudar_mapa(self):
        for npc in v.npc_grupo:
            npc.kill()
        for sprite in v.casa_grupo:
            sprite.kill()
        if v.Norte == 0 and v.Sul == 0 and v.Leste == 0 and v.Oeste == 0:
            self.mapa_atual = pygame.image.load(r'graphics/first_map.png')
        if v.Norte != 0 or v.Sul != 0 or v.Leste != 0 or v.Oeste != 0:
            self.mapa_atual = pygame.image.load(r'graphics/floresta_negra.png')
        if v.Norte == 1 and v.Oeste == 2:
            muros.npc_cidade((70,150),guarda1,False,False)#Guarda1
            muros.npc_cidade((70,300),guarda1,False,False)#Guarda2
            muros.muro_N1O2()
            self.mapa_atual = pygame.image.load(r'graphics/N1O2.png')
        elif v.Norte == 1 and v.Oeste == 3:
                muros.muro_cidade()
                #####################################################CRIAR 2 guardas no N1O2 e no N1O4
                #npc_cidade(pos,image,quest,craft)
                muros.npc_cidade((100,120),npc1,True,False)#quest npc
                muros.npc_cidade((290,470),npc2,False,True)#ferreiro
                muros.npc_cidade((200,120),npc3,True,False)#quest npc
                muros.npc_cidade((730,150),guarda1,False,False)#Guarda1
                muros.npc_cidade((730,300),guarda1,False,False)#Guarda2
                muros.casa((50,30))
                muros.casa((200,30))
                muros.casa((350,30))
                muros.ferreiro((50,315))
                self.mapa_atual = pygame.image.load(r'graphics/mapa_cidade1.png')
        elif v.Norte == 2 and v.Oeste == 3:
            muros.muro_N2O3()
        elif v.Norte == 0 and v.Oeste == 3:
            muros.muro_N0O3()
        elif v.Norte == 1 and v.Oeste == 4:
            muros.npc_cidade((670,150),guarda1,False,False)#Guarda1
            muros.npc_cidade((670,300),guarda1,False,False)#Guarda2
            muros.muro_N1O4()
            
        else:
            for sprite in v.muro_grupo:
                sprite.kill()
            
            
            

class Mapa_FA:
    def __init__(self):
        self.mapa_atual = pygame.image.load(r'graphics/floresta_negra.png') #colocar primeiro mapa da Floresta Alta - Cidade 1

    def mudar_mapa(self):
        if v.Norte == 0 and v.Sul == 0 and v.Leste == 0 and v.Oeste == 0:
            self.mapa_atual = pygame.image.load(r'graphics/first_map.png') # ALTERAR PARA A CIDADE 1 DA FLORESTA ALTA
        if v.Norte != 0 or v.Sul != 0 or v.Leste != 0 or v.Oeste != 0:
            self.mapa_atual = pygame.image.load(r'graphics/floresta_negra.png') # ALTERAR PARA FLORESTA ALTA
        if v.Oeste == 5 and v.Norte == 0 and v.Sul == 0 :
            self.mapa_atual = pygame.image.load(r'graphics/first_map.png') #ALTERAR PARA ENTRADA DA CIDADE 2
        ####Criar entrada da cidade portuaria (3) e as outras entradas da cidade 2#####

class Mapa_FE:
    def __init__(self):
        self.mapa_atual = pygame.image.load(r'graphics/floresta_negra.png') #colocar primeiro mapa da Floresta Encantada - CIDADE

    def mudar_mapa(self):
        if v.Norte == 0 and v.Sul == 0 and v.Leste == 0 and v.Oeste == 0:
            self.mapa_atual = pygame.image.load(r'graphics/floresta_negra.png')#ALTERAR PARA CIDADE DAS FADAS       
        if v.Norte != 0 or v.Sul != 0 or v.Leste != 0 or v.Oeste != 0:
            self.mapa_atual = pygame.image.load(r'graphics/floresta_negra.png')#ALTERAR PARA FLORESTA ENCANTADO
        

def gerar_arvore():
    num_arvores = random.randrange(20,100)
    while num_arvores > 0:
        random_arvore = v.randomtree()
        if random_arvore == (350,300) or random_arvore == (400,300) or random_arvore == (400,350):
            random_arvore = v.randomtree()
        else:
            pass
        arvore1 = Arvore(random_arvore)
        v.arvore_grupo.add(arvore1)
        v.colisao_grupo.add(arvore1)
        num_arvores -= 1

Borda_topo = Borda_topo()
Borda_baixo = Borda_baixo()
Borda_direita = Borda_direita()
Borda_esquerda = Borda_esquerda()

FN = Mapa_FN()
FA = Mapa_FA()
FE = Mapa_FE()

char = Player()
gamehud = HUD()

