from datetime import datetime
import pymongo
import sys

sys.path.append('..')
from config import MONGODB_PASSWORD

# Create a MongoDB client and connect to the server
client = pymongo.MongoClient(f'mongodb+srv://thibaut:{MONGODB_PASSWORD}@cluster0.uvzljom.mongodb.net/?retryWrites=true&w=majority')
# Create a database named "leaderboard"
db = client["leaderboard"]

# Collection Utilisateur
utilisateurs = db["Utilisateur"]
utilisateurs_data = [
  { "id_user": 1, "scoreTotal": 100, "Finalposition": 1 },
  { "id_user": 2, "scoreTotal": 150, "Finalposition": 2 },
  { "id_user": 3, "scoreTotal": 200, "Finalposition": 3 },
  # ... Ajoutez plus d'utilisateurs ici
]
utilisateurs.insert_many(utilisateurs_data)

# Collection Partie
parties = db["Partie"]
parties_data = [
  { "id_partie": 1, "partie": 1, "_date": datetime(2023, 4, 20), "_position": 1, "name": "Nom de la partie 1", "score": 1000 },
  { "id_partie": 2, "partie": 2, "_date": datetime(2023, 4, 21), "_position": 2, "name": "Nom de la partie 2", "score": 1500 },
  { "id_partie": 3, "partie": 3, "_date": datetime(2023, 4, 22), "_position": 3, "name": "Nom de la partie 3", "score": 2000 },
  # ... Ajoutez plus de parties ici
]
parties.insert_many(parties_data)

# Collection Connexion
connexions = db["Connexion"]
from werkzeug.security import generate_password_hash

connexions_data = [
    {"id_connexion": 1, "username": "user1", "password": generate_password_hash("mdp1"), "email": "user1@example.com"},
    {"id_connexion": 2, "username": "user2", "password": generate_password_hash("mdp2"), "email": "user2@example.com"},
    {"id_connexion": 3, "username": "user3", "password": generate_password_hash("mdp3"), "email": "user3@example.com"},
    # ... Ajoutez plus de connexions ici
]
connexions.delete_many({})
connexions.insert_many(connexions_data)

# Collection UtilisateurJouePartie
utilisateur_joue_partie = db["UtilisateurJouePartie"]
utilisateur_joue_partie_data = [
  { "id_user": 1, "id_partie": 1 },
  { "id_user": 1, "id_partie": 2 },
  { "id_user": 2, "id_partie": 1 },
  # ... Ajoutez plus d'enregistrements ici
]
utilisateur_joue_partie.insert_many(utilisateur_joue_partie_data)

# Collection ConnexionAppartient
connexion_appartient = db["ConnexionAppartient"]
connexion_appartient_data = [
  { "id_user": 1, "id_connexion": 1 },
  { "id_user": 2, "id_connexion": 2 },
  { "id_user": 3, "id_connexion": 3 },
  # ... Ajoutez plus d'enregistrements ici
]
connexion_appartient.insert


# Collection Utilisateur
utilisateurs = db["Utilisateur"]
utilisateurs.create_index("scoreTotal")
utilisateurs.create_index("Finalposition")

# Collection Partie
parties = db["Partie"]
parties.create_index("_date")
parties.create_index("_position")
parties.create_index("name")
parties.create_index("score")

# Collection Connexion
connexions = db["Connexion"]
connexions.create_index("username")
connexions.create_index("email")

# Collection UtilisateurJouePartie
utilisateur_joue_partie = db["UtilisateurJouePartie"]
utilisateur_joue_partie.create_index("id_user")
utilisateur_joue_partie.create_index("id_partie")

# Collection ConnexionAppartient
connexion_appartient = db["ConnexionAppartient"]
connexion_appartient.create_index("id_user")
connexion_appartient.create_index("id_connexion")