import controller

from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.exceptions import RequestValidationError
from fastapi_router_controller import Controller, ControllersTags
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html)
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    openapi_tags=ControllersTags,
    docs_url=None, redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in Controller.routers():
    app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

add_pagination(app)
