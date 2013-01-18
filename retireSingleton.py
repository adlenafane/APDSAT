from simplifieSat import *

def retireSingleton(varData,pbSat):
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