import random as rd
import tkinter as tk
import numpy as np

#Parametres

longueur = 3
largeur = 5
Npro = 2
Npred = 1


#Etape 1

def naissances(Nproies, Npred):
    cases_libres = []
    for ligne in range(longueur+2):
        for colonne in range(largeur+2):
            nature_case = terrain[0,ligne,colonne]
            if nature_case == 0:
                cases_libres.append(ligne*(largeur+2)+colonne)
    nouvelles_proies = []
    rd.shuffle(cases_libres)
    while Nproies != 0:
        nouvelles_proies.append(cases_libres.pop())
        Nproies -= 1
    #nouvelles_proies = rd.sample(cases_libres, Nproies)
    for i in nouvelles_proies:
        ligne_nouvelle_proie = i//(largeur+2)
        colonne_nouvelle_proie = i%(largeur+2)
        nouveau_terrain[0, ligne_nouvelle_proie, colonne_nouvelle_proie] = 1
        nouveau_terrain[1, ligne_nouvelle_proie, colonne_nouvelle_proie] = rd.randint(3,9)
    nouveaux_predateurs = rd.sample(cases_libres, Npred)
    for i in nouveaux_predateurs:
        ligne_nouveau_predateur = i//(largeur+2)
        colonne_nouveau_predateur = i%(largeur+2)
        nouveau_terrain[0, ligne_nouveau_predateur, colonne_nouveau_predateur] = 2
        nouveau_terrain[1, ligne_nouveau_predateur, colonne_nouveau_predateur] = rd.randint(5,12)
    return nouveau_terrain

 




#Creation terrain

terrain = np.zeros((2, longueur+2, largeur+2))
#etage 0 : nature de la case (0:libre, 1:proie, 2:predateur, 3:inaccessible)
#etage 1: âge (et 3 si case inaccessible pour repère)
nouveau_terrain = terrain.copy()
for ligne in range(longueur+2):
    for colonne in range(largeur+2):
        nature_case = terrain[0,ligne,colonne]
        if ligne == 0 or ligne == longueur+1 or colonne == 0 or colonne == largeur+1:
            nouveau_terrain[0,ligne,colonne] = 3
            nouveau_terrain[1,ligne,colonne] = 3
terrain = nouveau_terrain
nouveau_terrain = terrain.copy()
naissances(Npro, Npred)

print(nouveau_terrain)

def deplacement(ligne, colonne):
    # 0 1 2
    # 7   3
    # 6 5 4
    cases_adjacentes_dispo = []
    if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
        cases_adjacentes_dispo.append(0)
    if terrain[0,ligne-1,colonne] == 0 and nouveau_terrain[0,ligne-1,colonne] == 0:
        cases_adjacentes_dispo.append(1)
    if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
        cases_adjacentes_dispo.append(2)
    if terrain[0,ligne,colonne+1] == 0 and nouveau_terrain[0,ligne,colonne+1] == 0:
        cases_adjacentes_dispo.append(3)
    if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
        cases_adjacentes_dispo.append(4)
    if terrain[0,ligne+1,colonne] == 0 and nouveau_terrain[0,ligne+1,colonne] == 0:
        cases_adjacentes_dispo.append(5)
    if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
        cases_adjacentes_dispo.append(6)
    if terrain[0,ligne,colonne-1] == 0 and nouveau_terrain[0,ligne,colonne-1] == 0:
        cases_adjacentes_dispo.append(7)
    if cases_adjacentes_dispo != []:
        nouvelle_case = rd.sample(cases_adjacentes_dispo, 1)
        if nouvelle_case == 0:
            nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
        elif nouvelle_case == 1:
            nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
        elif nouvelle_case == 2:
            nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
        elif nouvelle_case == 3:
            nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
        elif nouvelle_case == 4:
            nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
        elif nouvelle_case == 5:
            nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
        elif nouvelle_case == 6:
            nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
        elif nouvelle_case == 7:
            nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
            nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne]
            nouveau_terrain[0, ligne, colonne] = 0
            nouveau_terrain[1, ligne, colonne] = 0
    return nouveau_terrain


def etape(Fpro, Fpred):
    naissances(Fpro, Fpred)
    for ligne in range(longueur+2):
        for colonne in range(largeur+2):
            nature_case = nouveau_terrain[0,ligne, colonne]
            if nature_case == 1 or nature_case == 2:
                nouveau_terrain[1, ligne, colonne] -= 1
                if nouveau_terrain[1, ligne, colonne] == 0:
                    nouveau_terrain[0, ligne, colonne] == 0
                deplacement(ligne, colonne)
    return nouveau_terrain

etape(1, 0)

print(nouveau_terrain)