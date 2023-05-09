import pygame, random, sys
import var as v
import classes as c

#Inicializando o pygame
pygame.init()

#Criando janela do jogo
tela = pygame.display.set_mode((v.screen_width,v.screen_height))
pygame.display.set_caption('Journey to the Fairy City')
frames = pygame.time.Clock()


#define as imagens usadas no jogo 

arvore = pygame.image.load(r'graphics/arvore.png')



### cria as bordas para mudar de mapa
borda_topo = c.Borda_topo
borda_baixo = c.Borda_baixo
borda_esquerda = c.Borda_esquerda
borda_direita = c.Borda_direita
v.borda_grupo.add(borda_topo)
v.borda_grupo.add(borda_baixo)
v.borda_grupo.add(borda_esquerda)
v.borda_grupo.add(borda_direita)

#mais facil que mudar todos os char por ai KKK
char = c.char
v.char_grupo.add(char)

#gera o machado no chão pra iniciar o jogo!
machadinho_no_chao = pygame.image.load(r'graphics/machado.png')
machado_rect = machadinho_no_chao.get_rect(topleft=(350,300))

pygame.display.update()


#cria as arverezinha
c.gerar_arvore()

#cria o HUD todo
hud = c.HUD()

#inicia o jogo de fato
v.run_game = True

while v.run_game:
        frames.tick(60)

        #define o mapa do jogo
        if v.fase_atual == 'FN':
            fundo = c.FN.mapa_atual
        elif v.fase_atual == 'FA':
            fundo = c.FA.mapa_atual
        elif v.fase_atual == 'FE':
            fundo = c.FE.mapa_atual
        #blita o mapa
        tela.blit(fundo,(0,0))

        #define se o personagem ta com ou sem machado
        if v.machadinho:
            tela.blit(machadinho_no_chao,(350,300))

        #padrão pro jogo rodar no while
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v.run_game = False
                pygame.quit()
                sys.exit()
            #identifica os cliques de teclas, pra ataque ou pra pegar o machado #### futuramente irá identificar interações com NPC, uso da bussola e inventário
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if v.machadinho == True:
                        pass
                    else:
                        #realiza o ataque!
                        char.attack()
                    #Se o player ta sem o machado e usa o E perto dele, identifica e coleta o machado!
                    if char.rect.colliderect(machado_rect):
                        v.machadinho = False
                        #isso aqui vai precisar sofrer umas alterações quando o update do inventario vier
                        char.equipamento()
            #faz o que o nome diz... cria monstrinho haha quando derruba arvore, há chances de gerar monstro, e isso acontece aqui
            if v.criar_monstro == True:
                monstro = c.Monstro(v.monstrinhox, v.monstrinhoy)
                v.monstro_grupo.add(monstro)
                v.criar_monstro = False

        
        #desenhando os sprites na tela e atualizando eles o tempo todo!
        v.char_grupo.draw(tela)
        v.borda_grupo.draw(tela)
        v.arvore_grupo.draw(tela)
        v.monstro_grupo.draw(tela)
        v.attack_grupo.draw(tela)
        v.attack_grupo.update(0,0)
        v.monstro_grupo.update(0,0)
        v.borda_grupo.update()
        v.char_grupo.update()
        hud.draw()
        
        pygame.display.update()

        #definindo o fim do jogo. Aqui precisa mudar - Quem sabe criar essa definição em uma parte separada? 
        if char.health <= 0:
            #muda o sprite do personagem pra morto e gera a tela de fim de jogo
            char.image = pygame.image.load(r'graphics/charmorto.png').convert_alpha()
            endgame = pygame.image.load(r'graphics/endgame.png')
            tela.blit(endgame,(0,0))
            pygame.display.update()
            v.char_grupo.draw(tela)
            #pra funcionar o clique de reiniciar o jogo
            while char.health <= 0:
                #o basico pra fechar o jogo e bla bla bla
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        v.run_game = False
                        pygame.quit()
                        sys.exit()

                #gera as mensagens na tela de fim de jogo
                continue_game = pygame.image.load(r'graphics/continue.png')
                tela.blit(continue_game,(220,300))
                sim_bot = pygame.image.load(r'graphics/YES.png')
                nao_bot = pygame.image.load(r'graphics/NO.png')
                tela.blit(sim_bot,(350,350))
                tela.blit(nao_bot,(450,350))
                clicou_sim = pygame.Rect(350,350,50,50)
                clicou_nao = pygame.Rect(450,350,50,50)
                pygame.display.update()

                #identifica os cliques do mouse, pra saber onde to clicando
                if pygame.mouse.get_pressed() == (1,0,0):
                    #me da a pos do mouse
                    mouseposition = pygame.mouse.get_pos()
                    #verifica se a pos do mouse ta na pos de algum botao
                    if clicou_sim.collidepoint(mouseposition):
                        #junta todos os grupos em um só... devia ter feito um all? devia. Mas moh trampo agora
                        grupos = [v.attack_grupo, v.char_grupo, v.arvore_grupo, v.monstro_grupo]
                        for grupo in grupos:
                            for sprites in grupo:
                                #mata tudo pra começar do zero
                                sprites.kill()

                        #zera todas as vars
                        v.score = 0
                        v.money = 0
                        v.Norte = 0
                        v.Sul = 0
                        v.Leste = 0
                        v.Oeste = 0

                        #volta o mapa pra fase 0, ou pra onde precisar voltar dependendo do save game... o que significa que as vars ali em cima vão mudar e é por isso que o endgame precisa ser um arquivo separado.
                        if v.fase_atual == 'FN':
                            mudar = c.FN.mudar_mapa() ######CARREGAR ULTIMO JOGO SALVO - QUANDO IMPLEMENTADO
                            fundo = c.FN.mapa_atual
                        elif v.fase_atual == 'FA':
                            mudar = c.FA.mudar_mapa() ######CARREGAR ULTIMO JOGO SALVO - QUANDO IMPLEMENTADO
                            fundo = c.FA.mapa_atual
                        elif v.fase_atual == 'FE':
                            mudar = c.FE.mudar_mapa() ######CARREGAR ULTIMO JOGO SALVO - QUANDO IMPLEMENTADO
                            fundo = c.FE.mapa_atual

                        #reseta a vida do char... mesma questão dos vars acima
                        char.health = 50

                        #garante que o jogador não vai começar com o machadinho, então zera tudo
                        v.machadinho = True
                        v.equipamento = False

                        #regenera as arvores. #somosdapaz #todospelanatureza
                        c.gerar_arvore()
                        
                        #não sei se isso faz diferença... mas assim funcionou, então ta bom
                        v.char_grupo.add(char)
                        char.image = pygame.image.load(r'graphics/char.png').convert_alpha()

                        #redefine a pos do personagem pra pos inicial
                        char.pos.x = v.posinitix
                        char.pos.y = v.posinitiy
                        pygame.display.update()

                    #se clicou em não o jogo só fecha e tchau
                    if clicou_nao.collidepoint(mouseposition):
                        pygame.quit()
                        sys.exit()
