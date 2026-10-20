# ---------------------------------------------------------------
# Main program: console menu
# Run it from the project root: python main.py
# (otherwise Python cannot find the "managers" and "models" folders)
# ---------------------------------------------------------------

from managers.product_manager import ProductManager

# Triple quotes = multi-line string, printed as is
menu = """
1 - show products
2 - find product by reference
3 - find product by category
4 - find all categories
5 - find products by range
6 - Quit
"""


# Ask for a menu choice until the user types a valid integer between 1 and 6
def get_choice(value):
    while True:
        try:
            # int() raises a ValueError if the text is not a number
            choice = int(input(f"Entrez {value}"))
            if 0 < choice < 7:
                return choice
        except Exception:
            print("La valeur est incorrecte")


# Ask for a decimal number (e.g. a price) until the input is valid
def get_choice_float(value):
    while True:
        try:
            choice = float(input(f"Entrez {value}"))
            return choice
        except Exception:
            print("La valeur est incorrecte")


# Print every element of a list, one per line
def print_collection(collection):
    for e in collection:
        print(e)


def main(product_manager: ProductManager):
    # The loop runs until the user chooses "6 - Quit"
    continue_app = True
    while continue_app:
        print(menu)
        choice = get_choice("votre choix")

        # match / case (Python 3.10+): runs the block matching the choice
        match choice:
            case 1:
                # 1 - show products
                product_manager.display_products()
            case 2:
                # 2 - find product by reference
                ref = input("Entrez la référence : ")
                result_ref = product_manager.find_by_reference(ref)
                # prints the product, or "None" if the reference does not exist
                print(result_ref)
            case 3:
                # 3 - find product by category
                category = input("Entrez la category : ")
                result_categ = product_manager.find_by_category(category)

                print_collection(result_categ)
            case 4:
                # 4 - find all categories
                categories = product_manager.find_all_category()

                print_collection(categories)
            case 5:
                # 5 - find products by range
                min_price = get_choice_float("le prix minimum")
                max_price = get_choice_float("le prix maximum")
                result_range = product_manager.find_product_by_range(
                    min_price, max_price
                )

                print_collection(result_range)
            case 6:
                # 6 - Quit: the while loop stops at the next check
                continue_app = False
            case _:
                # _ = any other value (safety net)
                print("LE choix est incorrect : entrez une valeur entre 1 et 6")

    print("Merci à bientot")


# This block only runs when the file is launched directly (python main.py),
# not when it is imported from another file
if __name__ == "__main__":
    # Create the manager, load the CSV, then start the menu
    manager = ProductManager("data/products.csv")
    manager.load_products()
    main(manager)
