# coding=utf-8
from utility import *
from simplifieSat import *
from random import choice
from retireSingleton import *


cnf=loadCnfFile("testCnf.cnf")[2]
print "=== calculVariablesPourBranching ==="
resultat = []
print calculVariablesPourBranching(['U','U','U'], [2,1,3], resultat)
print resultat
print len(resultat)
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
print simplifieSat(liste_de_var,cnf)
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
print "input: simplifieSat(['U', 'T', 'F'],[[1, 2], [1], [2,3], [3]])"
print simplifieSat(['U', 'T', 'F'],[[1, 2], [1], [2,3], [3]])
print "input [[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]] + ['U','F','U', 'T']"
print simplifieSat(['U','F','U', 'T'],[[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]])

print "\n"
print "=== retireSingleton ==="
testvar = [[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1]]
print "input ['U','F','U', 'T'] + [[True],[False],[1],[2, 3], [1, 2, 3, 4], [2], [-1]]"
print retireSingleton(['U','F','U','T'],testvar)

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
print calculClassementLitteraux([[1],[2, 3], [1, 2, 3, 4], [2], [-1], [-2]])

print "\n"
print "=== Pretraitement ==="
print preTraitementSat([['T','U','U','U'],[[1],[2, 3], [1, 2, 3, 4], [2], [-1,-4], [-2,-4]]])
print "Resultat attendu: (['T', 'T', 'U', 'U'], [[-1, -4], [-2, -4]])"

print "\n"
print "=== Generation de sous-problemes SAT ==="
print "input: ['T','T','U','U'],[[-1,-4], [-2,-4]]"
print genererSousSat(['T','T','U','U'],[[-1,-4], [-2,-4]])
print "Resultat attendu: [['T','T','U','T'],[[-1,-4], [-2,-4]],['T','T','U','F'],[[-1,-4], [-2,-4]]]"


print "\n"
print "=== Generation de sous-problemes SAT ==="
print "input: ['T','U','U','U'],[[1],[-1,2, 3], [1, 2, -3, 4], [-1,2], [-1,-3], [1,-2,3]]"
print genererSousSat(['T','U','U','U'],[[1],[2, 3], [1, 2, -3, 4], [2], [-1,-3], [-2,3]])
print "Resultat attendu: [[['T','U','T','U'],[[1],[2, 3], [1, 2, -3, 4], [2], [-1,-3], [-2,3]]],[['T','U','F','U'],[[1],[2, 3], [1, 2, -3, 4], [2], [-1,-3], [-2,3]]]]"

