class Product:
    def __init__(self, reference, name, category, unit_price, minimum_quantity):
        self.reference = reference
        self.name = name
        self.category = category
        self.unit_price = unit_price
        self.minimum_quantity = minimum_quantity

    def __str__(self):
        return f"ref : {self.reference} - name : {self.name} - category : {self.category} - {self.unit_price} € - min qty : {self.minimum_quantity}"

