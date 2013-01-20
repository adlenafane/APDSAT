Pre-requis:
* Python
* Une bibliothèque MPI (MPICH2, OpenMPI...)
* mpi4py

Pour executer l'algorithme:
* lancer en ligne de commande "mpiexec -n 4 python main.py" lancera le script sur 4 processus, par defaut le script s'execute sur 'uf20-01.cnf'
* le fichier main.py permet de rajouter des arguments complementaires:
		* --file "monFichier.cnf" permet d'executer le script en chargeant la forme normale conjonctive definie dans "monFichier.cnf". Le Dossier "Data" contient des exemples de fichiers CNF trouvés sur internet, et permettant de vérifier notre algorithme.
		* --batch permet de modifier la taille des messages envoyés par le maitre aux esclaves. Par exemple avec "--batch 8", le message du maitre aux esclaves contiendra 8 problemes.


