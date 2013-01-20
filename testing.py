import os

for i in range(1, 5):
	resultat = os.system("mpiexec -n 5 C:\Python27\python.exe main.py")

