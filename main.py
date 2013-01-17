from mpi4py import MPI
from master import *
from slave import *

comm = MPI.COMM_WORLD

if comm.rank == 0:
	# Master
	comportementMaitre(comm)
else:
	# Slave
	comportementEsclave(comm)