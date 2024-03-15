import mysql.connector

# Établir la connexion à MySQL
connection = mysql.connector.connect(host='localhost', port=3306, user='user', password='password')

def create_table():
    # Créer la base de données si elle n'existe pas
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bdd")
    cursor.execute("USE bdd")

    # Créer la table salaires
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salaires (
            nom varchar(255) UNIQUE,
            salaire_encrypted VARBINARY(255)
        )
    """)

    # Fermer les connexions
    cursor.close()



create_table()
print("La base de données et la table ont été créées avec succès.")
connection.close()


