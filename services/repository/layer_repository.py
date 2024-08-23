from fastapi import Depends
from sqlalchemy import func, union, and_, or_, exists
from sqlalchemy.orm import Session, aliased
from utils.postgre_connect import get_db
from utils.filesve_connect import get_filedb
import json
from geoalchemy2.shape import to_shape
from models.model import vctlayer, sigutable, fileListTable
from dbfread import DBF
from io import BytesIO
import os
import tempfile


class Layer_Repository:
    def __init__(self, db_session: Session = Depends(get_db)) -> None:
        self.db = db_session

    def get_test_layer(self):
        data = self.db.query(vctlayer).all()
        return data


class Geofile_Repository:
    def __init__(self, db_session: Session = Depends(get_filedb)) -> None:
        self.db = db_session

    def get_test_def(self):
        data = self.db.query(sigutable).all()
        json_data = []
        for row in data:
            # GeoAlchemy2에서 GeoJSON 형식으로 변환
            geom_json = to_shape(row.geom).__geo_interface__
            json_data.append({
                'id_0': row.id_0,
                'geom': geom_json,
                'gm_layer': row.gm_layer,
                'gm_type': row.gm_type,
            })
        return json_data

    def set_DB_ShpFiles(self, files_info):
        for i in files_info:
            insert_db_name = fileListTable(
                fileid=i.get('filename'),
                filename=i.get('filename').split('.')[0],
                filetype=i.get('filename').split('.')[1],
                filepath=i.get('filepath')
            )
            self.db.add(insert_db_name)
        self.db.commit()
        getList = self.db.query(fileListTable).all()
        return getList

    def get_DB_ShpFiles(self, filenm):
        getList = self.db.query(fileListTable).filter(fileListTable.filename == filenm).all()
        return getList

    def get_all_DBFiles(self):
        getList = self.db.query(fileListTable).filter(fileListTable.filetype == 'shp').all()
        return getList
