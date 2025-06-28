class Product:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

class User:
    def __init__(self, email, password, role="client"):
        self.email = email
        self.password = password
        self.role = role
