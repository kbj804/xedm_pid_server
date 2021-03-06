# Auto Inatall Guideline
# require: docker image file, ml_model_file, configure_file, 
# 윈도우에서 작업한 쉘 스크립트를 리눅스에서 실행할때 필요
# sed -i -e 's/\r$//' [파일.sh]
# sed -i -e 's/\r$//' container_test.sh
CURRENT_PATH=$(pwd)
#
echo "Running Config file setting ..."
CONFIG_FILE=${CURRENT_PATH}/conf.ini
PROJECT_PATH=$(awk '/^\[shell]/{f=1} f==1&&/^PROJECT_PATH/{print $3;exit}' ${CONFIG_FILE})
GIT_URL=$(awk '/^\[shell]/{f=1} f==1&&/^GIT_URL/{print $3;exit}' ${CONFIG_FILE})
# 
DOCKER_IMAGE=$(awk '/^\[docker]/{f=1} f==1&&/^DOCKER_IMAGE/{print $3;exit}' ${CONFIG_FILE})
DOCKER_VERSION=$(awk '/^\[docker]/{f=1} f==1&&/^DOCKER_VERSION/{print $3;exit}' ${CONFIG_FILE})
DOCKER_PATH=$(awk '/^\[docker]/{f=1} f==1&&/^DOCKER_PATH/{print $3;exit}' ${CONFIG_FILE})
CONTAINER_NAME=$(awk '/^\[docker]/{f=1} f==1&&/^CONTAINER_NAME/{print $3;exit}' ${CONFIG_FILE})
DOCKER_PORT=$(awk '/^\[server]/{f=1} f==1&&/^PORT/{print $3;exit}' ${CONFIG_FILE})   # port forwarding - [server]의 PORT와 같아야함
AIZT_PORT=$(awk '/^\[docker]/{f=1} f==1&&/^AIZT_PORT/{print $3;exit}' ${CONFIG_FILE}) 
# 
CONFIG_NAME=$(awk '/^\[share]/{f=1} f==1&&/^CONFIG_NAME/{print $3;exit}' ${CONFIG_FILE})
ML_MODEL_NAME=$(awk '/^\[share]/{f=1} f==1&&/^ML_MODEL_NAME/{print $3;exit}' ${CONFIG_FILE})

echo "CURRENT PROJECT PATH is ${PROJECT_PATH}"
# 
# setting for dev
# sudo docker build --tag ${DOCKER_IMAGE}:${DOCKER_VERSION} .
# 
# init setting
sudo mkdir -p ${PROJECT_PATH}
sudo git clone ${GIT_URL} ${PROJECT_PATH}
# 
# docker containser start
# sudo docker restart $CONTAINER_NAME
echo "Docker container reset & restart ..."
sudo docker stop ${CONTAINER_NAME}
sudo docker rm ${CONTAINER_NAME}
sudo docker run -d --restart always --name ${CONTAINER_NAME} -p ${AIZT_PORT}:${DOCKER_PORT} ${DOCKER_IMAGE}:${DOCKER_VERSION}
# 
# make working directory in docker
# sudo docker exec ${CONTAINER_NAME} mkdir ${DOCKER_PATH}
# 
# input project source code
echo "Downloading XEDM ML Server source code ..."
sudo docker cp ${PROJECT_PATH} ${CONTAINER_NAME}:${DOCKER_PATH}
# 
echo "Setting app and ml config files ..."
sudo docker cp ${CURRENT_PATH}/${CONFIG_NAME} ${CONTAINER_NAME}:${DOCKER_PATH}/aizt/fastapp/common/${CONFIG_NAME}
sudo docker cp ${CURRENT_PATH}/${ML_MODEL_NAME} ${CONTAINER_NAME}:${DOCKER_PATH}/aizt/fastapp/data/results/ml_model/${ML_MODEL_NAME}
# 
# 
echo "Starting XEDM ML Server  ..."
sudo docker exec ${CONTAINER_NAME} python3 ${DOCKER_PATH}/aizt/fastapp/main.py