# ---------------------------------------------------------------
# ProductManager
# Reads the CSV file, keeps the products in memory
# and provides the basic actions (display, search, filter)
# ---------------------------------------------------------------

import csv  # standard Python module to read CSV files

from models.product import Product


class ProductManager:
    def __init__(self, file_path):
        # Path to the CSV file, e.g. "data/products.csv"
        self.file_path = file_path
        # List that will contain all the Product objects
        self.products = []

    # Read the CSV file and fill self.products
    def load_products(self):
        # encoding="utf-8" is needed for accented characters (Écran, Câble...)
        with open(self.file_path, encoding="utf-8") as fichier:
            # DictReader uses the first line (header) as column names
            # delimiter=";" because our file is separated by semicolons
            csv_reader = csv.DictReader(fichier, delimiter=";")

            for row in csv_reader:
                # row is a dictionary: {"reference": "KB-001", "name": "...", ...}
                # WARNING: every value read from a CSV is a string
                # -> convert the price to float and the quantity to int
                product = Product(
                    reference=row["reference"],
                    name=row["name"],
                    category=row["category"],
                    unit_price=float(row["unit_price"]),
                    minimum_quantity=int(row["minimum_quantity"]),
                )

                self.products.append(product)

    # Display every product (print calls Product.__str__)
    def display_products(self):
        for p in self.products:
            print(p)

    # Return ONE product (a reference is unique), or None if not found
    def find_by_reference(self, reference):
        for p in self.products:
            # upper() on both sides -> "kb-001" matches "KB-001"
            if p.reference.upper() == reference.upper():
                return p
        # We went through the whole list without finding it
        return None

    # Return the LIST of products of a category (may be empty)
    def find_by_category(self, category):
        products_category = []

        for p in self.products:
            # case-insensitive comparison
            if p.category.upper() == category.upper():
                products_category.append(p)

        return products_category

    # Return every category name, without duplicates, sorted alphabetically
    def find_all_category(self):
        # a set automatically ignores duplicates
        category = set()

        for p in self.products:
            category.add(p.category)

        # sorted() turns the set into a sorted list
        return sorted(category)

    # Return the products whose price is strictly between min_price and max_price
    def find_product_by_range(self, min_price, max_price):
        products = []

        for p in self.products:
            if min_price < p.unit_price < max_price:
                products.append(p)

        # Sort from cheapest to most expensive
        # key=... tells sort() which attribute to compare
        products.sort(key=lambda p: p.unit_price)
        return products
