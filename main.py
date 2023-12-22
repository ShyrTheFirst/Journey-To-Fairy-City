import pygame, sys
import var as v
import pickle



#
pygame.init()
pygame.mixer.init()

#
menumusic = pygame.mixer.Sound(r'sounds\musica_fundo.mp3')
pygame.mixer.Sound.set_volume(menumusic,0.05)
pygame.mixer.Sound.play(menumusic)

#Definições das fontes
pygame.font.init()
font_menu = pygame.font.Font(r'fonts\3270.ttf',10)

#
tela = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Journey to the Fairy City")
frames = pygame.time.Clock()

#esconder o mouse dentro do jogo para mudar o icone
pygame.mouse.set_visible(False)
mouse_button = pygame.image.load(r'Graphics\HUD\mouse_button.png')
mouse_rect = mouse_button.get_rect()

#
fundo = pygame.image.load(r'Graphics\Menu\menu.png')
iniciar = pygame.image.load(r'Graphics\Menu\start.png')
sair = pygame.image.load(r'Graphics\Menu\quitgame.png')
load = pygame.image.load(r'Graphics\Menu\loadgame.png')

loadgame_menu = False



while v.menu:
    tela.blit(fundo,(0,0))
    tela.blit(iniciar,(200,200))
    tela.blit(load,(200,300))
    tela.blit(sair,(450,500))
    
    clicou_iniciar = pygame.Rect(245,205,320,50)
    pygame.draw.rect(tela,(255,255,255),clicou_iniciar,1) #Test da rect
    
    clicou_loadgame = pygame.Rect(245,305,320,50)
    pygame.draw.rect(tela,(255,255,255),clicou_loadgame,1)#Test da rect

    clicou_sair = pygame.Rect(522,500,260,45)
    pygame.draw.rect(tela,(255,255,255),clicou_sair,1)#Test da rect

    clicou_load1 = pygame.Rect(600,225,120,100)
    clicou_load2 = pygame.Rect(600,325,120,100)

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
                pass #Mostrar que não há save para carregar

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
                pass #Mostrar que não há save para carregar
            
        
        if clicou_iniciar.collidepoint(mouseposition):
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