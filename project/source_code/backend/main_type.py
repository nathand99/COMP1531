from product import *
from util import *
from errors import *
from functools import reduce
from base import BaseClass

class MainType(BaseClass):
    def __init__(self, name, product_choices=None, base_price=0, base_selection_range=(1,1),major_filling_selection_range=(1,1), \
        base_quantity_range=(1,1), major_filling_quantity_range=(1,1), minor_filling_quantity_range=(1,1)):
        self._name = name # str
        self._product_choices = product_choices # List<ProductForMain>
        self._base_price = base_price # float
        self._selection_ranges = {Base: base_selection_range, MajorFilling: major_filling_selection_range}
        self._quantity_ranges = {Base: base_quantity_range, MajorFilling: major_filling_quantity_range, MinorFilling: minor_filling_quantity_range}
    
    @property
    def name(self):
        return self._name
    
    @property
    def product_choices(self):
        return self._product_choices
    
    @property
    def base_price(self):
        return self._base_price

    @property
    def selection_ranges(self):
        return self._selection_ranges
    
    @property
    def quantity_ranges(self):
        return self._quantity_ranges

    @product_choices.setter
    def product_choices(self, product_choices):
        self._product_choices = product_choices

    def is_product_allowed(self, product):
        return not isinstance(product, ProductForMain) or product in self._product_choices

    def is_available(self, ingredient_stock):
        return self.get_default_products(ingredient_stock) != []
    
    def get_default_products(self, ingredient_stock):
        """ Returns a list of ProductForMain based on the available ingredients in the stock
        Args:
            ingredient_stock: List of ingredient quantities in stock (List<(Ingredient, int)>) (may be subject to modification)
        Returns:
            If there is sufficient amount of ingredients to produce a minimum main: List of default ProductForMain (List<(ProductForMain, int)>)
            else: None
        """
        ingredient_stock_copy = ingredient_stock.copy()
        default_products = []
        conditions_for_each_type = {Base: False, MajorFilling: False}
        for p in self._product_choices:
            for t in conditions_for_each_type.keys():
                if isinstance(p, t) and not conditions_for_each_type.get(t, True):
                    if is_contain_stock(ingredient_stock_copy, p.get_ingredient_consumption(self._quantity_ranges[t][0])):
                        default_products.append((p, self._quantity_ranges[t][0]))
                        ingredient_stock_copy = cancel_stock(ingredient_stock_copy, p.get_ingredient_consumption(self._quantity_ranges[t][0]))
                        conditions_for_each_type.update({t: True})

        if reduce(lambda c1, c2: c1 and c2, list(conditions_for_each_type.values())):
            return default_products
        return []

    def get_default_ingredient_consumption(self, ingredient_stock):
        product_quantities = self.get_default_products(ingredient_stock)
        stock = []
        for p, q in product_quantities:
            stock = merge_stock(stock, p.get_ingredient_consumption(q))
        return stock


    def is_num_selections_within_limits(self, products, product_type=None, upper_only=False):
        product_types = list(self._selection_ranges) if product_type is None else [product_type]
        for pt in product_types:
            num_selection_of_such_type = len([p for p in products if isinstance(p, pt)])
            if upper_only:
                if self.selection_ranges.get(pt, (0, math.inf))[1] < num_selection_of_such_type:
                    return False
            elif not is_within_range_inclusive(self._selection_ranges.get(pt, None), num_selection_of_such_type):
                return False
        return True

    def is_quantities_within_limits(self, product_quantities, product_type=None, upper_only=False):
        product_types = list(self._selection_ranges) if product_type == None else [product_type]
        for pt in product_types:
            total_quantity_of_such_type = sum([q for p,q in product_quantities if isinstance(p, pt)])
            if upper_only:
                if self._quantity_ranges.get(pt, (0, math.inf))[1] < total_quantity_of_such_type:
                    return False
            elif not is_within_range_inclusive(self._quantity_ranges.get(pt, None), total_quantity_of_such_type):
                return False
        return True





    
    # def check_if_product_is_allowed(self, product):
    #     if not self.is_product_allowed(product):
    #         return [ProductNotAllowedForMainException("main_type", f"Product {product.name} cannot gp onto main type {self.name} ")]
    #     return []

    # def check_selection_within_range_when_ordering_product(self, product, ordered_product_quantities):
    #     list_products_of_same_type = [p for (p,q) in ordered_product_quantities if isinstance(p, product.__class__)]
    #     num_selection = len(list_products_of_same_type) + (1 if product not in list_products_of_same_type else 0)
    #     if not is_within_range_inclusive(self._selection_ranges.get(product.__class__, None), num_selection):
    #         return [ExceedLimitException("main_type/selection", \
    #             f"There are already {len(list_products_of_same_type)} selections of {product.__class__.__name__} for the main, \
    #                 whose number is limited by range {self._selection_ranges.get(product.__class__, (0,0))}")]
    #     return []

    # def check_quantity_within_range_when_ordering_product(self, product, quantity, ordered_product_quantities):
    #     quantity_list = [q for (p,q) in ordered_product_quantities if isinstance(p, product.__class__) and product != p]
    #     total_quantity = sum(quantity_list) + quantity
    #     if not is_within_range_inclusive(self._quantity_ranges.get(product.__class__, None), total_quantity):
    #         return [ExceedLimitException("main_type/quantity", \
    #             f"There are already {total_quantity - quantity} {product.__class__.__name__} for the main, \
    #                 whose number is limited by range {self._quantity_ranges.get(product.__class__, (0,0))}")]
    #     return []

    # def check_when_ordering_product(self, product, quantity, ordered_product_quantities):
    #     err = self.check_if_product_is_allowed(product)
    #     err += self.check_selection_within_range_when_ordering_product(product, ordered_product_quantities)
    #     err += self.check_quantity_within_range_when_ordering_product(product, quantity, ordered_product_quantities)
    #     return err

    # def check_when_checkout(self, products):
    #     err = []
    #     bases = [i for i in products if isinstance(i, Base)]
    #     major_fillings = [i for i in products if isinstance(i, MajorFilling)]
    #     minor_fillings = [i for i in products if isinstance(i, MinorFilling)]
        
    #     for type_product, list_products in zip((Base, MajorFilling, MinorFilling), (bases, major_fillings, minor_fillings)):
    #         if not is_within_range_inclusive(self._selection_ranges.get(type_product), len(list_products)):
    #             err.append(ExceedLimitException("main_type/selection", \
    #             f"There are already {len(list_products)} selections of {type_product.__name__} for the main, \
    #                 whose number is limited by range {self._selection_ranges.get(type_product, (0,0))}"))
    #         elif not is_within_range_inclusive(self._quantity_ranges.get(type_product), sum([p[1] for p in list_products])):
    #             err.append(ExceedLimitException("main_type/quantity", \
    #             f"There are already {sum([p[1] for p in list_products])} {type_product.__name__} for the main, \
    #                 whose number is limited by range {self._quantity_ranges.get(type_product, (0,0))}"))
    #     return err
                    
    def __str__(self):
        return f"MainType <name:{self.name}, base price:{self.base_price}"