import os
import boto3

import boto3
import os

s3 = boto3.resource(
    service_name='s3',
    region_name= os.environ["REGION_NAME"],
    aws_access_key_id=os.environ["KEY_ID"],
    aws_secret_access_key=os.environ["SECRET_KEY"]
)

bucket = s3.Bucket('patatoremoto')

def get_log_objects(task_id, bucket = bucket):
    err = bucket.Object(f'logs/{task_id}_stderr.txt')
    out = bucket.Object(f'logs/{task_id}_stdout.txt')
    return (out, err)

def get_log_strings(task_id, bucket = bucket):
    out, err = get_log_objects(task_id)

    try:
        out_str = out.get()['Body'].read().decode('ascii')
    except s3.meta.client.exceptions.NoSuchKey:
        out_str = f"There is no log file. \nThis is normal if your task hasn't been completed yet"
    except Exception as e:
        out_str = f"there was an error: {e}"

    try:
        err_str = err.get()['Body'].read().decode('utf-8')
    except s3.meta.client.exceptions.NoSuchKey:
        err_str = f"There is no log file. \nThis is normal if your task hasn't been completed yet"
    except Exception as e:
        err_str = f"there was an error: {e}"
    
    return (out_str, err_str)


def create_obj(key, bucket = bucket):
    bucket.put_object(Key="picture_log/" + key)