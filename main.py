from mpi4py import MPI
from master import *
from slave import *

comm = MPI.COMM_WORLD

if comm.rank == 0:
	# Master
	filename = 'uf20-09.cnf'
	comportementMaitre(comm, filename)
else:
	# Slave
	comportementEsclave(comm)