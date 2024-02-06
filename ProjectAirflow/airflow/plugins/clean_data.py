import os
import pandas as pd

def clean_data():
    # 1. load raw data into DataFrame
    # downloaded files are stored in tmp (in airflow)
    # here, we will store it in tmp/xrate.csv
    path = '/tmp/xrate.csv' 
    data = pd.read_csv('/tmp/xrate.csv', header=None)

    # cleanse data
    default_values = {
        int: 0,
        float: 0.0,
        str: ''
    }

    # replace all int fields by 0, float fields by 0.0, etc.
    cleaned_data = data.fillna(value=default_values)

    # get the current date components
    now = pd.Timestamp.now()
    year = now.year
    month = now.month
    day = now.day

    # create the directory path if it does not exist
    data_dir = f'/opt/airflow/data/xrate_cleansed/{year}/{month}/{day}'
    os.mkdir(data_dir, exist_ok=True)

    # save the cleaned data to a new file
    clean_data.to_csv(f'{data_dir}/xrate.csv', index=False)

