from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
import boto3
from botocore.parsers import JSONParser
import os 
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


def s3_uploader(file):
 
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    s3.upload_file(filename,'read-online-book', 'story_pictures/'+filename)
    fs.delete(filename)

    