#TODO

*Fonction pour évaluer la valeur d'une clause en fonction des litéraux (T, F, [littéraux restants])*  
```
simplifieClause(Clause)  
	return nouvelleClause 
```

*Fonction pour évaluer le nouveau SAT en fonction des valeurs des littéraux*  
```
simplifieSAT ([pbSAT], [data])  
	for clause in [pbSAT]  
		nvlleClause = simplifierClause(clause)  
		[nouveauSAT].append(nvlleclause)  
	return [nouveuSAT]  
```

*Evalue le pb SAT et renvoie soit un message de fin soit un nouveau pbSAT*  
```
testSAT([pbSAT])  
	if [pbSAT]  
		return youpi  
	for clause in [pbSAT]  
		if clause == F  
			return dead  
		else  
			if clause != T  
				[nouveauSAT].append(clause)  
```

*Parcours les clauses et modifie les données en conséquence  
Note: Ne pas oublier de réappliquer simplifieSAT lorsqu'on modifie une variable*  
```
removeSingletonClauses([pbSAT])  
	return([pbSAT], [data])  
```

*Calcul la fréquence d'apparition de chaque variable*  
```
calculfrequence([pbSAT])  
	return listeOrDicoVariableCount  
```

*Renvoyer les 2 messages au maitre*  
```
renvoyerResultatAuMaitre(SAT1, data1, branch)  
	envoyerMessageMaitre(SAT1, data avec le branch à T)  
	envoyerMessageMaitre(SAT1, data avec le branch à F)  
```

*Maitre gérer la pile et les messages (reception et emission)*  
  
*Esclave*  
```
SAT1 = simplifieSAT(SAT0, data0)  
resultTemp = removeSingletonClause(SAT1, data0)  
SAT1 = resultTemp[0]  
data1 = resultTemp[1]  
	if (testSAT(SAT1) == message)  
		envoieMessageAuMaitre  
	else   
		SAT1 = testSAT(SAT1)  
		dico = calculFrequence(SAT1)  
		renvoyerResultatAuMaitre(SAT1, data1, branch)  
```