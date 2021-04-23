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
    except Exception as e:
        out_str = f"there was an error: {e}"

    try:
        err_str = err.get()['Body'].read().decode('utf-8')
    except Exception as e:
        out_str = f"there was an error: {e}"
    
    return (out_str, err_str)

