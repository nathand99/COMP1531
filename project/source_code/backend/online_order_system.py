from order import Order
from functools import wraps
"""
    Notation: Raises:
                - : should not fail if the frontend is implemeneted correctly
                * : might fail if the frontend is still implemented correctly
"""

from ingredient import *
from product import *
from main_type import MainType
from standard_main import StandardMain
from util import *
from id_generator import IDGenerator
from staff_manager import StaffManager
from errors import *
import os, pickle
class OnlineOrderSystem(object):
    class _SessionDecorator:
        @classmethod
        def save_session_wrapper(cls,fun):
            def wrapper(self, *args, **kwargs):
                returned_object = fun(self, *args, **kwargs)
                self.save_session()
                return returned_object
            return wrapper

    _default_saved_session_file_dir = "./database/"
    _default_saved_session_file_name = "saved_session.pkl"

    @classmethod
    def init(cls, file_dir=None, file_name=None, reinstantiate_if_fail=False):
        file_dir = OnlineOrderSystem._default_saved_session_file_dir if file_dir is None else file_dir
        file_name = OnlineOrderSystem._default_saved_session_file_name if file_name is None else file_name
        try:
            os.makedirs(file_dir,exist_ok=True)
            with open(os.path.join(file_dir, file_name), "rb+") as f:
                system = pickle.load(f)
            # Remove order with STATUS_CREATING
            for o in system.orders:
                if o.status == Order.STATUS_CREATING:
                    system.cancel_order(o)
            return system
        except IOError:
            print(f"Cannot retrieve pickle file from path: {os.path.join(file_dir,file_name)}.")
            if reinstantiate_if_fail:
                print("A new empty instance is initiated instead")
                return cls(file_dir=file_dir, file_name=file_name)
        
        return None
    
    def save_session(self):
        try:
            os.makedirs(self._file_dir,exist_ok=True)
            with open(os.path.join(self._file_dir, self._file_name), "wb+") as f:
                system = pickle.dump(self, f)
        except IOError:
            print(f"Cannot store pickle file to path: {os.path.join(self._file_dir, self._file_name)}.")
            return False
        return True
    
    
        

    def __init__(self, order_id_generator=None, file_dir=None, file_name=None):
        self._order_id_generator = IDGenerator(id_length=6) if order_id_generator is None else order_id_generator
        self._dict_ingredient_stock = {} # Dict<Ingredient.name, (Ingredient, int)>
        self._dict_main_types = {} # Dict<MainType.name, MainType>
        self._dict_standard_mains = {} # Dict<StandardMain.name, StandardMain>
        self._dict_products = {} # Dict<Product.name, Product>
        self._dict_orders = {} # List<Order>
        self._staff_manager = StaffManager()
        self._file_dir = OnlineOrderSystem._default_saved_session_file_dir if file_dir is None else file_dir
        self._file_name = OnlineOrderSystem._default_saved_session_file_name if file_name is None else file_name

    """
        Conversion: Convert str to corresponding objects
    """
    def get_ingredient(self, ingredient):
        """ Search ingredient that match the keyword
        Args:
            ingredient: ingredient name: str
        Returns:
            ingredient with name == keyword (Ingredient)
        """
        if isinstance(ingredient, Ingredient):
            return ingredient if ingredient in self.ingredients else None
        pair = self._dict_ingredient_stock.get(ingredient, None)
        return pair[0] if pair is not None else None
    
    def get_main_type(self, main_type):
        """ Search main_type that match the keyword
        Args:
            main_type: main_type name: (MainType, str)
        Returns:
            main_type with name == keyword (MainType)
        """
        if isinstance(main_type, MainType):
            return main_type if main_type in self.main_types else None
        return self._dict_main_types.get(main_type, None)

    def get_standard_main(self, standard_main):
        """ Search standard_main that match the str
        Args:
            standard_main: main_type name: (StandardMain, str)
        Returns:
            standard main with name == keyword (StandardMain)
        """
        if isinstance(standard_main, StandardMain):
            return standard_main if standard_main in self.standard_mains else None
        return self.dict_standard_mains.get(standard_main, None)

    def get_product(self, product):
        """ Search product that match the keyword
        Args:
            product: product name: str
        Returns:
            product with name == keyword (Product)
        """
        if isinstance(product, Product):
            return product if product in self.products else None
        return self._dict_products.get(product, None)

    """
        END: Conversion: Convert str to corresponding objects
    """
    """
        Retrieve details to be pulished to the users
    """
    def get_available_main_types(self, order=None):##
        """ Get a list of main types
        Args:
            is_available_only: Whether to only include available mains (bool)
            order: order of the user (Order OR None)
            
            If order is not None, the returned list will take account of the ingredient availability when switching main

        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"

        Returns:
            List of mains (List<Main>)
        """
        if order is not None:
            self._check_order(order)
        temp_stock = merge_stock(self.ingredient_stock, order.get_ingredient_consumption(product_types=ProductForMain) if order is not None else [])
        return [m for m in self.main_types if m.get_default_products(temp_stock)]

    def get_main_types_and_availability(self, order=None):
        if order is not None:
            self._check_order(order)
        temp_stock = merge_stock(self.ingredient_stock, order.get_ingredient_consumption(product_types=ProductForMain) if order is not None else [])
        return [(m, True if m.get_default_products(temp_stock) else False) for m in self.main_types]

    def get_available_standard_mains(self, is_available_only= False, order=None):
        """ Get a list of available standard mains
        Args:
            order: order of the user (Order OR None) (default: None)
        
        If order is None, available standard mains regardless of main type are returned,
        else only the available standard mains of the main type order is returned

        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"

        Returns:
            List of available standard mains (List<StandardMain>)
        """
        if order is not None:
            self._check_order(order)
        return [sm for sm in self.standard_mains \
            if (order is None or sm.main_type == order.main_type) and \
                    is_contain_stock(merge_stock(self.ingredient_stock, order.get_ingredient_consumption(product_types=ProductForMain) if order is not None else []), sm.get_ingredient_consumption())]

    def get_standard_mains_and_availability(self, order=None):
        """ Get a list of standard main and whether they are available
        Args:
            order: order of the user (Order OR None) (default: None)
        
        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"

        Returns:
            List of all standard mains and their availability (List<(StandardMain, bool)>)
        """
        if order is not None:
            self._check_order(order)
        temp_stock = merge_stock(self.ingredient_stock, order.get_ingredient_consumption(product_types=ProductForMain) if order is not None else [])
        return [(sm, is_contain_stock(temp_stock, sm.get_ingredient_consumption())) 
            for sm in self.standard_mains \
            if (order is None or sm.main_type == order.main_type)]

    def get_available_product_quantities(self, is_available_only= False, order=None, product_types=Product):##
        """ Get a list of products and their quantities
        Args:
            is_available_only: Whether to only include available products (bool) (default: False)
            order: order of the user (Order OR None) (default: None)
        
        If order is None, the returned quantities would also include the already ordered products, 
        but exclude the ProductForMain which are not allowed to be added to the selected main

        Note that since some products share the same ingredient, once a product is selected, 
        the availability of other product(s) might reduce

        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"
            - IncorrectTypeException: "product_type"
            - IncorrectValueException: "product_type"

        Returns:
            List of product and its available quantities (List<(Product, int)>)
        """
        self._check_product_types(product_types)
        if order is not None:
            self._check_order(order)
        a =  [(p, p.get_available_quantity(self.ingredient_stock)+(order.get_quantity_of_product(p) if order is not None else 0)) \
            for p in self.products \
                if isinstance(p, product_types) and \
                    (order is None or order.is_product_allowed(p)) and \
                    (not is_available_only or p.is_available(self.ingredient_stock) or (order is not None and p in order.product))]

        return a
    # def get_ingredient_quantity(self, ingredient):
    #     """ Get the quantity of the ingredient in the stock
    #     Args:
    #         is_available_only: Whether to only include available products (bool) (default: False)
    #         order: order of the user (Order OR None) (default: None)
        
    #     If order is None, the returned quantities would also include the already ordered products
    #     Returns:
    #         List of product and its available quantities (List<(Product, int)>)
    #     """
    #     if isinstance(ingredient, str):
    #         return self._dict_ingredient_stock[ingredient]  
    #     else:
    #         return self._dict_ingredient_stock[ingredient.name]       

    """
        END: Retrieve details to be pulished to the users
    """

    """
        Order: Creation -> Checkout
    """
    @_SessionDecorator.save_session_wrapper
    def create_order(self):##
        """ Create an order
        The order is assigned with a different
        Returns:
            A newly created order with state 'creating' (Order)
        """
        new_order = Order(id=self._order_id_generator.generate_id([o.id for o in self.orders]))
        self._dict_orders.update({new_order.id: new_order})
        return new_order

    @_SessionDecorator.save_session_wrapper
    def select_main_type(self, order, main_type): ##
        """ Choose / Change the main type of the order
        Args:
            order: The order for which the change is initiated (Order)
            main_type: The main type to be changed to (str OR MainType)
        
        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"
            - IncorrectTypeException: "main_type"
            - NotFoundException: "main_type"
            - IncorrectOrderStatusException: "order"
            * NotEnoughStockException: "main_type"
        """
        self._check_when_selecting_main(order, main_type)
        main_type = self.get_main_type(main_type) # To convert str to MainType if necessary
        
        sub_stock = order.select_main_type(main_type, self.ingredient_stock)
        new_stock = cancel_stock(self.ingredient_stock, sub_stock, remove_zero=False)
        self._set_ingredient_stock(new_stock)
    
    @_SessionDecorator.save_session_wrapper
    def select_standard_main(self, order, standard_main):
        """ Choose / Change the standard main in the beginning of creation
        Args:
            order: The order for which the change is initiated (Order)
            main_type: The main type to be changed to (str OR StandardMain)
        
        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"
            - IncorrectTypeException: "standard_main"
            - NotFoundException: "standard_main"
            - IncorrectOrderStatusException: "order"
            - MainTypeNotSelectedException: "standard_main"
            - NotAllowedForMainTypeException: "standard_main"
            * NotEnoughStockException: "standard_main"
        """
        self._check_when_selecting_standard_main(order, standard_main)

        standard_main = self.get_standard_main(standard_main)
        original_ingredint_consumption_for_main = order.get_ingredient_consumption(product_types=ProductForMain)
        order.remove_products(product_types=ProductForMain)
        
        for p,q in standard_main.product_quantities:
            order.set_product(p, q)
        stock_change = cancel_stock(original_ingredint_consumption_for_main, standard_main.get_ingredient_consumption())
        self._set_ingredient_stock(merge_stock(self.ingredient_stock, stock_change, remove_zero=False))
        
    @_SessionDecorator.save_session_wrapper
    def order_product(self, order, product, quantity):
        """ Change the preferred product quantity
        Args:
            order: The order for which the change is initiated (Order)
            product: The product whose quantity to be changed (str OR Product)
            quantity: The amount of the product preferred (int)
        
        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"

            - IncorrectTypeException: "product"
            - NotFoundException: "product"

            - IncorrectTypeException: "quantity"
            - IncorrectValueException: "quantity"

            - IncorrectOrderStatusException: "order"

            - MainTypeNotSelectedException: "product"

            - NotAllowedForMainTypeException: "product"

            * ExceedLimitException: "product"
            * NotEnoughStockException: "product"
        """
        self._check_when_ordering_product(order, product, quantity)
        product = self.get_product(product)
        new_stock = cancel_stock(self.ingredient_stock, \
            order.set_product(product , quantity), remove_zero=False)
        self._set_ingredient_stock(new_stock)

    @_SessionDecorator.save_session_wrapper
    def cancel_order(self, order): ##
        """ Cancel the order
        Args:
            order: The order to be cancelled (Order)

        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"
        """
        self._check_when_cancelling_order(order)
        self._dict_orders.pop(order.id)
        self._set_ingredient_stock(merge_stock(self.ingredient_stock, order.get_ingredient_consumption()))
    
    """
        END: Order: Creation -> Checkout
    """
    """
        Order: Checkout -> Ready -> Picked up
    """
    def check_errors_for_checkout(self, order):
        """ Check the possible errors before checkout. There might be multiple errors and thus a list of errors is returned
        Args:
            order: Order of the customer (Order)

        Returns:
            List of exceptions that does not meet the checkout requirement (List<(BasicException)>)
            If system.checkout(order) is called, it will definitely raise an exception if the returned list of this function is not empty
        """
        self._check_order(order)
        if order.status != Order.STATUS_CREATING:
            raise IncorrectOrderStatusException("order", f"Order that is not in {Order.STATUS_CREATING} status cannot be set to {Order.STATUS_CHECKOUT}")
        
        err = []
        for t in (Base, MajorFilling, MinorFilling):
            product_quantities = order.get_product_quantities(t)
            if order.main_type is None:
                err.append(MainTypeNotSelectedException("main_type", "You must select a main type before checkout"))
            # ensures the number of selection of such product type is within limit
            elif not order.main_type.is_num_selections_within_limits([p for p,_ in product_quantities], t):
                current_num_selection = len(order.get_product_quantities(t))
                err.append(ExceedLimitException("product", f"""There are {"only" if order.main_type.selection_ranges.get(t, (0,0))[0] > current_num_selection else "already"} {current_num_selection} \
                number of selections of {t.key_str()} for your order, \
                which does not meet the limit range of min:{order.main_type.selection_ranges[t][0]}, max:{order.main_type.selection_ranges[t][1]}."""))
            
            # ensures the total quantities of such product type is within limit
            elif not order.main_type.is_quantities_within_limits(product_quantities, t):
                current_quantity = sum([q for p,q in product_quantities])
                err.append(ExceedLimitException("product", f"""There are {"only" if order.main_type.quantity_ranges.get(t, (0,0))[0] > current_quantity else "already"} {current_quantity} \
                    of {t.key_str()} for your order, \
                    which does not meet the limit range of min:{order.main_type.selection_ranges[t][0]}, max:{order.main_type.selection_ranges[t][1]}."""))
        return err

    @_SessionDecorator.save_session_wrapper
    def checkout(self, order): ##
        """ Checkout the order
        Args:
            order: The order to be checkouted (Order)
        
        Raises:
            - IncorrectTypeException: "order"
            - NotFoundException: "order"

            - IncorrectOrderStatusException: "order"
            * ExceedLimitException: "product"

        Returns:
            ID for the corresponding order (str)
        """
        self._check_when_checkout(order)
        order.checkout()

    @_SessionDecorator.save_session_wrapper
    def set_order_ready_to_serve(self, staff_code, order):
        """ Inform the system that the order is ready to serve
        Args:
            order: The order to be ready to serve (Order)

        Raises:
            - IncorrectTypeException: "staff_code"
            * NotFoundException: "staff_code"
            - IncorrectTypeException: "order"
            - NotFoundException: "order"

            - IncorrectOrderStatusException: "order"
        """
        self._check_when_ready_to_serve(staff_code, order)
        order.status = Order.STATUS_READY
    
    @_SessionDecorator.save_session_wrapper
    def set_order_picked_up(self, staff_code, order):
        """ Inform the system that the order is ready to serve
        Args:
            order: The order to be ready to serve (Order)
        
        Raises:
            - IncorrectTypeException: "staff_code"
            * NotFoundException: "staff_code"
            - IncorrectTypeException: "order"
            - NotFoundException: "order"

            - IncorrectOrderStatusException: "order"
        """
        self._check_when_order_picked_up(staff_code, order)
        order.status = Order.STATUS_PICKED_UP


    def search_order(self, order_id):
        """ Get the order based on the order id
        Args:
            order_id: ID of the order (str)
        Raises:
            - IncorrectTypeException: "order_id"
            * NotFoundException: "order_id"
        Returns:
            The corresponding order (Order)
        """
        self._check_when_search_order(order_id)
        return self.dict_orders.get(order_id, None)
        

    def search_orders(self, staff_code, status=None, excluded_status=()):
        """ Get a list of orders with the corresponding status
        Args:
            staff_code: Staff ID (str)
            status: The status of the order (str)
        Raises:
            - IncorrectTypeException: "staff_code"
            * NotFoundException: "staff_code"
            - IncorrectTypeException: "status"
            - IncorrectValueException: "status"
        Returns:
            List of orders which satisfy the status (List<Order>)
        """
        self._check_when_search_orders(staff_code, status)
        excluded_status = excluded_status if isinstance(excluded_status, (tuple,list)) else (excluded_status, )
        if status == None:
            return [c for c in self.orders if c.status not in excluded_status]
        else:
            return [c for c in self.orders if c.status == status and c.status not in excluded_status] 

    """
        END: Order: Checkout -> Ready -> Picked up
    """

    """
        Ingredient stock: Modification
    """
    @_SessionDecorator.save_session_wrapper
    def modify_stock(self, staff_code, ingredient_stock_change):
        """ Increase the stock of the corresonding ingredient
        Args:
            staff_code: Staff ID (str)
            ingredient_stock_change: Ingredient and its quantity change in stock (List<(str OR Ingredient, int)>)
        Raises:
            - IncorrectTypeException: "staff_code"
            * NotFoundException: "staff_code"
            - IncorrectTypeException: "ingredient"
            - NotFoundException: "ingredient"
            - IncorrectTypeException: "quantity"
            * IncorrectValueException: "quantity"
        """
        for i,q in ingredient_stock_change:
            self._check_when_modify_stock(staff_code, i, q)
        stock_change = []
        for i,q in ingredient_stock_change:
            stock_change = merge_stock(stock_change, ((self.get_ingredient(i), q),))
        self._set_ingredient_stock(merge_stock(self.ingredient_stock, stock_change, remove_zero=False))
    
    """
        END: Ingredient stock: Modification
    """
    """
        Staff management
    """
    def is_staff_exist(self, staff_code):
        """ Check if the staff code has been registered
        Args:
            staff_code: Staff ID (str)
        Returns:
            True if the staff code is registered on the system (bool)
        """
        return self._staff_manager.is_exist(staff_code)
    """
        END: Staff management
    """


    """
        Parameters checking + Action validity checking. 
        If error is encountered, error will be raised
    """
    @staticmethod
    def _check_type_error(item, item_name, types): ##
        if not isinstance(item, types):
            types = types if isinstance(types, tuple) else (types,)
            raise IncorrectTypeException(item_name, f"{item_name} {item} is not of type(s) {concat_type_string(types)}")
    
    @staticmethod
    def _check_if_registered(item, item_name, dict_type_cond): ##
        cond_func = dict_type_cond.get(type(item))
        if not cond_func or not cond_func(item):
            raise NotFoundException(item_name, f"{item_name} {item} is not registered")

    def _check_product_types(self, product_types):
        item_name = "product_type"
        if not isinstance(product_types, tuple):
            product_types = (product_types, )
        for pt in product_types:
            self._check_type_error(pt, item_name, type)
            if not issubclass(pt, Product):
                raise IncorrectValueException("product_type", f"{pt} is not a subclass of Product")
         
    def _check_ingredient(self, ingredient): ##
        item_name = "ingredient"
        self._check_type_error(ingredient, item_name, (Ingredient, str))
        self._check_if_registered(ingredient, item_name, {
            Ingredient: lambda x: x in self.ingredients,
            str: lambda x:  self.get_ingredient(x)
        })

    def _check_order(self, order): ##
        item_name = "order"
        self._check_type_error(order, item_name, (Order, str))
        self._check_if_registered(order, item_name, {
            Order: lambda x: x in self.orders,
            str: lambda x:  self.dict_orders.get(x, False)
        })

    def _check_main_type(self, main_type): ##
        item_name = "main_type"
        self._check_type_error(main_type, item_name, (MainType, str))
        self._check_if_registered(main_type, item_name, {
            MainType: lambda x: x in self.main_types,
            str: lambda x: self.get_main_type(x)
        })

    def _check_standard_main(self, standard_main): ##
        item_name = "standard_main"
        self._check_type_error(standard_main, item_name, (StandardMain, str))
        self._check_if_registered(standard_main, item_name, {
            StandardMain: lambda x: x in self.standard_mains,
            str: lambda x: self.get_standard_main(x)
        })
    
    def _check_product(self, product): ##
        item_name = "product"
        self._check_type_error(product, item_name, (Product, str))
        self._check_if_registered(product, item_name, {
            Product: lambda x: x in self.products,
            str: lambda x:  self.get_product(x)
        })

    def _check_quantity(self, quantity): ##
        item_name = "quantity"
        self._check_type_error(quantity, item_name, int)
        if quantity < 0:
            raise IncorrectValueException(item_name, f"quantity must be greater than 0")

    def _check_staff_code(self, staff_code): ##
        item_name = "staff_code"
        self._check_type_error(staff_code, item_name, str)
        self._check_if_registered(staff_code, item_name, {
            str: lambda x: self._staff_manager.is_exist(x)
        })
    
    
    def _check_when_selecting_main(self, order, main_type):
        self._check_order(order)
        self._check_main_type(main_type)

        if order.status != Order.STATUS_CREATING:
            raise IncorrectOrderStatusException("order", f"Order that is not in {Order.STATUS_CREATING} status cannot select main")
        
        main_type = self.get_main_type(main_type)
        temp_available_stock = merge_stock(self.ingredient_stock, order.get_ingredient_consumption(product_types=ProductForMain))
        if not main_type.get_default_ingredient_consumption(temp_available_stock):
            raise NotEnoughStockException("main_type", f"Sorry, there are not enough stock to produce minimal {main_type}")

    def _check_when_selecting_standard_main(self, order, standard_main):
        self._check_order(order)
        self._check_standard_main(standard_main)
        standard_main = self.get_standard_main(standard_main)
        if order.status != Order.STATUS_CREATING:
            raise IncorrectOrderStatusException("order", f"Order that is not in {Order.STATUS_CREATING} status cannot select standard main")

        if order.main_type == None:
            raise MainTypeNotSelectedException("standard_main", f"Standard main cannot be selected until a main type has been chosen.")
        
        if order.main_type != standard_main.main_type:
            raise NotAllowedForMainTypeException("standard_main", f"{standard_main} cannot be chosen since the selected main type is {order.main_type}")
        
        temp_available_stock = merge_stock(order.get_ingredient_consumption(product_types=ProductForMain), self.ingredient_stock)
        if not is_contain_stock(temp_available_stock, standard_main.get_ingredient_consumption()):
            raise NotEnoughStockException("standard_main", f"Sorry, there are not enough stock for {standard_main}")
    
    def _check_when_ordering_product(self, order, product, quantity):
        self._check_order(order)
        self._check_product(product)
        self._check_quantity(quantity)

        if order.status != Order.STATUS_CREATING:
            raise IncorrectOrderStatusException("order", f"Order that is not in {Order.STATUS_CREATING} status cannot configure the products")

        # Take special care on ProductForMain
        product = self.get_product(product)
        if isinstance(product, ProductForMain):
            # main type must have been selected
            if not order.main_type:
                raise MainTypeNotSelectedException("main_type", "No base and filling for main can be added until 1 main type has been selected")

            # main type must allow such product
            if not order.main_type.is_product_allowed(product):
                raise NotAllowedForMainTypeException("product", f"{product} cannot go onto {order.main_type}")

            # !!Only check the upper limit
            temp_product_quantities = merge_stock([(p,q) for p,q in order.product_quantities if p != product], [(product, quantity)])

            # ensures the number of selection of such product type is within limit
            if not order.main_type.is_num_selections_within_limits(temp_product_quantities, type(product), upper_only=True):
                current_num_selection = len(order.get_product_quantities(type(product)))
                raise ExceedLimitException("product", f"There are already {current_num_selection} \
                    number of selections of {product.key_str() + ('' if current_num_selection<=1 else 's')} for your order, \
                    which has a upper cap of {order.main_type.selection_ranges.get(type(product), (0,'infinity'))[1]}. Therefore, you cannot select more of this.")
            
            # # ensures the total quantities of such product type is within limit
            if not order.main_type.is_quantities_within_limits(temp_product_quantities, type(product),  upper_only=True):
                current_quantity = sum([q for p,q in order.get_product_quantities(type(product))])
                diff = quantity-current_quantity
                raise ExceedLimitException("product", f"There are already {current_quantity} \
                     {product.key_str() + ('' if current_quantity<=1 else 's')} for your order, \
                    which has a upper cap of {order.main_type.quantity_ranges.get(type(product), (0,'infinity'))[1]}. Therefore, you cannot select {str(abs(diff)) + (' extra more ' if diff > 0 else ' fewer ')} of this.")
        
        # ensures there is enough stock to product extra products
        original_quantity = order.get_quantity_of_product(product)
        diff = quantity-original_quantity
        temp_ingredient_consumption = product.get_ingredient_consumption(diff)
        if not is_contain_stock(self.ingredient_stock, temp_ingredient_consumption):
            raise NotEnoughStockException("product", f"Sorry, there are not enough stock for extra {diff} {product}")
        

    def _check_when_cancelling_order(self, order): ##
        self._check_order(order)

    def _check_when_checkout(self, order):
        self._check_order(order)
        if order.status != Order.STATUS_CREATING:
            raise IncorrectOrderStatusException("order", f"Order that is not in {Order.STATUS_CREATING} status cannot be set to {Order.STATUS_CHECKOUT}")
        
        
        for t in (Base, MajorFilling, MinorFilling):
            product_quantities = order.get_product_quantities(t)

            # ensures the number of selection of such product type is within limit
            if not order.main_type.is_num_selections_within_limits([p for p,_ in product_quantities], t):
                current_num_selection = len(order.get_product_quantities(t))
                raise ExceedLimitException("product", f"""There are already {current_num_selection} \
                number of selections of {t.key_str()} for your order, \
                which has a limit range of {order.main_type.selection_ranges.get(t, 0)}.""")
            
            # ensures the total quantities of such product type is within limit
            elif not order.main_type.is_quantities_within_limits(product_quantities, t):
                current_quantity = sum([q for p,q in product_quantities])
                raise ExceedLimitException("product", f"""There are already {current_quantity} \
                    of {t.key_str()} for your order, \
                        which has a limit range of {order.main_type.quantity_ranges.get(t, 0)}.""")
        

    def _check_when_ready_to_serve(self, staff_code, order): ##
        self._check_staff_code(staff_code)
        self._check_order(order)
        if order.status != Order.STATUS_CHECKOUT:
            raise IncorrectOrderStatusException("order", f"Order that is not in {Order.STATUS_CHECKOUT} status cannot be set to {Order.STATUS_READY}")
    
    def _check_when_order_picked_up(self, staff_code, order): ##
        self._check_staff_code(staff_code)
        self._check_order(order)
        if order.status != Order.STATUS_READY:
            raise IncorrectOrderStatusException("order", f"Order that is not in {Order.STATUS_READY} status cannot be set to {Order.STATUS_PICKED_UP}")

    def _check_when_search_order(self, order_id):
        item_name = "order_id"
        self._check_type_error(order_id, item_name, str)
        self._check_if_registered(order_id, item_name, {
            str: lambda x: self.dict_orders.get(x, False)
        })

    def _check_when_search_orders(self, staff_code, status):
        self._check_staff_code(staff_code)
        if status is not None:
            self._check_type_error(status, "status", (type(Order.STATUS_CHECKOUT)))
            if status not in Order.all_status():
                raise IncorrectValueException("status", f"'{status}' is not valid value of STATUS")

    def _check_when_modify_stock(self, staff_code, ingredient, quantity):
        self._check_staff_code(staff_code)
        self._check_ingredient(ingredient)
        self._check_type_error(quantity, "quantity", int)
        
        ingredient = self.get_ingredient(ingredient)
        quantity = int(quantity)
        current_stock = self.dict_ingredient_stock[ingredient.name][1]
        if current_stock + quantity < 0:
            raise IncorrectValueException("quantity", f"""Current stock for {ingredient.name} is {current_stock} {ingredient.unit}(s), \
                but you want to change it by {quantity} {ingredient.unit}(s), which will result in {current_stock+quantity} {ingredient.unit}(s) which is fewer than 0""")
        

    
    """
        Parameter checking ends
    """

    """
    For system initialization only. Correct parameters are assumed
    """
    def set_ingredient_stock(self, ingredient_quantity_pairs):
        for i,p in ingredient_quantity_pairs:
            self._dict_ingredient_stock.update({i.name: (i,p)})
        
    
    
    def set_products(self, product_ingredient_consumption_pairs):
        for p, ic in product_ingredient_consumption_pairs:
            converted_ic = [(self._dict_ingredient_stock[i][0] if isinstance(i, str) else i, q) for i, q in ic]
            p.ingredient_consumption = converted_ic
            self._dict_products.update({p.name: p})
    
    

    def set_main_types(self, main_type_product_list_pairs):
        for m, pl in main_type_product_list_pairs:
            m.product_choices = [(self._dict_products[p] if isinstance(p, str) else p) for p in pl]
            self._dict_main_types.update({m.name: m})
    
    
    def set_staff_codes(self, staff_codes):
        self._staff_manager.staff_codes = staff_codes

    # def set_ingredient_stock_with_instantiation(self, tuples_name_unit_initQuantity):
    #     """ Set ingredients with parameters without pre-instantiation
    #         tuples_name_unit_initQuantity: List<(name, unit, initQuantity)>
    #                                                 List<(str, str, int)>
    #     """
    #     for n,u,q in tuples_name_unit_initQuantity:
    #         self._dict_ingredient_stock.update({n: (Ingredient(n, u), q)})

    # def set_products_with_instantiation(self, tuples_name_price_ingredientConsumption):
    #     """ Set products with parameters without pre-instantiation
    #         tuples_name_price_ingredientConsumption: List<(name, price, product_choice:List<(ingredient, int)>)>
    #                                                 List<(str, int, List<(str, int)>)>
    #     """
    #     for name, price, ic in tuples_name_price_ingredientConsumption:
    #         converted_ic = [(self._dict_ingredient_stock[i][0] if isinstance(i, str) else i, q) for i, q in ic]
    #         product = Product(name, price, converted_ic)
    #         self._dict_products.update({name: product})

    # def set_main_types_with_instantiation(self, tuples_name_basePrice_productChoices):
    #     """ Set main types with parameters without pre-instantiation
    #         tuples_name_basePrice_productChoices: List<(name, basePrice, product_choice:List<product>)>
    #                                                 List<(str, int, List<str>)>
    #     """
    #     for name, base_price, pc in tuples_name_basePrice_productChoices:
    #         converted_pc = [(self._dict_products[p] if isinstance(p, str) else p) for p in pc]
    #         main_type = MainType(name, base_price, converted_pc)
    #         self._dict_main_types.update({name: main_type})

    def set_standard_mains_with_instantiation(self, tuples_name_mainType_productQuantities):
        """ Set standard mains with parameters without pre-instantiation
            tuples_name_mainType_productQuantities: List<(name, mainType, product_quantities:List<(product, quantity)>)>
                                                    List<(str, str, List<(str, int)>)>
        """
        for name, main_type, pq in tuples_name_mainType_productQuantities:
            converted_main_type = self.get_main_type(main_type)
            converted_pq = [(self._dict_products[p] if isinstance(p, str) else p, q) for p, q in pq]
            standard_main = StandardMain(name, converted_main_type, converted_pq)
            self._dict_standard_mains.update({name: standard_main})

    def _set_ingredient_stock(self, new_stock):
        self._dict_ingredient_stock = {}
        for i, q in new_stock:
            self._dict_ingredient_stock.update({i.name: (i, q)})
    

    """
        Properties
    """
    @property
    def dict_ingredient_stock(self):
        return self._dict_ingredient_stock
    
    @property
    def ingredient_stock(self):
        return list(self._dict_ingredient_stock.values())
    
    @property
    def ingredients(self):
        return [c[0] for c in self.ingredient_stock]
    
    @property
    def dict_products(self):
        return self._dict_products.copy()

    @property
    def products(self):
        return list(self._dict_products.values())
    

    @property
    def dict_main_types(self):
        return self._dict_main_types

    @property
    def main_types(self):
        return list(self._dict_main_types.values())

    @property
    def dict_standard_mains(self):
        return self._dict_standard_mains

    @property
    def standard_mains(self):
        return list(self._dict_standard_mains.values())

    @property
    def dict_orders(self):
        return self._dict_orders

    @property
    def orders(self):
        return list(self._dict_orders.values())

    @property
    def staff_codes(self):
        return self._staff_manager.staff_codes
    
    
    # @ingredient_stock.setter
    # def ingredient_stock(self, new_stock):
    #     self._dict_ingredient_stock = {}
    #     for i, q in new_stock:
    #         self._dict_ingredient_stock.update({i.name: (i, q)})
