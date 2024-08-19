from src.database.minio_handler import Minio_handler

from src.utils.video_cutter import Video_cutter
from src.api.cut_handler import Cut_handler, Cut_request
from src.api.download_handler import Download_handler, Download_request
from src.api.upload_handler import Upload_handler
from src.api.delete_handler import Delete_handler


import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# endpoints
DATABASE_ENDPOINT = os.environ['DATABASE_ENDPOINT']
DATABASE_PORT = os.environ['DATABASE_PORT']
DATABASE_USR = os.environ['DATABASE_USR']
DATABASE_PASSWD = os.environ['DATABASE_PASSWD']
DATABASE_BUCKET_NAME = os.environ['DATABASE_BUCKET_NAME']

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/list')
def list_videos():
    database = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    return database.list()

@app.post('/cut')
async def cut_video(request : Cut_request):
    logging.info(request.video_name)
    database = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    cutter = Video_cutter()
    cut_handler = Cut_handler(database=database, cutter=cutter)
    return cut_handler.cut(request=request)

@app.post('/download')
def download_video(request : Download_request):
    database = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    download_handler = Download_handler(database=database)
    return download_handler.download(request=request)

@app.post('/upload')
def upload_video(file : UploadFile = File(...)):
    database = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                             minio_usr=DATABASE_USR,
                             minio_passwd=DATABASE_PASSWD,
                             default_bucket=DATABASE_BUCKET_NAME)
    upload_handler = Upload_handler(database)
    return upload_handler.upload(file)
 
@app.delete('/delete_video')
def delete_video(video_name : str):
    database = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                             minio_usr=DATABASE_USR,
                             minio_passwd=DATABASE_PASSWD,
                             default_bucket=DATABASE_BUCKET_NAME)
    delete_handler = Delete_handler(database)
    return delete_handler.delete(video_name)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7000)