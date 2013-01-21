import os

path = 'data/'
listing = os.listdir(path)

for tailleDeBatch in [2**x for x in range(2,10)]:
	for filename in listing:
		for i in range(1, 2):
			os.system("mpiexec -n 4 python main.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))
os.system("python sequentiel.py" + " --file "+ "data/" +  str(filename))

for tailleDeBatch in [2**x for x in range(2,10)]:
	for filename in listing:
		for i in range(1, 2):
			os.system("mpiexec -n 4 python main_random.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))
os.system("python sequentiel.py" + " --file "+ "data/" +  str(filename))

