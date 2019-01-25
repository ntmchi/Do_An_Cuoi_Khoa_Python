from KiehlShop import app
from flask import Flask, render_template, Markup, session, request, flash, Response,jsonify
from sqlalchemy import exc
from KiehlShop.Xu_ly.Xu_ly_3L import *
from KiehlShop.Xu_ly.Xu_ly_Model import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from flask_mail import Mail, Message
from KiehlShop.Xu_ly.Xu_ly_3L_User import *
import datetime
import random
import string

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session_1 = DBSession()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'python244t7cn@gmail.com'
app.config['MAIL_PASSWORD'] = 'Python244'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/shoping-cart", methods=['GET', 'POST'])
def shopping_cart():
    Chuoi_Thong_bao = ""
    Chuoi_Gio_hang = ""
    Danh_sach_Gio_hang = Doc_Danh_sach_Gio_hang(session)
    if(Danh_sach_Gio_hang != None and len(Danh_sach_Gio_hang) > 0):
        Chuoi_Gio_hang += Tao_chuoi_HTML_Gio_hang(Danh_sach_Gio_hang)
    if(request.method =="POST"):
        Chuoi_Thong_tin_Dang_nhap = ""
        Ngay_dat_hang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        Ho_ten = request.form.get("Th_Ho_ten")
        Email = request.form.get("Th_Email")
        So_dien_thoai = request.form.get("Th_So_dien_thoai")
        Dia_chi = request.form.get("Th_Dia_chi") + ", " + request.form.get("Th_Thanh_pho")
        Tong_tien = request.form.get("Th_Thanh_tien")
    
        # Khách vãng lai, chưa tạo tài khoản
        Ma_khach_hang = ""
        if(current_user.is_authenticated == False):
            letters = string.ascii_lowercase 
            random_password = ''.join(random.choice(letters) for i in range(10)) 
            khach_hang = Nguoi_dung(Ma_loai_nguoi_dung = 1, Ho_ten = Ho_ten, Email = Email, Mat_khau = Encode_password(random_password))
            session_1.add(khach_hang)
            try:
                session_1.commit()
                Chuoi_Thong_tin_Dang_nhap +='<br><p> Bạn có thể đăng nhập để kiểm tra trạng thái của đơn hàng.' + \
                                            '<br>    Tên đăng nhập: ' + Email + \
                                            '<br>    Mật khẩu: '+ random_password + '</p>'
                Ma_khach_hang = khach_hang.Ma_nguoi_dung
            except exc.SQLAlchemyError :
                Chuoi_Thong_bao += '<div class="container p-t-75 p-b-100 text-center">'
                Chuoi_Thong_bao += 'Có lỗi, bạn vui lòng thử thanh toán lại'
                Chuoi_Thong_bao += '/div>'
                pass
        else: # Khách hàng đã đăng nhập
            Ma_khach_hang = current_user.Ma_nguoi_dung

        hoa_don = Hoa_don(Ngay_hoa_don = Ngay_dat_hang, Ma_khach_hang = Ma_khach_hang,
                        Dia_chi_giao_hang = Dia_chi, Dien_thoai_nhan_hang = So_dien_thoai, Tong_tien = Tong_tien)
        session_1.add(hoa_don)
        session_1.commit()
        if(Danh_sach_Gio_hang != None and len(Danh_sach_Gio_hang) > 0):
            for san_pham in Danh_sach_Gio_hang:
                chi_tiet_hoa_don = Chi_tiet_hoa_don(Ma_hoa_don = hoa_don.Ma_hoa_don, Ma_san_pham = san_pham['Ma_san_pham'],
                                        So_luong = san_pham['So_luong'], Size = san_pham['Size'], Don_gia = san_pham['Don_gia'])
                session_1.add(chi_tiet_hoa_don)
                session_1.commit()
        Chuoi_Thong_bao += '<div class="container p-t-75 p-b-100 text-center">'
        Chuoi_Thong_bao +='<h4>Đơn hàng '+ str(hoa_don.Ma_hoa_don) +' đã được tạo thành công.'
        Chuoi_Thong_bao +='<br>'
        Chuoi_Thong_bao +='Thông tin đơn hàng sẽ được gởi qua mail '+ Email +' cho bạn.'
        Chuoi_Thong_bao +='<br>'
        Chuoi_Thong_bao +='Cảm ơn bạn đã mua hàng tại Kiehl.'
        Chuoi_Thong_bao +='<br>'
        Chuoi_Thong_bao +='<small><a href="/">Quay lại trang chủ. </a><a href="collections/all">Tiếp tục mua hàng. </a></small>'
        Chuoi_Thong_bao +='</h4></div>'
        # Gởi mail thông tin đơn hàng
        Chuoi_tieu_de = '[Kiehl] Thông báo xác nhận đơn hàng ' + str(hoa_don.Ma_hoa_don)
        msg = Message(Chuoi_tieu_de, sender = 'python244t7cn@gmail.com', recipients = [Email])
        Noi_dung_email = '<p><h1>Kiehl</h1> - ' + Ngay_dat_hang + ' - Đơn hàng '+ str(hoa_don.Ma_hoa_don) +'</p>'+\
                    '</br><strong> Cảm ơn bạn đã mua hàng!</strong>' + \
                    '</br><p> Xin chào '+Ho_ten+', Chúng tôi đã nhận được đặt hàng của bạn và đã sẵn sàng để vận chuyển.'+ \
                    '<br> Chúng tôi sẽ thông báo cho bạn khi đơn hàng được gửi đi.</p>'
        if(Chuoi_Thong_tin_Dang_nhap!=""):
            Noi_dung_email += Chuoi_Thong_tin_Dang_nhap
        Noi_dung_email +='</br></br> Thân!'
        mail.body = Noi_dung_email
        msg.html = mail.body
        mail.send(msg)
        session.pop('gio_hang', None)
        return render_template("Checkout.html", Chuoi_Thong_bao = Markup(Chuoi_Thong_bao))
    return render_template("Gio_hang.html", 
                        Th_Chuoi_gio_hang=Markup(Chuoi_Gio_hang),
                           Danh_sach_Gio_hang=Danh_sach_Gio_hang)


@app.route("/add-to-cart", methods=['POST'])
def add_to_cart():
    item = request.form.get('item')
    item = json.loads(item)    
    Cap_nhat_Danh_sach_Gio_hang(session, item)
    session['gio_hang'] = session['gio_hang']
    return jsonify(len=len(session['gio_hang']), html=render_template('Layouts/cart.html'))

        

