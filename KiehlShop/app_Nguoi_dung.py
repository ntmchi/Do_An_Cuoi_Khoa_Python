from KiehlShop import app
from flask import Flask, render_template, Markup, session, request, flash, Response,jsonify, redirect, url_for
from sqlalchemy import exc
from KiehlShop.Xu_ly.Xu_ly_3L_User import *
from KiehlShop.Xu_ly.Xu_ly_Model import *
import datetime
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user

DBsession = sessionmaker(bind=engine)
session = DBsession()

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(Ma_nguoi_dung):    
    nguoi_dung = session.query(Nguoi_dung).filter(Nguoi_dung.Ma_nguoi_dung == Ma_nguoi_dung).first()
    return nguoi_dung

@app.route("/nguoi-dung/dang-nhap", methods=['POST'])
def login():
    status = False
    item = request.form.get('item')
    item = json.loads(item)    
    
    nguoi_dung = Kiem_tra_Nguoi_dung(item)
    
    if nguoi_dung is not None:
        status = True
        login_user(nguoi_dung, False, None, True)
        
    return jsonify(status=status)

@app.route("/nguoi-dung/dang-xuat", methods=['GET'])
def logout():
    logout_user()

    return redirect('/')    
