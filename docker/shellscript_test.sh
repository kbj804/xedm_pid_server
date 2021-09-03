# sed -i -e 's/\r$//' shellscript_test.sh

CURRENT_PATH=$(pwd)

CONFIG_FILE=${CURRENT_PATH}/conf.ini

A=$(awk '/^STORAGE/{print $0}' ${CONFIG_FILE})
B=$(awk '/^STORAGE/{print $1}' ${CONFIG_FILE})
C=$(awk '/^STORAGE/{print $2}' ${CONFIG_FILE})
D=$(awk '/^STORAGE/{print $3}' ${CONFIG_FILE})

sport=$(awk '/^\[server]/{f=1} f==1&&/^PORT/{print $3;exit}' ${CONFIG_FILE})
dport=$(awk '/^\[db]/{f=1} f==1&&/^PORT/{print $3;exit}' ${CONFIG_FILE})

path=$(awk '/^\[shell]/{f=1} f==1&&/^PROJECT_PATH/{print $3;exit}' ${CONFIG_FILE})

echo ${A}
echo ${B}
echo ${C}
echo ${D}

echo "server PORT is $sport and DB PORT is $dport"
echo $path