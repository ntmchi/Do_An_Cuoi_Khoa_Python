from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from sqlalchemy import create_engine
from flask_login import UserMixin, LoginManager, current_user, login_user

engine = create_engine('sqlite:///KiehlShop/Du_lieu/ban_hang_truc_tuyen.db?check_same_thread=False')
Base = declarative_base()

class Loai_san_pham(Base):
    __tablename__ = 'Loai_san_pham'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_loai = Column(Integer, primary_key = True)
    Ten_loai = Column(String(50), nullable = False)
    Hinh_dai_dien = Column(String(200), nullable = False)
    def __str__(self):
        return self.Ten_loai

class San_pham(Base):
    __tablename__ = 'San_pham'
    Ma_san_pham = Column(String(50), nullable = False, primary_key = True)
    Ten_san_pham = Column(String(100), nullable = False)
    Ma_loai = Column(Integer, ForeignKey('Loai_san_pham.Ma_loai'), nullable = False)
    ma_loai_san_pham = relation(Loai_san_pham, backref = "ma_loai")
    Mo_ta = Column(String())
    Chat_lieu = Column(String())
    Don_gia = Column(Integer, nullable = False)
    Tinh_trang = Column(Integer, nullable = False, default = 1)

class San_pham_chi_tiet(Base):
    __tablename__ = 'San_pham_chi_tiet'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_san_pham_chi_tiet = Column(Integer, primary_key = True)
    Ma_san_pham = Column(Integer,  ForeignKey('San_pham.Ma_san_pham'))
    Mau_sac = Column(String(100),nullable = False)
    Size = Column(String(5), nullable = False)
    So_luong = Column(Integer, nullable = False)
    So_luong_da_ban = Column(Integer)
    san_pham = relation(San_pham, backref = "ma_san_pham")

class Hinh_san_pham(Base):
    __tablename__ = 'Hinh_san_pham'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_hinh_anh = Column(Integer, primary_key = True)
    Ma_san_pham = Column(Integer,  ForeignKey('San_pham.Ma_san_pham'))
    ma_san_pham_chi_tiet = relation(San_pham, backref = "ma_san_pham_chi_tiet")
    Hinh_anh = Column(String(100),nullable = False)
    def __str__(self):
        return self.Hinh_anh

class Cua_hang(Base):
    __tablename__ = 'Cua_hang'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_cua_hang = Column(Integer, primary_key = True)
    Ten_cua_hang = Column(String(200),nullable = False)
    Dia_chi = Column(String(200),nullable = False)
    Dien_thoai = Column(String(100))

    def __str__(self):
        return self.Ten_cua_hang

class Lien_he(Base):
    __tablename__ = 'Lien_he'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_lien_he = Column(Integer, primary_key = True)
    Ho_ten = Column(String(100),nullable = False)
    Email = Column(String(100),nullable = False)
    So_dien_thoai = Column(String(15),nullable = False)
    Noi_dung = Column(String(),nullable = False)

class Loai_nguoi_dung(Base):
    __tablename__ = 'Loai_nguoi_dung'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_loai_nguoi_dung = Column(Integer, primary_key = True)
    Ten_loai_nguoi_dung = Column(String(100), nullable = False)

    def __str__(self):
        return self.Ten_loai_nguoi_dung

class Nguoi_dung(Base):
    __tablename__ = 'Nguoi_dung'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_nguoi_dung = Column(Integer, primary_key = True)
    Ma_loai_nguoi_dung = Column(Integer, ForeignKey('Loai_nguoi_dung.Ma_loai_nguoi_dung'))
    loai_nguoi_dung = relation(Loai_nguoi_dung, backref = "ma_loai_nguoi_dung")
    Ho_ten = Column(String(100), nullable = False)
    Email = Column(String(100), nullable = False)
    Mat_khau = Column(String(255), nullable = False)

    def get_id(self):
        return self.Ma_nguoi_dung
    def is_authenticated(self):
        return True
    
class Hoa_don(Base):
    __tablename__ = 'Hoa_don'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_hoa_don = Column(Integer, primary_key = True)
    Ngay_hoa_don = Column(String(), nullable = False)
    Ma_khach_hang = Column(Integer, ForeignKey('Nguoi_dung.Ma_nguoi_dung'))
    Dia_chi_giao_hang = Column(String(), nullable = False)
    Dien_thoai_nhan_hang = Column(String(20), nullable = False)
    ma_khach_hang = relation(Nguoi_dung, backref = "ma_khach_hang")
    Tong_tien = Column(Float, nullable = False)

class Chi_tiet_hoa_don(Base):
    __tablename__ = 'Chi_tiet_hoa_don'
    __table_args__ = {'sqlite_autoincrement': True}
    Ma_chi_tiet_hoa_don = Column(Integer, primary_key = True)
    Ma_hoa_don = Column(Integer, ForeignKey('Hoa_don.Ma_hoa_don'))
    hoa_don = relation(Hoa_don, backref = "ma_hoa_don_chi_tiet")
    Ma_san_pham = Column(String(50), ForeignKey('San_pham.Ma_san_pham'))
    san_pham = relation(San_pham, backref = "ma_san_pham_trong_hoa_don")
    So_luong = Column(Integer, nullable = False)
    Size = Column(String(5),nullable = False)
    Don_gia =  Column(Integer, nullable = False)

    
class Quan_tri(Base, UserMixin):
    __tablename__ = 'Quan_tri'
    id = Column(Integer, primary_key= True) 
    Ho_ten = Column(String(200), nullable=False)
    Ten_dang_nhap = Column(String(50), nullable=False) 
    Mat_khau = Column(String(255), nullable=False) 


if __name__=="__main__":
    Base.metadata.create_all(engine)

  