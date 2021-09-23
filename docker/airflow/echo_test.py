# airflow.cfg에서 dags_folder를 /root/airflow/dags 인지 확인 / airflow.cfg의 가장 상단에 있는 dags_folder에 존재하는 Workflow 파이썬 파일만 인식하기 때문
# docker cp ./echo_test.py sTest:/root/airflow/dags/echo_test.py
# airflow scheduler
from airflow import models
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
 
default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2020, 2, 9),
        'retries': 1,
        'retry_delay': timedelta(minutes=5)}
 
with models.DAG(
        dag_id='echo_test', description='echo_test',
        schedule_interval=None,
        max_active_runs=5,
        concurrency=10,
        default_args=default_args) as dag:
 
    text_file_path = '/root/airflow/dags'
 
    #### create txt file  --> 텍스트 파일을 생성합니다
    create_text_file_command = f'cd {text_file_path} && echo hello airflow > test.txt'
    create_text_file = BashOperator(
            task_id='create_text_file',
            bash_command=create_text_file_command,
            dag=dag)
 
    #### cat txt file  --> 텍스트 파일을 읽습니다
    read_text_file_command = f'cd {text_file_path} && cat test.txt'
    read_text_file = BashOperator(
            task_id='cat_text_file',
            bash_command=read_text_file_command,
            dag=dag)
 
    #### remove txt file  --> 텍스트 파일을 삭제합니다.
    remove_text_file_command = f'cd {text_file_path} && rm test.txt'
    remove_text_file = BashOperator(
            task_id='remove_text_file',
            bash_command=remove_text_file_command,
            dag=dag)
 
    create_text_file >> read_text_file >> remove_text_file  # 이것은 위의 task를 이어주는 줄입니다.
