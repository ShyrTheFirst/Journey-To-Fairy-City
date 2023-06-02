import pygame, random, sys
import var as v



# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            self.image = pygame.image.load(r'graphics/char.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = v.posinitix
            self.rect.y = v.posinitiy
            self.old_rect = self.rect.copy()
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
            #mostrar tela de lvlup?!
            self.level += 1
            self.exp = 0
        

    def equipamento(self):
            self.image = pygame.image.load(r'graphics/charequipado.png').convert_alpha()
            v.equipamento = True

    def collision(self,direction):
            collision_sprites = pygame.sprite.spritecollide(self,self.obstaculo,False)
            if collision_sprites:
                if direction == 'horizontal':
                    for sprite in collision_sprites:
                        if sprite.type == 'monstro':
                            self.health -= sprite.dano
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
            attack = Attack(ax,ay,adir)
            v.attack_grupo.add(attack)
        if self.direction == 'left':
            ax = self.rect.x
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir)
            v.attack_grupo.add(attack)
        if self.direction == 'up':
            ax = self.rect.x
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir)
            v.attack_grupo.add(attack)
        if self.direction == 'down':
            ax = self.rect.x
            ay = self.rect.y +10
            adir = self.direction
            attack = Attack(ax,ay,adir)
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
            self.dano = self.level * 2
        else:
            self.dano = 1

        #criar ataque igual ao do player, mas uma mordida. Empurra o player alguns quadros pra trás, evitando dano continuo

    
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            pygame.draw.rect(v.tela, v.red, (x, y, self.health, 5))

    def update(self,x,y):
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
        def __init__(self, x, y, direction):
            super().__init__()
            self.image = pygame.image.load(r'graphics/vazio.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 15
            self.direction = direction
            
        def update(self,x,y):
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
                        ############# FAZER APARECER BOLSINHA DE DINHEIRO, IGUAL MONSTRO E SOMAR DINHEIRO QUANDO ENCOSTAR, FAZENDO-A SUMIR OU TALVEZ GERAR RECURSOS QUANDO CORTA. MAIS CONDIZENTE COM CORTAR A ARVORE

    # Verifica colisão com os inimigos
            hit_enemies = pygame.sprite.spritecollide(self, v.monstro_grupo, False)
            for enemy in hit_enemies:
                enemy.health -= 1
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
                    v.exp += 1

    # Remove o ataque da v.tela quando atinge o limite da distância
            player_pos = char.rect.center
            player_posxd = player_pos[0] + 50 #direita
            player_posyb = player_pos[1] + 50 #baixo
            player_posxe = player_pos[0] - 80 #esquerda
            player_posyc = player_pos[1] - 80 #cima
            if self.rect.x > player_posxd or self.rect.y > player_posyb or self.rect.x < player_posxe or self.rect.y < player_posyc:
                    self.kill()

#Classe da HUD
class HUD:
    def draw(self):
# Desenha as informações na v.tela
            health_text = v.font.render('Health: ', True, v.red)
            pygame.draw.rect(v.tela, v.red, (10, 50, char.health*10, 10))
            score_text = v.font.render('Score: ' + str(v.score), True, v.red)
            v.tela.blit(health_text, (10, 10))
            v.tela.blit(score_text, (v.screen_width - score_text.get_width() - 10, 10))
            for i, enemy in enumerate(v.monstro_grupo.sprites()):
                    enemy.draw_health(enemy.rect.x, enemy.rect.y - 10)

    def inventario(self):
        caixa_inv = pygame.image.load(r'graphics/fundo_inv.png')
        caixa_inv.set_alpha(10)
        inv_text = v.font.render('Inventory', False, v.red)
        v.tela.blit(inv_text, (50,50))
        v.tela.blit(caixa_inv,(50,50))
        pygame.display.update()

    def busola(self):
        busola = pygame.image.load(r'graphics/busola.png')
        busola.set_alpha(50)
        v.tela.blit(busola, (v.screen_width/2,v.screen_height/2))
        pygame.display.update()

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
        if v.Norte == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Sul == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Leste == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Oeste == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')

class Mapa_FA:
    def __init__(self):
        self.mapa_atual = pygame.image.load(r'graphics/N1.png') #colocar primeiro mapa da Floresta Alta

    def mudar_mapa(self):
        if v.Norte == 0 and v.Sul == 0 and v.Leste == 0 and v.Oeste == 0:
            self.mapa_atual = pygame.image.load(r'graphics/first_map.png')
        if v.Norte == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Sul == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Leste == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Oeste == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')

class Mapa_FE:
    def __init__(self):
        self.mapa_atual = pygame.image.load(r'graphics/N1.png') #colocar primeiro mapa da Floresta Encantada

    def mudar_mapa(self):
        if v.Norte == 0 and v.Sul == 0 and v.Leste == 0 and v.Oeste == 0:
            self.mapa_atual = pygame.image.load(r'graphics/first_map.png')
        if v.Norte == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Sul == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Leste == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')
        if v.Oeste == 1:
            self.mapa_atual = pygame.image.load(r'graphics/N1.png')

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

