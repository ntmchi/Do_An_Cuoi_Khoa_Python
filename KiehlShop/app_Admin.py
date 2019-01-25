from KiehlShop import app
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, Markup
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.contrib import sqlamodel
from KiehlShop.Xu_ly.Xu_ly_Model import *
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy import exc
from flask_admin import BaseView, expose

configure_mappers()
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///KiehlShop/Du_lieu/ban_hang_truc_tuyen.db?check_same_thread=False'
login = LoginManager(app)

@login.user_loader
def load_user(id):
    quan_tri = session.query(Quan_tri).filter(Quan_tri.id == id).first()
    return quan_tri

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('index'))

class LoaiSanPhamView(MyModelView):
    column_display_pk = True
    can_create = True
    can_delete = False
    can_edit = True
    can_export = True
    form_columns = ('Ten_loai', 'Hinh_dai_dien')
    

class SanPhamView(MyModelView):
    column_display_pk = True
    can_create = True
    can_delete = False
    can_edit = True
    page_size = 10 # Cho phep phan trang
    column_list = ('ma_loai_san_pham.Ma_loai', 'Ma_san_pham', 'Ten_san_pham', 'Mo_ta', 'Chat_lieu', 'Don_gia', 'Tinh_trang')
    form_columns = ('Ma_loai','Ma_san_pham', 'Ten_san_pham', 'Mo_ta', 'Chat_lieu', 'Don_gia', 'Tinh_trang')
    inline_models = [(Hinh_san_pham), (San_pham_chi_tiet, dict(form_columns=['Ma_san_pham_chi_tiet', 'Mau_sac', 'Size', 'So_luong']))]

class HinhSanPhamView(MyModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    page_size = 10 # Cho phep phan trang
    column_list = ('ma_san_pham_chi_tiet.Ma_san_pham', 'Hinh_anh')

class SanPhamChiTietView(MyModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    page_size = 10 # Cho phep phan trang
    column_list = ('san_pham.Ma_san_pham', 'Mau_sac', 'Size', 'So_luong')

class CuaHangView(MyModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    form_columns = ('Ten_cua_hang', 'Dia_chi', 'Dien_thoai')

class LoaiNguoiDungView(MyModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    column_list = ('Ma_loai_nguoi_dung', "Ten_loai_nguoi_dung")
    inline_models = [(Nguoi_dung,dict(form_columns=['Ma_nguoi_dung','Ho_ten', 'Email', 'Mat_khau']))]

class NguoiDungView(MyModelView):
    column_display_pk = True
    can_create = True
    can_edit = True
    column_list = ('loai_nguoi_dung.Ma_loai_nguoi_dung','Ho_ten', 'Email', 'Mat_khau')

admin = Admin(app, name='Quản lý KiehlShop', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(LoaiSanPhamView(Loai_san_pham, session, 'Danh mục sản phẩm'))
admin.add_view(SanPhamView(San_pham, session, 'Sản phẩm'))
admin.add_view(SanPhamChiTietView(San_pham_chi_tiet, session, 'Sản phẩm chi tiết'))
admin.add_view(HinhSanPhamView(Hinh_san_pham, session, 'Hình ảnh'))
admin.add_view(CuaHangView(Cua_hang, session, 'Cửa hàng'))
admin.add_view(LoaiNguoiDungView(Loai_nguoi_dung, session, 'Loại user'))
admin.add_view(NguoiDungView(Nguoi_dung, session, 'User'))

admin.add_view(LogoutView(name='Đăng xuất', menu_icon_type='glyph'))
    
@app.route('/quan-ly', methods=['GET', 'POST'])
def dang_nhap():
    Chuoi_thong_bao = ""
    if(request.method == 'POST'):
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        quan_tri = session.query(Quan_tri).filter(Quan_tri.Ten_dang_nhap == Ten_dang_nhap and Quan_tri.Mat_khau == Mat_khau).first()
        Hop_le = quan_tri
        if Hop_le:
            login_user(quan_tri)
            return redirect(url_for('admin.index'))
        else:
            Chuoi_thong_bao = "Đăng nhập không hợp lệ"
    return render_template('Dang_nhap.html', Chuoi_thong_bao = Chuoi_thong_bao)

