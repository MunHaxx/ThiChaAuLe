from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import stripe
from pymongo import MongoClient

# Se connecter à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.commerce_db

# Définir les collections
users_collection = db['users']
stocks_collection = db['stocks']

app = Flask(__name__, static_folder='./build/static', template_folder='./build')
app.secret_key = 'my super secret key'.encode('utf8')

# configuration de l'interface de paiement
stripe.api_key = "secret_key"


# accueil
@app.route('/')
def index():
    return render_template('index.html')


# --------------------------------------- Gestion des users ---------------------------------------

# Créer un nouvel utilisateur
def add_user(id, password, type):
    users_data = users_collection.find_one({})  # Récupérer les données actuelles dans la collection 'users'
    if id not in users_data['users_list'].get('admin', {}) and id not in users_data['users_list'].get('user', {}):
        new_user = {

            id: {
                "id": id,
                "password": password,
                "panier": {
                    "Vide": "True",
                    "content": {}
                }
            }
        }

        if type == "user":
            users_data["users_list"]["user"].update(new_user)  # MAJ la collection avec le nouvel utilisateur
        elif type == "admin":
            users_data["users_list"]["admin"].update(new_user)
        else:
            print("Erreur, le type d'utilisateur n'est pas reconnu")
        users_collection.replace_one({}, users_data)  # MAJ la BDD avec les nouvelles données

    else:
        print("L'utilisateur existe déjà")


# Supprime un utilisateur de la base
@app.route('/delete_user/<usertodel>')
def delete_user(usertodel):
    if session['type'] == "admin" or usertodel == session['id']:

        # Superviseur est un utilisateur intouchable
        if usertodel == "superviseur":
            return render_template('index.html',message="On ne peut pas supprimer le superviseur")

        else:

            users_data = users_collection.find_one({})
            # Vérifie si l'utilisateur à supprimer est un user ou un admin
            if usertodel in users_data['users_list']['admin']:
                del users_data['users_list']['admin'][usertodel]
                users_collection.replace_one({}, users_data) # MAJ de la collection
                return render_template('index.html',message="On a supprimé l'utilisateur"+ usertodel)

            elif usertodel in users_data['users_list']['user']:
                del users_data['users_list']['user'][usertodel]
                users_collection.replace_one({}, users_data)  # MAJ de la collection
                return render_template('index.html',message="On a supprimé l'utilisateur"+ usertodel)

            elif usertodel == session['id']:
                print("Vous suprimez votre propre compte")
                return redirect(url_for('logout'))

            else:
                return render_template('index.html',message="L'utilisateur n'existe pas")

    else:
        # ERREUR !!!!
        return render_template('index.html',message="Vous n'êtes pas administrateur, vous ne pouvez pas supprimer un autre utilisateur")


# Page d'inscription pour les utilisateurs
@app.route('/register', methods=['GET', 'POST'])
def register():
    # si on envoi des données (formulaire)
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        # print(password)

        add_user(id, password, "user")

        # on redirige vers la page de connexion
        return redirect(url_for('login'))

    # Sinon on attend que le formulaire soit rempli
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
            print("L'identifiant ou le mot de passe sont incorrects")
            return render_template('index.html', error="Email ou mot de passe incorrect")

    # On attend que le formulaire soit rempli
    return render_template('index.html')


# Déconnexion de l'utilisateur
@app.route('/logout')
def logout():
    # si on se déco on détruit la session et retourne à l'acceuil
    session.clear()
    #return redirect(url_for('/'))
    return render_template('index.html')


# Passe un utilisateur en administrateur (+ de droits)
@app.route('/user_to_admin/<user>')
def user_to_admin(user):
    if session['type'] == "admin":
        users_data = users_collection.find_one({})

        # Superviseur est un utilisateur intouchable
        if user == "superviseur":
            print("On ne peut pas modifier le superviseur")

        # Déjà admin
        elif user in users_data['users_list']['admin']:
            print(user, " est déjà administrateur")

        # Modif de l'user
        elif user in users_data['users_list']['user']:
            usertemp = users_data['users_list']['user'].get(user, {})
            print(usertemp.get('id'))
            delete_user(user)
            add_user(usertemp.get('id'), usertemp.get('password'), "admin")
            print(user, "est maintenant administrateur")

        # Pas de user
        else:
            print("L'utilisateur n'existe pas")

    else:
        # ERREUR !!!!
        print("Vous n'êtes pas administrateur, vous ne pouvez pas supprimer un autre utilisateur")

    return render_template('index.html')


# Passe un utilisateur en administrateur (+ de droits)
@app.route('/admin_to_user/<user>')
def admin_to_user(user):
    if session['type'] == "admin":
        users_data = users_collection.find_one({})

        # Superviseur est un utilisateur intouchable
        if user == "superviseur":
            print("On ne peut pas modifier le superviseur")

        # Déjà user
        elif user in users_data['users_list']['user']:
            print(user, " est déjà utilisateur")

        # Modif de l'user
        elif user in users_data['users_list']['admin']:
            usertemp = users_data['users_list']['admin'].get(user, {})
            #print(usertemp.get('id'))
            delete_user(user)
            add_user(usertemp.get('id'), usertemp.get('password'), "user")
            print(user, "est maintenant utilisateur")

        # Pas de user
        else:
            print("L'utilisateur n'existe pas")

    else:
        # ERREUR !!!!
        print("Vous n'êtes pas administrateur, vous ne pouvez pas supprimer un autre utilisateur")

    return render_template('index.html')


# --------------------------------------- Tableau de bord ---------------------------------------

# tableau de bord admin avec gestion des users et commandes
@app.route('/admin')
def admin():
    return render_template('index.html')

# tableau de bord user avec panier etc.
@app.route('/userdashboard/<user>')
def userdashboard(user):
    # Récupérer les données de l'utilisateur depuis la collection 'users'
    user_data = users_collection.find_one({"users_list.user": {user: {"$exists": True}}})

    if user_data and user_data["users_list"]["user"][user]["panier"]["Vide"] == "False":
        return jsonify(user_data["users_list"]["user"][user]["panier"]["content"])

    return render_template('index.html')


# Tableau de bord
@app.route('/dashboard')
def dashboard():
    # on verifie que le user est co
    if 'id' in session:
        if 'id' == "admin":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('userdashboard', user=id))
    # sinon on lui dis de se co
    else:
        return redirect(url_for('login'))


# --------------------------------------- Gestion des achats ---------------------------------------

@app.route('/AddCart/<product>')
def AddCart(product):
    print(session['id'])
    print(session['type'])
    if session['type'] == "user":

        # Mettre à jour les données du stock dans la collection 'stocks'
        query = {"stocks." + product: {"$exists": True}}
        stock = stocks_collection.find_one(query)

        print(stock)
        if stock:
            if stock["stocks"][product]["quantity"] > 0:

                # Récupérer l'utilisateur actuel depuis la collection 'users'
                user = users_collection.find_one({"users_list.user." + session['id']: {"$exists": True}})

                print(user)

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
                        {"users_list.user." + session['id']: {"$exists": True}},
                        {"$set": {"users_list.user." + session['id']: user["users_list"]["user"][session['id']]}}
                    )

                    stocks_collection.update_one(
                        {"stocks.{}".format(product): {"$exists": True}},
                        {"$inc": {"stocks.{}.quantity".format(product): -1}}
                    )


            else:
                print("Le produit est en rupture de stock.")
        else:
            print("Le produit n'existe pas dans le stock.")


    return redirect(url_for("index"))



@app.route('/DelCart/<product>')
def DelCart(product):
    if session['type'] == "user":
        # Récupérer l'utilisateur actuel depuis la collection 'users'
        user = users_collection.find_one({"users_list.user." + session['id']: {"$exists": True}})

        if user:
            # Vérifier si le produit est présent dans le panier de l'utilisateur
            if product in user["users_list"]["user"][session['id']]["panier"]["content"]:
                # Réduire la quantité du produit dans le panier de l'utilisateur
                user["users_list"]["user"][session['id']]["panier"]["content"][product] -= 1

                # Si la quantité atteint 0, supprimer le produit du panier
                if user["users_list"]["user"][session['id']]["panier"]["content"][product] == 0:
                    del user["users_list"]["user"][session['id']]["panier"]["content"][product]

                # Mettre à jour les données de l'utilisateur dans la collection 'users'
                users_collection.update_one(
                    {"users_list.user." + session['id']: {"$exists": True}},
                    {"$set": {"users_list.user." + session['id']: user["users_list"]["user"][session['id']]}}
                )

                # Mettre à jour les données de stock dans la collection 'stocks'
                stocks_collection.update_one(
                    {"stocks.{}".format(product): {"$exists": True}},
                    {"$inc": {"stocks.{}.quantity".format(product): 1}}
                )

            else:
                print("Le produit n'est pas présent dans le panier de l'utilisateur.")
        else:
            print("Utilisateur non trouvé.")

    return redirect(url_for("index"))




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
        description="Shop paiement"
    )
    return redirect(url_for("payment_succes"))


# page de paiement réussi
@app.route("/payment_succes")
def payment_succes():
    render_template("index.html")


# --------------------------------------- Programme principal ---------------------------------------

# lancement de l'appli flask
if __name__ == '__main__':
    app.run(debug=True)