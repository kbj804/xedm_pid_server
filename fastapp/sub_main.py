from dataclasses import asdict
from typing import Optional

from fastapi import FastAPI


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware


from Scripts.fastapp.database.conn import db
from Scripts.fastapp.common.config import conf
from Scripts.fastapp.middlewares.token_validator import access_control
from Scripts.fastapp.middlewares.trusted_hosts import TrustedHostMiddleware

from Scripts.fastapp.routes import pid, ml, xedm

def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    # 데이터 베이스 이니셜라이즈

    # 레디스 이니셜라이즈

    # 미들웨어 정의
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    # app.add_middleware(AccessControl, except_path_list=EXCEPT_PATH_LIST, except_path_regex=EXCEPT_PATH_REGEX)
    
    # 개발용. 일단 누구든 들어올 수 있도록... 개발중에만 이렇게해야함.. 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=["/health"])
    # 삽질.. 미들웨어는 가장 밑에있는 미들웨어부터 시작함. access_control이 CORS보다 밑에있으면 무조건 에러남.. access control이 가장 마지막으로 실행 되어야 한다


    # 라우터 정의
    # app.include_router(index.router)
    app.include_router(xedm.router, tags=["Xedm"], prefix="/api")
    app.include_router(ml.router, tags=["Machine Learning"], prefix="/api")
    # app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    app.include_router(pid.router, tags=["Personal Information Detection"], prefix="/api")
    # app.include_router(services.router, tags=["Services"], prefix="/api")
    # Dpends 하면 자물쇠 생김 - dependencies 를 안넣으면 토큰 검사 안함
    # app.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    
    return app

