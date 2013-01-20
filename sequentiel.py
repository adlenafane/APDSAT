# coding=utf-8
from utility import *
import Queue
import time
import argparse
import socket

parser = argparse.ArgumentParser(description='ArgumentParser')
parser.add_argument('--file', default='uf20-010.cnf')
args = parser.parse_args()

start = time.time()
pbNonFini = True
filename = args.file
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
while pbNonFini:
    probleme = fileDesPb.get()
    valeursVariables,resultatPreTraitement=preTraitementSat(probleme)
    if resultatPreTraitement==True:
        print "Une solution a ete trouvee, il s'agit de:"
        print str(valeursVariables)
        pbNonFini = False
        result = True
    elif resultatPreTraitement==False:
        pass
        #print "Cette branche n'a pas de solution"
    else:
        fileDesPb.put(genererSousSat(valeursVariables,resultatPreTraitement)[0])
        fileDesPb.put(genererSousSat(valeursVariables,resultatPreTraitement)[1])
    if fileDesPb.empty():
        print "Le probleme n'a pas de solution"
        pbNonFini = False
        result = False
elapsed = (time.time() - start)
print "Temps ecoule: " + "%.5f" %elapsed + " secondes"

# Ecris les resultats dans un fichier
with open('resultatParallele.txt', 'a') as resultFile:
    resultFile.write(str(filename) + "," + "1"  + "," + "1" + "," + str(nombreDeVariables) + "," + str(nombreDeClauses) + "," + str(result) + "," + str(elapsed) + "," + str(socket.gethostname()))
    resultFile.write("\n")