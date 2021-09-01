# Auto Inatall Guideline
# require: docker image file, ml_model_file, configure_file, 
# 윈도우에서 작업한 쉘 스크립트를 리눅스에서 실행할때 필요
# sed -i -e 's/\r$//' [파일.sh]
# sed -i -e 's/\r$//' container_test.sh
CURRENT_PATH=$(pwd)
read_lines()
{
    while IFS = read -r line
    do
        echo $line
    done <$1
}

eval $(read_lines) ${CURRENT_PATH}/config_for_install.txt
# 
# setting for dev
# sudo docker build --tag ${DOCKER_IMAGE}:${DOCKER_VERSION} .
# 
# init setting
# sudo mkdir -p ${PROJECT_PATH}
# sudo git clone ${GIT_URL} ${PROJECT_PATH}
# 
# docker containser start
# sudo docker restart $CONTAINER_NAME
sudo docker stop ${CONTAINER_NAME}
sudo docker rm ${CONTAINER_NAME}
sudo docker run -d --restart always --name ${CONTAINER_NAME} -p ${AIZT_PORT}:${DOCKER_PORT} ${DOCKER_IMAGE}:${DOCKER_VERSION}
# 
# make working directory in docker
# sudo docker exec ${CONTAINER_NAME} mkdir ${DOCKER_PATH}
# 
# input project source code
sudo docker cp ${PROJECT_PATH} ${CONTAINER_NAME}:${DOCKER_PATH}
# 
# setting config file
sudo docker cp ${CURRENT_PATH}/${CONFIG_NAME} ${CONTAINER_NAME}:${DOCKER_PATH}/aizt/fastapp/common/${CONFIG_NAME}
sudo docker cp ${CURRENT_PATH}/${ML_MODEL_NAME} ${CONTAINER_NAME}:${DOCKER_PATH}/aizt/fastapp/data/results/ml_model/${ML_MODEL_NAME}
# 
#
# start
sudo docker exec ${CONTAINER_NAME} python3 ${DOCKER_PATH}/aizt/fastapp/main.py