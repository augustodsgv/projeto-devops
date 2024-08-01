from pydantic import BaseModel
from fastapi import HTTPException
import os
from src.database.database_handler import Database_handler
from src.utils.video_cutter import Video_cutter
import logging
logger = logging.getLogger(__name__)

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

class Cut_request(BaseModel):
    video_name : str
    video_start : int
    video_end : int

class Cut_handler:
    def __init__(self, database : Database_handler, cutter : Video_cutter):
        self.database : Database_handler = database
        self.cutter : Video_cutter = cutter

    def cut(self, request : Cut_request):
        
        # Downloading the video from database
        if not request.video_name in self.database.list():
            logger.warning(f'Request to cut video {request.video_name} but there were no such video')
            raise HTTPException(status_code=404, detail=f'Video {request.video_name} not found!')
        video_path = TEMP_FILES_PATH + request.video_name
        self.database.get(request.video_name, video_path)
        
        # Cutting the video
        try:
            self.cutter.cut(input_path=video_path, video_start=request.video_start, video_end=request.video_end)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        self.database.insert(video_path, object_name=request.video_name)

        # Deleting temp files
        if os.path.exists(video_path):
            os.remove(video_path)

        return {'Video was cutted successfully!'}