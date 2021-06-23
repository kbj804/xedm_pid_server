import os
from konfig import Config


JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"
MAX_API_KEY = 3
MAX_API_WHITELIST = 10


# Folder Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # fastapp/
print(f'BASE_PATH : {BASE_DIR}')
# Config Path
_CONFIG_PATH = f'{BASE_DIR}\\common\\conf.ini'
print(f'CONFIG_PATH : {_CONFIG_PATH}')
cc = Config(_CONFIG_PATH)


# Upload File Directory
# Create target Directory if don't exist
"""  linux에서 파일 업로드 할때 파일 저장공간 체크하고 없으면 생성
storage = cc.get_map("file")
UPLOAD_DIRECTORY = storage['STORAGE']
if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)
    print("Directory " , UPLOAD_DIRECTORY ,  " Created ")
else:    
    print("Directory " , UPLOAD_DIRECTORY ,  " already exists")
"""

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

ML_MODEL_PATH= f'{BASE_DIR}\\data\\results\\ml_model\\auto_ml_model_0623'

# URL
xedm = cc.get_map("xedm")
X_URL = xedm['ADD']
X_PORT = xedm['PORT']
XEDM_URL = f'{X_URL}:{X_PORT}'

# uvicorn Server setting
app = cc.get_map("server")
APP_HOST_ADD=app['HOST']
APP_PORT=app['PORT']


# DB Setting
db = cc.get_map("db")
DB_USER = db['USER']
DB_PW = db['PW']
DB_ADD = db['ADD']
DB_PORT = db['PORT']
DB_NAME = db['NAME']

# support EXT
SUPPORT_EXT = ['pdf','pptx','docx','csv','xlsx','txt','json','xml']
_TODO=['hwp','html']
# ','.join(SUPPORT_EXT) 