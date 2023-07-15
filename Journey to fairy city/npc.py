import pygame, random, sys
import var as v
import classes as c




def Criar_npc(pos,image,quest,craft):
    npc = c.NPC(pos,image,quest,craft)
    v.npc_grupo.add(npc)
    v.colisao_grupo.add(npc)

def Criar_muro(pos):
    muro = c.Muro(pos)
    v.muro_grupo.add(muro)
    v.colisao_grupo.add(muro)
