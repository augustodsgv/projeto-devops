from pydantic import BaseModel
from fastapi import UploadFile
from src.database.database_handler import Database_handler

import os

# Path to set temp files
try:
    TEMP_FILES_PATH = os.environ['TEMP_FILES_PATH']
except:
    if not os.path.exists('/tmp/ffmpeg'):
        os.mkdir('/tmp/ffmpeg')
    TEMP_FILES_PATH = '/tmp/ffmpeg'
finally:
    if TEMP_FILES_PATH[-1] != '/':
        TEMP_FILES_PATH += '/'

class Upload_handler:
    def __init__(self, database : Database_handler):
        self.database = database

    def upload(self, request_file : UploadFile):
        upload_path = TEMP_FILES_PATH + request_file.filename
        # Recieving the file from the user
        with open(upload_path, "wb") as f:
            f.write(request_file.file.read())
        
        # Saving it to the database
        self.database.insert(upload_path, request_file.filename)
        if os.path.exists(upload_path):
            os.remove(upload_path)
        return {"Your have been successfully uploaded!"}
