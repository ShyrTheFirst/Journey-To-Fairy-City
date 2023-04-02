import random

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


def randomgen():
    randomizando = random.randrange(0,10)
    if randomizando <= 5:
        return 'monstro'
    elif randomizando > 5:
        return 'dinheiro'

