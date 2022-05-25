

from online_order_system import *
from ingredient import *
from main_type import *
from product import *
from order import *




def virgin_sys():
    return OnlineOrderSystem()


def sys():
    sys = OnlineOrderSystem()
    sys.set_ingredient_stock(get_ingredient_stock())
    sys.set_products(get_products())
    sys.set_main_types(get_main_types())
    return sys

def get_ingredient_stock():
    return [
        (Ingredient("white bun", "piece"), 2),
        (Ingredient("white flat bread", "piece"), 1),
        (Ingredient("shredded chicken breast", "g"), 400),
        (Ingredient("beef patty", "piece"), 2),
        (Ingredient("lettuce", "g"), 80),
        (Ingredient("tomato", "g"), 300),
        (Ingredient("onion", "g"), 0),
        (Ingredient("tomato sauce", "g"), 100),
        (Ingredient("fries", "g"), 200),
        (Ingredient("chicken nugget", "piece"), 100),
        (Ingredient("Greedy Coke", "ml"), 500),
        (Ingredient("coffee bean", "g"), 9)
    ]

def get_products():
    return [
        (Base("white bun", 1.1),  [("white bun", 1)]),
        (Base("white flat bread", 2), [("white flat bread", 1)]),

        (MajorFilling("shredded chicken breast 100g", 5), [("shredded chicken breast", 100)]),
        (MajorFilling("beef patty", 3), [("beef patty",1)]),

        (MinorFilling("lettuce slaw", 1), [("lettuce", 30)]),
        (MinorFilling("tomato slice",1),  [("tomato", 30)]),
        (MinorFilling("onion shreds",1),  [("onion", 20)]),
        (MinorFilling("tomato sauce", 0.5),  [("tomato sauce", 10)]),

        (Side("medium fries", 3.5),  [("fries", 75), ("tomato sauce", 10)]),
        (Side("large fries", 4.5), [("fries", 125), ("tomato sauce", 10)]),
        (Side("6 piece chicken nuggets", 6), [('chicken nugget', 6)]),
        (Side("10 piece chicken nuggets", 8), [('chicken nugget', 10)]),
        (Side("medium chicken salad", 7), [("lettuce", 70), ("shredded chicken breast", 50)]),
        
        (Drink("medium Greedy Coke", 3), [("Greedy Coke", 350)]),
        (Drink("large Greedy Coke", 5), [("Greedy Coke", 500)]),
        (Drink("small coffee", 3.5), [("coffee bean", 6)]),
        (Drink("medium coffee", 4.2), [("coffee bean", 8)]),
        (Drink("large coffee", 5), [("coffee bean", 10)]),
    ]

def get_main_types():
    return [
        (MainType("burger", 0, base_selection_range=(1,1), base_quantity_range=(2,4), \
                major_filling_selection_range=(1,2), major_filling_quantity_range=(1,3), \
                minor_filling_quantity_range=(0,5), base_price=1),\
            ["white bun", "beef patty", "shredded chicken breast 100g", "lettuce slaw", "tomato slice", "onion shreds", "tomato sauce"]),
        (MainType("wrap", 0, base_selection_range=(1,1), base_quantity_range=(1,1), \
                major_filling_selection_range=(1,3), major_filling_quantity_range=(1,4), \
                minor_filling_quantity_range=(0,5), base_price=1),\
             ["white flat bread", "shredded chicken breast 100g", "lettuce slaw", "tomato slice", "onion shreds", "tomato sauce"])
    ]

def get_staff_codes():
    return["1234"]
    
def _test_setup(virgin_sys):
    sys = virgin_sys
    ingredient_stock = get_ingredient_stock()
    sys.set_ingredient_stock(ingredient_stock)

    assert len(sys.ingredients) == len(ingredient_stock)
    for i,j in zip(sys.ingredients, ingredient_stock):
        assert i == j
    for i,j in zip(list(sys.dict_ingredient_stock.keys()), ingredient_stock):
        assert i == j[0].name
    

    
    products = get_products()
    sys.set_products(products)

    assert len(sys.products) == len(products)
    for i,j in zip(list(sys.products.values()), [p for (p,ic) in products]):
        assert i == j
    for i,j in zip(list(sys.products.keys()), [p for (p,ic) in products]):
        assert i == j.name 



    main_types = get_main_types()
    sys.set_main_types(main_types)

    assert len(sys.main_types) == len(main_types)
    for i,j in zip(list(sys.main_types.values()), [m for (m,p) in main_types]):
        assert i == j
    for i,j in zip(list(sys.main_types.keys()), [m for (m,p) in main_types]):
        assert i == j.name
        
    staff_codes = get_staff_codes()
    sys.set_staff_codes(staff_codes)
    
    assert len(sys.staff_codes) == len(staff_codes)
    
