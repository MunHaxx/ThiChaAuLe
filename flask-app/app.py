from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import stripe
from pymongo import MongoClient

# Se connecter à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.commerce_db

# Définir la collection 'users'
users_collection = db['users']

# Définir la collection 'stocks'
stocks_collection = db['stocks']

app = Flask(__name__, static_folder='./build/static', template_folder='./build')
app.secret_key = 'my super secret key'.encode('utf8')

# configuration de l'interface de paiement
stripe.api_key = "secret_key"


# accueil
@app.route('/')
def index():
    return render_template('index.html')


# tableau de bord user avec panier etc.
@app.route('/userdashboard/<user>')
def userdashboard(user):
    # Récupérer les données de l'utilisateur depuis la collection 'users'
    user_data = users_collection.find_one({"users_list.user": {user: {"$exists": True}}})

    if user_data and user_data["users_list"]["user"][user]["panier"]["Vide"] == "False":
        return jsonify(user_data["users_list"]["user"][user]["panier"]["content"])

    return render_template('index.html')

@app.route('/AddCart/<product>')
def AddCart(product):
    if session['type'] == "user":
        # Récupérer l'utilisateur actuel depuis la collection 'users'
        user = users_collection.find_one({"users_list.user": {session['id']: {"$exists": True}}})

        if user:
            # Mettre à jour le panier de l'utilisateur
            if user["users_list"]["user"][session['id']]["panier"]["Vide"] == "True":
                user["users_list"]["user"][session['id']]["panier"]["Vide"] = "False"
                user["users_list"]["user"][session['id']]["panier"]["content"][product] = 1
            else:
                if product in user["users_list"]["user"][session['id']]["panier"]["content"]:
                    user["users_list"]["user"][session['id']]["panier"]["content"][product] += 1
                else:
                    user["users_list"]["user"][session['id']]["panier"]["content"][product] = 1

            # Mettre à jour les données de l'utilisateur dans la collection 'users'
            users_collection.update_one(
                {"users_list.user": {session['id']: {"$exists": True}}},
                {"$set": {"users_list.user." + session['id']: user["users_list"]["user"][session['id']]}}
            )

    return render_template("index.html")


# Page de paiement
@app.route("/payment", methods=["POST"])
def payment():
    amount = 100  # Valeur à adapter en fonction de la logique de paiement
    customer = stripe.Customer.create(
        email=request.form["mail"],
        source=request.form["token"]
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency="usd",
        description ="Shop paiement"
    )
    return redirect(url_for("payment_succes"))


# page de paiement réussi
@app.route("/payment_succes")
def payment_succes():
    render_template("index.html")


# Page d'inscription pour les utilisateurs
@app.route('/register', methods=['GET', 'POST'])
def register():

    # si on envoi des données (formulaire)
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
       # print(password)

        # Créer le nouvel utilisateur
        new_user = {

            id : {
            "id": id,
            "password": password,
            "panier": {
                "Vide": "True",
                "content": {}
            }
            }
        }

        # Insérer le nouvel utilisateur dans la collection 'users'
        # Récupérer les données actuelles dans la collection 'users'
        users_data = users_collection.find_one({})

        # Mettre à jour les données avec le nouvel utilisateur
        users_data["users_list"]["user"].update(new_user)

        # Mettre à jour le document dans la collection 'users' avec les données mises à jour
        users_collection.replace_one({}, users_data)

        # on redirige vers la page de connexion
        return redirect(url_for('login'))

    # on attend que le formulaire soit rempli
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # si le formulaire de connexion est rempli, on récupère les entrées
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']

        user = users_collection.find_one({
            "$or": [
                {"users_list.user." + id + ".password": password},
                {"users_list.admin." + id + ".password": password}
            ]
        })

        if user:
            # si le mot de passe est correct
            session['id'] = id
            session['type'] = 'admin' if user['users_list'].get('admin', {}).get(id) else 'user'

            # Rediriger vers le site web adapté à la personne connectée
            return redirect(url_for('userdashboard', user=id))

        else:
            # Si l'utilisateur n'existe pas ou le mot de passe est incorrect
            print("incorrect")
            return render_template('index.html', error="Email ou mot de passe incorrect")

    # On attend que le formulaire soit rempli
    return render_template('index.html')



# tableau de bord admin avec gestion des users et commandes
@app.route('/admin')
def admin():
    return render_template('index.html')


# tableau de bord user avec panier ect
@app.route('/delete_user/<usertodel>')
def deleteuser(usertodel):
    print("Vous êtes ", session['id'])
    if session['type'] == "admin":
        print("session['type'] == admin")
        if usertodel == "superviseur":
            # ERREUR
            print("On ne peut pas suprimer le superviseur")
        else:
            # ouvre JSON
            with open("users.json", "r") as f:
                # on récupère les users sous forme de dico
                data = json.load(f)

            # Recherche le user à suppr
            if usertodel in data['users_list']["admin"]:
                # Supprimer l'utilisateur
                del data['users_list']["admin"][usertodel]

                # on écrase le fichier user avec les users - le user supprimé
                with open("users.json", "w") as f:
                    f.write("")
                    json.dump(data, f)

            elif usertodel in data['users_list']["user"]:
                # Supprimer l'utilisateur
                del data['users_list']["user"][usertodel]

                # on écrase le fichier user avec les users - le user supprimé
                with open("users.json", "w") as f:
                    f.write("")
                    json.dump(data, f)
    else:
        # ERREUR !!!!
        print("erreur : vous n'êtes pas admin")

    return render_template('index.html')


# Tableau de bord
@app.route('/dashboard')
def dashboard():
    # on verifie que le user est co
    if 'id' in session:
        if 'id' == "admin":
            return redirect(url_for('admin'))
        else :
            return redirect(url_for('userdashboard' , user = id ))
    # sinon on lui dis de se co
    else:
        return redirect(url_for('login'))


# Déconnexion de l'utilisateur
@app.route('/logout')
def logout():
    # si on se déco on détruit la session et retourne à l'acceuil
    session.clear()
    return redirect(url_for('/'))


# lancement de l'appli flask
if __name__ == '__main__':
    app.run(debug=True)
