import pygame, sys
import var as v
import pickle



#Inicializando o pygame
pygame.init()
pygame.mixer.init()

#Definindo os sons
menumusic = pygame.mixer.Sound(r'sounds\musica_fundo.mp3')
pygame.mixer.Sound.set_volume(menumusic,0.05)
pygame.mixer.Sound.play(menumusic)

#Definições das fontes
pygame.font.init()
font_menu = pygame.font.Font(r'fonts\3270.ttf',10)

#Definições da tela do jogo
pygame.display.set_icon(pygame.image.load(r'Graphics\Menu\icon.png'))
tela = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Journey to the Fairy City")

frames = pygame.time.Clock()

#esconder o mouse dentro do jogo para mudar o icone
pygame.mouse.set_visible(False)
mouse_button = pygame.image.load(r'Graphics\HUD\mouse_button.png')
mouse_rect = mouse_button.get_rect()

#Definindo os botões e o fundo do menu
fundo = pygame.image.load(r'Graphics\Menu\menu.png')
iniciar = pygame.image.load(r'Graphics\Menu\start.png')
sair = pygame.image.load(r'Graphics\Menu\quitgame.png')
load = pygame.image.load(r'Graphics\Menu\loadgame.png')

loadgame_menu = False



while v.menu:
    tela.blit(fundo,(0,0))
    tela.blit(iniciar,(100,200))
    tela.blit(load,(100,300))
    tela.blit(sair,(500,500))
    
    clicou_iniciar = pygame.Rect(100,200,200,45)    
    clicou_loadgame = pygame.Rect(100,300,200,45)
    clicou_sair = pygame.Rect(500,500,200,45)

    clicou_load1 = pygame.Rect(600,225,120,100)
    clicou_load2 = pygame.Rect(600,325,120,100)

    mousepos = pygame.mouse.get_pos()
    if clicou_iniciar.collidepoint(mousepos):
        iniciar = pygame.image.load(r'Graphics\Menu\start_click.png')
    else:
        iniciar = pygame.image.load(r'Graphics\Menu\start.png')
        
    if clicou_loadgame.collidepoint(mousepos):
        load = pygame.image.load(r'Graphics\Menu\loadgame_click.png')
    else:
        load = pygame.image.load(r'Graphics\Menu\loadgame.png')

    if clicou_sair.collidepoint(mousepos):
        sair = pygame.image.load(r'Graphics\Menu\quitgame_click.png')
    else:
        sair = pygame.image.load(r'Graphics\Menu\quitgame.png')

    if loadgame_menu == True:       
        
        #rect:
        pygame.draw.rect(tela,(255,255,255),clicou_load1)
        #delimitador da rect:
        pygame.draw.rect(tela,(0,0,0),clicou_load1,1)
        
        #Rect:
        pygame.draw.rect(tela,(255,255,255),clicou_load2)
        #delimitador da rect:
        pygame.draw.rect(tela,(0,0,0),clicou_load2,1)

        #mostrar dia e hora do save
        try:
                with open('save1.dat','rb') as arquivo1:
                    dados1 = pickle.load(arquivo1)
                    savetime_load = dados1['save_time']
                    texto_render = font_menu.render(str(savetime_load),1,(0,0,0))
                    tela.blit(texto_render,(605,275))                
        except FileNotFoundError:
                pass

        try:
                with open('save2.dat','rb') as arquivo2:
                    dados2 = pickle.load(arquivo2)
                    savetime_load2 = dados2['save_time']
                    texto_render = font_menu.render(str(savetime_load),1,(0,0,0))
                    tela.blit(texto_render,(605,375))
        except FileNotFoundError:
                pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseposition = pygame.mouse.get_pos()
            if clicou_loadgame.collidepoint(mouseposition):
                load = pygame.image.load(r'Graphics\Menu\loadgame_clicked.png')
                if not loadgame_menu:
                    loadgame_menu = True
                else:
                    loadgame_menu = False
    
    if pygame.mouse.get_pressed() == (1,0,0):      
        if clicou_load1.collidepoint(mouseposition) and loadgame_menu == True:
            dados_jogo = {}
            try:
                with open('save1.dat', 'rb') as arquivo:
                    v.dados_jogo = pickle.load(arquivo)
                    pygame.mixer.Sound.stop(menumusic)
                    v.menu = False
                    v.run_game = True
                    v.loadgame_from_menu = True
                    import game
            except FileNotFoundError:
                pass

        if clicou_load2.collidepoint(mouseposition) and loadgame_menu == True:
            dados_jogo = {}
            try:
                with open('save2.dat', 'rb') as arquivo:
                    v.dados_jogo = pickle.load(arquivo)
                    pygame.mixer.Sound.stop(menumusic)
                    v.menu = False
                    v.run_game = True
                    v.loadgame_from_menu = True
                    import game
            except FileNotFoundError:
                pass
            
        
        if clicou_iniciar.collidepoint(mouseposition):
            iniciar = pygame.image.load(r'Graphics\Menu\start_clicked.png')
            v.menu = False
            v.run_game = True
            pygame.mixer.Sound.stop(menumusic)
            import game
            
        if clicou_sair.collidepoint(mouseposition):
            v.menu = False
            pygame.quit()
            sys.exit()

    


    #Definir mouse do jogo
    mouse_rect.center = pygame.mouse.get_pos()
    tela.blit(mouse_button, mouse_rect)
    
    pygame.display.update()
    frames.tick(60)
