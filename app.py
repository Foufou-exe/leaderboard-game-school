import subprocess
import os

if __name__ == "__main__":
    chemin_python = os.path.abspath(__file__)
    repertoire_travail = os.path.dirname(chemin_python)
    app_connexion = os.path.join(repertoire_travail, "app/app.py")
    subprocess.call(["python", app_connexion], shell=True)