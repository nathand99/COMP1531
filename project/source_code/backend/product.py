from base import BaseClass
import math
from util import *

class Product(BaseClass):
    def __init__(self, name, price, ingredient_consumption=None):
        self._name = name # str
        self._ingredient_consumption = ingredient_consumption # List<Ingredient, int>
        self._price = price # float
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price

    @property
    def ingredient_consumption(self):
        return self._ingredient_consumption

    @ingredient_consumption.setter
    def ingredient_consumption(self, ingredient_consumption):
        self._ingredient_consumption = ingredient_consumption

    def is_available(self, ingredient_stock, quantity=1):
        """
        Args:
            ingredient_stock: ingredients and their available quantities (List<(Ingredient, int)>)
            quantity: quantity of the products to be checked (int)
        Returns:
            whether there are enough ingredients to serve such quantity of products (bool)
        """
        return self.get_available_quantity(ingredient_stock) >= quantity

    def get_available_quantity(self, ingredient_stock):
        """
        Args:
            ingredient_stock: ingredients and their available quantities (List<(Ingredient, int)>)
        Returns:
            the amount of this products able to be served based on the available ingredients (int)
        """
        ingredient_stock_copy = ingredient_stock.copy()
        max_available = math.inf
        for i in self._ingredient_consumption:
            for  j in ingredient_stock_copy:
                if i[0] == j[0]:
                    temp_max_available = j[1] // i[1]
                    if temp_max_available < 1:
                        return 0
                    
                    max_available = min(max_available, temp_max_available)
        return max_available if max_available != math.inf else 0
    
    def get_ingredient_consumption(self, quantity=1):
        """
        Args:
            quantity: quantity of the products required (int)
        Returns:
            list of ingredient and their required quantities to produce that many of such products (List<(Ingredient, int)>)
        """
        return [(i, c*quantity) for i,c in self._ingredient_consumption]

    def __str__(self):
        ingredient_consumption_string = ""
        for i,q in self.ingredient_consumption:
            ingredient_consumption_string += str(i)  + ":" + str(q) + ", "
        return f"Product <name: {self._name}, ingredient consumption: {ingredient_consumption_string}, price: {self._price}>"

class Side(Product):
    def __str__(self):
        return "Side" + super().__str__()

class Drink(Product):
    def __str__(self):
        return "Drink" + super().__str__()

class ProductForMain(Product):
    pass

class Base(ProductForMain):
    def __str__(self):
        return "Base" + super().__str__()

class MajorFilling(ProductForMain):
    def __str__(self):
        return "MajorFilling" + super().__str__()

class MinorFilling(ProductForMain):
    def __str__(self):
        return "MinorFilling" + super().__str__()