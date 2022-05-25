from flask import Flask
import os
app_name = "Gourmet Outlet"
app = Flask(app_name, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')) # To prevent unknown auto path relocation
app.secret_key = "who_cares about_secretKey"

from backend.online_order_system import OnlineOrderSystem
system = OnlineOrderSystem.init()

if system is None:
    from backend.init_sys import get_init_sys
    system = get_init_sys()