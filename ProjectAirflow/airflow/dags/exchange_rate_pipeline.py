# Imports
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from clean_data import clean_data

# note: if there is a problem in your import, for example you write
# pyton instead of python, your file will not be imported by airflow in the ui.

# define or instatiate DAG
dag = DAG(
    'exchange_rate_etl',  # dag name
    start_date=datetime(2024, 2, 6),  # dag starts at
    end_date=datetime(2024, 2, 8),  # end at
    schedule_interval='0 22 * * *',  # executed at 22h each time
    default_args={
        'retries': 2,  # if issues, retry a max of 2 times
        'retry_delay': timedelta(minutes=5)  # 5min btw two retries
    },
    catchup=False
)

# define or instantiate a task
# 1. download task
# this task use BashOperator to execute Bash command
# here, we use curl to download a csv file from the URL
# and save it as 'xrate.csv'. The file is stored in '/tmp/
download_task = BashOperator(
    task_id='download_file',
    bash_command='curl -o /tmp/xrate.csv https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata',
    dag=dag
)

# 2. clean the downloaded file
# We use a PythonOperator to execute a python function (clean_data)
# This function, clean the downloaded data
clean_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag
)

# 3. send email to notify that the processed has been successful
send_email_task = EmailOperator(
    task_id='send_email',
    to='vadombi@gmail.com',
    subject='Exchange Rate Download - Successful',
    html_content='The Exchange Rate data has been successfully downloaded, cleaned, and loaded.',
    dag=dag
)

# define task dependencies
download_task >> clean_data_task >> send_email_task
