import os
from konfig import Config
import platform

JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"
MAX_API_KEY = 3
MAX_API_WHITELIST = 10

CURRENT_OS = platform.system() # mac: Darwin
print(f"CURRENT_OS is {CURRENT_OS}")

if CURRENT_OS == 'Windows':
    
    # Folder Path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # fastapp/
    print(f'BASE_PATH : {BASE_DIR}')
    # Config Path
    # _CONFIG_PATH = f'{BASE_DIR}\\common\\conf.ini'
    _CONFIG_PATH = os.path.join(BASE_DIR, 'common', 'conf.ini')
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
    DATA_FOLDER_PATH = os.path.join(BASE_DIR, 'data')
    SAMPLE_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'samples')
    TRAIN_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'train')

    RESULT_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'results')
    REGEX_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'regex')
    UPLOAD_DIRECTORY = os.path.join(RESULT_FOLDER_PATH, 'uploadfiles')

    # PyCaret Model Path
    ML_MODEL_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'ml_model')
    ML_MODEL_PATH = os.path.join(ML_MODEL_FOLDER_PATH, 'auto_ml_model_0623')
    # ML_MODEL_PATH = f'{BASE_DIR}\\data\\results\\ml_model\\auto_ml_model_0623'

    # SAMPLE_FOLDER_PATH = f'{BASE_DIR}\\data\\samples'
    # TRAIN_FOLDER_PATH = f'{BASE_DIR}\\data\\train\\'
    # REGEX_FOLDER_PATH = f'{BASE_DIR}\\data\\results\\regex\\'
    # UPLOAD_DIRECTORY = f'{BASE_DIR}\\data\\results\\uploadfiles\\'

    # File path
    # KEYWORD_DICTIONARY_PATH = f'{BASE_DIR}\\common\\dic.txt'
    KEYWORD_DICTIONARY_PATH = os.path.join(BASE_DIR, 'common','dic.txt')
    # DEFAULT_CSV_PATH = f'{BASE_DIR}\\'

    # Save h2o model
    # H2O_MODEL_PATH = f'{BASE_DIR}\\data\\results\\ml_model\\'
    # USING_MODEL_PATH = f'{H2O_MODEL_PATH}\\GBM_1_AutoML_20210423_140912'

    

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

elif CURRENT_OS == 'Linux':
    # Folder Path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # fastapp/
    print(f"BASE_DIR : {BASE_DIR}")

    SAMPLE_FOLDER_PATH = f'{BASE_DIR}/data/samples'
    TRAIN_FOLDER_PATH = f'{BASE_DIR}/data/train/'

    REGEX_FOLDER_PATH = f'{BASE_DIR}/data/results/regex/'

    # File path
    KEYWORD_DICTIONARY_PATH = f'{BASE_DIR}/common/dic.txt'
    DEFAULT_CSV_PATH = f'{BASE_DIR}/'

    # Save h2o model
    H2O_MODEL_PATH = f'{BASE_DIR}/data/results/ml_model/'

    USING_MODEL_PATH = f'{H2O_MODEL_PATH}/GBM_1_AutoML_20210423_140912'

    # Config File Load 
    _CONFIG_PATH = f'{BASE_DIR}/common/conf.ini'
    print(f'CONFIG_PATH : {_CONFIG_PATH}')
    cc = Config(_CONFIG_PATH)

    # Upload File Directory
    # Create target Directory if don't exist
    storage = cc.get_map("file")
    UPLOAD_DIRECTORY = storage['STORAGE']
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.mkdir(UPLOAD_DIRECTORY)
        print("Directory " , UPLOAD_DIRECTORY ,  " Created ")
    else:
        print("Directory " , UPLOAD_DIRECTORY ,  " already exists")

    # UPLOAD_DIRECTORY = f'{BASE_DIR}/data/results/uploadfiles/'

    ML_MODEL_PATH= f'{BASE_DIR}/common/auto_ml_model_0623'


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