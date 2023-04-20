# LIB APP
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient

# LIB LOGIN 
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from datetime import datetime, timedelta

from config import MONGODB_PASSWORD, SECRET_KEY


# Ajoutez la fonction document_to_dict ici
def document_to_dict(document):
    if document is not None:
        document_dict = dict(document)
        document_dict["_id"] = str(document["_id"])
        return document_dict
    return None


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY



mongo = MongoClient(f'mongodb+srv://******:{MONGODB_PASSWORD}@cluster0.uvzljom.mongodb.net/leaderboard?retryWrites=true&w=majority')
db = mongo.get_default_database('leaderboard')
users = db["Connexion"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({"_id": user_id})
    return (
        User(
            user_data["_id"],
            user_data["username"],
            user_data["email"],
            user_data["password"],
        )
        if user_data
        else None
    )

    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method != 'POST':
        return render_template('register.html')
    # Check if the username or email is already taken
    username = request.form['username']
    email = request.form['email']
    if existing_user := users.find_one(
        {"$or": [{"username": username}, {"email": email}]}
    ):
        flash('Le nom d\'utilisateur ou l\'adresse e-mail est déjà utilisé.', 'error')
        return redirect(url_for('register'))
    # Add the new user to the database
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        flash('Les mots de passe ne correspondent pas.', 'error')
        return redirect(url_for('register'))
    hashed_password = generate_password_hash(password)
    user_id = users.insert_one({"username": username, "email": email, "password": hashed_password}).inserted_id
    user = User(user_id, username, email, hashed_password)
    login_user(user)
    flash('Inscription réussie !', 'success')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user_data = users.find_one({"username": username})
    if user_data and check_password_hash(user_data['password'], password):
        user = User(user_data["_id"], user_data["username"], user_data["email"], user_data["password"])
        login_user(user)
        return redirect(url_for('dashboard'))
    flash('Nom d\'utilisateur ou mot de passe invalide.', 'error')
    return redirect(url_for('login'))




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', current_user=current_user)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
