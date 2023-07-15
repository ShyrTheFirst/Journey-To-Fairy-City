import pygame, random, sys
import var as v
import muros

npc1 = pygame.image.load(r'graphics/npc1.png').convert_alpha()
npc2 = pygame.image.load(r'graphics/npc2.png').convert_alpha()
npc3 = pygame.image.load(r'graphics/npc3.png').convert_alpha()
guarda1  = pygame.image.load(r'graphics/guarda1.png').convert_alpha()

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
                            #talvez eu tire isso pra identificar o ataque do mob e só mantenha a colisão pra não atravessar os mob################################################################################
                        if sprite.type == 'arvore':
                            pass      #colocar som de folhas
                        # colisão na direita
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:                                                       
                            self.rect.right = sprite.rect.left
                            self.pos.x = self.rect.x

                        # colisão na esquerda
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:                           
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.x

                if direction == 'vertical':
                    for sprite in collision_sprites:
                        if sprite.type == 'monstro':
                            self.health -= sprite.dano
                            #talvez eu tire isso pra identificar o ataque do mob e só mantenha a colisão pra não atravessar os mob
                        if sprite.type == 'arvore':
                            pass      #colocar som de folhas
                        # colisão em baixo
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y

                        # colisão em cima
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:                            
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.y
     

    

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
            self.type = 'arvore'

class NPC(pygame.sprite.Sprite): ############################################################ FINALIZAR NPC
    def __init__(self,pos,image,quest,craft):
            super().__init__()
            self.image = image #criar imagem do npc#
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.type = 'npc'
            self.quest = quest
            self.craft = craft
    def quests(self):
        print("quest on")
    #criar quest aqui

    def crafts(self):
        print("craft on")
    #criar craft aqui
        
    def update(self):
        print("Diga olá")
        if self.quest == True and self.craft == False:
            self.quests()
        if self.craft == True and self.quest == False:
            self.crafts()
        if self.craft == True and self.quest == True:
            self.quests()
            self.crafts()
        if self.craft == False and self.quest == False:
            print("nada")

    

class Monstro(pygame.sprite.Sprite):
    def __init__(self, posx,posy):
            super().__init__()
            self.image = pygame.image.load(r'graphics/monstro.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = posx
            self.rect.y = posy
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.health = 50
            self.speed = 1
            self.old_rect = self.rect.copy()
            self.jogador = char
            self.dx = 0
            self.dy = 0
            self.type = 'monstro'
            self.dano = 1
            self.level = 1
            

    def Ataque(self):
        if v.score > 0:
            self.level = v.score * 0.5
            self.dano = self.level
        else:
            self.dano = 1

        if self.level >= 10 and self.level <= 19.5:
            self.image = pygame.image.load(r'graphics/aranha2.png').convert_alpha()
            self.health = 100
        if self.level >= 20 and self.level <= 29.5:
            self.image = pygame.image.load(r'graphics/aranha3.png').convert_alpha()
            self.health = 150
        if self.level >= 30 and self.level <= 49.5:
            self.image = pygame.image.load(r'graphics/aranha4.png').convert_alpha()
            self.health = 200
        if self.level >= 50:
            self.image = pygame.image.load(r'graphics/aranha5.png').convert_alpha()
            self.health = 500

        #criar ataque igual ao do player, mas uma mordida. Empurra o player alguns quadros pra trás, evitando dano continuo
        #criar def colisao, onde vai detectar a colisao com o player e ativar o ataque de mordida, empurrando o player para trás conforme o local aonde identificou a colisao######################

    
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            pygame.draw.rect(v.tela, v.red, (x, y, self.health, 1))

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
            
        def update(self,x,y):
            if self.level == 1:
                self.dano = 1
            if self.level == 2:
                self.dano = 1
            elif self.dano > 2:
                self.dano = self.level*0,5
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
            elif v.Norte == 1 and v.Oeste == 3:
                    self.image = pygame.image.load(r'graphics/vazio.png').convert_alpha()

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
                        #tronco_img = pygame.image.load(r'graphics/tronco.png')
                        v.troncos += random.randrange(0,4)
                        ############# FAZER APARECER TRONCO PARA ILUSTRAR QUE GANHOU ALGO

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
                    v.score += 1
                    v.exp += v.exp_mob

    # Remove o ataque da v.tela quando atinge o limite da distância
            player_pos = char.rect.center
            player_posxd = player_pos[0] + 50 #direita
            player_posyb = player_pos[1] + 50 #baixo
            player_posxe = player_pos[0] - 80 #esquerda
            player_posyc = player_pos[1] - 80 #cima
            if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                    self.kill()


                ##################################################################################################################################### Mordida ainda não ta pronta

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
            pygame.draw.rect(v.tela, v.red, (10, 50, frac_hp*5, 5))
            score_text = v.font.render('Score: ' + str(v.score), True, v.red)
            level_text = v.font.render('Level: ' + str(char.level), True, v.red)
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
        if v.fase_atual == 'FN':
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
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
        if v.fase_atual == 'FN':
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
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
        if v.fase_atual == 'FN':
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
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
        if v.fase_atual == 'FN':
            FN.mudar_mapa()
        elif v.fase_atual == 'FA':
            FA.mudar_mapa()
        elif v.fase_atual == 'FE':
            FE.mudar_mapa()
################################################## BORDA DIREITA ###################################################        

class Mapa_FN:
    def __init__(self):
        self.mapa_atual = pygame.image.load(r'graphics/first_map.png')
        
    def mudar_mapa(self):
        
        if v.Norte == 0 and v.Sul == 0 and v.Leste == 0 and v.Oeste == 0:
            self.mapa_atual = pygame.image.load(r'graphics/first_map.png')
        if v.Norte != 0 or v.Sul != 0 or v.Leste != 0 or v.Oeste != 0:
            self.mapa_atual = pygame.image.load(r'graphics/floresta_negra.png')
        if v.Norte == 1 and v.Oeste == 2:
            for npc in v.npc_grupo:
                npc.kill()
            muros.muro_N1O2()
            self.mapa_atual = pygame.image.load(r'graphics/N1O2.png')
        elif v.Norte == 1 and v.Oeste == 3:
                muros.muro_cidade()
                #####################################################CRIAR OS NPCS NO LUGAR CERTO - +2 guardas no N1O2 e no N1O4
                muros.npc_cidade((100,80),npc1,True,False)
                muros.npc_cidade((150,80),npc2,False,True)
                muros.npc_cidade((200,80),npc3,True,True)
                muros.npc_cidade((250,80),guarda1,False,False)#Criar mais um guarda para ficar em cada ponta do mapa!
                self.mapa_atual = pygame.image.load(r'graphics/mapa_cidade1.png')
        elif v.Norte == 2 and v.Oeste == 3:
            muros.muro_N2O3()
        elif v.Norte == 0 and v.Oeste == 3:
            muros.muro_N0O3()
        elif v.Norte == 1 and v.Oeste == 4:
            for npc in v.npc_grupo:
                npc.kill()
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

