import os
import konfig as konf
import platform
import logging

def get_logger():
    """로거 인스턴스 반환
    """

    __logger = logging.getLogger('logger')

    # Check handler exists
    if len(__logger.handlers) > 0:
        return __logger # Logger already exists
    # 로그 레벨 정의
    __logger.setLevel(logging.DEBUG)

    # 로그 포멧 정의
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] # %(message)s >> [ file::%(filename)s | @@line::%(lineno)s ]')

    # 스트림 핸들러 정의
    stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.DEBUG)
    # 각 핸들러에 포멧 지정
    stream_handler.setFormatter(formatter)
    # 로거 인스턴스에 핸들러 삽입
    __logger.addHandler(stream_handler)

    # 파일 핸들러
    file_handler = logging.FileHandler('my.log')
    file_handler.setFormatter(formatter)
    __logger.addHandler(file_handler)

    return __logger

logger = get_logger()

JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"
MAX_API_KEY = 3
MAX_API_WHITELIST = 10

CURRENT_OS = platform.system() # mac: Darwin
logger.info(f"CURRENT_OS is {CURRENT_OS}")
# Folder Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # fastapp/
logger.info(f'BASE_PATH : {BASE_DIR}')

# Common Path
COMMON_PATH = os.path.join(BASE_DIR, 'common')
KEYWORD_DICTIONARY_PATH = os.path.join(COMMON_PATH, 'dic.txt')

# Addreses Path
ADDRESS_PATH = os.path.join(COMMON_PATH, 'address')
ADDRESS_RoGil = os.path.join(ADDRESS_PATH, 'rogil.txt')
ADDRESS_SiGunGu = os.path.join(ADDRESS_PATH, 'sigungu.txt')
ADDRESS_UmMyunDong = os.path.join(ADDRESS_PATH, 'umyundong.txt')



# Config Path
_CONFIG_PATH = os.path.join(COMMON_PATH, 'conf.ini')
logger.info(f'CONFIG_PATH : {_CONFIG_PATH}')
cc = konf.Config(_CONFIG_PATH)



if CURRENT_OS == 'Linux': # 'Windows', 'MacOS'
    """Upload File Directory
    Create target Directory if don't exist"""
    storage = cc.get_map("file")
    UPLOAD_DIRECTORY = storage['STORAGE']
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.mkdir(UPLOAD_DIRECTORY)
        logger.info(f"Directory {UPLOAD_DIRECTORY} Created ")
    else:
        logger.info(f"Directory {UPLOAD_DIRECTORY} already exists")


DATA_FOLDER_PATH = os.path.join(BASE_DIR, 'data')
SAMPLE_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'samples')
TRAIN_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'train')

RESULT_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'results')
REGEX_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'regex')
UPLOAD_DIRECTORY = os.path.join(RESULT_FOLDER_PATH, 'uploadfiles')

# PyCaret Model Path
ML_MODEL_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'ml_model')
ML_MODEL_PATH = os.path.join(ML_MODEL_FOLDER_PATH, 'auto_ml_model_0623')


# DEFAULT_CSV_PATH = f'{BASE_DIR}\\'


# URL
xedm = cc.get_map("xedm")
X_URL = xedm['ADD']
X_PORT = xedm['PORT']
XEDM_URL = f'{X_URL}:{X_PORT}'
logger.info(f'[ XEDM URL: {XEDM_URL} ]')

# uvicorn Server setting
app = cc.get_map("server")
APP_HOST_ADD=app['HOST']
APP_PORT=app['PORT']
logger.info(f'[ AI SERVER INFO: {APP_HOST_ADD}:{APP_PORT} ]')

# DB Setting
db = cc.get_map("db")
DB_USER = db['USER']
DB_PW = db['PW']
DB_ADD = db['ADD']
DB_PORT = db['PORT']
DB_NAME = db['NAME']
logger.info(f'[ DB INFO : postgresql://{DB_USER}:{DB_PW}@{DB_ADD}:{DB_PORT}/{DB_NAME} ]')

# support EXT
SUPPORT_EXT = ['pdf','pptx','docx','csv','xlsx','txt','json','xml']
_TODO=['hwp','html']
# ','.join(SUPPORT_EXT) 
