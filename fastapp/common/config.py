from dataclasses import dataclass
from os import path, environ
import logging
from Scripts.fastapp.common.consts import DB_USER, DB_PW, DB_ADD, DB_PORT, DB_NAME
base_dir = path.dirname(path.abspath(__file__))
print(base_dir)
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
    PROJ_RELOAD: bool = True
    # postgresql://federer:grandestslam@localhost:5432/tennis
    # user, password, host, port, db
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PW}@{DB_ADD}:{DB_PORT}/{DB_NAME}"

    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]

@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False

    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]

# @dataclass
# class PathConfig(Config):
#     # Folder path
#     SAMPLE_FOLDER_PATH = r'D:\\Project\\tesseract\\sample\\'
#     TRAIN_FOLDER_PATH = r'D:\\Project\\tesseract\\tesseract_Project\\Scripts\\tp\\ml\\train\\'

#     # File path
#     KEYWORD_DICTIONARY_PATH = r'D:\\Project\\tesseract\\tesseract_Project\Scripts\\tp\\nlp\\dic.txt'
#     DEFAULT_CSV_PATH = r'D:\\Project\\tesseract\\tesseract_Project\\Scripts\\tp\\ml\\train\\model.csv'

#     # Save h2o model
#     H2O_MODEL_PATH = r'D:\\Project\\tesseract\\model'

#     USING_MODEL_PATH = H2O_MODEL_PATH + '/GBM_1_AutoML_20210324_171907'


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))

# print(asdict(LocalConfig()))

def get_logger():
    """로거 인스턴스 반환
    """

    __logger = logging.getLogger('logger')

    # 로그 포멧 정의
    formatter = logging.Formatter(
        'BATCH##AWSBATCH##%(levelname)s##%(asctime)s##%(message)s >> @@file::%(filename)s@@line::%(lineno)s')
    # 스트림 핸들러 정의
    stream_handler = logging.StreamHandler()
    # 각 핸들러에 포멧 지정
    stream_handler.setFormatter(formatter)
    # 로거 인스턴스에 핸들러 삽입
    __logger.addHandler(stream_handler)
    # 로그 레벨 정의
    __logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('my.log')
    file_handler.setFormatter(formatter)
    __logger.addHandler(file_handler)

    return __logger