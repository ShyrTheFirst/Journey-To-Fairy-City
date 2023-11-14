import pygame, random, sys
import var as v
import classes as c




def Criar_npc(pos,image,quest,craft,loja):
    npc = c.NPC(pos,image,quest,craft,loja)
    v.npc_grupo.add(npc)
    v.colisao_grupo.add(npc)

def Criar_muro(pos):
    muro = c.Muro(pos)
    v.muro_grupo.add(muro)
    v.colisao_grupo.add(muro)

def Criar_casa(pos):
    Casinha = c.Casa(pos)
    v.colisao_grupo.add(Casinha)
    v.casa_grupo.add(Casinha)

def Criar_ferreiro(pos):
    Ferreirinho = c.Ferreiro(pos)
    v.colisao_grupo.add(Ferreirinho)
    v.casa_grupo.add(Ferreirinho)
    
    
