from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = str(id)
        self.username = username
        self.email = email
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    
    def get_id_user(self):
        return self.id_user
