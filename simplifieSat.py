# -*- coding: cp1252 -*-

def simplifieSat(pbSat, varData):
    """ entrée: liste de liste(clauses) décrivant le pb sat, liste d'état des variables: T pour True, F pour False, U pour undecided.
sortie: un nouveau problème sat simplifié avec l'état des variables passées en argument"""
    if len(pbSat)==0:
        return "Erreur: le probleme ne contient aucune clause !"
    nouveauSat = []
    for clause in pbSat:
        nouvelleClause = simplifierClause(clause, varData)
        nouveauSat.append(nouvelleClause)
    return nouveauSat

def simplifieClause(clause, varData):
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
                clauseFausse = false
        elif k<0:
            if varData[k-1]=='F':
                return [True]
            elif varData[k-1]!='T':
                clauseFausse = false
    # Si clauseFausse est restee vraie, cela signifie qu'on a vu au moins une clause non fausse
    if clauseFausse == true:
        return [False]
    return clause #cette ligne n'est atteinte que si le programme n'est pas entré dans le if ou le elif ci-dessus
#attention pour le moment la fonction ne prend pas en compte le cas où tous les litéraux de la clause sont False, ce qui devrait renvoyer un False

def testSatOk(pbSat):
    if pbSat == []:
        return True
    for clause in pbSat:
        if clause == False:
            return False
        else:
            if clause != True:
                nouveauSat.append(clause)
    return nouveauSat