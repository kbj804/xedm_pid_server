FROM ubuntu:20.04
LABEL maintainer "Boungjin Kim<kbj804@inzent.com>"
LABEL title="FastAPI"
LABEL version="1.0"
LABEL description="This image is XEDM Machine Learning API Server"

# setting ENV
ENV XEDM_DOCKER="YES" \
    XEDM_HOME=/xedm_app \
    # XEDM_PYTHON_PACKAGES=/usr/local/lib/python3.6/dist-packages \
    XEDM_WORKING_STG=/xedm_storage \
    TZ=Asia/Seoul \
    MODEL_PATH=/xedm_app/docker/fastapp/data/results/ml_model/auto_ml_model_0623.pkl

RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

# XEDM SERVER temp Storage
RUN mkdir -p ${XEDM_WORKING_STG}

# docker volume
RUN mkdir -p ${XEDM_HOME}

# apt setting
RUN apt-get update -qq
RUN apt-get upgrade -y
RUN apt-get install git -y

# 한글 출력을 위한 패키지
RUN apt-get install locales
RUN apt-get install -y \
    language-pack-ko && \
    dpkg-reconfigure locales && \
    locale-gen ko_KR.UTF-8 && \
    /usr/sbin/update-locale LANG=ko_KR.UTF-8

# 한글을 출력하기 위해 환경변수 등록
ENV LANG=ko_KR.UTF-8    \
    LANGUAGE=ko_KR.UTF-8    \
    LC_ALL=ko_KR.UTF-8  \

    # 파이썬에서 한글을 사용할 수 있도록 환경변수 등록
    PYTHONIOENCODING=UTF-8

# tesseract 설치
RUN apt install -y tesseract-ocr tesseract-ocr-kor libtesseract-dev tesseract-ocr-script-hang tesseract-ocr-script-hang-vert libgl1-mesa-glx

# WORKDIR: RUN이 실행 될 공간
# WORKDIR ${XEDM_HOME}

# COPY ./auto_ml_model_0623.pkl ${MODEL_PATH}

# python 설치
RUN apt install -y python3 python3-pip


# 개인정보 검출 python Lib 설치
RUN pip install requests uvicorn fastapi sqlalchemy pyjwt bcrypt pdfminer.six python-pptx python-docx openpyxl xmltodict pandas python-multipart psycopg2-binary konfig

# Auto Machine Learning
RUN pip install pycaret

# OCR
RUN pip install pymuPDF pillow opencv-python pytesseract scikit-image

# use bash always
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# PORT Setting
# EXPOSE 8889

# Docker가 실행된 후 계속 켜져있는 상태를 유지시키는 방법
CMD tail -f /dev/null


# DOCKER Container Run Scripts
# docker run -it -v [OS_PATH]:[DOCKER_PATH] --name [container_name] -p 8899:8899 [ImageName]
# docker run -it -v /home/kbj/buildfile:/localshare --name sTest -p 8889:8889 build_test:0.7
# docker run -it --name sTest -p 8889:8889 build_test:0.7

# DOCKER Container 내부 Config 파일 변경하는 방법
# docker cp [LOCAL_PATH] [CONTAINER]:[DOCKER_PATH]
# docker cp ./conf.ini sTest:/xedm_app/docker/fastapp/common/conf.ini