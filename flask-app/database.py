from pymongo import MongoClient

# Se connecter à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.commerce_db

# Définir la collection 'stocks'
stocks_collection = db['stocks']

# Définir la collection 'users'
users_collection = db['users']

# Données initiales
users_data = {
    "users_list": {
        "admin": {
            "superviseur": {
                "id": "superviseur",
                "password": "123",
                "panier": {
                    "Vide": "True",
                    "content": {}
                }
            }
        },
        "user": {
            "a": {
                "id": "a",
                "password": "a",
                "panier": {
                    "Vide": "True",
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
