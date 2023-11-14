import random as rd
import var as v


#Gerador randomico para quantidade de mobs
def gerar_quant_mobs(x,y):
    quant = rd.randrange(x,y)
    return quant

#Gerador randomico para escolher mob
def escolher_mob():
    grupo_mobs = ['spiders','wolfs','bears']
    mob = rd.randrange(0,3)
    return grupo_mobs[mob]


#Configurar dialogo de quests SE NECESSÁRIO
def dialogo_quest():
    if v.quest_num == 0:
        frase_quest0 = "Could you help us?"
        return frase_quest0
    if v.quest_num == 1:
        frase_quest1 = "Lá lá lá lá"
        return frase_quest1
    elif v.quest_num == 2:
        frase_quest2 = "Le le le le"
        return frase_quest2
    elif v.quest_num == 3:
        frase_quest3 = "Li li li li"
        return frase_quest3

#Blita texto na tela
def escrever_dialogo(texto,pos):
    texto_render = v.font_quest.render(texto,1,v.white)
    v.tela.blit(texto_render,pos)



