# THIS FILE HOLDS THE MAIN FUNCTIONS THAT INTERACT WITH OUR CONTROLLERS TO DISPLAY THE DATA

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oc_p5.controller.database_interactions import *
from oc_p5.database.generate_objects import *

database_name = "oc_p5"
engine = create_engine("mysql+pymysql://root:admin@localhost:3306/"+database_name)
session = Session(engine)


class TextColor:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def login_screen():
    """ This function display the login screen """
    print("\n---------------------------------------------------------------")
    print(TextColor.GREEN + "LOGIN" + TextColor.END)
    print("---------------------------------------------------------------\n")
    user_in_db = False
    user_is_authenticated = False
    while not user_in_db:
        username_input = input("Username : ")
        print("")
        user_in_db = is_user_in_db(session=session, username=username_input)
        if not user_in_db:
            print(TextColor.RED + "This user does not exists\n" + TextColor.END)
    while not user_is_authenticated:
        password_input = input("Password : ")
        print("")
        user_authentication = authenticate_user(session=session, username=username_input,
                                                password=password_input)
        if user_authentication["is_authenticated"]:
            logged_in_screen(user_authentication["user"])
        else:
            print(TextColor.RED + "Incorrect Password\n" + TextColor.END)


def register_screen():
    """ This function display the register screen """
    print("\n---------------------------------------------------------------")
    print(TextColor.GREEN + "REGISTER" + TextColor.END)
    print("---------------------------------------------------------------\n")
    user_already_existing = True
    while user_already_existing:
        username_input = input("Choose a username : ")
        if not is_user_in_db(session=session, username=username_input):
            user_already_existing = False
        else:
            print("\nThis user already exists\n")
    password_input = (input("\nChoose a password : "))

    add_user(session=session, user=generate_user(username=username_input, password=password_input))
    print(TextColor.GREEN + "\nYou successfully created an account, you can now log in")
    input(TextColor.BLUE + "\nPress ENTER to get back to the main menu\n" + TextColor.END)
    logged_out_screen()


def categories_screen(user):
    """
        This function display a list of the categries stored in the database
            user : User
    """
    print("\n---------------------------------------------------------------")
    print(TextColor.GREEN + "CATEGORIES LIST" + TextColor.END)
    print("---------------------------------------------------------------\n")
    for category in get_categories(session):
        print("- ", category)
    input(TextColor.BLUE + "\nPress ENTER to get back to the main menu\n" + TextColor.END)
    if user:
        logged_in_screen(user)
    else:
        logged_out_screen()


def import_products_screen(user):
    """
        This function display the menu to import the products of a category the user can select
            user : User
    """
    choice = 0
    print("\n---------------------------------------------------------------")
    print(TextColor.GREEN + "PRODUCT IMPORTER" + TextColor.END)
    print("---------------------------------------------------------------\n")
    print("Select a category you would like to import the products of :")
    print("")
    categories = get_categories(session)
    choices = display_categories(categories=categories)
    print(len(choices) + 1, "- All of the categories")
    choices.append(str(len(choices) + 1))
    print("")
    while choice not in choices:
        choice = input(TextColor.GREEN + "Your choice: " + TextColor.END)
        print("")
        if choice not in choices:
            print("This choice is not correct !")
            print("")
    print("Importing products...")
    if int(choice) == len(categories) + 1:
        products = generate_products(session, categories)
    else:
        products = generate_products(session, [categories[int(choice) - 1]])
    add_products_to_bdd(session=session, products=products)
    input(TextColor.BLUE + "\nPress ENTER to get back to the main menu\n" + TextColor.END)
    if user:
        logged_in_screen(user)
    else:
        logged_out_screen()


def display_categories(categories):
    """
        This function display a specified list of categories
            categories : list
            choices : list
    """
    choices = []
    for i in range(1, len(categories) + 1):
        print(i, "-", categories[i - 1])
        choices.append(str(i))
    return choices


def choose_category_screen():
    """
        This function lets the user choose for category
            return : str
    """
    categories = get_categories(session)
    choice = 0
    print("\n---------------------------------------------------------------")
    print(TextColor.GREEN + "PRODUCT REPLACER" + TextColor.END)
    print("---------------------------------------------------------------\n")
    print("Select a category you would like to view the products of :")
    print("")
    choices = display_categories(categories=categories)
    print("")
    while choice not in choices:
        choice = input(TextColor.GREEN + "Your choice: " + TextColor.END)
        print("")
        if choice not in choices:
            print("This choice is not correct !")
            print("")

    return categories[int(choice) - 1]


def replace_product_screen(user, category):
    """
        This function lets the user select a product from a specified category and a healthier substitute
        he can then choose to save his selections or not
            user : User
            category : str
    """
    products = get_products_from_bdd(session, [category])
    choices = [product["id"] for product in products]
    choice = 0
    display_products(products)
    while choice not in choices:
        choice = int(input("\nSelect a product by its Id, to get healthier options : "))
        if choice not in choices:
            print("\nThis product does not exist!")
    product_to_replace = get_product_by_id(session, choice)
    input("\nPress ENTER to reveal a list of healthier products from the same category\n")
    healthier_products = get_healthier_products(session, product_to_replace)
    choices = [product["id"] for product in healthier_products]
    choice = 0

    display_products(healthier_products)
    while choice not in choices:
        choice = int(input("\nSelect a product by its Id, to replace the original product with : "))
        if choice not in choices:
            print("\nThis product does not exist!")
    healthier_selected_product = get_product_by_id(session, choice)
    print(TextColor.GREEN + "\nYou originally selected this product :\n" + TextColor.END)
    display_products([product_to_replace.__dict__])
    print(TextColor.GREEN + "\nYou chose to replace it with this healthier product :\n" + TextColor.END)
    display_products([healthier_selected_product.__dict__])
    print(TextColor.GREEN + "\nWould you like to save these products in your account?\n" + TextColor.END)
    print(TextColor.GREEN + "1 - Yes, save it" + TextColor.END)
    print(TextColor.RED + "2 - No, don't" + TextColor.END)
    choices = ["1", "2"]
    while choice not in choices or (choice == "1" and not user):
        choice = input(TextColor.GREEN + "Your choice: " + TextColor.END)
        if choice not in choices:
            print("\nThis choice does not exist!")
        if choice == "1" and not user:
            print("\nYou have to be connected to save your product replacements!\n\nYou can create an account from the "
                  "home page")
    if choice == "1":

        save_replaced_product(session, generate_saved_product(user, product_to_replace, healthier_selected_product))
    else:
        logged_out_screen()


def display_products(products):
    """
        This function displays a specified list of products as a table
            products : list
    """
    print("{:<8} | {:<80} | {:<50} | {:<10} | {:<30}".format("Id", "Name", "Brand", "Nutriscore", "Url"))
    print("------------------------------------------------------------------"
          "--------------------------------------------------------------------"
          "----------------------------------------------------------------------"
          "-----------------------------------------------------------------------"
          "-------------------------------------------------------------------------------------------------")
    for product in products:
        print("{:<8} | {:<80} | {:<50} | {:<10} | {:<30}".format(product["id"], product["name"], product["brand"],
                                                                 int(product["nutriscore"]), product["url"], ))

def saved_products_screen(user):
    """
        This function displays the list of all the saved products for a specified user
            user : User
    """
    saved_products = get_saved_products_from_bdd(session, user)
    print("---------------------------------------------------------------")
    print(TextColor.GREEN + "MY SAVED PRODUCTS" + TextColor.END)
    print("---------------------------------------------------------------\n")
    print("\033[93m {:<20} | {:<50} | {:<50} | {:<25} \033[94m| {:<50} | {:<50} | {:<50} | {:<50}\033[0m".format(


                                                                                "Original Id",
                                                                                "Original Name",
                                                                                "Original Brand",
                                                                                "Original Nutriscore",

                                                                                "Substitute Id",
                                                                                "Substitute Name",
                                                                                "Substitute Brand",
                                                                                "Substitute Nutriscore"))

    print("\033[0m------------------------------------------------------------------"
          "----------------------------------------------"
          "----------------------------------------------------------------------"
          "----------------------------------------------------------------------"
          "-----------------------------------------------------------------------"
          "-------------------------------------------------------------------------------------------------")
    for product in saved_products:

        print("\033[93m {:<20} | {:<50} | {:<50} | {:<25} \033[94m| {:<50} | {:<50} | {:<50} | {:<50}\033[0m".format(



                                                                                 product["original_product"]["id"],
                                                                                 product["original_product"]["name"],
                                                                                 product["original_product"]["brand"],
                                                                                 int(product["original_product"]["nutriscore"]),

                                                                                 product["substitute_product"]["id"],
                                                                                 product["substitute_product"]["name"],
                                                                                 product["substitute_product"]["brand"],
                                                                                 int(product["substitute_product"]["nutriscore"])))
    input(TextColor.BLUE + "\nPress ENTER to get back to the main menu\n" + TextColor.END)
    if user:
        logged_in_screen(user)
    else:
        logged_out_screen()

def logged_out_screen():
    """ This function displays the main menu for a non-authenticated user """
    print("\n---------------------------------------------------------------")
    print(TextColor.GREEN + "WELCOME" + TextColor.END)
    print("---------------------------------------------------------------\n")
    print(TextColor.BLUE + "1" + TextColor.END + " - Login")
    print(TextColor.BLUE + "2" + TextColor.END + " - Register")
    print(TextColor.BLUE + "3" + TextColor.END + " - Replace My Product!")
    print(TextColor.BLUE + "4" + TextColor.END + " - My Saved Products")
    print(TextColor.BLUE + "5" + TextColor.END + " - Categories list")
    print(TextColor.BLUE + "6" + TextColor.END + " - Products Importer\n")
    choice = 0
    choices = ["1", "2", "3", "5", "6"]
    while choice not in choices:
        choice = input(TextColor.GREEN + "Your choice: " + TextColor.END)
        if choice not in choices and choice != "4":
            print("\nThis choice doesn't exist!\n")
        if choice == "4":
            print(TextColor.RED + "\nYou have to be logged-in to view your saved products!\n" + TextColor.END)

    if choice == "1":
        login_screen()
    elif choice == "2":
        register_screen()
    elif choice == "3":
        replace_product_screen(user=None, category=choose_category_screen())
    elif choice == "5":
        categories_screen(user=None)
    elif choice == "6":
        import_products_screen(user=None)


def logged_in_screen(user):
    """ This function displays the main menu for an authenticated user """
    print("\n---------------------------------------------------------------")
    print(TextColor.GREEN + "WELCOME {}!".format(user.username) + TextColor.END)
    print("---------------------------------------------------------------\n")
    print(TextColor.BLUE + "1" + TextColor.END + " - Replace My Product!")
    print(TextColor.BLUE + "2" + TextColor.END + " - My Saved Products")
    print(TextColor.BLUE + "3" + TextColor.END + " - Categories list")
    print(TextColor.BLUE + "4" + TextColor.END + " - Products Importer")
    print(TextColor.BLUE + "5" + TextColor.END + " - Logout\n")
    choice = 0
    choices = ["1", "2", "3", "4", "5"]
    while choice not in choices:
        choice = input(TextColor.GREEN + "Your choice: " + TextColor.END)
        print("")
        if choice not in choices:
            print("This choice doesn't exist!")
            print("")
    if choice == "1":
        replace_product_screen(user, choose_category_screen())
    elif choice == "2":
        saved_products_screen(user)
    elif choice == "3":
        categories_screen(user)
    elif choice == "4":
        import_products_screen(user)
    elif choice == "5":
        logged_out_screen()

categories = ["sandwichs", "bonbons", "jambons", "chips"]

add_categories_to_bdd(session=session, categories=generate_categories(categories))

logged_out_screen()
