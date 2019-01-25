from KiehlShop import app
from flask import Flask, render_template, Markup, session, request, flash, redirect
from flask_ckeditor import CKEditor
from flask_mail import Mail, Message
from sqlalchemy import exc
from KiehlShop.Xu_ly.Xu_ly_3L import *
from KiehlShop.Xu_ly.Xu_ly_Form import *

ckeditor = CKEditor(app)

Danh_sach_Danh_muc = Doc_Danh_sach_Loai_San_Pham()
Danh_sach_San_pham = Doc_Danh_sach_San_Pham()

Danh_muc_chinh = ""
for loai in Danh_sach_Danh_muc:
    Danh_muc_chinh += Tao_chuoi_HTML_Loai_San_Pham(loai)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'python244t7cn@gmail.com'
app.config['MAIL_PASSWORD'] = 'Python244'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    # Cho gio hang =None moi khi login vao --> remove sau
    session.pop('gio_hang',None)
    global Danh_sach_San_pham
    global Danh_muc_chinh
    Th_Danh_sach_San_pham_Hot = ""
    Modal_san_pham = ""
    # Search
    if (request.method == 'POST'):
        if (request.form.get("Th_Chuoi_Tra_cuu") != None and request.form.get("Th_Chuoi_Tra_cuu") != ""):
            return redirect(url_for('search', Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")))
    # Tao the hien cho trang chu
    i = 0
    while(i < 8):
        Ma_so = i + 1
        san_pham = Lay_San_pham_theo_Ma(
                Danh_sach_San_pham, "SP_" + str(Ma_so))
        Th_Danh_sach_San_pham_Hot += Tao_chuoi_HTML_San_Pham(san_pham)
        Modal_san_pham += Tao_modal(san_pham)
        i += 1
    return render_template("Trang_chu.html",
                           Th_Danh_sach_San_pham_Hot=Markup(
                               Th_Danh_sach_San_pham_Hot),
                            Modal_san_pham=Markup(Modal_san_pham))


@app.route("/Kiehl", methods=['GET','POST'])
def Gioi_thieu():
    # Search
    if (request.method == 'POST'):
        if (request.form.get("Th_Chuoi_Tra_cuu") != None and request.form.get("Th_Chuoi_Tra_cuu") != ""):
            return redirect(url_for('search', Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")))
    return render_template("Gioi_thieu.html", Loai_san_pham_cha=Markup(Danh_muc_chinh))


@app.route("/collections/all", methods=['GET', 'POST'])
def productAll():
    global Danh_sach_San_pham
    global Danh_muc_chinh
    Th_Danh_sach_San_pham = ""
    Modal_san_pham = ""
    # Search
    if (request.method == 'POST'):
        if (request.form.get("Th_Chuoi_Tra_cuu") != None and request.form.get("Th_Chuoi_Tra_cuu") != ""):
            return redirect(url_for('search', Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")))
    # Trang san pham
    Th_Danh_sach_San_pham += '<div class="row isotope-grid" id="myList">'
    for san_pham in Danh_sach_San_pham:
        Th_Danh_sach_San_pham += Tao_chuoi_HTML_San_Pham(san_pham)
        Modal_san_pham += Tao_modal(san_pham)
    Th_Danh_sach_San_pham += '</div>'
    return render_template("San_pham.html", Loai_san_pham_cha=Markup(Danh_muc_chinh),
                            Th_Danh_sach_San_pham=Markup(Th_Danh_sach_San_pham),
                            Modal_san_pham=Markup(Modal_san_pham))


@app.route("/product/<string:Ma_so>", methods=['GET', 'POST'])
def san_pham_chi_tiet(Ma_so):
    global Danh_sach_San_pham
    # Search
    if (request.method == 'POST'):
        if (request.form.get("Th_Chuoi_Tra_cuu") != None and request.form.get("Th_Chuoi_Tra_cuu") != ""):
            return redirect(url_for('search', Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")))
    # San pham chi tiet
    San_pham = Lay_San_pham_theo_Ma(Danh_sach_San_pham, Ma_so)
    breadcrum = Tao_breadcrum(San_pham)
    Chuoi_hinh_anh = Tao_chuoi_HTML_Hinh_San_pham_Chi_tiet(San_pham)
    Chuoi_Mau_sac = Tao_chuoi_Mau_sac_San_pham(San_pham)
    Chuoi_thong_tin_SP = Tao_chuoi_Thong_tin_San_pham_Chi_tiet(San_pham)
    return render_template("San_pham_chi_tiet.html",
                            Breadcrum_Chi_Tiet=Markup(breadcrum), Th_Hinh_chi_tiet=Markup(Chuoi_hinh_anh),
                            Mau_sac_san_pham=Markup(Chuoi_Mau_sac), Thong_tin_SP=Markup(Chuoi_thong_tin_SP), 
                            Ma_so=Ma_so, Don_gia=San_pham['Don_gia'])



@app.route("/search?<string:Chuoi_tra_cuu>", methods=['GET','POST'])
def search(Chuoi_tra_cuu):  
    chuoi_tim_kiem = ""
    if (request.method == 'POST'):
        if (request.form.get("Th_Chuoi_Tra_cuu") != None and request.form.get("Th_Chuoi_Tra_cuu") != ""):
            chuoi_tim_kiem = request.form.get("Th_Chuoi_Tra_cuu")
    else:
        chuoi_tim_kiem = Chuoi_tra_cuu
    print(chuoi_tim_kiem)
    Danh_sach_San_pham_Search = Tra_cuu_san_pham(chuoi_tim_kiem, Danh_sach_San_pham)
    Th_Danh_sach_San_pham = ""
    Modal_san_pham = ""
    if (len(Danh_sach_San_pham_Search)>0):
        Th_Danh_sach_San_pham += '<div class="row isotope-grid" id="myList">'
        for san_pham in Danh_sach_San_pham_Search:
            Th_Danh_sach_San_pham += Tao_chuoi_HTML_San_Pham(san_pham)
            Modal_san_pham += Tao_modal(san_pham)
        Th_Danh_sach_San_pham +='</div>'
    else:
        Th_Danh_sach_San_pham = '<div class="text-center p-t-16"><strong>Không tìm thấy nội dung bạn yêu cầu</strong></br>Không tìm thấy "'+chuoi_tim_kiem +'". Vui lòng kiểm tra chính tả, sử dụng các từ tổng quát hơn và thử lại!</div>'
    return render_template("Tim_kiem.html",
                           Th_Danh_sach_San_pham=Markup(Th_Danh_sach_San_pham),
                            Modal_san_pham=Markup(Modal_san_pham))

@app.route("/contact", methods=['GET', 'POST'])
def lien_he():
    chuoi_ket_qua = ""
    form = From_Lien_He()
    Chuoi_Thong_bao =""
    # Search
    if (request.method == 'POST'):
        if (request.form.get("Th_Chuoi_Tra_cuu") != None and request.form.get("Th_Chuoi_Tra_cuu") != ""):
            return redirect(url_for('search', Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")))
    # Lien he
    if form.validate_on_submit():
        Ho_ten = request.form['Th_Ho_ten']
        Email = request.form['Th_Email'].strip()
        So_dien_thoai = request.form['Th_So_dien_thoai']
        Noi_dung = request.form['Th_Noi_dung']
        # ghi len he
        lien_he = Lien_he(Ho_ten=Ho_ten, Email=Email,
                        So_dien_thoai=So_dien_thoai, Noi_dung = Noi_dung)
        session_1.add(lien_he)
        try:
            session_1.commit()
            # gui mail
            Ngay = datetime.now().strftime('%d-%m-%Y')
            Chuoi_tieu_de = '[Kiehl] Thông báo xác nhận mail'
            msg = Message(Chuoi_tieu_de, sender = 'python244t7cn@gmail.com', recipients = [Email])
            Noi_dung_email = '<p>Kiehl - ' + Ngay + '</p>'+\
                    '</br> Kính gởi: ' + Ho_ten + ', <br/> Cảm ơn quý khách đã dành thời gian cho chúng tôi.' + \
                    '</br> Chúng tôi muốn thông tin lại nội dung quý khách đã gởi như sau: </br>' +\
                    '</br><p style="margin-left:15px"> Khách hàng: ' + Ho_ten + \
                    '<br/> Số điện thoại: ' + str(So_dien_thoai) + \
                    '<br/> Email: ' + Email + \
                    '<br/> Nội dung câu hỏi: "' + Noi_dung + '"</p>' + \
                    '</br><br/> Chúng tôi sẽ phản hồi lại bạn trong thời gian sớm nhất!!! '
            mail.body = Noi_dung_email
            msg.html = mail.body
            mail.send(msg)
            Chuoi_Thong_bao += '<div class="text-primary text-center"> Chúng tôi đã nhận được thông tin và sẽ phản hồi lại bạn trong thời gian sớm nhất</div>'
        except exc.SQLAlchemyError:
            Chuoi_Thong_bao = '<div class="text-danger text-center">Xin lỗi vì sự bất tiện này. Vui lòng thử lại lần sau.</div>'
        pass
    else:
        flash("Error: Cần nhập đủ các nội dung yêu cầu")
    return render_template('Lien_he.html', form=form, Chuoi_ket_qua= Markup(chuoi_ket_qua), 
                        Chuoi_Thong_bao = Markup(Chuoi_Thong_bao))
