# -*- coding: cp1252 -*-
# coding=utf-8

def loadCnfFile(fileName='example.cnf'):
    """ retourne une liste contenant: le nombre de variables, puis le nombre de clauses, puis la liste de listes d'entiers decrivants la forme normale conjonctive"""
    result=[]
    cnf=[]
    with open(fileName) as cnfFile:
        for line in cnfFile:
            if line.startswith("p"):   #on extrait les infos de la ligne de configuration du fichier cnf
                result.append(int(line.split()[2]))
                result.append(int(line.split()[3]))
            elif line[0]!="c":
                cnf.append([int(x) for x in line.split(" 0")[0].split()])  #split(" 0" découpe la chaine de caractère en une liste de sous chaines autour de la sous chaine " 0"
    result.append(cnf)
    return result


def findCountOfLitterals(listOfClauses):
	countOfLitterals = {}
	# Parcours de toutes les clauses pour prendre les valeurs absolues
	for clause in listOfClauses:
		# Applique la fonction abs a chaque element de la clause
		tempClause = map(abs, clause)
		# Met a jour le compte des litteraux en parcourant la clause en valeur absolue
		for litteral in tempClause:
			# Si le litteral existe dans le dictionnaire on ajoute 1
			if litteral in countOfLitterals:
				countOfLitterals[litteral] += 1
			# Sinon on cree la cle
			else:
				countOfLitterals[litteral] = 1
	return countOfLitterals

def genererRepartitionDesPositifsEtNegatifs(listeDeClauses):
	#Renvoie un dico avec pour chaque litteral une liste contenant le nbr d apparitions positives et negatives dans le probleme SAT
	result={}
	for clause in listeDeClauses:
		for litteral in clause:
			if abs(litteral) in result:
				if litteral>0:
					result[abs(litteral)][0]=result[abs(litteral)][0]+1
				elif litteral<0:
					result[abs(litteral)][1]=result[abs(litteral)][1]+1
				else:
					return "Error - 0 in listeDeClauses"

			else:
				if litteral>0:
					result[abs(litteral)]=[1,0]
				elif litteral<0:
					result[abs(litteral)]=[0,1]
				else:
					return "Error - 0 in listeDeClauses"
	return result

def calculDuRatioDePositifsEtNegatifs(dictionnaireDeRepartitionDesClausesEnPositifEtNegatif):
	# Prend en entree le resultat de la fonction genererRepartitionDesPositifsEtNegatifs
	#Calcule le ratio de repartion entre xi et xibarre pour chaque litteral
	result={}
	for litteral in dictionnaireDeRepartitionDesClausesEnPositifEtNegatif:
		litteralDistributionList=dictionnaireDeRepartitionDesClausesEnPositifEtNegatif[litteral]
		result[litteral]=abs(float(litteralDistributionList[0]-litteralDistributionList[1])/(litteralDistributionList[0]+litteralDistributionList[1]))
	return result
