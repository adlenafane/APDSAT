# coding=utf-8
from mpi4py import MPI
from utility import loadCnfFile, calculVariablesPourBranching, calculClassementLitteraux
import Queue
from math import log

def comportementMaitre(comm, filename):
	rank = comm.rank
	size = comm.size
	pbNonFini = True
	tailleBatch = 2
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

	while pbNonFini:
		if fileDesPb.empty() == False and esclaveDisponible >=1:
			batchDesProblemes = []
			while (fileDesPb.empty() == False and len(batchDesProblemes) < tailleBatch):
				batchDesProblemes.append(fileDesPb.get())
			esclaveTrouve = False
			for indexEsclave in range(1, size):
				if listeEsclave[indexEsclave]==0 and esclaveTrouve==False:
					listeEsclave[indexEsclave] = 1
					esclaveDisponible = esclaveDisponible - 1
					comm.send(batchDesProblemes, dest=indexEsclave, tag=1)
					print "Batch"
					print batchDesProblemes
					esclaveTrouve = True
		"""
		print "slave loop"
		message = comm.Irecv(source = 1, tag=1)
		print message
		fileDesPb.put(message)
		"""

		pbNonFini = False
	return