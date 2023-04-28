"""Auteur: Foufou-exe"""

import subprocess
import os

if __name__ == "__main__":
    """
        Si ce script est exécuté directement, la variable name prend la valeur 'main'. Dans ce cas,
        la variable chemin_python est initialisée avec le chemin absolu du script courant et la variable
        repertoire_travail est initialisée avec le répertoire contenant le script courant.
        Ensuite, la variable app_connexion est initialisée avec le chemin du script app.py situé dans le même
        répertoire que le script courant.
        Enfin, le script app.py est exécuté en appelant la fonction call() du module subprocess, avec comme
        arguments la commande à exécuter ("python" suivi du chemin de app.py) et l'option shell=True.
    """
    chemin_python = os.path.abspath(__file__)
    repertoire_travail = os.path.dirname(chemin_python)
    app_connexion = os.path.join(repertoire_travail, "app/app.py")
    subprocess.call(["python", app_connexion], shell=True)