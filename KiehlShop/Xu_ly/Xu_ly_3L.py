from flask import Markup, url_for
import json
import os
import sqlite3
from datetime import datetime
import codecs
from sqlalchemy.orm import sessionmaker
from KiehlShop.Xu_ly.Xu_ly_Model import *

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session_1 = DBSession()

# Xử lý Lưu trữ
def remove_accents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

def Doc_Danh_sach_Cua_hang():
    ds_CH = None
    Danh_sach_Cua_hang = []
    ds_CH = session_1.query(Cua_hang).all()
    for item in ds_CH:
        cua_hang = {"Ma_cua_hang": item.Ma_cua_hang, "Ten_cua_hang": item.Ten_cua_hang,
                          "Dia_chi": item.Dia_chi, "Dien_thoai": item.Dien_thoai}
        Danh_sach_Cua_hang.append(cua_hang)
    return Danh_sach_Cua_hang

def Doc_Danh_sach_Loai_San_Pham(Ma_loai='All'):
    ds_loai_sp = None
    danh_sach_loai_san_pham = []
    if Ma_loai != 'All': 
        ds_loai_sp = session_1.query(Loai_san_pham).filter(
            Loai_san_pham.Ma_loai == Ma_loai).all()
    else:
        ds_loai_sp = session_1.query(Loai_san_pham).all()
    for item in ds_loai_sp:
        loai_san_pham = {"Ma_loai": item.Ma_loai, "Ten_loai": item.Ten_loai,
                         "Hinh_dai_dien": item.Hinh_dai_dien}
        danh_sach_loai_san_pham.append(loai_san_pham)
    return danh_sach_loai_san_pham

def Doc_Thong_Tin_Hinh_San_pham(Ma_san_pham):
    danh_sach = []
    ds_hinh_Sp = None
    ds_hinh_Sp = session_1.query(Hinh_san_pham).filter(
            Hinh_san_pham.Ma_san_pham == Ma_san_pham).all()
    for item in ds_hinh_Sp:
        hinh_anh = {"Ma_san_pham": item.Ma_san_pham, "Hinh_anh": item.Hinh_anh}
        danh_sach.append(hinh_anh)
    return danh_sach

def Doc_Thong_Tin_San_pham_Chi_tiet(Ma_san_pham):
    danh_sach = []
    ds_thong_so_SP = None
    ds_thong_so_SP = session_1.query(San_pham_chi_tiet).filter(
            San_pham_chi_tiet.Ma_san_pham == Ma_san_pham).group_by(San_pham_chi_tiet.Mau_sac).all()
    for item in ds_thong_so_SP:
        chi_tiet = {"Ma_san_pham": item.Ma_san_pham, "Mau_sac": item.Mau_sac,
                         "Size": item.Size, "So_luong": item.So_luong}
        danh_sach.append(chi_tiet)
    return danh_sach

def Doc_Danh_sach_San_Pham():    
    ds_sp = None
    danh_sach_san_pham = []
    ds_sp = session_1.query(San_pham).all()    
    for item in ds_sp:                
        Ma_sp = item.Ma_san_pham
        ds_hinh_anh = Doc_Thong_Tin_Hinh_San_pham(Ma_sp)
        loai_san_pham = Doc_Danh_sach_Loai_San_Pham(item.Ma_loai)[0]
        san_pham_chi_tiet = Doc_Thong_Tin_San_pham_Chi_tiet(Ma_sp)

        san_pham = {"Ma_loai": item.Ma_loai, "Ten_loai": loai_san_pham["Ten_loai"], "Ma_san_pham": Ma_sp, 
                    "Ten_san_pham": item.Ten_san_pham, "Mo_ta": item.Mo_ta,"Chat_lieu":item.Chat_lieu, "Don_gia": item.Don_gia, "Hinh": ds_hinh_anh,
                    "Danh_sach_Chi_tiet": san_pham_chi_tiet}
        danh_sach_san_pham.append(san_pham)
    return danh_sach_san_pham

def Lay_San_pham_theo_Ma(Danh_sach_SP, Ma_sp):    
    Danh_sach  = list(filter(
        lambda Sp: Sp["Ma_san_pham"] == Ma_sp, Danh_sach_SP
    ))
    Sp = Danh_sach[0] if len(Danh_sach)==1 else None
    return Sp

def Tinh_tong_So_luong_Theo_SP(Ma_san_pham):
    danh_sach = []
    ds_thong_so_SP = None
    ds_thong_so_SP = session_1.query(San_pham_chi_tiet).filter(
            San_pham_chi_tiet.Ma_san_pham == Ma_san_pham).group_by(San_pham_chi_tiet.Mau_sac).all()
    for item in ds_thong_so_SP:
        chi_tiet = {"Ma_san_pham": item.Ma_san_pham, "Mau_sac": item.Mau_sac,
                         "Size": item.Size, "So_luong": item.So_luong}
        danh_sach.append(chi_tiet)
    return danh_sach

def Tra_cuu_san_pham(chuoi_tra_cuu, ds_San_pham):
    danh_sach = list(filter(lambda san_pham: chuoi_tra_cuu.upper() in san_pham['Ten_san_pham'].upper(), ds_San_pham))
    return danh_sach
    

# Xử lý Thể hiện
def Tao_chuoi_HTML_Loai_San_Pham(Loai_san_pham):
    Danh_muc = remove_accents(Loai_san_pham['Ten_loai'])
    Chuoi_HTML = '<button id="' + Danh_muc.lower() + '" data-href="#' + Danh_muc.lower() + '" class="stext-106 cl6 hov1 bor3 trans-04 m-r-32 m-tb-5" data-filter=".DanhMuc_' + \
        str(Loai_san_pham['Ma_loai']) + '">'
    Chuoi_HTML += Loai_san_pham['Ten_loai'].upper()
    Chuoi_HTML += '</button>'
    return Chuoi_HTML

def Tao_chuoi_HTML_Submenu_San_pham(Session):        
    Chuoi_HTML = ''    
    if 'sub_menu' in Session:         
        Chuoi_HTML = Session['sub_menu']
    else:        
        Danh_sach_Danh_muc = Doc_Danh_sach_Loai_San_Pham()

        for loai in Danh_sach_Danh_muc:    
            Danh_muc = remove_accents(loai['Ten_loai'])
            Chuoi_HTML += '<li><a data-id="' + Danh_muc.lower() + '"href="/collections/all#'+ Danh_muc.lower() +'" data-filter=".DanhMuc_' + str(loai['Ma_loai']) + '">' + \
            loai['Ten_loai'].upper()+'</a></li>'  
        Session['sub_menu'] = Markup(Chuoi_HTML)

    return Session

def Tao_breadcrum(San_pham):
    Danh_muc = remove_accents(San_pham['Ten_loai'])
    Chuoi_HTML='<div class="container">'
    Chuoi_HTML += '<div class="bread-crumb flex-w p-l-25 p-r-15 p-t-30 p-lr-0-lg">'
    Chuoi_HTML += '<a href="/" class="stext-109 cl8 hov-cl1 trans-04"> Trang chủ'
    Chuoi_HTML += '<i class="fa fa-angle-right m-l-9 m-r-10" aria-hidden="true"></i>'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '<a data-id="' + Danh_muc.lower() + '" href="/collections/all#'+ Danh_muc.lower() +'" class="stext-109 cl8 hov-cl1 trans-04" data-filter=".DanhMuc_' + str(San_pham['Ma_loai']) + '">'
    Chuoi_HTML += San_pham["Ten_loai"]
    Chuoi_HTML += '<i class="fa fa-angle-right m-l-9 m-r-10" aria-hidden="true"></i>'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '<span class="stext-109 cl4">'
    Chuoi_HTML += San_pham["Ten_san_pham"]
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    return Chuoi_HTML

def Tao_chuoi_HTML_Hinh_San_pham_Chi_tiet(San_pham):
    Chuoi_HTML = ""
    for hinh in San_pham["Hinh"]:
        Chuoi_HTML += '<div class="item-slick3" data-thumb="'+ url_for('static', filename = "image/" + hinh["Hinh_anh"]) + '"/>'
        Chuoi_HTML += '<div class="wrap-pic-w pos-relative">'
        Chuoi_HTML += '<img src="'+ url_for('static', filename = "image/" + hinh["Hinh_anh"]) + '" alt="IMG-PRODUCT">'
        Chuoi_HTML += '<a class="flex-c-m size-108 how-pos1 bor0 fs-16 cl10 bg0 hov-btn3 trans-04" href="'+ url_for('static', filename = "image/" + hinh["Hinh_anh"]) + '"/>'
        Chuoi_HTML += '<i class="fa fa-expand"></i></a></div></div>'
    return Chuoi_HTML

def Tao_chuoi_Mau_sac_San_pham(San_pham):
    Chuoi_HTML = ""
    for chi_tiet in San_pham["Danh_sach_Chi_tiet"]:
        Chuoi_HTML += '<option value="' + chi_tiet['Mau_sac'] + '">'+chi_tiet["Mau_sac"]+'</option>'
    return Chuoi_HTML

def Tao_chuoi_Thong_tin_San_pham_Chi_tiet(San_pham):
    Chuoi_HTML = ""
    Chuoi_HTML += '<h4 class="mtext-105 cl2 js-name-detail p-b-14">'
    Chuoi_HTML += San_pham["Ten_san_pham"]
    Chuoi_HTML += '</h4>'
    Chuoi_HTML += '<span class="mtext-106 cl2" id="Th_Don_gia">'
    Chuoi_HTML += "{:,}".format(San_pham["Don_gia"]) + '₫'
    Chuoi_HTML += '</span>'
    if(San_pham["Mo_ta"] != ""):
        Chuoi_HTML += '<p class="stext-102 cl3 p-t-23">'
        Chuoi_HTML += 'Miêu tả: ' + San_pham["Mo_ta"]
        Chuoi_HTML += "</p>"
    if(San_pham["Chat_lieu"] != ""):
        Chuoi_HTML += '<p class="stext-102 cl3 p-t-23">'
        Chuoi_HTML += 'Chất liệu: ' +  San_pham["Chat_lieu"]
        Chuoi_HTML += '</p>'
    return Chuoi_HTML


def Tao_chuoi_HTML_San_Pham(San_pham):
    Chuoi_HTML = '<div class="col-sm-6 col-md-4 col-lg-3 p-b-35 isotope-item DanhMuc_'+ str(San_pham["Ma_loai"]) +'">'
    Chuoi_HTML += '<!-- Block2 -->'
    Chuoi_HTML += '<div class="block2">'
    Chuoi_HTML += '<div class="block2-pic hov-img0">'
    Chuoi_HTML += '<img src="'+url_for('static', filename='image/' + str(
        San_pham["Hinh"][0]["Hinh_anh"]))+'" alt="'+San_pham["Ten_san_pham"]+'" height="468" width="396">'
    Chuoi_HTML += '<a href="#" class="block2-btn flex-c-m stext-103 cl2 size-102 bg0 bor2 hov-btn1 p-lr-15 trans-04 js-show-modal1" data-toggle="wrap-modal1" data-id='+ San_pham["Ma_san_pham"] +' data-target="#' + \
        San_pham["Ma_san_pham"]+'">'
    Chuoi_HTML += 'Xem nhanh'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="block2-txt flex-w flex-t p-t-14">'
    Chuoi_HTML += '<div class="block2-txt-child1 flex-col-l ">'
    Chuoi_HTML += '<a href="/product/'+San_pham["Ma_san_pham"] +'" class="stext-104 cl4 hov-cl1 trans-04 js-name-b2 p-b-6">'
    Chuoi_HTML += San_pham["Ten_san_pham"].upper()
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '<span class="stext-105 cl3">'
    Chuoi_HTML += "{:,}".format(San_pham["Don_gia"]) + '₫'
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '</div>'
    # Icon love --> cần improve
    Chuoi_HTML += '<div class="block2-txt-child2 flex-r p-t-3">'
    Chuoi_HTML += '<a href="#" class="btn-addwish-b2 dis-block pos-relative js-addwish-b2">'
    Chuoi_HTML += '<img class="icon-heart1 dis-block trans-04" src="' + \
        url_for('static', filename='images/icons/icon-heart-01.png') + '"'
    Chuoi_HTML += 'alt="ICON">'
    Chuoi_HTML += '<img class="icon-heart2 dis-block trans-04 ab-t-l" src="' + \
        url_for('static', filename='images/icons/icon-heart-02.png') + '"'
    Chuoi_HTML += 'alt="ICON">'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    return Chuoi_HTML

def Tao_modal(San_pham):
    Chuoi_HTML = '<div class="wrap-modal1 js-modal1 p-t-60 p-b-20" id=' + \
         San_pham["Ma_san_pham"]+'>'
    Chuoi_HTML += '<div class="overlay-modal1 js-hide-modal1"></div>'
    Chuoi_HTML += '<div class="container">'
    Chuoi_HTML += '<div class="bg0 p-t-60 p-b-30 p-lr-15-lg how-pos3-parent">'
    Chuoi_HTML += '<button class="how-pos3 hov3 trans-04 js-hide-modal1">'
    Chuoi_HTML += '<img src="' + \
        url_for('static', filename='images/icons/icon-close.png') + \
        '" alt="CLOSE">'
    Chuoi_HTML += '</button>'
    Chuoi_HTML += '<div class="row">'
    Chuoi_HTML += '<div class="col-md-6 col-lg-7 p-b-30">'
    Chuoi_HTML += '<div class="p-l-25 p-r-30 p-lr-0-lg">'
    Chuoi_HTML += '<div class="wrap-slick3 flex-sb flex-w">'
    Chuoi_HTML += '<div class="wrap-slick3-dots"></div>'
    Chuoi_HTML += '<div class="wrap-slick3-arrows flex-sb-m flex-w"></div>'
    Chuoi_HTML += '<div class="slick3 gallery-lb">'
    Chuoi_HTML_Hinh_anh = Tao_chuoi_HTML_Hinh_San_pham_Chi_tiet(San_pham)
    Chuoi_HTML += Chuoi_HTML_Hinh_anh
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="col-md-6 col-lg-5 p-b-30">'
    Chuoi_HTML += '<div class="p-r-50 p-t-5 p-lr-0-lg">'
    Chuoi_HTML_San_pham_Info = Tao_chuoi_Thong_tin_San_pham_Chi_tiet(San_pham)
    Chuoi_HTML += Chuoi_HTML_San_pham_Info
    Chuoi_HTML += '<div class="p-t-33">'
    Chuoi_HTML += '<div class="flex-w flex-r-m p-b-10">'
    Chuoi_HTML += '<div class="size-203 flex-c-m respon6">'
    Chuoi_HTML += 'Size'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="size-204 respon6-next">'
    Chuoi_HTML += '<div class="rs1-select2 bor8 bg0">'
    Chuoi_HTML += '<select class="js-select2 ma-size" name="time">'
    Chuoi_HTML += '<option>S</option>'
    Chuoi_HTML += '<option>M</option>'
    Chuoi_HTML += '<option>L</option>'
    Chuoi_HTML += '</select>'
    Chuoi_HTML += '<div class="dropDownSelect2"></div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="flex-w flex-r-m p-b-10">'
    Chuoi_HTML += '<div class="size-203 flex-c-m respon6">'
    Chuoi_HTML += 'Màu sắc'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="size-204 respon6-next">'
    Chuoi_HTML += '<div class="rs1-select2 bor8 bg0">'
    Chuoi_HTML += '<select class="js-select2 mau-sac" name="time">'
    Chuoi_HTML_Mau_sac = Tao_chuoi_Mau_sac_San_pham(San_pham)
    Chuoi_HTML += Chuoi_HTML_Mau_sac
    Chuoi_HTML += '</select>'
    Chuoi_HTML += '<div class="dropDownSelect2"></div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="flex-w flex-r-m p-b-10">'
    Chuoi_HTML += '<div class="size-204 flex-w flex-m respon6-next">'
    Chuoi_HTML += '<div class="wrap-num-product flex-w m-r-20 m-tb-10">'
    Chuoi_HTML += '<div class="btn-num-product-down cl8 hov-btn3 trans-04 flex-c-m">'
    Chuoi_HTML += '<i class="fs-16 zmdi zmdi-minus"></i>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<input class="mtext-104 cl3 txt-center num-product" type="number" name="num-product" value="1">'
    Chuoi_HTML += '<div class="btn-num-product-up cl8 hov-btn3 trans-04 flex-c-m">'
    Chuoi_HTML += '<i class="fs-16 zmdi zmdi-plus"></i>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<button class="flex-c-m stext-101 cl0 size-101 bg1 bor1 hov-btn1 p-lr-15 trans-04 js-addcart-detail">'
    Chuoi_HTML += 'Thêm vào giỏ hàng'
    Chuoi_HTML += '</button>'
    Chuoi_HTML += '<input type="hidden" value="'+ San_pham["Ma_san_pham"] +'" name="Th_Ma_so" />'
    Chuoi_HTML += '<input type="hidden" value="' + str(San_pham["Don_gia"]) +'" name="Th_Don_gia" />'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="flex-w flex-m p-l-100 p-t-40 respon7">'
    Chuoi_HTML += '<div class="flex-m bor9 p-r-10 m-r-11">'
    Chuoi_HTML += '<a href="#" class="fs-14 cl3 hov-cl1 trans-04 lh-10 p-lr-5 p-tb-2 js-addwish-detail tooltip100" data-tooltip="Add to Wishlist">'
    Chuoi_HTML += '<i class="zmdi zmdi-favorite"></i>'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<a href="#" class="fs-14 cl3 hov-cl1 trans-04 lh-10 p-lr-5 p-tb-2 m-r-8 tooltip100" data-tooltip="Facebook">'
    Chuoi_HTML += '<i class="fa fa-facebook"></i>'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '<a href="#" class="fs-14 cl3 hov-cl1 trans-04 lh-10 p-lr-5 p-tb-2 m-r-8 tooltip100" data-tooltip="Twitter">'
    Chuoi_HTML += '<i class="fa fa-twitter"></i>'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '<a href="#" class="fs-14 cl3 hov-cl1 trans-04 lh-10 p-lr-5 p-tb-2 m-r-8 tooltip100" data-tooltip="Google Plus">'
    Chuoi_HTML += '<i class="fa fa-google-plus"></i>'
    Chuoi_HTML += '</a>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'    
    Chuoi_HTML += '</div>'    
    return Chuoi_HTML

def Tao_chuoi_HTML_Thong_tin_Cua_hang(Cua_hang):
    Chuoi_HTML = '<div class="size-100 bor10 flex-w flex-col-m p-lr-93 p-tb-30 p-lr-15-lg w-full-md thong-tin-cua-hang" id="CH_' + str(Cua_hang["Ma_cua_hang"]) + '" style="display:none">'
    Chuoi_HTML += '<div class="flex-w w-full p-b-42">'
    Chuoi_HTML += '<h4 class="ltext-108">'
    Chuoi_HTML += 'Kiehl ' + Cua_hang['Ten_cua_hang']
    Chuoi_HTML += '</h4>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="flex-w w-full p-b-42">'
    Chuoi_HTML += '<span class="fs-18 cl5 txt-center size-211">'
    Chuoi_HTML += '<span class="lnr lnr-map-marker"></span>'
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '<div class="size-212 p-t-2">'
    Chuoi_HTML += '<span class="mtext-110 cl2">'
    Chuoi_HTML += 'Địa Chỉ'
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '<p class="stext-115 cl6 size-213 p-t-18">'
    Chuoi_HTML += Cua_hang["Dia_chi"]
    Chuoi_HTML += '</p>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="flex-w w-full p-b-42">'
    Chuoi_HTML += '<span class="fs-18 cl5 txt-center size-211">'
    Chuoi_HTML += '<span class="lnr lnr-phone-handset"></span>'
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '<div class="size-212 p-t-2">'
    Chuoi_HTML += '<span class="mtext-110 cl2">'
    Chuoi_HTML += 'Số Điện Thoại'
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '<p class="stext-115 cl1 size-213 p-t-18">'
    Chuoi_HTML += Cua_hang["Dien_thoai"]
    Chuoi_HTML += '</p>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '<div class="flex-w w-full">'
    Chuoi_HTML += '<span class="fs-18 cl5 txt-center size-211">'
    Chuoi_HTML += '<span class="lnr lnr-envelope"></span>'
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '<div class="size-212 p-t-2">'
    Chuoi_HTML += '<span class="mtext-110 cl2">'
    Chuoi_HTML += 'Email'
    Chuoi_HTML += '</span>'
    Chuoi_HTML += '<p class="stext-115 cl1 size-213 p-t-18">'
    Chuoi_HTML += 'contact@example.com'
    Chuoi_HTML += '</p>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'
    Chuoi_HTML += '</div>'

    return Chuoi_HTML

def Cap_nhat_Danh_sach_Gio_hang(Session, San_pham):    
    if 'gio_hang' in Session:        
        if not any(San_pham['Ma_san_pham'] in d['Ma_san_pham'] for d in Session['gio_hang']):                    
            Session['gio_hang'].append(San_pham)
        else:
            flag=False
            for item in Session['gio_hang']:              
                if (item["Ma_san_pham"]==item["Ma_san_pham"] and item["Size"] == San_pham['Size'] and item["Mau_sac"] == San_pham['Mau_sac']):                        
                    item['So_luong'] = int(item['So_luong']) + int(San_pham['So_luong'])                        
                    flag=True
                    break
            if(flag == False):
                Session['gio_hang'].append(San_pham)                     
    else:        
        Session['gio_hang'] = [San_pham]
    return Session


def Doc_Danh_sach_Gio_hang(Session):        
    if 'gio_hang' in Session:
        return Session['gio_hang']                           
    return None

def Tao_chuoi_HTML_Gio_hang(Danh_sach_Gio_hang):
    Chuoi_HTML = ''

    for San_pham in Danh_sach_Gio_hang:
        Thanh_tien = int(San_pham['Don_gia']) * int(San_pham['So_luong'])

        Chuoi_HTML += '<tr class="table_row">'
        Chuoi_HTML += '<td class="column-1">'
        Chuoi_HTML += '<div class="how-itemcart1">'
        Chuoi_HTML += '<img src="' + str(San_pham['Hinh']) + '" alt="' + San_pham["Ten_san_pham"] + '" height="80" width="396">'
        Chuoi_HTML += '</div>'
        Chuoi_HTML += '</td>'
        Chuoi_HTML += '<td class="column-2">' + San_pham['Ten_san_pham'] + '<br><small>'+San_pham['Mau_sac'] +' / '+ San_pham['Size']+'</small></td>'
        Chuoi_HTML += '<td class="column-3 text-center">' + "{:,}".format(int(San_pham['Don_gia'])) + ' đ</td>'
        Chuoi_HTML += '<td class="column-4 text-center">'
        Chuoi_HTML += "{:,}".format(int(San_pham['So_luong']))
        Chuoi_HTML += '</td>'
        Chuoi_HTML += '<td class="column-5 text-center">' + "{:,}".format(Thanh_tien) + ' đ</td>'
        Chuoi_HTML += '</tr>'

    return Chuoi_HTML