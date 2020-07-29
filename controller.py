import urllib
from math import ceil
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import User, Category, Product, SavedProduct


class Controller:

    def __init__(self, session):
        self.session = session

    def is_user_in_db(self, username):
        """
            This function checks if the user exists in the database by his username
                username : str
                return : bool
        """
        if self.session.query(User).filter_by(username=username).first():
            return True
        else:
            return False

    def add_user(self, user):
        """
            This function adds a specified User object to the database
                user : User
        """
        self.session.add(user)
        self.session.commit()

    def get_user(self, username):
        """
            This function gets the User object associated with a specified username from the database
                username : str
                return : User or None if user is not in database
        """
        if self.is_user_in_db(username):
            return self.session.query(User).filter_by(username=username).first()
        else:
            return None

    def authenticate_user(self, username, password):
        """
            This function checks the specified password for a specified username and returns a dict containing
            the user if so
                username : str
                password : str
                return : dict {
                                user_exists : bool
                                is_authenticated : bool
                                user : User
                        }
        """
        user = self.get_user(username)
        if user:
            if user.check_password(password):
                return {"user_exists": True,
                        "is_authenticated": True,
                        "user": user
                        }
            else:
                return {"user_exists": True,
                        "is_authenticated": False,
                        "user": user
                        }
        else:
            return {"user_exists": False,
                    "is_authenticated": False,
                    "user": None
                    }

    def add_categories_to_bdd(self, categories):
        """
            This function adds a specified list of Category objects to the database
                categories : list
        """
        print("Initializing categories...")
        for category in categories:
            self.session.add(category)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()

    def get_categories(self):
        """
            This function gets all categories' names from the database
                return : list
        """
        return [category[0] for category in self.session.query(Category.name).all()]

    def get_category_id(self, category):
        """
            This function gets the id of a category for a specified category name
                category : str
                return : int
        """
        return self.session.query(Category.id).filter(Category.name == category)

    def add_products_to_bdd(self, products):
        """
            This function adds products to the database
                products : list
        """
        imported_count = 0
        already_in_bdd_count = 0
        for product in products:
            self.session.add(product)
            try:
                self.session.commit()
                imported_count += 1
            except IntegrityError:
                already_in_bdd_count += 1
                self.session.rollback()

        print(imported_count, "out of", len(products), "products were imported.", already_in_bdd_count,
              "products were already in the database.")

    def get_products_from_bdd(self, categories):
        """
            This function gets all the products for a specified list of categories from the database
                categories : list
                return : list
        """
        products = []
        for category in categories:
            products += self.session.query(Product).filter(Product.category_id == self.get_category_id(category))
        return [product.__dict__ for product in products]

    def get_product_by_id(self, id):
        """
            This function gets the product associated by a specified id from the database
                id : int
                return : Product
        """
        return self.session.query(Product).filter(Product.id == id).first()

    def get_healthier_products(self, product_to_replace):
        """
            This function gets a list of all the Product objects with a better nutriscore from the database
                product_to_replace : Product
                return : list
        """
        return [product.__dict__ for product in self.session.query(Product)
            .filter(Product.category_id == product_to_replace.category_id)
            .filter(Product.nutriscore > product_to_replace.nutriscore)]

    def save_replaced_product(self, replacement):
        """
            This function save a specified SavedProduct object to the database
                replacement : SavedProduct
        """
        self.session.add(replacement)
        self.session.commit()

    def get_saved_products_from_bdd(self, user):
        """
            This function gets a all the saved products for a specified user
                user : User
        """
        return [{
            "SavedProduct": product.__dict__,
            "original_product": self.get_product_by_id(product.original_product_id).__dict__,
            "substitute_product": self.get_product_by_id(product.substitute_product_id).__dict__
        } for product in self.session.query(SavedProduct).filter(SavedProduct.user == user)
        ]

    def create_search_url(self, page, category):
        """
            This function creates the search url for a specified category and page number
                page : int
                category : str
                url : str
        """

        parameters = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": 100,
            "page": page,
            "json": "1"
        }
        url = "https://fr.openfoodfacts.org/cgi/search.pl?" + urllib.parse.urlencode(parameters)

        return url

    def get_pages_count(self, category):
        """
            This function retrieves the amount of result pages for a specified category
                category : str
                page_amount : int
        """

        url = self.create_search_url("1", category)

        request = requests.get(url)
        data = request.json()
        page_amount = ceil(int(data["count"]) / 100)

        return page_amount

    def get_products(self, page, category):
        """
            This function retrieves the final products of a specified page number and category by using the other functions
                page : int
                category : str
                return : list
        """
        return requests.get(self.create_search_url(page, category)).json()["products"]

    def generate_products(self, categories):
        """
            This function creates a list of Product Objects for a specified list of categories, to be inserted in the
            database by the controller
                categories : list or str
                products : list
        """
        if type(categories) == str:
            categories = [categories]
        products = []
        for index, category in enumerate(categories, 1):
            category_id = self.get_category_id(category)
            for page in range(1, self.get_pages_count(category) + 1):
                for i in self.get_products(page, category):
                    if "nutrition-facts-completed" in i["states"] and "product-name-completed" \
                            in i["states"] and "brands-completed" in i[
                        "states"] and "nutriscore_score" in i and "id" in i \
                            and "stores" in i:
                        try:
                            i["brands"].index(",")
                            multiple_brands = True
                        except ValueError:
                            multiple_brands = False
                        products.append(
                            Product(
                                ref_id=i["id"],
                                name=i["product_name"].replace("\n", ""),
                                brand=i["brands"][:i["brands"].index(",")] if multiple_brands else i["brands"],
                                nutriscore=i["nutriscore_score"],
                                category_id=category_id,
                                retailer=i["stores"],
                                url=i["url"]
                            )
                        )
                if len(products) > index * 400:
                    break
        return products

    def generate_categories(self, categories):
        """
            This function creates a list of Category Objects for a specified list of categories, to be inserted in the
            database by the controller
                categories : list
                products : list
        """
        categories_created = []
        for category in categories:
            categories_created.append(
                Category(
                    name=category
                )
            )
        return categories_created

    def generate_user(self, username, password):
        """
            This function creates a User object with a specified username and password
                username : str
                password : str
                return : User
        """
        user = User(username=username)
        user.set_password(password)
        return user

    def generate_SavedProduct(self, user, product_to_replace, healthier_selected_product):
        """
            This function creates a SavedProduct object with a specified product to replace and healthier product
                product_to_replace : Product
                healthier_selected_product : Product
                return : SavedProduct
        """
        return SavedProduct(
            original_product_id=product_to_replace.id,
            substitute_product_id=healthier_selected_product.id,
            user_id=user.id
        )