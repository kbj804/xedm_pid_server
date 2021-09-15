### AirFlow


- 사용중인 db에 Airflow 전용 DB 추가 (접속 및 TABLE 생성)
  > - psql --username=kbj --dbname=pidb
  > - CREATE DATABASE airflow OWNER kbj;
  > - or $ sudo -u postgres createdb airflow --owner=kbj
  > - 확인 \l
- Airflow HOME PATH 설정 및 환경설정 변경
  > - HOME_PATH 확인: find | grep airflow.cfg
  > - executor = LocalExecutor
  > - sql_alchemy_conn = postgresql+psycopg2://kbj:1234@192.168.0.2:5432/airflow
  > - Format： dialect+driver://username:password@host:port/database

  ##### column Error 발생할 경우
> pip install SQLAlchemy==1.3.23 \

- network port 겹칠때 확인 및 종료
> - sudo apt-get install net-tools
> - netstat -tnlp
> - kill [pid]

- Airflow
> - airflow db init
> - airflow users create -r Admin -u kbj -e kbj804@inzent.com -f Boungjin -l Kim -p 1234
> - airflow webserver