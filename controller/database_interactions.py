# THIS FILE HOLDS THE FUNCTIONS THAT INTERACT WITH THE DATABASE

from sqlalchemy.exc import IntegrityError
from database.create_tables import User, Category, Product, Saved_Product


def is_user_in_db(session, username):
    """
        This function checks if the user exists in the database by his username
            session : sqlalchemy.orm.session.Session
            username : str
            return : bool
    """
    if session.query(User).filter_by(username=username).first():
        return True
    else:
        return False


def add_user(session, user):
    """
        This function adds a specified User object to the database
            session : sqlalchemy.orm.session.Session
            user : User
    """
    session.add(user)
    session.commit()


def get_user(session, username):
    """
        This function gets the User object associated with a specified username from the database
            session : sqlalchemy.orm.session.Session
            username : str
            return : User or None if user is not in database
    """
    if is_user_in_db(session, username):
        return session.query(User).filter_by(username=username).first()
    else:
        return None


def authenticate_user(session, username, password):
    """
        This function checks the specified password for a specified username and returns a dict containing
        the user if so
            session : sqlalchemy.orm.session.Session
            username : str
            password : str
            return : dict {
                            user_exists : bool
                            is_authenticated : bool
                            user : User
                    }
    """
    user = get_user(session, username)
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


def add_categories_to_bdd(session, categories):
    """
        This function adds a specified list of Category objects to the database
            session : sqlalchemy.orm.session.Session
            categories : list
    """
    print("Initializing categories...")
    for category in categories:
        session.add(category)
        try:
            session.commit()
            print("The", category.name, "category was imported")
        except IntegrityError:
            session.rollback()
            print("The", category.name, "category already exists")


def get_categories(session):
    """
        This function gets all categories' names from the database
            session : sqlalchemy.orm.session.Session
            return : list
    """
    return [category[0] for category in session.query(Category.name).all()]


def get_category_id(session, category):
    """
        This function gets the id of a category for a specified category name
            session : sqlalchemy.orm.session.Session
            category : str
            return : int
    """
    return session.query(Category.id).filter(Category.name == category)


def add_products_to_bdd(session, products):
    """
        This function adds products to the database
            session : sqlalchemy.orm.session.Session
            products : list
    """
    imported_count = 0
    already_in_bdd_count = 0
    for product in products:
        session.add(product)
        try:
            session.commit()
            imported_count += 1
        except IntegrityError:
            already_in_bdd_count += 1
            session.rollback()

    print(imported_count, "out of", len(products), "products were imported.", already_in_bdd_count,
          "products were already in the database.")


def get_products_from_bdd(session, categories):
    """
        This function gets all the products for a specified list of categories from the database
            session : sqlalchemy.orm.session.Session
            categories : list
            return : list
    """
    products = []
    for category in categories:
        products += session.query(Product).filter(Product.category_id == get_category_id(session, category))
    return [product.__dict__ for product in products]


def get_product_by_id(session, id):
    """
        This function gets the product associated by a specified id from the database
            session : sqlalchemy.orm.session.Session
            id : int
            return : Product
    """
    return session.query(Product).filter(Product.id == id).first()


def get_healthier_products(session, product_to_replace):
    """
        This function gets a list of all the Product objects with a better nutriscore from the database
            session : sqlalchemy.orm.session.Session
            product_to_replace : Product
            return : list
    """
    return [product.__dict__ for product in session.query(Product)
        .filter(Product.category_id == product_to_replace.category_id)
        .filter(Product.nutriscore > product_to_replace.nutriscore)]


def save_replaced_product(session, replacement):
    """
        This function save a specified Saved_Product object to the database
            session : sqlalchemy.orm.session.Session
            replacement : Saved_Product
    """
    session.add(replacement)
    session.commit()


def get_saved_products_from_bdd(session, user):
    """
        This function gets a all the saved products for a specified user
            session : sqlalchemy.orm.session.Session
            user : User
    """
    return [{
                "saved_product": product.__dict__,
                "original_product": get_product_by_id(session, product.original_product_id).__dict__,
                "substitute_product": get_product_by_id(session, product.substitute_product_id).__dict__
        } for product in session.query(Saved_Product).filter(Saved_Product.user == user)
    ]