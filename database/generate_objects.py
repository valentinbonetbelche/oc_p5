# THIS FILE HOLDS THE FUNCTIONS THAT GENERATE THE PRODUCT, CATEGORY, SavedProduct and USER OBJECTS TO BE INSERTED IN
# THE DATABASE

from controller.api_interactions import get_pages_count, get_products
from controller.database_interactions import get_category_id
from database.create_tables import Product, Category, User, SavedProduct


def generate_products(session, categories):
    """
        This function creates a list of Product Objects for a specified list of categories, to be inserted in the
        database by the controller
            session : sqlalchemy.orm.session.Session
            categories : list
            products : list
    """
    products = []
    for index, category in enumerate(categories, 1):
        category_id = get_category_id(session, category)
        for page in range(1, get_pages_count(category) + 1):
            for i in get_products(page, category):
                if "nutrition-facts-completed" in i["states"] and "product-name-completed" \
                        in i["states"] and "brands-completed" in i["states"] and "nutriscore_score" in i and "id" in i \
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


def generate_categories(categories):
    """
        This function creates a list of Category Objects for a specified list of categories, to be inserted in the
        database by the controller
            session : sqlalchemy.orm.session.Session
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


def generate_user(username, password):
    """
        This function creates a User object with a specified username and password
            username : str
            password : str
            return : User
    """
    user = User(username=username)
    user.set_password(password)
    return user


def generate_SavedProduct(user, product_to_replace, healthier_selected_product):
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
