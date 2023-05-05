import pygame, random, sys
import var as v

#Inicializando o pygame
pygame.init()

#Criando janela do jogo
screen_width = 800 #largura
screen_height = 600 #altura
tela = pygame.display.set_mode((screen_width,screen_height))
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
font = pygame.font.SysFont('Arial', 30)

#variaveis e grupos de sprites
score = 0
money = 0
attack_grupo = pygame.sprite.Group()
arvore_grupo = pygame.sprite.Group()
monstro_grupo = pygame.sprite.Group()
char_grupo = pygame.sprite.Group()

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
            super().__init__()
            self.image = pygame.image.load(r'graphics/char.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = screen_width / 2
            self.rect.y = screen_height / 2
            self.old_rect = self.rect.copy()
            self.health = 50
            self.direction = 'right'
            self.dir = pygame.math.Vector2()
            self.speed = 2
            self.obstaculo = arvore_grupo
            self.pos = pygame.math.Vector2(self.rect.topleft)

    def equipamento(self):
            self.image = pygame.image.load(r'graphics/charequipado.png').convert_alpha()
            v.equipamento = True

    def collision(self,direction):
            collision_sprites = pygame.sprite.spritecollide(self,self.obstaculo,False)
            if collision_sprites:
                if direction == 'horizontal':
                    for sprite in collision_sprites:
                        # colisão na direita
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            v.right = True
                            self.rect.right = sprite.rect.left
                            self.pos.x = self.rect.x
                        else:
                            v.right = False

                        # colisão na esquerda
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            v.left = True
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.x
                        else:
                            v.left = False

                if direction == 'vertical':
                    for sprite in collision_sprites:
                        # colisão em baixo
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            v.bottom = True
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y
                        else:
                            v.bottom = False

                        # colisão em cima
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            v.top = True
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.y
                        else:
                            v.top = False
     

    

    def entrada(self): #Verifica as teclas pressionadas para dar comandos
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:            
                self.dir.y = -1
                self.direction = 'up'
            elif keys[pygame.K_DOWN]:
                self.dir.y = 1
                self.direction = 'down'
            else:
                self.dir.y = 0

            if keys[pygame.K_RIGHT]:
                self.dir.x = 1
                self.direction = 'right'
            elif keys[pygame.K_LEFT]:
                self.dir.x = -1
                self.direction = 'left'
            else:
                self.dir.x = 0

    def update(self):
            self.entrada()
            self.pos.x += self.dir.x * self.speed
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.pos.y += self.dir.y * self.speed
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
        if self.direction == 'right':
            ax = self.rect.x +25
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir)
            attack_grupo.add(attack)
        if self.direction == 'left':
            ax = self.rect.x
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir)
            attack_grupo.add(attack)
        if self.direction == 'up':
            ax = self.rect.x
            ay = self.rect.y
            adir = self.direction
            attack = Attack(ax,ay,adir)
            attack_grupo.add(attack)
        if self.direction == 'down':
            ax = self.rect.x
            ay = self.rect.y +10
            adir = self.direction
            attack = Attack(ax,ay,adir)
            attack_grupo.add(attack)
  

class Arvore(pygame.sprite.Sprite):
        def __init__(self,pos):
            super().__init__()
            self.image = pygame.image.load(r'graphics/arvore.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()


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

    def collision(self,direction):
            collision_sprites = pygame.sprite.spritecollide(self,char_grupo,False)
            if collision_sprites:
                if direction == 'horizontal':
                    for sprite in collision_sprites:
                        # colisao na direita
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            self.rect.right = sprite.rect.left
                            self.pos.x = self.rect.x                        
                            self.jogador.health -= 1
                            v.hit_right = True
                        else:
                            v.hit_right = False

                        # colisao na esquerda
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.x
                            self.jogador.health -= 1
                            v.hit_left = True
                        else:
                            v.hit_left = False


                if direction == 'vertical':
                    for sprite in collision_sprites:
                        # colisao em baixo
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y
                            self.jogador.health -= 1
                            v.hit_bottom = True
                        else:
                            v.hit_bottom = False

                        # colisao em cima
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.y
                            self.jogador.health -= 1
                            v.hit_top = True
                        else:
                            v.hit_top = False
         
    def draw_health(self, x, y):
    # Desenha a barra de vida do inimigo acima dele
            pygame.draw.rect(tela, red, (x, y, self.health, 5))

    def update(self,x,y):
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

            #verifica colisão com o jogador
            self.collision('horizontal')
            self.collision('vertical')



class Attack(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            super().__init__()
            self.image = pygame.image.load(r'graphics/right.png').convert_alpha()
            self.image_right = pygame.image.load(r'graphics/right.png').convert_alpha()
            self.image_up = pygame.image.load(r'graphics/up.png').convert_alpha()
            self.image_left = pygame.image.load(r'graphics/left.png').convert_alpha()
            self.image_down = pygame.image.load(r'graphics/down.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 15
            self.direction = direction
        def update(self,x,y):
    # Movimenta o ataque na direção em que o jogador está se movendo
            if self.direction == 'left':
                    self.rect.x -= self.speed
                    self.image = self.image_left
            elif self.direction == 'right':
                    self.rect.x += self.speed
                    self.image = self.image_right
            elif self.direction == 'up':
                    self.rect.y -= self.speed
                    self.image = self.image_up
            elif self.direction == 'down':
                    self.rect.y += self.speed
                    self.image = self.image_down
                    
    #verifica se o ataque corta a arvore
            if v.equipamento:
                spriteszinhos = pygame.sprite.spritecollide(self, arvore_grupo, True)
                if spriteszinhos:
                    if v.randomgen() == 'monstro':
                        
                        for sprites in spriteszinhos:
                            v.monstrinhox = sprites.old_rect.x
                            v.monstrinhoy = sprites.old_rect.y
                            
                            v.criar_monstro = True
                    elif v.randomgen() == 'dinheiro':
                        global money
                        money += 10
                        ############# FAZER APARECER BOLSINHA DE DINHEIRO, IGUAL MONSTRO E SOMAR DINHEIRO QUANDO ENCOSTAR, FAZENDO-A SUMIR (facil de fazer, né)

    # Verifica colisão com os inimigos
            hit_enemies = pygame.sprite.spritecollide(self, monstro_grupo, False)
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
                    global score
                    enemy.kill()
                    score += 1

    # Remove o ataque da tela quando atinge as bordas
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
# Desenha as informações na tela
            health_text = font.render('Health: ', True, red)
            pygame.draw.rect(tela, red, (10, 50, char.health*10, 10))
            score_text = font.render('Score: ' + str(score), True, red)
            money_text = font.render('Money: ' + str(money), True, red)
            tela.blit(health_text, (10, 10))
            tela.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
            tela.blit(money_text, (screen_width - money_text.get_width() -10, 50))
            for i, enemy in enumerate(monstro_grupo.sprites()):
                    enemy.draw_health(enemy.rect.x, enemy.rect.y - 10)



char = Player()
char_grupo.add(char)
machadinho_no_chao = pygame.image.load(r'graphics/machado.png')
machado_rect = machadinho_no_chao.get_rect(topleft=(350,300))

pygame.display.update()

pos_arvores = [(0,0),(50,0),(100,0),(150,0),(200,0),(250,0),(300,0),(350,0),(400,0),(450,0),(500,0),(550,0),(600,0),(650,0),(700,0),(750,0),
                   (0,50),(0,100),(0,150),(0,200),(0,250),(0,300),(0,350),(0,400),(0,450),(0,500),(0,550),
                   (50,50),(100,50),(150,50),(200,50),(250,50),(300,50),(350,50),(400,50),(450,50),(500,50),(550,50),(600,50),(650,50),(700,50),(750,50),
                   (50,100),(100,100),(150,100),(200,100),(250,100),(300,100),(350,100),(400,100),(450,100),(500,100),(550,100),(600,100),(650,100),(700,100),(750,100),
                   (50,150),(100,150),(150,150),(200,150),(250,150),(300,150),(350,150),(400,150),(450,150),(500,150),(550,150),(600,150),(650,150),(700,150),(750,150),
                   (50,200),(100,200),(150,200),(200,200),(250,200),
                   (550,200),(600,200),(650,200),(700,200),(750,200),
                   (50,250),(100,250),(150,250),(200,250),(250,250),
                   (550,250),(600,250),(650,250),(700,250),(750,250),
                   (50,300),(100,300),(150,300),(200,300),(250,300),
                   (550,300),(600,300),(650,300),(700,300),(750,300),
                   (50,350),(100,350),(150,350),(200,350),(250,350),
                   (550,350),(600,350),(650,350),(700,350),(750,350),
                   (50,400),(100,400),(150,400),(200,400),(250,400),(300,400),(350,400),(400,400),(450,400),(500,400),(550,400),(600,400),(650,400),(700,400),(750,400),
                   (50,450),(100,450),(150,450),(200,450),(250,450),(300,450),(350,450),(400,450),(450,450),(500,450),(550,450),(600,450),(650,450),(700,450),(750,450),
                   (50,500),(100,500),(150,500),(200,500),(250,500),(300,500),(350,500),(400,500),(450,500),(500,500),(550,500),(600,500),(650,500),(700,500),(750,500),
                   (50,550),(100,550),(150,550),(200,550),(250,550),(300,550),(350,550),(400,550),(450,550),(500,550),(550,550),(600,550),(650,550),(700,550),(750,550)]
arvore1 = [Arvore(arvores) for arvores in pos_arvores]
arvore_grupo.add(arvore1)

hud = HUD()
v.run_game = True

while v.run_game:
        frames.tick(60)
        tela.blit(fundo,(0,0))
        if v.machadinho:
            tela.blit(machadinho_no_chao,(350,300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v.run_game = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if v.machadinho == True:
                        pass
                    else:
                        char.attack()
                    if char.rect.colliderect(machado_rect):
                        v.machadinho = False
                        char.equipamento()

            if v.criar_monstro == True:
                monstro = Monstro(v.monstrinhox, v.monstrinhoy)
                monstro_grupo.add(monstro)
                v.criar_monstro = False

        
        
        char_grupo.draw(tela)
        arvore_grupo.draw(tela)
        monstro_grupo.draw(tela)
        attack_grupo.draw(tela)
        attack_grupo.update(0,0)
        monstro_grupo.update(0,0)
        char_grupo.update()
        hud.draw()
        
        pygame.display.update()
        if char.health <= 0:
            while char.health <= 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        v.run_game = False
                        pygame.quit()
                        sys.exit()
                char.image = pygame.image.load(r'graphics/charmorto.png').convert_alpha()
                continue_game = pygame.image.load(r'graphics/continue.png')
                tela.blit(continue_game,(220,300))
                sim_bot = pygame.image.load(r'graphics/YES.png')
                nao_bot = pygame.image.load(r'graphics/NO.png')
                tela.blit(sim_bot,(350,350))
                tela.blit(nao_bot,(450,350))
                clicou_sim = pygame.Rect(350,350,50,50)
                clicou_nao = pygame.Rect(450,350,50,50)
                pygame.display.update()
                if pygame.mouse.get_pressed() == (1,0,0):
                    mouseposition = pygame.mouse.get_pos()
                    if clicou_sim.collidepoint(mouseposition):
                        grupos = [attack_grupo, char_grupo, arvore_grupo, monstro_grupo]
                        for grupo in grupos:
                            for sprites in grupo:
                                sprites.kill()
                        score = 0
                        money = 0
                        char.health = 50
                        v.machadinho = True
                        v.equipamento = False
                        arvore1 = [Arvore(arvores) for arvores in pos_arvores]
                        arvore_grupo.add(arvore1)
                        char_grupo.add(char)
                        char.image = pygame.image.load(r'graphics/char.png').convert_alpha()
                        char.rect.x = screen_width / 2
                        char.rect.y = screen_height / 2
                        pygame.display.update()
                    if clicou_nao.collidepoint(mouseposition):
                        pygame.quit()
                        sys.exit()
    
    
    
    
        
        
            
        
            
            





