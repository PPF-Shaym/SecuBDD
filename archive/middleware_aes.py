import pymysql
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
class OREMiddleware:
    def __init__(self, key):
        self.key = key
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        plaintext = pad(plaintext, AES.block_size)
        ciphertext = self.cipher.encrypt(plaintext)
        return ciphertext

    def decrypt(self, ciphertext):
        decrypted = self.cipher.decrypt(ciphertext)
        return unpad(decrypted, AES.block_size).decode('utf-8')

    def insert_data(self, cursor, nom_salarie, salaire):
        encrypted_salaire = self.encrypt(str(salaire).encode())
        cursor.execute("INSERT IGNORE INTO salaires (nom, salaire_encrypted) VALUES (%s, %s) ON DUPLICATE KEY UPDATE salaire_encrypted = %s",
                       (nom_salarie, encrypted_salaire, encrypted_salaire))

    def get_data(self, cursor, lower_bound, upper_bound):
        cursor.execute("SELECT nom, salaire_encrypted FROM salaires WHERE salaire_encrypted BETWEEN %s AND %s",
                       (self.encrypt(str(lower_bound).encode()), self.encrypt(str(upper_bound).encode())))
        results = cursor.fetchall()
        decrypted_results = [(row[0], int(self.decrypt(row[1]).encode())) for row in results]
        print(decrypted_results)
        return decrypted_results

# Exemple d'utilisation du middleware
key = b'MySecretKey12345'
middleware = OREMiddleware(key)
print(middleware)

"""
import mysql.connector
#from secret import SECRET_KEY  # Assurez-vous de sécuriser cette clé dans un environnement de production
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import secrets

SECRET_KEY = secrets.token_bytes(16)  # 16 bytes for AES-128, 24 bytes for AES-192, 32 bytes for AES-256
print(SECRET_KEY)
#SECRET_KEY = "password12345678"
connection = mysql.connector.connect(host='localhost', port=3306, user='user', password='password')

def chiffre_salaire(salaire, SECRET_KEY):
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(str(salaire).encode())
    return ciphertext, cipher.nonce, tag

def dechiffre_salaire(ciphertext, nonce, tag, SECRET_KEY):
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_text.decode()

def insert_salaire(nom, salaire):
    cursor = connection.cursor()

    ciphertext, nonce, tag = chiffre_salaire(salaire, SECRET_KEY)

    cursor.execute("INSERT INTO salaires (nom, salaire_encrypted) VALUES (%s, %s)", (nom, ciphertext))
    connection.commit()

    cursor.close()
    connection.close()

def retrieve_salaire():
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM salaires")
    result = cursor.fetchall()

    for row in result:
        decrypted_salaire = dechiffre_salaire(row['salaire_encrypted'], b'', b'')
        print(f"Nom: {row['nom']}, Salaire (déchiffré): {decrypted_salaire}")

    cursor.close()
    connection.close()

# Exemple d'utilisation
username = ["John Doe", "Jane Doe", "MArtin Dos", "Edouard Lie", "Bernard Boe", "Boudeer Pale"]
salaire_month = [1000, 2000, 3000, 4000, 5000, 6000]
for i in range(len(username)):
    insert_salaire(username[i], salaire_month[i])

#retrieve_salaire()
"""

"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import pymysql

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(str(data).encode('utf-8'), AES.block_size))
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')

def store_data(data):
    key = get_random_bytes(16)
    encrypted_data = encrypt_data(data, key)

    connection = pymysql.connect(host='your_mysql_host', user='your_username', password='your_password', database='example_database')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO encrypted_table (encrypted_column) VALUES (%s)", (encrypted_data,))
    connection.commit()

    cursor.close()
    connection.close()

def retrieve_data():
    connection = pymysql.connect(host='your_mysql_host', user='your_username', password='your_password', database='example_database')
    cursor = connection.cursor()

    cursor.execute("SELECT id, encrypted_column FROM encrypted_table ORDER BY encrypted_column")
    results = cursor.fetchall()

    for result in results:
        id, encrypted_data = result
        decrypted_data = decrypt_data(encrypted_data, key)
        print(f"ID: {id}, Decrypted Data: {decrypted_data}")

    cursor.close()
    connection.close()

# Example usage
store_data(42)
store_data(15)
retrieve_data()
"""