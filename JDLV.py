import numpy as np
import random
import time

def test_final(test_fin, pop_totale): # pseudo-stabilisation ou non ?
    fin = True
    for i in range(len(pop_totale)): # on teste si il s'agit de la même valeur qu'il y a 2 générations
        if test_fin[0][i] != pop_totale[i] or test_fin[1][i] != pop_totale[i]:
            fin = False
    return fin

def depassement_tableau(grille, num_pop, nb_voisins, l, c): # determine si la cellule est vivante pares avoir corrige la position
    l = (l % grille.shape[0] + grille.shape[0]) % grille.shape[0]
    c = (c % grille.shape[1] + grille.shape[1]) % grille.shape[1]
    if grille[l, c] == num_pop * 10 + 1 or grille[l, c] == num_pop * 10 + 3:
        nb_voisins += 1
    return nb_voisins

def voisinage(grille, num_pop, i, j, rang): # calcule le nombre de voisins
    nb_voisins = 0
    for l in range(i - rang, i + rang + 1):
        for c in range(j - rang, j + rang + 1):
            nb_voisins = depassement_tableau(grille, num_pop, nb_voisins, l, c)
    return nb_voisins

def fin_gen_transition(grille, num_pop):
    for i in range(grille.shape[0]):
        for j in range(grille.shape[1]):
            if grille[i, j] == num_pop * 10 + 2:
                grille[i, j] = num_pop * 10 + 1
            elif grille[i, j] == num_pop * 10 + 3:
                grille[i, j] = 0

def regle4b(grille, pop_totale, num_pop, i, j):
    exception = False
    for n_pop in range(len(pop_totale)):
        nb_voisins = voisinage(grille, n_pop, i, j, 1)
        if n_pop != num_pop and nb_voisins == 3:
            nb_voisins1 = voisinage(grille, n_pop, i, j, 2)
            nb_voisins2 = voisinage(grille, num_pop, i, j, 2)
            if nb_voisins1 == nb_voisins2:
                if pop_totale[n_pop] > pop_totale[num_pop]:
                    grille[i, j] = n_pop * 10 + 2
                elif pop_totale[n_pop] < pop_totale[num_pop]:
                    grille[i, j] = num_pop * 10 + 2
                else:
                    exception = True
            elif nb_voisins1 > nb_voisins2:
                grille[i, j] = n_pop * 10 + 2
            else:
                grille[i, j] = num_pop * 10 + 2
    if grille[i, j] == 0 and not exception:
        grille[i, j] = num_pop * 10 + 2

def generation_sup(grille, pop_totale, test_fin):
    populations = np.zeros_like(pop_totale)
    for num_pop in range(len(pop_totale)):
        fin_gen_transition(grille, num_pop)
        for i in range(grille.shape[0]):
            for j in range(grille.shape[1]):
                if grille[i, j] == num_pop * 10 + 1:
                    nb_voisins = voisinage(grille, num_pop, i, j, 1)
                    nb_voisins -= 1
                    if nb_voisins < 2 or nb_voisins > 3:
                        grille[i, j] = num_pop * 10 + 3
                if grille[i, j] == 0:
                    nb_voisins = voisinage(grille, num_pop, i, j, 1)
                    if nb_voisins == 3:
                        regle4b(grille, pop_totale, num_pop, i, j)
                if grille[i, j] == num_pop * 10 + 1 or grille[i, j] == num_pop * 10 + 2:
                    populations[num_pop] += 1
    for i in range(len(populations)):
        test_fin[0][i] = test_fin[1][i]
        test_fin[1][i] = pop_totale[i]
        pop_totale[i] = populations[i]

def initialisation(grille, pop_totale, test_fin, taux_dep):
    grille.fill(0)
    nb_cell_dep = round(grille.size * taux_dep)
    nb_cell_dep //= len(pop_totale)
    pop = 0
    for i in range(0, len(pop_totale) * 10, 10):
        rand_colonne = 0
        rand_ligne = 0
        for j in range(nb_cell_dep):
            while True:
                rand_ligne = random.randint(0, grille.shape[0] - 1)
                rand_colonne = random.randint(0, grille.shape[1] - 1)
                if grille[rand_ligne, rand_colonne] == 0:
                    break
            grille[rand_ligne, rand_colonne] = i + 1
        pop_totale[pop] = nb_cell_dep
        test_fin[1][pop] = nb_cell_dep
        pop += 1

def afficher_grille(grille, visu, pop_totale, generation):
    for i in range(grille.shape[0]):
        for j in range(grille.shape[1]):
            if grille[i, j] == 0 or grille[i, j] % 10 == 3:
                if grille[i, j] % 10 == 3 and visu:
                    print("*", end=" ")
                else:
                    print(".", end=" ")
            elif grille[i, j] % 10 == 1 or grille[i, j] % 10 == 2:
                if grille[i, j] % 10 == 2 and visu:
                    print("-", end=" ")
                else:
                    print("#", end=" ")
        print()
    if visu:
        print(" T" + str(generation) + "+")
        print()
        afficher_grille(grille, False, pop_totale, generation)
    else:
        generation += 1
        print(" T" + str(generation), end="")
        for i in range(1, len(pop_totale) + 1):
            print(" / Pop " + str(i) + ": " + str(pop_totale[i - 1]), end="")
        print()
        print()

def main():
    print("Combien de lignes?")
    n_ligne = int(input())
    print("Combien de colonnes?")
    n_colonne = int(input())
    print("Combien de populations?")
    nb_pop = int(input())
    print("Quel taux de remplissage de cellules au départ? (entre 0.1 et 0.9)")
    taux_dep = float(input())
    print("Jeu avec ou sans visualisation des états futurs? (True-avec False-sans)")
    visu = bool(input())

    grille = np.zeros((n_ligne, n_colonne), dtype=int)
    generation = 0
    pop_totale = np.zeros(nb_pop, dtype=int)
    test_fin = np.zeros((2, nb_pop), dtype=int)
    initialisation(grille, pop_totale, test_fin, taux_dep)
    afficher_grille(grille, False, pop_totale, generation)
    while not test_final(test_fin, pop_totale):
        time.sleep(1)
        generation_sup(grille, pop_totale, test_fin)
        afficher_grille(grille, visu, pop_totale, generation)
        generation += 1

if __name__ == "__main__":
    main()