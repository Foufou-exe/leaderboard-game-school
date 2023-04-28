"""
Auteur: Foufou-exe

Le module contient une application web Flask avec les fonctionnalités suivantes :

   - connexion
   - inscription
   - réinitialisation de mot de passe
   - tableau de bord
   - gestion des scores de jeu
    Les différentes bibliothèques importées sont :

   - bson pour manipuler les identifiants ObjectId de MongoDB
   - Flask pour créer l'application web
   - flask_login pour gérer la connexion/déconnexion des utilisateurs
   - pymongo pour manipuler la base de données MongoDB
   - os pour accéder aux variables d'environnement et gérer les chemins de fichiers
   - logging pour gérer les messages de log
   - datetime pour manipuler les dates
   - uuid pour générer des identifiants uniques
    Les variables MONGODB_PASSWORD, MONGODB_USER et SECRET_KEY sont définies à partir des variables d'environnement.

    La fonction load_user() est un gestionnaire d'utilisateur pour Flask-Login qui charge un utilisateur à partir de la base de données MongoDB.

    L'application contient les routes suivantes :

    - "/" : redirige vers la page de connexion
    - "/register" : gère l'inscription d'un nouvel utilisateur
    - "/login" : gère la connexion d'un utilisateur existant
    - "/reset_password" : gère la réinitialisation du mot de passe d'un utilisateur
    - "/logout" : déconnecte l'utilisateur actuel
    - "/dashboard" : affiche le tableau de bord de l'utilisateur
    - "/api/scores" : renvoie les scores pour un jeu donné au format JSON
    - "/api/add_game" : ajoute un nouveau jeu à la base de données
    - "/api/add_score" : ajoute un nouveau score à la base de données
    - "/api/game_stats" : renvoie les statistiques de jeu pour l'utilisateur actuel au format JSON
    
    La fonction get_scores() récupère les scores pour un jeu donné à partir de la base de données.

    La fonction get_game_stats() récupère les statistiques de jeu pour l'utilisateur actuel à partir de la base de données.

    La fonction inject_cache_buster() ajoute une chaîne aléatoire à l'URL pour éviter le caching des fichiers statiques.

    Si le script est exécuté directement, l'application est lancée sur le port 80.
"""

# LIB APP
from bson import ObjectId
from flask import Flask, jsonify, make_response
from flask_login import LoginManager
from pymongo import MongoClient
import os

# LIB LOGIN
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

# LIB GESTION DES ERREURS
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import uuid



MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_USER = os.environ.get("MONGODB_USER")
SECRET_KEY = os.environ.get("SECRET_KEY")



app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

log_filename = "app-" + datetime.now().strftime("%Y-%m-%d") + ".log"
chemin_python = os.path.abspath(__file__)
repertoire_travail = os.path.dirname(chemin_python)
log = os.path.join(repertoire_travail, f"logs/{log_filename}")

log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler = logging.handlers.RotatingFileHandler(
    log,
    maxBytes=1024 * 1024,
    backupCount=5,
)


logging.getLogger("werkzeug").setLevel(logging.DEBUG)
logging.getLogger("werkzeug").addHandler(handler)
app.logger.setLevel(logging.WARNING)
app.logger.setLevel(logging.INFO)
app.logger.setLevel(logging.ERROR)
app.logger.addHandler(handler)

mongo = MongoClient(
    f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@cluster0.uvzljom.mongodb.net/leaderboard?retryWrites=true&w=majority"
)
db = mongo.get_default_database("leaderboard")
users = db["User"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(
            str(user_data["_id"]),
            user_data["username"],
            user_data["email"],
            user_data["password"],
        )
    else:
        return None



@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method != "POST":
        
        return render_template("register.html")
    
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    existing_user = users.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        app.logger.error(f"User {username} already exists or email already used")
        flash("A user with that username or email already exists", "error")
        return redirect(url_for("register"))

    
    if password != confirm_password:
        flash("Passwords do not match", "error")
        app.logger.error(f"Passwords do not match for user {username}")
        return redirect(url_for("register"))

    
    hashed_password = generate_password_hash(password)

    
    user_data = {"username": username, "email": email, "password": hashed_password}
    result = users.insert_one(user_data)
    
    user_id = str(result.inserted_id)

    
    user = User(user_id, username, email, password)
    login_user(user)

   
    app.logger.info(f"New user registered: {username}")
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    user_data = users.find_one({"username": username})
    if user_data and check_password_hash(user_data["password"], password):
        user = User(
            str(user_data["_id"]),
            user_data["username"],
            user_data["email"],
            user_data["password"],
        )
        login_user(user)
        app.logger.info(f"User {username} logged in")
        flash({"type": "success", "message": "Vous êtes connecté !"})
        return redirect(url_for("dashboard"))
    app.logger.error(f"User {username} tried to log in with wrong password")
    flash({"type": "error", "message": "Nom d'utilisateur ou mot de passe invalide."})
    return redirect(url_for("login"))


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        
        username = request.form["username"]
        email = request.form["email"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        
        user = users.find_one({"username": username})
        if user and user["email"] == email:
           
            if new_password != confirm_password:
                app.logger.error(
                    f"User {username} tried to reset password with wrong confirmation"
                )
                flash("Les mots de passe ne correspondent pas.", "error")
                return redirect(url_for("reset_password"))
            # Update user's password
            hashed_password = generate_password_hash(new_password)
            users.update_one(
                {"_id": user["_id"]}, {"$set": {"password": hashed_password}}
            )
            app.logger.info(f"User {username} reset password")
            flash(
                {"type": "success", "message": "Mot de passe mis à jour avec succès !"}
            )
            return redirect(url_for("login"))
        else:
            app.logger.error(
                f"User {username} tried to reset password with wrong email"
            )
            flash({"type": "error", "message": "Nom d'utilisateur ou e-mail invalide."})
            return redirect(url_for("reset_password"))

    
    return render_template("reset_password.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if not current_user.is_authenticated:
        app.logger.error("User tried to access leaderboard without being logged in")
        flash(
            {
                "type": "error",
                "message": "Vous devez être connecté pour accéder à cette page.",
            }
        )
        return redirect(url_for("login"))

    jeux_collection = db["Jeux"]
    jeux = jeux_collection.find()
    jeux_list = list(jeux)

    response = make_response(render_template("index.html", jeux=jeux_list))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Expires"] = "-1"
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/api/scores", methods=["GET"])
@login_required
def api_scores():
    game_id = request.args.get("game_id")
    scores = get_scores(game_id)
    return jsonify(scores)


@login_required
def get_scores(game_id):
    if not current_user.is_authenticated:
        return (
            jsonify({"error": "Vous devez être connecté pour accéder à cette page."}),
            401,
        )
    partie_collection = db["Partie"]
    user_partie_collection = db["User_Partie"]
    user_collection = db["User"]

    parties = partie_collection.find({"id_jeux": ObjectId(game_id)})
    scores = {}
    for partie in parties:
        user_parties = user_partie_collection.find(
            {"id_partie": ObjectId(partie["_id"])}
        )
        for user_partie in user_parties:
            user_id = user_partie["id_user"]
            if str(user_id) not in scores:
                user = user_collection.find_one({"_id": ObjectId(user_id)})
                if user:
                    scores[str(user_id)] = {"username": user["username"], "score": 0}
            scores[str(user_id)]["score"] += user_partie["score"]

    sorted_scores = sorted(scores.values(), key=lambda x: x["score"], reverse=True)


    if str(game_id) == "644a6c68fb7f12aafa1c195d":
        sorted_scores.reverse()

    return {"scores": sorted_scores}


@app.route("/api/add_game", methods=["POST"])
@login_required
def api_add_game():
    if not current_user.is_authenticated:
        return (
            jsonify({"error": "Vous devez être connecté pour accéder à cette page."}),
            401,
        )

    game_name = request.json.get("name")
    print(game_name)

    if not game_name:
        return jsonify({"error": "Le nom du jeu est requis."}), 400

    jeux_collection = db["Jeux"]
    jeux_collection.insert_one({"name": game_name})

    return jsonify({"success": True})


@app.route("/api/add_score", methods=["POST"])
@login_required
def api_add_score():
    if not current_user.is_authenticated:
        return (
            jsonify({"error": "Vous devez être connecté pour accéder à cette page."}),
            401,
        )

    game_id = request.json.get("game_id")
    score = request.json.get("score")
    date = request.json.get("date")

    if not game_id or not score or not date:
        return (
            jsonify(
                {"error": "Toutes les données sont requises (game_id, score et date)."}
            ),
            400,
        )

    partie_collection = db["Partie"]
    user_partie_collection = db["User_Partie"]

    partie = {"id_jeux": ObjectId(game_id), "date": date}
    partie_id = partie_collection.insert_one(partie).inserted_id

    user_partie = {
        "id_user": ObjectId(current_user.id),
        "id_partie": partie_id,
        "score": int(score),
    }
    user_partie_collection.insert_one(user_partie)

    return jsonify({"success": True})


@app.route("/api/game_stats", methods=["GET"])
@login_required
def api_game_stats():
    game_stats = get_game_stats()
    return jsonify(game_stats)


@login_required
def get_game_stats():
    if not current_user.is_authenticated:
        return (
            jsonify({"error": "Vous devez être connecté pour accéder à cette page."}),
            401,
        )
    partie_collection = db["Partie"]
    user_partie_collection = db["User_Partie"]
    jeux_collection = db["Jeux"]

    games = jeux_collection.find()
    game_stats = []

    for game in games:
        game_id = game["_id"]
        total_wins = 0
        total_losses = 0

        parties = partie_collection.find({"id_jeux": ObjectId(game_id)})
        for partie in parties:
            user_partie = user_partie_collection.find_one(
                {
                    "id_partie": ObjectId(partie["_id"]),
                    "id_user": ObjectId(current_user.id),
                }
            )
            if user_partie:
                if user_partie["score"] > 0:
                    total_wins += 1
                else:
                    total_losses += 1

        game_stats.append(
            {"name": game["name"], "wins": total_wins, "losses": total_losses}
        )

    return {"gameStats": game_stats}


@app.context_processor
def inject_cache_buster():
    def cache_bust_url(url):
        return f"{url}?v={uuid.uuid4()}"

    return {"cache_bust_url": cache_bust_url}


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
