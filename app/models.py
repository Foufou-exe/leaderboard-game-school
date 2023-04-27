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
        # Chercher l'utilisateur dans la base de données
        # Retourne None si l'utilisateur n'est pas trouvé
        return None

    def check_password(self, password):
        # Vérifier le mot de passe en utilisant le hash stocké dans la base de données
        return check_password_hash(self.password_hash, password)
