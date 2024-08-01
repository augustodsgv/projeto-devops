from src.api.cut_handler import Cut_handler, Cut_request
from src.api.download_handler import Download_handler, Download_request
from src.utils.video_cutter import Video_cutter
from src.database.minio_handler import Minio_handler

import os
from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uvicorn

import logging
logger = logging.getLogger(__name__)

# endpoints
DATABASE_ENDPOINT = os.environ['DATABASE_ENDPOINT']
DATABASE_PORT = os.environ['DATABASE_PORT']
DATABASE_USR = os.environ['DATABASE_USR']
DATABASE_PASSWD = os.environ['DATABASE_PASSWD']
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
output_mount_path = ''

class Delete_request(BaseModel):
    video_name : str

@app.get('/list')
def list_videos():
    database = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    return database.list()

@app.post('/cut')
async def cut_video(request : Cut_request):
    database = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    cutter = Video_cutter()
    cut_handler = Cut_handler(database=database, cutter=cutter)
    return cut_handler.cut(request=request)

@app.post('/download')
def download_video(request : Download_request):
    database : Minio_handler = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    download_handler = Download_handler(database=database)
    return download_handler.download(request=request)
    
    

@app.post('/upload')
def upload_video(file : UploadFile = File(...)):
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    file_path = f"./tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    database : Minio_handler = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    database.insert(file_path, file.filename)
    return {"filename" : file.filename}

@app.delete('/delete_video')
def delete_video(video_name : str = None):
    if video_name == None:
        raise HTTPException(status_code=422, detail=f'Missing video_name parameter')
    database : Minio_handler = Minio_handler(minio_url=f"{DATABASE_ENDPOINT}:{DATABASE_PORT}",
                            minio_usr=DATABASE_USR,
                            minio_passwd=DATABASE_PASSWD,
                            default_bucket=DATABASE_BUCKET_NAME)
    try:
        database.remove(video_name)
        return {'Seu vídeo foi removido'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao deletar o vídeo:{str(e)}')


if __name__ == '__main__':
    if 'OUTPUT_MOUNT_PATH' in os.environ:
        output_mount_path = os.environ['OUTPUT_MOUNT_PATH']
    else:
        raise Exception('No output mount point indicated!')
    
    if 'REENCODE_CODEC' not in os.environ:
        raise Exception('No reencode codec provided!')
    
    uvicorn.run(app, host='0.0.0.0', port=7000)