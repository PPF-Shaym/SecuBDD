import mysql.connector
from Pyfhel import Pyfhel, PyCtxt
import time 

class SrvMiddleware:
    def __init__(self):
        """
        Initialise une instance du middleware serveur.

        Connecte la classe au serveur de base de données MySQL.

        Args:
            None

        Returns:
            None
        """
        self.connection = mysql.connector.connect(host='localhost', port=3306, user='user', password='password')
        self.cursor = self.connection.cursor()

    def populate_bdd(self, data_to_insert_ope_list, data_to_insert_he_list):
        """
        Peuple la base de données avec les données fournies.

        Crée les tables nécessaires si elles n'existent pas et insère les données dans ces tables.

        Args:
            data_to_insert_ope_list (list): Liste de tuples contenant les données chiffrées avec OPE.
            data_to_insert_he_list (list): Liste de tuples contenant les données chiffrées avec chiffrement homomorphique.

        Returns:
            None
        """
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS bdd")
        self.cursor.execute("USE bdd")

        self.cursor.execute("DROP TABLE IF EXISTS salaires_ope")
        self.cursor.execute("DROP TABLE IF EXISTS salaires_he")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS salaires_ope (
            nom varchar(255) UNIQUE,
            salaire_encrypted VARBINARY(255)
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS salaires_he (
            nom varchar(255) UNIQUE,
            salaire_encrypted LONGBLOB 
        )
        """)

        for data_to_insert in data_to_insert_ope_list:
            self.insert_data_ope(data_to_insert)
        for data_to_insert in data_to_insert_he_list:
            self.insert_data_he(data_to_insert)

        print("La base de données et la table ont été créées avec succès.")

    def insert_data_ope(self, data_to_insert):
        """
        Insère des données chiffrées avec OPE dans la base de données.

        Args:
            data_to_insert (tuple): Tuple contenant le nom de l'employé et le salaire chiffré avec OPE.

        Returns:
            None
        """
        self.cursor.execute("INSERT IGNORE INTO salaires_ope (nom, salaire_encrypted) VALUES (%s, %s)",
                       data_to_insert)
        self.connection.commit()
    
    def insert_data_he(self, data_to_insert):
        """
        Insère des données chiffrées avec le chiffrement homomorphique dans la base de données.

        Args:
            data_to_insert (tuple): Tuple contenant le nom de l'employé et le salaire chiffré avec le chiffrement homomorphique.

        Returns:
            None
        """
        self.cursor.execute("INSERT IGNORE INTO salaires_he (nom, salaire_encrypted) VALUES (%s, %s)", data_to_insert)
        self.connection.commit()
        time.sleep(2)

    def get_data(self, range_bound):
        """
        Récupère les données de la base de données dans une plage donnée.

        Args:
            range_bound (tuple): Tuple contenant les bornes de la plage de salaire.

        Returns:
            list: Résultats de la requête SQL.
        """
        self.cursor.execute("SELECT nom, salaire_encrypted FROM salaires_ope WHERE salaire_encrypted BETWEEN %s AND %s",
                       range_bound)
        results = self.cursor.fetchall()
        return results
    
    def get_user_list(self):
        """
        Récupère la liste des utilisateurs de la base de données.

        Returns:
            tuple: Résultats des requêtes SQL pour les tables OPE et chiffrement homomorphique.
        """
        self.cursor.execute("SELECT nom FROM salaires_ope")
        results_ope = self.cursor.fetchall()
        self.cursor.execute("SELECT nom FROM salaires_he")
        results_he = self.cursor.fetchall()
        return results_ope, results_he

    def get_data_greater_than(self, threshold):
        """
        Récupère les données de la base de données où le salaire est supérieur à une valeur donnée.

        Args:
            threshold (int): Valeur seuil pour les salaires.

        Returns:
            list: Résultats de la requête SQL.
        """
        self.cursor.execute("SELECT nom, salaire_encrypted FROM salaires_ope WHERE salaire_encrypted > %s",
                       (threshold,))
        results = self.cursor.fetchall()
        return results
    
    def get_data_lower_than(self, threshold):
        """
        Récupère les données de la base de données où le salaire est inférieur à une valeur donnée.

        Args:
            threshold (int): Valeur seuil pour les salaires.

        Returns:
            list: Résultats de la requête SQL.
        """
        self.cursor.execute("SELECT nom, salaire_encrypted FROM salaires_ope WHERE salaire_encrypted < %s",
                       (threshold,))
        results = self.cursor.fetchall()
        return results

    def get_data_compare(self, nom1, nom2):
        """
        Compare les données de deux employés et récupère le résultat.

        Args:
            nom1 (str): Nom du premier employé.
            nom2 (str): Nom du deuxième employé.

        Returns:
            list: Résultats de la requête SQL.
        """
        self.cursor.execute("""
            SELECT 
                CASE 
                    WHEN salaire_encrypted_1 > salaire_encrypted_2 THEN %s
                    WHEN salaire_encrypted_1 < salaire_encrypted_2 THEN %s
                    ELSE 'Salaries are equal'
                END AS higher_salary_owner
            FROM (
                SELECT 
                    (SELECT salaire_encrypted FROM salaires_ope WHERE nom = %s) AS salaire_encrypted_1,
                    (SELECT salaire_encrypted FROM salaires_ope WHERE nom = %s) AS salaire_encrypted_2
            ) AS salaries_comparison;
        """, (nom1,nom2,nom1,nom2,))
        result = self.cursor.fetchone()
        self.cursor.execute("SELECT nom, salaire_encrypted FROM salaires_ope WHERE nom = %s",
                       result)
        results = self.cursor.fetchall()
        return results

    def get_encrypted_integers_from_db(self, nom1, nom2, hfel):
        """
        Récupère les entiers chiffrés de la base de données pour les employés donnés.

        Args:
            nom1 (str): Nom du premier employé.
            nom2 (str): Nom du deuxième employé.
            hfel (Pyfhel): Instance de Pyfhel utilisée pour déchiffrer les entiers.

        Returns:
            PyCtxt: Résultat de la somme des entiers chiffrés.
        """
        self.cursor.execute("SELECT salaire_encrypted FROM salaires_he WHERE nom=(%s) OR nom=(%s)", (nom1, nom2))
        restult = self.cursor.fetchall()
        encrypted_integer_1 = PyCtxt(pyfhel=hfel, bytestring=bytes(restult[0][0]))
        encrypted_integer_2 = PyCtxt(pyfhel=hfel, bytestring=bytes(restult[1][0]))
        sum_result =  encrypted_integer_1 + encrypted_integer_2   
        return sum_result

    def close_db(self):
        """
        Ferme la connexion à la base de données.

        Returns:
            None
        """
        self.cursor.close()
        self.connection.close()
