
import pymongo
import sys

sys.path.append('..')
from config import MONGODB_PASSWORD

# Create a MongoDB client and connect to the server
client = pymongo.MongoClient(f'mongodb+srv://thibaut:{MONGODB_PASSWORD}@cluster0.uvzljom.mongodb.net/?retryWrites=true&w=majority')
# Create a database named "leaderboard"
db = client["leaderboard"]
connexions = db["Connexion"]

# Test username
test_username = "user1"
password = "mdp1"
if user_data := connexions.find_one({"username": test_username}):
    print(f"Utilisateur trouvé: {user_data}")
else:
    print("Aucun utilisateur trouvé avec ce nom d'utilisateur.")