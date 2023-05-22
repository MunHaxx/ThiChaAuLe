from pymongo import MongoClient

# Se connecter à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.commerce_db

# Définir les collections
stocks_collection = db['stocks']
users_collection = db['users']
commandes_collection = db['commandes']

# Données initiales
users_data = {
    "users_list": {
        "admin": {
            "superviseur": {
                "id": "superviseur",
                "password": "123"
            }
        },
        "user": {
            "Jean Pierre": {
                "id": "Jean Pierre",
                "password": "jp",
                "panier": {
                    "Vide": "True",
                    "Total": "0",
                    "content": {}
                }
            },
            "Anne Marie": {
                "id": "Anne Marie",
                "password": "am",
                "panier": {
                    "Vide": "True",
                    "Total": "0",
                    "content": {}
                }
            }
        }
    }
}

# Insérer les données initiales dans la collection 'users'
users_collection.insert_one(users_data)

# Données des stocks
stocks_data = {
    "stocks": {
        "BoxBoulang": {
            "name": "La box Boulangerie",
            "quantity": 6,
            "tarifs": 20,
            "promotion": 0
        },
        "BoxDecouverte": {
            "name": "La box Decouverte",
            "quantity": 30,
            "tarifs": 30,
            "promotion": 0
        },
        "BoxVinFrom": {
            "name": "La box Vin & Fromage",
            "quantity": 20,
            "tarifs": 39,
            "promotion": 10
        }
    }
}

# Insérer les données des stocks dans la collection 'stocks'
stocks_collection.insert_one(stocks_data)


# Données des stocks
cmd_data = {
    "commandes": {
        "1": {
            "client": "Jean Pierre",
            "date": "18/05/2023",
            "status": "Terminé",
            "prix": 20,
            "contenu": {
                "BoxBoulang": 1,
                "BoxDecouverte": 0,
                "BoxVinFrom": 0
            }
        },
        "2": {
            "client": "Anne Marie",
            "date": "22/05/2023",
            "status": "En cours",
            "prix": 69,
            "contenu": {
                "BoxBoulang": 0,
                "BoxDecouverte": 1,
                "BoxVinFrom": 1
            }
        },
        "3": {
            "client": "Jean Pierre",
            "date": "23/05/2023",
            "status": "En cours",
            "prix": 20,
            "contenu": {
                "BoxBoulang": 1,
                "BoxDecouverte": 0,
                "BoxVinFrom": 0
            }
        }
    }
}

# Insérer les données des stocks dans la collection 'stocks'
commandes_collection.insert_one(cmd_data)
