from client_middleware import ClientMiddleware

def populate_db(middleware):
    """
    Remplir la base de données avec les données fournies.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.

    Returns:
        None
    """
    username_dict = {"John":2000, 
                "Jane":2500, 
                "Martin":3000, 
                "Edouard":3500, 
                "Bernard":4000, 
                "Boudeer":4500
            }
    middleware.populate_bdd(username_dict)

def add_user(middleware, nom, salaire):
    """
    Ajouter un utilisateur à la base de données.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.
        nom (str): Nom de l'utilisateur à ajouter.
        salaire (int): Salaire de l'utilisateur à ajouter.

    Returns:
        None
    """
    username_dict = {nom: salaire}
    middleware.add_member(username_dict)

def get_employe_range(middleware, lower_bound, upper_bound):
    """
    Obtenir les employés dont le salaire est dans une plage donnée.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.
        lower_bound (int): Limite inférieure de la plage de salaire.
        upper_bound (int): Limite supérieure de la plage de salaire.

    Returns:
        None
    """
    decrypted_results = middleware.range_compare(lower_bound, upper_bound)
    for nom_salarie, salaire in decrypted_results:
        print(f"Nom: {nom_salarie}, Salaire: {salaire}")

def get_employe_upper(middleware, upper_salarie):
    """
    Obtenir les employés dont le salaire est supérieur à une valeur donnée.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.
        upper_salarie (int): Valeur de salaire supérieure.

    Returns:
        None
    """
    decrypted_results = middleware.get_data_greater_than(upper_salarie)
    for nom_salarie, salaire in decrypted_results:
        print(f"Nom: {nom_salarie}, Salaire: {salaire}")

def get_employe_lower(middleware, lower_salarie):
    """
    Obtenir les employés dont le salaire est inférieur à une valeur donnée.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.
        lower_salarie (int): Valeur de salaire inférieure.

    Returns:
        None
    """
    decrypted_results = middleware.get_data_lower_than(lower_salarie)
    for nom_salarie, salaire in decrypted_results:
        print(f"Nom: {nom_salarie}, Salaire : {salaire}")

def get_employe(middleware, nom1, nom2):
    """
    Obtenir les détails des employés en comparant leurs noms.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.
        nom1 (str): Nom du premier employé.
        nom2 (str): Nom du deuxième employé.

    Returns:
        None
    """
    decrypted_results = middleware.get_data_compare(nom1, nom2)
    for nom_salarie, salaire in decrypted_results:
        print(f"Nom: {nom_salarie}, Salaire: {salaire}")

def get_employe_sum(middleware, nom1, nom2):
    """
    Obtenir la somme des salaires de deux employés.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.
        nom1 (str): Nom du premier employé.
        nom2 (str): Nom du deuxième employé.

    Returns:
        None
    """
    decrypted_results = middleware.addition_data(nom1, nom2)
    print(f"Somme de {nom1}, {nom2}, Salaire: {decrypted_results}")

def get_user_list(middleware):
    """
    Obtenir la liste des utilisateurs de la base de données.

    Args:
        middleware (ClientMiddleware): Instance du middleware client pour interagir avec la base de données.

    Returns:
        None
    """
    results_ope, results_he = middleware.get_user_list()
    combined_lists = list(zip(results_ope, results_he))
    for item in combined_lists:
        print(item[0][0], " | ", item[1][0])

def main_menu():
    """
    Afficher le menu principal et gérer les actions de l'utilisateur.

    Returns:
        None
    """
    middleware = ClientMiddleware(b'random_key123456')
    populate_db(middleware)
    while True:
        print("1. Add User")
        print("2. Get Employees in Salary Range")
        print("3. Get Employees with Salary Upper Bound")
        print("4. Get Employees with Salary Lower Bound")
        print("5. Get Employee Details")
        print("6. Get Employee Salary Sum")
        print("7. Get Employee List")
        print("0. Exit")

        choice = input("Enter your choice (0-6): ")

        if choice == '1':
            nom1 = input("Enter first employee name: ")
            salaire = int(input("Enter Salaire: "))
            add_user(middleware, nom1, salaire)
        elif choice == '2':
            lower_bound = int(input("Enter lower salary bound: "))
            upper_bound = int(input("Enter upper salary bound: "))
            get_employe_range(middleware, lower_bound, upper_bound)
        elif choice == '3':
            upper_salarie = int(input("Enter upper salary bound: "))
            get_employe_upper(middleware, upper_salarie)
        elif choice == '4':
            lower_salarie = int(input("Enter lower salary bound: "))
            get_employe_lower(middleware, lower_salarie)
        elif choice == '5':
            nom1 = input("Enter first employee name: ")
            nom2 = input("Enter second employee name: ")
            get_employe(middleware, nom1, nom2)
        elif choice == '6':
            nom1 = input("Enter first employee name: ")
            nom2 = input("Enter second employee name: ")
            get_employe_sum(middleware, nom1, nom2)
        elif choice == '7':
            get_user_list(middleware)
        elif choice == '0':
            print("Exiting program. Goodbye!")
            middleware.close_db()
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 6.")

if __name__ == "__main__":
    main_menu()
