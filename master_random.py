# coding=utf-8
from mpi4py import MPI
from utility import *
from math import log
import time
import random

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
	fileDesPb = []

	# On charge les données provenant du fichier CNF
	donneesInitiales = loadCnfFile(filename)
	nombreDeVariables = donneesInitiales[0]
	nombreDeClauses = donneesInitiales[1]	
	pbSat = donneesInitiales[2]
	# On crée un tableau de taille le nombre de variable qui sont initialisées à 'U' pour 'Undecided'
	varData = ['U']*nombreDeVariables
	# DEBUG
	#varData = ['F', 'T', 'T', 'F', 'F', 'T', 'F', 'T', 'F', 'T', 'T', 'T', 'T', 'F', 'T', 'T', 'T', 'F', 'F', 'F']
	probleme = [varData, pbSat]
	fileDesPb.append(probleme)

	while pbNonFini:
		#Envoit de travaux aux esclaves
		if fileDesPb != [] and esclaveDisponible >=1:
			batchDesProblemes = []
			while (fileDesPb != [] and len(batchDesProblemes) < tailleBatch):
				index = random.randint(0, len(fileDesPb)-1)
				batchDesProblemes.append(fileDesPb[index])
				del fileDesPb[index]
			esclaveTrouve = False
			for indexEsclave in range(1, size):
				if listeEsclave[indexEsclave]==0 and esclaveTrouve==False:
					listeEsclave[indexEsclave] = 1
					esclaveDisponible = esclaveDisponible - 1
					comm.send(batchDesProblemes, dest=indexEsclave, tag=1)
					esclaveTrouve = True
		# Autre solution: faire ca sequentiellement. Mais du coup il faudrait aussi faire l'envoi de maniere sequentiel (ca n'optimise pas l'utilisation des processeurs, mais bon, l'avantage c'est que ca simplifie pas mal: plus besoin de la variable esclaveDisponible par exemple, et puis comme les taches sont de tailles similaire, et qu'on va les faire tourner sur le meme processeur, les temps de traitement seront très très très proches, donc a mon avis on n'y perd pas bcp...).
		#pour le Get_tag, j'ai pas pu tester, mais ca doit etre quelque chose commce ca, cf https://groups.google.com/forum/?fromgroups=#!topic/mpi4py/fHzY1gAEYpM
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
					# On ne peut pas arrêter la résolution du pb, celui peut avoir une solution sur une autre branche, c'est juste la branche qu'on kill
					pass
				#Tag 4 signifie l'esclave envoie un pb au maitre
				elif status.Get_tag()==4:
					listeEsclave[indexEsclave] = 0
					esclaveDisponible+=1
					for pb in message:
						fileDesPb.append(pb)
					pbNonFini = True
		if fileDesPb == [] and esclaveDisponible == size-1:
			elapsed = (time.time() - start)
			print "Le probleme n'a pas de solution. Temps écoulé:" + "%.5f" %elapsed
			resultat = False
			pbNonFini = False
	for indexEsclave in range(1, size):
		comm.send("", dest=indexEsclave, tag=5)
	return [size, tailleBatch, nombreDeVariables, nombreDeClauses, resultat, elapsed]