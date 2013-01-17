from mpi4py import MPI

def comportementEsclave(comm):
	print "Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size)
	return