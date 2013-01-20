from mpi4py import MPI
from master import *
from slave import *
import argparse
import socket

parser = argparse.ArgumentParser(description='ArgumentParser')
parser.add_argument('--file', default='uf20-010.cnf')
parser.add_argument('--batch', default=4)
args = parser.parse_args()

def main(args):
	comm = MPI.COMM_WORLD

	if comm.rank == 0:
		# Master
		filename = args.file
		tailleBatch = int(args.batch)
		result = comportementMaitre(comm, filename, tailleBatch)
		# Ecris les resultats dans un fichier
		with open('resultatParallele.txt', 'a') as resultFile:
			resultFile.write(str(filename) + "," + str(result[0])  + "," + str(result[1]) + "," + str(result[2]) + "," + str(result[3]) + "," + str(result[4]) + "," + str(result[5]) + "," + str(socket.gethostname()))
			resultFile.write("\n")
		return result
	else:
		# Slave
		comportementEsclave(comm)

main(args)