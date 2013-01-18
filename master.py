# coding=utf-8
from mpi4py import MPI
from utility import loadCnfFile, calculVariablesPourBranching, calculClassementLitteraux
import Queue
from math import log

def comportementMaitre(comm, filename):
	rank = comm.rank
	size = comm.size
	pbNonFini = True
	print "Hello! I'm rank %d from %d running in total..." % (rank, size)

	# On crée un tableau de taille le nombre de processeurs disponibles, 0 signifie esclave libre, 1 signifie esclave occupé et -1 pour le maitre
	listeEsclave = [0]*size
	listeEsclave[0] = -1
	esclaveDisponible = size - 1
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

	while(pbNonFini):
		probleme = fileDesPb.get()
		varData = probleme[0]
		pbSat = probleme[1]
		print varData
		print pbSat

		variablesOrdonnees = calculClassementLitteraux(pbSat)
		print variablesOrdonnees
		
		if esclaveDisponible >=1:
			# On choisit la taille de notre branching comme étant le minimum entre les ressources disponibles et le nombre de variables sur lequel faire des branches
			tailleBranching = min(int(log(esclaveDisponible)/log(2.0)), len(variablesOrdonnees))

			# Testing purpose, en réalité le nouveau set de données doit être calculé mais encore des pb avec la fonction 
			nouveauSetDeDonnees = [['U','U','T'], ['U','U','F']]
			calculVariablesPourBranching(varData, variablesOrdonnees[:tailleBranching], nouveauSetDeDonnees)
			# Envoi de tout ces nouveaux problèmes aux esclaves disponibles
			for donnees in nouveauSetDeDonnees:
				for indexEsclave in range(1, len(listeEsclave)):
					if listeEsclave[indexEsclave]==0:
						listeEsclave[indexEsclave] = 1
						esclaveDisponible = esclaveDisponible - 1
						problemeAEnvoyer = [donnees, pbSat]
						print problemeAEnvoyer
						comm.send(problemeAEnvoyer, dest=indexEsclave, tag=1)
						break
		

		pbNonFini = False
	return