from mpi4py import MPI
from master_random import *
from slave import *
import argparse
import socket

parser = argparse.ArgumentParser(description='ArgumentParser')
parser.add_argument('--file', default='uf20-01.cnf')
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
		try:
			with open('resultatParallele.txt', 'a') as resultFile:
				resultFile.write(str(filename) + "," + str(result[0])  + "," + str(result[1]) + "," + str(result[2]) + "," + str(result[3]) + "," + str(result[4]) + "," + str(result[5]) + "," + str(socket.gethostname()) + "," + "random")
				resultFile.write("\n")
		except IOError as e:
			print 'Operation failed: %s' % e.strerror
		return result
	else:
		# Slave
		comportementEsclave(comm)

main(args)