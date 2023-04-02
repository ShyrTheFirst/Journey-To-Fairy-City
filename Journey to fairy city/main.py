import pygame, sys
import var as v


pygame.init()
tela = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Journey to the Fairy City")
frames = pygame.time.Clock()




fundo = pygame.image.load(r'graphics/menu.png')
iniciar = pygame.image.load(r'graphics/start.png')
sair = pygame.image.load(r'graphics/quit.png')
tela.blit(fundo,(0,0))
pygame.display.update()


while v.menu:
    tela.blit(fundo,(0,0))
    tela.blit(iniciar,(150,350))
    tela.blit(sair,(450,350))
    clicou_iniciar = pygame.Rect(150,350,250,50)
    clicou_sair = pygame.Rect(450,350,250,50)
    
    if pygame.mouse.get_pressed() == (1,0,0):
        mouseposition = pygame.mouse.get_pos()
        if clicou_iniciar.collidepoint(mouseposition):
            v.menu = False
            v.game = True
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



