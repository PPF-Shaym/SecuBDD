from pyope.ope import OPE
from server_middleware import SrvMiddleware
from Pyfhel import Pyfhel 
import numpy as np

class ClientMiddleware:
    def __init__(self, key):
        """
        Initialise une instance du middleware client.

        Args:
            key (bytes): Clé utilisée pour l'initialisation du chiffrement OPE.

        Returns:
            None
        """
        self.ope = OPE(key)
        self.SrvMiddleware = SrvMiddleware()
        # Paire de clés pour le chiffrement homomorphique
        self.fhel = Pyfhel()
        self.fhel.contextGen(scheme='bfv', n=4096, t_bits=20, sec=128)
        self.fhel.keyGen()

    def chiffre_salaire_ope(self, salaire):
        """
        Chiffre le salaire en utilisant le chiffrement OPE.

        Args:
            salaire (int): Salaire à chiffrer.

        Returns:
            bytes: Salaire chiffré.
        """
        return self.ope.encrypt(salaire)
    
    def dechiffre_salaire_ope(self, salaire_chiffre):
        """
        Déchiffre le salaire chiffré en utilisant le chiffrement OPE.

        Args:
            salaire_chiffre (bytes): Salaire chiffré.

        Returns:
            int: Salaire déchiffré.
        """
        return self.ope.decrypt(salaire_chiffre)
    
    def chiffre_salaire_he(self, plaintext_salary):
        """
        Chiffre le salaire en utilisant le chiffrement homomorphique.

        Args:
            plaintext_salary (int): Salaire à chiffrer.

        Returns:
            bytes: Salaire chiffré.
        """
        encode_int = np.array([plaintext_salary], dtype=np.int64)
        int_ctx = self.fhel.encryptInt(encode_int)
        encrypted_salary = int_ctx.to_bytes()
        return encrypted_salary

    def dechiffre_salaire_he(self, encrypted_int):
        """
        Déchiffre le salaire chiffré en utilisant le chiffrement homomorphique.

        Args:
            encrypted_int (bytes): Salaire chiffré.

        Returns:
            int: Salaire déchiffré.
        """
        decrypted_int = self.fhel.decryptInt(encrypted_int)
        return decrypted_int
    
    def populate_bdd(self, username_dict):
        """
        Remplit la base de données avec les données chiffrées.

        Args:
            username_dict (dict): Dictionnaire contenant les noms d'utilisateur et les salaires.

        Returns:
            None
        """
        data_to_insert_ope_list = [] 
        data_to_insert_he_list = []

        for username, salaire in username_dict.items():
            salaire_chiffre_ope = self.chiffre_salaire_ope(salaire)
            data_to_insert_ope_list.append((username, salaire_chiffre_ope))
            salaire_chiffre_he = self.chiffre_salaire_he(salaire)
            data_to_insert_he_list.append((username, salaire_chiffre_he))
        self.SrvMiddleware.populate_bdd(data_to_insert_ope_list, data_to_insert_he_list)
    
    def add_member(self, username_dict):
        """
        Ajoute un utilisateur à la base de données.

        Args:
            username_dict (dict): Dictionnaire contenant le nom d'utilisateur et le salaire.

        Returns:
            None
        """
        for username, salaire in username_dict.items():
            salaire_chiffre_ope = self.chiffre_salaire_ope(salaire)
            salaire_chiffre_he = self.chiffre_salaire_he(salaire)
            self.SrvMiddleware.insert_data_ope((username,salaire_chiffre_ope))
            self.SrvMiddleware.insert_data_he((username,salaire_chiffre_ope))
            print(f"Add {username}, {salaire}")
    
    def get_user_list(self):
        """
        Récupère la liste des utilisateurs de la base de données.

        Returns:
            tuple: Résultats chiffrés avec OPE, résultats chiffrés avec chiffrement homomorphique.
        """
        results_ope, results_he = self.SrvMiddleware.get_user_list()
        return results_ope, results_he

    def ajout_data(self, nom_salarie, salaire):
        """
        Ajoute des données chiffrées à la base de données.

        Args:
            nom_salarie (str): Nom de l'employé.
            salaire (int): Salaire de l'employé.

        Returns:
            None
        """
        salaire_chiffre = self.chiffre_salaire_ope(salaire)
        data_to_insert = (nom_salarie, salaire_chiffre)
        self.SrvMiddleware.insert_data(data_to_insert)
    
    def range_compare(self, lower_bound, upper_bound):
        """
        Compare les salaires dans une plage donnée.

        Args:
            lower_bound (int): Limite inférieure de la plage de salaire.
            upper_bound (int): Limite supérieure de la plage de salaire.

        Returns:
            list: Résultats déchiffrés.
        """
        decrypted_results = []
        lower_bound_enc = self.chiffre_salaire_ope(lower_bound)
        upper_bound_enc = self.chiffre_salaire_ope(upper_bound)
        results = self.SrvMiddleware.get_data((lower_bound_enc, upper_bound_enc))
        for row in results:
            salaire_denc = int(self.dechiffre_salaire_ope(int(row[1])))
            decrypted_results.append((row[0], salaire_denc))

        return decrypted_results

    def get_data_greater_than(self, salaire):
        """
        Récupère les données des employés dont le salaire est supérieur à une valeur donnée.

        Args:
            salaire (int): Valeur de salaire supérieure.

        Returns:
            list: Résultats déchiffrés.
        """
        salaire_chiffre = self.chiffre_salaire_ope(salaire)
        results = self.SrvMiddleware.get_data_greater_than(salaire_chiffre)
        decrypted_results = []
        for row in results:
            salaire_denc = int(self.dechiffre_salaire_ope(int(row[1])))
            decrypted_results.append((row[0], salaire_denc))
        return decrypted_results
    
    def get_data_lower_than(self, salaire):
        """
        Récupère les données des employés dont le salaire est inférieur à une valeur donnée.

        Args:
            salaire (int): Valeur de salaire inférieure.

        Returns:
            list: Résultats déchiffrés.
        """
        salaire_chiffre = self.chiffre_salaire_ope(salaire)
        results = self.SrvMiddleware.get_data_lower_than(salaire_chiffre)
        decrypted_results = []
        for row in results:
            salaire_denc = int(self.dechiffre_salaire_ope(int(row[1])))
            decrypted_results.append((row[0], salaire_denc))
        return decrypted_results
    
    def get_data_compare(self, nom1, nom2):
        """
        Compare les données de deux employés.

        Args:
            nom1 (str): Nom du premier employé.
            nom2 (str): Nom du deuxième employé.

        Returns:
            list: Résultats déchiffrés.
        """
        results = self.SrvMiddleware.get_data_compare(nom1, nom2)
        decrypted_results = []
        for row in results:
            salaire_denc = int(self.dechiffre_salaire_ope(int(row[1])))
            decrypted_results.append((row[0], salaire_denc))
        return decrypted_results

    def ajout_data_phe(self, nom_salarie, salaire):
        """
        Ajoute des données chiffrées à la base de données avec le chiffrement homomorphique.

        Args:
            nom_salarie (str): Nom de l'employé.
            salaire (int): Salaire de l'employé.

        Returns:
            None
        """
        salaire_chiffre = self.chiffre_salaire_he(salaire)
        data_to_insert = (nom_salarie, salaire_chiffre)
        self.SrvMiddleware.inserer_entier_chiffre(data_to_insert)

    def addition_data(self, nom1, nom2):
        """
        Ajoute les salaires de deux employés.

        Args:
            nom1 (str): Nom du premier employé.
            nom2 (str): Nom du deuxième employé.

        Returns:
            int: Somme des salaires.
        """
        result = self.SrvMiddleware.get_encrypted_integers_from_db(nom1, nom2, self.fhel)
        clear_salaire = self.dechiffre_salaire_he(result)
        return clear_salaire[0]

    def close_db(self):
        """
        Ferme la connexion à la base de données.

        Returns:
            None
        """
        self.SrvMiddleware.close_db()
