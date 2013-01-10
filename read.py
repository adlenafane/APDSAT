# -*- coding: cp1252 -*-

def loadCnfFile(fileName='example.cnf'):
    """ retourne une liste contenant: le nombre de variables, puis le nombre de clauses, puis la liste de listes d'entiers decrivants la forme normale conjonctive"""
    result=[]
    cnf=[]
    with open(fileName) as cnfFile:
        for line in cnfFile:
            if line.startswith("p"):
                result.append(int(line.split()[2]))
                result.append(int(line.split()[3]))
            elif line[0]!="c":
                cnf.append([int(x) for x in line.split("0")[0].split()])
    result.append(cnf)
    return result


def varFreqTable(loadedCnf):
"""en entree: la sortie de loadCnfFile: liste contenant: le nombre de variables, puis le nombre de clauses, puis la liste de listes d'entiers decrivants la forme normale conjonctive
en sortie: un dictionnaire avec la variable : son nombre de fois ou elle apparait dans le problème"""
    dico={}
    for clause in loadedCnf[2]:
    for var in clause:
            a=abs(var)
            if str(a) in dico:
                dico[str(a)]+=1
            else:
                dico[str(a)]=1
    return dico
