from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
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

class Download_request(BaseModel):
    video_name : str

class Download_handler:
    def __init__(self, database : Database_handler):
        self.database = database

    def download(self, request : Download_request):
        file_name = TEMP_FILES_PATH + request.video_name
        
 # Downloading the video from database
        if not request.video_name in self.database.list():
            raise HTTPException(status_code=404, detail=f'Video {request.video_name} not found!')

        try:
            self.database.get(request.video_name, file_name)
            def iterfile():
                with open(file_name, 'rb') as file:
                    yield from file
            return StreamingResponse(iterfile(), media_type="video/mp4")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Erro ao fazer download do vídeo:{str(e)}')
        # TODO: delete the file after sent
