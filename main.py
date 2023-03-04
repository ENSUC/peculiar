import firebase_admin
from firebase_admin import credentials, storage
import os

# Initialize Firebase app
cred = credentials.Certificate("./serviceAccountKey.json")
if len(firebase_admin._apps) > 0:
    firebase_admin.delete_app(firebase_admin.get_app())
firebase_admin.initialize_app(cred, {'storageBucket': 'ensucdatabase.appspot.com'})

# Navigate to directory and import module
from pathlib import Path
import sys
path = Path("Yolov5/")
sys.path.append(str(path.resolve()))
from detect import run

def detect_image(event, context):
    # Get the file path of the image
    file_path = event['data']['name']
    # Get the user id from the file path
    user_id = file_path.split('/')[2]
    # Get the URL of the image
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    image_url = blob.generate_signed_url(expiration=300, method='GET')
    # Run the detection code
    run(weights='Yolov5/runs/train/yolov5s_results/weights/best.pt', imgsz = (416, 416), 
        conf_thres=0.4, source=image_url,save_txt=True, name=user_id)

    #Upload the results to firebase storage
    result_folder = f'Yolov5/pep-1/runs/detect/{user_id}/'
    for root, dirs, files in os.walk(result_folder):
        for file in files:
            local_path = os.path.join(root, file)
            storage_path = local_path.replace(result_folder, f'users/{user_id}/results/')
            blob = bucket.blob(storage_path)
            blob.upload_from_filename(local_path)


import boto3
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase app
firebase_cred = credentials.Certificate("./serviceAccountKey.json")
if len(firebase_admin._apps) > 0:
    firebase_admin.delete_app(firebase_admin.get_app())
firebase_admin.initialize_app(firebase_cred, {'storageBucket': 'ensucdatabase.appspot.com'})

# Initialize S3 client
aws_access_key_id = 'AKIA2ZX54AH5E33Y6SED'
aws_secret_access_key = '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'
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def detect_image(event, context):
    # Get the file path of the image
    file_path = event['data']['name']
    # Get the user id from the file path
    user_id = file_path.split('/')[2]
    # Download the image from Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    image_data = blob.download_as_string()
    # Send the image to the S3 bucket
    s3.put_object(Bucket='quicfarm', Key=f'{user_id}/{blob.name.split("/")[-1]}', Body=image_data)

