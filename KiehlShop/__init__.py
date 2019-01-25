from flask import Flask, session

app = Flask(__name__, template_folder="Giao_dien", static_folder="Media")

import KiehlShop.app_San_pham
import KiehlShop.app_Admin
import KiehlShop.app_Ban_do
import KiehlShop.app_Gio_hang
import KiehlShop.app_Nguoi_dung
from KiehlShop.Xu_ly.Xu_ly_3L import *

@app.before_request  
def before_request_callback():
    Tao_chuoi_HTML_Submenu_San_pham(session)           

@app.after_request 
def after_request_callback(response):
    return response