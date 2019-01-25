from KiehlShop import app
from flask import Flask, flash, url_for, redirect, render_template, session, abort, Markup, request
from flask_googlemaps import Map
from KiehlShop.Xu_ly.Xu_ly_3L import *

Danh_sach_Cua_hang = Doc_Danh_sach_Cua_hang()

@app.route("/store")
def store():
    Chuoi_Cua_hang = ""
    for Cua_hang in Danh_sach_Cua_hang:        
        Chuoi_Cua_hang += Tao_chuoi_HTML_Thong_tin_Cua_hang(Cua_hang)
    return render_template("Cua_hang.html",
                           Danh_sach_Cua_hang = Danh_sach_Cua_hang,
                           Chuoi_Cua_Hang = Markup(Chuoi_Cua_hang))
