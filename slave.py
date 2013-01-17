from mpi4py import MPI
from simplifieSat import *

def comportementEsclave(comm):
	print "Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size)
	return

data=comm.recv(source=0,tag=1)

#Recuperation de la liste des variables avec valeurs T pour True, F pour False et U pour Undefined
valeursVariables=data[0]
#Recuperation du Probleme SAT a traiter
problemeSAT=data[1]

pb=simplifieSat(valeursVariables, problemeSAT)
result=testSatOk(pb)

if result==True:
    #On envoie un message de type tag 2 au maître pour lui indiquer que le pb SAT a ete resolu
    #On envoie au maitre la valeur des variables resolvant le probleme SAT
    comm.send(valeursVariables,dest=0,tag=2)
elif result==False:
    #On envoie un message de type tag 3 au maître pour lui indiquer que le pb ne peut pas etre resolu

    #comm.send(dest=0,tag=3)
    pass:
else:
    pass:
    

