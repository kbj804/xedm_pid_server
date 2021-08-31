# Auto Inatall Guideline
# require: docker image file, ml_model_file, configure_file, 
# 윈도우에서 작업한 쉘 스크립트를 리눅스에서 실행할때 필요
# sed -i -e 's/\r$//' [파일.sh]
CURRENT_PATH=$(pwd)
PROJECT_PATH=/home/$USER/aizt
GIT_URL='https://github.com/kbj804/xedm_pid_server.git'
# 
DOCKER_IMAGE="build_test"
DOCKER_VERSION="0.8"
DOCKER_PATH=/xedm_app
CONTAINER_NAME="sTest"
AIZT_PORT=8889
# 
CONFIG_NAME="conf.ini"
ML_MODEL_NAME="auto_ml_model_0623.pkl"
# 
# setting for dev
sudo docker build --tag ${DOCKER_IMAGE}:${DOCKER_VERSION} .
# 
# init setting
sudo mkdir -p ${PROJECT_PATH}
sudo git clone ${GIT_URL} ${PROJECT_PATH}
# 
# docker containser start
# sudo docker restart $CONTAINER_NAME
sudo docker run -it --name ${CONTAINER_NAME} -p ${AIZT_PORT} ${DOCKER_IMAGE}:${DOCKER_VERSION}
# 
# make working directory in docker
sudo docker exec ${CONTAINER_NAME} mkdir ${DOCKER_PATH}
# 
# input project source code
sudo docker cp ${PROJECT_PATH} ${CONTAINER_NAME}:${DOCKER_PATH}
# 
# setting config file
sudo docker cp ${CURRENT_PATH}/${CONFIG_NAME} ${CONTAINER_NAME}:${DOCKER_PATH}/fastapp/common/${CONFIG_NAME}
sudo docker cp ${CURRENT_PATH}/${ML_MODEL_NAME} ${CONTAINER_NAME}:${DOCKER_PATH}/fastapp/data/results/ml_model/${ML_MODEL_NAME}
# 
#
# start
sudo docker exec ${CONTAINER_NAME} python3 ${DOCKER_PATH}/fastapp/main.py