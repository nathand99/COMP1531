import file_path
from test_system import get_ingredient_stock, get_products, get_main_types, sys
import pytest
from order import *
from online_order_system import *
# WARNING: This file is highly coupled to test_system.py. No change should be applied on test_system

def test_order_creation(sys):
    order = sys.create_order()
    assert len(sys.orders) == 1
    assert order == sys.orders[0]
    assert order.status == Order.STATUS_CREATING
    assert order.main_type == None
    assert order.product_quantities == []

    order2 = sys.create_order()
    assert len(sys.orders) == 2
    assert order == sys.orders[0]
    assert order2 == sys.orders[1]
    assert order2.status == Order.STATUS_CREATING
    assert order2.main_type == None
    assert order2.product_quantities == []

def test_select_main_success(sys):
    
    assert len(sys.main_types) == 2
    assert len(sys.get_available_main_types()) == 2
    assert "burger" in [m.name for m in sys.main_types]
    assert "wrap" in [m.name for m in sys.main_types]

    # Test: Select main type initially
    # Create an order and select check out the available mains, then select burger
    # Assumes at least 1 burger is allowed to be made, which should consists of at least 1 Base and 1 MajorFilling
    order = sys.create_order()
    main_type = sys.get_main_type("burger")
    sys.select_main_type(order, main_type)
    assert order.main_type.name == "burger"
    assert (sys.get_product("white bun"),2) in order.product_quantities
    assert (sys.get_product("beef patty"),1) in order.product_quantities # beef patty goes before shredded chicken breast
    assert sys.dict_ingredient_stock["white bun"][1] == 0
    assert sys.dict_ingredient_stock["beef patty"][1] == 1

    # Test: Change main type
    main_type = sys.get_main_type("wrap")
    sys.select_main_type(order, main_type)
    assert order.main_type.name == "wrap"
    # All the products belonging to ProductForMain are removed if the main type is switched 
    # since these products only belongs to the previous main type. And default ProductForMain of new main type is added
    assert (sys.get_product("white bun"), 2) not in order.product_quantities
    assert (sys.get_product("beef patty"), 1) not in order.product_quantities
    assert (sys.get_product("white bun"), 0) not in order.product_quantities
    assert (sys.get_product("beef patty"), 0) not in order.product_quantities
    assert (sys.get_product("white flat bread"),1) in order.product_quantities
    assert (sys.get_product("shredded chicken breast 100g"),1) in order.product_quantities
    assert sys.dict_ingredient_stock["white bun"][1] == 2
    assert sys.dict_ingredient_stock["beef patty"][1]== 2
    assert sys.dict_ingredient_stock["white flat bread"][1] == 0
    assert sys.dict_ingredient_stock["shredded chicken breast"][1] == 300

def test_select_main_fail(sys):
    # Test Unable to select main if there is not enough ingredient to produce a minimum main course
    # There are only 1 piece of flat bread in stock originally so only 1 wrap is allowed
    num_orders = 5
    main_type = sys.get_main_type("wrap")
    orders = [sys.create_order() for i in range(num_orders)]
    for i in range(num_orders):
        try:
            sys.select_main_type(orders[i], main_type)
        except NotEnoughStockException as e:
            if i <= 0:
                assert False

def test_select_ingredient_for_main_success(sys):
    order = sys.create_order()
    main_type = sys.get_main_type("burger")
    sys.select_main_type(order, main_type)
    
    # Test: increase number of patty
    assert sys.dict_ingredient_stock["beef patty"][1] == 1
    assert (sys.get_product("white bun"), 2) in order.product_quantities 
    assert (sys.get_product("beef patty"), 1) in order.product_quantities 

    sys.order_product(order, "beef patty", 2)
    assert sys.dict_ingredient_stock["beef patty"][1] == 0
    assert (sys.get_product("white bun"), 2) in order.product_quantities 
    assert (sys.get_product("beef patty"), 2) in order.product_quantities 

    # Test: add other MajorFilling
    sys.order_product(order, "shredded chicken breast 100g", 1)
    assert sys.dict_ingredient_stock["beef patty"][1] == 0
    assert sys.dict_ingredient_stock["shredded chicken breast"][1] == 300
    assert (sys.get_product("white bun"), 2) in order.product_quantities 
    assert (sys.get_product("beef patty"), 2) in order.product_quantities 
    assert (sys.get_product("shredded chicken breast 100g"), 1) in order.product_quantities 

    # Test: Add minor filling
    sys.order_product(order, "tomato sauce", 1)
    assert sys.dict_ingredient_stock["tomato sauce"][1] == 90
    assert (sys.get_product("white bun"), 2) in order.product_quantities 
    assert (sys.get_product("shredded chicken breast 100g"), 1) in order.product_quantities 
    assert (sys.get_product("tomato sauce"), 1) in order.product_quantities
    
    sys.order_product(order, "lettuce slaw", 2)
    assert sys.dict_ingredient_stock["lettuce"][1] == 20
    assert (sys.get_product("white bun"), 2) in order.product_quantities 
    assert (sys.get_product("shredded chicken breast 100g"), 1) in order.product_quantities 
    assert (sys.get_product("tomato sauce"), 1) in order.product_quantities 
    assert (sys.get_product("lettuce slaw"), 2) in order.product_quantities 

def test_select_ingredient_for_main_fail(sys):
    order = sys.create_order()
    main_type = sys.get_main_type("burger")
    sys.select_main_type(order, main_type)

    # Test add topping exceeds stock
    
    sys.order_product(order, "shredded chicken breast 100g", 0)
    try:
        sys.order_product(order, "beef patty", 3)
    except NotEnoughStockException:
        pass
    else:
        assert False
    assert sys.dict_ingredient_stock["beef patty"][1] == 1
    assert (sys.get_product("beef patty"), 1) in order.product_quantities 

    # Test add topping exceeds limit
    try:
        sys.order_product(order, "shredded chicken breast 100g", 3)
    except ExceedLimitException:
        pass
    else:
        assert False
    assert sys.dict_ingredient_stock["tomato sauce"][1] == 100
    assert (sys.get_product("tomato sauce"), 2) not in order.product_quantities 
    assert (sys.get_product("tomato sauce"), 0) not in order.product_quantities

def test_add_sides_success(sys):
    order = sys.create_order()
    # Test: add side of fries
    sys.order_product(order, "medium fries", 1)
    assert sys.dict_ingredient_stock["fries"][1] == 125
    assert sys.dict_ingredient_stock["tomato sauce"][1] == 90
    assert (sys.get_product("medium fries"), 1) in order.product_quantities

	# Test: add side of nuggets
    sys.order_product(order, "6 piece chicken nuggets", 1)
    assert sys.dict_ingredient_stock["chicken nugget"][1] == 94
    assert (sys.get_product("6 piece chicken nuggets"), 1) in order.product_quantities

	# Test: add a drinksys.order_product(order, "medium Greedy Coke", 1)
    sys.order_product(order, "medium Greedy Coke", 1)
    assert sys.dict_ingredient_stock["Greedy Coke"][1] == 150
    assert (sys.get_product("medium Greedy Coke"), 1) in order.product_quantities

def test_add_sides_fail(sys):
    order = sys.create_order()
    try:
        sys.order_product(order, "medium fries", 3)
    except NotEnoughStockException:
        pass
    else:
        assert False
    assert sys.dict_ingredient_stock["fries"][1] == 200
    assert sys.dict_ingredient_stock["tomato sauce"][1] == 100
    assert (sys.get_product("medium fries"), 0) not in order.product_quantities

	
