from flask import Flask, jsonify, render_template,request,redirect,url_for,session
import json
import bcrypt

# ça manque de front par ici


app = Flask(__name__, static_folder='./build/static', template_folder='./build')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    data = {'key': 'value'}
    return jsonify(data)


# Page d'inscription pour les utilisateurs
@app.route('/register', methods=['GET', 'POST'])
def register():

    # si on envoi des données (formulaire)
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # on ajoute le nouvelle user au fichier json des users
        user = {
            "id": id,
            "password": hashed_password
        }

        # on récupére l'ancien json pour le mettre à jour
        with open("users.json", "r") as f:
            # on récupére les users sous forme de dico
            data = json.load(f)
            # on rajoute le new user au dico
            data["users"].append(user)

        # on écrase le fichier user avec les users + le new user
        with open("users.json", "w") as f:
            f.write("")
            json.dump(data, f)


        # on redirige vers la page de connection
        return redirect(url_for('login'))

    # on attend que le formulaire sois rempli
    return render_template('register.html')


# Page de connexion pour les utilisateurs
@app.route('/login', methods=['GET', 'POST'])
def login():
    # si rempli le formulaire de connexion on récup des entrées
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password'].encode('utf-8')

        # on récupére le json des users
        with open("users.json", "r") as f:
            # on récupére les users sous forme de dico
            data = json.load(f)

        # pour chacun de mes user
        for user in data["users"]:
            # si c'est le user qui se connecte
            if user['id'] == id:
                # si le mdp est correct
                if bcrypt.checkpw(password, user['password']):
                    # je crée la session associé au id (admin ou users)
                    session['user_id'] = id
                    session['user_name'] = user['name']
                    # je redirige vers le site web adapté à la personne connecter (admin ou users)
                    return redirect(url_for('dashboard'))
        # si aucun user ne correspond on renvoi à la connexion et on indique que c'est incorrect
        return render_template('login.html', error="Email ou mot de passe incorrect")

    # on attend que le formulaire sois remplis
    return render_template('login.html')


# Tableau de bord pour les utilisateurs
@app.route('/dashboard')
def dashboard():
    # on verifie que le user est co
    if 'user_id' in session:
        return render_template('dashboard.html', user=session['user_name'])
    # sinon on lui dis de se co
    else:
        return redirect(url_for('login'))


# Déconnexion de l'utilisateur
@app.route('/logout')
def logout():
    # si on se déco on détruit la session et retourne à l'acceuil
    session.clear()
    return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True)
