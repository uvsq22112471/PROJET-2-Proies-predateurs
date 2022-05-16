import random as rd
import tkinter as tk
import numpy as np
import time

#Parametres

longueur = 30
largeur = 30
Npro = 5
Npred = 2
nbArbres = 10
Erepro = 10
AgeMinProies = 3
AgeMaxProies = 5
AgeMinPredateurs = 7
AgeMaxPredateurs = 12
nbTours = 1

def init():
    nouveau_terrain = initialisation()
    grille = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N):
        x = (i - 1) * LARGEUR_CASE
        for j in range(1, N):
            y = (j - 1) * HAUTEUR_CASE
            if nouveau_terrain[0, i, j] == 0:
                col = "white"
            elif nouveau_terrain[0, i, j] == 1:
                col = "blue"
            elif nouveau_terrain[0, i, j] == 2:
                col = "red"
            else:
                col = "black"
            carre = canvas.create_rectangle(x, y, x+LARGEUR_CASE, y+HAUTEUR_CASE, fill=col, outline = "grey50")
            grille[i][j] = carre
    return nouveau_terrain

#Creation terrain

def initialisation():
    global nbArbres
    terrain = np.zeros((3, longueur+4, largeur+4))
    #etage 0 : nature de la case (0:libre, 1:proie, 2:predateur, 3:inaccessible)
    #etage 1 : âge (et 3 si case inaccessible pour repère)
    #etage 2 : énergie prédateurs
    nouveau_terrain = terrain.copy()
    """On crée le tableau (avec un tableau numpy, plus élégant d'utilisation que les listes imbriquées et plus optimal pour la mémoire que les listes car non-extensible
    On aurait tout aussi bien pu avoir, au lieu de "terrain[1, ligne, colonne]" une syntaxe plus classique "terrain[ligne][colonne][1]"."""
    arbres = []
    while nbArbres != 0:
        arbres.append([rd.randint(2, longueur+2), rd.randint(2, largeur+2)])
        nbArbres -= 1
    for ligne in range(longueur+4):
        for colonne in range(largeur+4):
            if ligne == 0 or ligne == longueur+2 or ligne == 1 or ligne == longueur+3 or colonne == 0 or colonne == largeur+2 or colonne == 1 or colonne == largeur+3 or ([ligne, colonne] in arbres == True): #On crée des cases inaccessibles sur les bords
                terrain[0,ligne,colonne] = 3
    naissances(terrain, nouveau_terrain, Npro, Npred)
    return nouveau_terrain #les return sont non nécessaires au vu de la structure en tableaux, mais le code est plus lisible ainsi donc nous faisons le choix de les garder

def naissances(terrain, nouveau_terrain, Nproies, Npred):

    """Permet la génération des proies et prédateurs à des positions aléatoires"""
    cases_libres = []
    for ligne in range(longueur+4):
        for colonne in range(largeur+4):
            nature_case = terrain[0,ligne,colonne]
            if nature_case == 0:
                cases_libres.append(ligne*(largeur+4)+colonne) #indexation des cases par un indice plus compliqué mais adapté à un tableau unidimensionnel
    rd.shuffle(cases_libres) #On mélange pour obtenir un indice aléatoire
    nouvelles_proies = [] #Les prochaines lignes permettent d'obtenir un tirage sans remise dans les cases libres
    while Nproies != 0:
        nouvelles_proies.append(cases_libres.pop())
        Nproies -= 1
    #nouvelles_proies = rd.sample(cases_libres, Nproies)
    for i in nouvelles_proies:
        ligne_nouvelle_proie = i//(largeur+4)
        colonne_nouvelle_proie = i%(largeur+4)
        nouveau_terrain[0, ligne_nouvelle_proie, colonne_nouvelle_proie] = 1
        nouveau_terrain[1, ligne_nouvelle_proie, colonne_nouvelle_proie] = rd.randint(AgeMinProies, AgeMaxProies)
    nouveaux_predateurs = rd.sample(cases_libres, Npred) #Tirage sans remise mais ne modifie pas cases_libres car on ne s'en resservira pas
    for i in nouveaux_predateurs:
        ligne_nouveau_predateur = i//(largeur+4)
        colonne_nouveau_predateur = i%(largeur+4)
        nouveau_terrain[0, ligne_nouveau_predateur, colonne_nouveau_predateur] = 2
        nouveau_terrain[1, ligne_nouveau_predateur, colonne_nouveau_predateur] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        nouveau_terrain[2, ligne_nouveau_predateur, colonne_nouveau_predateur] = rd.randint(5, nouveau_terrain[1, ligne_nouveau_predateur, colonne_nouveau_predateur]-1) #On est bornés par la formule Epre<Apre
    return nouveau_terrain 

terrain = initialisation()
nouveau_terrain = terrain.copy() #On travaille sur les deux terrains en parallèle pour effectuer les modifications
def deplacement(ligne, colonne, terrain, nouveau_terrain):
    """Cette fonction assure le déplacement des animaux.
    Le déplacement est aussi aleatoire que possible"""
    
    
    #Attention, on rentre ici dans des disjonctions de cas longues et répétitives, mais elles assurent un déplacement vraiment aléatoire
    #deplacement
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
    if cases_adjacentes_dispo == []:
        return nouveau_terrain #on s'assure qu'un déplacement est effectivement possible
    nouvelle_case = cases_adjacentes_dispo[rd.randint(0, len(cases_adjacentes_dispo)-1)]#on chosit un déplacement au hasard parmi ceux possibles
    if nouvelle_case == 0:
        nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne-1, colonne-1] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif nouvelle_case == 1:
        nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne-1, colonne] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif nouvelle_case == 2:
        nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne-1, colonne+1] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif nouvelle_case == 3:
        nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne, colonne+1] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif nouvelle_case == 4:
        nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne+1, colonne+1] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif nouvelle_case == 5:
        nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne+1, colonne] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif nouvelle_case == 6:
        nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne+1, colonne-1] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif nouvelle_case == 7:
        nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne, colonne-1] = nouveau_terrain[2, ligne, colonne]-1
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    return nouveau_terrain

def manger(ligne, colonne, verslaproie, terrain, nouveau_terrain):
    if verslaproie == 0:
        nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne-1, colonne-1] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif verslaproie == 1:
        nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne-1, colonne] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif verslaproie == 2:
        nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne-1, colonne+1] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif verslaproie == 3:
        nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne, colonne+1] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif verslaproie == 4:
        nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne+1, colonne+1] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif verslaproie == 5:
        nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne+1, colonne] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif verslaproie == 6:
        nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne+1, colonne-1] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0
    elif verslaproie == 7:
        nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
        nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne]-1
        nouveau_terrain[2, ligne, colonne-1] = nouveau_terrain[2, ligne, colonne]+4
        nouveau_terrain[0, ligne, colonne] = 0
        nouveau_terrain[1, ligne, colonne] = 0
        nouveau_terrain[2, ligne, colonne] = 0

def chasse(ligne, colonne, terrain, nouveau_terrain):
    #nouvelle_case= 42 #valeur juste pour ne pas déclencher d'erreur
    """Correspond au parametre flair de l'enonce.
    Permet les deplacements optimaux des predateurs pour manger des proies
    Si une proie se situe dans les environs, cette fonction remplace deplacement"""
    #le predateur peut sentir la proie
    #    8 9 10 
    # 19 0 1 2 11
    # 18 7   3 12
    # 17 6 5 4 13
    #   16 15 14
    cases_avec_proie = []
    if nouveau_terrain[0,ligne-1,colonne-1] == 1:
        cases_avec_proie.append([0, 1])
    if nouveau_terrain[0,ligne-1,colonne] == 1:
        cases_avec_proie.append([1, 0])
    if nouveau_terrain[0,ligne-1,colonne+1] == 1:
        cases_avec_proie.append([2, 1])
    if terrain[0,ligne,colonne+1] == 1:
        cases_avec_proie.append([3, 0])
    if terrain[0,ligne+1,colonne+1] == 1:
        cases_avec_proie.append([4, 1])
    if terrain[0,ligne+1,colonne] == 1:
        cases_avec_proie.append([5, 0])
    if terrain[0,ligne+1,colonne-1] == 1:
        cases_avec_proie.append([6, 1])
    if nouveau_terrain[0,ligne,colonne-1] == 1:
        cases_avec_proie.append([7, 0])
    if nouveau_terrain[0,ligne-1,colonne-1] == 1:
        cases_avec_proie.append([8, 3])
    if nouveau_terrain[0,ligne-1,colonne] == 1:
        cases_avec_proie.append([9, 2])
    if nouveau_terrain[0,ligne-1,colonne+1] == 1:
        cases_avec_proie.append([10, 3])
    if nouveau_terrain[0,ligne,colonne+1] == 1:
        cases_avec_proie.append([11, 3])
    if terrain[0,ligne,colonne+2] == 1:
        cases_avec_proie.append([12, 2])
    if terrain[0,ligne-1,colonne+2] == 1:
        cases_avec_proie.append([13, 3])
    if terrain[0,ligne-2,colonne+1] == 1:
        cases_avec_proie.append([14, 3])
    if terrain[0,ligne-2,colonne] == 1:
        cases_avec_proie.append([15, 2])
    if terrain[0,ligne-2,colonne-1] == 1:
        cases_avec_proie.append([16, 3])
    if terrain[0,ligne-1,colonne-2] == 1:
        cases_avec_proie.append([17, 3])
    if nouveau_terrain[0,ligne+1,colonne+1] == 1:
        cases_avec_proie.append([18, 2])
    if nouveau_terrain[0,ligne+1,colonne+1] == 1:
        cases_avec_proie.append([19, 3]) 
        
    if cases_avec_proie == []:
        deplacement(ligne, colonne, terrain, nouveau_terrain)
        return nouveau_terrain
    else:
        proies_proches0 = []
        proies_proches1 = []
        proies_proches2 = []
        for i in range(len(cases_avec_proie)):
            if cases_avec_proie[i][1] == 0:
                proies_proches0.append(cases_avec_proie[0])
            elif cases_avec_proie[i][1] == 1:
                proies_proches1.append(cases_avec_proie[0])
            elif cases_avec_proie[i][1] == 2:
                proies_proches2.append(cases_avec_proie[0])
        if proies_proches0 != []:
            ind = rd.randint(0, len(proies_proches0)-1)
            verslaproie = proies_proches0[ind][0]
        elif proies_proches1 != []:
            ind = rd.randint(0, len(proies_proches1)-1)
            verslaproie = proies_proches1[ind][0]
        elif proies_proches2 != []:
            ind = rd.randint(0, len(proies_proches2)-1)
            verslaproie = proies_proches2[ind][0]
        else:
            ind = rd.randint(0, len(cases_avec_proie)-1)
            verslaproie = cases_avec_proie[ind][0]

        if verslaproie < 8:
            manger(ligne, colonne, verslaproie, terrain, nouveau_terrain)
        
        elif verslaproie == 8:
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
                cases_acces_dispo.append(0)
            if terrain[0,ligne-1,colonne] == 0 and nouveau_terrain[0,ligne-1,colonne] == 0:
                cases_acces_dispo.append(1)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]#on chosit un déplacement le plus rapide parmi ceux possibles
            if nouvelle_case == 0:
                nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 1:
                nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain
        
        
        elif verslaproie == 9:
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
                cases_acces_dispo.append(0)
            if terrain[0,ligne-1,colonne] == 0 and nouveau_terrain[0,ligne-1,colonne] == 0:
                cases_acces_dispo.append(1)
            if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
                cases_acces_dispo.append(2)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 0:
                nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne]- 1
                nouveau_terrain[2, ligne-1, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 1:
                nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne]- 1
                nouveau_terrain[2, ligne-1, colonne] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 2:
                nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain
        
        
        elif verslaproie == 10:
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne] == 0 and nouveau_terrain[0,ligne-1,colonne] == 0:
                cases_acces_dispo.append(1)
            if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
                cases_acces_dispo.append(2)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 1:
                nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            elif nouvelle_case == 2:
                nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain




        elif verslaproie == 11:
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
                cases_acces_dispo.append(2)
            if terrain[0,ligne,colonne+1] == 0 and nouveau_terrain[0,ligne,colonne+1] == 0:
                cases_acces_dispo.append(3)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 2:
                nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 3:
                nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain





        elif verslaproie == 12:
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
                cases_acces_dispo.append(2)
            if terrain[0,ligne,colonne+1] == 0 and nouveau_terrain[0,ligne,colonne+1] == 0:
                cases_acces_dispo.append(3)
            if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
                cases_acces_dispo.append(4)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 2:
                nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 3:
                nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 4:
                nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain


        elif verslaproie == 13:
            cases_acces_dispo = []
            if terrain[0,ligne,colonne+1] == 0 and nouveau_terrain[0,ligne,colonne+1] == 0:
                cases_acces_dispo.append(3)
            if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
                cases_acces_dispo.append(4)
            if cases_acces_dispo == []:
                return nouveau_terrain
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 3:
                nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 4:
                nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain


        elif verslaproie == 14:
            cases_acces_dispo = []
            if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
                cases_acces_dispo.append(4)
            if terrain[0,ligne+1,colonne] == 0 and nouveau_terrain[0,ligne+1,colonne] == 0:
                cases_acces_dispo.append(5)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 4:
                nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 5:
                nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain

        elif verslaproie == 15:
            cases_acces_dispo = []
            if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
                cases_acces_dispo.append(4)
            if terrain[0,ligne+1,colonne] == 0 and nouveau_terrain[0,ligne+1,colonne] == 0:
                cases_acces_dispo.append(5)
            if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
                cases_acces_dispo.append(6)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 4:
                nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 5:
                nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 6:
                nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain



        elif verslaproie == 16:
            cases_acces_dispo = []
            if terrain[0,ligne+1,colonne] == 0 and nouveau_terrain[0,ligne+1,colonne] == 0:
                cases_acces_dispo.append(5)
            if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
                cases_acces_dispo.append(6)
            if cases_acces_dispo == []:
                return nouveau_terrain
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 5:
                nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 6:
                nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain
        
        elif verslaproie == 17:
            cases_acces_dispo = []
            if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
                cases_acces_dispo.append(6)
            if terrain[0,ligne,colonne-1] == 0 and nouveau_terrain[0,ligne,colonne-1] == 0:
                cases_acces_dispo.append(7)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 6:
                nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne+1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 7:
                nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain
    
        
        elif verslaproie == 18:
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
                cases_acces_dispo.append(0)
            if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
                cases_acces_dispo.append(6)
            if terrain[0,ligne,colonne-1] == 0 and nouveau_terrain[0,ligne,colonne-1] == 0:
                cases_acces_dispo.append(7)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 0:
                nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 6:
                nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne+1, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 7:
                nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain

        elif verslaproie == 19:
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
                cases_acces_dispo.append(0)
            if terrain[0,ligne,colonne-1] == 0 and nouveau_terrain[0,ligne,colonne-1] == 0:
                cases_acces_dispo.append(7)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = cases_acces_dispo[rd.randint(0, len(cases_acces_dispo)-1)]
            if nouvelle_case == 0:
                nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne-1, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            elif nouvelle_case == 7:
                nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne] - 1
                nouveau_terrain[2, ligne, colonne-1] = nouveau_terrain[2, ligne, colonne] - 1
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            return nouveau_terrain
    return nouveau_terrain
def fuite(ligne, colonne, terrain, nouveau_terrain):
    """Permet la fuite optimale des proies quand elles detectent un predateur a proximite
    Remplace deplacement si un predateur est detecte"""
    #le predateur peut sentir la proie
    #      8  
    #    4 0 5 
    # 11 3   1 9 
    #    7 2 6 
    #      10
    cases_avec_predateur = []
    if nouveau_terrain[0,ligne-1,colonne-1] == 2:
        cases_avec_predateur.append([4, 1])
    if nouveau_terrain[0,ligne-1,colonne] == 2:
        cases_avec_predateur.append([0, 0])
    if nouveau_terrain[0,ligne-1,colonne+1] == 2:
        cases_avec_predateur.append([5, 1])
    if terrain[0,ligne,colonne+1] == 2:
        cases_avec_predateur.append([1, 0])
    if terrain[0,ligne+1,colonne+1] == 2:
        cases_avec_predateur.append([6, 1])
    if terrain[0,ligne+1,colonne] == 2:
        cases_avec_predateur.append([2, 0])
    if terrain[0,ligne+1,colonne-1] == 2:
        cases_avec_predateur.append([7, 1])
    if nouveau_terrain[0,ligne,colonne-1] == 2:
        cases_avec_predateur.append([3, 0])
    if nouveau_terrain[0,ligne-1,colonne] == 2:
        cases_avec_predateur.append([8, 2])
    if terrain[0,ligne,colonne+2] == 2:
        cases_avec_predateur.append([9, 2])
    if terrain[0,ligne-2,colonne] == 2:
        cases_avec_predateur.append([10, 2])
    if nouveau_terrain[0,ligne+1,colonne+1] == 2:
        cases_avec_predateur.append([11, 2])
    if cases_avec_predateur == []:
        deplacement(ligne, colonne, terrain, nouveau_terrain)
    else:
        pred_proches0 = []
        pred_proches1 = []
        pred_proches2 = []
        for i in range(len(cases_avec_predateur)):
            if cases_avec_predateur[i][1] == 0:
                pred_proches0.append(cases_avec_predateur[0])
            elif cases_avec_predateur[i][1] == 1:
                pred_proches1.append(cases_avec_predateur[0])
            elif cases_avec_predateur[i][1] == 2:
                pred_proches2.append(cases_avec_predateur[0])
        if pred_proches0 != []:
            pred = rd.sample(pred_proches0, 1)
        elif pred_proches1 != []:
            pred = rd.sample(pred_proches1, 1)
        elif pred_proches2 != []:
            pred = rd.sample(pred_proches2, 1)
        else:
            pred = rd.sample(cases_avec_predateur, 1)
        #if 3>= predateur_plus_proche -> paralysé : pas de mouvement
        
        if pred == 4:
            if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
                nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                return nouveau_terrain
            cases_acces_dispo = []
            if terrain[0,ligne,colonne+1] == 0 and nouveau_terrain[0,ligne,colonne+1] == 0:
                cases_acces_dispo.append(1)
            if terrain[0,ligne+1,colonne] == 0 and nouveau_terrain[0,ligne+1,colonne] == 0:
                cases_acces_dispo.append(2)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 1:
                nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            elif nouvelle_case == 2:
                nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain
        
        elif pred == 5:
            if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
                nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            cases_acces_dispo = []
            if terrain[0,ligne+1,colonne] == 0 and nouveau_terrain[0,ligne+1,colonne] == 0:
                cases_acces_dispo.append(2)
            if terrain[0,ligne,colonne-1] == 0 and nouveau_terrain[0,ligne,colonne-1] == 0:
                cases_acces_dispo.append(3)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 2:
                nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            elif nouvelle_case == 3:
                nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain
        
        elif pred == 6:
            if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
                nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                return nouveau_terrain
            cases_acces_dispo = []
            if terrain[0,ligne,colonne-1] == 0 and nouveau_terrain[0,ligne,colonne-1] == 0:
                cases_acces_dispo.append(3)
            if terrain[0,ligne-1,colonne] == 0 and nouveau_terrain[0,ligne-1,colonne] == 0:
                cases_acces_dispo.append(0)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 3:
                nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0               
            elif nouvelle_case == 0:
                nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain
        
        elif pred == 7:
            if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
                nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne] == 0 and nouveau_terrain[0,ligne-1,colonne] == 0:
                cases_acces_dispo.append(0)
            if terrain[0,ligne,colonne+1] == 0 and nouveau_terrain[0,ligne,colonne+1] == 0:
                cases_acces_dispo.append(1)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 0:
                nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0                
            elif nouvelle_case == 1:    
                nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain

        elif pred == 8:
            if terrain[0,ligne+1,colonne] == 0 and nouveau_terrain[0,ligne+1,colonne] == 0:
                nouveau_terrain[0, ligne+1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                return nouveau_terrain
            cases_acces_dispo = []
            if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
                cases_acces_dispo.append(6)
            if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
                cases_acces_dispo.append(7)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 6:
                nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            elif nouvelle_case == 7:
                nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain
        
        elif pred == 9:
            if terrain[0,ligne,colonne-1] == 0 and nouveau_terrain[0,ligne,colonne-1] == 0:
                nouveau_terrain[0, ligne, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                return nouveau_terrain
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
                cases_acces_dispo.append(4)
            if terrain[0,ligne+1,colonne-1] == 0 and nouveau_terrain[0,ligne+1,colonne-1] == 0:
                cases_acces_dispo.append(7)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 4:
                nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            elif nouvelle_case == 7:
                nouveau_terrain[0, ligne+1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain

        elif pred == 10:
            
            if terrain[0,ligne-1,colonne] == 0 and nouveau_terrain[0,ligne-1,colonne] == 0:
                nouveau_terrain[0, ligne-1, colonne] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                return nouveau_terrain
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne-1] == 0 and nouveau_terrain[0,ligne-1,colonne-1] == 0:
                cases_acces_dispo.append(4)
            if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
                cases_acces_dispo.append(5)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 4:
                nouveau_terrain[0, ligne-1, colonne-1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne-1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            elif nouvelle_case == 5:
                nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain
        
        elif pred == 11:
            if terrain[0,ligne,colonne+1] == 0 and nouveau_terrain[0,ligne,colonne+1] == 0:
                nouveau_terrain[0, ligne, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                return nouveau_terrain
            cases_acces_dispo = []
            if terrain[0,ligne-1,colonne+1] == 0 and nouveau_terrain[0,ligne-1,colonne+1] == 0:
                cases_acces_dispo.append(5)
            if terrain[0,ligne+1,colonne+1] == 0 and nouveau_terrain[0,ligne+1,colonne+1] == 0:
                cases_acces_dispo.append(6)
            if cases_acces_dispo == []:
                return nouveau_terrain
            nouvelle_case = rd.sample(cases_acces_dispo, 1)
            if nouvelle_case == 5:
                nouveau_terrain[0, ligne-1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne-1, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            elif nouvelle_case == 6:
                nouveau_terrain[0, ligne+1, colonne+1] = nouveau_terrain[0, ligne, colonne]
                nouveau_terrain[1, ligne+1, colonne+1] = nouveau_terrain[1, ligne, colonne]
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
            return nouveau_terrain
    return nouveau_terrain

def etape(terrain, nouveau_terrain):
    """Element répété tout au long du programme combinant vieillissement, déplacement et reproduction"""
    terrain = nouveau_terrain
    nouveau_terrain = 0
    nouveau_terrain = terrain.copy()
    #naissances(Fpro, Fpred)
    #terrain = nouveau_terrain
    #nouveau_terrain = terrain.copy()
    for ligne in range(longueur+2):
        for colonne in range(largeur+2):
            if nouveau_terrain[1, ligne, colonne] == 0 or (terrain[0, ligne, colonne] == 2 and nouveau_terrain[2, ligne, colonne]==0):
                nouveau_terrain[0, ligne, colonne] = 0
                nouveau_terrain[1, ligne, colonne] = 0
                nouveau_terrain[2, ligne, colonne] = 0
            if terrain[0, ligne, colonne] == 1:
                reproduction(1, ligne, colonne, terrain, nouveau_terrain)
                fuite(ligne, colonne, terrain, nouveau_terrain)
            elif terrain[0, ligne, colonne] == 2:
                reproduction(2, ligne, colonne, terrain, nouveau_terrain)
                chasse(ligne, colonne, terrain, nouveau_terrain)
    return nouveau_terrain

def reproduction(nature, ligne, colonne, terrain, nouveau_terrain):
    """Assure la reproduction de deux individus de la même espèce placés sur des cases adjacentes"""
    partenaires_potentiels = [] #On cherche si les cases adjacentes abritent un partenaire potentiel
    if terrain[0, ligne-1, colonne] == nature:
        if nature == 1 or (terrain[2, ligne-1, colonne] >= Erepro):
            partenaires_potentiels.append(1)
    if terrain[0, ligne, colonne+1] == nature:
        if nature == 1 or (terrain[2, ligne, colonne+1] >= Erepro):
            partenaires_potentiels.append(3)
    if terrain[0, ligne+1, colonne] == nature:
        if nature == 1 or (terrain[2, ligne+1, colonne] >= Erepro):
            partenaires_potentiels.append(5)
    if terrain[0, ligne, colonne-1] == nature:
        if nature == 1 or (terrain[2, ligne, colonne-1] >= Erepro):
            partenaires_potentiels.append(7)

    if partenaires_potentiels == []:
        return terrain
    rd.shuffle(partenaires_potentiels)
    partenaire = partenaires_potentiels.pop()
    position_possible_enfant = []
    # A B C D E
    # F G H I J
    # K L p N O
    # P Q R S T
    # U V W X Y

    if partenaire == 1:
        # B C D
        # G b I
        # L a N
        # Q R S
        if terrain[0, ligne-2, colonne-1] == 0:
            position_possible_enfant.append("B")
        if terrain[0, ligne-2, colonne] == 0:
            position_possible_enfant.append("C")
        if terrain[0, ligne-2, colonne+1] == 0:
            position_possible_enfant.append("D")
        if terrain[0, ligne-1, colonne+1] == 0:
            position_possible_enfant.append("I")
        if terrain[0, ligne, colonne+1] == 0:
            position_possible_enfant.append("N")
        if terrain[0, ligne+1, colonne+1] == 0:
            position_possible_enfant.append("S")
        if terrain[0, ligne+1, colonne] == 0:
            position_possible_enfant.append("R")
        if terrain[0, ligne+1, colonne-1] == 0:
            position_possible_enfant.append("Q")
        if terrain[0, ligne, colonne-1] == 0:
            position_possible_enfant.append("L")
        if terrain[0, ligne-1, colonne-1] == 0:
            position_possible_enfant.append("G")
    
    elif partenaire == 3:
        # G H I J
        # L a b O
        # Q R S T
        if terrain[0, ligne-1, colonne-1] == 0:
            position_possible_enfant.append("G")
        if terrain[0, ligne-1, colonne] == 0:
            position_possible_enfant.append("H")
        if terrain[0, ligne-1, colonne+1] == 0:
            position_possible_enfant.append("I")
        if terrain[0, ligne-1, colonne+2] == 0:
            position_possible_enfant.append("J")
        if terrain[0, ligne, colonne+2] == 0:
            position_possible_enfant.append("O")
        if terrain[0, ligne+1, colonne+2] == 0:
            position_possible_enfant.append("T")
        if terrain[0, ligne+1, colonne+1] == 0:
            position_possible_enfant.append("S")
        if terrain[0, ligne+1, colonne] == 0:
            position_possible_enfant.append("R")
        if terrain[0, ligne+1, colonne-1] == 0:
            position_possible_enfant.append("Q")
        if terrain[0, ligne, colonne-1] == 0:
            position_possible_enfant.append("L")
    
    elif partenaire == 5:
        # G H I
        # L a N
        # Q b S
        # V W X
        if terrain[0, ligne-1, colonne-1] == 0:
            position_possible_enfant.append("G")
        if terrain[0, ligne-1, colonne] == 0:
            position_possible_enfant.append("H")
        if terrain[0, ligne-1, colonne+1] == 0:
            position_possible_enfant.append("I")
        if terrain[0, ligne, colonne+1] == 0:
            position_possible_enfant.append("N")
        if terrain[0, ligne+1, colonne+1] == 0:
            position_possible_enfant.append("S")
        if terrain[0, ligne+2, colonne+1] == 0:
            position_possible_enfant.append("X")
        if terrain[0, ligne+2, colonne] == 0:
            position_possible_enfant.append("W")
        if terrain[0, ligne+2, colonne-1] == 0:
            position_possible_enfant.append("V")
        if terrain[0, ligne-1, colonne-1] == 0:
            position_possible_enfant.append("Q")
        if terrain[0, ligne, colonne-1] == 0:
            position_possible_enfant.append("L")

    elif partenaire == 7:
        # F G H I
        # K b a N
        # P Q R S
        if terrain[0, ligne-1, colonne-2] == 0:
            position_possible_enfant.append("F")
        if terrain[0, ligne-1, colonne-1] == 0:
            position_possible_enfant.append("G")
        if terrain[0, ligne-1, colonne] == 0:
            position_possible_enfant.append("H")
        if terrain[0, ligne-1, colonne+1] == 0:
            position_possible_enfant.append("I")
        if terrain[0, ligne, colonne+1] == 0:
            position_possible_enfant.append("N")
        if terrain[0, ligne+1, colonne+1] == 0:
            position_possible_enfant.append("S")
        if terrain[0, ligne+1, colonne] == 0:
            position_possible_enfant.append("R")
        if terrain[0, ligne+1, colonne-1] == 0:
            position_possible_enfant.append("Q")
        if terrain[0, ligne+1, colonne-2] == 0:
            position_possible_enfant.append("P")
        if terrain[0, ligne, colonne-2] == 0:
            position_possible_enfant.append("K")

    if position_possible_enfant != []:
        position_enfant = rd.sample(position_possible_enfant, 1)
        if position_enfant == "B":
            nouveau_terrain[0, ligne-2, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-2, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-2, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-2, colonne-1] = rd.randint(3, nouveau_terrain[1, ligne-2, colonne-1]-1)
        if position_enfant == "C":
            nouveau_terrain[0, ligne-2, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-2, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-2, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-2, colonne] = rd.randint(3, nouveau_terrain[1, ligne-2, colonne]-1)
        if position_enfant == "D":
            nouveau_terrain[0, ligne-2, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-2, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-2, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-2, colonne+1] = rd.randint(3, nouveau_terrain[1, ligne-2, colonne+1]-1)
        if position_enfant == "F":
            nouveau_terrain[0, ligne-1, colonne-2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne-2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne-2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-1, colonne-2] = rd.randint(3, nouveau_terrain[1, ligne-1, colonne-2]-1)
        if position_enfant == "G":
            nouveau_terrain[0, ligne-1, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-1, colonne-1] = rd.randint(3, nouveau_terrain[1, ligne-1, colonne-1]-1)
        if position_enfant == "H":
            nouveau_terrain[0, ligne-1, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-1, colonne] = rd.randint(3, nouveau_terrain[1, ligne-1, colonne]-1)
        if position_enfant == "I":
            nouveau_terrain[0, ligne-1, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-1, colonne+1] = rd.randint(3, nouveau_terrain[1, ligne-1, colonne+1]-1)
        if position_enfant == "J":
            nouveau_terrain[0, ligne-1, colonne+2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne+2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne+2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne-1, colonne+2] = rd.randint(3, nouveau_terrain[1, ligne-1, colonne+2]-1)
        if position_enfant == "K":
            nouveau_terrain[0, ligne, colonne-2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne-2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne-2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne, colonne-2] = rd.randint(3, nouveau_terrain[1, ligne, colonne-2]-1)
        if position_enfant == "L":
            nouveau_terrain[0, ligne, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne, colonne-1] = rd.randint(3, nouveau_terrain[1, ligne, colonne-1]-1)
        if position_enfant == "N":
            nouveau_terrain[0, ligne, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne, colonne+1] = rd.randint(3, nouveau_terrain[1, ligne, colonne+1]-1)
        if position_enfant == "O":
            nouveau_terrain[0, ligne, colonne+2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne+2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne+2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne, colonne+2] = rd.randint(3, nouveau_terrain[1, ligne, colonne+2]-1)
        if position_enfant == "P":
            nouveau_terrain[0, ligne+1, colonne-2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne-2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne-2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+1, colonne-2] = rd.randint(3, nouveau_terrain[1, ligne+1, colonne-2]-1)
        if position_enfant == "Q":
            nouveau_terrain[0, ligne-2, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+1, colonne-1] = rd.randint(3, nouveau_terrain[1, ligne+1, colonne-1]-1)
        if position_enfant == "R":
            nouveau_terrain[0, ligne+1, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+1, colonne] = rd.randint(3, nouveau_terrain[1, ligne+1, colonne]-1)
        if position_enfant == "S":
            nouveau_terrain[0, ligne+1, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+1, colonne+1] = rd.randint(3, nouveau_terrain[1, ligne+1, colonne+1]-1)
        if position_enfant == "T":
            nouveau_terrain[0, ligne+1, colonne+2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne+2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne+2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+1, colonne+2] = rd.randint(3, nouveau_terrain[1, ligne+1, colonne+2]-1)
        if position_enfant == "V":
            nouveau_terrain[0, ligne+2, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+2, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+2, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+2, colonne-1] = rd.randint(3, nouveau_terrain[1, ligne+2, colonne-1]-1)
        if position_enfant == "W":
            nouveau_terrain[0, ligne+2, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+2, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+2, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+2, colonne] = rd.randint(3, nouveau_terrain[1, ligne+2, colonne]-1)
        if position_enfant == "X":
            nouveau_terrain[0, ligne+2, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+2, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+2, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
                nouveau_terrain[2, ligne+2, colonne+1] = rd.randint(3, nouveau_terrain[1, ligne+2, colonne+1]-1)

#boucle principale :

"""nouveau_terrain = initialisation()
while nbTours != 0:
    etape()
    time.sleep(2)
    nbTours -= 1"""
    
#INTERFACE GRAPHIQUE

#L'interface affiche une grille mais nous n'avons pas reussi a etablir le lien entre la grille tkinter et le reste du programme.
#En effet l'un des membres a rencontré de gros problèmes informatique, et il se trouve qu'il s'agissait de la personne chargée de cette partie..
#Nous allons tenter de resoudre ce probleme avant la presentation
""" from tkinter import *


#La partie ci-dessous s'appuie fortement sur la correction du projet tas de sable.
# taille de la grille carrée
N = 30
# dimensions du canvas et de la grille
LARGEUR = 700
HAUTEUR = 700
LARGEUR_CASE = LARGEUR // N
HAUTEUR_CASE = HAUTEUR // N



racine = tk.Tk()
racine.title("Simulation proies predateurs")

# définition des widgets
canvas = tk.Canvas(racine, width=LARGEUR, height=HAUTEUR)

bouton_start = tk.Button(racine, text="Start")
def init():
    new_terrain = initialisation()
    grille = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N+1):
        x = (i - 1) * LARGEUR_CASE
        for j in range(1, N+1):
            y = (j - 1) * HAUTEUR_CASE
            if new_terrain[0, i, j] == 0:
                col = "white"
            elif new_terrain[0, i, j] == 1:
                col = "blue"
            elif new_terrain[0, i, j] == 2:
                col = "red"
            else:
                col = "black"
            carre = canvas.create_rectangle(x, y, x+LARGEUR_CASE, y+HAUTEUR_CASE, fill=col, outline = "grey50")
            grille[i][j] = carre

init()
canvas.grid(row=0, column=1, rowspan=6)

# boucle prinicipale
racine.mainloop() """

N = longueur
M = largeur

WIDTH = 700
HEIGHT = 700
LARGEUR_CASE = WIDTH // N
HAUTEUR_CASE = HEIGHT // N
grille = []
root = tk.Tk()

root.title("Simulation proies predateurs")

canvas = tk.Canvas(root, bg = "black", height=HEIGHT, width=WIDTH)

map = canvas.create_rectangle(0,0, WIDTH, HEIGHT, fill = "white")

for i in range(N):
    for j in range(M):
        grille.append([[0]*N]*M) 

def init():
    nouveau_terrain = initialisation()
    grille = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N):
        x = (i - 1) * LARGEUR_CASE
        for j in range(1, N):
            y = (j - 1) * HAUTEUR_CASE
            if nouveau_terrain[0, i, j] == 0:
                col = "white"
            elif nouveau_terrain[0, i, j] == 1:
                col = "blue"
            elif nouveau_terrain[0, i, j] == 2:
                col = "red"
            else:
                col = "black"
            carre = canvas.create_rectangle(x, y, x+LARGEUR_CASE, y+HAUTEUR_CASE, fill=col, outline = "grey50")
            grille[i][j] = carre
    return nouveau_terrain

def save_fct():
    fic = open("save.txt", "w")
    fic.write(str(nouveau_terrain) + "\n")
    fic.close()

def load_fct():
    global N
    fic = open("save.txt", "r")
    size = fic.readline()
    N = len(size)
    canvas.delete()
    initialisation()
    i = j = 0
    for ligne in fic:
        nouveau_terrain[ligne] = int(ligne)
        j += 1
        if j == N:
            j = 0
            i += 1
    fic.close()

#Boutons

def boucle(terrain, nouveau_terrain, grille):
    nouveau_terrain = np.array(etape(terrain, nouveau_terrain))
    for i in range (1, N):
        for j in range (1, N):
            if nouveau_terrain[0, i, j] == 0:
                col = "white"
            elif nouveau_terrain[0, i, j] == 1:
                col = "blue"
            elif nouveau_terrain[0, i, j] == 2:
                col = "red"
            else:
                col = "black"
            x = (i - 1) * LARGEUR_CASE
            y = (j - 1) * HAUTEUR_CASE
            carre = canvas.create_rectangle(x, y, x+LARGEUR_CASE, y+HAUTEUR_CASE, fill = col, outline = "grey50")
            grille[i][j] = carre

def start_fct():
    global terrain, nouveau_terrain
    tours = nbTours
    while tours != 0:
        boucle(terrain, nouveau_terrain, grille)
        terrain = nouveau_terrain
        nouveau_terrain = terrain.copy()
        time.sleep(1)
        tours -= 1

generation=tk.Button(root,text="générer terrain",command=init)
start = tk.Button(root, text="start", command=start_fct) #pour lancer la simulation. il faut mettre les fonctions en relation avec l'interface
arret=tk.Button(root, text="stop", command=root.destroy) #arret total
pause=tk.Button(root,text="pause") #mettre en pause
save=tk.Button(root,text="save", command = save_fct)
load=tk.Button(root,text="load", command = load_fct)


#grid

 

generation.grid()

start.grid()

save.grid()

load.grid()

arret.grid()

canvas.grid(row = 0, column = 1, rowspan = 6)

 

#Boucle

root.mainloop()

