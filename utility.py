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

