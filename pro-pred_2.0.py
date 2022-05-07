import random as rd
import tkinter as tk
import numpy as np

#Parametres

longueur = 5
largeur = 5
Npro = 5
Npred = 2
Erepro = 10
AgeMinProies = 3
AgeMaxProies = 5
AgeMinPredateurs = 7
AgeMaxPredateurs = 12

#Creation terrain
def initialisation():
    """On crée le tableau (avec un tableau numpy, plus élégant d'utilisation que les listes imbriquées et plus optimal pour la mémoire que les listes car non-extensible
    On aurait tout aussi bien pu avoir, au lieu de "terrain[1, ligne, colonne]" une syntaxe plus classique "terrain[ligne][colonne][1]"."""
    terrain = np.zeros((3, longueur+2, largeur+2))
    #etage 0 : nature de la case (0:libre, 1:proie, 2:predateur, 3:inaccessible)
    #etage 1 : âge (et 3 si case inaccessible pour repère)
    #etage 2 : énergie prédateurs
    nouveau_terrain = terrain.copy() #On travaille sur les deux terrains en parallèle pour effectuer les modifications
    for ligne in range(longueur+2):
        for colonne in range(largeur+2):
            if ligne == 0 or ligne == longueur+1 or colonne == 0 or colonne == largeur+1: #On crée des cases inaccessibles sur les bords
                nouveau_terrain[0,ligne,colonne] = 3
                nouveau_terrain[1,ligne,colonne] = 3
    terrain = nouveau_terrain
    nouveau_terrain = terrain.copy()
    naissances(terrain, nouveau_terrain, Npro, Npred)
    return nouveau_terrain #les return sont non nécessaires au vu de la structure en tableaux, mais le code est plus lisible ainsi donc nous faisons le choix de les garder

def naissances(terrain, nouveau_terrain, Nproies, Npred):
    """Permet la génération des proies et prédateurs à des positions aléatoires"""
    cases_libres = []
    for ligne in range(longueur+2):
        for colonne in range(largeur+2):
            nature_case = terrain[0,ligne,colonne]
            if nature_case == 0:
                cases_libres.append(ligne*(largeur+2)+colonne) #indexation des cases par un indice plus compliqué mais adapté à un tableau unidimensionnel
    rd.shuffle(cases_libres) #On mélange pour obtenir un indice aléatoire
    nouvelles_proies = [] #Les prochaines lignes permettent d'obtenir un tirage sans remise dans les cases libres
    while Nproies != 0:
        nouvelles_proies.append(cases_libres.pop())
        Nproies -= 1
    #nouvelles_proies = rd.sample(cases_libres, Nproies)
    for i in nouvelles_proies:
        ligne_nouvelle_proie = i//(largeur+2)
        colonne_nouvelle_proie = i%(largeur+2)
        nouveau_terrain[0, ligne_nouvelle_proie, colonne_nouvelle_proie] = 1
        nouveau_terrain[1, ligne_nouvelle_proie, colonne_nouvelle_proie] = rd.randint(AgeMinProies, AgeMaxProies)
    nouveaux_predateurs = rd.sample(cases_libres, Npred) #Tirage sans remise mais ne modifie pas cases_libres car on ne s'en resservira pas
    for i in nouveaux_predateurs:
        ligne_nouveau_predateur = i//(largeur+2)
        colonne_nouveau_predateur = i%(largeur+2)
        nouveau_terrain[0, ligne_nouveau_predateur, colonne_nouveau_predateur] = 2
        nouveau_terrain[1, ligne_nouveau_predateur, colonne_nouveau_predateur] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        nouveau_terrain[2, ligne_nouveau_predateur, colonne_nouveau_predateur] = rd.randint(3, nouveau_terrain[1, ligne_nouveau_predateur, colonne_nouveau_predateur]-1) #On est bornés par la formule Epre<Apre
    return nouveau_terrain 



def deplacement(ligne, colonne, direction):
    """Cette fonction assure le vieillissement et le déplacement des animaux.
    Le déplacement est à l'origine aléatoire, mais on peut le forcer dans une direction (numérotée de 0 à 8) pour répondre au mécanisme chasse ou fuite"""
    #vieillissement
    
    nouveau_terrain[1, ligne, colonne] -= 1
    nouveau_terrain[2, ligne, colonne] -= 1
    if nouveau_terrain[1, ligne, colonne] == 0 or nouveau_terrain[2, ligne, colonne]:
        nouveau_terrain[0, ligne, colonne] == 0
    
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
    if cases_adjacentes_dispo != []:#on s'assure qu'un déplacement est effectivement possible
        nouvelle_case = cases_adjacentes_dispo[rd.randint(0, len(cases_adjacentes_dispo)-1)]#on chosit un déplacement au hasard parmi ceux possibles
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


def etape():
    """Element répété tout au long du programme combinant vieillissement, déplacement et reproduction"""
    global terrain, nouveau_terrain
    terrain = nouveau_terrain
    nouveau_terrain = terrain.copy()
    #naissances(Fpro, Fpred)
    #terrain = nouveau_terrain
    #nouveau_terrain = terrain.copy()
    for ligne in range(longueur+2):
        for colonne in range(largeur+2):
            nature_case = terrain[0, ligne, colonne]
            if nature_case == 1 or nature_case == 2:
                if nature_case == 1:
                    reproduction(1, ligne, colonne)
                else:
                    reproduction(2, ligne, colonne)
                deplacement(ligne, colonne)
    return nouveau_terrain

def reproduction(nature, ligne, colonne):
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
        if position_enfant == "C":
            nouveau_terrain[0, ligne-2, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-2, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-2, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "D":
            nouveau_terrain[0, ligne-2, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-2, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-2, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "F":
            nouveau_terrain[0, ligne-1, colonne-2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne-2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne-2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "G":
            nouveau_terrain[0, ligne-1, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "H":
            nouveau_terrain[0, ligne-1, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "I":
            nouveau_terrain[0, ligne-1, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "J":
            nouveau_terrain[0, ligne-1, colonne+2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne-1, colonne+2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne-1, colonne+2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "K":
            nouveau_terrain[0, ligne, colonne-2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne-2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne-2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "L":
            nouveau_terrain[0, ligne, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "N":
            nouveau_terrain[0, ligne, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "O":
            nouveau_terrain[0, ligne, colonne+2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne, colonne+2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne, colonne+2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "P":
            nouveau_terrain[0, ligne+1, colonne-2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne-2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne-2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "Q":
            nouveau_terrain[0, ligne-2, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "R":
            nouveau_terrain[0, ligne+1, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "S":
            nouveau_terrain[0, ligne+1, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "T":
            nouveau_terrain[0, ligne+1, colonne+2] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+1, colonne+2] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+1, colonne+2] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "V":
            nouveau_terrain[0, ligne+2, colonne-1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+2, colonne-1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+2, colonne-1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "W":
            nouveau_terrain[0, ligne+2, colonne] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+2, colonne] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+2, colonne] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)
        if position_enfant == "X":
            nouveau_terrain[0, ligne+2, colonne+1] = nature
            if nature == 1:
                nouveau_terrain[1, ligne+2, colonne+1] = rd.randint(AgeMinProies, AgeMaxProies)
            else:
                nouveau_terrain[1, ligne+2, colonne+1] = rd.randint(AgeMinPredateurs, AgeMaxPredateurs)


#INTERFACE GRAPHIQUE
"""
WIDTH = 1400
HEIGHT = 900
max = 30
grille = []

for i in range(max):
    grille.append([0]*max)

root = tk.Tk()
canvas = tk.Canvas(root, bg = "white", height=HEIGHT, width=WIDTH)
terrain = canvas.create_rectangle(0,0, WIDTH-500, HEIGHT, fill = "white")

for i in range (0, max+1):
    for j in range (0, max+1):
        case = canvas.create_rectangle(900-max*(max-i), 900-max*(max-j), 900-max*(max-(i+1)), 900-max*(max-(j+1)), fill = "white")
        grille[i][j]=case


demarrer = tk.Button(root, text="démarrer", command=initialisation())

demarrer.grid()
canvas.grid()
root.mainloop()
"""
