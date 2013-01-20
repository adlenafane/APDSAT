from mpi4py import MPI
from master import *
from slave import *

def main():
	comm = MPI.COMM_WORLD

	if comm.rank == 0:
		# Master
		filename = 'uf20-010.cnf'
		result = comportementMaitre(comm, filename)
		# Ecris les resultats dans un fichier
		with open('resultatParallele.txt', 'a') as resultFile:
			resultFile.write(str(filename) + "," + str(result[0])  + "," + str(result[1]) + "," + str(result[2]) + "," + str(result[3]) + "," + str(result[4]) + "," + str(result[5]))
			resultFile.write("\n")
		return result
	else:
		# Slave
		comportementEsclave(comm)

main()