# -*- coding: cp1252 -*-
# coding=utf-8
from simplifieSat import *
from retireSingleton import *

def loadCnfFile(fileName='example.cnf'):
    """ 
    entree: le chemin vers le fichier de definition de la forme normale conjonctive. Par defaut, ce chemin est initialise a 'example.cnf'
    retourne une liste contenant: le nombre de variables, puis le nombre de clauses, puis la liste de listes d'entiers decrivants la forme normale conjonctive
    """
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
	"""
	entree: un probleme Sat (une liste de clauses)
	Renvoie un dictionnaire donant la frequence d'apparition dans la liste de clauses pour chaque litteral.
	"""
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
	"""
	Renvoie un dictionnaire avec pour chaque litteral une liste contenant le nbr d apparitions positives et negatives dans le probleme SAT
	"""
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
	"""
	Prend en entree le resultat de la fonction genererRepartitionDesPositifsEtNegatifs
	Calcule le ratio de repartion entre xi et xibarre pour chaque litteral
	"""

	result={}
	for litteral in dictionnaireDeRepartitionDesClausesEnPositifEtNegatif:
		litteralDistributionList=dictionnaireDeRepartitionDesClausesEnPositifEtNegatif[litteral]
		result[litteral]=1-abs(float(litteralDistributionList[0]-litteralDistributionList[1])/(litteralDistributionList[0]+litteralDistributionList[1]))
	return result


def calculClassementFrequence(dicoFrequence):
    """
    Renvoie une liste contenant les numeros de variables classes par ordre croissant par rapport a leur frequence
    """
    return sorted(dicoFrequence, key=lambda key: dicoFrequence[key])


def calculClassementPositifsEtNegatifs(dicoPositifsNegatifs):
    """
    Renvoie une liste contenant les numeros de variables classes par ordre croissant par rapport a leur ratio de repartition en xi et xibarre
    """
    return sorted(dicoPositifsNegatifs, key=lambda key: dicoPositifsNegatifs[key])


def calculClassementLitteraux(listeDeClauses):
    """
    Retourne une liste contenant le classement des litteraux par ordre decroissant d'"importance"
    l'importance d'un litteral augmente avec sa frequence et avec son equirepartition d'apparition en Xi et xibarre
    C est ce classement de litteraux qui va definir sur quelle variable effectuer une disjonction pour generer deux sous problemes.
    """
    listeFrequence = calculClassementFrequence(findCountOfLitterals(listeDeClauses))
    listePositifsNegatifs = calculClassementPositifsEtNegatifs(calculDuRatioDePositifsEtNegatifs(genererRepartitionDesPositifsEtNegatifs(listeDeClauses)))
    dicoClassement={}
    for i in range(0,len(listeFrequence)):
        dicoClassement[listeFrequence[i]]=i+1
    for i in range(0,len(listePositifsNegatifs)):
        dicoClassement[listePositifsNegatifs[i]]= dicoClassement[listePositifsNegatifs[i]] + (i+1)
    return sorted(dicoClassement, key=lambda key: dicoClassement[key],reverse=True)


def preTraitementSat(probleme):
	"""
	entree: une liste contenant un jeu de variables, et une liste de clause
	Cette fontion agrege les premieres operations que l esclave va effectuer quand le maitre lui envoie un probleme
	Ces operations consistent a simplifier le probleme en fonction des valeurs de variables.
	"""
    #Recuperation de la liste des variables avec valeurs T pour True, F pour False et U pour Undefined
    valeursVariables=probleme[0]
    #Recuperation du Probleme SAT a traiter
    problemeSAT=probleme[1]

    #Etapes de simplification:
    pb=simplifieSat(valeursVariables,problemeSAT)
    pb=retireSingleton(valeursVariables,pb)
    nouveauSat=pb[1]
    resultat=testSatOk(nouveauSat)   
    
    return pb[0],resultat



def genererSousSat(var,pbSat):
	"""
	entree: un jeu (valeurs des variables, probleme Sat)
	Cette fonciton va generer deux sous problemes du probleme sat passe en argument en faisant une disjonction sur une variable
	"""
    varAffectationTrue=[]
    varAffectationFalse=[]
    lengthVar=len(var)
    resultat=[]
    
    #Recuperation de la variable sur laquelle on va effectuer la disjonction
    varDisjonction=calculClassementLitteraux(pbSat)[0]
    
    #On cree l'affectation des variables pour la valeur True de la variable de disjonction
    for i in range(0,lengthVar):
        if i==(varDisjonction-1):
            varAffectationTrue.append('T')
        else:
            varAffectationTrue.append(var[i])

    #On cree l'affectation des variables pour la valeur False de la variable de disjonction
    for i in range(0,lengthVar):
        if i==(varDisjonction-1):
            varAffectationFalse.append('F')
        else:
            varAffectationFalse.append(var[i])
    #On mets tt ca dans la liste resultat
    resultat.append([varAffectationTrue,pbSat])
    resultat.append([varAffectationFalse,pbSat])

    return resultat


def simplifieSat(varData, pbSat):
    """ 
    entrée: liste de liste(clauses) décrivant le pb sat, liste d'état des variables: T pour True, F pour False, U pour undecided
    cette fonction va simplifier le pbSat compte tenu des valeurs de variables passees en argument.
    Exemple: si le pbSat en argument contient possede une clause 3 qui contient la variable 1, et que cette variable est fixee a T (True) dans varData, la fonction renvoie un nouveau probleme Sat dont la clause 3 sera [True] 
	sortie: un nouveau problème sat simplifié avec l'état des variables passées en argument
	"""
    if len(pbSat)==0:
        return "Erreur: le probleme ne contient aucune clause !"
    nouveauSat = []
    for clause in pbSat:
        nouvelleClause = simplifieClause(varData, clause)
        nouveauSat.append(nouvelleClause)
    return nouveauSat



def simplifieClause(varData,clause):
    """ 
    entree: une clause, liste d'etat des variables: T pour True, F pour False, U pour undecided
    Cette fonction simplifie la clause passee en argument compte tenu des valeurs de variables passees en argument
    Exemple: si la clause contient la variable 1, et que cette variable est fixee a T (True) dans varData, la fonction renvoie [True] pour indiquer que la clause est True
	sortie: un nouvelle clause simplifiee avec l'etat des variables passees en argument
	"""
    if len(clause)==0:
        # Si la clause est vide, c'est peutetre qu'on a enleve un F un peu salement non? On pourrait faire un check de clause non vide dans le Load
        return "Erreur: la clause ne contient aucun litteral !"
    # On suppose que la clause est fausse et si on trouve autre chose qu'un 'F' on modifiera la clause
    clauseFausse = True
    nouvelleClause = []
    for k in clause:
        if k>0:
            if varData[k-1]=='T':
                return [True]
            elif varData[k-1]=='U':
                nouvelleClause.append(k)
                clauseFausse = False
        elif k<0:
            if varData[abs(k)-1]=='F':
                return [True]
            elif varData[abs(k)-1]=='U':
                nouvelleClause.append(k)
                clauseFausse = False

    # Si clauseFausse est restee vraie, cela signifie qu'on a vu au moins une clause non fausse
    if clauseFausse == True:
        return [False]

    return nouvelleClause #cette ligne n'est atteinte que si le programme n'est pas entré dans le if ou le elif ci-dessus


def testSatOk(pbSat):
    """
    Cette fonction teste le probleme donne en arguement:
    Si le probleme est vide, renvoie True 
    Si le probleme contient une clause False, renvoie False
    Sinon, renvoie un nouveau probleme epure des clauses "True"
    """
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


def retireSingleton(varData,pbSat):
	"""
	entree: une liste de definition des variables et une liste de clause
	on cherche les clauses qui ne contiennent qu'un seul litteral 'U', si il y en a, on modifie la valeur de la valeur correspondante pour que la clause soit vraie pour pouvoir ensuite l'enlever du probleme.
	renvoie un nouveau couple (variables, nouveau probleme sat) dont le "nouveau probleme Sat" a ete epure de clause mono-litteral 'U'
	"""
	for clause in pbSat:
		if (len(clause) == 1) and (str(clause) != "[True]") and (str(clause) != "[False]"):
			k = clause[0]
			if k>0 and varData[k-1] == 'U':
				varData[k-1] = 'T'
			elif k<0 and varData[(-k)-1] == 'U':
				k = abs(k)
				varData[k-1] = 'F'
	nouveauSat = simplifieSat(varData,pbSat)
	return [varData,nouveauSat]