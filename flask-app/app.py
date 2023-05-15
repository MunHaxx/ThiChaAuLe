from flask import Flask, jsonify, render_template,request,redirect,url_for,session
import json
import paypalrestsdk
import bcrypt
import stripe

# ça manque de front par ici


app = Flask(__name__, static_folder='./build/static', template_folder='./build')
app.secret_key  = 'my super secret key'.encode('utf8')

# configuration de l'interface de paiement
stripe.api_key = "secret_key"


# acceuil
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
        # on récupére les users sous forme de dico
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
        print(password)

        # on ajoute le nouvelle user au fichier json des users
        user = {
            id: {
                "id": id,
                "password": password ,
                "panier": { "Vide": "True"
                }
            }
        }

        # on récupére l'ancien json pour le mettre à jour
        with open("users.json", "r") as f:
            # on récupére les users sous forme de dico
            data = json.load(f)
            # on rajoute le new user au dico
            data["users"].update(user)

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

        # on récupére le json des users
        with open("users.json", "r") as f:
            # on récupére les users sous forme de dico
            data = json.load(f)

        # pour chacun de mes user
        for user in data["users"].keys():
            # si c'est le user qui se connecte
            if user == id:
                # si le mdp est correct
                if data["users"][user]['password'] == password:
                    # je crée la session associé au id (admin ou users)
                    session['id'] = id
                    # je redirige vers le site web adapté à la personne connecter (admin ou users)
                    return redirect(url_for('dashboard'))
        # si aucun user ne correspond on renvoi à la connexion et on indique que c'est incorrect
        return render_template('index.html', error="Email ou mot de passe incorrect")

    # on attend que le formulaire sois remplis
    return render_template('index.html')

# tableau de bord admin avec gestion des users et commandes
@app.route('/admin')
def admin():
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
