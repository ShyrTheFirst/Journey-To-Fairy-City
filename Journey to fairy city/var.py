import pygame, random, sys


#Inicia o pygame e as fonts
pygame.init()
pygame.font.init()

#Definições da tela
screen_width = 800 #largura
screen_height = 600 #altura
tela = pygame.display.set_mode((screen_width,screen_height))

# Define as cores utilizadas no jogo
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

#Variaveis para verificar utilidade*
CUSTOM = pygame.USEREVENT +1
custom_event1 = pygame.event.Event(CUSTOM)
damage_rect_x = 0
damage_rect_y = 0
damage_sprite = 0

#variaveis do jogo
delta_time = 0

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


####Switch dos mob
aranha_on = True
lobo_on = False
urso_on = False
rainha_aranha_on = False

####personagem
score_aranha = 0
score_lobo = 0
score_urso = 0
score_rainha_aranha = 0

#Quests
quest_num = 0
quest_em_progresso = False
score_atual_quest = 0
score_alvo_quest = 0
mob_atual = ''

score = 0
exp = 0
level = 1
exp_mob = 0

####inventario
gold = 0
troncos = 0
metais = 0
tecidos = 0
couros = 0




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
muro_grupo = pygame.sprite.Group()
colisao_grupo = pygame.sprite.Group()
npc_grupo = pygame.sprite.Group()
casa_grupo = pygame.sprite.Group()

#fontes pro HUD
font = pygame.font.Font(r'fonts/teutonic.ttf',30)
font_inv = pygame.font.Font(r'fonts/teutonic.ttf',15)
font_quest = pygame.font.Font(r'fonts/teutonic.ttf',22)
fonte_augusta = pygame.font.Font(r'fonts/augusta.ttf',26)


#Geradores randomicos
def randomgen():
    randomizando = random.randrange(0,10)
    if randomizando <= 4:
        return 'monstro'
    elif randomizando > 4:
        return 'troncos'

def randomtree():
    randomgen1 = random.randrange(0,750,50)
    randomgen2 = random.randrange(0,550,50)
    randomgen_location = (randomgen1,randomgen2)

    return randomgen_location



    
