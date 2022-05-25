from util import merge_stock
from base import BaseClass
class StandardMain(BaseClass):
    def __init__(self, name, main_type, product_quantities):
        self._name = name
        self._main_type = main_type
        self._product_quantities = product_quantities

    @property
    def name(self):
        return self._name

    @property
    def main_type(self):
        return self._main_type

    @property
    def product_quantities(self):
        return self._product_quantities

    def get_ingredient_consumption(self):
        ingredient_consumption = []
        for p,q in self.product_quantities:
            ingredient_consumption = merge_stock(ingredient_consumption, p.get_ingredient_consumption(quantity=q))
        return ingredient_consumption


    