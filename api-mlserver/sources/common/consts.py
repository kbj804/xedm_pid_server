import os
import konfig as konf
import platform
from utils.logger_handler import get_logger

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
logger.info(f'consts.py - BASE_PATH : {BASE_DIR}')

# Common Path
COMMON_PATH = os.path.join(BASE_DIR, 'common')
KEYWORD_DICTIONARY_PATH = os.path.join(COMMON_PATH, 'dic.txt')

# Addreses Path
ADDRESS_PATH = os.path.join(COMMON_PATH, 'address')
ADDRESS_RoGil = os.path.join(ADDRESS_PATH, 'rogil.txt')
ADDRESS_SiGunGu = os.path.join(ADDRESS_PATH, 'sigungu.txt')
ADDRESS_UmMyunDong = os.path.join(ADDRESS_PATH, 'umyundong.txt')

# Image preprocessing Path
UTILS_PATH = os.path.join(BASE_DIR, 'utils')
FILE_MOUDULE_PATH = os.path.join(UTILS_PATH, 'file_module')

# Image output Dir check
IMG_OUTPUT_PATH = os.path.join(FILE_MOUDULE_PATH, 'img_output')
if not os.path.exists(IMG_OUTPUT_PATH):
    os.mkdir(IMG_OUTPUT_PATH)
    logger.info(f"Directory {IMG_OUTPUT_PATH} Created ")
else:
    logger.info(f"Directory {IMG_OUTPUT_PATH} already exist ")

IMG_OUTPUT_PATH = '/ocr_work'
IMG_OUTPUT = os.path.join(IMG_OUTPUT_PATH, 'output')
IMG_INPUT = os.path.join(IMG_OUTPUT_PATH, 'input')

if not os.path.exists(IMG_OUTPUT):
    os.mkdir(IMG_OUTPUT)
    logger.info(f"Directory {IMG_OUTPUT} Created ")
else:
    logger.info(f"Directory {IMG_OUTPUT} already exist ")

if not os.path.exists(IMG_INPUT):
    os.mkdir(IMG_INPUT)
    logger.info(f"Directory {IMG_INPUT} Created ")
else:
    logger.info(f"Directory {IMG_INPUT} already exist ")


# Config Path
_CONFIG_PATH = os.path.join(COMMON_PATH, 'conf.ini')
logger.info(f'CONFIG_PATH : {_CONFIG_PATH}')
cc = konf.Config(_CONFIG_PATH)

# Data Path
DATA_FOLDER_PATH = os.path.join(BASE_DIR, 'data')
SAMPLE_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'samples')

# # Log Path
# 파일 읽어오는 순서 문제로 logger.py 자체에 넣어둠
# LOG_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'logs')
# if not os.path.exists(LOG_FOLDER_PATH):
#     os.mkdir(LOG_FOLDER_PATH)
#     logger.info(f"Directory {LOG_FOLDER_PATH} Created ")
# else:
#     logger.info(f"Directory {LOG_FOLDER_PATH} already exist ")


RESULT_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'results')
TRAIN_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'train')
REGEX_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'regex')

if CURRENT_OS == 'Linux': # 'Windows', 'MacOS'
    """Upload File Directory
    Create target Directory if don't exist"""
    storage = cc.get_map("file")
    UPLOAD_DIRECTORY = storage['STORAGE']
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.mkdir(UPLOAD_DIRECTORY)
        logger.info(f"Directory {UPLOAD_DIRECTORY} Created ")
    else:
        logger.info(f"Directory {UPLOAD_DIRECTORY} already exist ")
else:
    UPLOAD_DIRECTORY = os.path.join(RESULT_FOLDER_PATH, 'uploadfiles')


# PyCaret Model Path
ML_MODEL_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'ml_model')
ML_MODEL_PATH = os.path.join(ML_MODEL_FOLDER_PATH, 'auto_ml_model_0623')


#--------------------------------------------------#
# ./sources/common/conf.ini
#--------------------------------------------------#
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
DB_PORT = db['PORT']
DB_NAME = db['NAME']
logger.info(f'[ DB INFO : postgresql://{DB_USER}:{DB_PW}@postgres-xedm/{DB_NAME} ]')

# support EXT
SUPPORT_EXT = ['pdf','pptx','docx','csv','xlsx','txt','json','xml']
_TODO=['hwp','html']
# ','.join(SUPPORT_EXT) 
