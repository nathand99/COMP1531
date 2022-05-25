from flask import render_template, request, redirect, url_for, abort, make_response, session, flash
from errors import *
from product import *
from main_type import *
from standard_main import *
from server import app, system
from message_to_be_displayed import *
from order import Order


KEY_POSITIVE_MESSAGES = "positive"
KEY_NEGATIVE_MESSAGES = "negative"

SESSION_KEY_ORDER_ID = "order_id"
SESSION_KEY_STAFF_CODE = "staff_code"

VERSION_CUSTOMER = "customer"
VERSION_STAFF = "staff"

STATUS_ALL = "All"

ACTION_SET_READY = "Ready to serve"
ACTION_SET_PICKED_UP = "Set picked up"
ACTION_RETURN = "Return to order list"

temp_top_messages = {KEY_POSITIVE_MESSAGES: [], KEY_NEGATIVE_MESSAGES: []}

@app.route("/", methods=["GET"])
def route_index(): ##
    """ 
    Receive from: 
        GET: First time open the page
    Direct to: 
        1. index.html (plain)
    """
    return render_template("index.html", version=get_version(), top_messages=get_top_messages())


@app.route("/404")
@app.errorhandler(404)
def route_page_not_found(e=None): ##
    """ 
    Receive from: 
        ANY METHODS: When the address does not exist or the methods does not match
    Direct to: 
        1. index.html (error message printed on the top below the tabs)
    """
    add_negative_message(nm_page_not_found)
    return redirect(url_for("route_index"))

@app.route("/order/creation/<product_type>", methods=["GET", "POST"])
def route_create_order(product_type):
    """ 
    Receive from: 
        GET: Access via "Order Creation" tab
        POST: switch product types 
        POST: select a main
        POST: select a standard main 
        POST: change quantity of a product (Need Javascript to trigger form transfer without pressing submit button)
        POST: press "return" button on "order/checkout" page
    Direct to: 
        1. order_creation_<product_type>.html (wtih appropreiate layout based on the main ordering procedure and product types)
        2. 404 (if order is empty)
    """
    if system.get_available_main_types() == []:
        add_negative_message(nm_not_enough_stock_for_any_minimal_main_type)
        redirect(url_for("route_index"))

    order_id = get_order_id_in_session()
    if order_id is None:
        order = system.create_order()
        store_order_id_in_session(order.id)
    else:
        try:
            order = system.search_order(order_id)
            if order.status != Order.STATUS_CREATING:
                raise ValueError
        except:
            dispose_order_id_in_session()
            order = system.create_order()
            store_order_id_in_session(order.id)
    order_id = order.id
    
    # print(f"Order id: {order_id}")

    if request.method == 'POST':
        if  "reset" in request.form:
            try:
                system.select_main_type(order, order.main_type)
            except BasicException as e:
                add_negative_message(e.message)
                return redirect(url_for("route_index"))

        elif product_type == "main":
            if MainType.key_str() in request.form:
                main_type = request.form[MainType.key_str()]
                try:
                    system.select_main_type(order, main_type)
                except NotEnoughStockException as e:
                    add_negative_message(e.message)
            elif StandardMain.key_str() in request.form:
                standard_main = request.form[StandardMain.key_str()]
                try:
                    system.select_standard_main(order, standard_main)
                except NotEnoughStockException as e:
                    add_negative_message(e.message)
            else:
                for p,q in request.form.items():
                    q = int(q)
                    try:
                        system.order_product(order, p, q)
                    except NotEnoughStockException as e:
                        add_negative_message(e.message)
                    except ExceedLimitException as e:
                        add_negative_message(e.message)
            
        else:
            for p,q in request.form.items():
                q = int(q)
                try:
                    system.order_product(order, p, q)
                except NotEnoughStockException as e:
                    add_negative_message(e.message)
                except ExceedLimitException as e:
                    add_negative_message(e.message)

    ordered_main_type, ordered_products = map_products_of_order(order)

    items_for_selection = {}
    if product_type == "main":
        template = "order_creation_main.html"
        items_for_selection = {
            MainType.key_str(): [{'name': m.name, 'is_available': a} for m,a in system.get_main_types_and_availability(order=order)], \
            StandardMain.key_str(): [{'name': sm.name, 'product_quantities':sm.product_quantities, 'is_available': a} for sm,a in system.get_standard_mains_and_availability(order=order)], \
        }
        for c in (Base, MajorFilling, MinorFilling):
            items_for_selection.update({c.key_str(): [{'name': i.name, 'max_quantity': q, 'price':i.price, 'ordered_quantity': order.get_quantity_of_product(i)} \
                for i,q in system.get_available_product_quantities(is_available_only=False, order=order, product_types=c)]})
        
        
    else:
        template = "order_creation_side&drink.html"
        for c in (Side, Drink):
            items_for_selection.update({c.key_str(): [{'name': i.name, 'max_quantity': q, 'price':i.price, 'ordered_quantity': order.get_quantity_of_product(i)} \
                for i,q in system.get_available_product_quantities(is_available_only=False, order=order, product_types=c)]})

    return render_template(template, \
            version=get_version(),\
            top_messages=get_top_messages(), \
            product_type=product_type, \
            items_for_selection=items_for_selection, \
            ordered_main_type=ordered_main_type, \
            ordered_products=ordered_products, \
            total_price=order.compute_total_price(), \
            is_dropdown=True) 

@app.route("/order/checkout", methods=["GET"])
def route_checkout_order():
    """ 
    Receive from: 
        GET: press "checkout" button on order_creation_<product_type>.html
    Direct to: 
        1. order_checkout.html (initially)
    """ 
    order_id = get_order_id_in_session()
    order = None
    if order_id is None:
        add_negative_message(nm_order_id_not_found)
        return redirect(url_for("route_create_order", product_type="main"))
    else:
        try:
            order = system.search_order(order_id)
        except NotFoundException:
            dispose_order_id_in_session()
            add_negative_message(nm_order_id_not_found)
            return redirect(url_for("route_create_order", product_type="main"))
    
    errs = system.check_errors_for_checkout(order)
    if errs != []:
        for e in errs:
            add_negative_message(e.message)
            return redirect(url_for("route_create_order",product_type="main"))
    
    ordered_main_type, ordered_products = map_products_of_order(order)

    return render_template("order_checkout.html", version=get_version(),top_messages=get_top_messages(), \
        ordered_main_type=ordered_main_type, ordered_products=ordered_products, total_price=order.compute_total_price()) # filler

@app.route("/order/confirm", methods=["GET"])
def route_confirm_order():
    """ 
    Receive from: 
        GET: press "confirm" button on order_checkout.html
    Direct to: 
        1. order_confirm.html (initially)
    """ 
    order_id = get_order_id_in_session()
    order = None
    if order_id is None:
        add_negative_message(nm_order_id_not_found)
        return redirect(url_for("route_create_order", product_type="main"))
    else:
        try:
            order = system.search_order(order_id)
        except NotFoundException:
            dispose_order_id_in_session()
            add_negative_message(nm_order_id_not_found)
            return redirect(url_for("route_create_order", product_type="main"))
    
    system.checkout(order)
    ordered_main_type, ordered_products = map_products_of_order(order)
    return render_template("order_confirmation.html", version=get_version(),top_messages=get_top_messages(), \
        ordered_main_type=ordered_main_type, ordered_products=ordered_products, total_price=order.compute_total_price(), \
            order_id=order.id)

@app.route("/order/inquiry", methods=["GET", "POST"])
def route_customer_inquire_order():
    """ 
    Receive from: 
        Get: Access via "Order Inquiry" tab
        POST: Press "search" button after entering the order ID
    Direct to: 
        1. order_inquiry.html (wtih based on whether an order ID is queried, and possibly error message for non-existant order ID)
    """
    # dispose_order_id_in_session()

    order_id = ""
    order = None
    if request.method == 'POST':
        order_id = request.form["order_id"]
        try:
            order = system.search_order(order_id)
            if order.status == Order.STATUS_CREATING:
                add_positive_message(pm_order_on_creation)
                return redirect(url_for("route_create_order", product_type="main"))
        except:
            add_negative_message(nm_order_id_not_found)
            order = None

    status = None if order is None else order.status
    ordered_main_type, ordered_products = map_products_of_order(order)
    return render_template("order_inquiry.html", version=get_version(),top_messages=get_top_messages(), \
        status=status, ordered_main_type=ordered_main_type, ordered_products=ordered_products, order_id=order_id)

@app.route("/staff/login", methods=["GET", "POST"])
def route_staff_login(): ##
    """ 
    Receive from: 
        Get: Access via "Staff login" tab
        Post: Press "enter" button after entering the staff code
    Direct to: 
        1. staff_login.html (initially, or if the entered staff code does not exist and an error message is printed)
        2. index.html (if the entered staff code exists, with message "Login Successful" on top and tabs changed to staff version)
    """
    # dispose_order_id_in_session()

    #first time user clicks on login, direct to staff_login.html
    if request.method == 'GET':
        return render_template("staff_login.html", version=get_version(), staff_code="")

    #user clicked submit
    if request.method == 'POST':
        staff_code = request.form["staff_code"]
        #check whether staff login is good
        if system.is_staff_exist(staff_code):
            store_login_staff_code_in_session(staff_code)
            add_positive_message(pm_successful_login)
            return redirect(url_for("route_index"))
        else:
            add_negative_message(nm_incorrect_staff_code_for_login)
            return render_template("staff_login.html", version=get_version(), staff_code=staff_code, top_messages=get_top_messages()) 

@app.route("/staff/logout", methods=["GET"])
def route_staff_logout():
    """ 
    Receive from:
        Get: Access via "Staff logout" tab
    Direct to: 
        1. index.html (with message "Logout Successful" on top and tabs changed to customer version)
    """
    dispose_order_id_in_session()

    if is_user_login_staff():
        dispose_login_staff_code_in_session()
        add_positive_message(pm_successful_logout)
    else:
        add_negative_message(nm_incorrect_staff_code_for_logout)
    return redirect(url_for("route_index"))
        

@app.route("/staff/order/monitoring/<status>", methods=["GET"])
def route_staff_monitor_orders(status): ##
    """ 
    Receive from:
        GET: Access from "Monitor Order" tab
        GET: Press "return" button on "staff/order/inquiry"
    Direct to: 
        1. staff_order_monitoring.html (plain)
        2. 404 (if staff_code is empty)
    """
    dispose_order_id_in_session()

    staff_code = get_login_staff_code_in_session(None)
    validate_staff_code(staff_code)

    try:
        orders = system.search_orders(staff_code, None if status == STATUS_ALL else status, excluded_status=Order.STATUS_CREATING)
    except NotFoundException as e:
        add_negative_message(e.message)
        return redirect(url_for("route_page_not_found"))

    all_status = Order.all_checked_out_status()
    all_status.insert(0, STATUS_ALL)
    selected_status = status
    orders.sort(key=lambda o: o.duration_from_checkout)
    return render_template("staff_orders_monitoring.html", version=get_version(), top_messages=get_top_messages(), \
        all_status=all_status, selected_status=selected_status,orders=orders)

@app.route("/staff/order/inquiry", methods=["POST"])
def route_staff_inquiry_order():
    """ 
    Receive from:
        GET: Access from "Monitor Order" tab
        GET: Press "return" button on "staff/order/inquiry"
    Direct to: 
        1. staff_order_monitoring.html (plain)
        2. 404 (if staff_code is empty)
    """
    dispose_order_id_in_session()
    staff_code = get_login_staff_code_in_session(None)
    validate_staff_code(staff_code)
    
    order_id = request.form.get("order_id")
    try:
        order = system.search_order(order_id)
    except BasicException as e:
        add_negative_message(e.message)
        return redirect(url_for("route_staff_monitor_orders", status=STATUS_ALL))
    
    action_from_request = request.form.get("action")
    try:
        if action_from_request == ACTION_RETURN:
            return redirect(url_for("route_staff_monitor_orders", status=STATUS_ALL))
        elif action_from_request == ACTION_SET_READY:
            system.set_order_ready_to_serve(staff_code, order)
        elif action_from_request == ACTION_SET_PICKED_UP:
            system.set_order_picked_up(staff_code, order)
        elif action_from_request is not None:
            add_negative_message(nm_incorrect_action_staff_inquiry_order)
    except NotFoundException as e:
        add_negative_message(nm_incorrect_staff_code)
        return redirect(url_for("route_index")) 
    
    actions = [ACTION_RETURN]
    if order.status == Order.STATUS_READY:
        actions.insert(0,ACTION_SET_PICKED_UP)
    elif order.status == Order.STATUS_PICKED_UP:
        pass
    else:
       actions.insert(0,ACTION_SET_READY)

    return render_template("staff_order_inquiry.html", version=get_version(), top_messages=get_top_messages(), order=order, \
        actions=actions)


@app.route("/staff/stock_modification", methods=["GET", "POST"])
def route_staff_modify_stock():
    """ 
    Receive from:
        GET: Access via "Modify Stock" tab
        POST: Press "update" button at the bottom after entering all the increased quantities
    Direct to: 
        1. staff_modify_ingredient.html (plain)
        2. 404 (if staff_code is empty)
    """
    dispose_order_id_in_session()
    staff_code = get_login_staff_code_in_session(None)
    validate_staff_code(staff_code)

    if request.method == "POST":
        try:
            ingredient_stock_change = [(name, int(q_change)) for name, q_change in request.form.items() if q_change != ""]
            system.modify_stock(staff_code, ingredient_stock_change)
        except ValueError:
            add_negative_message(nm_quantity_cannot_be_noninteger)
        except BasicException as e:
            add_negative_message(e.message)
                

    return render_template("staff_stock_modification.html", version=get_version(),top_messages=get_top_messages(), \
        ingredient_stock=system.ingredient_stock) 

# @app.route("/staff/product_modification", methods=["GET", "POST"])
# def route_staff_modify_product():
#     """ BONUS
#     Receive from:
#         GET: Access via "Modify Product" tab
#         POST: Press "update" button at the bottom after entering all details of new product
#     Direct to: 
#         1. staff_modify_product.html (plain)
#         2. 404 (if staff_code is empty)
#     """
#     return render_template("index.html", version="customer",top_messages=get_top_messages()) # filler


def add_positive_message(message):
    temp_top_messages[KEY_POSITIVE_MESSAGES].append(message)

def add_negative_message(message):
    temp_top_messages[KEY_NEGATIVE_MESSAGES].append(message)



def get_top_messages(pop_after=True):
    top_messages = {}
    for key in temp_top_messages:
        top_messages[key] = temp_top_messages[key]
    
    if pop_after:
        temp_top_messages[KEY_POSITIVE_MESSAGES] = []
        temp_top_messages[KEY_NEGATIVE_MESSAGES] = []   
    return top_messages

def get_version():
    return VERSION_STAFF if is_user_login_staff() else VERSION_CUSTOMER

def is_user_login_staff():
    return SESSION_KEY_STAFF_CODE in session

def store_login_staff_code_in_session(staff_code):
    session[SESSION_KEY_STAFF_CODE] = staff_code

def get_login_staff_code_in_session(default_value=None):
    return session.get(SESSION_KEY_STAFF_CODE, default_value)

def dispose_login_staff_code_in_session():
    if is_user_login_staff():
        session.pop(SESSION_KEY_STAFF_CODE)

def store_order_id_in_session(order_id):
    session[SESSION_KEY_ORDER_ID] = order_id

def get_order_id_in_session(default_value=None):
    return session.get(SESSION_KEY_ORDER_ID, default_value)

def dispose_order_id_in_session(cancel_order_if_creating=True):
    if SESSION_KEY_ORDER_ID in session:
        order_id = session.pop(SESSION_KEY_ORDER_ID)
        if cancel_order_if_creating:
            try:
                order = system.search_order(order_id)
                if order.status == STATUS.STATUS_ORDER:
                    system.cancel_order(order)

            except:
                pass

def map_products_of_order(order):
    if order == None:
        return {}, {}
    ordered_main_type = order.main_type
    ordered_products = {}
    for c in (Base, MajorFilling, MinorFilling, Side, Drink):
        ordered_products.update({c.key_str(): [{'name': i.name, 'quantity':q, 'price': i.price} for i,q in order.get_product_quantities(product_types=c)]})
    return ordered_main_type, ordered_products

def validate_staff_code(staff_code):
    if staff_code is None:
        return redirect(url_for("route_page_not_found"))
    if not system.is_staff_exist(staff_code):
        dispose_login_staff_code_in_session()
        add_negative_message(nm_incorrect_staff_code)
        return redirect(url_for("route_page_not_found"))
