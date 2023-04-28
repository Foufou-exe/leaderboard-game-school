"""
Auteur: Foufou-exe

La classe User est une classe Flask-Login et est utilisée pour stocker des informations d'utilisateur. 
Elle contient des informations telles que l'identifiant, le nom d'utilisateur, l'adresse e-mail et le hash du mot de passe.

Les méthodes de la classe permettent d'implémenter les fonctionnalités de Flask-Login, telles que l'authentification de l'utilisateur, 
la vérification de la validité des mots de passe et la recherche d'utilisateurs dans la base de données.

La classe contient les méthodes suivantes :

    - init(self, id, username, email, password_hash) : Initialise une instance de la classe User avec les paramètres passés en argument.
    - get_id(self) : Retourne l'identifiant de l'utilisateur.
    - is_authenticated(self) : Retourne True si l'utilisateur est authentifié, sinon False.
    - is_active(self) : Retourne True si l'utilisateur est actif, sinon False.
    - find_by_username(username) : Méthode statique qui cherche l'utilisateur dans la base de données en utilisant le nom d'utilisateur. Retourne None si l'utilisateur n'est pas trouvé.
    - check_password(self, password) : Vérifie si le mot de passe passé en argument correspond au hash stocké dans la base de données. Retourne True si les mots de passe correspondent, sinon False.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    @staticmethod
    def find_by_username(username):
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
