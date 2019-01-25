from flask import Markup, url_for, session, redirect
import json
import os
import sqlite3
from datetime import datetime
import codecs
from sqlalchemy.orm import sessionmaker
from KiehlShop.Xu_ly.Xu_ly_Model import *

from hashlib import sha256

DBSession = sessionmaker(bind=engine)
session_1 = DBSession()

def Encode_password(password):
    sha = sha256()
    sha.update(password.encode())
    passwd = sha.hexdigest()
    return passwd

def Kiem_tra_Nguoi_dung(data):
    passwd = Encode_password(data['password'])
    return session_1.query(Nguoi_dung).filter(
            Nguoi_dung.Email == data['email'], Nguoi_dung.Mat_khau == passwd).first()    
    