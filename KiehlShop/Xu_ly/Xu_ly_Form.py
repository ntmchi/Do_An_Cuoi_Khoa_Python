from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField, IntegerField, SubmitField, RadioField, SelectField, PasswordField, StringField
from wtforms.widgets import PasswordInput
from wtforms import validators, ValidationError
from flask_ckeditor import CKEditorField

class From_Lien_He(FlaskForm):
    Th_Ho_ten = TextField("Tên khách hàng",[validators.Required("Vui lòng nhập tên."), validators.length(min=2,max=-1, message='Độ dài của họ tên lớn hơn 2 kí tự')])
    Th_Email = TextField("Email", [validators.Required("Vui lòng nhập email"), validators.Email("Email phải đúng quy định"), validators.length(6,-1, message='Độ dài của họ tên lớn hơn 6 kí tự')])
    Th_So_dien_thoai = IntegerField("Số điện thoại", [validators.Required("Vui lòng nhập số điện thoại")])
    Th_Noi_dung = CKEditorField("Nội dung",[validators.Required("Vui lòng nhập nhận xét.")])
    Th_Submit = SubmitField("Gửi")


