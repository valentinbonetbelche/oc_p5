separator_f =  "\n---------------------------------------------------------------"
separator_e =  "---------------------------------------------------------------\n"

saved_products_table =  "\033[93m {:<20} | {:<50} | {:<50} | {:<25} \033[94m| {:<50} | {:<50} | {:<50} | {:<50}\033[0m".format("Original Id", "Original Name", "Original Brand",
                   "Original Nutriscore", "Substitute Id", "Substitute Name",
                   "Substitute Brand", "Substitute Nutriscore")

products_table = "{:<8} | {:<80} | {:<50} | {:<50} | {:<10} | {:<30}".format(
            "Id", "Name", "Brand", "Retailers", "Nutriscore", "Url")

def display_saved_product(product):
    print("\033[93m {:<20} | {:<50} | {:<50} | {:<25} \033[94m| {:<50} | {:<50} | {:<50} | {:<50}\033[0m".format(product["original_product"]["id"],
           product["original_product"]["name"],
           product["original_product"]["brand"],
           int(product["original_product"]["nutriscore"]),
           product["substitute_product"]["id"],
           product["substitute_product"]["name"],
           product["substitute_product"]["brand"],
           int(product["substitute_product"]["nutriscore"])))

def display_product(product):
    print("{:<8} | {:<80} | {:<50} | {:<50} | {:<10} | {:<30}".format(
        product["id"], product["name"],
        product["brand"], product["retailer"],
        int(product["nutriscore"]), product["url"]))

product_table_separator = "\033------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

connexion_needed = "\nYou have to be connected to save your product replacements!\n\nYou can create an account from the home page\n"