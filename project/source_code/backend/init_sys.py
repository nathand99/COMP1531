from online_order_system import *
from product import *
from ingredient import *
from standard_main import *
def get_init_sys():
    sys = OnlineOrderSystem()
    sys.set_ingredient_stock(get_ingredient_stock())
    sys.set_products(get_products())
    sys.set_main_types(get_main_types())
    sys.set_standard_mains_with_instantiation(get_standard_mains_details())
    sys.set_staff_codes(get_staff_codes())
    return sys

def get_ingredient_stock():
    return [
        (Ingredient("white bun", "piece"), 4),
        (Ingredient("wheat bun", "piece"), 6),
        (Ingredient("white flat bread", "piece"), 1),
        (Ingredient("shredded chicken breast", "g"), 400),
        (Ingredient("beef patty", "piece"), 2),
        (Ingredient("lettuce", "g"), 80),
        (Ingredient("tomato", "g"), 300),
        (Ingredient("onion", "g"), 0),
        (Ingredient("tomato sauce", "g"), 100),
        (Ingredient("mustard", "g"), 50), 
        (Ingredient("fries", "g"), 200),
        (Ingredient("chicken nugget", "piece"), 100),
        (Ingredient("Greedy Coke", "ml"), 500),
        (Ingredient("coffee bean", "g"), 9)
    ]

def get_products():
    return [
        (Base("white bun", 1.1),  [("white bun", 1)]),
        (Base("wheat bun", 1.5), [("wheat bun", 1)]), 
        (Base("white flat bread", 2), [("white flat bread", 1)]),

        (MajorFilling("shredded chicken breast 100g", 5), [("shredded chicken breast", 100)]),
        (MajorFilling("beef patty", 3), [("beef patty",1)]),

        (MinorFilling("lettuce slaw", 1), [("lettuce", 30)]),
        (MinorFilling("tomato slice",1),  [("tomato", 30)]),
        (MinorFilling("onion shreds",1),  [("onion", 20)]),
        (MinorFilling("tomato sauce", 0.5),  [("tomato sauce", 10)]),
        (MinorFilling("mustard", 0.5), [("mustard",10)]), 

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
                minor_filling_quantity_range=(0,8), base_price=1),\
            ["white bun", "wheat bun", "beef patty", "shredded chicken breast 100g", "lettuce slaw", "tomato slice", "onion shreds", "tomato sauce", "mustard"]),
        (MainType("wrap", 0, base_selection_range=(1,1), base_quantity_range=(1,1), \
                major_filling_selection_range=(1,3), major_filling_quantity_range=(1,4), \
                minor_filling_quantity_range=(0,10), base_price=1),\
             ["white flat bread", "shredded chicken breast 100g", "lettuce slaw", "tomato slice", "onion shreds", "tomato sauce"])
    ]

def get_standard_mains_details():
    return [
        ("Big Mac","burger", [("white bun", 3), ("beef patty",2), ("lettuce slaw", 2), ("tomato slice",2), ("tomato sauce",2)]),
        ("Shreddy Burger", "burger", [("wheat bun",2), ("shredded chicken breast 100g", 2), ("lettuce slaw",2), ("mustard",3)]),
        ("Healthy wrap", "wrap", [("white flat bread",2), ("shredded chicken breast 100g",3), ("lettuce slaw",3), ("onion shreds",2), ("tomato sauce",3)])
    ]

def get_staff_codes():
    return ["1234"]