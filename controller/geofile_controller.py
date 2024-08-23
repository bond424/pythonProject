from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, StreamingResponse, Response
from typing import List
import io
import os
import logging
from schema.errors import Errors
from fastapi_router_controller import Controller
from schema.schema import SigutableModel
import json
import zipfile
from io import BytesIO
import re
import urllib.parse
from dbfread import DBF


from services.geofile_service import Geofile_Services

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/geoFileController')
controller = Controller(router, openapi_tag={
    'name': 'geofile_con'
})

directory = '../uploaddir/shpfiles'


@controller.use()
@controller.resource()
class GeoFileController:
    def __init__(self, service: Geofile_Services = Depends()) -> None:
        self.service = service

    @controller.route.get(
        '/euckr_epsg',
        tags=['euckr_epsg5179'],
        response_model=List
    )
    async def get_test_layer(self):
        try:
            layer = self.service.get_test_layer()
            return layer
        except Exception as error:
            logger.error(f'Error : {error}')
            return Errors.HTTP_500_INTERNAL_SERVER_ERROR

    def get_unique_filename(self, directory, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = f"{base}({counter}){ext}"
            counter += 1
        return new_filename

    @controller.route.post(
        '/saveShpFiles',
        tags=['save_Files']
    )
    async def set_DB_ShpFiles(self, file: UploadFile = File(...), file2: UploadFile = File(...), file3: UploadFile = File(...)):
        os.makedirs(directory, exist_ok=True)

        shp_filename = self.get_unique_filename(directory, file.filename)
        dbf_filename = self.get_unique_filename(directory, file2.filename)
        shx_filename = self.get_unique_filename(directory, file3.filename)

        shp_filepath = os.path.join(directory, shp_filename)
        dbf_filepath = os.path.join(directory, dbf_filename)
        shx_filepath = os.path.join(directory, shx_filename)

        shpcontents = await file.read()
        dbfcontents = await file2.read()
        shxcontents = await file3.read()

        with open(shp_filepath, "wb") as f:
            f.write(shpcontents)
        with open(dbf_filepath, "wb") as f:
            f.write(dbfcontents)
        with open(shx_filepath, "wb") as f:
            f.write(shxcontents)

        # dbf_table = DBF(dbf_filepath, encoding='euc-kr')
        #
        # records = [record for record in dbf_table]

        files_info = [
            {"filename": shp_filename, "filepath": shp_filepath},
            {"filename": dbf_filename, "filepath": dbf_filepath},
            {"filename": shx_filename, "filepath": shx_filepath},
        ]
        try:
            layer = self.service.set_DB_ShpFiles(files_info)
            return layer
        except Exception as error:
            logger.error(f'Error : {error}')
            return Errors.HTTP_500_INTERNAL_SERVER_ERROR

    @controller.route.get(
        '/downloadShpFiles',
        tags=['save_Files']
    )
    async def get_DB_ShpFiles(self, filename):
        try:
            # decoded_filename = json.loads(filename)['filename']
            jsonobj = json.loads(filename)
            filenm = jsonobj.get('filename')
            # filenm = decoded_filename.encode('iso-8859-1').decode('utf-8')

            get_files = self.service.get_DB_ShpFiles(filenm)
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i in get_files:
                    file_id = i.fileid
                    filepath = os.path.join(directory, file_id)
                    if os.path.exists(filepath):
                        zip_file.write(filepath, arcname=file_id)
                    else:
                        raise HTTPException(status_code=404, detail="File not found")

            zip_buffer.seek(0)

            quoted_filenm = filenm.encode('utf-8').decode('iso-8859-1') + ".zip"

            return StreamingResponse(zip_buffer, media_type="application/zip",
                                     headers={"Content-Disposition": f"attachment; filename*=UTF-8\'\'%s'{quoted_filenm}"})
        except Exception as error:
            logger.error(f'Error : {error}')
            return Errors.HTTP_500_INTERNAL_SERVER_ERROR

    @controller.route.get(
        '/getallDBFiles',
        tags=['getallDBFiles'],
    )
    async def get_all_DBFiles(self):
        try:
            get_all_Files = self.service.get_all_DBFiles()
            return get_all_Files
        except Exception as error:
            logger.error(f'Error : {error}')
            return Errors.HTTP_500_INTERNAL_SERVER_ERROR

    @controller.route.get(
        '/downloadShp',
        tags=['save_Files']
    )
    async def get_on_ShpFiles(self, filename):
        try:
            jsonobj = json.loads(filename)
            filenm = jsonobj.get('filename')
            filepath = os.path.join(directory, filenm)
            quoted_filenm = filenm.encode('utf-8').decode('iso-8859-1')
            if os.path.exists(filepath):
                return FileResponse(filepath, media_type='application/octet-stream',
                                    headers={"Content-Disposition": f"attachment; filename*=UTF-8\'\'%s'{quoted_filenm}"})
            else:
                raise HTTPException(status_code=404, detail="File not found")
        except Exception as error:
            logger.error(f'Error : {error}')
            return Errors.HTTP_500_INTERNAL_SERVER_ERROR

    @controller.route.get(
        '/startdbfset',
        tags=['startdbfset']
    )
    async def set_start_dbf(self, param):
        try:
            jsonobj = json.loads(param)
            filenm = jsonobj.get('filenm')
            shpfilepath = os.path.join(directory, jsonobj.get('shp'))
            dbffilepath = os.path.join(directory, jsonobj.get('dbf'))
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                if os.path.exists(shpfilepath) and os.path.exists(dbffilepath):
                    zip_file.write(shpfilepath, arcname=jsonobj.get('shp'))
                    zip_file.write(dbffilepath, arcname=jsonobj.get('dbf'))
                else:
                    raise HTTPException(status_code=404, detail="File not found")

            zip_buffer.seek(0)

            quoted_filenm = filenm.encode('utf-8').decode('iso-8859-1') + ".zip"

            return StreamingResponse(zip_buffer, media_type="application/zip",
                                     headers={"Content-Disposition": f"attachment; filename*=UTF-8\'\'%s'{quoted_filenm}"})
        except Exception as error:
            logger.error(f'Error : {error}')
            return Errors.HTTP_500_INTERNAL_SERVER_ERROR
