# coding=utf-8
from mpi4py import MPI
from utility import *
import Queue
from math import log
import time

def comportementMaitre(comm, filename, tailleBatch):
	start = time.time()
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

	# On crée un tableau de taille le nombre de variable qui sont initialisées à 'U' pour 'Undecided' et on initialise notre file
	varData = ['U']*nombreDeVariables
	probleme = [varData, pbSat]
	fileDesPb.put(probleme)

	while pbNonFini:

		#Envoi de travaux aux esclaves
		while fileDesPb.empty() == False and esclaveDisponible >=1:
			batchDesProblemes = []
			# on sort de ce while des que l'on arrive au bout de la fileDesPb OU que notre batchDesProbleme atteint la tailleDeBatch definie.
			while (fileDesPb.empty() == False and len(batchDesProblemes) < tailleBatch):  
				batchDesProblemes.append(fileDesPb.get())
			# On cherche un esclave disponible et on lui envoie le batch de probleme a traiter
			esclaveTrouve = False
			for indexEsclave in range(1, size):
				if listeEsclave[indexEsclave]==0 and esclaveTrouve==False:
					listeEsclave[indexEsclave] = 1
					esclaveDisponible = esclaveDisponible - 1
					comm.send(batchDesProblemes, dest=indexEsclave, tag=1)
					esclaveTrouve = True
		# On récupère les réponses des esclaves
		for indexEsclave in range(1,size):
			if listeEsclave[indexEsclave] == 1:
				status = MPI.Status()
				message = comm.recv(source=indexEsclave, tag = MPI.ANY_TAG, status= status)
				#Tag 2 pour un message de l'esclave vers le maitre indiquant que le pbSAT a ete resolu
				if status.Get_tag()==2:
					print "Une solution a ete trouvee, il s'agit de:"
					print str(message)
					elapsed = (time.time() - start)
					print "La solution a ete trouvee en:" + "%.5f" %elapsed
					resultat = True
					indexDernierEsclave = indexEsclave
					pbNonFini = False
				#Tag 3 pour un message de l'esclave vers le maitre indiquant que le pbSAT ne peut pas etre resolu (une clause est fausse)
				elif status.Get_tag()==3:
					pass
				#Tag 4 signifie l'esclave envoie un pb au maitre
				elif status.Get_tag()==4:
					listeEsclave[indexEsclave] = 0
					esclaveDisponible+=1
					for pb in message:
						fileDesPb.put(pb)
					pbNonFini = True
		# Si on n'a plus de probleme et que tout le monde a répondu c'est qu'on a vérifié toutes les possibilités
		if fileDesPb.empty() and esclaveDisponible == size-1:
			elapsed = (time.time() - start)
			print "Le probleme n'a pas de solution. Temps écoulé:" + "%.5f" %elapsed
			resultat = False
			pbNonFini = False
	for indexEsclave in range(1, size):
		if listeEsclave[indexEsclave] == 1:
			message = comm.recv(source=indexEsclave, tag = MPI.ANY_TAG, status= status)
		comm.send("", dest=indexEsclave, tag=5)
	return [size, tailleBatch, nombreDeVariables, nombreDeClauses, resultat, elapsed]