# coding=utf-8
from utility import *
from simplifieSat import *
from random import choice
from retireSingleton import *


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
print "\n"

print "=== testSatOk ==="
print "input: [[True], [1]]"
print str(testSatOk([[True], [1]])) + " should be [[1]]"
print "input: []"
print str(testSatOk([])) + " should be True"
print "input: [[False], [1]]"
print str(testSatOk([[False], [1]])) + " should be False"

print "\n"
print "=== simplifieSat ==="
print "input: simplifieSat([[1, 2], [1], [2,3], [3]], ['U', 'T', 'F'])"
print simplifieSat([[1, 2], [1], [2,3], [3]], ['U', 'T', 'F'])
print "input [[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]] + ['U','F','U', 'T']"
print simplifieSat([[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]], ['U','F','U', 'T'])

print "\n"
print "=== retireSingleton ==="
testvar = [[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1]]
print "input [[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1]] + ['U','F','U', 'T']"
print retireSingleton(testvar, ['U','F','U', 'T'])

print "\n"
print "=== Répartion et ration des nombres ==="
print genererRepartitionDesPositifsEtNegatifs([[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]])
print calculDuRatioDePositifsEtNegatifs(genererRepartitionDesPositifsEtNegatifs([[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]]))
a= calculClassementFrequence(findCountOfLitterals([[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]]))
print a
print "Should be [4, 3, 1, 2]"
b=calculClassementPositifsEtNegatifs(calculDuRatioDePositifsEtNegatifs(genererRepartitionDesPositifsEtNegatifs([[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]])))
print b
print "Should be [3, 4, 2, 1]"
print "Classement:"
print calculClassementLitteraux(a,b)