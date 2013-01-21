import os
from random import choice

path = 'data/'
listing = os.listdir(path)
k=0


for n in range(1, len(listing)):
	filename=choice(listing)
	print "\n\n"+str(filename)
	print "Sequentiel:"
	os.system("python sequentiel.py" + " --file "+ "data/" +  str(filename))
	for tailleDeBatch in [2**x for x in range(2,5)]:
		k+=1
		print "\n\n"+str(k)	
		print str(filename)
		os.system("mpiexec -n 4 python main_random.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))



for tailleDeBatch in [2**x for x in range(2,5)]:
	for n in range(1, len(listing)):
		filename=choice(listing)
		os.system("mpiexec -n 4 python main.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))