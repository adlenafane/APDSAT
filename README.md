Pre-requis:
* Python
* Une bibliothèque MPI: MPICH2

Installation de la librairie MPI4Py:
Pré-requis: librairie PIP installée
* Lancer la ligne de commande: ```[sudo] pip install mpi4py```
Normallement, mpi4py doit être correctement installé suite à cela

* Cependant, il peut parfois être nécessaire de procéder différemment:
Note de la doc:  If the mpicc compiler wrapper is not on your search path (or if it has a different name) you can use env to pass the environment variable MPICC providing the full path to the MPI compiler wrapper executable:
```[sudo] env MPICC=/path/to/mpicc pip install mpi4py```
Soit, dans mon cas: ```env MPICC=/Users/nicolas/APD/mpich2-install/bin/mpicc pip install mpi4py```


Pour executer l'algorithme:
* lancer en ligne de commande par exemple: ```mpiexec -n 4 python main.py```, qui lancera le script sur 4 processus, par defaut le script s'execute sur 'uf20-01.cnf'
* Pour lancer la résolution avec une file FIFO, il faut utiliser le fichier main.py, pour la gestion avec priorité main_priority.py, pour l'aléatoire main_random.py
* Le fichier main.py permet de rajouter des arguments complementaires:
		* ```--file "monFichier.cnf"``` permet d'executer le script en chargeant la forme normale conjonctive definie dans "monFichier.cnf". Le Dossier "Data" contient des exemples de fichiers CNF trouvés sur internet, et permettant de vérifier notre algorithme.
		* ```--batch n``` permet de modifier la taille des messages envoyés par le maitre aux esclaves: n etant le nombre de travaux à envoyer par message. Par exemple avec "--batch 8", le message du maitre aux esclaves contiendra 8 problemes.

Contenu des fichiers
* Fichier main.py, main_random.py, main_priority.py correspondent au lancement de l'algorithme sur l'ensemble des processeurs demandés
* Fichier master.py, master_random.py, master_priority correspondent au comportement du maitre en fonction de la file d'attente choisie. Chacun de ces fichiers/comportement et appelé par le main correspondant
* Fichier slave.py implémente le comportement de l'esclave, indépendant de la file d'attente choisie
* Fichier utility.py correspond aux fonctions utilitaires utilisées, notamment par les esclaves
* Dossiers data et BigData regroupent des exemples de jeux de données

A noter que tout le code MPI est concentré dans slave.py, master.py (et main.py pour l'initialisation).
