import pygame, random, sys
import var as v
import classes as c


#Inicializando o pygame
pygame.init()
pygame.mixer.init()

#esconder o mouse dentro do jogo
pygame.mouse.set_visible(False)

#definindo os sons
pygame.mixer.music.load(r'sounds\musica_fundo.mp3')
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1)

som_ataque = pygame.mixer.Sound(r'sounds\ataque.mp3')
som_acao = pygame.mixer.Sound(r'sounds\personagem.wav')
som_pegar_machado = pygame.mixer.Sound(r'sounds\pegar_machado.mp3')
abrir_inventario = pygame.mixer.Sound(r'sounds\inventario.mp3')
abrir_mapa = pygame.mixer.Sound(r'sounds\mapa.mp3')
batalha = pygame.mixer.Sound(r'sounds\batalha.mp3')
fim_do_jogo = pygame.mixer.Sound(r'sounds\fim_de_jogo.mp3')

#Criando janela do jogo
tela_Larg = 800
tela_Alt = 600

#Definições da tela do jogo
tela = pygame.display.set_mode((tela_Larg,tela_Alt))
pygame.display.set_caption('Journey to the Fairy City')
frames = pygame.time.Clock()

#Definições das fontes
pygame.font.init()
font_grande = pygame.font.Font(r'fonts/teutonic.ttf',30)
font_damage = pygame.font.Font(r'fonts/augusta.ttf',15)
font_quest = pygame.font.Font(r'fonts/augusta.ttf',22)

#loop do jogo
run_game = True


#Grupos de sprites
pg = pygame.sprite.Group() #Grupo do jogador
todos_sprites = pygame.sprite.Group() #Grupo pra desenhar sprites
ig = pygame.sprite.Group() #Grupo dos inimigos
ag = pygame.sprite.Group() #Grupo de ataques
arvores = pygame.sprite.Group() #Grupo das arvores
NPCs = pygame.sprite.Group() #Grupo dos NPCs
bordas = pygame.sprite.Group() #Grupo das bordas do mapa

obstaculos = pygame.sprite.Group() #Grupo para verificar colisões

#Inicializar a class player
player1 = c.Player(360,350,tela)
pg.add(player1)
todos_sprites.add(player1)

#Inicializar outras classes importantes
damage_show = c.Damage_Show() #Class para mostrar dano causado na tela
menu = c.Menu() #Class do menu do jogo
HUD = c.HUD()
mapa_jogo = c.Mapa_jogo()

#Criando as bordas do mapa
borda_topo = c.Borda_topo()
borda_baixo = c.Borda_baixo()
borda_esquerda = c.Borda_esquerda()
borda_direita = c.Borda_direita()

#Adicionando bordas no grupo
bordas.add(borda_topo)
bordas.add(borda_baixo)
bordas.add(borda_esquerda)
bordas.add(borda_direita)

#Inicializar a class Equipamentos
equip = c.Equipamentos()

#Definir equipamento inicial (usar isso no craft para mudar os equipamentos)
equip.definir_nivel()
equip.definir_equipamentos(player1)

#Inicializar a class NPC
#Em andamento - receber class 'player1' e 'equip'

#Criar as arvores do primeiro mapa
c.gerar_arvore(arvores, obstaculos, tela)

while run_game:
        tela.blit(mapa_jogo.mapa_atual,(0,0)) #blita a imagem de fundo do jogo
        
        frames.tick(60)#Define frame rate
        delta_time = frames.tick(60)/1000 #Define o delta_time com base no frame rate
        
        #Gerar machado no chão ao iniciar, para o personagem pegar
        if v.axe_equip == False:
                machadinho_no_chao = pygame.image.load(r'Graphics\Mapa\machado.png') ######################### PRECISO REDESENHAR ESSE SPRITE
                machado_rect = machadinho_no_chao.get_rect(topleft=(350,300)) #rect pra fins de colisão
                tela.blit(machadinho_no_chao,(350,300))
                
                if player1.rect.colliderect(machado_rect): #detectar a colisão com o machado e pegar automaticamente
                        pygame.mixer.Sound.set_volume(som_pegar_machado,0.05)
                        pygame.mixer.Sound.play(som_pegar_machado)
                        v.axe_equip = True

        if v.gerando_arvores == True:
                c.gerar_arvore(arvores, obstaculos, tela) #Gera as arvores toda vez que muda de mapa
        
        for event in pygame.event.get():
                #Função do botão de sair do jogo
                if event.type == pygame.QUIT: 
                        run_game = False
                        pygame.quit()
                        sys.exit()
                        
                #Detecta se os botões são clicados
                elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_e: #Caso o botão clicado seja 'e', realiza ação
                                        if not v.in_city:
                                                player1.key_down = True
                                        if v.in_city:
                                                pygame.mixer.Sound.set_volume(som_acao,0.05)
                                                pygame.mixer.Sound.play(som_acao)
                                        
                                elif event.key == pygame.K_ESCAPE:
                                        v.abrir_menu = True
                                        while v.abrir_menu:
                                                menu.abrir(tela)
                                                ########################################### CRIAR AQUI SETINHA DIRECIONAL PRA ESCOLHER AS OPÇÕES SEM O USO DO MOUSE
                                                for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                                pygame.quit()
                                                                sys.exit()
                                                        elif event.type == pygame.KEYDOWN:
                                                                if event.key == pygame.K_ESCAPE:
                                                                        v.abrir_menu = False
                                                                        
                                elif event.key == pygame.K_i: #inventario
                                        pygame.mixer.Sound.set_volume(abrir_inventario,0.05)
                                        pygame.mixer.Sound.play(abrir_inventario)
                                        open_inventario = True
                                        while open_inventario:
                                                for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                                pygame.quit()
                                                                sys.exit()
                                                        if event.type == pygame.KEYDOWN:
                                                                if event.key == pygame.K_i:
                                                                        pygame.mixer.Sound.stop(abrir_inventario)
                                                                        open_inventario = False
                                                HUD.inventario(tela,player1,font_quest)
                                                pygame.display.update()
                                                
                                elif event.key == pygame.K_m: #mapa
                                        pygame.mixer.Sound.set_volume(abrir_mapa,0.05)
                                        pygame.mixer.Sound.play(abrir_mapa)
                                        open_mapa = True
                                        while open_mapa:
                                                for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                                pygame.quit()
                                                                sys.exit()
                                                        if event.type == pygame.KEYDOWN:
                                                                if event.key == pygame.K_m:
                                                                        open_mapa = False
                                                HUD.bussola(tela,font_grande)
                                                pygame.display.update()
                                                
                                elif event.key == pygame.K_q: #quests
                                        pygame.mixer.Sound.set_volume(abrir_mapa,0.05)
                                        pygame.mixer.Sound.play(abrir_mapa)
                                        open_quests = True
                                        while open_quests:
                                                for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                                pygame.quit()
                                                                sys.exit()
                                                        if event.type == pygame.KEYDOWN:
                                                                if event.key == pygame.K_q:
                                                                        open_quests = False
                                                HUD.quest(tela)
                                                pygame.display.update()
                                       
                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_e: #Caso o botão solto seja 'e', realiza ação
                                player1.key_down = False #para o ataque
                                if v.axe_equip == True and v.in_city == False:
                                        ataque = c.Attack() #Class de ataque do personagem
                                        ag.add(ataque)
                                        ataque.criar(player1.rect.x, player1.rect.y, player1.ataque_dir, player1.nivel)
                                        pygame.mixer.Sound.set_volume(som_ataque,0.05)
                                        pygame.mixer.Sound.play(som_ataque)

        #testando conceitos
        #render_text = font_grande.render(str(player1.momentum),1,(0,0,0))
        #tela.blit(render_text, (300,300))           
                
        #desenhar sprites
        todos_sprites.draw(tela)
        ag.draw(tela)
        arvores.draw(tela)
        bordas.draw(tela)
        
        #atualizar classes de sprites
        pg.update(delta_time, tela)
        ig.update(tela, player1)
        ag.update(todos_sprites, player1, NPCs, ig, arvores, damage_show, delta_time, tela, font_damage, obstaculos)
        bordas.update(pg, player1, arvores, ig, mapa_jogo, NPCs)

        #detectar as colisões
        player1.colisao(obstaculos, damage_show, font_damage, delta_time, tela)

        if player1.health <= 0:
                pygame.mixer.Sound.set_volume(fim_do_jogo,0.1)
                pygame.mixer.Sound.play(fim_do_jogo)
                #definir endgame

        #Atualiza tela
        pygame.display.update()

