# -*- coding: cp1252 -*-
# coding=utf-8

def simplifieSat(varData, pbSat):
    """ entrée: liste de liste(clauses) décrivant le pb sat, liste d'état des variables: T pour True, F pour False, U pour undecided.
sortie: un nouveau problème sat simplifié avec l'état des variables passées en argument"""
    if len(pbSat)==0:
        return "Erreur: le probleme ne contient aucune clause !"
    nouveauSat = []
    for clause in pbSat:
        nouvelleClause = simplifieClause(varData, clause)
        nouveauSat.append(nouvelleClause)
    return nouveauSat

def simplifieClause(varData,clause):
    """ entrée: une clause, liste d'état des variables: T pour True, F pour False, U pour undecided.
sortie: un nouvelle clause simplifié avec l'état des variables passées en argument"""
    if len(clause)==0:
        return "Erreur: la clause ne contient aucun litteral !"
    # On suppose que la clause est fausse et si on trouve autre chose qu'un 'F' on modifiera la clause
    clauseFausse = True
    for k in clause:
        if k>0:
            if varData[k-1]=='T':
                return [True]
            elif varData[k-1]!='F':
                clauseFausse = False
        elif k<0:
            k = abs(k)
            if varData[k-1]=='F':
                return [True]
            elif varData[k-1]!='T':
                clauseFausse = False
    # Si clauseFausse est restee vraie, cela signifie qu'on a vu au moins une clause non fausse
    if clauseFausse == True:
        return [False]
    return clause #cette ligne n'est atteinte que si le programme n'est pas entré dans le if ou le elif ci-dessus


def testSatOk(pbSat):
    #Renvoie True ou False si le problème est terminé, et supprime les clauses composées uniquement de True
    nouveauSat = []
    if pbSat == []:
        return True
    for clause in pbSat:
        if clause == [False]:
            return False
        else:
            if str(clause) != "[True]":
                print "Clause: " + str(clause)
                nouveauSat.append(clause)
    return nouveauSat

