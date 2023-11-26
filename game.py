import pygame, random, sys
import var as v
import classes as c


#Inicializando o pygame
pygame.init()

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

#Inicializar a class player
player1 = c.Player(10,10,tela)
pg.add(player1)
todos_sprites.add(player1)

#Inicializar outras classes importantes
damage_show = c.Damage_Show() #Class para mostrar dano causado na tela
menu = c.Menu() #Class do menu do jogo

#Inicializar a class Equipamentos
equip = c.Equipamentos()

#Definir equipamento inicial (usar isso no craft para mudar os equipamentos)
equip.definir_nivel()
equip.definir_equipamentos(player1)

#Inicializar a class Inimigos PARA TESTE
inimigos1 = c.Inimigos(200,200)
inimigos1.tipo() #define o sprite quando o inimigo é criado, portanto usar junto com o init da class
todos_sprites.add(inimigos1)
ig.add(inimigos1)

#Inicializar a class NPC
#Em andamento - receber class 'player1' e 'equip'

while run_game:
        tela.fill((255,255,255)) #provisório para cor da tela
        frames.tick(60)#Define frame rate
        delta_time = frames.tick(60)/1000 #Define o delta_time com base no frame rate

        
        for event in pygame.event.get():
                #Função do botão de sair do jogo
                if event.type == pygame.QUIT: 
                        run_game = False
                        pygame.quit()
                        sys.exit()
                #Detecta se os botões são clicados
                elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_e: #Caso o botão clicado seja 'e', realiza ação
                                        player1.key_down = True
                                        
                                elif event.key == pygame.K_ESCAPE:
                                        v.abrir_menu = True
                                        while v.abrir_menu:
                                                menu.abrir(tela)
                                                for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                                pygame.quit()
                                                                sys.exit()
                                                        elif event.type == pygame.KEYDOWN:
                                                                if event.key == pygame.K_ESCAPE:
                                                                        v.abrir_menu = False
                                                                        
                                elif event.key == pygame.K_i: #inventario
                                        pass
                                elif event.key == pygame.K_m: #mapa
                                        pass
                                elif event.key == pygame.K_q: #quests
                                        pass
                                       
                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_e: #Caso o botão solto seja 'e', realiza ação
                                player1.key_down = False #para o ataque
                                ataque = c.Attack() #Class de ataque do personagem
                                ag.add(ataque)
                                ataque.criar(player1.rect.x, player1.rect.y, player1.ataque_dir, player1.nivel)
                                #criar aqui o ataque em sí. chamando a class ataque?
                                
        
        

                        
                        
                
        #desenhar sprites
        todos_sprites.draw(tela)
        ag.draw(tela)
        
        #atualizar classes de sprites        
        pg.update(delta_time, tela)
        ig.update(tela,player1)
        ag.update(player1,'npc',ig,'arvore',damage_show,delta_time,tela,font_damage)

        #detectar as colisões
        player1.colisao(ig,damage_show,font_damage,delta_time,tela)
        

        #Atualiza tela
        pygame.display.update()
        
        v.axe_equip = True #provisório - irá definir se o personagem está equipado ao pegar o machado do chão!
