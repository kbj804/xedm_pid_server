import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

    
    # Log Path
    LOG_FOLDER_PATH = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(LOG_FOLDER_PATH):
        os.mkdir(LOG_FOLDER_PATH)
        print(f"Directory {LOG_FOLDER_PATH} Created ")

    # 파일 핸들러
    LOG_HANDLER = os.path.join(LOG_FOLDER_PATH, 'handler.log')


    file_handler = logging.FileHandler(LOG_HANDLER)
    file_handler.setFormatter(formatter)
    __logger.addHandler(file_handler)

    return __logger