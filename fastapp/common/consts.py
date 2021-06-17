import os

JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"
MAX_API_KEY = 3
MAX_API_WHITELIST = 10


# Folder Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # fastapp/

SAMPLE_FOLDER_PATH = f'{BASE_DIR}\\data\\samples'
TRAIN_FOLDER_PATH = f'{BASE_DIR}\\data\\train\\'

REGEX_FOLDER_PATH = f'{BASE_DIR}\\data\\results\\regex\\'

UPLOAD_DIRECTORY = f'{BASE_DIR}\\data\\results\\uploadfiles\\'

# File path
KEYWORD_DICTIONARY_PATH = f'{BASE_DIR}\\common\\dic.txt'
DEFAULT_CSV_PATH = f'{BASE_DIR}\\'

# Save h2o model
H2O_MODEL_PATH = f'{BASE_DIR}\\data\\results\\ml_model\\'

USING_MODEL_PATH = f'{H2O_MODEL_PATH}\\GBM_1_AutoML_20210423_140912'


# URL
XEDM_URL = '192.168.21.29:9080'

# uvicorn Server setting
APP_HOST_ADD="0.0.0.0"
APP_PORT=8000

# DB Setting
DB_USER = 'iztbj'
DB_PW = '1234'
DB_ADD = '192.168.21.204'
DB_PORT = '2345'
DB_NAME = 'pidb'