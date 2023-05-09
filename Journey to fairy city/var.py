import pygame, random, sys

pygame.init()
pygame.font.init()

screen_width = 800 #largura
screen_height = 600 #altura
tela = pygame.display.set_mode((screen_width,screen_height))

# Define as cores utilizadas no jogo
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

#variaveis do jogo

top = False
bottom = False
right = False
left = False
criar_monstro = False
equipamento = False
monstrinhox = 0
monstrinhoy = 0
hit_right = False
hit_left = False
hit_bottom = False
hit_top = False
machadinho = True
menu = True
game = False
run_game = False
posinitix = screen_width / 2
posinitiy = screen_height / 2
score = 0
money = 0

#variaveis do mapa
Norte = 0
Sul = 0
Leste = 0
Oeste = 0

fase_atual = 'FN'

#grupos de sprites
attack_grupo = pygame.sprite.Group()
arvore_grupo = pygame.sprite.Group()
monstro_grupo = pygame.sprite.Group()
char_grupo = pygame.sprite.Group()
borda_grupo = pygame.sprite.Group()

#fontes pro HUD
font = pygame.font.SysFont('Arial', 30)

def randomgen():
    randomizando = random.randrange(0,10)
    if randomizando <= 5:
        return 'monstro'
    elif randomizando > 5:
        return 'dinheiro'

def randomtree():
    randomgen1 = random.randrange(0,750,50)
    randomgen2 = random.randrange(0,550,50)
    randomgen_location = (randomgen1,randomgen2)

    return randomgen_location
