import pygame
import var as v

####################################NÃO IMPLEMENTADO

pygame.init()
pygame.font.init()

fonte = v.fonte_augusta


def esperar(milissegundos):
    time = pygame.time.get_ticks()
    tempo_de_espera = time+milissegundos
    while time <= tempo_de_espera:
        time = pygame.time.get_ticks()

def escrever_por_letra(frase,posx,posy,cor,tempo):
    escrever = ' '
    for letra in frase:
        escrever += letra
        mostrar_escrita = fonte.render(escrever,1,cor)
        limpar_escrita_anterior = pygame.Rect(posx,posy,v.screen_width,v.screen_height)
        pygame.draw.rect(v.tela,(0,0,0),limpar_escrita_anterior)#mudar por blit do fundo?
        v.tela.blit(mostrar_escrita,(posx,posy))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        esperar(tempo)


##################teste:
#frase = "Frase de teste para verificar se a def funciona "
#escrever_por_letra(frase,100,100,(255,255,255),100)
        
