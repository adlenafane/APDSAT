# coding=utf-8
from mpi4py import MPI
from simplifieSat import *
from utility import *
from retireSingleton import *

#Tag 1 signifie maitre envoie du travail a l esclave
#Tag 2 pour un message de l'esclave vers le maitre indiquant que le pbSAT a ete resolu
#Tag 3 pour un message de l'esclave vers le maitre indiquant que le pbSAT ne peut pas etre resolu (une clause est fausse)
#Tag 4 signifie l'esclave envoie un pb au maitre


def comportementEsclave(comm):
    print "Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size)
        
        
    data=comm.recv(source=0,tag=1)
    print "Received " + str(data)
    resultat=[]
    for probleme in data:
        valeursVariables,resultatPreTraitement=preTraitementSat(probleme)
        
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

"""
Modification à implémenter quand on comprendra mieux le fonctionnement des messages, sinon les esclaves ne pourront que faire une tâche et/ou ne jamais s'arrêter
def comportementEsclave(comm):
    print "Hello! I'm rank %d from %d running in total..." % (comm.rank, comm.size)
    problemeFini = False
    while(problemeFini != True):
        data=comm.recv(source=0, tag=MPI.ANY_TAG)
        status = MPI.Request()
        if status.Get_tag()==1:
            print "Received " + str(data)
            resultat=[]
            for probleme in data:
                valeursVariables,resultatPreTraitement=preTraitementSat(probleme)
                if resultatPreTraitement==True:
                    #On envoie un message de type tag 2 au maître pour lui indiquer que le pb SAT a ete resolu
                    #On envoie au maitre la valeur des variables resolvant le probleme SAT
                    comm.send(valeursVariables,dest=0,tag=2)
                    problemeFini = True

                elif resultatPreTraitement==False:
                    #On envoie un message de type tag 3 au maître pour lui indiquer que le pb ne peut pas etre resolu
                    comm.send(dest=0,tag=3)
                else:
                    resultat.append(genererSousSat(valeursVariables,resultatPreTraitement)[0])
                    resultat.append(genererSousSat(valeursVariables,resultatPreTraitement)[1])
            
            print "Termine"
            comm.send(resultat,dest=0,tag=4)
        if status.Get_tag()==2:
            problemeFini = True
"""