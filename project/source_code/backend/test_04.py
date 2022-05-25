import file_path
import pytest
from util import *
from order import *
from online_order_system import *
from test_system import get_ingredient_stock, get_products, get_main_types, sys
from init_sys import get_ingredient_stock, get_products, get_main_types, get_standard_mains_details

@pytest.fixture
def sys():
    sys = OnlineOrderSystem()
    sys.set_ingredient_stock(get_ingredient_stock())
    sys.set_products(get_products())
    sys.set_main_types(get_main_types())
    sys.set_standard_mains_with_instantiation(get_standard_mains_details())
    sys.set_staff_codes("1234")
    return sys
    
def test_merge_stock():
    a = [(1,2), (3,4)]
    b = [(3,2), (4,5)]
    assert merge_stock(a,b) == [(1,2), (3,6), (4,5)]

def test_cancel_stock():
    a = [(1,2), (3,4)]
    b = [(3,2), (4,5)]
    assert cancel_stock(a,b) == [(1,2), (3,2), (4,-5)]

def test_is_contain_stock():
    a = [(1,2), (3,4)]
    b = [(3,4)]
    assert is_contain_stock(a,b)
    assert not is_contain_stock(b,a)
    
def test_modify_stock(sys):
    #there is 4 white buns when this system is initiated 
    assert(sys.dict_ingredient_stock["white bun"][1] == 4)
    #there are 300g of tomatos when system is initiated
    assert(sys.dict_ingredient_stock["tomato"][1] == 300)
    
    #increase "white bun" stock by 1
    sys.modify_stock("1234", [("white bun", 1)])
    assert(sys.dict_ingredient_stock["white bun"][1] == 5)
    
    #decrease "white bun" stock by 4
    sys.modify_stock("1234", [("white bun", -4)])
    assert(sys.dict_ingredient_stock["white bun"][1] == 1)
    
    #decrease "white bun" stock by 1
    sys.modify_stock("1234", [("white bun", -1)])
    assert(sys.dict_ingredient_stock["white bun"][1] == 0)
    
    #decrease "tomato" stock by 100
    sys.modify_stock("1234", [("tomato", -100)])
    assert(sys.dict_ingredient_stock["tomato"][1] == 200)
    
    #increase "tomato" stock by 100
    sys.modify_stock("1234", [("tomato", 100)])
    assert(sys.dict_ingredient_stock["tomato"][1] == 300)
    
    #stock cannot be negative. raises exception
    with pytest.raises(IncorrectValueException):
        sys.modify_stock("1234", [("white bun", -1)])
        sys.modify_stock("1234", [("tomato", -1000)])
    
    #can alter 2 or more ingredients stock at once
    sys.modify_stock("1234", [("white bun", 10),("tomato", 20)])
    assert(sys.dict_ingredient_stock["white bun"][1] == 10)
    assert(sys.dict_ingredient_stock["tomato"][1] == 320)
    
    #can alter 2 or more ingredients stock at once with no change
    sys.modify_stock("1234", [("white bun", 0),("tomato", 0)])
    assert(sys.dict_ingredient_stock["white bun"][1] == 10)
    assert(sys.dict_ingredient_stock["tomato"][1] == 320)
    
    #invalid staff code raises NotFoundException
    with pytest.raises(NotFoundException):
        sys.modify_stock("7890", [("white bun", 2)])
        sys.modify_stock("5463", [("tomato", -2)])
        
    #non existing ingredient raises NotFoundException
    with pytest.raises(NotFoundException):
        sys.modify_stock("1234", [("black bun", 2)])
        sys.modify_stock("1234", [("noningredient", -2)])
        sys.modify_stock("1234", [("apple", -2)])
        
    #invalid stock change raises IncorrectTypeException
    with pytest.raises(IncorrectTypeException):
        sys.modify_stock("1234", [("white bun", "hello")])
        sys.modify_stock("1234", [("white bun", "not a number")])
        sys.modify_stock("1234", [("white bun", nonnumber)])
        
