import file_path
from test_system import get_ingredient_stock, get_products, get_main_types, sys
import pytest
from order import *
from online_order_system import *

#test the function search_orders
#this function allows staff to collect all orders which have a given status,
#all orders and all orders except orders of a given status
def test_search_orders(sys):
    STATUS_CREATING = "Creating"
    STATUS_CHECKOUT = "Checked out"
    STATUS_READY = "Ready"
    STATUS_PICKUPED = "Picked up"
    #a staff code is needed to search for orders according to status
    sys.set_staff_codes("1234")
    
    #create orders with different status's
    order1 = sys.create_order()
    order1._status = STATUS_CHECKOUT
    order2 = sys.create_order()
    order2._status = STATUS_CHECKOUT
    order3 = sys.create_order()
    order3._status = STATUS_READY
    order4 = sys.create_order()
    #created orders have status of CREATING by default
    assert (order4._status == STATUS_CREATING)
    
    assert (len(sys.orders) == 4)
    assert (order1 == sys.orders[0])
    assert (order2 == sys.orders[1])
    assert (order3 == sys.orders[2])
    assert (order4 == sys.orders[3])
    
    #get orders with status "CHECKOUT"
    o1 = sys.search_orders("1234", STATUS_CHECKOUT)
    assert(order1 in o1)
    assert(order2 in o1)
    assert(order3 not in o1)
    assert(order4 not in o1)
    assert(len(o1)==2)

    #get orders with status "READY"
    o2 = sys.search_orders("1234", STATUS_READY)
    assert(order1 not in o2)
    assert(order2 not in o2)
    assert(order3 in o2)
    assert(order4 not in o2)
    assert(len(o2)==1)
    
    #get orders with status "CREATING"
    o3 = sys.search_orders("1234", STATUS_CREATING)
    assert(order1 not in o3)
    assert(order2 not in o3)
    assert(order3 not in o3)
    assert(order4 in o3)
    assert(len(o3)==1)
    
    #when status entered is None, get all orders
    o4 = sys.search_orders("1234")
    assert(order1 in o4)
    assert(order2 in o4)
    assert(order3 in o4)
    assert(order4 in o4)
    assert(len(o4)==4)
    
    #get all orders excluding orders with staus of creating
    o4 = sys.search_orders("1234", None, STATUS_CREATING)
    assert(order1 in o4)
    assert(order2 in o4)
    assert(order3 in o4)
    assert(order4 not in o4)
    assert(len(o3)==1)
    #invalid status
    with pytest.raises(IncorrectValueException):
        sys.search_orders("1234","ABC")
    #invalid staff code
    with pytest.raises(NotFoundException):
        sys.search_orders("789")

