# coding=utf-8
from mpi4py import MPI
from utility import loadCnfFile, calculVariablesPourBranching, calculClassementLitteraux
import Queue
from math import log

#Example assez complet en C++ sur un master qui distribue des jobs à ses esclaves: http://www.lam-mpi.org/tutorials/one-step/ezstart.php

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

		#Envoit de travaux aux esclaves
		if fileDesPb.empty() == False and esclaveDisponible >=1:
			batchDesProblemes = []
			while (fileDesPb.empty() == False and len(batchDesProblemes) < tailleBatch):  #on sort de ce while des que l'on arrive au bout de la fileDesPb OU que notre batchDesProbleme atteint la tailleDeBatch definie.
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
		# reception des travaux des esclaves:
		print "slave loop"
		#comment on fait si dans le "buffer à messages recus" il y a plusieurs réponses (de plusieurs esclaves)? Il faudrait parcourir le buffer avec une boucle for...  https://groups.google.com/forum/#!msg/mpi4py/LDHbzApI55c/gENCO-_HAwUJ  et   https://groups.google.com/forum/?fromgroups=#!topic/mpi4py/Y0HrQkaPeNs
		message = comm.Irecv(source = 1, tag=1)  
		print message
		fileDesPb.put(message)
		"""

		"""
		# Autre solution: faire ca sequentiellement. Mais du coup il faudrait aussi faire l'envoi de maniere sequentiel (ca n'optimise pas l'utilisation des processeurs, mais bon, l'avantage c'est que ca simplifie pas mal: plus besoin de la variable esclaveDisponible par exemple, et puis comme les taches sont de tailles similaire, et qu'on va les faire tourner sur le meme processeur, les temps de traitement seront très très très proches, donc a mon avis on n'y perd pas bcp...).
		#pour le Get_tag, j'ai pas pu tester, mais ca doit etre quelque chose commce ca, cf https://groups.google.com/forum/?fromgroups=#!topic/mpi4py/fHzY1gAEYpM
		for esclave in range(1,size): 
			reception = []
			#message = comm.Irecv(self, reception, source=esclave, tag=MPI.ANY_TAG)
			message = comm.irecv()
			MPI.
			message.Test(status)
			#Tag 2 pour un message de l'esclave vers le maitre indiquant que le pbSAT a ete resolu
			if status.Get_tag()==2:
				print "Une solution a ete trouvee, il s'agit de:"
				print str(message)
				pbNonFini = False

			#Tag 3 pour un message de l'esclave vers le maitre indiquant que le pbSAT ne peut pas etre resolu (une clause est fausse)
			elif status.get_tag()==3:
				print "Cette branche n'a pas de solution"
				# On ne peut pas arrêter la résolution du pb, celui peut avoir une solution sur une autre branche, c'est juste la branche qu'on kill
				#pbNonFini = False

			#Tag 4 signifie l'esclave envoie un pb au maitre
			elif status.get_tag()==4:
				print "la resolution continue avec " + str(message)
				esclaveDisponible+=1
				for pb in message:
					fileDesPb.put(pb)
		"""
		pbNonFini = False
	message = ""
	for indexEsclave in range(1, size):
		comm.send(message, dest=indexEsclave, tag=2)
	return