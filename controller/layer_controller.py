from fastapi import APIRouter, Depends, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse, Response
from typing import List
import io
import logging
from schema.errors import Errors
from fastapi_router_controller import Controller

from services.layer_service import Layer_Services

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/layerController')
controller = Controller(router, openapi_tag={
    'name': 'layer_con'
})


@controller.use()
@controller.resource()
class LayerController:
    def __init__(self, service: Layer_Services = Depends()) -> None:
        self.service = service

    @controller.route.get(
        '/vectorlayer',
        tags=['vcttestname'],
        # response_model=List
    )
    def get_test_layer(self):
        try:
            layer = self.service.get_test_layer()
            return layer
        except Exception as error:
            logger.error(f'Error : {error}')
            return Errors.HTTP_500_INTERNAL_SERVER_ERROR


