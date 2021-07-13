import os, sys
from dataclasses import asdict
from typing import Optional

import uvicorn
# from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader


# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.middleware.cors import CORSMiddleware

# from Scripts.fastapp.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX

# from Scripts.fastapp.database.conn import db
# from Scripts.fastapp.common.config import conf
# from Scripts.fastapp.middlewares.token_validator import access_control
# from Scripts.fastapp.middlewares.trusted_hosts import TrustedHostMiddleware
from sub_main import create_app
from common.consts import APP_HOST_ADD, APP_PORT
# from Scripts.fastapp.routes import pid, ml, xedm

# auto_error False 중요 Swagger 위에 Authorization 버튼 만듬
API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
app = create_app()
def serve_dev():
    uvicorn.run("main:app", host=APP_HOST_ADD, port=APP_PORT, reload = True)

def serve_app():
    uvicorn.run( app , host=APP_HOST_ADD, port=APP_PORT)


if __name__ == "__main__":
    try:
        os.chdir(sys._MEIPASS)
        print(f'## SERVICE MODE / sys_MEIPASS : {sys._MEIPASS}')
        serve_app()
    except:
        os.chdir(os.getcwd())
        print(f'## DEV MODE: {os.chdir(os.getcwd())} ##')
        serve_dev()
    # uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=False, workers=1)