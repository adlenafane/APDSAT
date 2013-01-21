Pre-requis:
* Python
* Une bibliothèque MPI (MPICH2, OpenMPI...)
* mpi4py

Pour executer l'algorithme:
* lancer en ligne de commande "mpiexec -n 4 python main.py" lancera le script sur 4 processus, par defaut le script s'execute sur 'uf20-01.cnf'
* le fichier main.py permet de rajouter des arguments complementaires:
		* --file "monFichier.cnf" permet d'executer le script en chargeant la forme normale conjonctive definie dans "monFichier.cnf". Le Dossier "Data" contient des exemples de fichiers CNF trouvés sur internet, et permettant de vérifier notre algorithme.
		* --batch permet de modifier la taille des messages envoyés par le maitre aux esclaves. Par exemple avec "--batch 8", le message du maitre aux esclaves contiendra 8 problemes.
* Pour lancer la résolution avec une file FIFO, il faut utiliser le fichier main.py, pour la gestion avec priorité main_priority.py, pour l'aléatoire main_random.py

Contenu
Liste des fichiers
* Fichier main.py, main_random.py, main_priority.py correspondent au lancement de l'algorithme sur l'ensemble des processeurs demandés
* Fichier master.py, master_random.py, master_priority correspondent au comportement du maitre en fonction de la file d'attente choisie. Chacun de ces fichiers/comportement et appelé par le main correspondant
* Fichier slave.py implémente le comportement de l'esclave, indépendant de la file d'attente choisie
* Fichier utility.py correspond aux fonctions utilitaires utilisées, notamment par les esclaves
* Dossiers data et BigData regroupent des exemples de jeux de données
