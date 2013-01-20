# coding=utf-8
from utility import *
import Queue

pbNonFini = True
filename = 'uf20-010.cnf'
# File d'attente des problèmes à gérer composée de tableaux de taille 2 de la forme [état_des_variables, clauses_à_résoudre]
fileDesPb = Queue.Queue()

# On charge les données provenant du fichier CNF
donneesInitiales = loadCnfFile(filename)
nombreDeVariables = donneesInitiales[0]
nombreDeClauses = donneesInitiales[1]   
pbSat = donneesInitiales[2]
# On crée un tableau de taille le nombre de variable qui sont initialisées à 'U' pour 'Undecided'
varData = ['U']*nombreDeVariables
probleme = [varData, pbSat]
fileDesPb.put(probleme)
print "Load ok"
while pbNonFini:
    "print begin while"
    probleme = fileDesPb.get()
    valeursVariables,resultatPreTraitement=preTraitementSat(probleme)
    if resultatPreTraitement==True:
        print "Une solution a ete trouvee, il s'agit de:"
        print str(valeursVariables)
        pbNonFini = False
    elif resultatPreTraitement==False:
        print "Cette branche n'a pas de solution d'apres le processus "
    else:
        fileDesPb.put(genererSousSat(valeursVariables,resultatPreTraitement)[0])
        fileDesPb.put(genererSousSat(valeursVariables,resultatPreTraitement)[1])

    if fileDesPb.empty():
        print "Le probleme n'a pas de solution"
        pbNonFini = False