import pygame, sys
import var as v
import pickle


try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

pygame.init()
pygame.mixer.init()
menumusic = pygame.mixer.Sound(r'sounds\musica_fundo.mp3')
pygame.mixer.Sound.set_volume(menumusic,0.05)
pygame.mixer.Sound.play(menumusic)
tela = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Journey to the Fairy City")
frames = pygame.time.Clock()




fundo = pygame.image.load(r'graphics/menu.png')
iniciar = pygame.image.load(r'graphics/start.png')
sair = pygame.image.load(r'graphics/quit.png')
load = pygame.image.load(r'graphics/menuload.png')
tela.blit(fundo,(0,0))
pygame.display.update()


while v.menu:
    tela.blit(fundo,(0,0))
    tela.blit(iniciar,(150,350))
    tela.blit(sair,(450,350))
    tela.blit(load,(200,400))
    clicou_iniciar = pygame.Rect(150,350,250,50)
    clicou_sair = pygame.Rect(450,350,250,50)
    clicou_loadgame = pygame.Rect(200,400,250,50)
    
    if pygame.mouse.get_pressed() == (1,0,0):
        mouseposition = pygame.mouse.get_pos()
        if clicou_loadgame.collidepoint(mouseposition):
            #load
            dados_jogo = {}
            try:
                with open('savegame.dat', 'rb') as arquivo:
                    dados_jogo = pickle.load(arquivo)
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
                pygame.mixer.Sound.stop(menumusic)
                import game
            except FileNotFoundError:
                pass #Mostrar que não há save para carregar
        if clicou_iniciar.collidepoint(mouseposition):
            v.menu = False
            pygame.mixer.Sound.stop(menumusic)
            import game
        if clicou_sair.collidepoint(mouseposition):
            v.menu = False
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    pygame.display.update()
    frames.tick(60)
