import time

from flask import Flask, jsonify, render_template, request, redirect, url_for, session, render_template_string
import json
import stripe
import random
from pymongo import MongoClient
import os 
from datetime import date

# Se connecter à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.commerce_db

# Définir les collections
users_collection = db['users']
stocks_collection = db['stocks']
cmd_collection = db['commandes']

app = Flask(__name__, static_folder='./build/static', template_folder='./build')
app.debug = True

# Obtient le chemin absolu du répertoire de l'application Flask
#app_dir = os.path.dirname(os.path.abspath(__file__))

# Spécifie les répertoires statiques et les modèles
#static_folder = os.path.join(app_dir, 'build/static')
#template_folder = os.path.join(app_dir, 'build')

# Configure l'application Flask avec les répertoires appropriés
#app.static_folder = static_folder
#app.template_folder = template_folder

app.secret_key = 'my super secret key'.encode('utf8')

# configuration de l'interface de paiement
stripe.api_key = "secret_key"


# accueil
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json')


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
                    "Total": "0",
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
            return render_template('index.html', message="On ne peut pas supprimer le superviseur")

        else:
            users_data = users_collection.find_one({})

            # Vérifie si l'utilisateur à supprimer est un user ou un admin
            if users_data and usertodel in users_data['users_list']['admin']:
                # Supprime l'admin
                del users_data['users_list']['admin'][usertodel]
                users_collection.replace_one({}, users_data)  # MAJ de la collection
                # Si on supprime son propre compte, on se déconnecte
                if usertodel == session['id']:
                    print("Vous supprimez votre compte")
                    return redirect(url_for('logout'))
                return render_template('index.html', message="On a supprimé l'utilisateur" + usertodel)

            elif users_data and usertodel in users_data['users_list']['user']:
                # Supprime les commandes associées à l'utilisateur
                Lcmd = list_cmd_user(usertodel).get_json()  # convertit fichier JSON en dictionnaire python
                if Lcmd:
                    for num in Lcmd:
                        suppr_cmd(num)
                # Supprime l'utilisateur
                del users_data['users_list']['user'][usertodel]
                users_collection.replace_one({}, users_data)  # MAJ de la collection
                # Si on supprime son propre compte, on se déconnecte
                if usertodel == session['id']:
                    print("Vous supprimez votre compte")
                    return redirect(url_for('logout'))
                return redirect("/dashboard")

            else:
                return redirect("/dashboard")

    else:
        # ERREUR !!!!
        return redirect("/dashboard")

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


@app.route('/list_users')
def list_users():
    if session['type'] == "admin":
        users_data = users_collection.find_one({})
        if users_data:
            return jsonify(users_data["users_list"])
        else:
            print("Erreur, il n'y a pas d'utilisateurs dans la base")
    else:
        print("Erreur, vous n'êtes pas administrateur")

    return jsonify({})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "<SecureCookieSession" in session:
        return redirect("/dashboard")
    # si le formulaire de connexion est rempli, on récupère les entrées
    elif request.method == 'POST':
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
            return redirect(url_for('dashboard'))

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
    # return redirect(url_for('/'))
    return render_template('index.html')


# --------------------------------------- Gestion des droits ---------------------------------------

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
            delete_user(user)
            add_user(usertemp.get('id'), usertemp.get('password'), "admin")
            print(user, "est maintenant administrateur")

        # Pas de user
        else:
            print("L'utilisateur n'existe pas")

    else:
        # ERREUR !!!!
        print("Vous n'êtes pas administrateur, vous ne pouvez pas supprimer un autre utilisateur")

    return redirect("/dashboard")


# Passe un administrateur en utilisateur (- de droits)
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
            # print(usertemp.get('id'))
            delete_user(user)
            add_user(usertemp.get('id'), usertemp.get('password'), "user")
            print(user, "est maintenant utilisateur")

        # Pas de user
        else:
            print("L'utilisateur n'existe pas")

    else:
        # ERREUR !!!!
        print("Vous n'êtes pas administrateur, vous ne pouvez pas supprimer un autre utilisateur")

    return redirect("/dashboard")


# --------------------------------------- Tableau de bord ---------------------------------------

# tableau de bord admin avec gestion des users et commandes
@app.route('/admindashboard')
def admindashboard():
    return render_template('index.html')


# tableau de bord user avec panier etc.
@app.route('/userdashboard')
def userdashboard():
    # Récupérer les données de l'utilisateur depuis la collection 'users'
    user_data = users_collection.find_one({"users_list.user": {session['id']: {"$exists": True}}})

    if user_data and user_data["users_list"]["user"][session['id']]["panier"]["Vide"] == "False":
        return jsonify(user_data["users_list"]["user"][session['id']]["panier"]["content"])

    return render_template('index.html')


# Tableau de bord
@app.route('/dashboard')
def dashboard():
    print(session['type'])
    # on verifie que le user est co
    if 'type' in session:
        if session['type'] == "admin":
            return redirect(url_for('admindashboard'))
        else:
            return redirect(url_for('userdashboard'))
    # sinon on lui dis de se co
    else:
        return redirect(url_for('login'))


# --------------------------------------- Gestion des achats ---------------------------------------


# Page pour mettre à jour le total du panier
def UpdateTotalCart(user,stock):
    # Calcul du total du panier
    total = 0
    for item in user["users_list"]["user"][session['id']]["panier"]["content"]:
        quantity = user["users_list"]["user"][session['id']]["panier"]["content"][item]
        #print(stock)
        price = stock['stocks'][item]['tarifs']
        total += quantity * price

    #print("Total du panier:", total)
    return total


@app.route('/boxs')
def boxs():
    return render_template("index.html")

@app.route('/panier')
def panier():
    return render_template("index.html")


def addcart(product):
    if session['type'] == "user":
        # Mettre à jour les données du stock dans la collection 'stocks'
        query = {"stocks." + product: {"$exists": True}}
        stock = stocks_collection.find_one(query)

        if stock:
            if stock["stocks"][product]["quantity"] > 0:
                # Récupérer l'utilisateur actuel depuis la collection 'users'
                user = users_collection.find_one({"users_list.user." + session['id']: {"$exists": True}})

                # print(user)

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

                    total = UpdateTotalCart(user, stock)

                    # Mettre à jour le champ "Total" du panier de l'utilisateur
                    user["users_list"]["user"][session['id']]["panier"]["Total"] = str(total)

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


@app.route('/AddCart/<product>', methods=['GET', 'POST'])
def AddCart(product):
    addcart(product)
    return redirect("/boxs")


@app.route('/Cart/AddCart/<product>', methods=['GET', 'POST'])
def CartAddCart(product):
    addcart(product)
    return redirect("/panier")


@app.route('/DelCart/<product>')
def DelCart(product):
    if session['type'] == "user":
        # Récupérer l'utilisateur actuel depuis la collection 'users'
        user = users_collection.find_one({"users_list.user." + session['id']: {"$exists": True}})
        query = {"stocks." + product: {"$exists": True}}
        stock = stocks_collection.find_one(query)

        if user:
            # Vérifier si le produit est présent dans le panier de l'utilisateur
            if product in user["users_list"]["user"][session['id']]["panier"]["content"]:
                # Réduire la quantité du produit dans le panier de l'utilisateur
                user["users_list"]["user"][session['id']]["panier"]["content"][product] -= 1

                # Si la quantité atteint 0, supprimer le produit du panier
                if user["users_list"]["user"][session['id']]["panier"]["content"][product] == 0:
                    del user["users_list"]["user"][session['id']]["panier"]["content"][product]

                total = UpdateTotalCart(user, stock)

                # Mettre à jour le champ "Total" du panier de l'utilisateur
                user["users_list"]["user"][session['id']]["panier"]["Total"] = str(total)

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

    return redirect("/panier")


@app.route('/list_panier')
def list_panier():
    if session['type'] == 'user':
        users_data = users_collection.find_one({})
        if users_data:
            #print(users_data["users_list"]['user'][session['id']]['panier'])
            return jsonify(users_data["users_list"]['user'][session['id']]['panier'])
        else:
            print("Erreur, il n'y a pas d'utilisateurs dans la base")
    else:
        print("Vous êtes un admin, vous n'avez pas de panier")
    return jsonify({})


# --------------------------------------- Paiement ---------------------------------------

# Page de paiement
@app.route("/payment", methods=["POST"])
def payment():
    if request.method == 'POST':
        return redirect(url_for("paymentsuccess"))


# page de paiement réussi
@app.route("/paymentsuccess")
def payment_succes():
    print("cc")
    create_cmd()
    return render_template("index.html", message="paiement succesfull")


# --------------------------------------- Récupéré statistique ---------------------------------------

def calculate_statistics():
    # Récupérer les données de tous les utilisateurs depuis la collection 'users'
    users_data = users_collection.find_one({})

    # Initialiser un dictionnaire pour stocker les statistiques
    statistics = {
        "total_sales": 0,
        "bestsellers": {}
    }

    # Parcourir tous les utilisateurs et leurs paniers
    for user_type in ["admin", "user"]:
        users = users_data["users_list"].get(user_type, {})
        for user_id, user_info in users.items():
            panier = user_info.get("panier", {}).get("content", {})

            # Mettre à jour les statistiques pour chaque produit dans le panier
            for product, quantity in panier.items():
                statistics["total_sales"] += quantity
                if product in statistics["bestsellers"]:
                    statistics["bestsellers"][product] += quantity
                else:
                    statistics["bestsellers"][product] = quantity

    # Trier les bestsellers par quantité vendue (du plus élevé au plus bas)
    bestsellers = sorted(statistics["bestsellers"].items(), key=lambda x: x[1], reverse=True)
    statistics["bestsellers"] = bestsellers

    return statistics


@app.route('/Getstatistics')
def statistics():
    stats = calculate_statistics()
    return render_template('index.html', statistics=stats)


@app.route('/api/data', methods=['GET', 'POST'])
def get_data():
    stocks = stocks_collection.find_one()
    # on récupére les users sous forme de dico
    # print("hello")

    response = jsonify(stocks['stocks'])
    #response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# --------------------------------------- Gestion des commandes ---------------------------------------

def pass_data(data):
    return jsonify(data)


# Après le paiement, on crée une commande
@app.route("/create_cmd")
def create_cmd():
    print("hehe")
    user = session['id']
    # Récupérer les données du panier de l'utilisateur
    users_data = users_collection.find_one({})
    panier = users_data['users_list'].get('user', {}).get(user).get('panier')
    # Récupérer l'indice de la nouvelle commande
    cmd_data = cmd_collection.find_one({})
    #print(cmd_data)
    #if not cmd_data:
    #    num = 0
    #else:
    #    num = str(max(int(key) for key in cmd_data['commandes'].keys()) + 1)
    num = random.randint(2, 200)

    if cmd_data and users_data:
        if panier['Vide'] == 'True':
            print("Erreur, on ne peut pas créer de commande à partir d'un panier vide")
        else:
            # On crée une nouvelle commande
            print("hihi")
            new_cmd = {
                num: {
                    "client": user,
                    "date": date.today().strftime("%d/%m/%Y"),
                    "status": "En cours",
                    "prix": panier['Total'],
                    "contenu": panier['content']
                }
            }
            cmd_data['commandes'].update(new_cmd)
            cmd_collection.replace_one({}, cmd_data)  # MAJ la BDD avec les nouvelles données

            # On vide le panier de l'utilisateur
            panier['Vide'] = 'True'
            panier['content'] = {}
            users_collection.replace_one({}, users_data)  # MAJ la BDD avec les nouvelles données

    # Rediriger vers le site web adapté à la personne connectée
    return redirect(url_for('userdashboard'))


# Supprimer une commande
@app.route("/suppr_cmd/<num>")
def suppr_cmd(num):
    cmd_data = cmd_collection.find_one({})
    if cmd_data:
        if num in cmd_data["commandes"]:
            # Supprimer la commande
            del cmd_data["commandes"][num]
            cmd_collection.replace_one({}, cmd_data)
            print("La commande n°", num, " a bien été supprimée")
        else:
            print("La commande n°", num, " n'existe pas")
    return redirect("/dashboard")


# Récupère la liste des commandes d'un user
@app.route("/list_cmd_user/<user>")
def list_cmd_user(user):
    # Récupère les données de la base
    users_data = users_collection.find_one({})
    cmd_data = cmd_collection.find_one({})

    # Vérifie si l'utilisateur existe
    if users_data and user in users_data['users_list'].get('user', {}):
        if cmd_data:
            listCmd = {}
            # Parcourt toutes les commandes
            for num, cmd in cmd_data["commandes"].items():
                if cmd['client'] == user:
                    # Construit un json avec les commandes de l'utilisateur
                    listCmd[num] = cmd
            if listCmd == {}:
                print("L'utilisateur n'a pas encore réalisé de commandes")
            else:
                return jsonify(listCmd)  # Retourne le fichier json
    else:
        print("L'utilisateur n'existe pas")

    pass_data("{}")  # Retourne le fichier json
    return redirect("/dashboard")


@app.route("/list_cmd_user_term")
def list_cmd_user_term():
    user = session['id']
    if user:
        Lcmd = list_cmd_user(user).get_json()
        result = {}
        if Lcmd:
            for num, cmd in Lcmd.items():
                if cmd['client'] == user and cmd['status'] == "Terminé":
                    result[num] = cmd
            return jsonify(result)
        else:
            print("Erreur lors de la récup des commandes de l'utilisateur")
    else:
        print("Erreur, l'utilisateur n'existe pas")
    return jsonify("{}")

@app.route("/list_cmd_user_encours")
def list_cmd_user_encours():
    user = session['id']
    if user:
        Lcmd = list_cmd_user(user).get_json()
        result = {}
        if Lcmd:
            for num, cmd in Lcmd.items():
                if cmd['client'] == user and cmd['status'] == "En cours":
                    result[num] = cmd
            return jsonify(result)
        else:
            print("Erreur lors de la récup des commandes de l'utilisateur")
    else:
        print("Erreur, l'utilisateur n'existe pas")
    return jsonify("{}")


# Récupère la liste des commandes à préparer pour le dashboard ADMIN
@app.route("/list_cmd_encours")
def list_cmd_encours():
    if session['type'] == "admin":
        cmd_data = cmd_collection.find_one({})
        if cmd_data:
            listCmd = {}
            # Parcourt toutes les commandes
            for num, cmd in cmd_data["commandes"].items():
                # Construit un json avec les commandes en cours
                if cmd['status'] == 'En cours':
                    listCmd[num] = cmd
            if listCmd == {}:
                print("Il n'y a aucune commande à préparer")
            else:
                return jsonify(listCmd)  # Retourne le fichier json

    else:
        print("Erreur, vous n'êtes pas admin, vous ne pouvez pas accéder aux status des commandes")

    return jsonify("{}")


# Récupère la liste des commandes terminé pour le dashboard ADMIN
@app.route("/list_cmd_term")
def list_cmd_term():
    if session['type'] == "admin":
        cmd_data = cmd_collection.find_one({})
        if cmd_data:
            listCmd = {}
            # Parcourt toutes les commandes
            for num, cmd in cmd_data["commandes"].items():
                # Construit un json avec les commandes en cours
                if cmd['status'] == 'Terminé':
                    listCmd[num] = cmd
            if listCmd == {}:
                print("Il n'y a aucune commande terminée")
            else:
                return jsonify(listCmd)  # Retourne le fichier json

    else:
        print("Erreur, vous n'êtes pas admin, vous ne pouvez pas accéder aux status des commandes")

    return jsonify("{}")


# Modifie le status d'une commande pour la mettre en Terminé
@app.route("/terminer_cmd/<num>")
def terminer_cmd(num):
    if session['type'] == "admin":
        cmd_data = cmd_collection.find_one({})
        if cmd_data and num in cmd_data['commandes']:
            cmd = cmd_data['commandes'][num]
            cmd['status'] = 'Terminé'
            cmd_data['commandes'].update({num: cmd})
            cmd_collection.replace_one({}, cmd_data)  # MAJ la BDD avec les nouvelles données
        else:
            print("La commande n°", num, " n'existe pas")
    else:
        print("Erreur, vous n'êtes pas admin, vous ne pouvez pas modifier le status des commandes")
    return redirect("/dashboard")


# Modifie le status d'une commande pour la mettre en En cours
@app.route("/encours_cmd/<num>")
def encours_cmd(num):
    if session['type'] == "admin":
        cmd_data = cmd_collection.find_one({})
        if cmd_data and num in cmd_data['commandes']:
            cmd = cmd_data['commandes'][num]
            cmd['status'] = 'En cours'
            cmd_data['commandes'].update({num: cmd})
            cmd_collection.replace_one({}, cmd_data)  # MAJ la BDD avec les nouvelles données
        else:
            print("La commande n°", num, " n'existe pas")
    else:
        print("Erreur, vous n'êtes pas admin, vous ne pouvez pas modifier le status des commandes")
    return redirect("/dashboard")


# --------------------------------------- Programme principal ---------------------------------------

# lancement de l'appli flask
if __name__ == '__main__':
    app.run(debug=True)
