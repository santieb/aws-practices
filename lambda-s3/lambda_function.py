
import os
import uuid
from urllib.parse import unquote_plus
from PIL import Image
from io import BytesIO

s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        resized_image = image.resize((image.width // 2, image.height // 2))
        resized_image.save(resized_path)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)

        print(f"Processing file: s3://{bucket}/{key}")
        print(f"Temporary download path: {download_path}")
        print(f"Temporary upload path: {upload_path}")
        
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        print(f"Image resized successfully.")
        
        resized_key = 'resized-{}'.format(key)
        s3_client.upload_file(upload_path, 'alke-cloud-bucket-resized', resized_key)
        print(f"Upload complete: s3://alke-cloud-bucket-resized/{resized_key}")

if __name__ == "__main__":
    mock_event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "alke-cloud-bucket2"},
                    "object": {"key": "user-profiles/user-c7f5d7b8-9121-11ee-b9d1-0242ac120002.jpg"}
                }
            }
        ]
    }
    mock_context = None
    lambda_handler(mock_event, mock_context)
