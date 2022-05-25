from product import *
from util import *
from errors import *
from datetime import datetime

class Order:
    STATUS_CREATING = "Creating"
    STATUS_CHECKOUT = "Checked out"
    STATUS_READY = "Ready"
    STATUS_PICKED_UP = "Picked up"
    
    def __init__(self, id=None, init_status=None):
        self._id = id # int
        self._status = init_status if init_status is not None else Order.STATUS_CREATING # str
        self._main_type = None # MainType
        self._product_quantities = [] # List<(Product, int)>
        self._checkout_timestamp = None

    """
        Properties
    """
    @property
    def id(self):
        return self._id
    
    @property
    def status(self):
        return self._status

    @property
    def main_type(self):
        return self._main_type

    @property
    def product_quantities(self):
        return self._product_quantities.copy()

    @property
    def products(self):
        return [p for p,_ in self._product_quantities]
    
    @property
    def checkout_timestamp(self):
        return self._checkout_timestamp

    @property
    def checkout_timestamp_str(self):
        return self._checkout_timestamp.strftime("%H:%M:%S %d/%m/%Y")
    
    @property
    def duration_from_checkout(self):
        return datetime.now() - self.checkout_timestamp

    @property
    def duration_from_checkout_str(self):
        delta = self.duration_from_checkout
        return f"{str(delta.seconds//60) + ' m ' if delta.seconds//60>0 else ''}{str(delta.seconds) + ' s ' if delta.seconds%60!=0 else ''}"

    @property
    def type_quantities(self):
        types = set([type(p) for p in self.products])
        dict_type_quantities = {}
        for t in types:
            dict_type_quantities.update({t.key_str(): sum([q for _,q in self.get_product_quantities(product_types=t)])})
        return dict_type_quantities

    @property
    def type_product_quantities(self):
        types = set([type(p) for p in self.products])
        dict_type_quantities = {}
        for t in types:
            dict_type_quantities.update({t.key_str(): self.get_product_quantities(product_types=t)})
        return dict_type_quantities

    @staticmethod
    def all_status():
        return [Order.STATUS_CREATING, Order.STATUS_CHECKOUT, Order.STATUS_READY, Order.STATUS_PICKED_UP]

    @staticmethod
    def all_checked_out_status():
        return [Order.STATUS_CHECKOUT, Order.STATUS_READY, Order.STATUS_PICKED_UP]

    @id.setter
    def set_id(self, id):
        self._id = id

    @status.setter
    def status(self, status):
        self._status = status
        if self._status == Order.STATUS_CHECKOUT:
            self._checkout_timestamp = datetime.now()

    @main_type.setter
    def set_main_type(self, main_type):
        self._main_type = main_type

    @checkout_timestamp.setter
    def checkout_timestamp(self, timestamp):
        self._checkout_timestamp = timestamp
    
    def select_main_type(self, main_type, current_stock): ##
        """ Select main type and get ingredient consumption change
        Args:
            main_type: Main type to be switched to (MainType)
            current_stock: ingredient stock to determine what products goes onto the minimal main type (List<(Ingredient, int)>)
        Returns:
            ingredient consumption change (List<(Ingredient, int)>)
        """
        self._main_type = main_type
        ingredient_consumption_for_old_main = self.get_ingredient_consumption(product_types=(ProductForMain,))
        product_quantities_for_old_main = self.get_product_quantities(product_types=(ProductForMain,))
        self.remove_products(product_types=ProductForMain)
        temp_stock = merge_stock(current_stock, ingredient_consumption_for_old_main)
        product_quantities_for_new_main = main_type.get_default_products(temp_stock)
        self._product_quantities = merge_stock(self._product_quantities, product_quantities_for_new_main)
        ingredient_consumption_for_new_main = main_type.get_default_ingredient_consumption(temp_stock)
        return cancel_stock(ingredient_consumption_for_new_main, ingredient_consumption_for_old_main)

    def remove_products(self, product_types):
        """ Simply remove all the products belonging or extending that type
        """
        self._product_quantities = [(p,q) for p, q in self._product_quantities if not isinstance(p, product_types)]

    def set_product(self, product, quantity): ##
        """ Change the product quantity and get ingredient consumption change

        If the quantity = 0, the corresponding product will be removed from the order
        If the product has not been included in the order, it will be included
        
        Args:
            product: Product whose quantity to be changed (Product)
            quantity: New quantity of product to be stored in the order (int)
        Returns:
            ingredient consumption change (List<(Ingredient, int)>)
        """
        for p, q in self._product_quantities:
            if p == product:
                self._product_quantities.remove((p,q))
                if quantity != 0:
                    self._product_quantities.append((p, quantity))
                diff = quantity - q
                return product.get_ingredient_consumption(diff)
        if quantity != 0:
            self._product_quantities.append((product, quantity))
        return product.get_ingredient_consumption(quantity)
    
    def get_quantity_of_product(self, product):
        """ Get quantity of a product included in the order
        Args:
            product: Product whose quantity to be inspected (Product)
        Returns:

        """
        for p, q in self.product_quantities:
            if p is product:
                return q
        return 0


    def get_product_quantities(self, product_types=Product): ##
        """ Get product quantites of the respective product type
        Args:
            product_types: the type of the products to be included for computation (type OR (type,...))
        Returns:
            Product quantities contained in the order (List<(Product, int)>)
        """
        return [c for c in self._product_quantities if 
                    isinstance(c[0], product_types)]

    def get_ingredient_consumption(self, product_types=Product): ##
        """ Compute total ingredient consumption of the respective product type
        Args:
            product_types: the type of the products to be included for computation (type OR (type,...))
        Returns:
            Ingredient consumption by the order (List<(Ingredient, int)>)
        """
        product_quantities = self.get_product_quantities(product_types=product_types)
        stock = []
        for p,q in product_quantities:
            stock = merge_stock(stock, p.get_ingredient_consumption(q))
        return stock

    def compute_total_price(self): ##
        """ Compute the total price of the order
        
        Returns:
            Total price of the order (float)
        """
        price = self._main_type.base_price if self._main_type is not None else 0
        for p, q in self._product_quantities:
            price += p.price*q
        return price

    def checkout(self):
        """ Check out the order
        """
        self._status = Order.STATUS_CHECKOUT
        self.checkout_timestamp = datetime.now()

    # """
    #     Action Validation
    # """
    # def _check_when_checkout(self):
    #     if self.status != Order.STATUS_CREATING:
    #         IncorrectValueException("order", "Order that is not in 'Creating' state cannot be checked out")
    #     elif self._main_type is None:
    #         raise IncorrectMainTypeInOrderException("main_type", f"You need to select 1 main type in order to checkout")
    #     else:
    #         self._main_type.check_when_checkout(self._product_quantities)

    # def _check_when_ready_to_serve(self):
    #     if self.status == Order.STATUS_CHECKOUT:
    #         raise IncorrectValueException("order", "Order that has not been checked out cannot be prepared")

    
    # def _check_when_set_product(self, product, quantity, available_ingredients): ##
    #     if self.status != Order.STATUS_CREATING:
    #         IncorrectValueException("order", "Order that is not in 'Creating' state cannot be checked out")
    #     if self._main_type is not None:
    #         err += self._main_type.check_when_ordering_product(product, quantity, self._product_quantities)
    #     elif isinstance(product, ProductForMain):
    #         err.append(MainTypeNotSelectedException("order", f"You need to select 1 main type before you order its ingredients"))
    #     if err:  return err
    #     if not is_contain_stock(available_ingredients, product.get_ingredient_consumption(quantity - self._get_product_quantity(product))):
    #         err.append(NotEnoughStockException("order/product", f"There are not enough stock for {quantity} of {product}"))
    #     return err
    
    # def check_when_selecting_main(self, main_type, available_ingredients): ##
    #     err = self.check_when_ordering()
    #     if err or main_type == self._main_type:
    #         return err
    #     temp_ingredient_stock = merge_stock(available_ingredients, self.get_ingredient_consumption(product_types=ProductForMain))
    #     if not main_type.get_default_products(temp_ingredient_stock):
    #         err.append(NotEnoughStockException("order/main_type", f"There are not enough stock to change to {main_type}"))
    #     return err
        
    
    def is_product_allowed(self, product): ##
        """ Check if the product is allowed for the main type
        """
        return not isinstance(product, ProductForMain) or \
            (self._main_type is not None and \
                self._main_type.is_product_allowed(product))

    