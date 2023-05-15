from flask import Flask, jsonify, render_template,request,redirect,url_for,session
import json
import paypalrestsdk
import bcrypt
import stripe

# ça manque de front par ici


app = Flask(__name__, static_folder='./build/static', template_folder='./build')
app.secret_key = 'my super secret key'.encode('utf8')

# configuration de l'interface de paiement
stripe.api_key = "secret_key"


# accueil
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    with open("stock.json", "r") as f:
            # on récupére les users sous forme de dico
            data = json.load(f)
    return jsonify(data)

# @app.route('/api/data')
# def get_data():
#     with open("stock.json", "r") as f:
#         data = json.load(f)

#     return jsonify(data)

# tableau de bord user avec panier ect
@app.route('/user/user=<user>')
def userdashboard(user):

    with open("users.json", "r") as f:
        # on récupère les users sous forme de dico
        data = json.load(f)

    if data["users"][user]["panier"]["Vide"] == "False":
        return data["users"][user]["panier"]


# page de paiement
@app.route("/payment", methods=["POST"])
def payment(amount):
    customer = stripe.Customer.create(
        email = request.form["mail"],
        source=request.form["token"]
    )
    charge = stripe.Charge.create(
        customer= customer.id,
        amount=amount,
        currency="usd",
        description=" Shop paiement "
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

        # on ajoute le nouvel user au fichier json des users
        user = {
            id: {
                "id": id,
                "password": password ,
                "panier": { "Vide": "True"
                }
            }
        }

        # on récupère l'ancien json pour le mettre à jour
        with open("users.json", "r") as f:
            # on récupère les users sous forme de dico
            data = json.load(f)
            # on rajoute le new user au dico
            data["users_list"]["user"].update(user)

            # on écrase le fichier user avec les users + le new user
            with open("users.json", "w") as f:
                f.write("")
                json.dump(data, f)


        # on redirige vers la page de connection
        return redirect(url_for('login'))

    # on attend que le formulaire sois rempli
    return render_template('index.html')


# Page de connexion pour les utilisateurs
@app.route('/login', methods=['GET', 'POST'])
def login():
    # si rempli le formulaire de connexion on récup des entrées
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']

        # on récupère le json des users
        with open("users.json", "r") as f:
            # on récupère les users sous forme de dico
            data = json.load(f)

        # pour chacun de mes user
        if id in data["users_list"]["user"]:
            # si c'est le user qui se connecte
            user = id
            # si le mdp est correct
            if data["users_list"]["user"][user]['password'] == password:
                # je crée la session associé au id (admin ou users)
                session['id'] = id
                session['type'] = "user"

                # je redirige vers le site web adapté à la personne connecter (user)
                return redirect(url_for('dashboard'))

        elif id in data["users_list"]["admin"]:
            user = id
            # si admin
            if data["users_list"]["admin"][user]['password'] == password:
                # je crée la session associé au id (admin ou users)

                session['id'] = id
                session['type'] = "admin"
                # je redirige vers le site web adapté à la personne connecter (admin)
                print("Vous êtes connecté en tant que ", session['id'])
                return redirect(url_for('dashboard'))

        else:
            # ERREUR

            # si aucun user ne correspond on renvoi à la connexion et on indique que c'est incorrect
            return render_template('index.html', error="Email ou mot de passe incorrect")

    # on attend que le formulaire sois remplis
    return render_template('index.html')


# Déconnexion de l'utilisateur
@app.route('/logout')
def logout():
    # si on se déco on détruit la session et retourne à l'acceuil
    session.clear()
    return redirect(url_for('/'))


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
        if session['type'] == "admin":
            return redirect(url_for('admin'))
        else :
            return redirect(url_for('userdashboard' , user = id ))
    # sinon on lui dis de se co
    else:
        return redirect(url_for('login'))


# tableau de bord user avec panier ect
@app.route('/userdashboard/<user>')
def userdashboard(user):

    with open("users.json", "r") as f:
        # on récupère les users sous forme de dico
        data = json.load(f)

    #if data["users_list"][user]["panier"]["Vide"] == "False":
     #   return data["users"][user]["panier"]

    return render_template('index.html')


# lancement de l'appli flask
if __name__ == '__main__':
    app.run(debug=True)
