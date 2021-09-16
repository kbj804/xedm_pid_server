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

- Script for creating postgresql DB, Table
```
#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
  \connect $APP_DB_NAME $APP_DB_USER
  BEGIN;
    CREATE TABLE IF NOT EXISTS event (
	  id CHAR(26) NOT NULL CHECK (CHAR_LENGTH(id) = 26) PRIMARY KEY,
	  aggregate_id CHAR(26) NOT NULL CHECK (CHAR_LENGTH(aggregate_id) = 26),
	  event_data JSON NOT NULL,
	  version INT,
	  UNIQUE(aggregate_id, version)
	);
	CREATE INDEX idx_event_aggregate_id ON event (aggregate_id);
  COMMIT;
EOSQL
```