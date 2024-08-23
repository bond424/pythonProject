from sqlalchemy.dialects.mysql import MEDIUMBLOB, LONGTEXT
from sqlalchemy import Column, String, Integer, TEXT, inspect, BIGINT, Float, DateTime, JSON, DECIMAL, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base, as_declarative
from geoalchemy2 import Geometry

# LargeBinary = BYTEA = BLOB

Base = declarative_base()

class fileListTable(Base):
    __tablename__ = 'fileList'
    fileid = Column(String(255), primary_key=True)
    filename = Column(String(255))
    filetype = Column(String(15))
    filepath = Column(String(255))

class vctlayer(Base):
    __tablename__ = 'vectorlayersTest'
    layerid = Column(String(50), primary_key=True)
    label = Column(String(10))

class sigutable(Base):
    __tablename__ = 'euckr_table_949_5179'
    id_0 = Column(Integer, primary_key=True)
    geom = Column(Geometry('GEOMETRY', srid=5179))
    gm_layer = Column(String(21))
    gm_type = Column(String(17))
    serial_number = Column(String(254))
    street_number = Column(String(254))
    land_category = Column(String(254))
    number_address = Column(String(254))
    number_address_1 = Column(String(254))
    cadastre = Column(String(254))
    incorporation_area = Column(String(254))
    owner = Column(String(254))
    owner_ct = Column(String(254))
    related_person = Column(String(254))
    related = Column(String(254))
    related_person_1 = Column(String(254))
    note = Column(String(254))
    dong = Column(String(254))
    gu = Column(String(254))
    wkt = Column(String(254))
    area = Column(String(254))
    sgg_oid = Column(String(254))
    jibun = Column(String(254))
    pnu = Column(String(254))
    col_adm_se = Column(String(254))
    layer = Column(String(254))
    ufid = Column(String(254))
    bjcd = Column(String(254))
    name = Column(String(254))
    divi = Column(String(254))
    scls = Column(String(254))
    fmta = Column(String(254))
    id = Column(String(254))
    bchk = Column(String(254))
    path = Column(String(254))
