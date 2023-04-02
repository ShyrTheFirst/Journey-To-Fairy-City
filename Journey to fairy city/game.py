import var as v
while v.game == True:
    import pygame, sys, random
    

    #Iniciar o pygame###########
    pygame.init()
    tela = pygame.display.set_mode([800, 600])
    pygame.display.set_caption("Journey to the Fairy City")
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
    ############################

    #Classes####################

    class Monstro(pygame.sprite.Sprite):
        def __init__(self,posx,posy,player,player_group):
            super().__init__()
            self.image = pygame.image.load(r'graphics/monstro.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = posx, posy
            self.direction = pygame.math.Vector2()
            self.old_rect = self.rect.copy()
            self.jogador = player
            self.jogador_grupo = player_group
            self.speed = 1.2
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.hp = 10

        def collision(self,direction):
            collision_sprites = pygame.sprite.spritecollide(self,self.jogador_grupo,False)
            if collision_sprites:
                if direction == 'horizontal':
                    for sprite in collision_sprites:
                        # collision on the right
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            self.rect.right = sprite.rect.left
                            self.pos.x = self.rect.x                        
                            self.jogador.hp -= 1
                            v.hit_right = True
                        else:
                            v.hit_right = False

                        # collision on the left
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.x
                            self.jogador.hp -= 1
                            v.hit_left = True
                        else:
                            v.hit_left = False


                if direction == 'vertical':
                    for sprite in collision_sprites:
                        # collision on the bottom
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y
                            self.jogador.hp -= 1
                            v.hit_bottom = True
                        else:
                            v.hit_bottom = False

                        # collision on the top
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.y
                            self.jogador.hp -= 1
                            v.hit_top = True
                        else:
                            v.hit_top = False

        def update(self):
            dirvect = pygame.math.Vector2(self.jogador.rect.x - self.rect.x,
                                          self.jogador.rect.y - self.rect.y)
            dirvect.normalize()

            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
            self.collision('horizontal')
            self.collision('vertical')
            
            

            
          
    class Personagem(pygame.sprite.Sprite):
        def __init__(self,charx,chary,obstaculo):
            super().__init__()
            self.image = pygame.image.load(r'graphics/char.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = charx
            self.rect.y = chary
            self.direction = pygame.math.Vector2()
            self.speed = 2
            self.old_rect = self.rect.copy()

            self.hp = 100

            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.obstaculo = obstaculo

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

                
            
        def update(self): #tem que chamar update por conta do sprite.Group
            self.old_rect = self.rect.copy()
            self.entrada()

            self.pos.x += self.direction.x * self.speed
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.pos.y += self.direction.y * self.speed
            self.rect.y = round(self.pos.y)
            self.collision('vertical')

        def cortar(self):
            if v.equipamento:
                spriteszinhos = pygame.sprite.spritecollide(self, self.obstaculo, True)
                if spriteszinhos:
                    if v.randomgen() == 'monstro':
                        
                        for sprites in spriteszinhos:
                            v.monstrinhox = sprites.old_rect.x
                            v.monstrinhoy = sprites.old_rect.y
                            
                            v.criar_monstro = True
                    elif v.randomgen() == 'dinheiro':
                        pass

        def equipamento(self):
            self.image = pygame.image.load(r'graphics/charequipado.png').convert_alpha()
            v.equipamento = True

        def ataque(self,grupo):
            monstrinho = pygame.sprite.spritecollide(self, grupo, False)
            for monstro in monstrinho:
                monstro.hp -= 5
                if monstro.hp == 0:
                    pygame.sprite.Group.remove(monstro_grupo,monstro)
            

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
            
      

    ############################

    #Criando o Sprite.group######
    arvore_grupo = pygame.sprite.Group()
    monstro_grupo = pygame.sprite.Group()
    char_grupo = pygame.sprite.Group()
    todos_grupos = [arvore_grupo,monstro_grupo]
    ############################

    #Criando os itens###########
    char = Personagem(350,200,arvore_grupo)
    char_grupo.add(char)
    machadinho_no_chao = pygame.image.load(r'graphics/machado.png')
    machado_rect = machadinho_no_chao.get_rect(topleft=(350,300))

    ############################
    #game loop##################
    pygame.display.update()

    v.run_game = True

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


    while v.run_game:
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
                    char.ataque(monstro_grupo)
                    if v.top == True:
                        char.cortar()
                        char.rect.y -= 5
                    if v.bottom == True:                    
                        char.cortar()
                        char.rect.y += 5
                    if v.right == True:
                        char.cortar()
                        char.rect.x += 5
                    if v.left == True:                    
                        char.cortar()
                        char.rect.x -= 5

                        
                    if char.cortar() == True:
                        pass

                    
                    if char.rect.colliderect(machado_rect):
                        v.machadinho = False
                        char.equipamento()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    char.rect.y -= 5

            if v.criar_monstro == True:
                monstro = Monstro(v.monstrinhox, v.monstrinhoy, char,char_grupo)
                monstro_grupo.add(monstro)
                v.criar_monstro = False
        
        
       
       
        char.morreu()
        char_grupo.draw(tela)
        arvore_grupo.draw(tela)
        monstro_grupo.draw(tela)
        monstro_grupo.update()
        char_grupo.update()
        
        
        
        pygame.display.update()


        frames.tick(60)
    ############################
