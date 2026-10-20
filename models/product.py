# ---------------------------------------------------------------
# Product model
# One Product object = one line of data/products.csv
# CSV columns: reference;name;category;unit_price;minimum_quantity
# ---------------------------------------------------------------


class Product:
    def __init__(self, reference, name, category, unit_price, minimum_quantity):
        # Each CSV column becomes an attribute of the object
        self.reference = reference                  # unique code, e.g. "KB-001"
        self.name = name
        self.category = category
        self.unit_price = unit_price                # float (converted by the manager)
        self.minimum_quantity = minimum_quantity    # int (converted by the manager)

    # __str__ is called automatically by print(product)
    def __str__(self):
        return f"ref : {self.reference} - name : {self.name} - category : {self.category} - {self.unit_price} € - min qty : {self.minimum_quantity}"
