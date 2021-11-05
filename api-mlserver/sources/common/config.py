from dataclasses import dataclass
from os import path, environ
# import logging
from common.consts import DB_USER, DB_PW, DB_NAME

base_dir = path.dirname(path.abspath(__file__))
print(f'BASE_DIRECTORY : {base_dir}')

# dataclass 데코레이터 이유: 해당 클래스를 Dict 형태로 추출해서 사용 가능
@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    """
    Local 환경 설정
    """
    PROJ_RELOAD: bool = True
    # postgresql://federer:grandestslam@localhost:5432/tennis
    # user, password, host, port, db
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PW}@postgres-xedm/{DB_NAME}"

    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]

@dataclass
class ProdConfig(Config):
    """
    Product 환경 설정
    """
    PROJ_RELOAD: bool = False

    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]

def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))
