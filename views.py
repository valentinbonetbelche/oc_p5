class TextColor:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    def blue_text(self, text):
        return self.BLUE + str(text) + self.END

    def green_text(self, text):
        return self.GREEN + str(text) + self.END

    def red_text(self, text):
        return self.RED + str(text) + self.END


class View:
    logged_in_menu_choices = [
        "Replace My Product!", "My saved Products", "Categories list",
        "Products Importer", "Logout"
    ]
    logged_out_menu_choices = [
        "Login",
        "Register",
        "Replace My Product!",
        "My saved Products",
        "Categories list",
        "Products Importer",
    ]
    text_color = TextColor()

    def __init__(self, session, controller):
        self.session = session
        self.controller = controller
        self.state = "Menu"
        self.user = None
        self.change_state(self.state)

    def change_state(self, state):
        self.state = state
        {
            "Login": self.login_screen,
            "Register": self.register_screen,
            "Replace My Product!": self.replace_product_screen,
            "My saved Products": self.saved_products_screen,
            "Categories list": self.categories_list_screen,
            "Products Importer": self.products_importer_screen,
            "Menu": self.menu_screen,
            "Logout": self.log_out
        }[self.state]()

    def log_out(self):
        self.user = None
        self.change_state("Menu")

    def display_choices(self, choices, products_importer=False):
        if products_importer:
            choices.append("All of the categories")
        choices_input = []
        for index, choice in enumerate(choices, 1):
            print(self.text_color.blue_text(text=index), "-", choice)
            choices_input.append(str(index))
        choice = 0

        while choice not in choices_input:
            choice = input(self.text_color.green_text("\nYour choice: "))
            if choice not in choices_input:
                print("\nThis choice doesn't exist!\n")
        return choices[:-1] if products_importer and int(choice) == len(
            choices) else choices[int(choice) - 1]

    def menu_screen(self):
        print(
            "\n---------------------------------------------------------------"
        )
        print(
            self.text_color.green_text("WELCOME {}!".format(
                self.user.username) if self.user else "WELCOME"))
        print(
            "---------------------------------------------------------------\n"
        )
        if self.user:
            self.change_state(
                self.display_choices(self.logged_in_menu_choices))
        else:
            self.change_state(
                self.display_choices(self.logged_out_menu_choices))

    def login_screen(self):
        """ This method display the login screen """
        print(
            "\n---------------------------------------------------------------"
        )
        print(self.text_color.green_text("LOGIN"))
        print(
            "---------------------------------------------------------------\n"
        )
        user_in_db = False
        user_is_authenticated = False
        while not user_in_db:
            username_input = input("Username : ")
            user_in_db = self.controller.is_user_in_db(username=username_input)
            if not user_in_db:
                print(
                    self.text_color.red_text("\nThis user does not exists\n"))
        while not user_is_authenticated:
            password_input = input("Password : ")
            user_authentication = self.controller.authenticate_user(
                username=username_input, password=password_input)
            if user_authentication["is_authenticated"]:
                user_is_authenticated = True
                self.user = user_authentication["user"]
                self.change_state("Menu")

            else:
                print(self.text_color.red_text("\nIncorrect Password\n"))

    def register_screen(self):
        """ This method displays the register screen """
        print(
            "\n---------------------------------------------------------------"
        )
        print(self.text_color.green_text("REGISTER"))
        print(
            "---------------------------------------------------------------\n"
        )
        user_already_existing = True
        while user_already_existing:
            username_input = input("Choose a username : ")
            if not self.controller.is_user_in_db(username=username_input):
                user_already_existing = False
            else:
                print(
                    self.text_color.red_text(
                        "\nThis username already exists\n"))
        password_input = (input("\nChoose a password : "))
        self.controller.add_user(
            user=self.controller.generate_user(
                username=username_input, password=password_input))
        print(
            self.text_color.green_text(
                "\nYou successfully created an account, you can now log in"))
        input(
            self.text_color.blue_text(
                "\nPress ENTER to get back to the main menu\n"))
        self.change_state("Menu")

    def replace_product_screen(self):
        """ This method displays the product replacement screen """
        print(
            "\n---------------------------------------------------------------"
        )
        print(self.text_color.green_text("REPLACE MY PRODUCT!"))
        print(
            "---------------------------------------------------------------\n"
        )
        products = self.controller.get_products_from_bdd(
            [self.display_choices(self.controller.get_categories())])
        choices = [product["id"] for product in products]
        choice = 0
        self.display_products(products)
        while choice not in choices:
            choice = int(
                input(
                    self.text_color.blue_text(
                        "\nSelect a product by its Id, to get healthier options : "
                    )))
            if choice not in choices:
                print(
                    self.text_color.red_text("\nThis product does not exist!"))
        product_to_replace = self.controller.get_product_by_id(choice)
        input(
            self.text_color.blue_text(
                "\nPress ENTER to reveal a list of healthier products from the same category\n"
            ))
        healthier_products = self.controller.get_healthier_products(
            product_to_replace)
        choices = [product["id"] for product in healthier_products]
        choice = 0
        self.display_products(healthier_products)
        while choice not in choices:
            choice = int(
                input(
                    self.text_color.blue_text(
                        "\nSelect a product by its Id, to replace the original product with : "
                    )))
            if choice not in choices:
                print(
                    self.text_color.red_text("\nThis product does not exist!"))
        healthier_selected_product = self.controller.get_product_by_id(choice)
        print(
            self.text_color.green_text(
                "\nYou originally selected this product :\n"))
        self.display_products([product_to_replace.__dict__])
        print(
            self.text_color.green_text(
                "\nYou chose to replace it with this healthier product :\n"))
        self.display_products([healthier_selected_product.__dict__])
        print(
            self.text_color.green_text(
                "\nWould you like to save these products in your account?\n"))
        print(self.text_color.green_text("1 - Yes, save it"))
        print(self.text_color.red_text("2 - No, don't"))
        choices = ["1", "2"]
        while choice not in choices or (choice == "1" and not self.user):
            choice = input(self.text_color.green_text("\nYour choice : "))
            if choice not in choices:
                print(
                    self.text_color.red_text("\nThis choice does not exist!"))
        if choice == "1":
            if self.user:
                self.controller.save_replaced_product(
                    self.controller.generate_SavedProduct(
                        self.user, product_to_replace, healthier_selected_product))
                print(
                    self.text_color.green_text(
                        "\nYou successfully saved this product replacement!\n"))
            else:
                print(
                    self.text_color.red_text(
                        "\nYou have to be connected to save your product replacements!\n\nYou can create an account "
                        "from the "
                        "home page\n"))
        input(
            self.text_color.blue_text(
                "\nPress ENTER to get back to the main menu\n"))
        self.change_state("Menu")

    def categories_list_screen(self):
        """ This method display a list of the categories stored in the database """
        print(
            "\n---------------------------------------------------------------"
        )
        print(TextColor.GREEN + "CATEGORIES LIST" + TextColor.END)
        print(
            "---------------------------------------------------------------\n"
        )
        for category in self.controller.get_categories():
            print("- ", category)
        input(TextColor.BLUE + "\nPress ENTER to get back to the main menu\n" +
              TextColor.END)
        self.change_state("Menu")

    def products_importer_screen(self):
        """
            This method display the menu to import the products of a category the user can select
                user : User
        """
        print(
            "\n---------------------------------------------------------------"
        )
        print(TextColor.GREEN + "PRODUCT IMPORTER" + TextColor.END)
        print(
            "---------------------------------------------------------------\n"
        )
        print("Select a category you would like to import the products of :\n")
        products = self.controller.generate_products(
            self.display_choices(
                self.controller.get_categories(), products_importer=True))
        print(self.text_color.green_text("\nImporting products...\n"))
        self.controller.add_products_to_bdd(products=products)
        input(
            self.text_color.blue_text(
                "\nPress ENTER to get back to the main menu\n"))
        self.change_state("Menu")

    def saved_products_screen(self):
        """
            This method displays the list of all the saved products for a specified user
                user : User
        """
        saved_products = self.controller.get_saved_products_from_bdd(self.user)
        print(
            "---------------------------------------------------------------")
        print(TextColor.GREEN + "MY SAVED PRODUCTS" + TextColor.END)
        print(
            "---------------------------------------------------------------\n"
        )
        print(
            "\033[93m {:<20} | {:<50} | {:<50} | {:<25} \033[94m| {:<50} | {:<50} | {:<50} | {:<50}\033[0m".
            format("Original Id", "Original Name", "Original Brand",
                   "Original Nutriscore", "Substitute Id", "Substitute Name",
                   "Substitute Brand", "Substitute Nutriscore"))

        print(
            "\033[0m------------------------------------------------------------------"
            "----------------------------------------------"
            "----------------------------------------------------------------------"
            "----------------------------------------------------------------------"
            "-----------------------------------------------------------------------"
            "-------------------------------------------------------------------------------------------------"
        )
        for product in saved_products:
            print(
                "\033[93m {:<20} | {:<50} | {:<50} | {:<25} \033[94m| {:<50} | {:<50} | {:<50} | {:<50}\033[0m".
                format(product["original_product"]["id"],
                       product["original_product"]["name"],
                       product["original_product"]["brand"],
                       int(product["original_product"]["nutriscore"]),
                       product["substitute_product"]["id"],
                       product["substitute_product"]["name"],
                       product["substitute_product"]["brand"],
                       int(product["substitute_product"]["nutriscore"])))

        if not self.user:
            print(
                self.text_color.red_text(
                    "\nYou have to be logged in to save products and visualize them!\n"
                ))
        input(
            self.text_color.blue_text(
                "\nPress ENTER to get back to the main menu\n"))
        self.change_state("Menu")

    @staticmethod
    def display_products(products):
        """
            This method displays a specified list of products as a table
                products : list
        """
        print("{:<8} | {:<80} | {:<50} | {:<50} | {:<10} | {:<30}".format(
            "Id", "Name", "Brand", "Retailers", "Nutriscore", "Url"))
        print(
            "------------------------------------------------------------------"
            "--------------------------------------------------------------------"
            "----------------------------------------------------------------------"
            "-----------------------------------------------------------------------"
            "-------------------------------------------------------------------------------------------------"
        )
        for product in products:
            print("{:<8} | {:<80} | {:<50} | {:<50} | {:<10} | {:<30}".format(
                product["id"], product["name"],
                product["brand"], product["retailer"],
                int(product["nutriscore"]), product["url"]))
