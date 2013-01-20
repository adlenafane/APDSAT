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
    print "Received " + str(data)

    while status.Get_tag() != 5:
        resultat=[]
        print data
        for probleme in data:
            print "Slave in for in while"
            print probleme
            valeursVariables,resultatPreTraitement=preTraitementSat(probleme)
            print valeursVariables
            print resultatPreTraitement
            if resultatPreTraitement==True:
                #On envoie un message de type tag 2 au maître pour lui indiquer que le pb SAT a ete resolu
                #On envoie au maitre la valeur des variables resolvant le probleme SAT
                comm.send(valeursVariables,dest=0,tag=2)
            
            elif resultatPreTraitement==False:
                #On envoie un message de type tag 3 au maître pour lui indiquer que le pb ne peut pas etre resolu
                comm.send(dest=0,tag=3)
            else:
                resultat.append(genererSousSat(valeursVariables,resultatPreTraitement)[0])
                resultat.append(genererSousSat(valeursVariables,resultatPreTraitement)[1])
        
        print "Termine"
        comm.send(resultat,dest=0,tag=4)
        print "Sent"
        data=comm.recv(source=0,tag = MPI.ANY_TAG, status= status)
        print "New message Received"
    return