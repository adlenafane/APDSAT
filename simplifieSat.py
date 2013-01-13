# -*- coding: cp1252 -*-

def simplifieSat(pbSat, varData):
    """ entr�e: liste de liste(clauses) d�crivant le pb sat, liste d'�tat des variables: T pour True, F pour False, U pour undecided.
sortie: un nouveau probl�me sat simplifi� avec l'�tat des variables pass�es en argument"""
    if len(pbSat)==0:
        return "Erreur: le probleme ne contient aucune clause !"
    nouveauSat = []
    for clause in pbSat:
        nouvelleClause = simplifierClause(clause, varData)
        nouveauSat.append(nouvelleClause)
    return nouveauSat

def simplifieClause(clause, varData):
    """ entr�e: une clause, liste d'�tat des variables: T pour True, F pour False, U pour undecided.
sortie: un nouvelle clause simplifi� avec l'�tat des variables pass�es en argument"""
    if len(clause)==0:
        return "Erreur: la clause ne contient aucun litteral !"
    for k in clause:
        if k>0:
            if varData[k-1]=='T':
                return [True]
        elif k<0:
            if varData[k-1]=='F':
                return [True]
    return clause #cette ligne n'est atteinte que si le programme n'est pas entr� dans le if ou le elif ci-dessus
#attention pour le moment la fonction ne prend pas en compte le cas o� tous les lit�raux de la clause sont False, ce qui devrait renvoyer un False
