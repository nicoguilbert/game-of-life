from tkinter import *

import random
import time
import copy
import numpy as np

N = 15
M = 15
#taille par defaut
#taille = 25

def initDamier(damier, lig, col, proba):

	for i in range(lig):
		# On créé une liste vide
		l = []
		for j in range(col):
			# Pour chaque element du damier
			# append(rangeint(0,1) ajoute
			# à la fin de la liste un nombre
			# random entre 0 et 1
			l.append(np.random.choice(2, p = [1 - proba, proba]))
		damier.append(l)

# OK
def afficherDamier(damier,lig,col):
	print("===========================================\n")
	for i in range(lig):
		print(damier[i])

def nbVoisin(damier, i, j,taille):
	nb = 0
	nb += damier[(i)%taille][(j+1)%taille]
	nb += damier[(i)%taille][(j+taille-1)%taille]

	nb += damier[(i+1)%taille][j]
	nb += damier[(i+1)%taille][(j+1)%taille]
	nb += damier[(i+1)%taille][(j+taille-1)%taille]

	nb += damier[(i+taille-1)%taille][j]
	nb += damier[(i+taille-1)%taille][(j+1)%taille]
	nb += damier[(i+taille-1)%taille][(j+taille-1)%taille]
	return nb

def nextGen(damier, taille):
	newDamier  = []
	for i in range(taille):
		newDamier.insert(i, damier[i].copy())

	for i in range(taille):
		for j in range(taille):
			voisins = 0
			voisins = nbVoisin(damier,i,j,taille)
			if damier[i][j] == 1:
				if voisins < 2 or voisins > 3:
					newDamier[i][j] = 0
				else:
					newDamier[i][j] = 1
			else:
				if voisins == 3:
					newDamier[i][j] = 1

	for i in range(taille):
		damier[i] = newDamier[i].copy()

def initialiser():
	global damier, t
	t = sTaille.get()
	proba = esperance.get()
	proba = proba / 100
	damier = []
	initGrille(t)
	initDamier(damier, t, t, proba)
	afficherGrille(damier, t)

def start():
	global arret
	arret = False
	lancer()

def lancer():
	global arret, t
	v = vitesse.get()

	if(arret == False):
		#time.sleep(10/v)
		afficherGrille(damier, t)
		nextGen(damier, t)
		fen.after(int(1000 / v),lancer)

def arreter():
	global arret
	arret = True

global arret
arret = True

###### Fenetre #####

fen=Tk()
fen.title("SR01 Jeu de la vie")
fen.geometry("800x600")

###### Grille - canvas ######

grille = Canvas(fen, width = 600, height = 600, bg = "ivory", relief = SOLID)
grille.pack(padx = 20, pady = 10, side = LEFT, fill = X)

def initGrille(taille):
	#grille.delete('all')
	global cellule
	dimCase = (600/taille)
	cellule = [[0] * taille for i in range(taille)]

	for i in range (taille):
		for j in range (taille):
			x = i*dimCase
			dx = (i+1)*dimCase
			y = j*dimCase
			dy = (j+1)*dimCase
			cellule[i][j] = grille.create_rectangle(x, y, dx, dy, width = 1, fill = "white", outline = "white")

def afficherGrille(damier, taille):
	for i in range(taille):
		for j in range(taille):
			#print(i, j, str(damier[i][j]))
			if (damier[i][j] == 1):
				couleur = "green"
			else:
				couleur = "white"
			grille.itemconfig(cellule[i][j], fill = couleur, outline = "black")

###### Menu haut ##########

menu_h = Frame(fen, width = 100, height = 300)
menu_h.pack(side = TOP, fill = X)
bou_lancer = Button(menu_h, text = "Lancer", command = start).pack(fill = X)
bou_arret = Button(menu_h, text = "Arreter", command = arreter).pack(fill = X)
bou_init = Button(menu_h, text = "Initialiser", command = initialiser).pack(fill = X)

###### Menu bas ###########

menu_b = Frame(fen, width = 100, height = 300)
menu_b.pack(side = BOTTOM, fill = X)
sTaille = Scale(menu_b, orient = 'horizontal', from_ = 5, to = 100, resolution = 5, tickinterval = 1, length = 100, label = 'Taille de la Grille')
sTaille.pack(fill = X)
#global esperance
esperance = Scale(menu_b, orient = 'horizontal', from_ = 0, to = 100, resolution = 1, length = 100, label = 'Esperance de vie (%)')
esperance.pack(fill = X)
#global vitesse
vitesse = Scale(menu_b, orient = 'horizontal', from_ = 1, to = 30, resolution = 1, length = 100, label = 'Vitesse')
vitesse.pack(fill = X)
bou_quit = Button( menu_b, text = "Quitter", command = fen.destroy)
bou_quit.pack(side = BOTTOM, fill = X)

fen.mainloop()
