import csv

from models.product import Product


class ProductManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.products = []

    def load_products(self):
        with open(self.file_path, encoding="utf-8") as fichier:
            csv_reader = csv.DictReader(fichier, delimiter=";")

            for row in csv_reader:
                product = Product(
                    reference=row["reference"],
                    name=row["name"],
                    category=row["category"],
                    unit_price=float(row["unit_price"]),
                    minimum_quantity=int(row["minimum_quantity"]),
                )

                self.products.append(product)

    def display_products(self):
        for p in self.products:
            print(p)

    def find_by_reference(self, reference):
        for p in self.products:
            if p.reference.upper() == reference.upper():
                return p
        return None

    def find_by_category(self, category):
        products_category = []

        for p in self.products:
            if p.category.upper() == category.upper():
                products_category.append(p)

        return products_category

    def find_all_category(self):
        category = set()

        for p in self.products:
            category.add(p.category)

        return sorted(category)

    def find_product_by_range(self, min_price, max_price):
        products = []

        for p in self.products:
            if min_price < p.unit_price < max_price:
                products.append(p)

        products.sort(key=lambda p: p.unit_price)
        return products
