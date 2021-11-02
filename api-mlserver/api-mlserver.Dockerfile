FROM python:3.8.3-slim
LABEL maintainer "Boungjin Kim<kbj804@inzent.com>"
LABEL title="FastAPI"
LABEL version="1.0"
LABEL description="This image is XEDM Machine Learning API Server"

# setting ENV
ENV XEDM_DOCKER="YES" \
    XEDM_HOME=/api-mlserver \
    # XEDM_PYTHON_PACKAGES=/usr/local/lib/python3.6/dist-packages \
    XEDM_WORKING_STG=/xedm_storage \
    TZ=Asia/Seoul \
    MODEL_PATH=/api-mlserver/data/results/ml_model/auto_ml_model_0623.pkl

RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone


# Setting WORK DIR
COPY ./api-mlserver/sources /api-mlserver
COPY ./api-mlserver/requirements.txt /api-mlserver/requirements.txt
COPY ./datas/auto_ml_model_0623.pkl /api-mlserver/data/results/ml_model/auto_ml_model_0623.pkl

COPY ./wait-for-it.sh /bin/wait-for-it.sh
RUN chmod +x /bin/wait-for-it.sh

WORKDIR /api-mlserver

# XEDM SERVER temp Storage
RUN mkdir -p ${XEDM_WORKING_STG}

# apt setting
RUN apt-get update -qq
RUN apt-get upgrade -y
RUN apt-get install libgomp1 -y

# RUN apt-get install git -y

# 개인정보 검출 python Lib 설치
# RUN pip install requests uvicorn fastapi sqlalchemy pyjwt bcrypt pdfminer.six python-pptx python-docx openpyxl xmltodict pandas python-multipart psycopg2-binary konfig
RUN pip install -r /api-mlserver/requirements.txt

# Auto Machine Learning
# RUN pip install pycaret

ENTRYPOINT ["wait-for-it.sh", "postgres-xedm:5432", "--", "python", "main.py"]
