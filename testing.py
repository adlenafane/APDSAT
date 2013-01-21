import os

path = 'data/'
listing = os.listdir(path)

for tailleDeBatch in [2**x for x in range(6)]:
	for filename in listing:
		for i in range(1, 2):
			os.system("mpiexec -n 2 C:\Python27\python.exe main_random.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))
			os.system("mpiexec -n 4 C:\Python27\python.exe main_random.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))
			os.system("mpiexec -n 6 C:\Python27\python.exe main_random.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))
			os.system("mpiexec -n 2 C:\Python27\python.exe main_priority.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))
			os.system("mpiexec -n 4 C:\Python27\python.exe main_priority.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))
			os.system("mpiexec -n 6 C:\Python27\python.exe main_priority.py" + " --file "+ "data/" + str(filename) +" --batch " + str(tailleDeBatch))

for i in range(1,20): 
	os.system("mpiexec -n 4 C:\Python27\python.exe main_random.py --file data/uf75-01.cnf --batch 16")
	os.system("mpiexec -n 4 C:\Python27\python.exe main_priority.py --file data/uf75-01.cnf --batch 16")
