# coding=utf-8
from mpi4py import MPI
from utility import *

#Tag 1 signifie maitre envoie du travail a l esclave
#Tag 2 pour un message de l'esclave vers le maitre indiquant que le pbSAT a ete resolu
#Tag 3 pour un message de l'esclave vers le maitre indiquant que le pbSAT ne peut pas etre resolu (une clause est fausse)
#Tag 4 signifie l'esclave envoie un pb au maitre
#Tag 5 signifie que le problème est terminé

def comportementEsclave(comm):
    print "Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size)    
    status = MPI.Status()
    data=comm.recv(source=0,tag = MPI.ANY_TAG, status= status)

    while status.Get_tag() != 5:
        resultat=[]
        for probleme in data:
            valeursVariables,resultatPreTraitement=preTraitementSat(probleme)
            if resultatPreTraitement==True:
                #On envoie un message de type tag 2 au maître pour lui indiquer que le pb SAT a ete resolu
                #On envoie au maitre la valeur des variables resolvant le probleme SAT
                comm.send(valeursVariables,dest=0,tag=2)
                return
            
            elif resultatPreTraitement==False:
                #On envoie un message de type tag 3 au maître pour lui indiquer que le pb ne peut pas etre resolu
                comm.send(dest=0,tag=3)
            else:
                resultat.append(genererSousSat(valeursVariables,resultatPreTraitement)[0])
                resultat.append(genererSousSat(valeursVariables,resultatPreTraitement)[1])

        comm.send(resultat,dest=0,tag=4)
        data=comm.recv(source=0,tag = MPI.ANY_TAG, status= status)
    print "End message Received"
    return