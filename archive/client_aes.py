import mysql.connector
from middleware_aes import OREMiddleware

# Connexion à la base de données
connection = mysql.connector.connect(host='localhost', port=3306, user='user', password='password')

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS bdd")
cursor.execute("USE bdd")
key = b'MySecretKey12345'
middleware = OREMiddleware(key)

# Exemple d'insertion de données
username = ["John Doe", "Jane Doe", "Martin Dos", "Edouard Lie", "Bernard Boe", "Boudeer Pale"]
salaire_month = [1000, 2000, 3000, 4000, 5000, 6000]
for i in range(len(username)):
    print(username[i], salaire_month[i])
    middleware.insert_data(cursor, username[i], salaire_month[i])

connection.commit()

# Exemple de récupération de données dans un intervalle
lower_bound = 6000
upper_bound = 8000
decrypted_results = middleware.get_data(cursor, lower_bound, upper_bound)

# Affichage des résultats
for nom_salarie, salaire in decrypted_results:
    print(f"Nom: {nom_salarie}, Salaire: {salaire}")

# Fermeture de la connexion
cursor.close()
connection.close()
