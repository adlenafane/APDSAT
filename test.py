from utility import *
from simplifieSat import *
from random import choice


cnf=loadCnfFile("testCnf.cnf")[2]
print "la clause contenue dans testCnf.cnf est la suivante:"
print cnf
print "\n"

print "voici la fréquence d'apparition des variables dans cnf:"
print findCountOfLitterals(cnf)
print "\n"

varval=['T','F','U']
liste_de_var=[]
for k in range(0,loadCnfFile("testCnf.cnf")[0]):
    liste_de_var.append(choice(varval))

print "Avec le jeu de variable aléatoire suivant:"
print liste_de_var
print "La simplification du problème sat donné dans testCnf.cnf donne:"
print simplifieSat(cnf, liste_de_var)

